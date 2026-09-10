# Chapter 14: Component Coupling

## Core Idea
Three principles govern relationships *between* components — **ADP** (no cycles), **SDP** (depend in the direction of stability), and **SAP** (be as abstract as you are stable) — and together SDP + SAP are **the DIP for components**, with metrics that make conformance measurable.

## Frameworks Introduced
- **ADP — The Acyclic Dependencies Principle**: *"Allow no cycles in the component dependency graph."*
  - The problem it solves is **"the morning after syndrome"**: "you worked all day, got some stuff working, and then went home, only to arrive the next morning to find that your stuff no longer works... Because somebody stayed later than you and changed something you depend on!" Small teams tolerate it; large ones don't — "It is not uncommon for **weeks** to go by without the team being able to build a stable version."
  - Two historical solutions, both from telecommunications: the **weekly build** and the **ADP**.
- **SDP — The Stable Dependencies Principle**: *"Depend in the direction of stability."*
  - "It is the perversity of software that a module that you have designed to be easy to change can be made difficult to change by someone else who **simply hangs a dependency on it**. Not a line of source code in your module need change, yet your module will suddenly become more challenging to change."
  - Formally: **the I metric of a component should be larger than the I metrics of the components it depends on** — I should *decrease* in the direction of dependency.
- **SAP — The Stable Abstractions Principle**: *"A component should be as abstract as it is stable."*
  - Two directions: a stable component should be **abstract** so its stability doesn't prevent extension; an unstable component should be **concrete** since its instability allows easy change.
  - "**The SAP and the SDP combined amount to the DIP for components.** SDP says dependencies should run in the direction of stability, and SAP says stability implies abstraction. Thus dependencies run in the direction of abstraction."
  - The difference from DIP proper: "with classes there are no shades of gray. Either a class is abstract or it is not. The combination of the SDP and the SAP deals with components, and allows that a component can be **partially** abstract and **partially** stable."
- **The Main Sequence** — the line connecting (1, 0) and (0, 1) on the A/I graph; the locus of points maximally distant from both zones of exclusion. "A component that sits on the Main Sequence is not 'too abstract' for its stability, nor is it 'too unstable' for its abstractness. It is **depended on to the extent that it is abstract, and it depends on others to the extent that it is concrete**."

## Key Concepts
- **Stability has nothing to do with frequency of change.** "Stand a penny on its side. Is it stable in that position?... unless disturbed, it will remain in that position for a very long time." Webster's: stable means *"not easily moved."* Stability is about **the amount of work required to make a change**. A table is stable; a standing penny is not.
- **The one factor that matters for components** — ignoring size, complexity, and clarity: "One sure way to make a software component difficult to change is to make **lots of other software components depend on it**."
- **Responsible/independent vs. irresponsible/dependent** — a component many others depend on and which depends on nothing is *responsible* (reasons not to change) and *independent* (nothing forcing it to change): maximally stable. The reverse is *irresponsible* and *dependent*: maximally unstable.
- **Abstract component** — a component containing nothing but an interface, no executable code. "A very common, and necessary, tactic when using statically typed languages like Java and C#. These abstract components are very stable and, therefore, are ideal targets for less stable components to depend on." In Ruby and Python "these abstract components don't exist at all, nor do the dependencies that would have targeted them."
- **Useful diagram convention** — put unstable components at the top, "because **any arrow that points up is violating the SDP**" (and the ADP).
- **The metrics are not gods** — "a metric is not a god; it is merely a measurement against an arbitrary standard. These metrics are imperfect, at best, but it is my hope that you find them useful."

## Reference Tables

### The metrics

| Metric | Definition | Range | Meaning |
|---|---|---|---|
| **Fan-in** | Incoming dependencies — classes outside the component that depend on classes inside it | — | Reasons not to change |
| **Fan-out** | Outgoing dependencies — classes inside that depend on classes outside | — | Reasons to change |
| **I** (Instability) | `Fan-out / (Fan-in + Fan-out)` | [0, 1] | 0 = maximally stable (responsible, independent); 1 = maximally unstable (irresponsible, dependent) |
| **A** (Abstractness) | `Na / Nc` — abstract classes + interfaces over total classes | [0, 1] | 0 = no abstractions at all; 1 = nothing but abstractions |
| **D** (Distance) | `|A + I − 1|` | [0, 1] | 0 = directly on the Main Sequence; 1 = as far from it as possible |

Practical calculation: in C++ the dependencies are typically `#include` statements, and I is easiest to compute with one class per source file; in Java, count `import` statements and qualified names. (Historical note: Martin previously called Fan-out/Fan-in *efferent* and *afferent* couplings, Ce and Ca — "That was just hubris on my part: I liked the metaphor of the central nervous system." Similarly, D was previously D′.)

### The zones of exclusion

| Zone | Location | Why it's bad | Real examples |
|---|---|---|---|
| **Zone of Pain** | (0, 0) — stable and concrete | Rigid. Can't be extended (not abstract), can't be changed (too depended-on) | **Database schemas** — "notoriously volatile, extremely concrete, and highly depended on. This is one reason why the interface between OO applications and databases is so difficult to manage, and why schema updates are generally painful" |
| **Zone of Uselessness** | (1, 1) — abstract with no dependents | Maximally abstract yet nothing uses it | "Leftover abstract classes that no one ever implemented... sitting in the code base, unused" — "a kind of detritus" |

**Volatility is the hidden third axis.** A concrete utility library like `String` sits near (0, 0) but is nonvolatile — "it is so commonly used that changing it would create chaos." Nonvolatile components are harmless there. "The more volatile a component in the Zone of Pain, the more 'painful' it is." The published diagram "shows only the most painful plane, where volatility = 1."

## Worked Example
**The weekly build, and why it collapses.** All developers ignore each other Monday through Thursday, working on private copies. Friday they integrate everything and build.

"This approach has the wonderful advantage of allowing the developers to live in an isolated world for four days out of five. The disadvantage, of course, is the large integration penalty that is paid on Friday."

The decay is arithmetic: as the project grows, integration overflows into Saturday. "A few such Saturdays are enough to convince the developers that integration should really begin on Thursday" — and the start of integration creeps toward mid-week. "As the duty cycle of development versus integration decreases, the efficiency of the team decreases, too." Frustration leads to a biweekly build, which buys time until integration grows again. "Eventually, this scenario leads to a crisis. To maintain efficiency, the build schedule has to be continually lengthened — but lengthening the build schedule **increases project risks**. Integration and testing become increasingly harder to do, and the team loses the benefit of rapid feedback."

**The ADP alternative.** Partition the development environment into **releasable components**, each owned by a developer or team. When a component works, release it: give it a release number, move it to a directory other teams use, and keep modifying your own private copy. Other teams "can decide whether they will immediately adopt the new release. If they decide not to, they simply continue using the old release."

"Thus **no team is at the mercy of the others**... Moreover, integration happens in small increments. There is no single point in time when all developers must come together and integrate everything they are doing."

**What a DAG buys you, concretely.** In the acyclic diagram — Entities, Database, Interactors, Presenters, View, Controllers, Authorizer, Main:

- **Impact analysis is trivial.** Presenters makes a new release; follow the arrows backward to find View and Main affected. Nothing else.
- **Leaf releases are free.** "When Main is released, it has utterly no effect on any of the other components in the system. They don't know about Main, and they don't care when it changes."
- **Testing is cheap.** To test Presenters, build it against the versions of Interactors and Entities you're already using. "None of the other components in the system need be involved... relatively few variables to consider."
- **Build order is obvious.** Bottom up: Entities, then Database and Interactors, then Presenters, View, Controllers, Authorizer, and Main last. "We know how to build the system because we understand the dependencies between its parts."

**Now add one cycle.** A new requirement makes `User` in Entities use `Permissions` in Authorizer. The consequences cascade:

- Database must be compatible with Entities — and now, transitively, with Authorizer, which depends on Interactors. "This makes Database much more difficult to release."
- "Entities, Authorizer, and Interactors have, in effect, become **one large component**" — everyone working in any of them gets the morning after syndrome, "stepping all over one another because they must all use exactly the same release of one another's components."
- Testing Entities now requires building and integrating Authorizer and Interactors.
- "You may have wondered why you have to include so many different libraries, and so much of everybody else's stuff, just to run a simple unit test of one of your classes. If you investigate the matter a bit, you will probably discover that there are **cycles** in the dependency graph."
- Build order may not exist at all — "there probably is no correct order. This can lead to some very nasty problems in languages like Java that read their declarations from compiled binary files."
- "Build issues grow **geometrically** with the number of modules."

**Two ways to break it** (always possible):
1. **Apply DIP** — create an interface with the methods `User` needs, put it in Entities, and have Authorizer inherit it. This inverts the Entities→Authorizer dependency.
2. **Create a new component** that both Entities and Authorizer depend on, and move the shared class(es) into it.

The second implies the structure is volatile: "as the application grows, the component dependency structure **jitters and grows**. Thus the dependency structure must always be monitored for cycles."

**Fixing an SDP violation.** A `Flexible` component is designed to be easy to change (high I). A developer in `Stable` hangs a dependency on it. "This violates the SDP because the I metric for Stable is much smaller than the I metric for Flexible. As a result, **Flexible will no longer be easy to change**."

The fix, via DIP: class `U` in Stable needs class `C` in Flexible. Create an interface `US` declaring everything `U` needs, put it in a new component `UServer`, and make `C` implement it. "This breaks the dependency of Stable on Flexible, and forces **both** components to depend on UServer. UServer is very stable (I = 0), and Flexible retains its necessary instability (I = 1). All the dependencies now flow in the direction of decreasing I."

## Mental Models
- **Component structure cannot be designed top-down.** "It is not one of the first things about the system that is designed, but rather **evolves** as the system grows and changes." Counterintuitively, "component dependency diagrams have very little to do with describing the function of the application. Instead, they are **a map to the buildability and maintainability** of the application. This is why they aren't designed at the beginning of the project. There is no software to build or maintain, so there is no need for a build and maintenance map."
- **The order the principles come into play**: first SRP and CCP as modules accumulate (collocate what changes together); then **isolation of volatility** — "we don't want cosmetic changes to the GUI to have an impact on our business rules"; then CRP as reusable elements emerge; finally ADP as cycles appear.
- **Trying to design it first fails**: "We would not know much about common closure, we would be unaware of any reusable elements, and we would almost certainly create components that produced dependency cycles."
- **Not all components should be stable.** "If all the components in a system were maximally stable, the system would be **unchangeable**."
- **Why stable components must be abstract**: high-level policy belongs in stable components (I = 0), but that would make policy hard to change — "The answer is found in the OCP... it is possible and desirable to create classes that are flexible enough to be extended without requiring modification. Which kind of classes conform to this principle? **Abstract classes.**"
- **Use D statistically, and over time.** Compute mean and variance of D across components — "a conforming design [has] a mean and variance close to zero." Variance sets control limits identifying "exceptional" components. Plotting D for one component across releases catches drift: in the example, a control threshold at D = 0.1 and the Payroll component's R2.1 point exceeding it, "so it would be worth our while to find out why this component is so far from the main sequence."

## Key Takeaways
1. No cycles. Cycles fuse components into one giant one, destroy build order, make unit tests drag in the world, and reinstate the morning after syndrome.
2. Break cycles with DIP or by extracting a new shared component — and expect to keep doing it as requirements change.
3. Weekly builds decay predictably; releasable components with version numbers are the durable alternative.
4. Stability = work required to change = incoming dependencies. It is not change frequency.
5. Depend in the direction of decreasing I. An upward arrow in a conventional diagram is a violation.
6. Stable components must be abstract or the architecture goes rigid; unstable ones should be concrete.
7. SDP + SAP = DIP for components, with shades of gray that class-level DIP doesn't allow.
8. Aim for the Main Sequence endpoints; avoid the Zone of Pain (volatile, stable, concrete — e.g. database schemas) and the Zone of Uselessness (abstract, unused).
9. Component structure is discovered, not designed up front — it maps buildability, not functionality.

## Connects To
- **Ch 7 (SRP) / Ch 13 (CCP, CRP)**: the cohesion forces that shape components before coupling concerns arrive.
- **Ch 11 (DIP)**: the mechanism for both cycle-breaking and SDP repair.
- **Ch 8 (OCP)**: why stable components must be abstract to stay flexible.
- **Ch 30 (The Database Is a Detail)**: the Zone of Pain, explained at length.
- **Ch 34 (The Missing Chapter)**: package structure and enforced dependency rules in practice.
