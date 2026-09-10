---
name: clean-code
description: "Knowledge base from \"Clean Code: A Handbook of Agile Software Craftsmanship\" by Robert C. Martin (with Tim Ottinger, Michael Feathers, James Grenning, Jeff Langr, Brett Schuchert, Kevin Wampler). Use when applying Martin's practices for naming, functions, comments, formatting, error handling, boundaries, unit tests, classes, systems, emergence, concurrency, refactoring, and code smells — or when reviewing code, doing TDD, or studying the book."
---

<!-- argument-hint: [topic, heuristic ID like G34/N5/T7, or chapter number] -->

# Clean Code: A Handbook of Agile Software Craftsmanship
**Author**: Robert C. Martin (Uncle Bob), with contributors | **Pages**: ~462 | **Chapters**: 17 + Appendix A | **Generated**: 2026-08-29

## How to Use This Skill

- **Without arguments** — load the core practices below for reference
- **With a topic** — ask about `naming`, `function arguments`, `error handling`, `deadlock`, `TDD`; I find and read the relevant chapter
- **With a heuristic ID** — ask for `G34`, `N5`, `T7`, `C2`; ch17 holds the full catalogue
- **With a chapter** — ask for `ch09`; I load that file
- **Browse** — ask "what chapters do you have?"

When you ask about something not in Core Practices below, I read the relevant chapter file before answering.

---

## Core Practices

### The premise
Bad code is not a schedule problem. **The only way to go fast is to keep the code clean at all times** — a mess slows you down instantly, not eventually. **LeBlanc's Law: later equals never.** The reading-to-writing ratio is well over 10:1, so optimize for reading even when it makes writing harder. **The Boy Scout Rule**: check code in a little cleaner than you checked it out — one renamed variable, one split function, one removed duplication.

Working code is not the bar. "Code that works is often badly broken. Programmers who satisfy themselves with merely working code are behaving unprofessionally."

### Names
A name must answer *why it exists, what it does, how it is used*. **If a name needs a comment, the name failed.** Names that differ must *mean* something different — reject noise words (`Info`, `Data`, `Object`) and number series. **Name length tracks scope length**: `i` is right in five lines, wrong across a class. Drop encodings (`m_`, `f`, `IShapeFactory`). One word per concept, and never one word for two concepts. Prefer giving related variables a class over prefixing them, so the compiler enforces the context. Renaming is cheap — do it as soon as you find better.

### Functions
**Small, then smaller.** Rarely 20 lines; block bodies one line; indent depth one or two. A function does **one thing** when every statement sits one level of abstraction below its name — test it by describing it as "TO *X*, we…", or by asking whether you can extract a function whose name isn't a restatement of the implementation. Order functions by the **Stepdown Rule** so the file descends one level at a time.

Arguments: **0 > 1 > 2 > 3+**. Flag arguments announce that the function does two things — split it. Output arguments force a signature check — change the state of the owning object instead. **Side effects are lies**; they create temporal coupling. Separate commands from queries. Prefer exceptions to error codes, and extract the try and catch bodies into their own functions — error handling is one thing.

Bury switch statements in an ABSTRACT FACTORY and dispatch polymorphically. **ONE SWITCH rule**: at most one switch per selection type.

### Comments
"Comments are always failures" — compensation for an inability to express intent in code. They lie, because code moves and comments don't; **an inaccurate comment is worse than none**. Never comment bad code: rewrite it. Delete commented-out code, change journals, and bylines — source control owns that. Mandating a comment per function guarantees noise at scale. Keep only what code genuinely cannot carry: legal text, intent, warnings, amplification, clarification of code you can't change, and Javadoc on **public APIs only**.

### Formatting
Formatting is communication, and your style survives long after your code doesn't. Read a file like a **newspaper**: name, then concepts, then detail. Blank lines separate thoughts; density binds related lines. Callers above callees. Locals at first use, instance variables at the top of the class. Files ~200 lines (500 max), lines ≤120 chars. **Don't align columns** — a list long enough to want alignment is a class that needs splitting. In a team, the team's style wins.

### Objects vs. data structures
**Objects hide data and expose behavior; data structures expose data and have no behavior.** They are opposites: OO makes new *types* cheap and new *functions* expensive; procedural code makes new *functions* cheap and new *types* expensive. Choose by which axis will grow — "the idea that everything is an object is a myth." Getters and setters are not encapsulation; expose the abstraction that captures the *essence* of the data. Law of Demeter violations depend on whether the links are objects or data structures; the real fix for a train wreck is to send a message (`ctxt.createScratchFileStream(name)`) rather than to split the chain.

### Error handling and boundaries
Error handling is important, but **if it obscures logic it's wrong**. Write the `try-catch-finally` first, driven by a test that forces the exception — the try block is a transaction scope. Prefer **unchecked** exceptions; checked ones violate OCP by cascading `throws` clauses upward. Define exception classes by *how they will be caught*, not by source. Don't return null (return an empty collection or a SPECIAL CASE object) and don't pass null.

Wrap third-party APIs: it isolates the dependency, makes it mockable, and gives you an API you like. Keep boundary types like `Map` out of your public signatures. Write **learning tests** against new libraries — free, since you had to learn them anyway, and they turn version upgrades into an immediate signal. When the other side doesn't exist yet, define the interface you wish you had and write an ADAPTER later.

### Tests
**Test code is as important as production code.** Dirty tests are worse than no tests: they get harder to change, then get discarded, and then fear returns and the production code rots. **Tests enable all the -ilities, because tests enable change.**

Three Laws of TDD: no production code before a failing test; no more test than suffices to fail (not compiling *is* failing); no more production code than suffices to pass. Cycle ≈ 30 seconds.

Clean tests are readable above all — BUILD-OPERATE-CHECK (or given-when-then), with a **domain-specific testing language** that *evolves from refactoring*, never designed up front. Minimize asserts, but the real rule is **one concept per test**. Tests may trade efficiency (the dual standard) but never cleanliness. Make them **F.I.R.S.T.** — Fast, Independent, Repeatable, Self-Validating, Timely.

### Classes and systems
Class size is measured in **responsibilities**. If you can't name it concisely, or describe it in 25 words without "and," it's too big. **SRP**: one reason to change. Falling cohesion — variables serving only a subset of methods — means a class is trying to get out; split it. Apply **OCP** so new features arrive as new classes and nothing existing opens. Apply **DIP** — depend on abstractions — which is the same property as testability.

At system scale: separate construction from use (all wiring in `main`, a factory, or a DI container), write domain logic as framework-free **POJOs**, and weave cross-cutting concerns in noninvasively with aspects. Architecture can grow incrementally; **BDUF is harmful**. Postpone decisions to the last responsible moment.

### Emergence — the four rules of Simple Design
In priority order: **runs all the tests · contains no duplication · expresses the intent of the programmer · minimizes the number of classes and methods.** Rule 1 drives design, not just correctness, because testability forces small classes and low coupling. Rules 2–4 happen in the refactor step. **Duplication is the primary enemy** — identical lines, similar lines, and duplicated *implementation* alike.

### Concurrency
Concurrency decouples *what* from *when*. It is hard: `return ++lastIdUsed;` is eight byte-codes and **12,870 execution paths** for two threads. Apply SRP — keep threading policy in its own class, everything else a thread-ignorant POJO. Limit shared-data scope severely; prefer copies; keep threads independent. Keep critical sections minimal. Prefer nonblocking atomics (CAS) over `synchronized`. Prefer **server-based locking** over client-based. Break one of the four deadlock conditions — usually circular wait, via a global resource ordering. **Never write off a spurious failure as a one-off.** Find rare bugs by instrumenting (ConTest / jiggling), not by adding iterations.

### Refactoring
**"To write clean code, you must first write dirty code and then clean it."** Get a behavior-verifying test suite, then make a myriad of very tiny changes, running all tests after each — never a rewrite. Stop adding features the moment you can see the next ones will make the mess unfixable. Expect to undo your own earlier refactorings; refactoring is trial and error converging on something worthy of a professional. Cleanup cost grows with elapsed time: a mess made five minutes ago is trivial to clean.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-clean-code.md) | Clean Code | LeBlanc's Law, Boy Scout Rule, Total Cost of Owning a Mess, Grand Redesign in the Sky, Beck's rules of simple code |
| [ch02](chapters/ch02-meaningful-names.md) | Meaningful Names | Intention-revealing names, avoid disinformation, meaningful distinctions, searchable names, one word per concept |
| [ch03](chapters/ch03-functions.md) | Functions | Small!, Do One Thing, TO paragraph, Stepdown Rule, Command Query Separation, DRY, switch→factory |
| [ch04](chapters/ch04-comments.md) | Comments | Comments are failures, good/bad comment taxonomy, explain yourself in code |
| [ch05](chapters/ch05-formatting.md) | Formatting | Newspaper Metaphor, vertical openness/density/distance, dependency direction, Team Rules |
| [ch06](chapters/ch06-objects-and-data-structures.md) | Objects and Data Structures | Data abstraction, Data/Object Anti-Symmetry, Law of Demeter, hybrids, DTO/Active Record |
| [ch07](chapters/ch07-error-handling.md) | Error Handling | Exceptions over return codes, write try-catch first, unchecked exceptions, SPECIAL CASE, don't return/pass null |
| [ch08](chapters/ch08-boundaries.md) | Boundaries | Don't pass boundary interfaces, learning tests, write the interface you wish you had, ADAPTER |
| [ch09](chapters/ch09-unit-tests.md) | Unit Tests | Three Laws of TDD, BUILD-OPERATE-CHECK, testing DSL, dual standard, one concept per test, F.I.R.S.T. |
| [ch10](chapters/ch10-classes.md) | Classes | SRP, 25-word test, cohesion, OCP, DIP, organizing for change |
| [ch11](chapters/ch11-systems.md) | Systems | Separation of main, ABSTRACT FACTORY, Dependency Injection, AOP, POJOs, test-drive the architecture, no BDUF |
| [ch12](chapters/ch12-emergence.md) | Emergence | Four rules of Simple Design, reuse in the small, TEMPLATE METHOD |
| [ch13](chapters/ch13-concurrency.md) | Concurrency | Concurrency defense principles, Producer-Consumer / Readers-Writers / Dining Philosophers, jiggling |
| [ch14](chapters/ch14-successive-refinement.md) | Successive Refinement | Write dirty then clean, on incrementalism, ArgumentMarshaler case study |
| [ch15](chapters/ch15-junit-internals.md) | JUnit Internals | Critique of clean code, encapsulate conditionals, expose temporal coupling, ComparisonCompactor |
| [ch16](chapters/ch16-refactoring-serialdate.md) | Refactoring SerialDate | First make it work then make it right, coverage as diagnostic, professional review |
| [ch17](chapters/ch17-smells-and-heuristics.md) | Smells and Heuristics | The full catalogue: C1–C5, E1–E2, F1–F4, G1–G36, J1–J3, N1–N7, T1–T9 |
| [ch18](chapters/ch18-appendix-a-concurrency-ii.md) | Appendix A: Concurrency II | Execution path math, atomicity and byte-code, CAS, server-based locking, four deadlock conditions, ConTest |

## Topic Index

- **Abstraction levels** → ch03, ch06, ch17 (G6, G34)
- **Active Record / DTO / beans** → ch06
- **AOP / aspects / cross-cutting concerns** → ch11
- **Arguments (count, flags, output, selectors)** → ch03, ch17 (F1–F3, G15)
- **Atomicity / byte-code / CAS** → ch18
- **Boundaries / third-party code** → ch08, ch07
- **Boy Scout Rule** → ch01, ch15, ch16
- **Classes (size, cohesion, organization)** → ch10, ch05
- **Command Query Separation** → ch03
- **Comments** → ch04, ch17 (C1–C5)
- **Concurrency** → ch13, ch18
- **Deadlock / livelock / starvation** → ch13, ch18
- **Dependency Injection / IoC** → ch11
- **DIP (Dependency Inversion)** → ch10, ch11
- **DRY / duplication** → ch03, ch12, ch17 (G5)
- **Enums vs. constants** → ch16, ch17 (J2, J3)
- **Error handling / exceptions** → ch07, ch03
- **Feature Envy** → ch06, ch16, ch17 (G14)
- **Formatting / layout** → ch05
- **Functions** → ch03, ch17 (F1–F4, G30, G34)
- **Law of Demeter / train wrecks** → ch06, ch17 (G36)
- **Learning tests** → ch08
- **Magic numbers** → ch16, ch17 (G25)
- **Names** → ch02, ch17 (N1–N7)
- **Null (returning, passing)** → ch07
- **OCP (Open-Closed)** → ch10, ch07
- **Objects vs. data structures** → ch06
- **POJOs** → ch11, ch13
- **Polymorphism vs. switch** → ch03, ch06, ch16, ch17 (G23)
- **Refactoring process** → ch14, ch15, ch16
- **Simple Design (four rules)** → ch12, ch01
- **SRP (Single Responsibility)** → ch10, ch11, ch13
- **Stepdown Rule** → ch03, ch05
- **Systems / architecture** → ch11
- **TDD (Three Laws)** → ch09, ch12, ch14
- **Temporal coupling** → ch03, ch15, ch17 (G31)
- **Tests (F.I.R.S.T., coverage, patterns)** → ch09, ch16, ch17 (T1–T9)
- **Threading policy isolation** → ch13, ch18
- **Try-catch-finally** → ch07, ch03

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions and chapter references
- [patterns.md](patterns.md) — the techniques, with when-to-use and trade-offs
- [cheatsheet.md](cheatsheet.md) — thresholds, decision rules, tells and smells

---

## Scope & Limits

This skill covers the book's content only. The code is Java 5-era; the principles are language-neutral but some specifics (checked exceptions, `serialVersionUID`, wildcard imports, the `final` argument) are Java-particular and Martin's positions on several are explicitly contested in the text. Martin's later *Clean Architecture* covers system-level boundaries; see the `clean-architecture` skill. For applying these rules to a specific codebase, combine with project-specific tooling.
