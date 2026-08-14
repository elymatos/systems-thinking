# entrar activation probe

Layer-level follow-up to the Ollama-only tests in
`resource/docs/03-b3-attention-as-guardrail.md` Sec 6 and the "entrar" worked example in
`dynamic_schemas_proposal.md` Sec 4.6. Ollama's HTTP API only exposes one pooled vector per
input (`/api/embed`) -- no per-token, no per-layer access -- so it can't test the paper's
actual "role-filler recoverability" / "interference under superposition" metrics (see
`resource/docs/03-b3-attention-as-guardrail.md` Sec 5a). This does, by loading the model
directly with `transformers` and reading `output_hidden_states`.

Written on a machine with no GPU, meant to run for real on one -- see "Running on a GPU
machine" below. Everything here is a **small-N pilot** (6 examples per class): read the
numbers as a first pass, not a powered result.

## What it does

1. `extract_activations.py` -- loads a causal LM, runs a forward pass per sentence, and saves
   the per-layer hidden state at a target entity's token position.
2. `analyze_recoverability.py` -- loads those activations and:
   - reports class-centroid cosine similarity per layer (layer-resolved version of the
     pooled-embedding test that came back uninformative against Ollama);
   - fits two **independent** linear probes per layer (`is_antagonist`, `is_interior`), each
     trained only on its own pure/neutral classes, then scores them on the held-out `blend`
     condition -- does a shared token trigger *both* probes at once, the way
     `dynamic_schemas_proposal.md` Sec 4.6 says `r_joao` should (bound to both
     `PROCESS.Antagonist` and `CONTAINER.Interior`)?
   - reports a permutation-test null baseline (shuffled-label CV accuracy) alongside the real
     accuracy at every layer, because a linear probe with ~900+ dimensions and a dozen
     examples can separate noise by chance -- real accuracy only means something once it
     clears that baseline.

## A non-obvious design point, found the hard way

The first version of the sentence set put the target name at the very start of every
sentence ("João entrou na sala."). That gave exactly 1.0000 cosine similarity between every
condition at every layer -- not a null result, a bug: in a **causal** decoder, a token's
hidden state can only attend to what precedes it. A sentence-initial name is fully determined
by its own token id and position id alone; it structurally cannot reflect the verb or
container that comes after it, no matter how many layers you look at. Fixed by giving every
sentence a second clause reintroducing the same entity (`"...na sala. João sorriu."`) and
extracting at the **second** occurrence, which can attend back across everything in the first
clause. `find_target_token_span` uses `rfind`, not `find`, for exactly this reason.

The probe design had a second, subtler version of the same kind of mistake: the first version
trained `is_antagonist` and `is_interior` on the *same two classes* with the labels flipped,
which makes them near-mirror complements by construction -- `blend: %BOTH-pos` was
guaranteed to read 0.0% regardless of what the model actually encodes. Fixed by adding a
fourth `neutral` class (no PROCESS, no CONTAINER -- a plain property ascription) so each
probe gets its own, differently-composed negative set, and by holding `blend` out of training
for both probes entirely.

## Files

- `data/sentences.json` -- 24 sentences, 4 conditions x 6 name/container pairs
  (`antagonist_only`, `interior_only`, `blend`, `neutral`). Role glosses match
  `conceptual_schemas_catalog.md`'s `PROCESS` and `CONTAINER` entries exactly (`Antagonist` =
  "the entity undergoing change"; `Interior` = "inside the boundary").
- `extract_activations.py` -- model-agnostic; device (`cpu`/`cuda`) and dtype
  (`float32`/`bfloat16`) are auto-selected, so the same command works unmodified on this
  machine or a GPU box.
- `analyze_recoverability.py` -- pure numpy/sklearn, no GPU needed even if the extraction was
  done on one.
- `out/` -- gitignored; extracted `.npz` activations and analysis logs land here.

## Running here (CPU smoke test)

The `fn4.pytorch` conda env already has everything needed (`torch` 2.6.0+cu124 -- a CUDA
build that just runs CPU-only here and will pick up a GPU automatically elsewhere --
`transformers`, `accelerate`, `scikit-learn`, `numpy`). No fresh install required.

```bash
PY=/home/ematos/miniconda3/envs/fn4.pytorch/bin/python
$PY extract_activations.py --model Qwen/Qwen2.5-0.5B-Instruct \
    --data data/sentences.json --out out/activations_qwen0.5b.npz
$PY analyze_recoverability.py out/activations_qwen0.5b.npz
```

`Qwen2.5-0.5B-Instruct` (~1GB) is there to validate the pipeline mechanics on this
memory-constrained, GPU-less machine -- it is **not** one of the models the actual question
is about. Treat any signal from it as "the code works," not as an answer.

## Running on a GPU machine

Point `--model` at the real target instead. These are the HF repo ids matching the models
already pulled locally via Ollama (`ollama:test`), confirmed against Ollama's own
`/api/show` (architecture family, not guessed from the tag name alone):

| Ollama tag | Architecture (`ollama show`) | HF repo id |
|---|---|---|
| `qwen2.5:7b` | `qwen2`, basename `Qwen2.5` | `Qwen/Qwen2.5-7B-Instruct` |
| `aya-expanse:8b` | `command-r`, basename `aya-expanse` | `CohereForAI/aya-expanse-8b` |
| `llama3.1:8b` | (not re-checked here) | `meta-llama/Llama-3.1-8B-Instruct` -- **gated**, needs an approved HF token |
| `aya:35b` | `command-r`, basename unset | most likely `CohereForAI/c4ai-aya-23-35B` (the Aya line at 35B; Aya Expanse tops out at 8B/32B) -- **verify** against the model's own `ollama show aya:35b --modelfile` before trusting this, since the basename field was empty |

Command-R-family models (`aya-expanse`, `aya:35b`) need `transformers` >= 4.44ish for
`CohereForCausalLM` support; the `fn4.pytorch` env's 4.50.1 should cover it, but if loading
fails, upgrade `transformers` first before assuming something else is wrong.

For `aya:35b` specifically, add `--load-in-4bit` (needs `bitsandbytes`, not currently in
`fn4.pytorch` -- `pip install bitsandbytes`) -- 35B in fp16/bf16 is ~70GB, too large for most
single GPUs otherwise.

```bash
python extract_activations.py --model Qwen/Qwen2.5-7B-Instruct \
    --data data/sentences.json --out out/activations_qwen7b.npz
python analyze_recoverability.py out/activations_qwen7b.npz
```

Repeat per model to compare -- the Ollama-only behavioral test (Discussion 3 conversation)
already found `qwen2.5:7b` and `aya-expanse:8b` disagreed with each other at the behavioral
level, so it's worth checking whether that disagreement shows up here too, or only at the
surface/generation level.

Once on a GPU, it's also worth raising `N_PERMUTATIONS` in `analyze_recoverability.py` back
up from 50 (lowered here only because CPU-bound LOO-CV x permutations x 25 layers x 2 probes
was too slow to smoke-test against) -- 200+ gives a tighter null-distribution estimate.

## Open next steps (not yet done here)

- The "alignment with VSA operators" metric from the paper (Discussion 3 Sec 5a) --
  fitting a binding operator, e.g. circular convolution, to a head's actual behavior -- isn't
  implemented yet; this only covers role-filler recoverability and a crude version of
  interference (the `blend` condition itself, one binding pair; true "interference under
  superposition" would need sentences with *more* than two simultaneous bindings to see where
  recovery degrades as more gets packed into one residual stream).
- Everything here probes one hand-picked token position per sentence. Attention-pattern-level
  analysis (which heads actually move information from the role-defining clause to the
  second mention) is a natural follow-on once/if a layer shows a real, permutation-cleared
  signal -- no point chasing attention patterns before confirming there's something at the
  representation level to explain.
