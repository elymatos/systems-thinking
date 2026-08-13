# Discussion 3 — Is B.1→B.2→B.3 a Ladder or Three Projects? And What B.3 Actually Looks Like

**Status:** exploratory notes, not a settled position. Continues directly from
[Discussion 2](02-implementation-sketch-sentence-scale-and-neurosymbolic.md)'s three neurosymbolic
integration patterns (B.1 generate-then-check, B.2 TPR/VSA fillers, B.3 attention-as-settling).
Discussion paused here to be picked up later, not closed.

**Date:** 2026-08-13

**Question on the table, from the user:** is progressing B.1 → B.2 → B.3 a genuine gradual path,
where work done at each step stays valid at the next — or are the three different enough that
they should be treated as separate projects? If gradual, follow the path in order. If not, skip
straight to B.3, the most ambitious option, since that's the one worth discussing directly.

The user also flagged, independently, that "ontology as guardrail for LLMs" has been a recurring
topic at recent symposia, but the actual work still looks incipient — worth checking that
impression against a literature scan rather than taking it on faith either way.

---

## 1. Verdict on the ladder question

**B.1 ↔ B.2 is a real gradual step.** Both treat the LLM as an external, unmodified oracle — a
black box used only through its input/output interface. They differ only in what the downstream
structure is made of: B.1 builds discrete symbolic structure (accepted/rejected/repaired
candidate bindings) from the LLM's output; B.2 builds vector-encoded structure (role ⊗ filler
bindings) from the LLM's embeddings. Nothing about doing B.1 first forecloses or wastes work for
B.2 — the constraint vocabulary B.1 has to define (what counts as a legal binding, checked against
the schema/microframe type layer) is exactly what B.2 also needs, just given a different
downstream representation.

**B.2 ↔ B.3 turns out closer than Discussion 2 estimated — not farther.** Discussion 2 treated
B.3 (attention itself as the settling dynamics) as the most speculative option, with "no existing
worked example of this to point to." Two things found in this round's scan revise that:

- **["Attention as Binding: A Vector-Symbolic Perspective on Transformer Reasoning"](https://arxiv.org/pdf/2512.14709)**
  argues self-attention already performs something functionally like TPR-style role–filler
  binding as part of its ordinary computation. If that holds up under closer reading, B.2 isn't a
  separate representational layer that then has to be *injected into* B.3 — it may be a
  **description of what B.3's own mechanism is already doing**, unidentified and unsteered. That
  would make B.2 and B.3 two angles on one thing rather than sequential build phases.
- **["Constraint-biased transformers: attention bias injection for rule-compliant recommendation"](https://link.springer.com/article/10.1007/s41060-026-01078-w)**
  is a concrete existence proof, in an applied (non-linguistic) domain, that injecting rule
  constraints directly into attention bias matrices can steer a transformer toward valid
  configurations without destroying its general competence. Not proof this works for a
  conceptual-schema guardrail specifically, but proof the general move is not purely theoretical.

**Net verdict:** not a smooth three-rung ladder, but not three disconnected projects either. B.1's
output — a real, checkable constraint vocabulary over schema/microframe legality — is load-bearing
for *whichever* of B.2 or B.3 comes next; it has to exist before either can be attempted. Whether
B.2 is worth building as its own separate, external representational layer, versus going straight
to looking for its equivalent already inside attention (B.3), is now itself an open question this
scan raised rather than closed — see §4.

## 2. "Ontology as guardrail" — checking the incipient impression

The user's impression was that this specific theme is common at symposia but the actual work is
still early. The scan supports that read, and sharpens *where* the gap sits:

- **["Ontology-Constrained Neural Reasoning in Enterprise Agentic Systems"](https://arxiv.org/html/2604.00555v4)**
  (actively revised — multiple versions circulating in 2026) is representative of the current
  state: the ontology sits as "a formal ontology layer... a structured, symbolic representation of
  a domain that acts as logical guardrails **outside the model**," used as "a logical validation
  layer **prior to tool execution**." The same source states plainly that enterprise systems
  "rigorously constrain LLM inputs... but do not validate outputs against the same definitions" —
  an agent can receive perfectly ontology-grounded context and still emit output that violates
  that same ontology, because nothing checks the output against it.
- **NeSy** (the [Neurosymbolic AI Association](https://nesy-ai.org/) and its yearly
  [conference](https://2025.nesyconf.org/)) is a live, organized research community with ontology
  learning and reasoning-in-LLMs named as explicit interest areas — this is not a fringe topic —
  but the concrete work found through it (ontology *learning* from LLMs, e.g.
  [LLMs4OL](https://www.tib-op.org/ojs/index.php/ocp/article/view/2913)) mostly runs in the
  *opposite* direction from what this project wants: using LLMs to build ontologies, not using an
  existing ontology to constrain an LLM's own internal process.

**So the gap the user's impression pointed at is real and specific**: what exists is ontology as
an *input filter* and *output-adjacent validator*, sitting outside the model, checking before or
after generation. What doesn't exist yet, in anything found: a typed conceptual structure used to
steer the model's own internal settling process *while it runs*. That is precisely B.3, and it
appears to be genuinely open territory, not a solved problem being reinvented.

## 3. Two concrete mechanisms for B.3

Discussion 2 left B.3 as one option with no obvious entry point. This scan surfaces two candidate
mechanisms, differing in invasiveness and in what kind of model access they need:

| Mechanism | How it works | Access needed | Nearest precedent |
|---|---|---|---|
| **Attention-bias injection** | add a bias term to attention logits, computed from schema/microframe legality, so the model can only strongly attend between tokens whose implied binding would be type-legal | custom attention code — needs to sit inside the forward pass | [constraint-biased transformers](https://link.springer.com/article/10.1007/s41060-026-01078-w) (rule-compliant ordering, applied domain) |
| **Activation steering on discovered concept directions** | find linear directions/subspaces in residual-stream activations that correspond to schema elements or microframe relations (via probes or sparse autoencoders), then add steering vectors along those directions at chosen layers during inference | forward hooks on an open-weight model — no architecture change, no retraining | [Representation Engineering survey](https://arxiv.org/html/2502.17601v1); [sparse-autoencoder steering](https://arxiv.org/pdf/2601.02978); [sparse representation steering for guardrails](https://arxiv.org/html/2503.16851v2) |

The second is markedly more tractable as a first prototype: it requires only an open-weight model
and standard interpretability tooling (SAEs, linear probes, hook-based steering), not custom
attention internals. It also connects directly back to the "Attention as Binding" finding in §1 —
if attention is already doing role–filler binding natively, the directions activation steering
would be looking for and the bindings attention is already forming may be the *same* structure
viewed from outside versus from inside.

## 4. The concrete research question this reduces to

**Can directions corresponding to specific schema elements and microframe relations — `Agonist`,
`Antagonist`, `Container`'s `Interior`, `transition_from_to`, and so on — be found or induced in an
open-weight LLM's activation space, and used as steering vectors to bias generation or settling
toward schema-legal configurations?**

This reframes the project's technical core more sharply than Discussion 2 managed to: not "how do
we bolt symbolic structure onto a neural net from outside" (B.1's shape, and largely what the
existing "ontology as guardrail" literature already does), but **"does the conceptual structure
this project has already spent five documents formalizing already exist, unlabeled, inside a
model that was never told about it — and if so, can it be found and steered rather than
reconstructed"**. That's a different, and more interesting, question than either B.1 or B.2 asks
on its own.

## 5. What's still completely open

- Whether schema-element directions are actually **findable** in a real model at all, versus schema
  distinctions this framework cares about (e.g. `Agonist` vs. `Antagonist`, force vs. no-force)
  simply not being linearly separable in any given model's activation space.
- Whether attention-bias injection and activation steering are genuinely two paths to the same
  destination, or solve different sub-problems (the former shaping *which tokens interact*, the
  latter shaping *what a given representation means*) that would both end up needed.
- The B.1 constraint vocabulary itself still has to be built either way, and hasn't been started.

## 5a. Correction, after reading the full paper (2026-08-13, same-day follow-up)

§5's first bullet asked whether "Attention as Binding" holds up under a closer read. It's now
been read in full ([Dhayalkar 2025/2026, AAAI](https://arxiv.org/pdf/2512.14709), single-author,
Arizona State University). Two corrections to how §1 used it:

**It is not an empirical result — it's a same-genre theoretical argument, not independent
evidence.** The paper says so about itself: "Rather than a conventional survey, this paper offers
a *conceptual synthesis*..." It runs **no experiments**. Everything that would actually test the
claim — "VSA-likeness" metrics (role–filler recoverability, interference under superposition,
alignment with VSA operators), representational-similarity/probing analyses, behavioral
benchmarks — is laid out in an "Open problems and research agenda" section as *proposed* future
work, not conducted work. The paper's own "Approximation gap" section is explicit that the
binding/unbinding reading holds only when learned projections happen to be near-orthogonal and
attention happens to be sparse/crisp — conditions it does not check in any real model, because it
checks none. So §1's framing ("if that holds up under closer reading, B.2 isn't a separate layer
but a description of what B.3 is already doing") overstated what closer reading could settle: there
is no empirical claim in the paper to hold up or fail. What the paper *does* provide is a second,
independently-arrived-at theoretical argument for the same B.2≈B.3 intuition Discussion 1's
transformer-clustering literature already pointed at (§4.4 there) — real corroborating weight for
*a hypothesis worth testing*, not confirmation of the hypothesis itself. The net verdict in §1
("B.2 ↔ B.3 turns out closer than Discussion 2 estimated") should be read as "closer as a
*conjecture two independent theoretical lines now converge on*," not as an empirically narrowed
gap.

**A second, sharper distinction the paper makes that §1 didn't carry over:** its central claim —
attention *as it already exists*, unmodified, is interpretable as soft binding — is about
*current, off-the-shelf* transformers. That's the right target for the probing Discussion 3
proposes (finding directions in an *existing* open-weight model). Separately, the paper's own
"Designing VSA-inspired transformer layers" section proposes **explicit binding/unbinding heads**
and a **hyperdimensional memory layer** (eq. 8: `m ← m ⊕ Σ_k r_k ⊗ f_k`) as *new* architecture —
these are not evidence about current models at all, they're a competing, more invasive proposal
(build the mechanism in, rather than find it already there). Worth keeping these two apart:
Discussion 3's research question (§4) is squarely the "find it, don't build it" branch; the
hyperdimensional-memory-layer idea is closer to a fallback if directions turn out not to be
findable, not a next step on the same path.

**What the paper does hand over directly usable, regardless of the above:** concrete metric
definitions this project can borrow verbatim for the probing task in §6 below —
*role–filler recoverability* (inject synthetic role/filler pairs, e.g. via prompts or residual
edits, and measure whether a probe cued with the role vector recovers the filler), *interference
under superposition* (vary how many bindings are superposed at once and measure where recovery
degrades — a direct empirical handle on whether `Agonist`/`Antagonist`/`Interior` bindings survive
being packed into the same residual stream alongside a whole sentence's worth of other bindings),
and *alignment with VSA operators* (fit a simple binding operator, e.g. circular convolution, to a
head's actual input→output behavior and measure the fit). These map onto exactly the "what probe,
what counts as evidence" question §6 already poses — they're a ready-made starting methodology,
not a new open thread.

## 6. Next session

Proposed starting point, deferred to continue later: take one of *entrar*'s already fully-worked
bindings (`PROCESS.Antagonist`, `CONTAINER.Interior`, the shared token `r_joão` from
`dynamic_schemas_proposal.md` §4.6) and think through, concretely, what it would take to go
looking for a corresponding direction in a real open-weight model — what probe to train it against,
what would count as evidence it exists versus evidence it doesn't. §5a's three borrowed metrics
give this a concrete shape rather than starting from a blank page: role–filler recoverability as
the base test (can a probe cued on an `Agonist`-role vector recover the `r_joão` filler?),
interference under superposition as the stress test (does recovery hold up once *entrar*'s two
groundings, `PROCESS.Antagonist` and `CONTAINER.Interior`, are both present in the same sentence's
residual stream, not just one at a time?), and alignment-with-VSA-operators as a sanity check on
whether the recovered direction behaves like a binding at all, or just a correlated feature.
