# Chapter 5: Formatting

## Core Idea
Formatting is about communication, and communication is the professional developer's first order of business — your style and discipline survive long after the code you wrote has been changed beyond recognition.

## Frameworks Introduced
- **The Newspaper Metaphor**: a source file should read like a newspaper article — simple explanatory name as headline, high-level concepts and algorithms at the top, detail increasing as you scroll down, lowest-level functions last.
  - When to use: ordering members within a file.
  - How: a reader should be able to skim the first few functions and get the gist without immersing in details. A newspaper works because it is many small articles, not one long agglomeration of facts.
- **Vertical Openness Between Concepts**: separate each complete thought with a blank line — package declaration, imports, each function.
  - How: a blank line is a visual cue that a new concept begins; the eye is drawn to the first line after one. Unfocus your eyes on the code — groupings should pop out, not muddle.
- **Vertical Density Implies Association**: lines that are tightly related should be vertically dense, with nothing (especially useless comments) inserted between them.
  - How: aim for an "eye-full" — a class you can comprehend without moving your head.
- **Vertical Distance**: closely related concepts should be vertically close [G10], and the distance between them should measure how important each is to understanding the other.
- **Vertical Ordering / dependency direction**: function call dependencies point downward — the callee sits below the caller. (Note this is the *opposite* of Pascal/C/C++ definition-before-use.)
- **Conceptual Affinity**: code wants to be near code it resembles. Affinity can come from direct dependence (calls, shared variables) *or* from a shared naming scheme and a common task — JUnit's `assertTrue`/`assertFalse` family would want to be adjacent even if they didn't call each other.
- **Team Rules** (the pun is deliberate): every programmer has favorite formatting rules, but if he works in a team, then the team rules.
  - How: agree on a single style, encode it into the IDE's formatter, comply. The FitNesse team did this in about ten minutes in 2002 — braces, indent size, naming — and stuck with it. They were not Martin's preferred rules; he followed them anyway.

## Key Concepts
- **File size target** — FitNesse is ~50,000 lines built from files averaging ~65 lines, typically under 200, upper limit ~500. Not a hard rule, but "very desirable." Tomcat and Ant, by contrast, have files thousands of lines long with nearly half over 200.
- **Line width target** — Martin sets his personal limit at **120**. He is fine with 100–120; beyond that "is probably just careless." Measured distribution across seven projects shows every width from 20 to 60 characters accounting for ~1% of lines each (40% of the total), with a sharp drop-off above 80.
- **Horizontal openness** — whitespace to associate and disassociate: spaces around assignment operators (two distinct sides), *no* space between a function name and its opening paren (function and args are conjoined), spaces after commas (arguments are separate).
- **Operator precedence spacing** — `b*b - 4*a*c`: high-precedence factors tight, low-precedence terms spaced. Caveat: most reformatting tools are blind to precedence and will destroy this.
- **Horizontal alignment** — Martin used to align declarations and rvalues in columns; he stopped. It emphasizes the wrong axis (you read down the names without the types, down the rvalues without the operators), and reformatters kill it anyway. More importantly: **if the list is long enough to want alignment, the problem is the length of the list, not the lack of alignment** — the class should be split.
- **Breaking indentation** — collapsing a short `if`, `while`, or function onto one line. Martin has always regretted it and put the indentation back.
- **Dummy scope** — a `while`/`for` with an empty body. Avoid; when unavoidable, put the semicolon on its own indented line and brace it, because an invisible trailing `;` has fooled him repeatedly.

## Mental Models
- **Formatting is too important to ignore and too important to treat religiously.** "Getting it working" is *not* the first order of business — today's functionality will likely change next release; the readability affects every change that will ever be made.
- **Judge the project by the hood.** A reader who sees code that "looks like it was written by a bevy of drunken sailors" concludes that the same inattention pervades everything else.
- **Indentation is the visible hierarchy of scopes.** Programmers scan the left margin to hop over irrelevant scopes and to spot new declarations. Without it, programs are "virtually unreadable by humans" — the chapter demonstrates this with two semantically identical files, one indented and one not.
- **Let code be the coding standard document.** Martin's rules are simply illustrated by `CodeAnalyzer.java` (Listing 5-6) rather than written out as prose.

## Reference Tables

Where declarations go:

| Kind | Placement | Reason |
|---|---|---|
| Local variables | Top of the function | Functions are short, so "top" is close to use |
| Loop control variables | Inside the loop statement | Scope matches lifetime |
| A variable in a long-ish function | Top of its block or just before its loop | Rare; only when the function resists shortening |
| Instance variables | Top of the class, one well-known place | In a well-designed class they're used by most methods; the convention matters more than which end (C++ used the "scissors rule" — bottom) |

Formatting targets:

| Dimension | Target |
|---|---|
| File length | ~200 lines typical, 500 upper bound |
| Line width | ≤120 characters |
| Blank lines | Between every complete thought |
| Indent | One level per scope, never collapsed |
| Dependency direction | Caller above callee |

## Code Examples

Vertical openness — the same file with and without blank lines (Listings 5-1 / 5-2):

```java
package fitnesse.wikitext.widgets;

import java.util.regex.*;

public class BoldWidget extends ParentWidget {
    public static final String REGEXP = "'''.+?'''";
    private static final Pattern pattern = Pattern.compile("'''(.+?)'''",
        Pattern.MULTILINE + Pattern.DOTALL);

    public BoldWidget(ParentWidget parent, String text) throws Exception {
        super(parent);
        Matcher match = pattern.matcher(text);
        match.find();
        addChildWidgets(match.group(1));
    }

    public String render() throws Exception {
        StringBuffer html = new StringBuffer("<b>");
        html.append(childHtml()).append("</b>");
        return html.toString();
    }
}
```
- **What it demonstrates**: remove those blank lines and the module becomes a muddle. The difference is nothing but vertical openness.

Vertical density — comments that break the association of two related fields (5-3 → 5-4):

```java
// before: the fields no longer read as a pair
public class ReporterConfig {
    /**
     * The class name of the reporter listener
     */
    private String m_className;

    /**
     * The properties of the reporter listener
     */
    private List<Property> m_properties = new ArrayList<Property>();

    public void addProperty(Property property) { m_properties.add(property); }
```
```java
// after: one eye-full
public class ReporterConfig {
    private String m_className;
    private List<Property> m_properties = new ArrayList<Property>();

    public void addProperty(Property property) { m_properties.add(property); }
```

Horizontal openness and precedence:

```java
private void measureLine(String line) {
    lineCount++;
    int lineSize = line.length();
    totalChars += lineSize;
    lineWidthHistogram.addLine(lineSize, lineCount);
    recordWidestLine(lineSize);
}
```
```java
public static double root1(double a, double b, double c) {
    double determinant = determinant(a, b, c);
    return (-b + Math.sqrt(determinant)) / (2*a);
}

private static double determinant(double a, double b, double c) {
    return b*b - 4*a*c;
}
```
- **What it demonstrates**: spaces around `=` split the two sides of an assignment; no space before `(` keeps a call conjoined; tight factors and spaced terms make the equation read at a glance.

## Worked Example
**The alignment habit, and what it was hiding.** Martin came from assembly, where horizontal alignment accentuated structure, and carried the habit into C, C++, and Java:

```java
public class FitNesseExpediter implements ResponseSender {
    private   Socket          socket;
    private   InputStream     input;
    private   OutputStream    output;
    private   Request         request;
    private   Response        response;
    private   FitNesseContext context;
    protected long            requestParsingTimeLimit;
    private   long            requestProgress;
    private   long            requestParsingDeadline;
    private   boolean         hasError;

    public FitNesseExpediter(Socket          s,
                             FitNesseContext context) throws Exception {
        this.context =            context;
        socket =                  s;
        input =                   s.getInputStream();
        output =                  s.getOutputStream();
        requestParsingTimeLimit = 10000;
    }
```

He abandoned it for two reasons and one lesson. The reasons: the alignment leads the eye down the names without the types and down the rvalues without the assignment operators, emphasizing the wrong thing; and automatic reformatters destroy it anyway. The lesson is the valuable part — the unaligned version *points out a deficiency the aligned version concealed*:

```java
public class FitNesseExpediter implements ResponseSender {
    private Socket socket;
    private InputStream input;
    private OutputStream output;
    private Request request;
    private Response response;
    private FitNesseContext context;
    protected long requestParsingTimeLimit;
    private long requestProgress;
    private long requestParsingDeadline;
    private boolean hasError;
```

Ten instance variables in one class. "If I have long lists that need to be aligned, the problem is the length of the lists, not the lack of alignment." The list length says `FitNesseExpediter` should be split up — a formatting observation that turns out to be a design finding.

**The stepdown made concrete (Listing 5-5, `WikiPageResponder`).** `makeResponse` calls `getPageNameOrDefault`, `loadPage`, `notFoundResponse`, and `makePageResponse` — each defined below it, in the order called. The reader can trust that a definition follows shortly after its use. Note the aside on constants [G35]: `"FrontPage"` is passed *down* from `makeResponse`, the level that has business knowing the default, rather than buried inside the low-level `getPageNameOrDefault`.

## Key Takeaways
1. Formatting is communication, and communication outlives the code. Set rules, automate them, apply them consistently.
2. In a team, the team's style wins over your preferences — always.
3. Read the file top-down like a newspaper: name, then concepts, then detail.
4. Blank lines separate thoughts; density binds related lines. Both are load-carrying, not decoration.
5. Keep callers above callees so the reader flows downward and never hunts.
6. Declare locals at first use, loop counters in the loop, instance variables at the top of the class.
7. Aim for files ~200 lines (500 max) and lines ≤120 characters.
8. Don't align columns — a list long enough to need alignment is a class that needs splitting.
9. Never collapse a scope onto one line, and never leave a dummy body's semicolon invisible.

## Connects To
- **Ch 3 (Functions)**: the Stepdown Rule is the vertical-ordering rule applied to abstraction levels; Listing 3-7 is cited here as a model layout.
- **Ch 10 (Classes)**: file size is class size; the alignment example lands on a class that should be split (SRP).
- **Ch 15 (JUnit Internals)**: Listing 15-5 cited as a further example of good vertical ordering.
- **Ch 17**: [G10] vertical separation, [G34] functions should descend only one level of abstraction, [G35] keep configurable data at high levels.
