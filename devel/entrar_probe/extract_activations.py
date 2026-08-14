#!/usr/bin/env python3
"""
Extract per-layer residual-stream hidden states, at a target entity's token
position, across a set of labeled sentences -- the layer-level counterpart to
the Ollama-only tests in resource/docs/03-b3-attention-as-guardrail.md Sec 6.

Ollama's HTTP API only exposes one pooled vector per input (see the coarse
embedding test); this script goes underneath that, to the actual per-layer,
per-token hidden states, which is what the paper's "role-filler recoverability"
and "interference under superposition" metrics (Discussion 3 Sec 5a) need.

Runs on CPU or GPU without changes -- device and dtype are auto-selected.
On this dev machine (no GPU) use a small model to validate the pipeline; on
a GPU machine, point --model at one of the actual 7-8B models (see README.md
for the Ollama-tag -> HF-repo-id mapping).

Usage:
    python extract_activations.py \
        --model Qwen/Qwen2.5-0.5B-Instruct \
        --data data/sentences.json \
        --out out/activations_qwen0.5b.npz
"""
import argparse
import json
import sys

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def pick_device_dtype(requested_device: str, requested_dtype: str):
    if requested_device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = requested_device

    if requested_dtype == "auto":
        dtype = torch.bfloat16 if device == "cuda" else torch.float32
    else:
        dtype = {"float32": torch.float32, "float16": torch.float16, "bfloat16": torch.bfloat16}[requested_dtype]

    return device, dtype


def find_target_token_span(tokenizer, text: str, target_surface: str, encoding):
    """Map a substring of the raw sentence to the token indices that cover it,
    using the fast tokenizer's character offset mapping. Returns (start, end)
    token indices (end exclusive). Uses the LAST occurrence of target_surface
    deliberately: in a causal decoder a token can only attend to what precedes
    it, so a sentence-initial mention can never reflect role content that
    follows it -- only a later re-mention can. Raises if the substring isn't
    found or the tokenizer has no offset mapping (slow tokenizer)."""
    char_start = text.rfind(target_surface)
    if char_start == -1:
        raise ValueError(f"target_surface {target_surface!r} not found in text {text!r}")
    char_end = char_start + len(target_surface)

    offsets = encoding["offset_mapping"][0].tolist()
    tok_indices = [
        i for i, (s, e) in enumerate(offsets)
        if s < char_end and e > char_start and not (s == 0 and e == 0)
    ]
    if not tok_indices:
        raise ValueError(f"no tokens matched span ({char_start},{char_end}) for {target_surface!r} in {text!r}")
    return min(tok_indices), max(tok_indices) + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="HF model repo id, e.g. Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--data", default="data/sentences.json")
    ap.add_argument("--out", required=True, help="output .npz path")
    ap.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    ap.add_argument("--dtype", default="auto", choices=["auto", "float32", "float16", "bfloat16"])
    ap.add_argument("--load-in-4bit", action="store_true",
                     help="quantize with bitsandbytes (GPU only, needed for large models like aya:35b)")
    args = ap.parse_args()

    device, dtype = pick_device_dtype(args.device, args.dtype)
    print(f"[extract] model={args.model} device={device} dtype={dtype}", file=sys.stderr)

    with open(args.data) as f:
        sentences = json.load(f)["sentences"]

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    if not tokenizer.is_fast:
        raise SystemExit("This script needs a fast tokenizer (for offset_mapping). "
                          "Most HF causal LMs ship one; pass a different --model if not.")

    model_kwargs = dict(torch_dtype=dtype, output_hidden_states=True)
    if args.load_in_4bit:
        from transformers import BitsAndBytesConfig
        model_kwargs["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True)
        model_kwargs.pop("torch_dtype", None)

    model = AutoModelForCausalLM.from_pretrained(args.model, **model_kwargs)
    if not args.load_in_4bit:
        model = model.to(device)
    model.eval()

    per_sentence = {}  # id -> {layer_idx: np.array[hidden]}
    manifest = []

    with torch.no_grad():
        for s in sentences:
            text, target = s["text"], s["name"]
            encoding = tokenizer(text, return_tensors="pt", return_offsets_mapping=True)
            offset_mapping = encoding.pop("offset_mapping")
            start, end = find_target_token_span(
                tokenizer, text, target, {"offset_mapping": offset_mapping}
            )

            inputs = {k: v.to(device) for k, v in encoding.items()}
            out = model(**inputs)
            # hidden_states: tuple of (num_layers + 1) tensors, each [1, seq, hidden]
            # index 0 is the embedding layer output, before any transformer block.
            layer_vecs = []
            for layer_hidden in out.hidden_states:
                span_vec = layer_hidden[0, start:end, :].mean(dim=0)  # mean over sub-word pieces
                layer_vecs.append(span_vec.float().cpu().numpy())

            per_sentence[s["id"]] = np.stack(layer_vecs)  # [num_layers+1, hidden]
            manifest.append({"id": s["id"], "label": s["label"], "name": s["name"],
                              "container": s["container"], "text": text,
                              "token_span": [start, end]})
            print(f"  {s['id']:>10}  {text:<30} tokens[{start}:{end}] -> "
                  f"{tokenizer.convert_ids_to_tokens(encoding['input_ids'][0][start:end])}",
                  file=sys.stderr)

    np.savez(args.out, manifest=json.dumps(manifest), **per_sentence)
    print(f"[extract] wrote {args.out} ({len(per_sentence)} sentences, "
          f"{next(iter(per_sentence.values())).shape[0]} layers, "
          f"{next(iter(per_sentence.values())).shape[1]}-dim)", file=sys.stderr)


if __name__ == "__main__":
    main()
