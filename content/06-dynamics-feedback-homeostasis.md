# 6. Dynamics, Feedback, and Homeostasis

*Source: ebook ch. 10–11 ("Systems Dynamics", "Homeostasis"); slides 18–19 ("Nonlinear
Paradigm", "Nonlinear Thinking").*

Every chapter so far has treated systems relatively statically. This chapter introduces how
systems **change over time** — the *Linear → Nonlinear* paradigm shift previewed in
[`01-worldview-and-paradigm.md`](01-worldview-and-paradigm.md#nonlinear-thinking-preview).

## System dynamics

**System dynamics** is the branch of systems theory that models and understands the dynamic
behavior of complex systems — dealing with internal feedback loops and time delays that affect
the behavior of the entire system. First developed by Professor Jay Forrester at MIT as a
management method, it has since been applied to systems from earth science to the economy to
political regimes.

Analytical thinking sees the world in terms of linear cause and effect. Systems thinking instead
looks for the **interplay** between elements — the feedback loops through which elements are
interconnected in producing a joint outcome.

> "The world is made of circles and we think in straight lines." — Peter M. Senge

### Feedback loops and causal loop diagrams

A **feedback loop** can be defined as a channel or pathway formed by an *effect* returning to its
*cause*, generating either more or less of the same effect. Example: a dialogue between two
people — what one says now affects what the other says, which in turn feeds back as input to
what the first will say in the future.

Not every effect loops back, though: an effect that lands on *another* agent or system without
ever returning to its own source is an **externality**, not feedback. Feedback is self-regulating
by construction — the system that caused the effect is also the one that feels it come back. An
externality is not self-correcting in this way and typically requires some outside governance
(regulation, a shared norm) to be accounted for at all — pollution costs borne by a community
downstream of a factory are the classic example.

System dynamics uses **causal loop diagrams** to represent this: a simple map of a system with
all its constituent components and their interactions. By capturing interactions — and therefore
the feedback loops between them — a causal loop diagram reveals the system's *structure*. By
understanding not just the structure of these relations but also their nature, it becomes
possible to model and simulate a system's behavior over time.

Feedback loops come in two kinds:

- **Positive feedback loop**: values associated with the two linked nodes change in the *same*
  direction — if one decreases, so does the other; if one increases, so does the other.
  - Example: economies of scale between a business and its customers. More products sold → more
    revenue → more investment in scaling production → lower costs → more customers purchase →
    (repeat). This is a **virtuous cycle** where one party's gain is also the other's.
  - Positive feedback loops cannot go on forever — they are typically associated with
    **unstable** processes likely to crash at some point (e.g. a financial bubble that grows
    exponentially, then crashes). The named mechanism behind this crash is **overshoot**: because
    stocks and flows respond with a delay (see below), a growing quantity can keep drawing down a
    slow-replenishing stock past the point the stock can actually sustain — a boom that outruns
    its own resource base, only for feedback to catch up once the deficit becomes unavoidable
    (a town's population booms after a gold discovery, then collapses once the gold runs out).
- **Negative feedback loop**: the two linked nodes change in *opposite* directions — if one
  increases, the other decreases, and vice versa.
  - Example: predator–prey dynamics. More predators → fewer prey → (via reduced food supply)
    fewer predators → more prey → (repeat).
  - Negative feedback loops are typically associated with an overall **stable and sustainable**
    pattern of development — a wave-like graph, bounded within upper and lower limits, with
    relatively smooth fluctuations over a prolonged period.

### Stocks and flows

For a more detailed, quantitative analysis, a causal loop diagram is transformed into a **stock
and flow diagram**, useful for studying a system quantitatively, typically via computer
simulation.

- A **stock** is any entity that accumulates or depletes over time — a simple variable measured
  as a *quantity*. Example: a water reservoir, measured by the volume it contains.
- A **flow** is the *rate of change* in a stock — measured over an interval of time (like
  electrical current, telling us how fast something is flowing). Example: a tap on the side of
  the reservoir, pouring water out.

A quick test for telling the two apart: **if time stopped, would it still exist?** A stock
(an accumulation) would — the reservoir's water is still there. A flow (a rate) would not — "the
water is currently draining" is meaningless without time passing.

> "Systems thinkers see the world as a collection of stocks along with the mechanisms for
> regulating the levels in the stocks by manipulating flows." — Donella H. Meadows

### Nonlinear thinking, in short

| Linear thinking | Nonlinear thinking |
|---|---|
| Events are the result of simple linear interactions; for every effect we search for a mediate cause | Events are the product of a complex of interacting parts, where relations are often cyclical, with feedback loops |
| Analytical thinking's default mode | Systems thinking's default mode — think about the feedback loops in the system and cyclical causation |

## Homeostasis

Many systems require both a continuous input of resources from their environment and the
capacity to export entropy back to it, in order to maintain a specific level of functionality
(see also [`07-energy-entropy-efficiency.md`](07-energy-entropy-efficiency.md)). A tractor needs
periodic fuel input and must export heat and gases; a business needs continuous revenue and must
externalize waste material.

**Homeostasis** (Greek *homos*, "similar" + *stasis*, "standing still") is the state in which a
system's internal variables are regulated so that they remain stable and relatively constant,
despite changes in the system's external environment — its "normal" or equilibrium state. (It's
worth flagging early that equilibrium is not the only game in town — see the note on attractors
at the end of this chapter.)

To maintain homeostasis, a system needs a **regulatory mechanism**, also called a **control
system**, which regulates both the system's internal and external environment to ensure
conditions stay within the parameters needed for the system's internal processes to function. Any
control system can be broken into three parts: a **sensor** (measures the relevant variable), a
**controller** (compares the measurement to the target and decides what to do), and an
**actuator** (carries out the action). **Cybernetics** (from a Greek word meaning "to steer or
guide") is the area of systems theory that studies these regulatory mechanisms — designed to
guide the system toward the environmental parameters best suited to maintaining homeostasis.

A control system can only regulate what it can *distinguish*. **Requisite variety** (Ashby's Law)
states that a regulator must have at least as many internal states as the states it needs to
control in its target system or environment — a thermostat with only "on" and "off" cannot
regulate a target that needs five distinct temperature bands. Undersupplied variety is a common,
nameable failure mode of control systems generally, not just thermostats.

### The homeostatic control loop

1. If the system is within its homeostatic parameters, it simply continues its previous course
   of action.
2. If one or more monitored parameters fall outside those parameters, the system performs some
   operation to affect the state of its environment.
3. The control system then waits for **feedback** — information from the environment about how
   the previous action affected the desired parameters.
4. Depending on whether this information signals the system moving away from or back toward
   homeostasis, it reacts accordingly — and the loop repeats.

**Worked examples**:

- A **thermostat**: switches heaters or air conditioners on/off in response to a temperature
  sensor, regulating the environment to maintain conditions suited to the human body.
- **Driving a car**: while cruising, we simply continue what we were doing, while continuously
  monitoring feedback loops. As soon as information signals we're approaching a homeostatic
  limit (e.g. drifting toward the side of the road), we react by adjusting the steering wheel,
  then wait a fraction of a second to monitor the effect of that action, and react again — all
  in the service of returning to (or staying within) the desired homeostatic condition.

This concept of homeostasis is a powerful model for capturing the development of any **adaptive
system** — its course of development is the product of continuously acting on, and reacting to,
feedback loops. Two or more adaptive systems reacting to each other's behavior over time produces
increasingly complex, evolutionary-like dynamics — underpinning phenomena like international
politics, free-market economies, and social relations generally.

One nuance worth flagging before moving on: homeostasis/equilibrium is not always what a healthy
system is aiming for. Real complex adaptive systems often deliberately operate *away* from strict
equilibrium — homeostasis is better understood as one **attractor** among potentially several a
system could settle into, and under enough strain a system can **bifurcate** into a qualitatively
new attractor altogether rather than snapping back to its old one. This deeper dynamics-of-change
territory — attractors, the "edge of chaos," evolution, resilience — is developed in
[`10-complex-adaptive-systems.md`](10-complex-adaptive-systems.md).
