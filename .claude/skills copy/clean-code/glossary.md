# Glossary — Clean Code

**Active Record** — A DTO with navigational methods like `save` and `find`, usually a direct translation of a database table. Treat as a data structure; put business rules in separate objects. (Ch 6)

**Argument object** — A class wrapping variables that are always passed together; the fix for functions needing 3+ arguments. (Ch 3)

**Aspect** — A modular construct specifying which points in a system have their behavior modified for a cross-cutting concern, applied noninvasively. (Ch 11)

**Atomic operation** — Any uninterruptable operation. 32-bit assignment is atomic in the JVM; 64-bit assignment and `++` are not. (App A)

**BDUF (Big Design Up Front)** — Designing everything before implementing anything. Harmful in software; not the same as ordinary up-front design. (Ch 11)

**Bound resource** — A resource of fixed size or number used concurrently (DB connections, fixed-size buffers). (Ch 13)

**Boy Scout Rule** — "Leave the campground cleaner than you found it." Check code in slightly cleaner than you checked it out. (Ch 1, 15, 16)

**Broken windows** — One unrepaired defect signals nobody cares, inviting further decay. (Ch 1)

**BUILD-OPERATE-CHECK** — The three-part structure of a clean test: build the data, operate on it, check the result. (Ch 9)

**CAS (Compare and Swap)** — An atomic processor operation underlying nonblocking updates; optimistic locking, versus `synchronized`'s pessimistic locking. (App A)

**Code-sense** — The acquired aesthetic that lets a programmer see not just that code is a mess but which transformations will clean it. (Ch 1)

**Command Query Separation** — A function either does something or answers something, never both. (Ch 3)

**Critical section** — Code that must be protected from simultaneous use for the program to be correct. (Ch 13)

**Cross-cutting concern** — Persistence, transactions, security, caching, failover: concerns cutting across natural object boundaries. (Ch 11)

**Deadlock** — Two or more threads each holding a resource the other needs. Requires all four of: mutual exclusion, lock & wait, no preemption, circular wait. (Ch 13, App A)

**Defactoring** — Deliberately degrading clean code to show what its structure was buying. (Ch 15)

**Dependency Injection (DI)** — Inversion of Control applied to dependency management; the class is completely passive about resolving its dependencies. (Ch 11)

**Dependency Inversion Principle (DIP)** — Depend on abstractions, not on concrete details. (Ch 10)

**Dependency magnet** — A class or enum everything imports, so any change forces recompilation everywhere (e.g. a global `Error` enum). (Ch 3)

**Dining Philosophers** — The classic model of threads competing for adjacent resources; the shape of enterprise resource contention. (Ch 13)

**DRY (Don't Repeat Yourself)** — Hunt & Thomas's principle; Beck's "Once, and only once." "Duplication may be the root of all evil in software." (Ch 3, 12, 17)

**DSL (Domain-Specific Language)** — A small language or API letting code read like structured prose a domain expert would write. (Ch 11)

**DTO (Data Transfer Object)** — A class with public variables and no functions; the quintessential data structure. (Ch 6)

**Dummy scope** — A `while`/`for` with an empty body; brace it and indent the semicolon or an invisible `;` will fool you. (Ch 5)

**Explaining/explanatory temporary variables** — Named intermediate values that make a calculation readable. "It is hard to overdo this." (Ch 16, G19)

**F.I.R.S.T.** — Fast, Independent, Repeatable, Self-Validating, Timely: the five properties of clean tests. (Ch 9)

**Feature Envy** — A method more interested in another class's data than its own. Sometimes a necessary evil. (Ch 6, 17/G14)

**Flag argument** — A boolean parameter; it announces that the function does more than one thing. (Ch 3, 17/F3)

**Frame** — Per-invocation storage for return address, parameters, and local variables. (App A)

**Future** — A handle to a result computed concurrently; `get()` blocks until it completes. (App A)

**God class** — A class with far too many responsibilities, e.g. `SuperDashboard` with ~70 public methods. (Ch 10)

**Hybrid** — Half object, half data structure: real behavior plus exposed state. "The worst of both worlds." (Ch 6)

**Implicity** — The degree to which context is *not* explicit in the code itself. (Ch 2)

**Keyword form** — Encoding argument names into a function name: `assertExpectedEqualsActual(expected, actual)`. (Ch 3)

**LAZY INITIALIZATION/EVALUATION** — Constructing on first use. Real merits, but hard-codes dependencies and scatters the global setup strategy. "Just an optimization and perhaps premature." (Ch 11)

**Learning test** — A test written against a third-party API to check your understanding of it. Free, because you had to learn the API anyway. (Ch 8)

**LeBlanc's Law** — "Later equals never." (Ch 1)

**Livelock** — Threads in lockstep, each finding another in the way, making no progress. (Ch 13)

**Magic number** — Any token whose value is not self-describing — including strings, not just numbers. (Ch 17/G25)

**Mental mapping** — Forcing the reader to translate your name into the concept they hold. Clarity is king. (Ch 2)

**Monadic / dyadic / triadic / polyadic** — Functions of one / two / three / many arguments. (Ch 3)

**Monte Carlo Testing** — Tunable tests run repeatedly with randomized tuning values to shake out rare failures. (App A)

**Newspaper Metaphor** — A source file should read top-down: headline name, high-level concepts, increasing detail. (Ch 5)

**Niladic** — Taking zero arguments; the ideal. (Ch 3)

**Noise word** — A word added to differentiate that carries no meaning: `Info`, `Data`, `Object`, `the`. (Ch 2)

**ONE SWITCH rule** — No more than one switch statement per type of selection, and its cases must create the polymorphic objects that replace the others. (Ch 17/G23)

**Open-Closed Principle (OCP)** — Open for extension, closed for modification. (Ch 10)

**Operand stack** — LIFO structure holding JVM instruction parameters. (App A)

**Output argument** — A parameter used to return data; forces a signature check. In OO, `this` is the natural output argument. (Ch 3)

**POJO (Plain Old Java Object)** — An object focused purely on its domain, free of framework dependencies. (Ch 11, 13)

**Principle of Least Surprise / Least Astonishment** — Any function or class should implement the behavior another programmer could reasonably expect. (Ch 17/G2, G11, G17)

**Producer-Consumer** — Producers place work in a bound queue; consumers take it out; both signal each other. (Ch 13)

**Readers-Writers** — A shared resource read often and written occasionally; the difficulty is balancing throughput, staleness, and starvation. (Ch 13)

**Reuse in the small** — Extracting tiny commonalities, which raises visibility and enables larger reuse. "Essential to achieving reuse in the large." (Ch 12)

**Seam** — A point where a test double can be substituted for a real collaborator. (Ch 8)

**Selector argument** — Any argument (boolean, enum, int) passed to choose behavior. "A lazy way to avoid splitting a large function." (Ch 17/G15)

**Side effect** — A hidden state change. "Side effects are lies." Creates temporal coupling. (Ch 3)

**Simple Design, four rules of** (Beck) — Runs all the tests; contains no duplication; expresses the intent of the programmer; minimizes the number of classes and methods. In priority order. (Ch 12)

**Single Responsibility Principle (SRP)** — A class or module should have one, and only one, reason to change. (Ch 10)

**SPECIAL CASE PATTERN** — A class or configured object that handles the exceptional case, so clients never branch on it. (Ch 7)

**Starvation** — A thread or group prohibited from proceeding for an excessively long time or forever. (Ch 13)

**Stepdown Rule** — Each function is followed by those at the next level of abstraction, so the file reads as a descending narrative. (Ch 3)

**Structured programming** — Dijkstra's one-entry/one-exit discipline. Little benefit in small functions; `goto` still avoided. (Ch 3)

**Temporal coupling** — A function that can only be called at certain times or in a certain order. Make it structural, never conventional. (Ch 3, 15, 17/G31)

**TO paragraph** — Describing a function as "TO *FunctionName*, we…" to test whether it does one thing. From LOGO's `TO` keyword. (Ch 3)

**Train wreck** — A chain of calls like `a.getB().getC().doSomething()`. Whether it violates Demeter depends on whether the links are objects or data structures. (Ch 6, 17/G36)

**Three Laws of TDD** — No production code before a failing test; no more test than suffices to fail (not compiling is failing); no more production code than suffices to pass. (Ch 9)

**Ubiquitous language** (Evans) — A team's standard system of names for a project, used extensively in the code. (Ch 17/N3)

**Vertical openness / density** — Blank lines separate concepts; adjacency binds related lines. (Ch 5)

**Wading** — Slogging through bad code hunting for the thread of reasoning. (Ch 1)
