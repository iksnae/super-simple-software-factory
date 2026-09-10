# Chapter 15: JUnit Internals

## Core Idea
A critique of already-good code: JUnit's `ComparisonCompactor` is well-partitioned and 100% covered, and the Boy Scout Rule still applies — "no module is immune from improvement."

## Frameworks Introduced
- **Critique already-clean code, not just messes.** The chapter's subject is a module whose authors "had done an excellent job with it." The exercise is to find the remaining nits and to watch what the fixes reveal.
- **Extract a named predicate for every unencapsulated conditional** [G28]: `if (expected == null || actual == null || areStringsEqual())` becomes `if (shouldNotCompact())`.
- **Invert negatives** [G29]: negatives are slightly harder to understand than positives, so turn `shouldNotCompact` into `canBeCompacted` and flip the `if`.
- **Name the function for what it actually does** [N7]: `compact` might not compact anything (if `canBeCompacted` is false) and returns a *formatted message*, not compacted strings. The honest name is `formatCompactedComparison`.
- **One function, one job** [G30]: `formatCompactedComparison` should do all the formatting; the `compact...` function "should do nothing but compacting." Split them.
- **Use consistent conventions within a function** [G11]: when two of four lines return values and two don't, change the outliers so all four read the same way.
- **Expose hidden temporal coupling** [G31], then judge whether the exposure is honest.

## Key Concepts
- **Defactoring** — Listing 15-3, the same module deliberately degraded to `ctxt`, `s1`, `s2`, `pfx`, `sfx` with everything inlined into `compact`. It exists to show what the original authors' care actually bought.
- **`f` prefix for members** [N6] — scope encoding that today's environments make redundant. Delete it.
- **Shadowed names** [N4] — after renaming `fExpected` to `expected`, the local `expected` inside `compact` collides with the member. "Why are there variables in this function that have the same names as the member variables? Don't they represent something else?" Rename to `compactExpected` / `compactActual`.
- **Arbitrary parameter** [G32] — passing `prefixIndex` into `findCommonSuffix` *establishes* ordering but "does nothing to explain the need for that ordering. Another programmer might undo what we have done because there's no indication that the parameter is really needed."
- **Off-by-one as a naming problem** [G33] — `suffixIndex` is 1-based, which is why `computeCommonSuffix` is littered with `+1`s. Making it a true zero-based `suffixLength` moves the `-1` into `charFromEnd` (where it makes perfect sense) and the `<=` into `suffixOverlapsPrefix` (where it also makes perfect sense).
- **Topological sorting of a module** — the final version separates *analysis* functions from *synthesis* functions, each defined just after it is used, analysis first and synthesis last.
- **Refactoring reverses itself** — "I inlined some extracted methods back into `formatCompactedComparison`, and I changed the sense of the `shouldNotBeCompacted` expression. This is typical. Often one refactoring leads to another that leads to the undoing of the first."

## Mental Models
- **Read the tests to learn the requirements.** Martin introduces `ComparisonCompactor` by pointing at `ComparisonCompactorTest` — "I could explain it further, but the test cases do a better job." Nineteen tests, 100% line/branch coverage, which gives "a high degree of confidence that the code works and a high degree of respect for the craftsmanship of the authors."
- **When a change forces an operator you don't believe in, you've found something.** Reducing `suffixLength` by one implied changing `>` to `>=` — "But that makes no sense. It makes sense now! This means that it didn't use to make sense and was probably a bug."
- **Comment out the suspicious code and run the tests.** That is how the two `if` statements in `compactString` were proven extraneous.
- **Refactoring is trial and error converging on something worthy of a professional** — not a linear sequence of correct decisions.

## Code Examples

The module before (Listing 15-2, abridged) — good code with nits:

```java
public class ComparisonCompactor {
    private static final String ELLIPSIS = "...";
    private static final String DELTA_END = "]";
    private static final String DELTA_START = "[";

    private int fContextLength;
    private String fExpected;
    private String fActual;
    private int fPrefix;
    private int fSuffix;

    public String compact(String message) {
        if (fExpected == null || fActual == null || areStringsEqual())
            return Assert.format(message, fExpected, fActual);

        findCommonPrefix();
        findCommonSuffix();
        String expected = compactString(fExpected);
        String actual = compactString(fActual);
        return Assert.format(message, expected, actual);
    }

    private String computeCommonSuffix() {
        int end = Math.min(fExpected.length() - fSuffix + 1 + fContextLength,
                           fExpected.length());
        return fExpected.substring(fExpected.length() - fSuffix + 1, end) +
            (fExpected.length() - fSuffix + 1 < fExpected.length() - fContextLength
                ? ELLIPSIS : "");
    }
}
```
- **What it demonstrates**: the `f` prefixes, the unencapsulated conditional, the shadowed locals, and the `+1`s that turn out to be an off-by-one baked into a variable name.

The counterfactual (Listing 15-3, "defactored") — what the same logic looks like without the authors' care:

```java
public String compact(String msg) {
    if (s1 == null || s2 == null || s1.equals(s2))
        return Assert.format(msg, s1, s2);

    pfx = 0;
    for (; pfx < Math.min(s1.length(), s2.length()); pfx++) {
        if (s1.charAt(pfx) != s2.charAt(pfx)) break;
    }
    int sfx1 = s1.length() - 1;
    int sfx2 = s2.length() - 1;
    for (; sfx2 >= pfx && sfx1 >= pfx; sfx2--, sfx1--) {
        if (s1.charAt(sfx1) != s2.charAt(sfx2)) break;
    }
    sfx = s1.length() - sfx1;
    String cmp1 = compactString(s1);
    String cmp2 = compactString(s2);
    return Assert.format(msg, cmp1, cmp2);
}
```

The module after (Listing 15-5, final):

```java
public class ComparisonCompactor {
    private static final String ELLIPSIS = "...";
    private static final String DELTA_END = "]";
    private static final String DELTA_START = "[";

    private int contextLength;
    private String expected;
    private String actual;
    private int prefixLength;
    private int suffixLength;

    public String formatCompactedComparison(String message) {
        String compactExpected = expected;
        String compactActual = actual;
        if (shouldBeCompacted()) {
            findCommonPrefixAndSuffix();
            compactExpected = compact(expected);
            compactActual = compact(actual);
        }
        return Assert.format(message, compactExpected, compactActual);
    }

    private boolean shouldBeCompacted() {
        return !shouldNotBeCompacted();
    }

    private boolean shouldNotBeCompacted() {
        return expected == null || actual == null || expected.equals(actual);
    }

    private void findCommonPrefixAndSuffix() {
        findCommonPrefix();
        suffixLength = 0;
        for (; !suffixOverlapsPrefix(); suffixLength++) {
            if (charFromEnd(expected, suffixLength)
                != charFromEnd(actual, suffixLength))
                break;
        }
    }

    private char charFromEnd(String s, int i) {
        return s.charAt(s.length() - i - 1);
    }

    private boolean suffixOverlapsPrefix() {
        return actual.length() - suffixLength <= prefixLength ||
               expected.length() - suffixLength <= prefixLength;
    }

    private void findCommonPrefix() {
        prefixLength = 0;
        int end = Math.min(expected.length(), actual.length());
        for (; prefixLength < end; prefixLength++)
            if (expected.charAt(prefixLength) != actual.charAt(prefixLength))
                break;
    }

    private String compact(String s) {
        return new StringBuilder()
            .append(startingEllipsis())
            .append(startingContext())
            .append(DELTA_START)
            .append(delta(s))
            .append(DELTA_END)
            .append(endingContext())
            .append(endingEllipsis())
            .toString();
    }

    private String startingEllipsis() {
        return prefixLength > contextLength ? ELLIPSIS : "";
    }

    private String startingContext() {
        int contextStart = Math.max(0, prefixLength - contextLength);
        int contextEnd = prefixLength;
        return expected.substring(contextStart, contextEnd);
    }

    private String delta(String s) {
        int deltaStart = prefixLength;
        int deltaEnd = s.length() - suffixLength;
        return s.substring(deltaStart, deltaEnd);
    }

    private String endingContext() {
        int contextStart = expected.length() - suffixLength;
        int contextEnd = Math.min(contextStart + contextLength, expected.length());
        return expected.substring(contextStart, contextEnd);
    }

    private String endingEllipsis() {
        return (suffixLength > contextLength ? ELLIPSIS : "");
    }
}
```

## Worked Example
**The temporal coupling, and the fix that was rejected.** `findCommonSuffix` silently depends on `prefixIndex` having been computed by `findCommonPrefix`. Call them out of order and "there would be a difficult debugging session ahead." The obvious fix is to make the dependency a parameter [G31]:

```java
private void compactExpectedAndActual() {
    prefixIndex = findCommonPrefix();
    suffixIndex = findCommonSuffix(prefixIndex);
    ...
}

private int findCommonSuffix(int prefixIndex) { ... }
```

Martin rejects it: "The passing of the `prefixIndex` argument is a bit arbitrary [G32]. It works to establish the ordering but does nothing to explain the *need* for that ordering. Another programmer might undo what we have done because there's no indication that the parameter is really needed."

The accepted fix makes the dependency structural rather than conventional — one function that owns both, calling the prefix search first:

```java
private void compactExpectedAndActual() {
    findCommonPrefixAndSuffix();
    compactExpected = compactString(expected);
    compactActual = compactString(actual);
}

private void findCommonPrefixAndSuffix() {
    findCommonPrefix();
    int expectedSuffix = expected.length() - 1;
    int actualSuffix = actual.length() - 1;
    for (; actualSuffix >= prefixIndex && expectedSuffix >= prefixIndex;
           actualSuffix--, expectedSuffix--) {
        if (expected.charAt(expectedSuffix) != actual.charAt(actualSuffix))
            break;
    }
    suffixIndex = expected.length() - expectedSuffix;
}
```

"That establishes the temporal nature of the two functions in a much more dramatic way than the previous solution. It also points out how ugly `findCommonPrefixAndSuffix` is."

**The bug that surfaced from a rename.** Cleaning that ugliness led to `suffixLength` replacing the 1-based `suffixIndex`, which removed the `+1`s. Then this line in `compactString` stopped adding up:

```java
if (suffixLength > 0)
```

By rights it should become `>=`. "But that makes no sense. It makes sense *now*!" — meaning it had *not* made sense before, and was probably a bug. Analysis confirmed it: the `if` now prevents a zero-length suffix from being appended, whereas previously it was entirely non-functional because `suffixIndex` could never be less than one.

That called both `if` statements in `compactString` into question. Comment them out, run the tests: **they passed**. Which collapses the function to pure composition [G9]:

```java
private String compactString(String source) {
    return computeCommonPrefix()
        + DELTA_START
        + source.substring(prefixLength, source.length() - suffixLength)
        + DELTA_END
        + computeCommonSuffix();
}
```

A naming correction exposed a latent bug and deleted two dead branches — in code that was already good and already 100% covered.

## Key Takeaways
1. Apply the Boy Scout Rule to good code too; excellence is not immunity.
2. Encapsulate conditionals behind named predicates, and prefer positives over negatives.
3. Name a function for everything it does — including the side effects and the formatting the name currently hides.
4. Keep conventions consistent inside a function; inconsistency is a smell worth chasing.
5. Make temporal coupling structural, not conventional — a parameter that only *implies* an ordering will be removed by the next person.
6. Off-by-one clutter (`+1` everywhere) usually means a variable is misnamed; fix the concept and the arithmetic simplifies itself.
7. When a change demands an operator you don't believe, investigate — you have probably found a latent bug or dead code.
8. Expect to undo your own earlier refactorings. Convergence, not linearity.

## Connects To
- **Ch 1 (Clean Code)**: the Boy Scout Rule, invoked explicitly as the chapter's justification.
- **Ch 2 (Meaningful Names)**: `f` prefixes [N6], shadowed names [N4], names that describe side effects [N7], accurate names [N1].
- **Ch 3 (Functions)**: do one thing [G30], no hidden side effects, small composed functions.
- **Ch 5 (Formatting)**: this module cited as an example of good vertical ordering (Listing 15-5).
- **Ch 9 (Unit Tests)**: 100% coverage is what makes each speculative change safe.
- **Ch 14 / Ch 16**: the same tiny-step refactoring discipline, here applied to code that was already clean.
- **Ch 17**: [G9] dead code, [G11] inconsistency, [G28] encapsulate conditionals, [G29] avoid negative conditionals, [G30] functions should do one thing, [G31] hidden temporal couplings, [G32] don't be arbitrary, [G33] encapsulate boundary conditions.
