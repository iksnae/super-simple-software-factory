# Chapter 17: Smells and Heuristics

## Core Idea
The complete catalogue — Fowler's code smells plus Martin's own, compiled by refactoring several programs and writing down *why* each change was made. "What this list does do is imply a value system... Clean code is not written by following a set of rules. Professionalism and craftsmanship come from values that drive disciplines."

## Reference Tables

### Comments (C)

| ID | Heuristic | Substance |
|---|---|---|
| **C1** | Inappropriate Information | Meta-data (authors, last-modified date, SPR numbers, change histories) belongs in source control or issue tracking. Comments are for technical notes about the code and design. |
| **C2** | Obsolete Comment | Old, irrelevant, incorrect. Best not to write one that will become obsolete; when found, update or delete immediately. They "migrate away from the code they once described. They become floating islands of irrelevance and misdirection." |
| **C3** | Redundant Comment | `i++; // increment i`, or a Javadoc that says no more than the signature. "Comments should say things that the code cannot say for itself." |
| **C4** | Poorly Written Comment | "A comment worth writing is worth writing well." Correct grammar and punctuation, no rambling, no stating the obvious, be brief. |
| **C5** | Commented-Out Code | "An abomination." It calls functions that no longer exist, uses renamed variables, follows obsolete conventions. Delete it — source control remembers. |

### Environment (E)

| ID | Heuristic | Substance |
|---|---|---|
| **E1** | Build Requires More Than One Step | One command to check out, one to build. `svn get mySystem && cd mySystem && ant all` |
| **E2** | Tests Require More Than One Step | One button in the IDE, or one shell command. "So fundamental and so important that it should be quick, easy, and obvious." |

### Functions (F)

| ID | Heuristic | Substance |
|---|---|---|
| **F1** | Too Many Arguments | None is best, then one, two, three. "More than three is very questionable and should be avoided with prejudice." |
| **F2** | Output Arguments | Counterintuitive — readers expect inputs. Change the state of the object the function is called on instead. |
| **F3** | Flag Arguments | "Boolean arguments loudly declare that the function does more than one thing." |
| **F4** | Dead Function | Never called → discard. "Your source code control system still remembers it." |

### General (G)

| ID | Heuristic | Substance |
|---|---|---|
| **G1** | Multiple Languages in One Source File | A Java file may hold XML, HTML, YAML, Javadoc, English, JavaScript. "Confusing at best and carelessly sloppy at worst." Ideal is one language per file; minimize both the number and extent of extras. |
| **G2** | Obvious Behavior Is Unimplemented | The Principle of Least Surprise. `StringToDay("Monday")` should give `Day.MONDAY`, handle abbreviations, ignore case. When violated, readers "lose their trust in the original author and must fall back on reading the details of the code." |
| **G3** | Incorrect Behavior at the Boundaries | "Don't rely on your intuition. Look for every boundary condition and write a test for it." |
| **G4** | Overridden Safeties | Chernobyl melted down because the plant manager overrode each safety in turn. Turning off compiler warnings or failing tests "is as bad as pretending your credit cards are free money." |
| **G5** | Duplication | DRY (Hunt & Thomas), "Once, and only once" (Beck). Every duplication is a missed abstraction. Identical clumps → methods. Repeated switch/if-else chains on the same conditions → polymorphism. Similar algorithms without similar lines → TEMPLATE METHOD or STRATEGY. |
| **G6** | Code at Wrong Level of Abstraction | Separation must be **complete** — all lower-level concepts in derivatives, all higher-level in the base. "You cannot lie or fake your way out of a misplaced abstraction." |
| **G7** | Base Classes Depending on Their Derivatives | Base classes should know nothing about derivatives, so they can deploy in separate jars and be redeployed independently. Exception: a strictly fixed derivative set with base-class selection, e.g. finite state machines. |
| **G8** | Too Much Information | "Well-defined modules have very small interfaces that allow you to do a lot with a little." Hide data, utility functions, constants, temporaries. Fewer methods, fewer instance variables, fewer protected members. |
| **G9** | Dead Code | Unreachable `if` branches, `catch` blocks for exceptions never thrown, uncalled utilities, impossible switch cases. "It still compiles, but it does not follow newer conventions or rules." Give it a decent burial. |
| **G10** | Vertical Separation | Local variables declared just above first use, small vertical scope. Private functions defined just below first use — finding one should be "a matter of scanning downward." |
| **G11** | Inconsistency | Principle of least surprise. If a variable holding `HttpServletResponse` is `response` in one function, it is `response` everywhere. If one method is `processVerificationRequest`, its sibling is `processDeletionRequest`. |
| **G12** | Clutter | Empty default constructors, unused variables, uncalled functions, information-free comments. Remove them. |
| **G13** | Artificial Coupling | Coupling that serves no direct purpose — general enums nested in specific classes, general-purpose statics declared in specific classes. "A result of putting a variable, constant, or function in a temporarily convenient, though inappropriate, location. This is lazy and careless." |
| **G14** | Feature Envy | A method that uses another object's accessors and mutators to manipulate its data "wishes that it were inside that other class." Sometimes a necessary evil — moving a report format string into `HourlyEmployee` would violate SRP, OCP, and the Common Closure Principle. |
| **G15** | Selector Arguments | "Hardly anything more abominable than a dangling `false` argument at the end of a function call." Selectors need not be boolean — enums and ints count. "In general it is better to have many functions than to pass some code into a function to select the behavior." |
| **G16** | Obscured Intent | Run-on expressions, Hungarian notation, magic numbers. `m_otCalc()` is "small and dense... also virtually impenetrable." |
| **G17** | Misplaced Responsibility | Code goes where a reader would naturally expect it. `PI` with the trig functions; `OVERTIME_RATE` in `HourlyPayCalculator`. Use function names to decide — `getTotalHours` implies the total is computed there, `saveTimeCard` does not. |
| **G18** | Inappropriate Static | `Math.max(a, b)` is a good static — all data from arguments, no chance of wanting polymorphism. `HourlyPayCalculator.calculatePay(...)` is not, because you may want `OvertimeHourlyPayCalculator` and `StraightTimeHourlyPayCalculator`. **Prefer nonstatic. When in doubt, make it nonstatic.** |
| **G19** | Use Explanatory Variables | Break calculations into named intermediate values. "It is hard to overdo this. More explanatory variables are generally better than fewer." |
| **G20** | Function Names Should Say What They Do | `date.add(5)` — days? weeks? mutating or returning? If it mutates, `addDaysTo`/`increaseByDays`; if it returns a new value, `daysLater`/`daysSince`. "If you have to look at the implementation to know what it does, then you should work to find a better name." |
| **G21** | Understand the Algorithm | Getting it to "work" by adding `if`s and flags is a legitimate exploration, but not a stopping point. "It is not good enough that it passes all the tests. You must know that the solution is correct." Best route to that knowledge: refactor until it's obvious. |
| **G22** | Make Logical Dependencies Physical | The dependent module must explicitly *ask* for what it depends on, not assume it. `PAGE_SIZE = 55` in `HourlyReporter` assumes the formatter can handle 55 — physicalize it as `formatter.getMaxPageSize()`. |
| **G23** | Prefer Polymorphism to If/Else or Switch/Case | "Most people use switch statements because it's the obvious brute force solution, not because it's the right solution." Cases where functions are more volatile than types are rare, "so every switch statement should be suspect." **The ONE SWITCH rule**: no more than one switch for a given type of selection, and its cases must create the polymorphic objects that replace all the others. |
| **G24** | Follow Standard Conventions | Team coding standard based on industry norms. "The team should not need a document to describe these conventions because their code provides the examples." Each member must be "mature enough to realize that it doesn't matter a whit where you put your braces so long as you all agree." |
| **G25** | Replace Magic Numbers with Named Constants | 86,400 → `SECONDS_PER_DAY`; 55 → `LINES_PER_PAGE`. **With judgment**: `feetWalked/5280.0`, `hourlyRate * 8`, and `radius * Math.PI * 2` read fine raw. Applies to any non-self-describing token, not just numbers — `assertEquals(7777, Employee.find("John Doe")...)` has *two* magic values. |
| **G26** | Be Precise | "Using floating point numbers to represent currency is almost criminal." Expecting the first match to be the only match is naive; skipping locks because concurrent update seems unlikely is lazy; declaring `ArrayList` where `List` will do over-constrains; defaulting everything to protected under-constrains. |
| **G27** | Structure over Convention | "Naming conventions are good, but they are inferior to structures that force compliance." A switch over well-named enums is inferior to a base class with abstract methods, because nothing forces every switch to be written the same way. |
| **G28** | Encapsulate Conditionals | `if (shouldBeDeleted(timer))` over `if (timer.hasExpired() && !timer.isRecurrent())`. |
| **G29** | Avoid Negative Conditionals | `if (buffer.shouldCompact())` over `if (!buffer.shouldNotCompact())`. |
| **G30** | Functions Should Do One Thing | A function with sections performing a series of operations should become several functions. |
| **G31** | Hidden Temporal Couplings | Temporal coupling is often necessary; hiding it is not. Structure arguments so the call order is forced — a **bucket brigade** where each function produces what the next needs. The extra syntactic complexity "exposes the true temporal complexity of the situation." |
| **G32** | Don't Be Arbitrary | "If a structure appears arbitrary, others will feel empowered to change it. If a structure appears consistently throughout the system, others will use it and preserve the convention." Public classes that aren't utilities of another class belong at the top level of their package. |
| **G33** | Encapsulate Boundary Conditions | "We don't want swarms of +1s and -1s scattered hither and yon." `level + 1` appearing twice becomes `int nextLevel = level + 1;`. |
| **G34** | Functions Should Descend Only One Level of Abstraction | "This may be the hardest of these heuristics to interpret and follow... humans are just far too good at seamlessly mixing levels of abstraction." |
| **G35** | Keep Configurable Data at High Levels | Defaults known at a high level should not be buried in low-level functions; expose them as arguments passed down. FitNesse's `Arguments` class holds `DEFAULT_PATH`, `DEFAULT_ROOT`, `DEFAULT_PORT`, `DEFAULT_VERSION_DAYS` at the top. "The lower levels of the application do not own the values of these constants." |
| **G36** | Avoid Transitive Navigation | The Law of Demeter; the Pragmatic Programmers' "Writing Shy Code." If many modules say `a.getB().getC()`, interposing a `Q` between `B` and `C` requires finding every one. "This is how architectures become rigid." |

### Java (J)

| ID | Heuristic | Substance |
|---|---|---|
| **J1** | Avoid Long Import Lists by Using Wildcards | Two or more classes from a package → import the package. **Specific imports are hard dependencies; wildcard imports are not** — a wildcard just adds the package to the name search path, so no true dependency is created. Rare exception: legacy code where you're enumerating classes to mock. |
| **J2** | Don't Inherit Constants | Putting constants in an interface and inheriting it hides them at the top of the hierarchy. "This is a hideous practice! ... Don't use inheritance as a way to cheat the scoping rules of the language. Use a static import instead." |
| **J3** | Constants versus Enums | Since Java 5, use enums. "The meaning of ints can get lost. The meaning of enums cannot, because they belong to an enumeration that is named." Study the syntax — enums can have methods and fields, allowing far more expression and flexibility than ints. |

### Names (N)

| ID | Heuristic | Substance |
|---|---|---|
| **N1** | Choose Descriptive Names | "Names in software are 90 percent of what make software readable." Meanings drift as software evolves, so reevaluate frequently. |
| **N2** | Choose Names at the Appropriate Level of Abstraction | Don't encode implementation. `Modem.dial(phoneNumber)` breaks for hard-wired or USB-switched modems; `connect(connectionLocator)` doesn't. |
| **N3** | Use Standard Nomenclature Where Possible | Pattern names (`AutoHangupModemDecorator`), language conventions (`toString`), and Eric Evans's **ubiquitous language** for the project. |
| **N4** | Unambiguous Names | `doRename` containing a call to `renamePage` tells you nothing about the difference. Better: `renamePageAndOptionallyAllReferences` — long, but "it's only called from one place in the module, so its explanatory value outweighs the length." |
| **N5** | Use Long Names for Long Scopes | `i` and `j` are fine in a five-line scope and would be *obfuscated* by `rollCount`. "The longer the scope of the name, the longer and more precise the name should be." |
| **N6** | Avoid Encodings | No `m_`, no `f`, no subsystem prefixes like `vis_`. "Keep your names free of Hungarian pollution." |
| **N7** | Names Should Describe Side-Effects | `getOos()` that lazily *creates* the stream should be `createOrReturnOos`. |

### Tests (T)

| ID | Heuristic | Substance |
|---|---|---|
| **T1** | Insufficient Tests | The common metric is "that seems like enough." A suite should test everything that could possibly break — insufficient while any condition is unexplored or any calculation unvalidated. |
| **T2** | Use a Coverage Tool! | Reports gaps; most IDEs mark covered lines green and uncovered red, making unchecked `if`/`catch` bodies obvious. |
| **T3** | Don't Skip Trivial Tests | "Their documentary value is higher than the cost to produce them." |
| **T4** | An Ignored Test Is a Question about an Ambiguity | Express uncertainty about unclear requirements as a commented-out or `@Ignore`d test. Choose between them based on whether the ambiguity would compile. |
| **T5** | Test Boundary Conditions | "We often get the middle of an algorithm right but misjudge the boundaries." |
| **T6** | Exhaustively Test Near Bugs | "Bugs tend to congregate." Finding one warrants exhaustive testing of that function. |
| **T7** | Patterns of Failure Are Revealing | Complete test cases, ordered reasonably, expose patterns — "all tests with input larger than five characters failed," "any test passing a negative second argument failed." Sometimes the red/green pattern alone sparks the solution. |
| **T8** | Test Coverage Patterns Can Be Revealing | What the *passing* tests do and don't execute gives clues to why the failing ones fail. |
| **T9** | Tests Should Be Fast | "A slow test is a test that won't get run. When things get tight, it's the slow tests that will be dropped from the suite." |

## Code Examples

**G14 Feature Envy** — and the case where it's a necessary evil:

```java
// envious: reaches into HourlyEmployee for everything it operates on
public class HourlyPayCalculator {
    public Money calculateWeeklyPay(HourlyEmployee e) {
        int tenthRate = e.getTenthRate().getPennies();
        int tenthsWorked = e.getTenthsWorked();
        int straightTime = Math.min(400, tenthsWorked);
        int overTime = Math.max(0, tenthsWorked - straightTime);
        int straightPay = straightTime * tenthRate;
        int overtimePay = (int)Math.round(overTime*tenthRate*1.5);
        return new Money(straightPay + overtimePay);
    }
}
```
```java
// also envious — and correctly left that way, because moving the format
// string into HourlyEmployee would couple it to the report's format
public class HourlyEmployeeReport {
    private HourlyEmployee employee;

    String reportHours() {
        return String.format(
            "Name: %s\tHours:%d.%1d\n",
            employee.getName(),
            employee.getTenthsWorked()/10,
            employee.getTenthsWorked()%10);
    }
}
```

**G15 Selector Arguments** — and the functions the author failed to write:

```java
// what does calculateWeeklyPay(false) mean?
public int calculateWeeklyPay(boolean overtime) {
    int tenthRate = getTenthRate();
    int tenthsWorked = getTenthsWorked();
    int straightTime = Math.min(400, tenthsWorked);
    int overTime = Math.max(0, tenthsWorked - straightTime);
    int straightPay = straightTime * tenthRate;
    double overtimeRate = overtime ? 1.5 : 1.0 * tenthRate;
    int overtimePay = (int)Math.round(overTime*overtimeRate);
    return straightPay + overtimePay;
}
```
```java
public int straightPay() {
    return getTenthsWorked() * getTenthRate();
}

public int overTimePay() {
    int overTimeTenths = Math.max(0, getTenthsWorked() - 400);
    int overTimePay = overTimeBonus(overTimeTenths);
    return straightPay() + overTimePay;
}

private int overTimeBonus(int overTimeTenths) {
    double bonus = 0.5 * getTenthRate() * overTimeTenths;
    return (int) Math.round(bonus);
}
```

**G31 Hidden Temporal Couplings** — the bucket brigade:

```java
// order matters, nothing enforces it: calling reticulateSplines first
// yields an UnsaturatedGradientException
public void dive(String reason) {
    saturateGradient();
    reticulateSplines();
    diveForMoog(reason);
}
```
```java
// each function produces what the next needs — no reasonable way to
// call them out of order
public void dive(String reason) {
    Gradient gradient = saturateGradient();
    List<Spline> splines = reticulateSplines(gradient);
    diveForMoog(splines, reason);
}
```
Note: Martin keeps the instance variables (private methods need them) *and* adds the arguments anyway, purely to make the coupling explicit.

**N1 Choose Descriptive Names** — the bowling scorer, before and after:

```java
public int x() {
    int q = 0;
    int z = 0;
    for (int kk = 0; kk < 10; kk++) {
        if (l[z] == 10) {
            q += 10 + (l[z + 1] + l[z + 2]);
            z += 1;
        } else if (l[z] + l[z + 1] == 10) {
            q += 10 + l[z + 2];
            z += 2;
        } else {
            q += l[z] + l[z + 1];
            z += 2;
        }
    }
    return q;
}
```
```java
public int score() {
    int score = 0;
    int frame = 0;
    for (int frameNumber = 0; frameNumber < 10; frameNumber++) {
        if (isStrike(frame)) {
            score += 10 + nextTwoBallsForStrike(frame);
            frame += 1;
        } else if (isSpare(frame)) {
            score += 10 + nextBallForSpare(frame);
            frame += 2;
        } else {
            score += twoBallsInFrame(frame);
            frame += 2;
        }
    }
    return score;
}
```
- **What it demonstrates**: the second snippet is *less complete* than the first, yet you can infer what it does and could write the missing functions from the inferred meaning. "The power of carefully chosen names is that they overload the structure of the code with description." Reading `isStrike` afterward will be "pretty much what you expected" (Ward Cunningham, Ch 1).

**J3 Constants versus Enums** — an enum carrying behavior:

```java
public enum HourlyPayGrade {
    APPRENTICE           { public double rate() { return 1.0; } },
    LEUTENANT_JOURNEYMAN { public double rate() { return 1.2; } },
    JOURNEYMAN           { public double rate() { return 1.5; } },
    MASTER               { public double rate() { return 2.0; } };

    public abstract double rate();
}
```

## Worked Example
**G34, and the lesson that abstraction levels hide inside each other.** From FitNesse's `HruleWidget`, which converts a row of four or more dashes into an `<hr>` tag whose size grows with the dash count:

```java
public String render() throws Exception {
    StringBuffer html = new StringBuffer("<hr");
    if(size > 0)
        html.append(" size=\"").append(size + 1).append("\"");
    html.append(">");
    return html.toString();
}
```

Two levels are tangled: the notion that a horizontal rule *has a size*, and the *syntax of the HR tag*. Martin's first attempt at separation:

```java
public String render() throws Exception {
    HtmlTag hr = new HtmlTag("hr");
    if (size > 0) {
        hr.addAttribute("size", ""+(size+1));
    }
    return hr.html();
}
```

Tests pass, and the tag syntax is now `HtmlTag`'s problem — but the function *still* mixes levels: constructing the tag, and interpreting/formatting the size. "When you break a function along lines of abstraction, you often uncover new lines of abstraction that were obscured by the previous structure." The second pass, which also renames `size` to reflect what it actually held:

```java
public String render() throws Exception {
    HtmlTag hr = new HtmlTag("hr");
    if (extraDashes > 0)
        hr.addAttribute("size", hrSize(extraDashes));
    return hr.html();
}

private String hrSize(int height) {
    int hrSize = height + 1;
    return String.format("%d", hrSize);
}
```

And the payoff nobody was looking for: the change **caught a subtle bug**. The original emitted `<hr>` rather than the XHTML-conformant `<hr/>`; `HtmlTag` had been updated to XHTML long ago, and hand-built markup had drifted from it silently. "Separating levels of abstraction is one of the most important functions of refactoring, and it's one of the hardest to do well."

## Key Takeaways
1. The list is deliberately incomplete — "perhaps completeness should not be the goal, because what this list does do is imply a value system."
2. Duplication [G5] and abstraction-level violations [G6][G34] are the two that recur most across the book's case studies.
3. Several heuristics are about *forcing* correctness rather than documenting it: structure over convention [G27], physical over logical dependencies [G22], exposed temporal coupling [G31].
4. Names carry 90% of readability [N1]; scope length sets name length [N5]; names must confess side effects [N7] and avoid implying implementation [N2].
5. Prefer nonstatic and polymorphic by default [G18][G23]; every switch is suspect, and the ONE SWITCH rule bounds the exceptions.
6. Test heuristics are diagnostic tools, not hygiene: failure patterns [T7] and coverage patterns [T8] locate bugs, and bugs congregate [T6].
7. Judgment is required throughout — magic numbers sometimes read better raw [G25], Feature Envy is sometimes the right trade [G14], and switches are occasionally correct [G23].
8. "You don't become a software craftsman by learning a list of heuristics."

## Connects To
- **Every chapter**: this catalogue is the book's index of practice. Appendix C cross-references each heuristic to where it appears in the text.
- **Ch 15 / Ch 16**: the two case studies where these tags are applied by number, change by change.
- **Ch 12 (Emergence)**: duplication and expressiveness as the rules that drive design.
- **[Refactoring]** Fowler: the original code smells, including Feature Envy. **[PRAG]**: DRY, Writing Shy Code. **[GOF]**: TEMPLATE METHOD, STRATEGY, DECORATOR. **[Beck97]/[Beck07]**: explanatory variables. **[PPP]**: SRP, OCP, Common Closure. **[DDD]** Evans: ubiquitous language.
