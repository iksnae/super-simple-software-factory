# Chapter 16: Refactoring SerialDate

## Core Idea
A full professional code review of someone else's good open-source code, worked end to end: **first make it work** (raise coverage, find and fix the bugs the missing tests were hiding), **then make it right** (walk the class top to bottom, applying the heuristics, running all tests after every change).

## Frameworks Introduced
- **First, Make It Work → Then Make It Right**: the chapter's structure and its method.
  - *Make it work*: you cannot refactor what you cannot verify. Measure coverage, write an independent test suite, comment out the tests describing behavior the class *should* have, and make them pass as you go.
  - *Make it right*: walk the file from line 1 downward, and after every single change run **all** of the framework's tests, not just this class's.
- **Professional review as a normal activity**: "What I am about to do is nothing more and nothing less than a professional review. It is something that we should all be comfortable doing. And it is something we should welcome when it is done for us. It is only through critiques like these that we will learn. Doctors do it. Pilots do it. Lawyers do it. And we programmers need to learn how to do it too."
  - The stance matters: Martin opens by naming David Gilbert as clearly experienced and competent, states plainly that his own code would yield plenty to complain about, and credits Gilbert for offering the code publicly for scrutiny. "This was well done!"
- **ABSTRACT FACTORY to break base-class-knows-derivative** [GOF]: `DayDate.addDays` → `createInstance` → constructs a `SpreadsheetDate` — a base class creating its own derivative [G7]. A `DayDateFactory` fixes it and can also answer implementation questions (min/max year) that clients legitimately need.
- **EXPLAINING TEMPORARY VARIABLES** [Beck97] [G19]: name the intermediate steps of a complicated algorithm rather than compressing it.
- **Replace a switch with polymorphic enum constants** [G23]: `isInRange`'s switch moves into `DateInterval`, where each enumerator implements `isIn`.

## Key Concepts
- **Coverage as a diagnostic map** — Clover reported the original tests executed 91 of 185 executable statements (~50%) [T2]; "the coverage map looks like a patchwork quilt." Martin's replacement suite reached 170/185 (92%).
- **Coverage patterns reveal bugs** [T8] — line 719 never executed, meaning the `if` on 718 was always false: `adjust` is always negative and can never be ≥ 4. "So this algorithm is just wrong."
- **Failure patterns reveal boundary errors** [T7][T5] — which `getNearestDayOfWeek` cases were commented out showed the algorithm fails when the nearest day is in the future.
- **A change history in the code is a signal, not just clutter** [T6] — the header showed prior "bug fixes" in `getPreviousDayOfWeek`, `getFollowingDayOfWeek`, and `getNearestDayOfWeek`. All three were still wrong.
- **Names that imply implementation are at the wrong level of abstraction** [N2] — `SerialDate` is abstract, so it should imply nothing about serial numbers. Martin also rejects "serial number" as inaccurate ("more of a relative offset... 'serial number' has more to do with product identification markers") and settles on `DayDate` as a compromise, since `Date` and `Day` are both taken in the Java library.
- **Constants belong in enums, not in inherited constant classes** [J2] — inheriting from `MonthConstants` to avoid writing `MonthConstants.January` is "an old trick... but it's a bad idea." Converting it took an hour and deleted `isValidMonthCode` and all the month-code error checking [G5], because the type system now does that work.
- **Members belong where they're used** [G6] — `EARLIEST_DATE_ORDINAL`, `LATEST_DATE_ORDINAL`, `MINIMUM/MAXIMUM_YEAR_SUPPORTED`, `leapYearCount`, and several tables all pushed down to `SpreadsheetDate`; `toDate`, `getDayOfWeek`, `compare`, and six other methods pulled *up* into `DayDate`.
- **Logical dependencies should be made physical** [G22] — `getDayOfWeek` has no *physical* dependency on `SpreadsheetDate`, but implicitly depends on the weekday of ordinal day zero. Fix: an abstract `getDayOfWeekForOrdinalZero()` implemented as `Day.SATURDAY`, letting the generic algorithm move up.
- **Martin's dissent on `final`** [G12] — he deleted all `final` keywords on arguments and variables. Robert Simmons recommends "spread `final` all over your code"; Martin disagrees: outside the occasional constant it "adds little value and creates a lot of clutter... Perhaps I feel this way because the kinds of errors that `final` might catch are already caught by the unit tests I write."
- **Martin's dissent on `serialVersionUID`** [G4] — he deleted it, preferring automatic control: "I'd much rather debug an `InvalidClassException` than the odd behavior that would ensue if I forgot to change the `serialVersionUID`." Reviewers objected; his footnote concedes the point is fair and concludes "the real moral of this story is that you should not expect to deserialize across versions."
- **Four languages in one comment** [G1] — Java, English, Javadoc, and HTML in a single file. The careful source-level line positioning is lost when Javadoc renders, and nobody wants `<ul>` and `<li>` in source. Suggested fix: wrap the whole comment in `<pre>`.

## Mental Models
- **A method that operates on a class's own variables should not be static** [G18]. `addDays`, `addMonths`, `addYears`, `getPreviousDayOfWeek`, `getFollowingDayOfWeek` were all converted to instance methods.
- **Then check whether the instance form now lies.** `date.addDays(7); // bump date by one week` reads as mutation and isn't [G20]. Renaming to `plusDays` / `plusMonths` makes `DayDate date = oldDate.plusDays(5);` read correctly, while a bare `date.plusDays(5);` no longer "read[s] fluidly enough for a reader to simply accept that the date object is changed" [N4].
- **A method that envies another class belongs to it** [G14] (FEATURE ENVY, from Fowler). `monthCodeToQuarter` became `Month.quarter()`; `stringToWeekdayCode` became `Day.parse`; `weekdayCodeToString` became `Day.toString`; `monthCodeToString`/`stringToMonthCode` moved into `Month`. `getEndOfCurrentMonth` was an instance method envying *its own class* by taking a `DayDate` argument.
- **A flag argument that selects output format is a smell** [G15] — the paired `monthCodeToString` methods became `toString()` and `toShortString()`.
- **Once constants are symbols rather than integers, they become safe to rename.** "They aren't passed as integers anymore; they are passed as symbols. I can use the 'change name' function of my IDE to change the names, or the types, without worrying that I missed some -1 or 2 somewhere."
- **Prefer standard nomenclature** [N3] — `INCLUDE_NONE`/`INCLUDE_FIRST`/`INCLUDE_SECOND`/`INCLUDE_BOTH` became a `DateInterval` enum with `OPEN`, `CLOSED_LEFT`, `CLOSED_RIGHT`, `CLOSED`, borrowing the mathematics of open and half-open intervals.
- **Falling coverage can mean success.** Final `DayDate` coverage dropped to 84.9% — "not because less functionality is being tested; rather it is because the class has shrunk so much that the few uncovered lines have a greater weight." 45 of 53 executable statements, the rest too trivial to test.

## Code Examples

The boundary-condition bug in `getFollowingDayOfWeek` [G3][T1][T5] — December 25th 2004 was a Saturday, and the function returned December 25th as the Saturday *following* December 25th:

```java
685         if (baseDOW >= targetWeekday) {   // was >
```

The dead-branch bug in `getNearestDayOfWeek`, and the correct algorithm:

```java
int delta = targetDOW - base.getDayOfWeek();
int positiveDelta = delta + 7;
int adjust = positiveDelta % 7;
if (adjust > 3)
    adjust -= 7;
return SerialDate.addDays(adjust, base);
```

The factory that breaks the base→derivative dependency:

```java
public abstract class DayDateFactory {
    private static DayDateFactory factory = new SpreadsheetDateFactory();

    public static void setInstance(DayDateFactory factory) {
        DayDateFactory.factory = factory;
    }

    protected abstract DayDate _makeDate(int ordinal);
    protected abstract DayDate _makeDate(int day, DayDate.Month month, int year);
    protected abstract DayDate _makeDate(int day, int month, int year);
    protected abstract DayDate _makeDate(java.util.Date date);
    protected abstract int _getMinimumYear();
    protected abstract int _getMaximumYear();

    public static DayDate makeDate(int ordinal) {
        return factory._makeDate(ordinal);
    }
    public static int getMinimumYear() { return factory._getMinimumYear(); }
    public static int getMaximumYear() { return factory._getMaximumYear(); }
}
```
- **What it demonstrates**: `createInstance` becomes `makeDate` (a better name [N1]); the static-delegating-to-abstract shape combines SINGLETON, DECORATOR, and ABSTRACT FACTORY — "a combination... that I have found to be useful."

Expressiveness [G16] — `isLeapYear` rewritten so the rule is readable:

```java
public static boolean isLeapYear(int year) {
    boolean fourth = year % 4 == 0;
    boolean hundredth = year % 100 == 0;
    boolean fourHundredth = year % 400 == 0;
    return fourth && (!hundredth || fourHundredth);
}
```

EXPLAINING TEMPORARY VARIABLES [G19] in `addMonths`:

```java
public DayDate addMonths(int months) {
    int thisMonthAsOrdinal = 12 * getYear() + getMonth().index - 1;
    int resultMonthAsOrdinal = thisMonthAsOrdinal + months;
    int resultYear = resultMonthAsOrdinal / 12;
    Month resultMonth = Month.make(resultMonthAsOrdinal % 12 + 1);
    int lastDayOfResultMonth = lastDayOfMonth(resultMonth, resultYear);
    int resultDay = Math.min(getDayOfMonth(), lastDayOfResultMonth);
    return DayDateFactory.makeDate(resultDay, resultMonth, resultYear);
}
```

The three day-of-week functions, made consistent [G11] and simple:

```java
public DayDate getPreviousDayOfWeek(Day targetDayOfWeek) {
    int offsetToTarget = targetDayOfWeek.index - getDayOfWeek().index;
    if (offsetToTarget >= 0)
        offsetToTarget -= 7;
    return plusDays(offsetToTarget);
}

public DayDate getFollowingDayOfWeek(Day targetDayOfWeek) {
    int offsetToTarget = targetDayOfWeek.index - getDayOfWeek().index;
    if (offsetToTarget <= 0)
        offsetToTarget += 7;
    return plusDays(offsetToTarget);
}

public DayDate getNearestDayOfWeek(final Day targetDay) {
    int offsetToThisWeeksTarget = targetDay.index - getDayOfWeek().index;
    int offsetToFutureTarget = (offsetToThisWeeksTarget + 7) % 7;
    int offsetToPreviousTarget = offsetToFutureTarget - 7;
    if (offsetToFutureTarget > 3)
        return plusDays(offsetToPreviousTarget);
    else
        return plusDays(offsetToFutureTarget);
}
```

Switch replaced by polymorphic enum [G23]:

```java
public enum DateInterval {
    OPEN {
        public boolean isIn(int d, int left, int right) {
            return d > left && d < right;
        }
    },
    CLOSED_LEFT {
        public boolean isIn(int d, int left, int right) {
            return d >= left && d < right;
        }
    },
    CLOSED_RIGHT {
        public boolean isIn(int d, int left, int right) {
            return d > left && d <= right;
        }
    },
    CLOSED {
        public boolean isIn(int d, int left, int right) {
            return d >= left && d <= right;
        }
    };
    public abstract boolean isIn(int d, int left, int right);
}

public boolean isInRange(DayDate d1, DayDate d2, DateInterval interval) {
    int left = Math.min(d1.getOrdinalDay(), d2.getOrdinalDay());
    int right = Math.max(d1.getOrdinalDay(), d2.getOrdinalDay());
    return interval.isIn(getOrdinalDay(), left, right);
}
```

## Worked Example
**The elegant refactoring chain that ended in a delete — twice.** Refactoring `weekInMonthToString` is the chapter's best-told sequence, and its lesson is the opposite of what it appears to be.

Step by step, using the IDE's refactoring tools:
1. Move the method into the `WeekInMonth` enum created earlier. Tests pass.
2. Rename it to `toString`. Tests pass.
3. Change it from static to an instance method. Tests pass.
4. **Delete the method entirely.** Five asserts fail.
5. Change those five assertions to use the enumerator names (`FIRST`, `SECOND`, …). All tests pass.

Why it works: every enumerator implements `toString` to return its own name, so the refactoring tool had already redirected every caller of `weekInMonthToString` to `toString` on the enumerator — which now needs no implementation at all. The whole method dissolved.

Then the deflation: "Unfortunately, I was a bit too clever. As elegant as that wonderful chain of refactorings was, I finally realized that the only users of this function were the tests I had just modified, so I deleted the tests."

And the lesson applied immediately: "Fool me once, shame on you. Fool me twice, shame on me! So after determining that nobody other than the tests called `relativeToString`, I simply deleted the function and its tests."

**Check for callers before you refactor.** A beautiful transformation of dead code is still work spent on dead code.

**The final pass.** After reaching the bottom of the class, Martin makes one more sweep for flow: shorten the out-of-date opening comment [C2]; move all remaining enums into their own files [G12]; move `dateFormatSymbols`, `getMonthNames`, `isLeapYear`, and `lastDayOfMonth` into a new `DateUtil` class [G6]; move abstract methods to the top where they belong [G24]; rename `Month.make` to `Month.fromInt` and add `toInt()` accessors with private index fields [N1]; extract `correctLastDayOfMonth` to remove duplication between `plusYears` and `plusMonths` [G5]; and replace the magic number 1 with `Month.JANUARY.toInt()` or `Day.SUNDAY.toInt()` [G25].

## Key Takeaways
1. Raise coverage before refactoring; you cannot restructure what you cannot verify.
2. Read the coverage map and the failure pattern as diagnostics — unexecuted lines and clustered failures point straight at bugs.
3. Comment out tests describing behavior the class *should* have, then make them pass as the refactoring proceeds.
4. Run the whole framework's tests after every change, not just the class's own.
5. Push members down to the implementation that uses them; pull implementations up when they don't depend on the derivative — and when a logical dependency remains, make it physical.
6. Convert constant sets to enums, then move envying methods onto them; the type system deletes whole categories of validation code.
7. Rename until the call site cannot be misread — `addDays` implies mutation, `plusDays` does not.
8. Check for callers before refactoring; the most elegant chain of transformations is wasted on dead code.
9. Review is a normal professional act. Offer it without malice, welcome it without defensiveness.

## Connects To
- **Ch 1 (Clean Code)**: the Boy Scout Rule, the chapter's closing justification.
- **Ch 3 (Functions)**: flag arguments [G15], burying switches, small instance methods.
- **Ch 4 (Comments)**: change history [C1], redundant comments [C2][C3], HTML in comments.
- **Ch 9 (Unit Tests)**: the `testAddMonths` example from this codebase; insufficient tests [T1], coverage tools [T2].
- **Ch 14 / Ch 15**: the same successive-refinement discipline, here applied to a stranger's code.
- **Ch 17 (Smells and Heuristics)**: this chapter is the heuristics catalogue in action — nearly every fix carries its [Gn]/[Nn]/[Tn]/[Cn]/[Jn] tag.
- **Appendix B**: full listings B-1 through B-16.
- **[GOF]**: ABSTRACT FACTORY, SINGLETON, DECORATOR. **[Refactoring]**: Feature Envy. **[Beck97]**: explaining temporary variables. **[Simmons04]**: the `final` recommendation Martin rejects.
