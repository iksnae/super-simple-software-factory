# Chapter 4: Structured Programming

## Core Idea
Dijkstra's dream of formally proving programs correct died — but the structure it required survived, because **software is a science, not a mathematics**: we show correctness by failing to prove incorrectness, and only decomposable programs can be falsified at all.

## Frameworks Introduced
- **Proof by decomposition**: Dijkstra's plan was a Euclidean hierarchy of postulates, theorems, corollaries, and lemmas — programmers would use proven structures and prove the connecting code themselves.
  - The obstacle he found: certain uses of `goto` **prevent modules from being decomposed recursively** into smaller units, killing the divide-and-conquer approach proofs require.
  - The discovery: the "good" uses of `goto` correspond exactly to simple selection and iteration (`if/then/else`, `do/while`). Modules using only those can be recursively subdivided into provable units.
  - **The remarkable coincidence**: Böhm and Jacopini had proved two years earlier that all programs can be built from just **sequence, selection, and iteration**. "The very control structures that made a module provable were the same minimum set of control structures from which all programs can be built. Thus structured programming was born."
- **The three proof techniques**:
  - *Sequence* — proved by simple **enumeration**, tracing inputs to outputs; no different from a normal mathematical proof.
  - *Selection* — **reapplication of enumeration**; each path enumerated, and if both produce appropriate results the proof is solid.
  - *Iteration* — requires **induction**: prove the case for 1 by enumeration, then that N correct implies N+1 correct, plus the starting and ending criteria.
- **Mathematics vs. science**: "mathematics is the discipline of proving provable statements **true**. Science, in contrast, is the discipline of proving provable statements **false**."
  - Scientific laws are **falsifiable but not provable**. You cannot prove F = ma; you can demonstrate it and measure it to many decimal places, and there remains a chance some experiment disproves it. "And yet we bet our lives on these laws every day."
- **Tests as falsification**: Dijkstra — *"Testing shows the presence, not the absence, of bugs."*
  - Therefore: "Software development is **not** a mathematical endeavor, even though it seems to manipulate mathematical constructs. Rather, software is like a science. We show correctness by failing to prove incorrectness, despite our best efforts."
  - **The critical corollary**: "Such proofs of incorrectness can be applied only to *provable* programs. A program that is not provable — due to unrestrained use of `goto`, for example — **cannot be deemed correct no matter how many tests are applied to it**."

## Key Concepts
- **"Go To Statement Considered Harmful"** — Dijkstra's letter to the editor of *CACM*, published March 1968. "And the programming world caught fire." The battle lasted about a decade and petered out for a simple reason: **Dijkstra had won.** The `goto` statement moved ever rearward until it all but disappeared. "Nowadays we are all structured programmers, though not necessarily by choice. It's just that our languages don't give us the option."
- **Named breaks and exceptions are not `goto`** — "these structures are not the utterly unrestricted transfers of control that older languages like Fortran or COBOL once had. Indeed, even languages that still support the `goto` keyword often restrict the target to within the scope of the current function."
- **Functional decomposition** — because structured programming allows recursive decomposition into provable units, a large-scale problem can be decomposed into high-level functions, then lower-level ones, ad infinitum. This foundation produced structured analysis and structured design, popularized in the late 1970s–1980s by Ed Yourdon, Larry Constantine, Tom DeMarco, and Meilir Page-Jones.
- **The proofs never came.** "The Euclidean hierarchy of theorems was never built. And programmers at large never saw the benefits of working through the laborious process of formally proving each and every little function correct. In the end, Dijkstra's dream faded and died."
- **Not all statements are provable** — "This is a lie" is neither true nor false; one of the simplest unprovable statements.

## Mental Models
- **Architects are in the falsifiability business.** "At every level, from the smallest function to the largest component, software is like a science and, therefore, is driven by falsifiability. Software architects strive to define modules, components, and services that are easily falsifiable (**testable**). To do so, they employ restrictive disciplines similar to structured programming, albeit at a much higher level."
- **Testability is not a nice-to-have; it is the only route to a correctness claim.** Unstructured code isn't merely harder to test — it is outside the reach of the argument entirely.
- **"Correct enough for our purposes" is the honest ceiling.** After sufficient testing effort, that is all a test can give you — and the same is true of every scientific law you stake your life on daily.

## Worked Example
**Dijkstra's biography as the argument's setup.** Born Rotterdam 1930; survived the bombing of Rotterdam and the German occupation; graduated in 1948 with the highest possible marks in math, physics, chemistry, and biology. In March 1952, aged 21, he became **the Netherlands' very first programmer**, at the Mathematical Center of Amsterdam.

Two details carry the chapter's point. First, in 1955 — three years into programming, still a student — he concluded that *the intellectual challenge of programming was greater than the intellectual challenge of theoretical physics*, and chose it as his career. Second, in 1957 the Dutch marriage rites required stating a profession, and the authorities **refused to accept "programmer"** — they had never heard of it. Dijkstra settled for "theoretical physicist."

His concern on committing to the career was precisely that no discipline or science of programming had been identified, so he would not be taken seriously. His boss, Adriaan van Wijngaarden, replied that Dijkstra might be one of the people who would discover such disciplines, "thereby evolving software into a science."

The environment: vacuum tubes; huge, fragile, slow, unreliable, extremely limited machines; programs in binary or crude assembly; input on paper tape or punched cards; an edit/compile/test loop **hours or days long**. "It was in this primitive environment that Dijkstra made his great discoveries."

**The argument that survives the failed dream.** Dijkstra's goal (formal proof) was abandoned. What replaced it keeps the same structural requirement:

1. Programming is hard, and a program of any complexity holds too many details for a human brain unaided. "Overlooking just one small detail results in programs that may seem to work, but fail in surprising ways."
2. Formal proof would solve that — but requires recursive decomposition into small units.
3. Unrestricted `goto` blocks decomposition; restricted control structures permit it.
4. Those same restricted structures turn out to be sufficient to write **every** program (Böhm & Jacopini).
5. Formal proof failed in practice; **falsification by test succeeded**.
6. But falsification also requires decomposition into small units.
7. Therefore the structural discipline is still mandatory — for a completely different reason than the one it was invented for.

"It is this ability to create falsifiable units of programming that makes structured programming valuable today... Moreover, at the architectural level, this is why we still consider functional decomposition to be one of our best practices."

## Key Takeaways
1. Unrestricted `goto` destroys the recursive decomposition that both proof and testing depend on.
2. Sequence, selection, and iteration are simultaneously sufficient to write any program and necessary to reason about one.
3. Formal proof of programs was tried, was laborious, and did not take. Testing replaced it.
4. Tests falsify; they cannot verify. "Correct enough for our purposes" is the strongest available claim.
5. An unprovable (undecomposable) program cannot be deemed correct **however much** you test it.
6. Architects apply the same restrictive discipline at module, component, and service scale — and the property they're buying is testability.

## Connects To
- **Ch 3 (Paradigm Overview)**: structured programming as the algorithmic foundation of modules.
- **Ch 1**: Gorman's TDD experiment — falsifiability paying off inside 30 minutes.
- **Ch 28 (The Test Boundary)**: tests as a first-class architectural concern.
- **Clean Code, Ch 9 & 12**: the Three Laws of TDD, and "runs all the tests" as the first rule of simple design.
