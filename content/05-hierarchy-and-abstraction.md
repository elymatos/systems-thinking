# 5. Hierarchy and Abstraction

*Source: ebook ch. 9 ("Hierarchy & Abstraction").*

Up to this point, systems have been treated as if they existed on a single level of analysis.
This chapter introduces the tools for capturing the layered, nested structure that real systems
actually exhibit.

## Abstraction and encapsulation

**Abstraction** is the process of successively removing layers of detail from a representation
in order to capture only the most essential features of a system. An architect's master plan of
a building is an abstract representation — it captures only what's needed to grasp the building's
overall make-up, not every structural detail.

Using abstraction, we can define different levels of a model according to its degree of detail
or granularity — this is called **encapsulation**: nesting one model of a system inside another,
which may in turn be encapsulated within a third, and so on, creating a **hierarchical
structure** to the representation.

This has broad reach: it applies whether we're talking about physical systems (atoms make up
molecules, which make up substances...) or social institutions (individuals make up
organizations, which make up societies...).

**Why encapsulate at all, rather than build flat?** Herbert Simon's *Parable of the Watchmakers*
answers this: two watchmakers, Hora and Tempus, each build watches of 1,000 parts. Tempus builds
his in one continuous sequence — if interrupted before completion (e.g. by a phone call), the
entire unfinished assembly falls apart and he must start over. Hora builds his out of stable
sub-assemblies of ~10 parts each, which combine into larger sub-assemblies, and so on — an
interruption only costs him the one small sub-assembly in progress. Hora finishes far more watches
in the long run. **Hierarchical, encapsulated structure isn't just a convenience for our models —
it's what makes real systems robust and evolvable** under the kind of ongoing disruption every
system actually faces.

## Four levels of terminology

| Level | Definition |
|---|---|
| **Element** | The most basic level. Elements are *elemental* — they have no constituent components; we treat them as a whole, described only by their properties. An electron is an element: we cannot look inside it because it isn't made of separate parts. |
| **Subsystem** | A set of elements which make up a system, which is in turn a component of a larger system. Example: the brakes in a car — made up of elements, but also an integral part of the broader system, the car. |
| **System-of-systems** | The level at which a system (itself made of subsystems) is understood as one component within a still-larger system. Example: the car (a system of personal mobility) is in turn part of a transportation system. |
| **Environment** | The ultimate, outermost unit of analysis — everything encapsulating the system-of-systems level (see [`03-boundary-and-environment.md`](03-boundary-and-environment.md)). |

```
Element  ⊂  Subsystem  ⊂  System-of-systems  ⊂  Environment
```

## Integrative levels

Different types of systems base their hierarchy on different organizing features:

- Ecosystem hierarchies are often based on where creatures lie in the food chain.
- Social system hierarchies may be based on age, occupation, education, or other factors.

The **theory of integrative levels** tries to describe the underlying dynamics and
characteristics of this hierarchical-organization feature common to essentially every kind of
system — the idea that units of matter are organized and integrated into levels of increasing
integration and complexity, letting us describe the evolution from the inanimate to the animate
to the social world.

Higher integrative levels are thought to be more complex and to demonstrate more variation and
characteristics than lower ones. Because of **emergence** (see
[`04-relations-synergy-emergence.md`](04-relations-synergy-emergence.md)), each level has its own
unique internal dynamics and cannot be fully reduced to the level below — which is precisely why
we have distinct domains of knowledge (biology, sociology, cultural studies): novel features
emerge at each particular level of integration that cannot be described by simple reference to
physical structures and processes alone.

Three properties recur going up an integrative hierarchy: higher levels (1) *depend on*, and are
made more precarious by, the continued functioning of their lower-level building blocks; (2) have
progressively *fewer instances*, since many lower-level elements combine into each higher-level
one; and (3) *increase in complexity and interdependence* as more elements' worth of relations get
folded into a single higher-level unit.

A phenomenon that is fully explainable by reference to relations among *lower*-level features,
and assumed to exert no independent causal effect back down on them, is called an
**epiphenomenon** — the product of pure upward causation. It's the reductionist counterpart to the
downward causation discussed under strong emergence (see
[`04-relations-synergy-emergence.md`](04-relations-synergy-emergence.md#weak-vs-strong-emergence)).

## Bottom-up vs. top-down causality

As soon as a system has emergence and hierarchical structure, a new dynamic appears between its
levels. Because emergence implies that the rules governing any given level may be qualitatively
different from those governing another, this becomes particularly pronounced at the two
extremes — the system's **micro** level and its **macro** level — which nonetheless have to work
together as one entire system.

The open question: is it the rules that govern the micro level, or the rules that govern the
macro level, that ultimately determine the system's functioning as a whole? This is also known
as the **bottom-up vs. top-down causality** dynamic, a key theme within systems theory.

**Worked example**: a doctor has a patient in poor physical health and who is psychologically
depressed.

- A **bottom-up** explanation looks for a physiological cause — a virus or infection driving the
  overall problem.
- A **top-down** explanation reasons instead that it is the patient's psychological state that is
  inducing their physiological state of poor health.

The point isn't to resolve which is "correct" in general — within any emergent hierarchical
system (the human body, a political regime, an ecosystem), there will always be this complex
dynamic between the rules that govern the system on the micro level and those that govern it on
the macro level.

One framing (after ecologist Timothy Allen) sharpens the question rather than resolving it: the
**micro level answers "how"** — what's physically *possible* given the parts and their local
rules — while the **macro level answers "why"** — which of those many possibilities was actually
*selected* and persists. A mammal's limb could in principle have any number of digits (the micro
level permits it); the "why" of having five is a constraint handed down from evolutionary
heritage, operating at the macro/lineage level. A concrete mechanism for this kind of top-down
selection: in evolutionary systems, the macro-level environment doesn't dictate the micro-level
agents' behavior directly — it **selects** among whatever variety those agents already generate,
favoring some contributions over others and thereby reshaping the population over time (see
[`10-complex-adaptive-systems.md`](10-complex-adaptive-systems.md) for evolution as a general
systems process).

## Why this matters

Abstraction is a powerful method of reasoning: by using encapsulation to nest subsystems within
systems, we can build models that capture the emergent, hierarchical structures we see all
around us in the world — without collapsing every question into either "just look at the parts"
or "just look at the whole."
