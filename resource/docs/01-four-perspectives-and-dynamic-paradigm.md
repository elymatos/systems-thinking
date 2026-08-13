# Discussion 1 — Capra's Four Perspectives, Applied to a Conceptual/Linguistic System

**Status:** exploratory notes, not a settled position. Nothing here is established framework —
it's a record of a first conversation, kept so the reasoning isn't lost, not a spec.

**Date:** 2026-08-13

**Participants' source material:**
- `resource/capra.txt` — excerpt from Fritjof Capra, *The Hidden Connections*, on the
  form/matter/process/meaning account of living and social systems.
- FNBr conceptual dimension docs (`/home/ematos/devel/fnbr/webtool45/app/UI/views/Documentation/conceptual_dimension/`)
  — the existing schema/frame/profiling framework this discussion is trying to extend.
- FNBr's `dynamic_schemas_proposal.md` (`/home/ematos/devel/fnbr/webtool45/docs/conceptual/`) — an
  ungoverned proposal for an instance/runtime layer under the schema type layer.
- `content/01-worldview-and-paradigm.md` (this repo) — the four paradigm shifts.

---

## 1. The starting idea

Capra extends the systems view of life (pattern/structure/process, in his vocabulary: *form*,
*matter*, *process*) to the social domain by adding a fourth perspective, **meaning** — necessary
once reflective consciousness, mental imagery, and choice enter the picture. The proposal on the
table: a **conceptual dimension** (image-schema-like, grounding a linguistic system) can be
organized along the same four axes.

Initial mapping proposed:

| Capra | Conceptual dimension candidate |
|---|---|
| Structure (pattern) | the graph of DIMENSION-family schemas and the relations (microframes) between them |
| Process | the EVENT-family schemas — force, transformation |
| Matter | linguistic content — lemmas, sentences, corpus tokens |
| Meaning | the pattern established by a lexical unit or frame |

## 2. What held up, what needed correcting

**Held up directly:** Structure ↔ the static schema graph (REGION/LINK and everything built on
them — DIMENSION, CLASS, PART_WHOLE, CONTAINER, the event family as *types*), and Matter ↔ actual
linguistic tokens. Both are genuinely close to Capra's "nonmaterial network of relationships" and
"material embodiment."

**Process was mis-located at first.** Capra's process is not "the class of things that denote a
happening" — it's *the self-generating activity that continually produces and sustains the
pattern* (autopoiesis in biology; communication, in Luhmann's reading, for the social domain).
The EVENT-family schema catalog (AGENTIVE, CHANGE, MOTION, …) is still declarative — it's part of
*structure*, just the dynamically-shaped part of it. The better candidate turned out to be
FNBr's own **`dynamic_schemas_proposal.md`**, which is a genuinely separate instance/runtime
layer under the type layer:

- schema *instances* with their own identity, distinct from the type they instantiate (§4.1–4.2);
- steps classified as **test** / **trigger** / **mutation**, where mutation is specifically
  "mints a new instance" (§2, §4.3) — an actual state change, not a static fact;
- the worked `entrar` example (§4.6): a single token (`r_joão`) is shared across two different
  schema groundings (`PROCESS.Antagonist` and `CONTAINER.Interior`) at once, drawn from "one
  shared pool per sentence/construal," not one pool per edge.

That last point matters beyond just "process": it's already a graph of shared instances, not a
tree assembling parts — see §4 below.

**Meaning was also mis-located.** "The pattern a frame/LU establishes" describes a settled
*structure*, not the act Capra is pointing at (mental imagery, selective attention, choice among
alternatives). The much closer analogue already inside the framework is **profiling/construal
itself** — foregrounding part of a base while the rest stays backgrounded, ranked around a
trajector. That is close to verbatim what Capra means by holding a mental image: a selective,
purposive view over structure, not the structure itself. Consistent with the existing framework's
own commitment (from `introduction.md`) that a lexical unit is only one of several things that can
evoke a schema — images, gestures, deixis — so meaning-as-construal isn't tied to the lexicon
specifically, which avoids the reductionism the user explicitly wants to avoid here.

**Open, not resolved:** whether meaning belongs at the level of a single construal act (one
sentence, one interpretation event) or at the level of the whole conventionalized system (the
shared "culture" of construals a language community has settled into, closer to Luhmann's
social-autopoiesis reading of meaning as sustained by recurring communication). Capra's own social
extension leans toward the latter as what actually accumulates into rules and structures; the
per-utterance case is the process that produces it.

## 3. The paradigm argument

The reason to care about "process" as a genuine runtime rather than a static taxonomy connects to
a separate, larger claim: mainstream computational-linguistic practice (parsers, and — the user's
point — transformer-based LLMs underneath the surface, despite the added complexity) is still
tied to what ch. 1 of this repo calls the mechanistic/analytical paradigm — a sentence as a
**whole** composed from **parts** (words), processed **linearly**, with word classes combining by
fixed rules, no force involved, structure fixed before interpretation starts.

The alternative sketched: a sentence as a **dynamical network** of interacting concepts — nodes
richer than "word," each linked outward into its own network, with the *actual* structure of
relations partly settling *during* interpretation rather than being fixed in advance by a parse
tree.

This maps precisely onto the repo's own four paradigm shifts (`01-worldview-and-paradigm.md`),
not just loosely:

| Ch. 1 shift | Cartesian/parser paradigm | Proposed alternative |
|---|---|---|
| Parts → Whole | sentence = words combining into a whole | sentence = a network state, not an assembly |
| Reduction → Emergence | meaning composed bottom-up by fixed rules | meaning settles out of interaction, not derivable from parts alone |
| Linear → Non-linear | sequential, word-by-word processing | mutually adjusting interpretation — force, not sequence |
| Disconnected → Connected | word classes + combination rules (properties first) | concepts as nodes whose relations are primary |

This is a strong reason to treat the systems-thinking review as the actual vocabulary base for
this argument, rather than importing new terminology from scratch.

**The user's caveat, correcting scope:** this isn't proposing something wholly new. Connectionist,
spreading-activation parsing already exists and has already been implemented (including, per the
user, in FNBr's own prior work) — the "network, not tree" idea is not novel. Talmy's force
dynamics and Construction Grammar are already part of the ground being stood on. What's
specifically underexplored is treating language with the actual *apparatus* of dynamical systems
theory — states, forces, settling, equilibria — rather than borrowing only the "network" metaphor
from connectionism while keeping the underlying computation static/associative.

## 4. Literature scan

Run 2026-08-13, focused on (a) precedent for network/dynamical treatments of sentence processing,
old and new, and (b) how recent the "connectionism revolution" (transformers) has actually made
the dynamical-systems framing, since the user flagged this as the area most likely to have moved
in the last few years.

### 4.1 Historical precedent (1980s–90s) — spreading activation, connectionist parsing

- **Collins & Loftus (1975), "A Spreading Activation Theory of Semantic Processing"** — the
  foundational psycholinguistic source for spreading activation over a semantic network;
  everything downstream cites this.
- **Small, Cottrell, Shastri, Pollack, Waltz (early 1980s)** — the first connectionist parsers,
  localist spreading-activation networks over layered nodes (lexical / word-sense / case-role),
  aimed mainly at lexical disambiguation. [Spreading Activation and Connectionist Models for NLP](https://www.degruyterbrill.com/document/doi/10.1515/thli.1990.16.1.25/html?lang=en)
- **Smolensky & Legendre, *The Harmonic Mind* (2006)**, and the Harmonic Grammar /
  Optimality-Theoretic-Grammar line generally — the closest full theoretical precedent for
  "settling to an equilibrium construal." A sentence's well-formedness is the *globally maximal
  Harmony* state of a continuous network — literally a dynamical system relaxing toward a stable
  configuration, with a symbolic grammar (OT constraint ranking) read off the network's
  equilibria. This is the strongest existing bridge between force/energy-landscape dynamics and
  an explicit, checkable symbolic structure — worth reading closely before going further, since
  it already solved a version of "how does an explicit grammar emerge from a settling process."

### 4.2 Construction Grammar's own recent turn toward dynamics

**This corrects something said earlier in this discussion.** Construction Grammar's network was
described as "static, not processual" — a taxonomy of constructions, not a runtime. **Holger
Diessel, *The Constructicon: Taxonomies and Networks* (Cambridge, 2023)** complicates that:
Diessel reconceives the constructicon explicitly as a **spreading-activation network**, with
constructions linked by non-taxonomic associative relations, and activation spread determined by
three factors — the network's structure, the current context, and the user's prior experience
with specific forms. This is recent (2023) and moves CxG itself toward exactly the kind of dynamic
account this discussion is reaching for, from the construction-grammar side rather than the
computational side. [LINGUIST List review](https://linguistlist.org/issues/35/1623/)

### 4.3 Recent (2024) dynamical-systems models of meaning specifically

**"Contextual Modulation of Language Comprehension in a Dynamic Neural Field Model of Lexical
Meaning" (arXiv:2407.14701, 2024)** — a **dynamic neural field (DNF)** model: word meaning as a
continuous, time-evolving activation pattern over semantic space, governed by differential
equations, where context reshapes activation via recurrent connectivity and gain modulation
rather than by discrete rule application. Meaning genuinely "builds up, competes, and stabilizes"
over the course of comprehension rather than being computed in one shot. This is close in spirit
to the equilibrium/settling idea from §3 above, and recent enough to represent current practice
rather than a historical artifact.

### 4.4 Transformers *as* dynamical systems — the "connectionism revolution" the user flagged

This is the area that has genuinely moved, and it's directly relevant to the user's point that
LLMs "blurred the scene" without changing the paradigm:

- **Geshkovski et al., "The emergence of clusters in self-attention dynamics" (NeurIPS 2023,
  arXiv:2305.05465)** and the companion **"A mathematical perspective on Transformers"** — prove,
  not just claim, that self-attention *is* an interacting-particle system: tokens behave as
  particles that cluster toward limiting configurations as depth → ∞, with cluster identity
  determined by the value matrix's spectrum. Extended to causal (decoder) attention in
  [Karagodin & Polyanskiy, 2024](https://arxiv.org/pdf/2411.04990). Tokens are shown to pass
  through long-lived **metastable multi-cluster states** before final collapse — i.e., the
  network genuinely has an equilibrium-seeking dynamics, not merely a "network" topology.
- **"Transformer Dynamics: A neuroscientific approach to interpretability" (arXiv:2502.12131,
  2025)** — explicitly imports dynamical-systems/neuroscience interpretability tooling onto LLM
  internals, motivated by the same interpretability gap the user raised: it's hard to know what
  "structures" a transformer is actually using.

**The point worth taking from this cluster of results:** the mathematics underneath transformers
already *is* a dynamical system of interacting elements settling toward stable states — confirming
the user's claim that transformers "increased the complexity" without changing the paradigm at the
level of what's *interpretable*. What none of this literature has is an explicit, typed,
checkable layer of conceptual structure for the dynamics to be settling *over* — the clusters that
emerge are geometric, not conceptually labeled. That's exactly the gap the schema/microframe
layer (structure) is positioned to fill, if the instance layer (process) can be extended to a
genuine cross-word settling dynamic (the open problem flagged in §3 of the prior discussion turn).

### 4.5 Force dynamics — grounding without a dynamical implementation

Talmy's force dynamics itself is well established (Talmy 1988, *Force Dynamics in Language and
Cognition*; recent work continues, e.g. *Cognitive Semantics* 11.1, 2025, "Force Dynamics in
Unexpected Places"). No search turned up an existing **computational, dynamical-systems
implementation** of force dynamics specifically — it has stayed a descriptive semantic vocabulary
(which is exactly the vocabulary schemas.md's `Agonist`/`Antagonist` already borrows). This matches
the user's own assessment: the conceptual ground (force dynamics, Construction Grammar) is
established; running it as an actual dynamical system is the underexplored part.

### 4.6 Not yet located

The user mentioned FNBr has already implemented a parser using spreading activation. That
implementation isn't in the material read for this discussion — worth pointing to directly
(file/repo path) in a follow-up so it can be compared against Diessel's associative-constructicon
model and the Harmonic Grammar precedent above, rather than reasoning about it from memory.

## 5. Where this leaves things

- **Structure** = the static schema/frame/microframe graph (unchanged from the original mapping).
- **Process** = FNBr's proposed instance/runtime layer (test/trigger/mutation, shared token pools),
  not the EVENT-schema catalog — and its open frontier is extending the shared-pool mechanism
  (currently scoped to one LU's own multiple groundings, e.g. *entrar*) across an entire sentence,
  so that multiple words' constructions genuinely constrain each other and settle to a joint
  construal — which is exactly the kind of dynamics Harmonic Grammar, DNF models, and the
  transformer-clustering literature all already formalize in their own domains, without an
  interpretable conceptual layer underneath.
- **Matter** = linguistic tokens (unchanged), with a concrete open question inherited from the
  proposal itself (§4.5 there): what an atomic instance actually points at outside the simulation
  — an annotation span, an LU token, or an uninterpreted bookkeeping identity. That's precisely
  the matter/process interface.
- **Meaning** = the construal/profiling act — a selective, purposive view over structure, produced
  by (and only fully real *as*) the settling process — not a static label on a frame. Still open
  whether "meaning" belongs at the individual-construal grain or the conventionalized-system
  grain (or, per Capra's own account of social systems, both — recursively).

## 6. Open threads for next discussion

1. Locate and compare FNBr's existing spreading-activation parser against Diessel (2023) and
   Harmonic Grammar.
2. Work out what a cross-word settling dynamic would actually look like on top of the
   `dynamic_schemas_proposal.md` instance layer — this is the concrete research question the
   whole paradigm argument reduces to.
3. Decide the individual-construal vs. conventionalized-system grain question for "meaning."
4. Read Smolensky & Legendre's *Harmonic Mind* closely — it may already contain a template for
   "explicit structure that a settling dynamical system converges toward," which is exactly the
   combination this project is reaching for.
