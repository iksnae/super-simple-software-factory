# Chapter 14: Successive Refinement
*Case Study of a Command-Line Argument Parser*

## Core Idea
"To write clean code, you must first write dirty code and then clean it" — this chapter shows a module that started well, did not scale, and was refactored through many tiny behavior-preserving steps rather than a rewrite.

## Frameworks Introduced
- **Successive Refinement**: the rough-draft discipline from grade-school composition, applied to code. Write a first draft, then a second, then subsequent drafts until the final version.
  - When to use: always. "I am not expecting you to be able to write clean and elegant programs in one pass."
  - Why: "programming is a craft more than it is a science."
- **Stop when the mess starts costing more than the feature**: Martin had two more argument types to add and could see they would make things much worse. "If I bulldozed my way forward, I could probably get them to work, but I'd leave behind a mess that was too large to fix. If the structure of this code was ever going to be maintainable, now was the time to fix it."
  - The diagnostic that produced the design: each new argument type required new code in **three major places** — parse the schema element to select the right `HashMap`, parse and convert the command-line string to its true type, and a `getXXX` method to return it. "Many different types, all with similar methods — that sounds like a class to me. And so the `ArgumentMarshaler` concept was born."
- **On Incrementalism**: "One of the best ways to ruin a program is to make massive changes to its structure in the name of improvement. Some programs never recover from such 'improvements.'"
  - How: use TDD's central doctrine — **keep the system running at all times**. Every change must keep the system working as it worked before. This requires an automated test suite runnable on a whim. For `Args`, Martin had JUnit unit tests plus FitNesse wiki-page acceptance tests, written *while building the festering pile*.
  - Then: "a large number of very tiny changes," each moving structure toward `ArgumentMarshaler`, each keeping the system working.

## Key Concepts
- **The professional-suicide failure mode** — freshman programmers believe the primary goal is getting the program working, then move on, "leaving the 'working' program in whatever state they finally got it to 'work.'"
- **Good design is partitioning** — "creating appropriate places to put different kinds of code. This separation of concerns makes the code much simpler to understand and maintain." The majority of the final changes to `Args` were **deletions**: code moved out to `ArgsException` and to per-type marshaler files.
- **Extensibility as the visible result** — adding a date or complex-number argument to the finished design takes a new `ArgumentMarshaler` derivative, a new `getXXX`, a new case in `parseSchemaElement`, and probably a new `ErrorCode` and message. Trivial effort.
- **A knowingly-accepted compromise** — putting error-message formatting in `Args` violated SRP (`Args` should be about processing arguments, not message format). Moving it to `ArgsException` is "frankly, a compromise": users who dislike the canned messages must write their own, but the convenience of prepared messages "is not insignificant." Clean code allows for reasoned trade-offs, stated as such.
- Footnote worth keeping: Martin later rewrote the module in Ruby — "1/7th the size and had a subtly better structure."

## Mental Models
- **Cleanup cost is a function of elapsed time.** "If you made a mess in a module in the morning, it is easy to clean it up in the afternoon. Better yet, if you made a mess five minutes ago, it's very easy to clean it up right now." As code rots, modules insinuate themselves into each other, creating hidden tangled dependencies; finding and breaking those is long and arduous.
- **Bad code is the one project problem that doesn't recover on its own.** "Bad schedules can be redone, bad requirements can be redefined. Bad team dynamics can be repaired. But bad code rots and ferments, becoming an inexorable weight that drags the team down."
- **Working code is not the bar.** "It is not enough for code to work. Code that works is often badly broken. Programmers who satisfy themselves with merely working code are behaving unprofessionally."
- **When a test breaks during refactoring, fix it before making another change.** Incrementalism means never carrying a red bar into the next step.
- **A failing test that fails the *same way* after a change is evidence you introduced nothing new.** Martin uses this deliberately when removing `falseIfNull`.

## Code Examples

The finished interface — the target the refactoring reaches (Listing 14-1):

```java
public static void main(String[] args) {
    try {
        Args arg = new Args("l,p#,d*", args);
        boolean logging = arg.getBoolean('l');
        int port = arg.getInt('p');
        String directory = arg.getString('d');
        executeApplication(logging, port, directory);
    } catch (ArgsException e) {
        System.out.printf("Argument error: %s\n", e.errorMessage());
    }
}
```
- **What it demonstrates**: the schema string `"l,p#,d*"` declares a boolean `-l`, an integer `-p`, and a string `-d`. Construction either succeeds and is ready to query, or throws with a retrievable description.

The rough draft's field list, which is the whole diagnosis (Listing 14-8):

```java
public class Args {
    private String schema;
    private String[] args;
    private boolean valid = true;
    private Set<Character> unexpectedArguments = new TreeSet<Character>();
    private Map<Character, Boolean> booleanArgs = new HashMap<Character, Boolean>();
    private Map<Character, String> stringArgs = new HashMap<Character, String>();
    private Map<Character, Integer> intArgs = new HashMap<Character, Integer>();
    private Set<Character> argsFound = new HashSet<Character>();
    private int currentArgument;
    private char errorArgumentId = '\0';
    private String errorParameter = "TILT";
    private ErrorCode errorCode = ErrorCode.OK;
```
- **What it demonstrates**: one `HashMap` per type, plus error state, plus parse state, all in one class. It "works. And it's messy." Every new type adds another map and another three touch points.

The end state (Listing 14-16), same class after the marshaler concept lands:

```java
public class Args {
    private String schema;
    private Map<Character, ArgumentMarshaler> marshalers =
        new HashMap<Character, ArgumentMarshaler>();
    private Set<Character> argsFound = new HashSet<Character>();
    private Iterator<String> currentArgument;
    private List<String> argsList;

    private void parseSchemaElement(String element) throws ArgsException {
        char elementId = element.charAt(0);
        String elementTail = element.substring(1);
        validateSchemaElementId(elementId);
        if (elementTail.length() == 0)
            marshalers.put(elementId, new BooleanArgumentMarshaler());
        else if (elementTail.equals("*"))
            marshalers.put(elementId, new StringArgumentMarshaler());
        else if (elementTail.equals("#"))
            marshalers.put(elementId, new IntegerArgumentMarshaler());
        else if (elementTail.equals("##"))
            marshalers.put(elementId, new DoubleArgumentMarshaler());
        else
            throw new ArgsException(
                ArgsException.ErrorCode.INVALID_FORMAT, elementId, elementTail);
    }

    private boolean setArgument(char argChar) throws ArgsException {
        ArgumentMarshaler m = marshalers.get(argChar);
        if (m == null) return false;
        try {
            m.set(currentArgument);
            return true;
        } catch (ArgsException e) {
            e.setErrorArgumentId(argChar);
            throw e;
        }
    }
}
```
- **What it demonstrates**: three type-specific maps collapsed into one `Map<Character, ArgumentMarshaler>`; type knowledge moved into polymorphic derivatives; error state moved out entirely.

## Worked Example
**The first four steps, in the order Martin actually took them.** This is the chapter's most transferable content — not the destination, but the step size.

**Step 1 — add the skeleton where it cannot break anything.** Append the new concept to the end of the festering pile (Listing 14-11):

```java
private class ArgumentMarshaler {
    private boolean booleanValue = false;
    public void setBoolean(boolean value) { booleanValue = value; }
    public boolean getBoolean() { return booleanValue; }
}

private class BooleanArgumentMarshaler extends ArgumentMarshaler { }
private class StringArgumentMarshaler extends ArgumentMarshaler { }
private class IntegerArgumentMarshaler extends ArgumentMarshaler { }
```

"Clearly, this wasn't going to break anything."

**Step 2 — the smallest modification that could break the least.** Change only the boolean map's value type:

```java
private Map<Character, ArgumentMarshaler> booleanArgs =
    new HashMap<Character, ArgumentMarshaler>();
```

and fix the statements that broke — precisely the three places predicted: parse, set, get.

```java
private void parseBooleanSchemaElement(char elementId) {
    booleanArgs.put(elementId, new BooleanArgumentMarshaler());
}

private void setBooleanArg(char argChar, boolean value) {
    booleanArgs.get(argChar).setBoolean(value);
}

public boolean getBoolean(char arg) {
    return falseIfNull(booleanArgs.get(arg).getBoolean());
}
```

**Step 3 — tests fail; fix that before anything else.** Calling `getBoolean('y')` when no `y` argument exists makes `booleanArgs.get('y')` return null and throws `NullPointerException`. `falseIfNull` had guarded this, but the change made it irrelevant — it is now the *marshaler* that can be null, not the boolean. "Incrementalism demanded that I get this working quickly before making any other changes."

Remove the useless call and the now-dead function:

```java
public boolean getBoolean(char arg) {
    return booleanArgs.get(arg).getBoolean();
}
```

The tests still fail *in the same way* — confirmation that no new error was introduced. Split into two lines, naming the marshaler `am` (short, because the scope is tiny [N5]):

```java
public boolean getBoolean(char arg) {
    Args.ArgumentMarshaler am = booleanArgs.get(arg);
    return am.getBoolean();
}
```

Then put the null check where it now belongs:

```java
public boolean getBoolean(char arg) {
    Args.ArgumentMarshaler am = booleanArgs.get(arg);
    return am != null && am.getBoolean();
}
```

**Step 4 — repeat for the next type.** String arguments follow the identical shape: change the map, then get parse/set/get working.

```java
private Map<Character, ArgumentMarshaler> stringArgs =
    new HashMap<Character, ArgumentMarshaler>();

private void parseStringSchemaElement(char elementId) {
    stringArgs.put(elementId, new StringArgumentMarshaler());
}

public String getString(char arg) {
    Args.ArgumentMarshaler am = stringArgs.get(arg);
    return am == null ? "" : am.getString();
}
```

Note what Martin flags himself: at this stage all the marshalling implementation still sits in the `ArgumentMarshaler` **base class** rather than being distributed to the derivatives. That is deliberate — pushing behavior down into the subclasses is a later step. The intermediate state is allowed to be imperfect as long as it is working.

## Key Takeaways
1. Write it dirty, then clean it. Nobody produces the final structure in one pass.
2. Stop adding features the moment you can see the next ones will make the mess unfixable — that is the cheapest moment to restructure.
3. Notice when "many different types, all with similar methods" appear across several touch points; that is a class waiting to be born.
4. Never restructure without a test suite that verifies unchanged behavior; TDD's requirement to keep the system running at all times is what makes large restructuring safe.
5. Move in very tiny steps, fixing each break before taking the next one.
6. Most of a good refactoring is deletion and relocation — partitioning code into appropriate places.
7. Trade-offs are legitimate when reasoned and stated (error messages in `ArgsException`).
8. Cleanup cost grows with elapsed time; clean continuously and never let the rot start.

## Connects To
- **Ch 3 (Functions)**: "How Do You Write Functions Like This?" — the same write-then-massage process at function scale.
- **Ch 9 (Unit Tests)**: the suite that made this refactoring possible; FitNesse acceptance tests alongside JUnit.
- **Ch 10 (Classes)**: SRP, and the `PrintPrimes` refactoring done by the identical tiny-step method.
- **Ch 7 (Error Handling)**: `ArgsException` and error codes vs. exceptions.
- **Ch 16 (Refactoring SerialDate)**: the same discipline applied to someone else's code.
- **Ch 17**: [N5] use long names for long scopes — and therefore short ones for short scopes, as with `am`.
