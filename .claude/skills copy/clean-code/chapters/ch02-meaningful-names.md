# Chapter 2: Meaningful Names
*(by Tim Ottinger)*

## Core Idea
A name must answer why the thing exists, what it does, and how it is used — if a name needs a comment to explain it, the name has failed.

## Frameworks Introduced
- **Use Intention-Revealing Names**: the name states the measured quantity *and* its unit, or the concept *and* its role.
  - When to use: every declaration.
  - How: if you are about to write a trailing comment explaining a name, put that explanation into the name instead. `int d; // elapsed time in days` → `int elapsedTimeInDays`.
- **Avoid Disinformation**: never leave false clues.
  - When to use: naming containers, abbreviations, and near-identical siblings.
  - How: don't call it `accountList` unless it is a `List`; avoid platform names (`hp`, `aix`, `sco`) as abbreviations; never use lowercase `l` or uppercase `O`; make names that differ *differ obviously* — `XYZControllerForEfficientHandlingOfStrings` vs `XYZControllerForEfficientStorageOfStrings` is a defect waiting to happen.
- **Make Meaningful Distinctions**: if names must differ, they must *mean* something different.
  - When to use: any time the compiler forces you to rename.
  - How: reject number series (`a1, a2, …aN`) and noise words (`Info`, `Data`, `Object`, `variable`, `table`). `getActiveAccount()` / `getActiveAccounts()` / `getActiveAccountInfo()` is unusable — nobody can tell which to call.
- **Use Pronounceable Names**: programming is a social activity; you must be able to say the name aloud in a design discussion.
- **Use Searchable Names**: name length should correspond to scope size. Single-letter names ONLY as locals inside short methods.
  - How: `MAX_CLASSES_PER_STUDENT` is greppable; `7` is not. `e` is the worst possible searchable name.
- **Avoid Encodings**: no Hungarian Notation, no `m_` member prefixes, no `I` interface prefix.
  - How: modern type systems and IDEs already carry the information. If you must encode one side, encode the *implementation* (`ShapeFactoryImp`), never the interface.
- **Pick One Word per Concept**: one verb per abstract concept across the whole codebase.
  - How: choose `get` *or* `fetch` *or* `retrieve` and stop. Don't run `DeviceManager` alongside `ProtocolController` unless the difference is real.
- **Don't Pun**: never reuse one word for two semantics. If `add` means "combine two values" elsewhere, a method that puts one item into a collection is `insert` or `append`.
- **Add Meaningful Context**: enclose names in well-named classes, functions, or namespaces; prefix only as a last resort.
  - How: `state` alone is ambiguous; `addrState` is better; an `Address` class is best, because then the compiler knows too.
- **Don't Add Gratuitous Context**: no `GSD` prefix on every class in "Gas Station Deluxe." Shorter is better so long as it stays clear.

## Key Concepts
- **Implicity** — the degree to which context is *not* explicit in the code itself; the real reason simple-looking code is unreadable.
- **Noise word** — a word added to differentiate that carries no meaning: `Info`, `Data`, `a`, `an`, `the`, `Object`, `String`.
- **Mental mapping** — forcing the reader to translate your name into the concept they already hold; the professional's rule is that **clarity is king**.
- **Solution domain name** — CS, algorithm, pattern, or math terminology (`AccountVisitor`, `JobQueue`); use it, because your readers are programmers.
- **Problem domain name** — used when there is no "programmer-eese"; lets a maintainer ask a domain expert.
- **Class name** — noun or noun phrase (`Customer`, `WikiPage`, `AddressParser`), never a verb, never `Manager`/`Processor`/`Data`/`Info`.
- **Method name** — verb or verb phrase (`postPayment`, `deletePage`, `save`); accessors/mutators/predicates prefixed `get`/`set`/`is`.

## Mental Models
- **Use the "does it need a comment?" test as a naming lint.** A name requiring a comment is a name that failed.
- **Think of name length as a function of scope.** Tiny scope tolerates `i`; wide scope demands a searchable, spellable, pronounceable name.
- **Treat renaming as cheap and expected.** Modern tooling makes it near-free; fear of objection is not a reason to keep a bad name. Expect to rename several times before settling.
- **When overloading constructors, prefer static factory methods named for their arguments** — and make the constructors private to enforce it.

## Code Examples

The chapter's central refactoring — same operators, same nesting, radically different clarity:

```java
// implicit: what is theList? what is subscript 0? what is 4?
public List<int[]> getThem() {
    List<int[]> list1 = new ArrayList<int[]>();
    for (int[] x : theList)
        if (x[0] == 4)
            list1.add(x);
    return list1;
}
```

```java
// step 1: name the concepts
public List<int[]> getFlaggedCells() {
    List<int[]> flaggedCells = new ArrayList<int[]>();
    for (int[] cell : gameBoard)
        if (cell[STATUS_VALUE] == FLAGGED)
            flaggedCells.add(cell);
    return flaggedCells;
}
```

```java
// step 2: wrap the magic number in an intention-revealing type
public List<Cell> getFlaggedCells() {
    List<Cell> flaggedCells = new ArrayList<Cell>();
    for (Cell cell : gameBoard)
        if (cell.isFlagged())
            flaggedCells.add(cell);
    return flaggedCells;
}
```
- **What it demonstrates**: complexity did not change — operator count, constant count, and nesting depth are identical. Only the explicitness changed.

Searchable names, and why the longer function is the better one:

```java
for (int j=0; j<34; j++) {
    s += (t[j]*4)/5;
}
```
```java
int realDaysPerIdealDay = 4;
const int WORK_DAYS_PER_WEEK = 5;
int sum = 0;
for (int j=0; j < NUMBER_OF_TASKS; j++) {
    int realTaskDays = taskEstimate[j] * realDaysPerIdealDay;
    int realTaskWeeks = (realdays / WORK_DAYS_PER_WEEK);
    sum += realTaskWeeks;
}
```
- **What it demonstrates**: `sum` is a weak name but a searchable one. Finding `WORK_DAYS_PER_WEEK` is trivial; finding every meaningful `5` is not.

## Worked Example
**Listing 2-1 → 2-2: context by extraction.** The variables `number`, `verb`, and `pluralModifier` belong to a "guess statistics" message, but nothing in the code says so — the reader must infer it from the algorithm.

```java
// Listing 2-1: variables with unclear context
private void printGuessStatistics(char candidate, int count) {
    String number;
    String verb;
    String pluralModifier;
    if (count == 0) {
        number = "no";  verb = "are"; pluralModifier = "s";
    } else if (count == 1) {
        number = "1";   verb = "is";  pluralModifier = "";
    } else {
        number = Integer.toString(count); verb = "are"; pluralModifier = "s";
    }
    String guessMessage = String.format(
        "There %s %s %s%s", verb, number, candidate, pluralModifier);
    print(guessMessage);
}
```

Making the three variables fields of a `GuessStatisticsMessage` class gives them a definitive context — and *because* they now have a home, the algorithm can be split into small, named functions:

```java
// Listing 2-2: variables have a context
public class GuessStatisticsMessage {
    private String number;
    private String verb;
    private String pluralModifier;

    public String make(char candidate, int count) {
        createPluralDependentMessageParts(count);
        return String.format(
            "There %s %s %s%s", verb, number, candidate, pluralModifier);
    }

    private void createPluralDependentMessageParts(int count) {
        if (count == 0)      { thereAreNoLetters(); }
        else if (count == 1) { thereIsOneLetter(); }
        else                 { thereAreManyLetters(count); }
    }

    private void thereAreManyLetters(int count) {
        number = Integer.toString(count); verb = "are"; pluralModifier = "s";
    }
    private void thereIsOneLetter() {
        number = "1"; verb = "is"; pluralModifier = "";
    }
    private void thereAreNoLetters() {
        number = "no"; verb = "are"; pluralModifier = "s";
    }
}
```

The order matters: adding context *enabled* the decomposition, rather than following it.

## Key Takeaways
1. If a name requires a comment, the name is wrong — fix the name, delete the comment.
2. Names that differ must mean something different; noise words and number series are non-information.
3. Name length should track scope size: single letters only in tiny scopes, searchable names everywhere else.
4. Drop encodings — Hungarian notation, `m_` prefixes, and `IShapeFactory` are all obsolete impediments.
5. One word per concept, and never the same word for two concepts.
6. Prefer giving a group of related variables a class over prefixing them; the compiler then enforces the context.
7. Renaming is cheap. Do it as soon as you find a better name, and don't let fear of others' objections stop you.

## Connects To
- **Ch 3 (Functions)**: extracting small named functions is the main mechanism that makes good naming possible.
- **Ch 4 (Comments)**: most comments exist to compensate for a name that should have carried the meaning.
- **Ch 10 (Classes)**: a class that is hard to name precisely is doing too much (SRP).
- **Ch 17 (Smells and Heuristics)**: the N-series heuristics (N1–N7), including N5 "use long names for long scopes."
