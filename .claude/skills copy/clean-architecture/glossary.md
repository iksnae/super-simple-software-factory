# Glossary — Clean Architecture

**A (Abstractness)** — `Na / Nc`: abstract classes and interfaces over total classes in a component. Range [0, 1]. (Ch 14)

**Abstract component** — A component containing nothing but interfaces; no executable code. Very stable, and an ideal target for less stable components to depend on. Doesn't exist in dynamically typed languages. (Ch 14)

**Abstract use case** — A use case that sets a general policy which another use case fleshes out (e.g. `View Catalog` inherited by `View Catalog as Viewer` and `as Purchaser`). (Ch 33)

**Acyclic Dependencies Principle (ADP)** — Allow no cycles in the component dependency graph. (Ch 14)

**Actor** — One or more people who require the same change; the unit SRP is actually about. (Ch 7)

**App-titude test** — Getting the app to work, and nothing more. Passing it is not the job. (Ch 29)

**Asymmetric marriage** — The framework relationship: your commitment is total, the author's is zero. (Ch 32)

**BCE** — Boundary/Control/Entity, Ivar Jacobson's architecture from *Object Oriented Software Engineering*. One of the Clean Architecture's three antecedents. (Ch 22)

**Boundary** — A line separating software elements and restricting what one side may know about the other. Drawn where there is an axis of change. (Ch 17)

**Bucket brigade** — Structuring functions so each produces what the next consumes, making a required call order impossible to violate. (Clean Code G31; used in Ch 17-adjacent reasoning)

**C4 model** — Simon Brown's hierarchy: a software system contains containers, which contain components, which are implemented by classes. (Ch 34)

**Central Transform** — Meilir Page-Jones's name for the highest-level component: the one farthest from inputs and outputs. (Ch 19, Ch 25)

**Common Closure Principle (CCP)** — Gather into components classes that change for the same reasons at the same times. SRP for components. (Ch 13)

**Common Reuse Principle (CRP)** — Don't force users of a component to depend on things they don't need. ISP generalized. (Ch 13)

**Component** — Martin: the unit of deployment (jar, gem, DLL). Brown: a grouping of related functionality behind a clean interface, residing inside an execution environment. (Ch 12, Ch 34)

**Critical Business Data** — Data that would exist even if the system were not automated (loan balance, rate, schedule). (Ch 20)

**Critical Business Rules** — Rules that make or save money irrespective of whether a computer implements them. (Ch 20)

**D (Distance)** — `|A + I − 1|`. 0 = on the Main Sequence, 1 = as far from it as possible. (Ch 14)

**Data mapper** — What an ORM actually is: it loads data into data structures from relational tables. "There is no such thing as an object relational mapper." (Ch 23)

**DCI** — Data, Context, Interaction; Coplien and Reenskaug. A Clean Architecture antecedent. (Ch 22)

**Decoupling mode** — Source level, deployment level, or service level. Itself an option to leave open. (Ch 16)

**Dependency Injection (DI)** — Inversion of Control applied to dependency management; the class is passive about resolving its dependencies. (Clean Code Ch 11; Ch 26, Ch 32)

**Dependency Inversion Principle (DIP)** — Source code dependencies should refer only to abstractions, not to volatile concretions. (Ch 11)

**Dependency Rule** — "Source code dependencies must point only inward, toward higher-level policies." Nothing in an inner circle may name anything in an outer circle, including data formats. (Ch 22)

**Details** — Everything necessary to communicate with policy that does not affect policy's behavior: IO devices, databases, web systems, servers, frameworks, protocols, hardware. (Ch 15, Ch 29–32)

**Device independence** — Writing programs against abstract IO services rather than specific devices. Invented in the late 1960s; the OCP "born but not yet named." (Ch 15)

**Entity** — An object embodying a small set of Critical Business Rules operating on Critical Business Data. Needs no OO language — only a single separate module binding rules to data. (Ch 20)

**Event sourcing** — Store the transactions, not the state; derive state by replaying them. Makes applications CR rather than CRUD, eliminating concurrent update problems. (Ch 6)

**Fan-in / Fan-out** — Incoming / outgoing dependencies of a component. (Previously called afferent and efferent couplings, Ca and Ce.) (Ch 14)

**Firmware** — Not code that lives in ROM. Code defined by what it depends on and how hard it is to change as hardware evolves. Burying SQL or platform APIs in business logic is writing firmware. (Ch 29)

**Fragile Tests Problem** — Tests coupled to the system break en masse on trivial changes, which makes the production code rigid because teams stop making changes. (Ch 28)

**HAL (Hardware Abstraction Layer)** — The boundary between software and firmware. Its API is tailored to the software's needs, not the hardware's. (Ch 29)

**Hexagonal Architecture** — Ports and Adapters; Alistair Cockburn. A Clean Architecture antecedent. (Ch 22)

**Humble Object pattern** — Split behaviors into a humble module (hard to test, stripped to essentials) and a testable one. Found near every architectural boundary. (Ch 23)

**I (Instability)** — `Fan-out / (Fan-in + Fan-out)`. 0 = maximally stable, 1 = maximally unstable. (Ch 14)

**Interface Segregation Principle (ISP)** — Don't depend on modules containing more than you need. (Ch 10)

**Kitty Problem** — The taxi-aggregator example where one cross-cutting feature forces changes to every microservice. (Ch 27)

**Level** — "The distance from the inputs and outputs." Farther = higher level. (Ch 19)

**Liskov Substitution Principle (LSP)** — Subtypes must be substitutable such that a program's behavior is unchanged. Extends to interfaces, duck types, and REST services. (Ch 9)

**Main** — The ultimate detail; the lowest-level policy; the dirtiest component. Creates everything and hands over control. Best treated as a plugin, one per configuration. (Ch 26)

**Main Sequence** — The line from (1,0) to (0,1) on the A/I graph; the locus maximally distant from both zones of exclusion. (Ch 14)

**Morning after syndrome** — Arriving to find your work broken because someone changed what you depend on. What ADP prevents. (Ch 14)

**OSAL (Operating System Abstraction Layer)** — Isolates software from the RTOS or OS. (Ch 29)

**Open-Closed Principle (OCP)** — A software artifact should be open for extension but closed for modification. (Ch 8)

**Output port / Input port** — Boundary interfaces owned by the inner circle, implemented by the outer, letting control flow outward while dependencies point inward. (Ch 22)

**PAL (Processor Abstraction Layer)** — Isolates firmware from vendor C extensions and register access. (Ch 29)

**Package by component** — Bundle all responsibilities for a coarse-grained component into one package with a single public interface. Brown's recommendation. (Ch 34)

**Package by feature / by layer** — Vertical vs. horizontal slicing of code into packages. (Ch 34)

**Partial boundary** — A placeholder for a full boundary: skip-the-last-step, one-dimensional (Strategy), or Facade. (Ch 24)

**Périphérique anti-pattern** — With all infrastructure in one source tree, a web controller can call a repository directly, circumnavigating the domain. (Ch 34)

**Plugin architecture** — Core business rules kept independent of components that are optional or implementable many ways; changes cannot propagate across the firewall. (Ch 17, Ch 5)

**Policy** — A statement of how inputs are transformed into outputs. All software is policy. (Ch 19)

**POJO** — Plain Old Java Object; domain-focused, no framework dependencies. (Clean Code Ch 11; Ch 29)

**Relaxed layered architecture** — Layers permitted to skip their adjacent neighbors. Sometimes intended (CQRS); often a defect. (Ch 34)

**Request/Response models** — Simple data structures crossing a use case boundary, depending on nothing — no `HttpRequest`, no framework base types, no Entity references. (Ch 20, Ch 22)

**Reuse/Release Equivalence Principle (REP)** — The granule of reuse is the granule of release. (Ch 13)

**Screaming architecture** — A structure that announces its domain ("HOME," "LIBRARY," "health care system") rather than its framework. (Ch 21)

**Scope vs. shape** — Change difficulty should be proportional to the *scope* of a change, never to its *shape*. (Ch 2)

**Segregation of mutability** — Splitting an application into immutable components and mutable ones protected by transactional memory. (Ch 6)

**Single Responsibility Principle (SRP)** — A module should be responsible to one, and only one, actor. *Not* "a module should do one thing." (Ch 7)

**Stable Abstractions Principle (SAP)** — A component should be as abstract as it is stable. (Ch 14)

**Stable Dependencies Principle (SDP)** — Depend in the direction of stability; I should decrease along dependency edges. (Ch 14)

**Stability** — Not change frequency, but the work required to change. Driven by incoming dependencies. (Ch 14)

**Structural coupling** — Tests mirroring production structure class-for-class and method-for-method; the most insidious form of test coupling. (Ch 28)

**Target-hardware bottleneck** — Being able to test embedded code only on the target. (Ch 29)

**Testing API** — A superset of the interactors and interface adapters, with superpowers to bypass security and expensive resources and to force testable states. (Ch 28)

**Transactional memory** — Treating in-memory variables the way a database treats records, with transaction- or retry-based protection. (Ch 6)

**True vs. accidental duplication** — True: every change to one requires the same change to all. Accidental: they will diverge over time. Unifying accidental duplicates makes later separation hard. (Ch 16)

**Ubiquitous language** — Eric Evans's term; naming on the "inside" uses the domain's language (`Orders`, not `OrdersRepository`). (Ch 34; Clean Code N3)

**Use case** — A description of how an automated system is used: inputs, processing, outputs. Application-specific rules that control the dance of the Entities. (Ch 20)

**View Model** — A plain object of strings, booleans, and enums holding everything on the screen the application controls, so the View makes no decisions. (Ch 22, Ch 23)

**YAGNI** — "You Aren't Going to Need It." Real wisdom, in tension with the cost of adding a boundary later. (Ch 24, Ch 25)

**Zone of Pain** — (0,0) on the A/I graph: stable and concrete. Database schemas live here. Harmless only if nonvolatile. (Ch 14)

**Zone of Uselessness** — (1,1): maximally abstract with no dependents. Leftover abstractions nobody implemented. (Ch 14)
