# Chapter 3: Functions

## Core Idea
Functions should be small, do exactly one thing, stay at a single level of abstraction, take as few arguments as possible, and have no side effects — because functions are the verbs of the domain-specific language your system is written in.

## Frameworks Introduced
- **Small! (and then smaller)**: "The first rule of functions is that they should be small. The second rule of functions is that they should be smaller than that."
  - When to use: every function you write or touch.
  - How: functions should hardly ever be 20 lines long. Martin's benchmark is Kent Beck's *Sparkle* program — every function two, three, or four lines, each transparently obvious, each leading to the next.
- **Blocks and Indenting**: the body of an `if`/`else`/`while` should be one line, and that line should probably be a function call.
  - How: indent level of a function should not exceed one or two. This also buys documentary value, since the called function gets a descriptive name.
- **Do One Thing**: "FUNCTIONS SHOULD DO ONE THING. THEY SHOULD DO IT WELL. THEY SHOULD DO IT ONLY."
  - How to tell: a function does one thing if all its steps are **one level of abstraction below its name**. Two tests — (a) can you extract another function from it whose name is not just a restatement of the implementation [G34]? If yes, it does more than one thing. (b) Can it be divided into sections (`declarations`, `initializations`, `sieve`)? If yes, it does more than one thing.
- **The TO Paragraph test**: describe the function as "TO *FunctionName*, we …". If the description needs steps at mixed levels, the function is not doing one thing. (LOGO used `TO` where Ruby/Python use `def`.)
- **The Stepdown Rule**: code should read like a top-down narrative — every function followed by those one level of abstraction lower, so you descend one level at a time reading down the file.
- **Command Query Separation** (Meyer): a function either *does* something or *answers* something, never both.
  - How: `if (set("username", "unclebob"))` is ambiguous — is `set` verb or adjective? Split into `attributeExists(…)` then `setAttribute(…)`.
- **Prefer Exceptions to Returning Error Codes**: error codes are a subtle CQS violation and force the caller to handle the error immediately, producing deep nesting.
- **Extract Try/Catch Blocks**: pull the `try` body and the `catch` body into their own functions, so one function is all error processing and the other is all happy path.
- **Error Handling Is One Thing**: if `try` appears in a function it must be the very first word, and nothing may follow the `catch`/`finally` blocks.
- **DRY — Don't Repeat Yourself**: "Duplication may be the root of all evil in software."
  - How: Listing 3-1 repeats one algorithm four times (SetUp, SuiteSetUp, TearDown, SuiteTearDown), non-uniformly, so it is hard to spot. Four-fold change cost, four-fold chance of an error of omission.

## Key Concepts
- **Niladic / monadic / dyadic / triadic / polyadic** — 0/1/2/3/many arguments. Ideal is zero; three should be avoided; more than three "requires very special justification — and then shouldn't be used anyway."
- **Flag argument** — a boolean parameter; it "loudly proclaims that this function does more than one thing." Split into `renderForSuite()` and `renderForSingleTest()` instead.
- **Output argument** — a parameter used to return data; forces a double-take and a signature check. In OO, `this` is the natural output argument: prefer `report.appendFooter()` over `appendFooter(report)`.
- **Side effect** — "Side effects are lies." A hidden state change that creates **temporal coupling** and order dependencies.
- **Temporal coupling** — a function that can only be called at certain times; if you must have it, put it in the name (`checkPasswordAndInitializeSession` — which then violates Do One Thing, which is the point).
- **Dependency magnet** — a class or enum (e.g. `public enum Error {…}`) that everything imports, so any change forces recompile/redeploy everywhere. Programmers then reuse wrong error codes rather than add right ones. Exceptions avoid this: new exception types are derivatives, addable without recompilation (an application of OCP).
- **Keyword form** — encoding argument names into the function name: `assertExpectedEqualsActual(expected, actual)` instead of `assertEquals(expected, actual)`.
- **Argument object** — when a function needs 3+ arguments, some of them likely form a concept deserving a name: `makeCircle(Point center, double radius)` over `makeCircle(double x, double y, double radius)`.

## Mental Models
- **Think of functions as verbs and classes as nouns of a domain-specific language.** Master programmers think of systems as stories to be told, not programs to be written. The art of programming is the art of language design.
- **Use polymorphism to bury switch statements.** A `switch` inherently does N things and violates SRP and OCP. Tolerate it only if it appears **once**, is used to **create polymorphic objects**, and is **hidden behind an inheritance relationship** [G23] — typically inside an ABSTRACT FACTORY.
- **Treat argument count as a testing cost.** Zero arguments = trivial to test; each additional argument multiplies the combinations you must cover.
- **Two arguments are only natural when they are ordered components of one value.** `new Point(0,0)` is fine; `writeField(outputStream, name)` is not, because those two have neither cohesion nor natural ordering. Convert dyads to monads: make the method a member of `outputStream`, make `outputStream` a field, or extract a `FieldWriter` class.
- **Relax Dijkstra's single-entry/single-exit rule for small functions.** Multiple `return`, `break`, and `continue` do no harm and are often more expressive when functions are small. `goto` only makes sense in large functions, so avoid it entirely.
- **Write badly first, then refine.** Martin's own functions come out long, nested, badly named, and duplicated — with a full suite of unit tests covering every clumsy line. He then massages: split, rename, de-duplicate, reorder, extract classes, tests green throughout. "I don't write them that way to start. I don't think anyone could."

## Code Examples

The switch-to-polymorphism transformation:

```java
// Listing 3-4 — large, grows with each new type, violates SRP and OCP,
// and an unlimited number of sibling functions will share the same shape
public Money calculatePay(Employee e) throws InvalidEmployeeType {
    switch (e.type) {
        case COMMISSIONED: return calculateCommissionedPay(e);
        case HOURLY:       return calculateHourlyPay(e);
        case SALARIED:     return calculateSalariedPay(e);
        default: throw new InvalidEmployeeType(e.type);
    }
}
```

```java
// Listing 3-5 — the switch survives exactly once, in the factory basement
public abstract class Employee {
    public abstract boolean isPayday();
    public abstract Money calculatePay();
    public abstract void deliverPay(Money pay);
}

public interface EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType;
}

public class EmployeeFactoryImpl implements EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType {
        switch (r.type) {
            case COMMISSIONED: return new CommissionedEmployee(r);
            case HOURLY:       return new HourlyEmployee(r);
            case SALARIED:     return new SalariedEmploye(r);
            default: throw new InvalidEmployeeType(r.type);
        }
    }
}
```
- **What it demonstrates**: `isPayday`, `calculatePay`, and `deliverPay` all dispatch polymorphically; only object *creation* keeps the switch.

Error codes vs. exceptions:

```java
// error codes force immediate handling and deep nesting
if (deletePage(page) == E_OK) {
    if (registry.deleteReference(page.name) == E_OK) {
        if (configKeys.deleteKey(page.name.makeKey()) == E_OK) {
            logger.log("page deleted");
        } else { logger.log("configKey not deleted"); }
    } else { logger.log("deleteReference from registry failed"); }
} else { logger.log("delete failed"); return E_ERROR; }
```

```java
// exceptions separate error processing from the happy path
try {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
} catch (Exception e) {
    logger.log(e.getMessage());
}
```

Extracting try/catch so each function does one thing:

```java
public void delete(Page page) {
    try {
        deletePageAndAllReferences(page);
    } catch (Exception e) {
        logError(e);
    }
}

private void deletePageAndAllReferences(Page page) throws Exception {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
}

private void logError(Exception e) {
    logger.log(e.getMessage());
}
```

The side effect that lies (Listing 3-6):

```java
public class UserValidator {
    private Cryptographer cryptographer;

    public boolean checkPassword(String userName, String password) {
        User user = UserGateway.findByName(userName);
        if (user != User.NULL) {
            String codedPhrase = user.getPhraseEncodedByPassword();
            String phrase = cryptographer.decrypt(codedPhrase, password);
            if ("Valid Password".equals(phrase)) {
                Session.initialize();   // <-- the lie
                return true;
            }
        }
        return false;
    }
}
```
- **What it demonstrates**: the name promises a check; the call erases existing session data. A caller who trusts the name loses data when calling out of order.

## Reference Tables

| Argument count | Name | Verdict | Notes |
|---|---|---|---|
| 0 | niladic | Ideal | Trivial to test |
| 1 | monadic | Next best | Three valid forms: ask a question (`fileExists(name)`), transform and return (`fileOpen(name)`), or event (`passwordAttemptFailedNtimes(n)`) |
| 2 | dyadic | Costs something | Justified only when the two are ordered components of one value (`new Point(0,0)`) |
| 3 | triadic | Avoid | `assertEquals(message, expected, actual)` — the message reads as the expected every time |
| 4+ | polyadic | Never | Wrap into an argument object |

Varargs follow the same rule: `format(String format, Object... args)` is dyadic, because identically-treated variable arguments count as one `List` parameter.

## Worked Example
**Listing 3-1 → 3-7: the FitNesse `testableHtml` refactoring.** The original is a long function with duplicated code, odd strings, nested `if`s controlled by flags, and expressions ranging from `getHtml()` (high abstraction) through `PathParser.render(pagePath)` (middle) down to `.append("\n")` (low). Three minutes of study leaves most readers unable to say what it does.

Method extraction, renaming, and restructuring produce a nine-line version (3-2) that any reader can summarize — it includes setup and teardown pages into a test page, then renders HTML. But 3-2 still holds two levels of abstraction, so it shrinks again:

```java
// Listing 3-3
public static String renderPageWithSetupsAndTeardowns(
    PageData pageData, boolean isSuite) throws Exception {
    if (isTestPage(pageData))
        includeSetupAndTeardownPages(pageData, isSuite);
    return pageData.getHtml();
}
```

The endpoint is Listing 3-7, `SetupTeardownIncluder`, where every function is two to four lines and each introduces the next one level down — the Stepdown Rule made literal:

```java
private String render(boolean isSuite) throws Exception {
    this.isSuite = isSuite;
    if (isTestPage())
        includeSetupAndTeardownPages();
    return pageData.getHtml();
}

private void includeSetupAndTeardownPages() throws Exception {
    includeSetupPages();
    includePageContent();
    includeTeardownPages();
    updatePageContent();
}

private void includeSetupPages() throws Exception {
    if (isSuite)
        includeSuiteSetupPage();
    includeSetupPage();
}

private void includeSuiteSetupPage() throws Exception {
    include(SuiteResponder.SUITE_SETUP_NAME, "-setup");
}

private void includeSetupPage() throws Exception {
    include("SetUp", "-setup");
}

// the four-fold duplication of Listing 3-1 collapses into one method
private void include(String pageName, String arg) throws Exception {
    WikiPage inheritedPage = findInheritedPage(pageName);
    if (inheritedPage != null) {
        String pagePathName = getPathNameForPage(inheritedPage);
        buildIncludeDirective(pagePathName, arg);
    }
}
```

Note the naming discipline: `includeSetupAndTeardownPages`, `includeSetupPages`, `includeSuiteSetupPage`, `includeSetupPage`. The phraseology is consistent enough that seeing the setup sequence makes you ask where the teardown siblings are — Ward's "pretty much what you expected," achieved by construction. Note also what the class-based refactoring bought: the `StringBuffer` became a field, which removed it from every signature (`includeSetupPage()` rather than `includeSetupPageInto(newPageContent)`).

## Key Takeaways
1. Small, then smaller. Rarely 20 lines; blocks inside control statements are one line; indent depth one or two.
2. A function does one thing when every statement in it sits one level of abstraction below its name.
3. Read down the file as a stepdown of TO paragraphs; each function introduces the next.
4. Fewer arguments is always better. Flag arguments and output arguments are defects, not style preferences.
5. Separate commands from queries; prefer exceptions over error codes; make error handling its own function.
6. Bury switch statements in a factory and dispatch polymorphically.
7. Duplication is the root of all evil — most of the discipline's innovations since the subroutine exist to eliminate it.
8. Nobody writes clean functions on the first pass. Get it working under test, then refine relentlessly.

## Connects To
- **Ch 2 (Meaningful Names)**: long descriptive names beat short enigmatic ones and beat long descriptive comments; hunting for a good name often produces a better structure.
- **Ch 7 (Error Handling)**: the exceptions-over-error-codes argument is developed in full.
- **Ch 10 (Classes)**: extracting functions eventually extracts classes; SRP applies at both scales.
- **Ch 14 (Successive Refinement)**: the "write it badly, then massage it" process worked end to end.
- **Ch 17**: [G23] prefer polymorphism to if/else or switch/case; [G34] functions should descend only one level of abstraction.
- **PPP / GOF**: SRP, OCP, and ABSTRACT FACTORY.
