# Discussion 2 — Toward an Implementation: Sentence Scale and the Neurosymbolic Premise

**Status:** exploratory sketch, not a design decision. The point of this document is to lay out
*options*, mapped onto the vocabulary built up in
[Discussion 1](01-four-perspectives-and-dynamic-paradigm.md), not to commit to one.

**Date:** 2026-08-13

**Two questions on the table, from the user directly:**

1. `dynamic_schemas_proposal.md`'s instance layer is scoped to one LU's own multiple groundings
   (the *entrar* case: one token shared across `PROCESS` and `CONTAINER`). It needs to extend to
   a whole sentence — and, for the image modality, the analogue of an "LU" is a tagged region of
   an image.
2. No project today can avoid using LLMs. That's a **premise**, not a decision point: this project
   is, whatever else it turns out to be, **neurosymbolic**. How the mix actually works is open.

---

## Part A — From one LU to a sentence (and a scene)

### A.1 What already generalizes for free

The `entrar` walkthrough already established the key move: instances are drawn from **one shared
pool per construal**, not one pool per grounding edge. Nothing about that pooling is specific to
"one word's own two groundings" — it's already stated in terms of a construal, and a sentence is
just a bigger construal. The type layer (schemas, microframes, coercion checks) doesn't need to
change at all to scale up; what's missing is *what proposes candidate sharing between tokens that
belong to different evoking elements*, and *what decides whether a proposed sharing actually
holds*.

### A.2 The two things a sentence-level extension needs

**1. Candidate cross-element bindings.** Within one LU, which tokens *could* be shared was easy —
both edges belong to the same frame's own grounding, so the frame elements themselves say what
lines up (`Tema` bound in both edges → one token). Across two different words in a sentence,
nothing currently proposes "the `Buyer` this verb profiles and the entity this noun denotes might
be the same token." Something has to generate that candidate — this is a natural place for the
LLM to contribute (Part B.1 below): treat it as a *candidate generator*, not a *decision-maker*.

**2. A settling procedure that accepts or rejects candidates.** Once candidates exist, something
has to decide which actually hold, given that binding is typed (§4.4 of the proposal already
checks coercion-compatibility for a single instance against its element's target). Three existing
templates for "settling," from the literature scan in Discussion 1, differ in how principled vs.
how cheap they are:

| Template | What it does | Fit here |
|---|---|---|
| **Harmonic Grammar** (Smolensky & Legendre) | maximize a global "Harmony" function over constraint violations; the grammatical parse *is* the equilibrium | closest existing account of "many local forces settle to one global structure" — but needs a numeric Harmony function defined over schema/microframe constraints, which doesn't exist yet |
| **Dynamic Neural Fields** (2024 lexical-meaning model) | continuous activation competes and stabilizes under recurrent, context-driven modulation | good model for *within-word* sense competition; less obviously suited to *discrete* structural decisions like "is this token shared or not" |
| **Transformer self-attention as interacting particles** | tokens cluster toward stable configurations through iterated, weighted interaction | closest to what's actually available off-the-shelf (attention already computes pairwise token affinities) — but uninterpreted; see Part B.3 |

None of these is a drop-in answer. The honest state: the *type layer* (structure) and the
*single-construal instance mechanism* (process, for one grounding) are worked out; the *settling
procedure across multiple evoking elements* is the actual open research problem this whole line
of work reduces to. Worth treating that as the central implementation question rather than a
detail to fill in later.

### A.3 The image case is not a separate problem

`introduction.md` (conceptual dimension) already treats a lexical unit as *one kind of evoking
element* among several — images, gestures, deixis all evoke schemas too, and a word can recur
across sentences the way an image region cannot recur across photographs. That distinction is
already the right shape for this extension: nothing about "candidate binding + settling" is
lexicon-specific. A tagged image region is exactly a second kind of evoking element feeding the
same shared instance pool, with its own frame/schema grounding.

This also isn't unprecedented as an engineering target — **Visual Semantic Role Labeling (vSRL)**
already does "map a frame role (agent, patient, instrument) to a specific image region," and
**GLIP**-style models already do word-region alignment (extending CLIP's whole-image/whole-text
matching down to a region/phrase level). Those give a concrete, working precedent for the
candidate-generation half of A.2 in the image case — a vision-language model proposing
region-to-role candidates — with the same symbolic settling/checking layer from A.2 sitting
downstream of it, unmodified in kind from the text case.

---

## Part B — The neurosymbolic premise

### B.1 LLM as candidate generator, symbolic layer as checker

The lowest-risk pattern, and the one with the most mature tooling *right now* (2025): the LLM
proposes structure, and a formal grammar or symbolic checker filters what it's allowed to output
or accepts/rejects/repairs it after the fact.

- **Grammar-Constrained Decoding (GCD)** — logit-masking during generation so the LLM can only
  emit tokens that keep its output inside a formal grammar, actively developed in 2025
  ([ACL 2025](https://aclanthology.org/2025.acl-industry.34/),
  [flexible/efficient GCD, Feb 2025](https://arxiv.org/pdf/2502.05111)). Directly applicable: the
  schema/microframe layer's own coercion rules could plausibly *be* that grammar, constraining an
  LLM to only ever propose typeable bindings in the first place.
  - **Caveat found in the same scan, worth taking seriously:** strict GCD is reported to disrupt
    an LLM's own autoregressive chain-of-thought reasoning — hence proposals for a "dual-phase
    cascaded" split (let the LLM reason freely, then lift the result into the grammar
    afterward) rather than constraining every generated token in-line. That tradeoff — constrain
    while generating vs. generate freely then check/repair — is a real design fork, not just an
    implementation detail.
- **LLM → symbolic solver verification** — the LLM translates natural language into a symbolic
  representation, which an external checker verifies. Maps directly onto this framework: LLM
  produces a candidate `Grounded_in` binding + profile, the schema layer's existing conformance
  check (§4.4 of the proposal) accepts or flags it.
- **CCG-lifting** (2025) — a concrete example of exactly this shape done for grammar specifically:
  take free-form LLM output and *lift* it into a compositional (Combinatory Categorial Grammar)
  structure after generation, rather than constraining generation itself.

**Why this is the natural first move:** it requires no change to the type layer or the instance
mechanism already designed. The LLM sits entirely outside both, as a source of candidates and,
optionally, a target for post-hoc checking.

### B.2 LLM embeddings as fillers, schema roles as the binding structure

This resolves an open question `dynamic_schemas_proposal.md` left genuinely unanswered (§4.5):
*"what does an atomic REGION instance actually point at outside the simulation — an annotation
span, an LU token, or does it stay an uninterpreted bookkeeping identity?"* **Tensor Product
Representations** (Smolensky, 1990 — the same person behind Harmonic Grammar, not a coincidental
second citation) answer exactly this shape of question in general: a structured object is encoded
as the superposition of **role ⊗ filler** bindings, where roles are symbolic slots (here:
`Agonist`, `Antagonist`, `Ground`, `Interior`, …) and fillers are vectors. If a `REGION` instance's
filler is an LLM (or vision-language model) embedding of the actual token/region it points at,
every instance gets a real vector-space payload instead of staying bare bookkeeping identity —
and the type layer's roles are exactly what already exists (schema elements). **Vector Symbolic
Architectures / Holographic Reduced Representations** are the same idea with a different binding
operator (circular convolution instead of outer product) and are the actively-developed 2024
successor line if TPR's outer product turns out to be too expensive dimensionally.

This is the theoretically cleanest fit of the three patterns here, because it doesn't just bolt an
LLM onto the framework — it answers a question the framework already had open, using a mechanism
from the same intellectual lineage (Smolensky) that Harmonic Grammar already put on the table in
Discussion 1.

### B.3 LLM attention itself as (part of) the settling dynamics

The most speculative and most ambitious option, and the one that most directly follows from
Discussion 1's finding that self-attention *already is* a dynamical system of interacting
token-particles that cluster toward stable states. Rather than treating the LLM purely as an
external proposal generator (B.1) or embedding source (B.2), this option treats attention's own
settling behavior as a first draft of the cross-word settling procedure Part A.2 needs — with
schema/microframe constraints injected as a bias or mask on attention, so the configurations it
settles into are type-checked concept instances rather than uninterpreted geometric clusters. This
is the option that would make the LLM genuinely part of *process* rather than a separate module
feeding into it — but there's no existing worked example of this to point to (the transformer-
clustering papers describe what attention does, not how to constrain it toward externally-typed
structure), so it belongs on the far end of the risk spectrum, not as a starting point.

### B.4 A fourth, narrower pattern worth knowing about

**KG–LLM fusion techniques** (2025, e.g. relational tokens that let a knowledge graph "speak" in
an LLM's own semantic space) are relevant less as a mechanism for A.2's settling problem and more
for a narrower, later need: once the schema/microframe graph is large, querying or extending it
*through* an LLM (disambiguation, coverage-checking, semi-automated candidate schemas) will likely
want some version of this. Flagged for later, not a near-term concern.

---

## B.5 Where this leaves the mix

Not a decision, but a rough shape:

- **B.1 (generate-then-check)** is the pragmatic entry point — existing tooling, no redesign of
  the type or instance layers required, and it's exactly what's needed to bootstrap candidate
  cross-word bindings for Part A's settling problem.
- **B.2 (TPR/VSA fillers)** is the theoretically motivated piece — it answers an already-open
  question in the existing framework rather than adding a new one, and shares its intellectual
  lineage with Harmonic Grammar, so it isn't a foreign graft.
- **B.3 (attention as settling)** is the long-run, high-risk direction that would make the
  "dynamical, not mechanical" paradigm argument from Discussion 1 literally true at the
  implementation level, rather than true by analogy — worth keeping as the target to aim at, not
  something to attempt first.

## Open threads for next discussion

1. Define what a Harmony-style (or equivalent) objective function would even look like over
   schema/microframe constraints — this is the missing piece A.2's settling procedure needs no
   matter which of B.1–B.3 supplies the candidates.
2. Decide the in-line-constrain vs. generate-then-lift fork from B.1 — it changes how much of the
   pipeline touches the LLM's own decoding loop versus stays entirely downstream of it.
3. Prototype B.2 on a single already-worked case (*entrar*, since it's already traced end to end
   in the proposal) — bind its known elements to real embeddings and see whether anything breaks
   before trying it on a full sentence.
4. Revisit vSRL/GLIP more closely once the text-side candidate-generation approach is chosen, to
   check whether the same mechanism actually transfers to the image case or only rhymes with it.
