# Patterns & Techniques — Clean Code

## Extract Till You Drop
**When to use**: any function longer than a handful of lines, or one whose body can be divided into named sections.
**How**: extract each section into a function named for what it does. Repeat until every function's statements sit one level of abstraction below its name. Section comments (`// declarations`, `// sieve`) mark the extraction points.
**Trade-offs**: the program gets *longer* — longer names, declarations used as commentary, more whitespace. Longer is correct here; density of meaning per line rises.
(Ch 3, 4, 10)

## The Stepdown Rule
**When to use**: ordering functions within a file.
**How**: after each function, place those one level of abstraction lower. Read the file as a set of "TO *X*, we…" paragraphs descending one level at a time.
**Trade-offs**: opposite of Pascal/C definition-before-use; requires discipline that Martin calls "very difficult for programmers to learn."
(Ch 3, 5)

## Bury the Switch in an Abstract Factory
**When to use**: a `switch`/`if-else` chain over a type code, especially when sibling functions will share the same shape.
**How**: create polymorphic derivatives; put the switch in a factory that creates them; dispatch every other operation through the interface.
**Trade-offs**: the ONE SWITCH rule permits exactly one such switch per selection type. Legitimate to keep the procedural form when new *functions* are more likely than new *types* (Ch 6's anti-symmetry).
(Ch 3, 6, 17/G23)

## Replace Constants with Enums Carrying Behavior
**When to use**: `public static final int` sets, inherited constant interfaces, switches over type codes.
**How**: define an enum; move the envying methods onto it (`Month.quarter()`, `Day.parse()`, `HourlyPayGrade.rate()`); give each enumerator its own method body where behavior varies.
**Trade-offs**: converting is invasive (an hour for `MonthConstants` in SerialDate) but deletes whole categories of validation code and makes later renames safe.
(Ch 16, 17/J2, J3)

## Exceptions Over Error Codes, with Extracted Try/Catch
**When to use**: any operation that can fail.
**How**: throw from the detecting method; extract the `try` body and the `catch` body into their own functions so one function is all error processing and the other is all happy path; `try` must be the first word in its function, with nothing after `catch`/`finally`.
**Trade-offs**: prefer *unchecked* exceptions — checked ones violate OCP by cascading `throws` clauses up the call stack. Checked exceptions remain defensible in critical libraries.
(Ch 3, 7)

## Write the Try-Catch-Finally First
**When to use**: writing code that can throw.
**How**: start with a test that forces the exception, build the `try-catch-finally` skeleton to make it pass, narrow the caught type, then TDD the rest of the logic inside the `try` assuming nothing goes wrong.
**Trade-offs**: none in practice — it builds the transaction scope before the code that depends on it.
(Ch 7)

## SPECIAL CASE Object
**When to use**: a business alternative currently expressed as an exception or a null check.
**How**: return a class that implements the interface and encapsulates the exceptional behavior (`PerDiemMealExpenses.getTotal()` returns the per diem).
**Trade-offs**: adds a type; removes a branch from every client.
(Ch 7)

## Never Return Null, Never Pass Null
**When to use**: any method returning a collection or an optional object.
**How**: return an empty collection (`Collections.emptyList()`), throw, or return a SPECIAL CASE. Forbid null arguments by convention so a null in an argument list is a known defect signal.
**Trade-offs**: `assert` documents the contract but still fails at runtime; a custom `InvalidArgumentException` still needs a handler with no good action. Prohibition is the only real fix.
(Ch 7)

## Wrap the Boundary
**When to use**: any third-party type appearing in your own signatures — `Map`, a logging framework, a vendor's exception zoo.
**How**: hide the foreign interface inside one class exposing only what your application needs; translate its exceptions into a single type of your own; keep boundary types out of public APIs.
**Trade-offs**: an extra class. Buys dependency isolation, mockability, enforceable business rules, and freedom from the vendor's API design.
(Ch 7, 8)

## Learning Tests
**When to use**: adopting an unfamiliar third-party library.
**How**: call the API exactly as you intend to use it, in tests, before touching production code. Re-run them on every upgrade of the package.
**Trade-offs**: free — you had to learn the API anyway — and they turn a risky version migration into an immediate signal.
(Ch 8)

## Write the Interface You Wish You Had
**When to use**: the code on the other side of a boundary doesn't exist yet.
**How**: define your own interface in domain terms, work against it with a fake, and write an ADAPTER when the real API lands. The adapter is the single place to absorb the API's evolution.
**Trade-offs**: the adapter is real work; the seam it creates pays for it in testability.
(Ch 8)

## Domain-Specific Testing Language
**When to use**: tests obscured by setup detail, casting, and construction noise.
**How**: refactor tests into helper functions expressing intent (`makePages`, `submitRequest`, `assertResponseIsXML`). **Never design this API up front** — let it evolve from refactoring tainted tests.
**Trade-offs**: test helpers may trade efficiency for expressiveness (the dual standard) — but never cleanliness.
(Ch 9)

## The Dual Standard
**When to use**: deciding whether test code may differ from production code.
**How**: tests must be simple, succinct, and expressive but need not be as *efficient* — string concatenation instead of `StringBuffer` is fine in a test jig for an embedded system.
**Trade-offs**: the line is efficiency only. "They never involve issues of cleanliness."
(Ch 9)

## Split Classes on Falling Cohesion
**When to use**: instance variables accumulating that only a subset of methods uses — the usual result of shrinking functions and parameter lists.
**How**: separate the co-dependent variables and methods into a new class. Name it; if you can't name it concisely, it's still too big.
**Trade-offs**: more classes, none of them more total complexity. Toolbox with labeled drawers vs. drawers you toss things into.
(Ch 10)

## Refactor to a Set of Closed Classes (OCP)
**When to use**: a class you keep having to open — e.g. an `Sql` builder that changes both when statement types are added and when a statement type's details change.
**How**: make the base abstract with one operation (`generate()`); give each public method its own derivative; move private helpers to where they're needed; extract shared behavior into small utilities.
**Trade-offs**: many small classes; adding a new feature touches **no existing class**.
(Ch 10)

## Isolate from Change with an Interface (DIP)
**When to use**: a class depends on a volatile or slow concrete collaborator (`TokyoStockExchange`).
**How**: extract an interface naming the abstract capability (`StockExchange.currentPrice(symbol)`); inject it through the constructor; substitute a stub in tests.
**Trade-offs**: an interface plus a stub. What you get is testability, which is the same property as flexibility.
(Ch 10)

## Separate Construction from Use (Main / Factory / DI)
**When to use**: any application with non-trivial startup wiring.
**How**: three escalating options — move all construction to `main` (dependencies point away from `main`); use an ABSTRACT FACTORY when the application must control creation *timing*; use a DI container when wiring is large or configuration-driven.
**Trade-offs**: lazy initialization is convenient and scatters the global setup strategy; DI containers add a framework but usually only a couple of lines of framework-specific code.
(Ch 11)

## POJOs + Aspects
**When to use**: cross-cutting concerns — persistence, transactions, security, caching, failover.
**How**: write domain logic as framework-free POJOs; declare infrastructure separately (Spring/JBoss AOP configuration or annotations; AspectJ for the hard 10–20%).
**Trade-offs**: Java proxies are verbose and cannot express system-wide execution points; AspectJ is full-featured but demands new tools and idioms.
(Ch 11)

## TEMPLATE METHOD for Algorithmic Duplication
**When to use**: two or more methods sharing a shape and differing in one step.
**How**: put the algorithm and its invariant steps in the base class; make the varying step abstract; subclasses fill the hole.
**Trade-offs**: introduces inheritance. STRATEGY is the composition alternative for the same duplication.
(Ch 12, 17/G5)

## Isolate the Threading Policy
**When to use**: any concurrent system.
**How**: put all thread management behind one interface (`ClientScheduler`) with nothing else in it; make everything else a thread-ignorant POJO. Swapping thread-per-request for an `Executor` pool then means writing one class.
**Trade-offs**: none. It is what makes concurrency testable, instrumentable, and tunable at all.
(Ch 13, App A)

## Server-Based Locking
**When to use**: a shared object whose clients must call more than one method (`hasNext()` then `next()`).
**How**: change the server's API to be multithread-aware — one method that does the composite operation (`getNextOrNull()`). If you don't own the server, wrap it in an ADAPTER, or use a thread-safe collection with extended operations (`putIfAbsent`).
**Trade-offs**: changes the API. Preferable to client-based locking on every axis: no duplication, one policy, one place to look, swappable for a non-locking version in single-threaded deployment, and no client can forget.
(Ch 13, App A)

## Nonblocking Updates (CAS)
**When to use**: a shared counter or reference updated by multiple threads.
**How**: `AtomicInteger`/`AtomicBoolean`/`AtomicReference` instead of `synchronized`. Optimistic: detect interference and retry, rather than always acquiring a lock.
**Trade-offs**: object instead of primitive, `incrementAndGet()` instead of `++`. "The cases where it will be slower are virtually nonexistent."
(App A)

## Break One Deadlock Condition
**When to use**: any system with multiple limited resource pools.
**How**: pick the cheapest of the four to break — usually **circular wait**, via a global resource ordering all threads honor.
**Trade-offs**: ordering may not match use order (resources held longer than needed) and is infeasible when resource 2's identity comes from operating on resource 1. Breaking lock & wait risks starvation and livelock; breaking preemption means managing a request protocol.
(Ch 13, App A)

## Jiggling / ConTest Instrumentation
**When to use**: hunting threading bugs that appear once in millions of iterations.
**How**: insert `ThreadJigglePoint.jiggle()` calls; give the class two implementations — a no-op for production, a randomized sleep/yield/fall-through for tests. Or use IBM's ConTest.
**Trade-offs**: hand-placed `yield()` calls are a shotgun approach and slow production if left in. Measured effect of instrumentation: failure rate from ~1 in 10,000,000 to ~1 in 30.
(Ch 13, App A)

## Successive Refinement Under Test
**When to use**: restructuring anything — your own draft or someone else's module.
**How**: get a behavior-verifying test suite first; add the new concept's skeleton where it can break nothing; make the smallest possible change; fix every break before the next change; repeat. Never rewrite.
**Trade-offs**: intermediate states are knowingly imperfect (all marshalling in the base class before it's pushed to derivatives). That is the point — the system works at every step.
(Ch 14, 15, 16)

## Encapsulate Conditionals and Boundary Conditions
**When to use**: any compound boolean in an `if`/`while`, or a `+1`/`-1` appearing more than once.
**How**: extract a named predicate (`shouldBeDeleted(timer)`); name the boundary expression (`int nextLevel = level + 1;`). Prefer positive conditionals over negative ones.
**Trade-offs**: none. Off-by-one clutter usually signals a misnamed variable — fixing the concept simplifies the arithmetic (`suffixIndex` → `suffixLength`).
(Ch 15, 17/G28, G29, G33)

## Bucket Brigade for Temporal Coupling
**When to use**: functions that must be called in a specific order.
**How**: have each produce what the next consumes, so out-of-order calls don't compile. Keep the instance variables if private methods need them; add the arguments anyway to make the coupling explicit.
**Trade-offs**: more syntactic complexity, which "exposes the true temporal complexity of the situation." A parameter that merely *implies* ordering (without a data reason) is arbitrary and will be removed by the next person.
(Ch 15, 17/G31, G32)
