# Patterns & Techniques — Clean Architecture

## Invert a Dependency with an Interface
**When to use**: any time a source code dependency points the wrong way — from policy toward detail, or from a stable component toward a volatile one.
**How**: define the interface on the **higher-level (consuming) side**; have the lower-level module implement it. Source dependencies then oppose the flow of control.
**Trade-offs**: an extra type, and an apparent contradiction in the diagram (control goes one way, arrows the other) that readers must be taught. This is the single lever behind plugins, testability, and independent deployability.
(Ch 5, 11, 18, 22)

## Concentrate DIP Violations in `main`
**When to use**: always — something must eventually name the concrete classes.
**How**: `main` instantiates factories and implementations, places them behind abstract types, and hands control to the high-level policy. Let the DI framework operate only here; distribute dependencies normally afterward.
**Trade-offs**: `main` is knowingly dirty. That is the point — it is one small component, outside the boundary, and nothing depends on it.
(Ch 11, 26, 32)

## Abstract Factory for Creation Across a Boundary
**When to use**: an inner circle needs instances of an outer-circle type; object creation inherently requires a dependency on the concrete definition.
**How**: the application depends on a `ServiceFactory` interface and a `Service` interface; a `ServiceFactoryImpl` on the concrete side instantiates and returns the concretion as the abstraction.
**Trade-offs**: two extra interfaces per creation site. Buys full inversion, including creation timing under the application's control.
(Ch 11, 27, 33)

## Put the Database Behind a Gateway Interface
**When to use**: any persistent storage.
**How**: the business rules define a gateway interface with a method per operation they need (`getLastNamesOfUsersWhoLoggedInAfter(Date)`), owned by the business-rules component. The database component implements it and holds all SQL.
**Trade-offs**: you write method-per-query interfaces instead of ad-hoc SQL. Buys: the database becomes replaceable, the decision deferrable, the business rules unit-testable with stubs, and tests that run fast because no database exists.
(Ch 17, 22, 23, 30)

## Defer the Database Decision Into Nonexistence
**When to use**: early in a project, when the storage decision is not yet forced.
**How**: FitNesse's sequence — a stubbed mock, then an in-memory hash table, then flat files, then (only if ever needed) a real database via a new derivative.
**Trade-offs**: none until scale demands otherwise. Eighteen months without schema issues, query issues, server issues, password issues, connection-time issues — and fast tests.
(Ch 17)

## Humble Object at Every Boundary
**When to use**: wherever hard-to-test behavior abuts easy-to-test behavior.
**How**: strip the untestable side to its barest essence (View, gateway implementation, data mapper, service listener) and move every decision to the testable side (Presenter, interactor, application).
**Trade-offs**: one more class per boundary and a data structure between them. Buys near-total testability — the untestable remainder contains nothing capable of being interestingly wrong.
(Ch 23)

## Presenter → View Model → View
**When to use**: any user interface.
**How**: the interactor produces `OutputData` (plain object, may hold `Date`/`Currency`); the Presenter formats it into a **ViewModel** of strings, booleans, and enums — including button names and greyed-out flags; the View only moves ViewModel values onto the screen.
**Trade-offs**: three data objects where one might do. Buys a View with no decisions in it, and assertions on formatting and enablement without a screen.
(Ch 22, 23)

## Cross a Boundary Against the Flow of Control (Output Port)
**When to use**: an inner circle needs to invoke something in an outer circle.
**How**: the inner circle declares an interface (the *output port*) and calls it; the outer circle implements it. The inner circle never names the outer class.
**Trade-offs**: indirection. It is the only way to obey the Dependency Rule when control must flow outward.
(Ch 22, 18)

## Pass Only Simple Data Structures Across Boundaries
**When to use**: every boundary crossing.
**How**: basic structs, DTOs, function arguments, or a hashmap — always in the form most convenient for the **inner** circle. Never Entity objects, never database row structures, never framework types.
**Trade-offs**: copying and mapping code. Prevents an inner circle from acquiring knowledge of an outer one, which is the failure mode that quietly ends the architecture.
(Ch 20, 22)

## Break a Dependency Cycle
**When to use**: the moment a cycle appears in the component dependency graph.
**How**: two options — (1) apply DIP: put an interface in the upstream component and have the downstream one inherit it; (2) extract a new component holding what both depend on.
**Trade-offs**: option 2 makes the component structure grow and jitter. Expect to monitor continuously; cycles fuse components, destroy build order, and drag the world into unit tests.
(Ch 14)

## Repair an SDP Violation
**When to use**: a stable component has acquired a dependency on a component designed to be volatile.
**How**: extract an interface declaring exactly what the stable side needs, put it in its own **abstract component**, and have the volatile class implement it. Both now depend on the abstract component (I = 0), and the volatile one keeps its instability (I = 1).
**Trade-offs**: a component containing nothing but an interface — normal and necessary in statically typed languages, unnecessary in dynamic ones.
(Ch 14)

## Partial Boundary — Skip the Last Step
**When to use**: you judge a full boundary's cost too high but want to hold the place.
**How**: build the reciprocal interfaces and input/output structures completely, then compile and deploy everything as one component.
**Trade-offs**: full design and code cost, zero release-management cost. Decays if the boundary never materializes and nobody is enforcing it (FitNesse's web component).
(Ch 24)

## Partial Boundary — Strategy or Facade
**When to use**: cheaper placeholders when even the full design cost is unjustified.
**How**: Strategy — a `ServiceBoundary` interface used by clients, implemented by `ServiceImpl` (dependency inversion in one direction). Facade — a class listing services as methods, delegating to classes clients shouldn't touch (no inversion at all).
**Trade-offs**: Strategy allows backchannels that only discipline prevents. Facade adds transitive client dependencies and recompilation on any service change.
(Ch 24)

## Package by Component with Restrictive Access Modifiers
**When to use**: monolithic applications in languages with package-level access control.
**How**: bundle business logic and persistence for one concept into one package; expose exactly one public interface (`OrdersComponent`); make everything else package-protected. In .NET use `internal` with one assembly per component.
**Trade-offs**: coarser packages than package-by-layer. Buys **compiler-enforced** architecture — no discipline, no code review, no static-analysis rules, no delayed feedback.
(Ch 34)

## Separate Source Trees as a Decoupling Mode
**When to use**: when language access modifiers are insufficient and you want compile-time enforcement across larger units.
**How**: separate build modules/projects — ideally one per component; at minimum domain ("inside") and infrastructure ("outside"), with a compile-time dependency running only inward.
**Trade-offs**: "very much an idealistic solution" at full granularity — real performance, complexity, and maintenance costs. The two-tree version invites the **Périphérique anti-pattern**.
(Ch 34)

## HAL / PAL / OSAL for Embedded Code
**When to use**: any embedded system that must outlive its hardware, processor, or RTOS.
**How**: a HAL between software and firmware whose API speaks the *application's* language (`Indicate_LowBattery()`, name/value pairs) rather than the hardware's (`Led_TurnOn(5)`, flash bytes); a PAL confining vendor C extensions and register access; an OSAL wrapping the RTOS API.
**Trade-offs**: extra layers and some duplication concentrated in one place. Buys off-target, off-OS testability — the escape from the target-hardware bottleneck.
(Ch 29)

## Write Your Own `stdint.h`
**When to use**: a vendor toolchain supplies a proprietary types header you cannot compile without.
**How**: create a `stdint.h` that includes the vendor header and typedefs the standard names onto its types. Every other file includes yours.
**Trade-offs**: one file of ceremony. Confines the vendor dependency to a single location and makes off-target compilation possible.
(Ch 29)

## Replace Mass Conditional Compilation with a HAL
**When to use**: `#ifdef BOARD_V2` appearing more than a handful of times.
**How**: make board type a detail hidden under the HAL, and bind the implementation with the linker or at runtime instead of the preprocessor.
**Trade-offs**: build configuration replaces source conditionals. "If I see `#ifdef BOARD_V2` once, it's not really a problem. Six thousand times is an extreme problem."
(Ch 29)

## Wrap a Framework in Proxies
**When to use**: a framework demands that you derive your business objects from its base classes.
**How**: say no. Derive **proxies** in a plugin component that delegate to untouched business objects. Keep the framework in an outer circle; confine DI frameworks to `main`.
**Trade-offs**: a proxy class per integration point. Buys business objects that compile, run, and test with no framework present, and a migration path that touches one component.
(Ch 32)

## Component-Based Services
**When to use**: you have (or want) services, and you also want cross-cutting features not to require touching every one of them.
**How**: give each service an internal component structure following the Dependency Rule. Abstract classes in one jar; each new feature in another jar of derivatives, via Template Method or Strategy.
**Trade-offs**: more design inside each service. Deploying a feature becomes adding jars to load paths rather than redeploying services — OCP at service scale.
(Ch 27)

## Testing API
**When to use**: any system whose business rules would otherwise be verified through the UI.
**How**: build an API that is a superset of the interactors and interface adapters, with superpowers to bypass security, skip expensive resources, and force testable states. Its real job is hiding **application structure** from tests.
**Trade-offs**: an extra surface to maintain, and a security question — if the superpowers are dangerous, ship the API in a separate, independently deployable component.
(Ch 28)

## Watch for the Boundary Inflection Point
**When to use**: continuously, for every boundary you chose not to build.
**How**: note where boundaries may be required; watch for "the first inkling of friction because those boundaries don't exist"; weigh implementing vs. ignoring; review frequently; build "right at the inflection point where the cost of implementing becomes less than the cost of ignoring."
**Trade-offs**: requires sustained attention rather than a one-time decision. Both errors are real — over-engineering is often worse than under-engineering, and retrofitting a missing boundary is expensive even with good tests and refactoring discipline.
(Ch 25)
