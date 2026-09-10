# Chapter 4: Comments

## Core Idea
"Comments are always failures" — every comment is compensation for an inability to express intent in code, so the only truly good comment is the one you found a way not to write.

## Frameworks Introduced
- **Comments lie, and code cannot**: the older a comment is and the farther from the code it describes, the more likely it is wrong, because programmers cannot realistically maintain them.
  - When to use: deciding whether to trust a comment during debugging.
  - How: treat the code as the single source of truth. Inaccurate comments are *worse* than no comments — they set expectations that will never be fulfilled and codify rules that should no longer be followed.
- **Comments Do Not Make Up for Bad Code**: the urge "ooh, I'd better comment that" is the signal that you should clean it instead.
- **Explain Yourself in Code**: before writing a comment, try to express it as a function or a variable name.
  - How: `// Check to see if the employee is eligible for full benefits` + a flag test becomes `if (employee.isEligibleForFullBenefits())`.
- **The good-comment taxonomy**: Legal, Informative, Explanation of Intent, Clarification, Warning of Consequences, TODO, Amplification, Javadocs in public APIs. Everything else is suspect.
- **The bad-comment taxonomy**: Mumbling, Redundant, Misleading, Mandated, Journal, Noise, Position Markers, Closing Brace Comments, Attributions/Bylines, Commented-Out Code, HTML Comments, Nonlocal Information, Too Much Information, Inobvious Connection, Function Headers, Javadocs in nonpublic code.

## Key Concepts
- **Mumbling** — a comment that meant something to its author and nothing to anyone else. "Any comment that forces you to look in another module for the meaning of that comment has failed to communicate and is not worth the bits it consumes."
- **Redundant comment** — takes longer to read than the code, is less precise than the code, and "entices the reader to accept that lack of precision in lieu of true understanding."
- **Mandated comment** — the rule that every function needs a javadoc or every variable a comment; it manufactures clutter and lies at scale.
- **Journal comment** — a change log at the top of a module; obsolete since source control, and should be deleted entirely.
- **Noise comment** — `/** Default constructor. */`. Readers learn to skip them, and then they rot into lies.
- **Position marker / banner** — `// Actions //////////////////`. Startling and obvious only if rare; overuse makes them invisible.
- **Nonlocal information** — a local comment describing a distant part of the system (e.g. documenting a default port in a setter that has no control over the default). Nothing will keep it in sync.
- **Inobvious connection** — a comment that itself needs explaining: "It is a pity when a comment needs its own explanation."

## Mental Models
- **Feel the failure.** Every time you express yourself in code, pat yourself on the back; every time you write a comment, grimace at the failure of expression.
- **Treat commented-out code as poison.** Nobody who comes after has the courage to delete it — they assume it's there for a reason — so it accumulates "like dregs at the bottom of a bad bottle of wine." Source control remembers. Just delete it.
- **Route metadata to the tool that owns it.** Authorship and change history belong to source control, not bylines and journals. HTML markup belongs to Javadoc the tool, not to the programmer writing the comment.
- **When the urge is to vent in a comment, refactor instead.** `//Give me a break!` in a nested catch is frustration that should have gone into extracting the block into a named function.
- **Closing-brace comments mean your function is too long.** If you want to mark `} //while`, shorten the function.
- **Javadocs are for public APIs only.** Inside a system they are formality-cruft, and they can be as misleading, nonlocal, and dishonest as any other comment.

## Code Examples

The canonical replacement of a comment by a function:

```java
// Check to see if the employee is eligible for full benefits
if ((employee.flags & HOURLY_FLAG) && (employee.age > 65))
```
```java
if (employee.isEligibleForFullBenefits())
```

A comment worth keeping — warning of a real consequence:

```java
public static SimpleDateFormat makeStandardHttpDateFormat() {
    //SimpleDateFormat is not thread safe,
    //so we need to create each instance independently.
    SimpleDateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z");
    df.setTimeZone(TimeZone.getTimeZone("GMT"));
    return df;
}
```
- **What it demonstrates**: prevents an overly eager programmer from "optimizing" this into a static initializer.

Redundant *and* misleading (Listing 4-1) — the trap that makes redundancy dangerous:

```java
// Utility method that returns when this.closed is true. Throws an exception
// if the timeout is reached.
public synchronized void waitForClose(final long timeoutMillis) throws Exception {
    if(!closed) {
        wait(timeoutMillis);
        if(!closed)
            throw new Exception("MockResponseSender could not be closed");
    }
}
```
- **What it demonstrates**: the method does *not* return when `this.closed` becomes true. It returns *if* `closed` is already true; otherwise it waits out a blind timeout and throws. A caller trusting the comment gets a slow-code debugging session.

Noise that should have been a refactoring (Listing 4-4 → 4-5):

```java
// before
private void startSending() {
    try {
        doSending();
    } catch(SocketException e) {
        // normal. someone stopped the request.
    } catch(Exception e) {
        try {
            response.add(ErrorResponder.makeExceptionString(e));
            response.closeAll();
        } catch(Exception e1) {
            //Give me a break!
        }
    }
}
```
```java
// after
private void startSending() {
    try {
        doSending();
    } catch(SocketException e) {
        // normal. someone stopped the request.
    } catch(Exception e) {
        addExceptionAndCloseResponse(e);
    }
}

private void addExceptionAndCloseResponse(Exception e) {
    try {
        response.add(ErrorResponder.makeExceptionString(e));
        response.closeAll();
    } catch(Exception e1) {
    }
}
```

Comment → local variables:

```java
// does the module from the global list <mod> depend on the
// subsystem we are part of?
if (smodule.getDependSubsystems().contains(subSysMod.getSubSystem()))
```
```java
ArrayList moduleDependees = smodule.getDependSubsystems();
String ourSubSystem = subSysMod.getSubSystem();
if (moduleDependees.contains(ourSubSystem))
```

## Reference Tables

| Good comment | What earns its place |
|---|---|
| Legal | Copyright/license headers mandated by corporate standards; refer to an external license rather than inlining terms |
| Informative | Basic facts (e.g. what format a regex matches) — but prefer renaming the function |
| Explanation of Intent | The *why* behind a decision (`return 1; // we are greater because we are the right type`) |
| Clarification | Translating an obscure argument or return value you cannot change (standard library, third-party code) — risky, verify carefully |
| Warning of Consequences | "Don't run unless you have some time to kill"; thread-safety caveats |
| TODO | Why a function is degenerate and what its future should be. Scan and eliminate regularly; **never an excuse to leave bad code in the system** |
| Amplification | Marking something inconsequential-looking as critical ("the trim is real important") |
| Javadocs in public APIs | Genuinely valuable — while remaining subject to every other rule here |

| Bad comment | Why it fails |
|---|---|
| Mumbling | Meaning only recoverable by reading other modules |
| Redundant | Slower to read and less precise than the code |
| Misleading | Subtly inaccurate; causes real bugs |
| Mandated | Rule-driven clutter that manufactures lies |
| Journal | Superseded by source control |
| Noise | Restates the obvious; trains readers to skip |
| Position markers | Banners lose force through overuse |
| Closing brace | Symptom of an over-long function |
| Bylines | Source control knows; these rot |
| Commented-out code | Nobody dares delete it; it accumulates forever |
| HTML in comments | Unreadable where it matters most — the IDE |
| Nonlocal information | Describes a distant part of the system; guaranteed to drift |
| Too much information | Historical/RFC detail nobody reading this code needs |
| Inobvious connection | The comment needs its own explanation |
| Function headers | A good name on a small function beats a header |
| Javadocs in nonpublic code | Formality cruft and distraction |

## Worked Example
**Listing 4-7 → 4-8: `GeneratePrimes` refactored.** Martin wrote 4-7 for the first XP Immersion as a deliberate example of bad coding and commenting style; Kent Beck refactored it live in front of the class. The point he stresses: there was a time when many of us would have called this module *well documented*.

The original carries a class javadoc containing a biography of Eratosthenes of Cyrene, an `@author`/`@version` byline, a `// the only valid case` aside, and section markers — `// declarations`, `// initialize array to true`, `// get rid of known non-primes`, `// sieve`, `// how many primes are there?`, `// move the primes into the result` — with single-letter names (`s`, `f`, `i`, `j`) underneath. Those section comments are the tell: a function that can be divided into named sections is doing more than one thing, and each section comment is a function begging to be extracted.

The refactored `PrimeGenerator` extracts exactly those sections into named methods and keeps **two** comments in the whole module:

```java
/**
 * This class Generates prime numbers up to a user specified
 * maximum.  The algorithm used is the Sieve of Eratosthenes.
 * Given an array of integers starting at 2:
 * Find the first uncrossed integer, and cross out all its
 * multiples.  Repeat until there are no more multiples
 * in the array.
 */
public class PrimeGenerator {
    private static boolean[] crossedOut;
    private static int[] result;

    public static int[] generatePrimes(int maxValue) {
        if (maxValue < 2)
            return new int[0];
        else {
            uncrossIntegersUpTo(maxValue);
            crossOutMultiples();
            putUncrossedIntegersIntoResult();
            return result;
        }
    }

    private static void crossOutMultiples() {
        int limit = determineIterationLimit();
        for (int i = 2; i <= limit; i++)
            if (notCrossed(i))
                crossOutMultiplesOf(i);
    }

    private static int determineIterationLimit() {
        // Every multiple in the array has a prime factor that
        // is less than or equal to the root of the array size,
        // so we don't have to cross out multiples of numbers
        // larger than that root.
        double iterationLimit = Math.sqrt(crossedOut.length);
        return (int) iterationLimit;
    }

    private static boolean notCrossed(int i) {
        return crossedOut[i] == false;
    }
}
```

Martin's own verdict on the two survivors is the useful part. The class comment is arguably redundant with `generatePrimes` itself, but he keeps it because it eases the reader into the algorithm. The square-root comment is "almost certainly necessary" — he could find no variable name or structure that made the rationale clear. And then he turns on his own optimization: is the square root even saving time, or is computing it costing more than it saves? "Using the square root as the iteration limit satisfies the old C and assembly language hacker in me, but I'm not convinced it's worth the time and effort that everyone else will expend to understand it." A comment that has to justify a clever line is evidence against the clever line.

## Key Takeaways
1. A comment is an admission of failure to express intent in code. Try the function-or-variable rewrite first, every time.
2. Comments rot because code moves and comments don't. Inaccurate comments are worse than none.
3. Never comment bad code — rewrite it.
4. Delete commented-out code, journals, and bylines outright; source control owns that information.
5. Section comments inside a function are extraction points, not documentation.
6. Mandating comments (every function, every variable) guarantees noise and lies.
7. Keep only comments that carry information the code genuinely cannot: legal text, intent, warnings, amplification, and clarification of code you cannot change.
8. Javadocs earn their place on public APIs and almost nowhere else.

## Connects To
- **Ch 2 (Meaningful Names)**: most comments are names that were never found.
- **Ch 3 (Functions)**: "Sections within Functions" points at Listing 4-7; extraction is the mechanism that removes comments.
- **Ch 5 (Formatting)**: the file as a newspaper — comments and layout are both about the reader's eye.
- **Ch 17 (Smells and Heuristics)**: the C-series comment smells (C1 inappropriate information, C2 obsolete comment, C3 redundant comment, C4 poorly written comment, C5 commented-out code).
