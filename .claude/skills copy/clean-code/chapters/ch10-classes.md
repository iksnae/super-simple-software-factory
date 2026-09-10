# Chapter 10: Classes
*(with Jeff Langr)*

## Core Idea
Classes should be small — measured in **responsibilities**, not lines — and a system should be composed of many small classes, each with one reason to change, collaborating to achieve the system's behavior.

## Frameworks Introduced
- **Class Organization** (standard Java convention): public static constants first, then private static variables, then private instance variables. "There is seldom a good reason to have a public variable." Public functions follow; each private utility goes immediately after the public function that calls it — the stepdown rule, so the class reads like a newspaper article.
- **Classes Should Be Small!** — and then smaller. Size is counted in responsibilities.
  - **The naming test**: "If we cannot derive a concise name for a class, then it's likely too large." Weasel words like `Processor`, `Manager`, or `Super` hint at unfortunate aggregation of responsibilities.
  - **The 25-word test**: describe the class in about 25 words without using "if," "and," "or," or "but." The first "and" is the tell.
- **The Single Responsibility Principle (SRP)** [PPP]: a class or module should have **one, and only one, reason to change**. This supplies both the definition of a responsibility and the guideline for class size.
- **Cohesion**: classes should have a small number of instance variables, and each method should manipulate one or more of them. A class where every variable is used by every method is maximally cohesive.
  - Rule of thumb: maximal cohesion is neither advisable nor usually possible, but keep cohesion high — high cohesion means methods and variables are co-dependent and hang together as a logical whole.
  - **The extraction chain**: keeping functions small and parameter lists short → instance variables used by only a subset of methods → cohesion drops → *that subset is a class trying to get out*. "When classes lose cohesion, split them!"
- **The Open-Closed Principle (OCP)** [PPP]: classes should be **open for extension but closed for modification**. Incorporate new features by extending the system, not by modifying existing code.
- **The Dependency Inversion Principle (DIP)** [PPP]: classes should depend upon **abstractions, not concrete details**.

## Key Concepts
- **God class** — `SuperDashboard` with ~70 public methods; nobody defends it. The chapter's real point is the *five*-method version, which is still wrong: "Five methods isn't too much, is it? In this case it is because despite its small number of methods, `SuperDashboard` has too many responsibilities."
- **Encapsulation, non-fanatically** — keep variables and utilities private, but "for us, tests rule." Make something protected or package-scope if a same-package test needs it, after first looking for a way to preserve privacy. Loosening encapsulation is always a last resort.
- **Opening a class introduces risk** — any modification can break other code in it, and the whole class must be retested. This is the practical cost that OCP buys away.
- **Private-method locality as a heuristic** — private behavior that applies to only a small subset of a class (e.g. `selectWithCriteria` in an `Sql` class) points at a potential split. **But the primary spur for taking action should be system change itself**: if `Sql` is logically complete and no `update` support is coming, leave it alone. "As soon as we find ourselves opening up a class, we should consider fixing our design."
- **Isolating from change for testability** — a class depending on concrete details is at the mercy of their volatility. Testing `Portfolio` against a live `TokyoStockExchange` is hopeless: "It's hard to write a test when we get a different answer every five minutes!"

## Mental Models
- **Getting software to work and making software clean are two different activities.** Focusing on the first is wholly appropriate — the failure is thinking you are done when the program works, and moving on instead of breaking overstuffed classes into decoupled units.
- **Answer the "too many small classes" objection with the toolbox.** A system of many small classes has no more moving parts than one with a few large classes; there is exactly as much to learn. "Do you want your tools organized into toolboxes with many small drawers each containing well-defined and well-labeled components? Or do you want a few drawers that you just toss everything into?"
- **The goal of organizing complexity is locality of understanding.** A developer should know where to look, and need only understand the directly affected complexity at any moment. Large multipurpose classes force you to wade through what you don't need to know right now.
- **Testability drives design.** "If a system is decoupled enough to be tested in this way, it will also be more flexible and promote more reuse."
- **Identifying reasons to change surfaces better abstractions.** Pulling version tracking out of `SuperDashboard` yields a `Version` class with high reuse potential in other applications — an abstraction that was invisible until responsibilities were named.

## Code Examples

Cohesion, illustrated (Listing 10-4):

```java
public class Stack {
    private int topOfStack = 0;
    List<Integer> elements = new LinkedList<Integer>();

    public int size() {
        return topOfStack;
    }

    public void push(int element) {
        topOfStack++;
        elements.add(element);
    }

    public int pop() throws PoppedWhenEmpty {
        if (topOfStack == 0)
            throw new PoppedWhenEmpty();
        int element = elements.get(--topOfStack);
        elements.remove(topOfStack);
        return element;
    }
}
```
- **What it demonstrates**: of three methods, only `size()` fails to use both variables. Very cohesive.

SRP extraction from `SuperDashboard` (Listing 10-3):

```java
public class Version {
    public int getMajorVersionNumber()
    public int getMinorVersionNumber()
    public int getBuildNumber()
}
```
- **What it demonstrates**: `SuperDashboard`'s two reasons to change were version tracking (updated on every ship) and Swing component management (it extends `JFrame`). Those change independently, so they are two classes.

DIP and the testable `Portfolio`:

```java
public interface StockExchange {
    Money currentPrice(String symbol);
}

public Portfolio {
    private StockExchange exchange;
    public Portfolio(StockExchange exchange) {
        this.exchange = exchange;
    }
    // ...
}
```
```java
public class PortfolioTest {
    private FixedStockExchangeStub exchange;
    private Portfolio portfolio;

    @Before
    protected void setUp() throws Exception {
        exchange = new FixedStockExchangeStub();
        exchange.fix("MSFT", 100);
        portfolio = new Portfolio(exchange);
    }

    @Test
    public void GivenFiveMSFTTotalShouldBe500() throws Exception {
        portfolio.add(5, "MSFT");
        Assert.assertEquals(500, portfolio.value());
    }
}
```
- **What it demonstrates**: `StockExchange` abstracts "ask for the current price of a symbol," isolating *where* the price comes from. The test stub reduces to a table lookup.

## Reference Tables

The `Sql` refactoring — one open class becomes a set of closed ones:

| Before (Listing 10-9) | After (Listing 10-10) |
|---|---|
| `Sql` with `create()`, `insert()`, `selectAll()`, `findByKey()`, `select(Column,…)`, `select(Criteria)`, `preparedInsert()` plus private helpers | `abstract Sql` with `generate()`; derivatives `CreateSql`, `SelectSql`, `InsertSql`, `SelectWithCriteriaSql`, `SelectWithMatchSql`, `FindByKeySql`, `PreparedInsertSql`; utilities `Where`, `ColumnList` |
| Two reasons to change: new statement types, and changes to an existing statement type → SRP violation | Each class has one reason to change |
| Adding `update` means opening the class and retesting all of it | Adding `update` means adding `UpdateSql`; **no existing class changes** |
| Private helpers like `valuesList` and `selectWithCriteria` serve only some methods | Private helpers move directly to where they're needed; common behavior isolated in `Where` and `ColumnList` |

## Worked Example
**Knuth's `PrintPrimes`, split into three responsibilities.** The starting point (Listing 10-5) is a Java translation of the program as output by Knuth's WEB tool: one `main` function with `M`, `RR`, `CC`, `WW`, `ORDMAX`, `P[]`, `PAGENUMBER`, `PAGEOFFSET`, `ROWOFFSET`, `C`, `J`, `K`, `JPRIME`, `ORD`, `SQUARE`, `N`, and `MULT[]` — deeply indented, tightly coupled, odd variables throughout.

The refactoring produces three classes, each named for what changes it:

```java
// PrimePrinter — owns the execution environment.
// Changes if the method of invocation changes (e.g. converted to a SOAP service).
public class PrimePrinter {
    public static void main(String[] args) {
        final int NUMBER_OF_PRIMES = 1000;
        int[] primes = PrimeGenerator.generate(NUMBER_OF_PRIMES);

        final int ROWS_PER_PAGE = 50;
        final int COLUMNS_PER_PAGE = 4;
        RowColumnPagePrinter tablePrinter =
            new RowColumnPagePrinter(ROWS_PER_PAGE, COLUMNS_PER_PAGE,
                "The First " + NUMBER_OF_PRIMES + " Prime Numbers");
        tablePrinter.print(primes);
    }
}
```

```java
// RowColumnPagePrinter — owns formatting a list of numbers into paginated
// rows and columns. Changes if the output format changes.
public class RowColumnPagePrinter {
    private int rowsPerPage;
    private int columnsPerPage;
    private int numbersPerPage;
    private String pageHeader;
    private PrintStream printStream;

    public void print(int data[]) {
        int pageNumber = 1;
        for (int firstIndexOnPage = 0;
             firstIndexOnPage < data.length;
             firstIndexOnPage += numbersPerPage) {
            int lastIndexOnPage =
                Math.min(firstIndexOnPage + numbersPerPage - 1, data.length - 1);
            printPageHeader(pageHeader, pageNumber);
            printPage(firstIndexOnPage, lastIndexOnPage, data);
            printStream.println("\f");
            pageNumber++;
        }
    }
    // printPage, printRow, printPageHeader, setOutput …
}
```

```java
// PrimeGenerator — owns the algorithm. Changes if the way primes are computed
// changes. Not meant to be instantiated: the class is "just a useful scope in
// which its variables can be declared and kept hidden."
public class PrimeGenerator {
    private static int[] primes;
    private static ArrayList<Integer> multiplesOfPrimeFactors;

    protected static int[] generate(int n) {
        primes = new int[n];
        multiplesOfPrimeFactors = new ArrayList<Integer>();
        set2AsFirstPrime();
        checkOddNumbersForSubsequentPrimes();
        return primes;
    }

    private static boolean isPrime(int candidate) {
        if (isLeastRelevantMultipleOfNextLargerPrimeFactor(candidate)) {
            multiplesOfPrimeFactors.add(candidate);
            return false;
        }
        return isNotMultipleOfAnyPreviousPrimeFactor(candidate);
    }
    // …
}
```

Two observations the chapter insists on. First, **the program got longer** — from just over one page to nearly three — for three reasons: longer descriptive names, function and class declarations used as commentary, and whitespace/formatting for readability. Longer is not worse here.

Second, and more important: **this was not a rewrite.** Both versions use the same algorithm and mechanics. The transformation was made by writing a test suite that verified the precise behavior of the original, then making "a myriad of tiny little changes... one at a time," executing after each to confirm behavior had not changed. One tiny step after another.

## Key Takeaways
1. Measure class size in responsibilities, not lines. If you can't name it concisely, or can't describe it in 25 words without "and," it's too big.
2. SRP is the most-understood and most-abused design principle; the failure is stopping when the code works instead of switching to organization.
3. Many small classes cost nothing in total complexity and buy locality of understanding.
4. Falling cohesion is the signal that a class is hiding inside another; split as soon as a subset of variables serves a subset of methods.
5. Apply OCP so new features arrive as new subclasses and no existing class opens.
6. Let *actual* change, not speculation, trigger the split — a logically complete class needs no rescue.
7. Depend on abstractions (DIP): it isolates from change and is what makes the code testable at all.
8. Restructure under a behavior-verifying test suite in tiny steps. Never rewrite.

## Connects To
- **Ch 3 (Functions)**: extracting small functions is what produces the class-splitting opportunity described here.
- **Ch 4 (Comments)**: `PrimeGenerator` here is the same example refactored in Listing 4-8.
- **Ch 5 (Formatting)**: the alignment example ends in the same finding — a long declaration list means the class should split.
- **Ch 6 (Objects and Data Structures)**: hiding structure behind abstractions is DIP at the data level.
- **Ch 11 (Systems)**: the same principles applied at system scale.
- **Ch 12 (Emergence)**: cohesion and duplication as the rules that drive design.
- **[PPP]**: SRP, OCP, DIP. **[Knuth92]**: *Literate Programming*, source of `PrintPrimes`. **[RDD]**: Wirfs-Brock on responsibilities.
