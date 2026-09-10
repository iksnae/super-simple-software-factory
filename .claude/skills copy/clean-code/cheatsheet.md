# Cheatsheet — Clean Code

## Thresholds & defaults

| Thing | Martin's number |
|---|---|
| Function length | Rarely 20 lines; 2–4 is the benchmark (Beck's *Sparkle*) |
| Indent depth in a function | 1–2 levels; block bodies are one line, usually a call |
| Function arguments | 0 ideal, 1 good, 2 costly, 3 avoid, 4+ never |
| File length | ~200 lines typical, 500 upper bound (FitNesse: 50k lines, ~65-line average file) |
| Line width | ≤ 120 characters |
| Class size | Counted in *responsibilities*, not lines — one reason to change |
| Class description | ≤ 25 words, no "if"/"and"/"or"/"but" |
| TDD cycle | ~30 seconds |
| Switch statements per selection type | Exactly one (ONE SWITCH rule) |
| Comments per module | As few as possible; two is a lot (`PrimeGenerator`) |

## Decision rules

**When you want to write a comment** → try to express it as a function or variable name first. If you succeed, that was the right answer. If a name requires a comment, fix the name.

**When a function needs a section comment** (`// initialize`, `// sieve`) → extract that section into a named function. Functions that do one thing cannot be divided into sections.

**When you have 3+ arguments** → some of them form a concept. Make an argument object.

**When you're about to pass a boolean** → split the function in two (`renderForSuite()` / `renderForSingleTest()`).

**When a function both changes state and returns a status** → split it (Command Query Separation). `if (set("username", "unclebob"))` is unreadable in either direction.

**When you're deciding objects vs. data structures** → ask which axis will grow. New *types* coming → objects and polymorphism. New *functions* coming → data structures and procedures. "The idea that everything is an object is a myth."

**When you see a train wreck** (`a.getB().getC()`) → ask what you were going to *do* with the result, and send that as a message instead (`ctxt.createScratchFileStream(name)`). Splitting the chain into locals fixes nothing.

**When a class accumulates variables used by only some methods** → cohesion is falling; a class is trying to get out. Split it.

**When you find yourself opening a class to add a feature** → that is the moment to refactor toward OCP. A logically complete class you aren't touching needs no rescue.

**When you must decide static vs. instance** → nonstatic by default. Static only when all data comes from arguments *and* there is no chance you'll want polymorphism (`Math.max` yes, `HourlyPayCalculator.calculatePay` no).

**When a change forces an operator you don't believe in** → stop and investigate. You've probably found a latent bug or dead code (`suffixLength > 0` in JUnit's ComparisonCompactor).

**When two functions must be called in order** → make the second consume what the first produces. A parameter that only *implies* ordering is arbitrary and will be deleted by the next person.

**When you're about to refactor something elegant** → check for callers first. A beautiful transformation of dead code is still wasted.

**When adding the next feature will make the mess unfixable** → stop adding features now. That is the cheapest moment there will ever be.

**When you want to rewrite** → don't. Get a behavior-verifying test suite and make a myriad of tiny changes, running tests after each.

## Tells & smells (fast recognition)

| You see… | You probably have… |
|---|---|
| A section comment inside a function | A function that should be several functions |
| A closing-brace comment (`} //while`) | A function that's too long |
| Commented-out code | Code nobody dares delete; delete it |
| A change history in the file header | Work source control already does |
| Long aligned columns of declarations | A class that should be split |
| Duplicate `catch` bodies | An exception taxonomy built on source instead of on handling |
| `if (x != null)` on nearly every line | Too *many* null checks, not too few — stop returning null |
| Weasel-word class name (`Manager`, `Processor`, `Super`) | Aggregated responsibilities |
| `+1` and `-1` scattered around | A misnamed 1-based variable |
| A switch you're about to copy | A polymorphic hierarchy waiting to exist |
| Enum/constant sets passed as `int` | Enums that should carry the behavior |
| Real behavior *and* public accessors on the same class | A hybrid — worst of both worlds |
| A spurious, unreproducible failure | A threading bug. One-offs do not exist |
| A test that's slow | A test that will be dropped when things get tight |

## The four rules of Simple Design (priority order)
1. Runs all the tests — testability drives small classes, low coupling, DIP
2. Contains no duplication — extraction, TEMPLATE METHOD/STRATEGY, polymorphism
3. Expresses the intent of the programmer — names, small units, standard nomenclature, tests as docs
4. Minimizes the number of classes and methods — **lowest priority**; it bounds 2 and 3, never overrides them

## The Three Laws of TDD
1. No production code until a failing test exists
2. No more test than suffices to fail — **not compiling is failing**
3. No more production code than suffices to pass the current failing test

## F.I.R.S.T. — and what each failure costs you

| | Rule | Violation costs |
|---|---|---|
| **F** | Fast | Rare runs → late detection → fear of cleanup → rot |
| **I** | Independent, any order | Cascading failures hide downstream defects |
| **R** | Repeatable anywhere, offline | A permanent excuse for every failure |
| **S** | Self-validating (boolean) | Subjective results, manual log-reading |
| **T** | Timely — written just before the code | Code turns out hard or impossible to test |

## Concurrency decision table

| Situation | Do this |
|---|---|
| Any concurrent code | Put threading policy in its own class; everything else a thread-ignorant POJO |
| Shared counter or reference | `AtomicInteger`/`AtomicReference` (CAS), not `synchronized` |
| Composite op on a thread-safe collection | Use the collection's own (`putIfAbsent`), or wrap — method safety doesn't compose |
| Client must call 2+ methods on a shared object | Server-based locking: change the API (`getNextOrNull()`) |
| You don't own the server | ADAPTER with locking, or a thread-safe collection |
| Deadlock risk | Break circular wait via global resource ordering (cheapest of the four) |
| Rare threading bug | Instrument (ConTest / jiggling), not more iterations |
| Any threaded system | Run with more threads than cores, on every target platform, under varying load |

## Magic numbers — when the raw number wins
Hide `86400` → `SECONDS_PER_DAY`, `55` → `LINES_PER_PAGE`, `3.14159…` → `Math.PI` (the digit error is too easy to miss).
Keep raw: `feetWalked/5280.0`, `hourlyRate * 8`, `radius * Math.PI * 2`. Constants named `TWO` are absurd.
Remember magic *strings* too: `assertEquals(7777, Employee.find("John Doe")…)` has two.

## Comments that earn their place
Legal · Explanation of intent · Warning of consequences · Amplification · Clarification of code you cannot change · TODO (with a reason and an expiry) · Javadoc on **public APIs only**.
Everything else: fix the code instead.
