#!/usr/bin/env python3
"""
Analyze activations extracted by extract_activations.py.

Two things, per layer:

1. Cosine-similarity geometry between the four conditions (antagonist_only,
   interior_only, blend, neutral) -- the layer-resolved, entity-resolved
   counterpart to the pooled-sentence embedding test that came back
   uninformative (resource/docs conversation, Ollama /api/embed test).

2. Role-filler recoverability, adapted from the paper's own metric
   (resource/docs/03-b3-attention-as-guardrail.md Sec 5a): fit two
   INDEPENDENT one-vs-rest linear probes per layer, each trained only on
   the three PURE conditions (antagonist_only, interior_only, neutral) --
     is_antagonist: antagonist_only (1) vs {interior_only, neutral} (0)
     is_interior:   interior_only (1)   vs {antagonist_only, neutral} (0)
   `blend` is held out of training entirely for both probes. If the
   entrar-style shared-token binding is really encoded, both probes should
   fire positive on blend at the same layer(s) -- the token behaving as if
   it carries both bindings at once. `neutral` (also held out) is a sanity
   check: both probes should fire negative on it.

   Earlier version of this script trained is_antagonist and is_interior on
   the SAME two classes with flipped labels -- that makes them near-mirror
   complements by construction, so "both positive" was mathematically
   impossible to observe regardless of what the model actually encodes.
   Fixed here by giving each probe its own, different negative set.

   Also reports a permutation-test null baseline per layer: with ~900+
   hidden dims and only 6-18 training examples, a linear probe can often
   separate even RANDOMLY shuffled labels by chance (curse of
   dimensionality). Real accuracy is only evidence of something if it
   clears the shuffled-label distribution, not just chance-level 0.5.
"""
import argparse
import json

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import LeaveOneOut

N_PERMUTATIONS = 50  # LOO-CV x permutations x layers x 2 probes gets expensive fast; raise for a final run
RNG_SEED = 0


def load(npz_path):
    data = np.load(npz_path, allow_pickle=True)
    manifest = json.loads(str(data["manifest"]))
    acts = {m["id"]: data[m["id"]] for m in manifest}  # id -> [layers, hidden]
    return manifest, acts


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def class_centroid_geometry(manifest, acts, num_layers):
    labels = ["antagonist_only", "interior_only", "blend", "neutral"]
    by_label = {l: [] for l in labels}
    for m in manifest:
        by_label[m["label"]].append(acts[m["id"]])

    print("\n=== Class-centroid cosine similarity, per layer ===")
    print(f"{'layer':>5}  {'ant~int':>8}  {'ant~blend':>10}  {'int~blend':>10}  "
          f"{'blend~neu':>10}  {'ant~neu':>8}  {'int~neu':>8}")
    for layer in range(num_layers):
        c = {l: np.mean([a[layer] for a in by_label[l]], axis=0) for l in labels}
        print(f"{layer:>5}  "
              f"{cosine(c['antagonist_only'], c['interior_only']):>8.4f}  "
              f"{cosine(c['antagonist_only'], c['blend']):>10.4f}  "
              f"{cosine(c['interior_only'], c['blend']):>10.4f}  "
              f"{cosine(c['blend'], c['neutral']):>10.4f}  "
              f"{cosine(c['antagonist_only'], c['neutral']):>8.4f}  "
              f"{cosine(c['interior_only'], c['neutral']):>8.4f}")


def loo_cv_accuracy(X, y):
    loo = LeaveOneOut()
    correct = 0
    for train_idx, test_idx in loo.split(X):
        clf = LogisticRegression(max_iter=2000).fit(X[train_idx], y[train_idx])
        pred = clf.predict(X[test_idx])
        correct += int(pred[0] == y[test_idx][0])
    return correct / len(y)


def permutation_null(X, y, rng, n_perm=N_PERMUTATIONS):
    accs = np.empty(n_perm)
    for i in range(n_perm):
        y_shuf = rng.permutation(y)
        accs[i] = loo_cv_accuracy(X, y_shuf)
    return accs


def recoverability_probe(manifest, acts, num_layers):
    ids = {label: [m["id"] for m in manifest if m["label"] == label]
           for label in ["antagonist_only", "interior_only", "blend", "neutral"]}
    rng = np.random.default_rng(RNG_SEED)

    print("\n=== Role-filler recoverability probes, per layer ===")
    print("(each probe trained ONLY on its two pure/neutral classes; blend and the")
    print(" other pure class's own held-out points are never seen during training;")
    print(f" null = mean/95th-pct LOO-CV accuracy over {N_PERMUTATIONS} label-shuffles,")
    print(" same data -- real accuracy should clear this before it means anything)")
    header = (f"{'layer':>5}  {'is_ant acc':>10} {'(null)':>13}  {'is_int acc':>10} {'(null)':>13}  "
              f"{'blend:ant':>9}  {'blend:int':>9}  {'blend:BOTH':>10}  {'neu:ant':>7}  {'neu:int':>7}")
    print(header)

    for layer in range(num_layers):
        X_ant = np.stack([acts[i][layer] for i in ids["antagonist_only"]])
        X_int = np.stack([acts[i][layer] for i in ids["interior_only"]])
        X_neu = np.stack([acts[i][layer] for i in ids["neutral"]])
        X_blend = np.stack([acts[i][layer] for i in ids["blend"]])

        # is_antagonist: antagonist_only (1) vs {interior_only, neutral} (0)
        Xa = np.vstack([X_ant, X_int, X_neu])
        ya = np.array([1] * len(X_ant) + [0] * (len(X_int) + len(X_neu)))
        acc_a = loo_cv_accuracy(Xa, ya)
        null_a = permutation_null(Xa, ya, rng)
        clf_a = LogisticRegression(max_iter=2000).fit(Xa, ya)

        # is_interior: interior_only (1) vs {antagonist_only, neutral} (0)
        Xi = np.vstack([X_int, X_ant, X_neu])
        yi = np.array([1] * len(X_int) + [0] * (len(X_ant) + len(X_neu)))
        acc_i = loo_cv_accuracy(Xi, yi)
        null_i = permutation_null(Xi, yi, rng)
        clf_i = LogisticRegression(max_iter=2000).fit(Xi, yi)

        blend_pred_a = clf_a.predict(X_blend)
        blend_pred_i = clf_i.predict(X_blend)
        neu_pred_a = clf_a.predict(X_neu)
        neu_pred_i = clf_i.predict(X_neu)

        pct_ant_pos = 100 * blend_pred_a.mean()
        pct_int_pos = 100 * blend_pred_i.mean()
        pct_both_pos = 100 * np.mean((blend_pred_a == 1) & (blend_pred_i == 1))
        pct_neu_ant_pos = 100 * neu_pred_a.mean()
        pct_neu_int_pos = 100 * neu_pred_i.mean()

        print(f"{layer:>5}  {acc_a:>10.2f} "
              f"(mu={null_a.mean():.2f} p95={np.percentile(null_a, 95):.2f})  "
              f"{acc_i:>10.2f} "
              f"(mu={null_i.mean():.2f} p95={np.percentile(null_i, 95):.2f})  "
              f"{pct_ant_pos:>9.1f}  {pct_int_pos:>9.1f}  {pct_both_pos:>10.1f}  "
              f"{pct_neu_ant_pos:>7.1f}  {pct_neu_int_pos:>7.1f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("activations_npz")
    args = ap.parse_args()

    manifest, acts = load(args.activations_npz)
    num_layers = next(iter(acts.values())).shape[0]
    print(f"Loaded {len(manifest)} sentences, {num_layers} layers "
          f"(layer 0 = embeddings, layer {num_layers - 1} = final)")

    class_centroid_geometry(manifest, acts, num_layers)
    recoverability_probe(manifest, acts, num_layers)


if __name__ == "__main__":
    main()
