# Chapter 8: Boundaries
*(by James Grenning)*

## Core Idea
There is a natural tension between an interface's provider, who wants broad applicability, and its user, who wants a focused fit — manage it by keeping third-party interfaces in a few controlled places, because "it's better to depend on something you control than on something you don't control, lest it end up controlling you."

## Frameworks Introduced
- **Don't pass boundary interfaces around your system**: keep `Map` (or any boundary type) inside the class or close family of classes that uses it. Avoid returning it from, or accepting it as an argument to, public APIs.
  - When to use: any time a third-party type starts appearing in your own signatures.
  - How: wrap it in a class that exposes only the operations your application needs. The wrapper can then enforce design and business rules.
  - Why it matters concretely: `Map`'s interface changed when generics arrived in Java 5, and Grenning has seen systems "inhibited from using generics because of the sheer magnitude of changes needed to make up for the liberal use of `Map`s."
- **Learning Tests** (Jim Newkirk's term, via Beck's *TDD*): tests written against a third-party API to explore your understanding of it, rather than experimenting inside production code.
  - When to use: adopting any unfamiliar library.
  - How: call the API exactly as you intend to use it in the application. Run controlled experiments focused on what *you* want out of the API, not on testing their code.
- **Learning Tests Are Better Than Free**: you had to learn the API anyway, so the tests cost nothing — and they keep paying.
  - How: re-run them on every new release of the package. If the third party changes in a way incompatible with your expectations, you find out immediately rather than in production. Without such boundary tests, teams stay on old versions longer than they should because migration feels risky.
- **Write the interface you wish you had**: when the code on the other side of a boundary does not exist yet, define your own interface and keep working.
  - How: name the operation in your own domain terms, implement an ADAPTER once the real API lands, and use a fake for testing in the meantime.

## Key Concepts
- **Boundary** — any seam between code you control and code you don't: third-party packages, open source, other teams' subsystems, and the boundary between the known and the not-yet-known.
- **Broad interface as liability** — `java.util.Map` exposes `clear()` to every recipient, and cannot reliably constrain the types stored in it. Any determined user can defeat your intended conventions.
- **ADAPTER** [GOF] — encapsulates interaction with a foreign API and provides *a single place to change* when that API evolves.
- **Seam** [WELC] — the point where you can substitute a `FakeTransmitter` to test the code that depends on an undefined API.
- **Outbound boundary tests** — even when you don't need the learning, a clean boundary should have tests exercising the interface the same way production code does.

## Mental Models
- **Generics improve readability but do not solve the boundary problem.** `Map<Sensor>` removes casts, yet still hands every client more capability than you want and still spreads the dependency. The wrapper does both jobs.
- **Whether to use generics inside a wrapper is an implementation detail — and always should have been.** No user of `Sensors` cares.
- **Learning and integrating are each hard; doing both at once is doubly hard.** Learning tests split them, so you never debug your code and their code simultaneously.
- **Not every use of a boundary type needs encapsulation** — the rule is about *passing* them around, not about touching them at all.

## Code Examples

The `Map` boundary, three stages:

```java
// raw: every client casts, and the story is untold
Map sensors = new HashMap();
...
Sensor s = (Sensor)sensors.get(sensorId);
```
```java
// generics: better readability, same exposure and same dependency spread
Map<Sensor> sensors = new HashMap<Sensor>();
...
Sensor s = sensors.get(sensorId);
```
```java
// wrapped: the boundary interface is hidden and can evolve
public class Sensors {
    private Map sensors = new HashMap();

    public Sensor getById(String id) {
        return (Sensor) sensors.get(id);
    }
    //snip
}
```
- **What it demonstrates**: casting and type management move inside `Sensors`; the interface is tailored and constrained, "easier to understand and harder to misuse," and `Sensors` can enforce design and business rules that `Map` cannot.

## Worked Example
**Learning log4j by test.** The team wants Apache log4j instead of a hand-rolled logger. They download it, skim the intro page, and write the smallest test that should print "hello" to the console:

```java
@Test
public void testLogCreate() {
    Logger logger = Logger.getLogger("MyLogger");
    logger.info("hello");
}
```

It errors: log4j wants an `Appender`. More reading turns up `ConsoleAppender`:

```java
@Test
public void testLogAddAppender() {
    Logger logger = Logger.getLogger("MyLogger");
    ConsoleAppender appender = new ConsoleAppender();
    logger.addAppender(appender);
    logger.info("hello");
}
```

Now the appender has no output stream — odd, since a *console* appender might be expected to have one. Some googling later:

```java
@Test
public void testLogAddAppender() {
    Logger logger = Logger.getLogger("MyLogger");
    logger.removeAllAppenders();
    logger.addAppender(new ConsoleAppender(
        new PatternLayout("%p %t %m%n"),
        ConsoleAppender.SYSTEM_OUT));
    logger.info("hello");
}
```

That works. Then the probing continues, and this is where learning tests earn their keep: removing `ConsoleAppender.SystemOut` still prints, but removing `PatternLayout` brings back the missing-stream complaint. Closer reading of the docs explains it — the default `ConsoleAppender` constructor is "unconfigured," which is neither obvious nor useful, and reads like a bug or at least an inconsistency in log4j. That is a fact about a dependency the team now owns, captured executably rather than in someone's memory:

```java
public class LogTest {
    private Logger logger;

    @Before
    public void initialize() {
        logger = Logger.getLogger("logger");
        logger.removeAllAppenders();
        Logger.getRootLogger().removeAllAppenders();
    }

    @Test
    public void basicLogger() {
        BasicConfigurator.configure();
        logger.info("basicLogger");
    }

    @Test
    public void addAppenderWithStream() {
        logger.addAppender(new ConsoleAppender(
            new PatternLayout("%p %t %m%n"),
            ConsoleAppender.SYSTEM_OUT));
        logger.info("addAppenderWithStream");
    }

    @Test
    public void addAppenderWithoutStream() {
        logger.addAppender(new ConsoleAppender(
            new PatternLayout("%p %t %m%n")));
        logger.info("addAppenderWithoutStream");
    }
}
```

With that knowledge encoded, the team wraps it in their own logger class and the rest of the application never touches the log4j boundary.

**The Transmitter that didn't exist yet.** On a radio communications system, the "Transmitter" subsystem was owned by another group who had not defined their interface. Rather than block, the team worked away from the unknown and let their own work tell them what they wanted the boundary to say:

> Key the transmitter on the provided frequency and emit an analog representation of the data coming from this stream.

So they defined `Transmitter` themselves, with a `transmit` method taking a frequency and a data stream — the interface they wished they had, under their control, keeping `CommunicationsController` readable and focused. When the real API arrived they wrote a `TransmitterAdapter` to bridge it, giving one place to change as the API evolved. The same seam let them test `CommunicationsController` against a `FakeTransmitter` immediately, and add boundary tests against the real `TransmitterAPI` once it existed.

## Key Takeaways
1. Keep third-party interfaces out of your signatures; wrap them and expose only what your application needs.
2. A wrapper is not just insulation — it's where you enforce the constraints the foreign interface can't.
3. Write learning tests to understand a new library; they cost nothing because the learning was mandatory anyway.
4. Re-run learning tests on every upgrade — they turn a risky migration into an immediate signal.
5. When the other side of a boundary doesn't exist, define the interface you wish you had and adapt to reality later.
6. ADAPTER gives you one place to absorb an API's evolution; the same seam gives you your test double.
7. Minimize the number of places in your code that name a third-party particular.

## Connects To
- **Ch 7 (Error Handling)**: "wrapping third-party APIs is a best practice" — the `LocalPort`/`ACMEPort` wrapper is this chapter's technique applied to exceptions.
- **Ch 9 (Unit Tests)**: learning tests and boundary tests are ordinary tests aimed at foreign code.
- **Ch 11 (Systems)**: boundaries between application and infrastructure at system scale.
- **Ch 17**: [G36] avoid transitive navigation; boundary hygiene.
- **GOF**: ADAPTER. **[WELC]** Feathers, *Working Effectively with Legacy Code*: seams. **[BeckTDD]**: learning tests, pp. 136–137.
