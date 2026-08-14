# Discussion 4 — Graph Attention/Message-Passing as an Explicit Alternative to Probing Attention

**Status:** exploratory notes, not a settled position. Continues from
[Discussion 2](02-implementation-sketch-sentence-scale-and-neurosymbolic.md)'s Part A.2 (the
sentence-level "settling procedure" that decides which candidate cross-word bindings hold) and
[Discussion 3](03-b3-attention-as-guardrail.md)'s B.3 (attention-as-settling inside a pretrained
LLM). Discussion paused here to be picked up later, not closed.

**Date:** 2026-08-13

**Question on the table, from the user:** the conceptual framework — the type layer (schemas,
microframes) plus the lexical frames attached to it — is already, structurally, a **graph**. Given
that, shouldn't architectures built *for* graphs — Graph Attention Networks (GAT) specifically —
be considered as a candidate mechanism, alongside or instead of probing a token-sequence
transformer's implicit attention (B.3)?

---

## 1. Why the fit is natural

Discussion 2's Part A.2 laid out three existing "settling" templates (Harmonic Grammar, Dynamic
Neural Fields, transformer self-attention-as-interacting-particles) and judged none a drop-in
answer. All three share one property worth naming explicitly: none of them are handed a graph.
Harmonic Grammar's constraints, DNF's activation field, and a transformer's self-attention all
have to *discover* which elements relate to which, over a domain (a constraint set, a continuous
field, a token sequence) that doesn't itself encode structure going in. That's precisely why B.3
(Discussion 3) is the risky option — it means going looking for role–filler structure *hidden*
inside a mechanism that was never told the roles exist, entangled with everything else a
pretrained LLM's attention is simultaneously doing (syntax, coreference, world knowledge).

A graph-native architecture inverts that: the structure — nodes and candidate edges — is an
**input**, not something to be discovered. Given that the framework's own type layer (schema
graph, microframe relations) and instance layer (`dynamic_schemas_proposal.md`) are already
graph-shaped by construction, this isn't importing a foreign representation to fit the problem —
it's matching the architecture to the shape the problem already has. The "Attention as Binding"
paper cited in Discussion 3 makes the same point from the comparison side without pursuing it:
its own Table 1 lists TPRs/GNNs as a separate framework column from transformers, crediting graph
approaches with "very explicit structure... strong inductive bias for relational reasoning; often
highly interpretable," against "graph/program structure may be hard to induce from raw data" as
the cost. That cost is exactly what this project *doesn't* pay here — the graph (schema/microframe
types, frame elements) already exists; it doesn't need to be induced.

## 2. First refinement: this is a heterogeneous graph, not a plain GAT

The user's proposal — type nodes and token nodes, with tokens linked to the types they could
instantiate — has (at least) two distinct node kinds and, implicitly, at least two distinct edge
kinds (token↔type edges vs. the type layer's own internal structural edges, e.g. a microframe's
`Interior`/`Exterior` relation). Plain GAT (Veličković et al. 2018) assumes a **homogeneous**
graph — one node type, one edge type, one shared attention function. That's the wrong tool for a
graph with structurally different kinds of nodes and relations.

The right family is **heterogeneous graph neural networks** — Relational GCN (R-GCN, Schlichtkrull
et al. 2018), which assigns a separate learned transformation per edge *type* rather than one
shared weight matrix, and Heterogeneous Graph Attention Networks (HAN, Wang et al. 2019), which
does the same with GAT-style learned attention instead of fixed aggregation. "GAT" in what
follows should be read as shorthand for "GAT-style attention inside a heterogeneous
message-passing architecture," not literal vanilla GAT.

## 3. Second refinement: message passing as spreading activation, made precise

The user's intuition that this "resembles spreading activation" is correct, and it's a real
architectural correspondence, not a loose analogy. Spreading activation (Collins & Loftus 1975 —
already the foundational citation in
[Discussion 1](01-four-perspectives-and-dynamic-paradigm.md#41-historical-precedent-1980s90s--spreading-activation-connectionist-parsing)'s
literature scan) is: each node holds an activation value; at each step, activation flows to
neighbors weighted by (typically fixed) edge strength; each node sums its incoming activation and
updates. That *is* the general message-passing update rule (Gilmer et al. 2017's MPNN
formalization: aggregate incoming messages, then update node state) with a specific, simple
choice of message and aggregation function.

GAT is the natural generalization of that specific choice: instead of a fixed edge weight, it
**learns** a content-dependent compatibility function between the two nodes' current features to
set the weight per-input, then softmax-normalizes over a node's neighbors — the same
content-addressed character Discussion 1 §4.4 already found in transformer self-attention, but
computed only over edges that exist in the graph rather than over every pair in a sequence. This
sharpens (not just repeats) Discussion 1's point about attention being a modern, differentiable
descendant of spreading activation: on an explicit graph, that descent relationship is exact, not
metaphorical.

## 4. Correction: stacking GAT layers is not the same as settling to equilibrium

Here the user's framing needs a real correction. A standard GAT (or HAN/R-GCN) with *L* layers
propagates information exactly *L* hops and then stops — it's **bounded local propagation**, not
a dynamical system settling to a fixed point. Nothing about stacking a handful of graph-attention
layers guarantees an equilibrium in the sense Discussion 1's Harmonic Grammar comparison wants
("the grammatical parse *is* the equilibrium state").

Two existing mechanisms get genuine equilibrium-seeking behavior instead:

- **Implicit / equilibrium graph neural networks** (Gu et al. 2020, *IGNN*) — tie the same layer's
  weights across all "steps" and solve for the **fixed point** of that layer function directly
  (via root-finding), rather than applying a fixed number of distinct layers. This is the graph
  analogue of Deep Equilibrium Models. Depth becomes "iterate until it stops changing," which is
  what "settling" actually means.
- **Graph Neural Diffusion** (GRAND, Chamberlain et al. 2021) — reframes message passing itself as
  a discretization of a diffusion PDE on the graph, which provably evolves toward a steady state.
  This is the closer of the two to Harmonic Grammar's own framing, because it casts the dynamics
  explicitly as flowing toward a minimum of an implicit energy functional on the graph — i.e. it's
  the graph-native version of exactly the "many local forces settle to one global structure" idea
  Discussion 1 flagged Harmonic Grammar as the strongest existing precedent for, just instantiated
  over an explicit graph instead of a constraint-satisfaction network.

If "settling to the most probable final graph" is the actual target, GRAND (or IGNN) is the
mechanism to reach for — plain stacked GAT layers only get part of the way there.

## 5. Correction: attention reweights edges, it doesn't decide which edges exist

A second gap between the proposal and what GAT-style attention actually computes. Attention
weights — in a transformer or in GAT — are a **soft reweighting of messages over edges that
already exist**. They don't add or remove edges from the graph. "Computes the most probable final
graph" implies a discrete structural decision: which of the *candidate* token↔instance or
instance↔instance bindings actually hold. That's precisely Discussion 2 Part A.2's "settling
procedure that accepts or rejects candidates" — a different, harder problem than reweighting.

The closer existing precedent for that specific problem is **Neural Relational Inference** (NRI,
Kipf et al. 2018): given observed node behavior, it infers *which* edges of an interaction graph
exist at all, using a discrete latent-variable model over edge type/presence, trained end-to-end.
If the goal is genuinely "given candidate bindings, decide which survive," NRI-style discrete
structure inference is the more accurate target than GAT attention alone — GAT (or its
heterogeneous cousins) could still supply the *reweighting* that biases which candidates are more
or less likely to be accepted, with a discrete decision layered on top, rather than either
mechanism doing the whole job alone.

## 6. Refinement to the node design: three tiers, not two

A plain token↔type bipartite graph slightly flattens a distinction `dynamic_schemas_proposal.md`
already insists on, and which Discussion 1 already identified as the *process* layer specifically
(§2 there): **type**, **instance**, and **token** are three separate things, not two. An instance
has its own identity, distinct from the type it instantiates, and — critically — the *entrar*
worked example (§4.6 of the proposal, already traced in Discussion 1 §2 and Discussion 3 §6) only
works because a single token (`r_joão`) can ground **two different instances at once**
(`PROCESS.Antagonist` and `CONTAINER.Interior`). A direct token→type edge can't represent that: it
collapses "the token" and "the thing that gets bound to a role" into one node, when the whole point
of the instance layer is that they're not the same node.

The graph this architecture should actually operate over has three node kinds:

```
token --(grounds)--> instance --(is-of)--> type
```

with **instance↔instance edges** — not token↔token or token↔type edges — as what actually gets
proposed as a candidate binding and accepted or rejected during settling (e.g. two instances
sharing the same `Tema` role, as in Discussion 1's original single-LU case, now generalized across
words). This keeps a single token free to anchor multiple simultaneous instance nodes, which is
required for *entrar* and is presumably the norm, not the exception, once this scales past one
word to a whole sentence.

## 7. Updating Discussion 2's settling-template table

Discussion 2 Part A.2 listed three templates and judged none a drop-in fit. Worth adding a fourth,
now that this discussion has worked through it:

| Template | What it does | Fit here |
|---|---|---|
| **Harmonic Grammar** | maximize a global Harmony function over constraint violations | closest *conceptual* precedent; no existing Harmony function over schema/microframe constraints |
| **Dynamic Neural Fields** | continuous activation competes and stabilizes under recurrent modulation | good for within-word sense competition, not obviously suited to discrete structural decisions |
| **Transformer self-attention** | tokens cluster via iterated pairwise interaction | available off-the-shelf, but the graph is implicit/hidden, entangled with everything else attention does (B.3's risk) |
| **Graph message passing (GAT/HAN + GRAND/NRI)** | attention-weighted propagation over an *explicit* candidate graph, run to a fixed point (GRAND/IGNN) with discrete edge decisions (NRI) | the graph is given, not discovered — directly matches the type/instance/token structure already designed; lower risk than probing a pretrained LLM, but needs the candidate graph supplied from elsewhere first |

## 8. Where this leaves things relative to B.1–B.3

This isn't a competitor to Discussion 2's B.1–B.4 taxonomy — that taxonomy is about *how an LLM
participates*; this is about what actually runs the **settling** step once candidates exist,
which every one of B.1–B.3 still needs regardless of how candidates get generated. Concretely:

- The **candidate generation** half of Part A.2 is unchanged — something still has to propose
  "this instance and that instance might share a token," and an LLM (B.1's role) or a
  vision-language model (for the image case, Part A.3) is still the natural source of that
  proposal. A graph architecture doesn't remove that step; it consumes its output as the
  candidate edge set.
- What this discussion changes is where the **risk** sits for getting genuine settling dynamics.
  B.3 bet on finding binding structure already present, unlabeled, inside a pretrained
  transformer's dense attention. Building a heterogeneous graph-attention/diffusion architecture
  directly over the type/instance/token graph is a *build it*, not *find it*, move — closer in
  risk profile to B.1/B.2 (you design the mechanism) while still getting the attention-based,
  differentiable, potentially-equilibrium-seeking dynamics that made B.3 attractive in the first
  place. It's a way to de-risk B.3's ambition without giving up on the "genuine settling dynamics"
  goal.

## 9. Open threads for next discussion

1. Decide whether GAT-style reweighting (bias which candidates are likely) and NRI-style discrete
   inference (decide which candidates hold) are both needed as separate stages, or whether one
   subsumes the other for this problem.
2. Look more closely at GRAND (graph neural diffusion) specifically for whether a Harmony-style
   objective *can* be defined directly over schema/microframe legality as its implicit energy
   functional — this would answer Discussion 2's still-open "what would a Harmony function even
   look like here" question, on a graph instead of an unstructured constraint set.
3. Work out the three-tier token/instance/type graph concretely for *entrar*, as prep for the
   probing work already queued in [Discussion 3](03-b3-attention-as-guardrail.md#6-next-session) —
   the two lines of work (probe a pretrained LLM for hidden directions vs. build an explicit graph
   architecture) are not mutually exclusive and may be worth pursuing as parallel, comparable
   approaches to the same settling problem rather than a forced choice. **Update:** a first pilot
   run of the probing half is in — see §10 below. Pipeline built and validated; small-N tiny-model
   result in hand; real target models still to run on a GPU machine.
4. Check whether the same three-tier graph design transfers to the image case (Part A.3's
   region-as-evoking-element point) without modification, or whether image regions need a fourth
   node kind of their own.
5. Still entirely unstarted: where do the initial candidate edges (token→instance,
   instance→instance) actually come from in practice — this is still B.1's unbuilt constraint
   vocabulary, now doubling as the graph-construction step for whichever settling mechanism runs
   on top of it.

## 10. First empirical data point: the entrar activation probe (2026-08-13, same-day follow-up)

Before this discussion's own two-track suggestion (§9.3 — probe a pretrained model *and* build an
explicit graph, in parallel rather than as a forced choice) could stay purely hypothetical, the
probing half got a first real run, using local Ollama models as a jumping-off point and then going
underneath Ollama's API into actual per-layer residual-stream activations. Full pipeline and
sentence data live in `devel/entrar_probe/` (see its `README.md` for the complete design and how
to rerun on a GPU machine). Two things are worth folding back into this discussion specifically,
rather than just Discussion 3's — because both bear directly on §8's risk argument.

**What was tested.** Whether a single entity token's hidden state — at the same position, across a
controlled set of otherwise-matched sentences — carries a linearly recoverable signal of which
schema role it's playing: `PROCESS.Antagonist` alone, `CONTAINER.Interior` alone, both at once (the
*entrar* blend, matching `dynamic_schemas_proposal.md` §4.6's `r_joão`), or neither (a neutral
property-ascription control). Two independent linear probes (`is_antagonist`, `is_interior`), each
trained only on its own pure/neutral classes, were then scored on the **held-out** blend condition —
does a shared token trigger both probes at once, the way the instance layer's shared-pool design
says it should?

**A methodological finding worth keeping, independent of the result.** The first version of this
experiment reported a completely degenerate signal — cosine similarity of exactly 1.0000 between
every condition at every layer. Tempting to read as "no structure here," but it was a bug specific
to how these models work: the target names were sentence-initial, and a **causal decoder's token
can only attend to what precedes it** — a sentence-initial token's representation is fixed by its
own token id and position alone, structurally unable to reflect a verb or container that comes
*after* it in the sentence, no matter how many layers deep you look. This matters beyond this one
experiment: it's a standing constraint on *any* future attempt to probe or steer a causal LLM's
activations for this framework's role–filler structure (the B.3 line generally, not just this
pilot) — the target token has to be positioned so it can causally attend to the content that
determines its role, e.g. by re-mentioning the entity after the role-defining clause, which is
exactly the fix applied here.

**What the (tiny, 0.5B, CPU-only) smoke-test model actually showed, once fixed.** Real,
permutation-baseline-cleared signal: `is_interior` reached 0.94 leave-one-out CV accuracy by late
layers against a shuffled-label null of ~0.51–0.57 (95th percentile ≈ 0.70–0.81); `is_antagonist`
reached 0.83, clearing its own null less consistently. But on the held-out blend condition, neither
probe fired together — `blend: %BOTH-positive` read 0.0% at nearly every layer. Instead there was a
clean **depth-dependent handoff**: early-to-mid layers classify the blend entity as
`interior`-positive (up to 100%) and `antagonist`-negative; late layers flip to
`antagonist`-positive (up to 100%) and `interior`-negative. The neutral control correctly scored
negative on both probes throughout.

**Why this belongs in Discussion 4, not just Discussion 3.** §8 above frames this whole discussion
as de-risking B.3: building an explicit graph over the type/instance/token structure sidesteps
having to *find* the shared-token binding already sitting, unlabeled, inside a pretrained
transformer. This pilot is a first, small, not-yet-generalizable data point on exactly that
question — and what it found was not a stable superposition (both bindings held at once, which is
what the instance layer's shared-pool design actually requires — `r_joão` is simultaneously bound
to `PROCESS.Antagonist` and `CONTAINER.Interior`, not bound to one and then the other). What it
found instead looks more like a **sequential resolution across depth** than a superposition. If
that pattern held up on the real target models (it hasn't been tested there yet — this was a 0.5B
model chosen only to validate the pipeline on a GPU-less machine, not one of the models the actual
question is about), it would be a concrete point *in favor* of §8's argument: a pretrained
transformer settling on one role reading and then the other, rather than holding both
simultaneously, is a real obstacle for B.3 specifically, and doesn't afflict a graph architecture
built to hold `r_joão` as one instance bound into two roles at once by construction.

**What would actually settle this:** rerunning the identical pipeline against `Qwen2.5-7B-Instruct`
and `CohereForAI/aya-expanse-8b` — the real local-equivalent models, per `devel/entrar_probe/
README.md`'s Ollama-tag-to-HF-repo-id table — on a GPU machine. Scale could change this either way:
a bigger model might hold genuine superposition where a 0.5B one can't, or the same sequential
handoff might persist regardless of scale, which would be the more interesting and more
load-bearing result for this discussion's argument. Not run yet; flagged here rather than assumed.
