---
name: clean-architecture
description: "Knowledge base from \"Clean Architecture: A Craftsman's Guide to Software Structure and Design\" by Robert C. Martin (with James Grenning and Simon Brown). Use when applying Martin's architecture rules — SOLID principles, component cohesion and coupling, boundaries, the Dependency Rule, policy vs. detail, use cases and entities, services and microservices, embedded architecture, or package/directory structure — and when deciding what to defer, where to draw a line, or which way a dependency should point."
---

<!-- argument-hint: [topic, principle acronym like SRP/CCP/SDP, or chapter number] -->

# Clean Architecture: A Craftsman's Guide to Software Structure and Design
**Author**: Robert C. Martin (Uncle Bob), with James Grenning (Ch 29) and Simon Brown (Ch 34) | **Pages**: ~429 | **Chapters**: 34 + Appendix A | **Generated**: 2026-08-29

## How to Use This Skill

- **Without arguments** — load the core rules below for reference
- **With a topic** — ask about `boundaries`, `the Dependency Rule`, `microservices`, `deferring the database`, `package structure`; I find and read the relevant chapter
- **With an acronym** — `SRP`, `OCP`, `LSP`, `ISP`, `DIP`, `REP`, `CCP`, `CRP`, `ADP`, `SDP`, `SAP`
- **With a chapter** — ask for `ch22`; I load that file
- **Browse** — ask "what chapters do you have?"

When you ask about something not in Core Rules below, I read the relevant chapter file before answering.

---

## Core Rules

### The goal, and the measure
**"The goal of software architecture is to minimize the human resources required to build and maintain the required system."** Design quality is measured by the effort required to meet the customer's needs: low and staying low is good; growing with each release is bad. Design and architecture are the same continuum — there is no dividing line, only decisions from the highest level to the lowest.

**The only way to go fast is to go well.** Making messes is slower than staying clean at *every* time scale — Gorman's experiment showed TDD beating non-TDD on a 30-minute task. And the rewrite is not the escape: "the same overconfidence that led to the mess is now telling them that they can build it better if only they can start the race over."

### Two values, and which one is greater
Software delivers **behavior** (urgent, sometimes important) and **structure** (important, never urgent). Change cost should be proportional to the **scope** of a change, never to its **shape**. Settle the priority by extremes: a program that works perfectly but can't change becomes **useless**; one that's broken but easy to change stays **continually useful**.

On Eisenhower's matrix, architecture sits in quadrants 1–2 and behavior in 1 and 3; the standard organizational error is promoting quadrant 3 (urgent, unimportant) into quadrant 1. Managers aren't equipped to evaluate architecture — that's what developers were hired for. **"If architecture comes last... it means the software development team did not fight hard enough for what they knew was necessary."**

### The three paradigms are three removals
Structured programming removes `goto` (discipline on **direct** transfer of control) → the algorithmic foundation of modules. OO removes function pointers (discipline on **indirect** transfer of control) → the mechanism for **crossing architectural boundaries**. Functional programming removes assignment (discipline on **assignment**) → discipline on the location of and access to data. Each takes something away; none adds capability. "Software is composed of **sequence, selection, iteration, and indirection**. Nothing more. Nothing less."

Testing shows the presence, not the absence, of bugs — so **software is a science, not a mathematics**: we show correctness by failing to prove incorrectness. And only decomposable code can be falsified at all, which is why structural discipline survived the death of formal proof.

**What OO really is, to an architect**: the ability, through safe polymorphism, to gain **absolute control over every source code dependency in the system**. Any dependency can be inverted by inserting an interface — so source code dependencies need not follow the flow of control, which makes details into plugins and yields independent deployability and developability.

### SOLID — mid-level structure
- **SRP** — a module should be responsible to **one, and only one, actor**. Not "do one thing." Symptoms of violation: accidental duplication (a change for the CFO's team silently corrupts the COO's reports) and merges.
- **OCP** — open for extension, closed for modification. Achieved by separating what changes for different reasons (SRP), then ordering the dependencies (DIP). **"If component A should be protected from changes in component B, then component B should depend on component A."**
- **LSP** — implementations must be substitutable without changing the *user's* behavior. Applies to interfaces, duck types, and REST services alike. A violation costs you permanent extra mechanism, not a small bug.
- **ISP** — don't depend on modules containing more than you need. The recompile story is language-specific; the harm (unwanted redeployment, inherited failure modes) is architectural.
- **DIP** — depend on abstractions, not on **volatile** concretions. `java.lang.String` is fine. Four rules: don't refer to, don't derive from, don't override, and never name anything concrete and volatile. DIP violations can't be removed — gather them into `main`.

### Component principles
**Cohesion** (which classes go together): **REP** — the granule of reuse is the granule of release. **CCP** — gather classes that change for the same reasons at the same times (SRP for components). **CRP** — don't force users to depend on what they don't need (ISP for components). REP and CCP are inclusive; CRP is exclusive. Projects start favoring developability and slide toward reuse as consumers appear; expect the partitioning to jitter.

**Coupling**: **ADP** — no cycles (cycles fuse components, destroy build order, and drag the world into unit tests; break them with DIP or a new shared component). **SDP** — depend in the direction of stability. **SAP** — a component should be as abstract as it is stable. SDP + SAP = **DIP for components**.

Stability is not change frequency; it's the **work required to change**, driven by incoming dependencies. Measure with `I = Fan-out/(Fan-in+Fan-out)`, `A = Na/Nc`, and `D = |A + I − 1|`. Avoid the **Zone of Pain** (stable and concrete — database schemas) and the **Zone of Uselessness** (abstract and unused).

**Component structure cannot be designed top-down.** It is "a map to the buildability and maintainability of the application," not a description of its function, so it evolves as the system grows.

### Architecture, boundaries, and details
Architecture is the **shape** of a system — its components, their arrangement, their communication — serving **development, deployment, operation, and maintenance**. The strategy is **to leave as many options open as possible, for as long as possible**. Architects are programmers and keep programming.

**A good architect maximizes the number of decisions not made.** All systems decompose into **policy** (business rules — where the value lives) and **details** (IO devices, databases, web systems, servers, frameworks, protocols). Make the details irrelevant to policy so their decisions can be deferred; if someone already made one, "pretend the decision has not been made."

**Boundaries go on axes of change** — that's the SRP telling you where to draw. **Level = distance from inputs and outputs**; couple dependencies to level, never to data flow. What saps people-power is **coupling to premature decisions**.

**The Dependency Rule**: source code dependencies point only inward, toward higher-level policies. Nothing in an inner circle may name anything in an outer circle — including data formats. Cross against the flow of control with **output ports** implemented by outer-circle classes. Only **simple data structures** cross boundaries, always in the form most convenient for the inner circle — never Entities, never database rows.

**Business rules split in two**: **Entities** hold Critical Business Rules that would exist with no computer at all (a bank charges N% whether a program or a clerk computes it). **Use cases** hold application-specific rules that only make sense inside an automated system, and they "control the dance of the Entities." Entities are *higher* level because they're further from IO and reusable across applications.

**Your architecture should scream the domain, not the framework.** A new programmer should learn all the use cases before discovering how the system is delivered — "Oh, those are details that needn't concern us at the moment."

### The details, one by one
- **The database is a detail.** The *data model* is architecturally significant; the database is a utility for moving bytes between disk and RAM. Databases exist because disks are slow. You already convert stored data into in-memory structures — proof that the storage form was never the architecture. Passing rows around as objects is an architectural error.
- **The web is a detail.** It's one swing of a pendulum that has oscillated between centralized and distributed computing since punched cards. The GUI-is-too-rich objection is partly right — the *dance* resists abstraction — so draw the boundary where input data is complete and execute the use case over plain data structures.
- **Frameworks are details.** The relationship is an **asymmetric marriage**: your commitment is total, the author's is zero, and tight coupling serves them. Use frameworks; don't marry them. When one demands inheritance from its base classes, **derive proxies** in a plugin component. Confine DI frameworks to `main`.
- **Hardware and the OS are details** (embedded). Firmware is defined by dependency, not storage location — you write firmware whenever you bury SQL or platform APIs in business logic. Insert a **HAL** (with an API at the *application's* level: `Indicate_LowBattery()`, not `Led_TurnOn(5)`), a **PAL**, and an **OSAL**. The test: the software runs off-target and off-OS.

### Services, tests, and implementation
**Services are not an architecture.** They are "just function calls across process and/or platform boundaries." The decoupling is largely a fallacy — services are **strongly coupled by the data they share** — and independent deployability holds only where that coupling is absent. The Kitty Problem: one cross-cutting feature forces changes to every microservice. **Architectural boundaries run *through* services, dividing them into components**, not between them.

**Tests are part of the system** — the outermost circle, depending inward, depended on by nothing. Coupled tests are fragile, and fragile tests make production code **rigid** because teams start refusing changes. Don't test through volatile things; build a **testing API** with superpowers whose real job is hiding the *application's structure* from the tests.

**The devil is in the implementation details.** Mark everything `public` and packages become folders, at which point all organizational styles are syntactically identical. Minimize public types and **let the compiler enforce your architecture** — discipline fails under deadline, and static analysis is crude and slow.

### The judgment calls
Boundaries are expensive to build and expensive to retrofit; YAGNI and the retrofit cost are both real. So **watch**: note where boundaries may be needed, look for "the first inkling of friction because those boundaries don't exist," and build "right at the inflection point where the cost of implementing becomes less than the cost of ignoring." Review frequently. And keep the architecture sized to the problem — **"great architectures sometimes lead to great failures."**

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-what-is-design-and-architecture.md) | What Is Design and Architecture? | Design = architecture, the goal, the signature of a mess, "the only way to go fast is to go well" |
| [ch02](chapters/ch02-a-tale-of-two-values.md) | A Tale of Two Values | Behavior vs. structure, scope vs. shape, proof by extremes, Eisenhower's matrix |
| [ch03](chapters/ch03-paradigm-overview.md) | Paradigm Overview | The three paradigms as three removals |
| [ch04](chapters/ch04-structured-programming.md) | Structured Programming | Dijkstra, proof by decomposition, falsifiability, tests as science |
| [ch05](chapters/ch05-object-oriented-programming.md) | Object-Oriented Programming | Encapsulation/inheritance/polymorphism dismantled; dependency inversion; plugin architecture |
| [ch06](chapters/ch06-functional-programming.md) | Functional Programming | Immutability and architecture, segregation of mutability, event sourcing |
| [ch07](chapters/ch07-srp-single-responsibility-principle.md) | SRP | Responsible to one **actor**; accidental duplication; merges |
| [ch08](chapters/ch08-ocp-open-closed-principle.md) | OCP | The protection rule, hierarchy of level, directional control, information hiding |
| [ch09](chapters/ch09-lsp-liskov-substitution-principle.md) | LSP | Liskov's definition, square/rectangle, LSP at architectural scale |
| [ch10](chapters/ch10-isp-interface-segregation-principle.md) | ISP | Segregated interfaces; ISP as an architecture issue, not a language one |
| [ch11](chapters/ch11-dip-dependency-inversion-principle.md) | DIP | Volatile concretions, stable abstractions, Abstract Factory, concentrating violations in `main` |
| [ch12](chapters/ch12-components.md) | Components | Units of deployment; relocatability; linkers; Murphy vs. Moore |
| [ch13](chapters/ch13-component-cohesion.md) | Component Cohesion | REP, CCP, CRP and the tension triangle |
| [ch14](chapters/ch14-component-coupling.md) | Component Coupling | ADP, SDP, SAP; I/A/D metrics; the Main Sequence; zones of exclusion |
| [ch15](chapters/ch15-what-is-architecture.md) | What Is Architecture? | Development/deployment/operation/maintenance; policy vs. details; keeping options open |
| [ch16](chapters/ch16-independence.md) | Independence | Decoupling layers and use cases; true vs. accidental duplication; the three decoupling modes |
| [ch17](chapters/ch17-boundaries-drawing-lines.md) | Boundaries: Drawing Lines | Premature decisions; database behind an interface; IO is irrelevant; plugin architecture |
| [ch18](chapters/ch18-boundary-anatomy.md) | Boundary Anatomy | Monolith, deployment component, local process, service — and what each crossing costs |
| [ch19](chapters/ch19-policy-and-level.md) | Policy and Level | Level = distance from IO; decouple dependencies from data flow |
| [ch20](chapters/ch20-business-rules.md) | Business Rules | Critical Business Rules, Entities, use cases, request/response models |
| [ch21](chapters/ch21-screaming-architecture.md) | Screaming Architecture | The blueprint test; frameworks as tools; testable architectures |
| [ch22](chapters/ch22-the-clean-architecture.md) | The Clean Architecture | The four circles and **the Dependency Rule**; crossing boundaries; the typical scenario |
| [ch23](chapters/ch23-presenters-and-humble-objects.md) | Presenters and Humble Objects | Humble Object pattern; View Models; database gateways; "there is no such thing as an ORM" |
| [ch24](chapters/ch24-partial-boundaries.md) | Partial Boundaries | Skip the last step; Strategy; Facade — and how each decays |
| [ch25](chapters/ch25-layers-and-boundaries.md) | Layers and Boundaries | Hunt the Wumpus; data streams; the watchful-eye doctrine |
| [ch26](chapters/ch26-the-main-component.md) | The Main Component | `main` as the ultimate detail and as a plugin, one per configuration |
| [ch27](chapters/ch27-services-great-and-small.md) | Services: Great and Small | The decoupling fallacy; the Kitty Problem; component-based services |
| [ch28](chapters/ch28-the-test-boundary.md) | The Test Boundary | Tests as the outermost circle; Fragile Tests Problem; the testing API |
| [ch29](chapters/ch29-clean-embedded-architecture.md) | Clean Embedded Architecture | Firmware redefined; App-titude test; HAL, PAL, OSAL |
| [ch30](chapters/ch30-the-database-is-a-detail.md) | The Database Is a Detail | Data model vs. database; "what if there were no disk?"; the RDBMS anecdote |
| [ch31](chapters/ch31-the-web-is-a-detail.md) | The Web Is a Detail | The endless pendulum; the web as an IO device; where to draw the UI boundary |
| [ch32](chapters/ch32-frameworks-are-details.md) | Frameworks Are Details | The asymmetric marriage; the four risks; proxies; Spring in `main` |
| [ch33](chapters/ch33-case-study-video-sales.md) | Case Study: Video Sales | Actors → use cases → components; two dimensions of separation; deployment grouping |
| [ch34](chapters/ch34-the-missing-chapter.md) | The Missing Chapter *(Simon Brown)* | Package by layer/feature/component; ports and adapters; access modifiers; the Périphérique anti-pattern |
| [ch35](chapters/ch35-appendix-a-architecture-archaeology.md) | Appendix A: Architecture Archaeology | 45 years of projects; where SOLID came from; the reusable-framework law |

## Topic Index

- **Abstract Factory** → ch11, ch27, ch33
- **Actors** → ch07, ch33
- **Boundaries (where to draw)** → ch17, ch19, ch25
- **Boundaries (how to cross)** → ch18, ch22
- **Boundaries (partial)** → ch24
- **Business rules / Entities / use cases** → ch20, ch22
- **Component cohesion (REP, CCP, CRP)** → ch13
- **Component coupling (ADP, SDP, SAP)** → ch14
- **Components (definition, history)** → ch12, ch34
- **Database** → ch30, ch17, ch23, ch14
- **Decoupling modes** → ch16, ch18
- **Dependency Rule** → ch22, ch11, ch19
- **Deployment** → ch15, ch16, ch33
- **DIP** → ch11, ch05, ch08
- **Embedded / firmware / HAL** → ch29
- **Event sourcing / immutability** → ch06
- **Frameworks** → ch32, ch21, ch10
- **Humble Object / Presenters / View Models** → ch23, ch22
- **ISP** → ch10, ch13
- **LSP** → ch09
- **`main`** → ch26, ch11, ch32
- **Metrics (I, A, D, Main Sequence)** → ch14
- **Microservices / services** → ch27, ch16, ch18
- **OCP** → ch08, ch13, ch14
- **Package/directory structure** → ch34, ch33
- **Paradigms (structured, OO, functional)** → ch03, ch04, ch05, ch06
- **Plugin architecture** → ch17, ch05, ch26
- **Policy vs. details** → ch15, ch19, ch30, ch31, ch32
- **SRP** → ch07, ch13, ch33
- **Testing / test boundary** → ch28, ch23, ch21, ch04
- **Two values / fighting for architecture** → ch02, ch01
- **Web / GUI** → ch31, ch17, ch21
- **YAGNI vs. retrofit cost** → ch24, ch25

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions and chapter references
- [patterns.md](patterns.md) — the techniques, with when-to-use and trade-offs
- [cheatsheet.md](cheatsheet.md) — decision rules, metrics, tells and smells, the value argument

---

## Scope & Limits

This skill covers the book's content only. Examples are Java/C-era and occasionally dated (Java 9 modules were forthcoming at publication); the principles are language-neutral. Chapter 29 is James Grenning's on embedded systems; Chapter 34 is Simon Brown's on implementation structure, and Brown's definition of "component" deliberately differs from Martin's. For code-level craft — naming, functions, comments, tests, refactoring — see the companion `clean-code` skill. For applying these rules to a specific codebase, combine with project-specific tooling.
