# Chapter 24: Partial Boundaries

## Core Idea
Full architectural boundaries are expensive to build and to maintain, so an architect who thinks "I might need one here" can build a **partial** boundary — three techniques, each a placeholder that can also degrade if the boundary never materializes.

## Frameworks Introduced
- **What a full boundary costs**: "reciprocal polymorphic Boundary interfaces, Input and Output data structures, and all of the dependency management necessary to isolate the two sides into independently compilable and deployable components. That takes a lot of work. **It's also a lot of work to maintain.**"
- **The YAGNI tension, stated honestly**: "This kind of anticipatory design is often frowned upon by many in the Agile community as a violation of YAGNI: 'You Aren't Going to Need It.' Architects, however, sometimes look at the problem and think, **'Yeah, but I might.'**"
- **Technique 1 — Skip the Last Step**: "do all the work necessary to create independently compilable and deployable components, and then **simply keep them together in the same component**. The reciprocal interfaces are there, the input/output data structures are there, and everything is all set up — but we compile and deploy all of them as a single component."
  - What you save: "it does not require the administration of multiple components. There's **no version number tracking or release management burden**. That difference should not be taken lightly."
  - What you don't save: "this kind of partial boundary requires **the same amount of code and preparatory design work** as a full boundary."
- **Technique 2 — One-Dimensional Boundaries** (the Strategy pattern): "A `ServiceBoundary` interface is used by clients and implemented by `ServiceImpl` classes."
  - "This sets the stage for a future architectural boundary. The necessary dependency inversion is in place in an attempt to isolate the `Client` from the `ServiceImpl`."
  - The weakness: "the separation can degrade pretty rapidly... **Without reciprocal interfaces, nothing prevents this kind of backchannel other than the diligence and discipline of the developers and architects.**"
- **Technique 3 — Facades**: "even the dependency inversion is sacrificed. The boundary is simply defined by the `Facade` class, which lists all the services as methods, and deploys the service calls to classes that the client is not supposed to access."
  - The cost: "the `Client` has a **transitive dependency** on all those service classes. In static languages, a change to the source code in one of the `Service` classes will force the `Client` to recompile. Also, you can imagine how easy backchannels are to create with this structure."

## Key Concepts
- **Reciprocal interfaces are what make a boundary hold.** A full boundary maintains isolation *in both directions*; the one-dimensional and facade forms maintain it in one direction or none, which is exactly why they can decay.
- **Every partial boundary has a decay mode.** "Each is appropriate, in certain contexts, as a placeholder for an eventual full-fledged boundary. **Each can also be degraded if that boundary never materializes.**"
- **The architect's job here is a judgment call, twice over**: "to decide **where** an architectural boundary might one day exist, and **whether to fully or partially implement** that boundary."

## Reference Tables

| Technique | Dependency inversion? | Reciprocal interfaces? | Code/design cost | Admin cost | Main decay risk |
|---|---|---|---|---|---|
| **Skip the last step** | Yes | Yes | Same as a full boundary | None — one component, no versioning or release management | Dependencies quietly start crossing the line the wrong way |
| **One-dimensional (Strategy)** | Yes, one direction | No | Modest | None | Backchannels; only developer discipline prevents them |
| **Facade** | **No** | No | Lowest | None | Transitive dependency on every service class; recompilation on any service change; backchannels trivially easy |

## Worked Example
**FitNesse's web component — the technique and its failure mode, in one story.**

**The setup.** FitNesse's web server component "was designed to be separable from the wiki and testing part of FitNesse. The idea was that we might want to create other web-based applications by using that web component."

**Why it stayed partial.** The **Download and Go** rule: "we did not want users to have to download two components... It was our intent that users would download one jar file and execute it without having to hunt for other jar files, work out version compatibilities, and so on."

So they did all the boundary work — reciprocal interfaces, data structures, dependency management — and then skipped the last step, shipping one jar. That is precisely the trade the technique offers: pay the design cost, avoid the release-management cost, keep the option.

**And then the failure.** "The story of FitNesse also points out one of the dangers of this approach. **Over time, as it became clear that there would never be a need for a separate web component, the separation between the web component and the wiki component began to weaken. Dependencies started to cross the line in the wrong direction. Nowadays, it would be something of a chore to re-separate them.**"

Two things are worth extracting from that admission:

1. **The decay was rational, not sloppy.** Once the team knew the separate web component would never be needed, maintaining the discipline had no visible payoff — and nothing mechanical (no separate compilation unit) was enforcing it. A partial boundary's isolation is sustained by intent; when the intent lapses, so does the boundary.
2. **The cost was deferred, not avoided.** The option was preserved for years at near-zero admin cost, and then quietly expired. That is not a failure of the technique so much as a demonstration that a partial boundary is a *decaying* asset, and the architect should expect to revisit it.

## Key Takeaways
1. Full boundaries are expensive twice: to build and to maintain. Partial boundaries buy the option more cheaply.
2. "Skip the last step" costs full design effort but avoids all multi-component administration — and only compilation, not discipline, is what you gave up.
3. Strategy gives you dependency inversion in one direction; backchannels are prevented only by discipline.
4. Facade is cheapest and weakest: no inversion, transitive client dependencies, recompiles on any service change.
5. Every partial boundary decays if the full boundary never arrives — plan to re-check, not to set and forget.
6. Deciding where a boundary might belong, and how completely to build it, is an explicit architectural responsibility.

## Connects To
- **Ch 17 (Boundaries)** and **Ch 18 (Boundary Anatomy)**: what a full boundary is and what crossing one costs.
- **Ch 25 (Layers and Boundaries)**: the "watchful eye" doctrine — deciding *when* to promote a partial boundary to a full one.
- **Ch 16 (Independence)**: the same logic at the level of decoupling modes.
- **Clean Code, Ch 10**: the Facade pattern used to solve the SRP instantiation burden.
