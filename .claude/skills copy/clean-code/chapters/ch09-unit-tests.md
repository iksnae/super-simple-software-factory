# Chapter 9: Unit Tests

## Core Idea
Test code is just as important as production code — it is not a second-class citizen — because tests are the thing that lets you change production code without fear, and dirty tests are equivalent to, if not worse than, no tests.

## Frameworks Introduced
- **The Three Laws of TDD**:
  1. **First Law** — You may not write production code until you have written a failing unit test.
  2. **Second Law** — You may not write more of a unit test than is sufficient to fail, and **not compiling is failing**.
  3. **Third Law** — You may not write more production code than is sufficient to pass the currently failing test.
  - Effect: a cycle roughly **thirty seconds** long, tests running a few seconds ahead of production code. Dozens of tests a day, thousands a year, covering virtually all production code — a bulk that can rival the production code itself.
- **BUILD-OPERATE-CHECK**: every test splits into three visible parts — build the test data, operate on it, check that the operation yielded the expected result.
- **Domain-Specific Testing Language**: rather than using the APIs programmers use to manipulate the system, build a set of functions and utilities that make tests convenient to write and easy to read.
  - When to use: whenever obfuscating detail creeps into tests.
  - How: **it is not designed up front** — it evolves from continued refactoring of test code that has gotten too tainted by detail.
- **A Dual Standard**: test code must be simple, succinct, and expressive, but need not be as *efficient* as production code, because the test environment's constraints differ from production's.
  - The boundary: things you'd never do in production may be fine in a test when they involve **memory or CPU efficiency**. "But they never involve issues of cleanliness."
- **One Assert per Test**: a good guideline, not a law. Martin tries to build a DSL that supports it, "but I am not afraid to put more than one assert in a test."
- **Single Concept per Test** — the better rule: minimize asserts *per concept*, and test just one concept per test function.
- **F.I.R.S.T.**: **F**ast, **I**ndependent, **R**epeatable, **S**elf-Validating, **T**imely.

## Key Concepts
- **Tests enable the -ilities** — flexibility, maintainability, reusability. "Tests enable all the -ilities, because tests enable change." The higher the coverage, the less the fear; with tests you can improve a poor architecture *without fear*.
- **The death spiral of dirty tests** — tests must change as production code evolves; dirty tests are hard to change; cramming new tests in costs more than the production code; old tests fail and are hard to fix; the suite becomes a liability and is discarded; defect rate rises; fear of change returns; cleaning stops; production code rots. Martin coached a team through exactly this.
- **Clean test = readability, readability, readability** — clarity, simplicity, and density of expression. Say a lot with as few expressions as possible. Readability matters *more* in tests than in production code.
- **given-when-then** naming convention [RSpec] — `givenPages(...)`, `whenRequestIsIssued(...)`, `thenResponseShouldBeXML()`.
- **Encapsulation vs. tests** — "For us, tests rule." If a test in the same package needs a member, make it protected or package scope — but look for a way to keep it private first. Loosening encapsulation is always a last resort.

## Mental Models
- **Test code is where you spend design effort, not where you save it.** The team that gave itself "license to break the rules in their unit tests" lost the tests, then the production code.
- **When splitting tests creates duplication, weigh the mechanism against the benefit.** TEMPLATE METHOD [GOF] with given/when in a base class, or a separate class with given/when in `@Before`, both work — Martin judges them "too much mechanism for such a minor issue" and keeps the multiple asserts.
- **Miscellaneous tests hide missing tests.** Re-stating a lumped test as separate given/when/then sentences exposes the general rule underneath — and therefore the case nobody wrote.
- **Slow tests rot code.** Slow → run rarely → problems found late → afraid to clean → rot. The F in FIRST is a causal chain, not a preference.
- **Timely matters because testability is a design property.** Write tests *just before* the production code that passes them; write them after and you may find the code hard to test, or decide some of it is too hard to test at all.

## Reference Tables

F.I.R.S.T. in full:

| Letter | Rule | Failure mode if violated |
|---|---|---|
| **Fast** | Tests run quickly | You run them rarely, find problems late, stop cleaning, code rots |
| **Independent** | No test sets up conditions for another; any order | One failure cascades, diagnosis is hard, downstream defects hide |
| **Repeatable** | Runs in production, QA, and on a laptop with no network | You always have an excuse for a failure, and can't run them when the environment is missing |
| **Self-Validating** | Boolean output — pass or fail | Failure becomes subjective; requires reading logs or diffing files |
| **Timely** | Written just before the production code that passes them | Production code turns out to be hard or impossible to test |

## Code Examples

Tests obscured by detail (Listing 9-1), and the same tests refactored (9-2):

```java
// Listing 9-1 — duplication [G5] plus a swarm of irrelevant detail
public void testGetPageHieratchyAsXml() throws Exception {
    crawler.addPage(root, PathParser.parse("PageOne"));
    crawler.addPage(root, PathParser.parse("PageOne.ChildOne"));
    crawler.addPage(root, PathParser.parse("PageTwo"));

    request.setResource("root");
    request.addInput("type", "pages");
    Responder responder = new SerializedPageResponder();
    SimpleResponse response = (SimpleResponse) responder.makeResponse(
        new FitNesseContext(root), request);
    String xml = response.getContent();

    assertEquals("text/xml", response.getContentType());
    assertSubString("<name>PageOne</name>", xml);
    assertSubString("<name>PageTwo</name>", xml);
    assertSubString("<name>ChildOne</name>", xml);
}
```
```java
// Listing 9-2 — BUILD-OPERATE-CHECK is visible in the shape
public void testGetPageHierarchyAsXml() throws Exception {
    makePages("PageOne", "PageOne.ChildOne", "PageTwo");

    submitRequest("root", "type:pages");

    assertResponseIsXML();
    assertResponseContains(
        "<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>"
    );
}

public void testSymbolicLinksAreNotInXmlPageHierarchy() throws Exception {
    WikiPage page = makePage("PageOne");
    makePages("PageOne.ChildOne", "PageTwo");
    addLinkTo(page, "PageTwo", "SymPage");

    submitRequest("root", "type:pages");

    assertResponseIsXML();
    assertResponseContains(
        "<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>"
    );
    assertResponseDoesNotContain("SymPage");
}
```
- **What it demonstrates**: the `PathParser` calls, responder construction, and response casting were all noise. "In the end, this code was not designed to be read." (Martin notes he helped write the original, "so I feel free to roundly criticize it.")

One concept per test — Listing 9-8, the counter-example:

```java
/**
 * Miscellaneous tests for the addMonths() method.
 */
public void testAddMonths() {
    SerialDate d1 = SerialDate.createInstance(31, 5, 2004);

    SerialDate d2 = SerialDate.addMonths(1, d1);
    assertEquals(30, d2.getDayOfMonth());
    assertEquals(6, d2.getMonth());
    assertEquals(2004, d2.getYYYY());

    SerialDate d3 = SerialDate.addMonths(2, d1);
    assertEquals(31, d3.getDayOfMonth());
    assertEquals(7, d3.getMonth());
    assertEquals(2004, d3.getYYYY());

    SerialDate d4 = SerialDate.addMonths(1, SerialDate.addMonths(1, d1));
    assertEquals(30, d4.getDayOfMonth());
    assertEquals(7, d4.getMonth());
    assertEquals(2004, d4.getYYYY());
}
```
- **What it demonstrates**: the problem is not the multiple asserts per section; it is that three independent concepts share one function. Restated as given/when/then sentences, a general rule surfaces — *when you increment the month, the date can be no greater than the last day of that month* — which implies incrementing February 28th should yield March 28th. **That test is missing.**

## Worked Example
**The environment controller, and what a testing DSL buys.** The original test of a thermostat prototype (Listing 9-3):

```java
@Test
public void turnOnLoTempAlarmAtThreashold() throws Exception {
    hw.setTemp(WAY_TOO_COLD);
    controller.tic();
    assertTrue(hw.heaterState());
    assertTrue(hw.blowerState());
    assertFalse(hw.coolerState());
    assertFalse(hw.hiTempAlarm());
    assertTrue(hw.loTempAlarm());
}
```

It works, but reading it is tedious and unreliable: the eye reads `heaterState` then glissades left to `assertTrue`, reads `coolerState` then tracks left to `assertFalse`. The state and the sense of the state are in different columns.

```java
// Listing 9-4 — refactored
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
    wayTooCold();
    assertEquals("HBchL", hw.getState());
}
```

The `tic` detail is hidden behind `wayTooCold()`. The odd string is the interesting part: **uppercase means on, lowercase means off, and the letters are always in the order {heater, blower, cooler, hi-temp-alarm, lo-temp-alarm}**. Martin concedes this is "close to a violation of the rule about mental mapping" (Ch 2) — and keeps it, because once you know the encoding your eyes glide across it. The payoff shows when you see the family together:

```java
@Test public void turnOnCoolerAndBlowerIfTooHot() throws Exception {
    tooHot();
    assertEquals("hBChl", hw.getState());
}

@Test public void turnOnHeaterAndBlowerIfTooCold() throws Exception {
    tooCold();
    assertEquals("HBchl", hw.getState());
}

@Test public void turnOnHiTempAlarmAtThreshold() throws Exception {
    wayTooHot();
    assertEquals("hBCHl", hw.getState());
}

@Test public void turnOnLoTempAlarmAtThreshold() throws Exception {
    wayTooCold();
    assertEquals("HBchL", hw.getState());
}
```

And the dual standard shows in the implementation that makes it possible:

```java
public String getState() {
    String state = "";
    state += heater ? "H" : "h";
    state += blower ? "B" : "b";
    state += cooler ? "C" : "c";
    state += hiTempAlarm ? "H" : "h";
    state += loTempAlarm ? "L" : "l";
    return state;
}
```

String concatenation in a loop-shaped body is inefficient; a `StringBuffer` would be faster and uglier. This is an embedded real-time system where memory and CPU are constrained — but this code runs in the *test* environment, which is not constrained at all. Efficiency is negotiable across that line; cleanliness is not.

## Key Takeaways
1. Follow the three laws of TDD and the cycle stays about thirty seconds long, with coverage as a byproduct rather than a project.
2. Keep tests as clean as production code — dirty tests are a liability that eventually gets discarded, taking your ability to change with it.
3. Readability is the whole game in tests; build a domain-specific testing language by refactoring, never by up-front design.
4. Structure every test as BUILD-OPERATE-CHECK (or given-when-then).
5. Minimize asserts, but the real rule is one *concept* per test.
6. Apply the dual standard: tests may trade efficiency, never cleanliness.
7. Make tests FIRST — each letter prevents a specific failure mode.
8. If you let the tests rot, the code rots too.

## Connects To
- **Ch 2 (Meaningful Names)**: "Avoid Mental Mapping" — knowingly bent for the `"HBchL"` state string.
- **Ch 3 (Functions)**: the same smallness and single-purpose rules apply to test functions.
- **Ch 7 (Error Handling)**: writing tests that force exceptions, then building the try scope.
- **Ch 8 (Boundaries)**: learning tests and boundary tests are this discipline aimed at foreign code.
- **Ch 12 (Emergence)**: "Runs all the tests" is the first rule of simple design.
- **Ch 16 (Refactoring SerialDate)**: the `addMonths` test above is from that codebase.
- **Ch 17**: [G5] duplication.
- **[GOF]**: TEMPLATE METHOD. **[RSpec]**: given-when-then.
