# Chapter 12: Emergence
*(by Jeff Langr)*

## Core Idea
Kent Beck's four rules of Simple Design — in priority order: runs all the tests, contains no duplication, expresses the intent of the programmer, minimizes the number of classes and methods — let good design *emerge* from ordinary work rather than being decreed up front.

## Frameworks Introduced
- **The Four Rules of Simple Design** (Kent Beck), given in order of importance:
  1. **Runs all the tests**
  2. **Contains no duplication**
  3. **Expresses the intent of the programmer**
  4. **Minimizes the number of classes and methods**
  - When to use: continuously, during the refactoring step of every red-green-refactor cycle.
  - How: rule 1 is achieved by writing and running tests; rules 2–4 are achieved by refactoring under the safety those tests provide.
- **Rule 1 — Runs All the Tests**: "A system that cannot be verified should never be deployed."
  - Why it drives design, not just correctness: making a system testable pushes classes toward small and single-purpose (SRP is simply easier to test), and tight coupling makes tests hard to write — so the more tests you write, the more you reach for DIP, dependency injection, interfaces, and abstraction. **"Writing tests leads to better designs."** A simple, obvious rule about having tests turns out to drive the primary OO goals of low coupling and high cohesion.
- **Rules 2–4 — Refactoring**: for each few lines of code added, pause and reflect on the design. Did we just degrade it? Clean it up, run the tests to prove nothing broke. "The fact that we have these tests eliminates the fear that cleaning up the code will break it!"
- **Reuse in the small**: extracting commonality at a tiny level exposes SRP violations; the extracted method moves to another class, which elevates its visibility, which lets someone else abstract it further and reuse it elsewhere. "This 'reuse in the small' can cause system complexity to shrink dramatically. Understanding how to achieve reuse in the small is essential to achieving reuse in the large."
- **TEMPLATE METHOD** [GOF]: the standard technique for removing *higher-level* duplication — where two algorithms are the same except for one step.

## Key Concepts
- **Duplication is the primary enemy of a well-designed system** — additional work, additional risk, additional unnecessary complexity.
- **Forms of duplication** — identical lines; *similar* lines that can be massaged to look more alike so they can be refactored; and **duplication of implementation**, where two methods maintain separate state for facts that imply each other.
- **Expressiveness** — the majority of a software project's cost is long-term maintenance, and understanding is what limits safe change. Four levers: good names, small functions and classes, standard nomenclature (design pattern names like COMMAND or VISITOR communicate a design succinctly), and well-written unit tests as **documentation by example**.
- **"But the most important way to be expressive is to try."** The common failure is getting code working and moving on without thought for the next reader — "the most likely next person to read the code will be you."
- **Care is a precious resource.** Spend a little time with each function and class; take pride in the workmanship.
- **Rule 4's failure mode is dogmatism** — an interface for every class, or a rule that fields and behavior must always split into data classes and behavior classes. Resist the dogma; be pragmatic.
- **Rule 4 is the lowest priority.** Keeping class and function counts low matters, but having tests, eliminating duplication, and expressing yourself matter more.

## Mental Models
- **Simple design is a crystallized substitute for experience — not a replacement for it.** These practices "can and does encourage and enable developers to adhere to good principles and patterns that otherwise take years to learn."
- **Design emerges from the refactor step.** That is where the entire body of good-design knowledge gets applied: increase cohesion, decrease coupling, separate concerns, modularize, shrink functions and classes, choose better names.
- **You can take good rules too far.** Eliminating duplication, expressiveness, and SRP all have an over-application failure mode — a proliferation of tiny classes and methods. Rule 4 exists to bound the other three.
- **Small extractions have compounding effects.** A three-line `replaceImage` isn't worth much on its own; what it's worth is the SRP violation it exposes and the reuse it makes visible.

## Code Examples

Duplication of *implementation*:

```java
int size() {}
boolean isEmpty() {}
```
```java
// tie isEmpty to the definition of size instead of tracking a separate boolean
boolean isEmpty() {
    return 0 == size();
}
```

Small-scale duplication worth eliminating:

```java
// before — image.dispose(); System.gc(); image = newImage; appears twice
public void scaleToOneDimension(float desiredDimension, float imageDimension) {
    if (Math.abs(desiredDimension - imageDimension) < errorThreshold)
        return;
    float scalingFactor = desiredDimension / imageDimension;
    scalingFactor = (float)(Math.floor(scalingFactor * 100) * 0.01f);

    RenderedOp newImage = ImageUtilities.getScaledImage(
        image, scalingFactor, scalingFactor);
    image.dispose();
    System.gc();
    image = newImage;
}

public synchronized void rotate(int degrees) {
    RenderedOp newImage = ImageUtilities.getRotatedImage(image, degrees);
    image.dispose();
    System.gc();
    image = newImage;
}
```
```java
// after
public void scaleToOneDimension(float desiredDimension, float imageDimension) {
    if (Math.abs(desiredDimension - imageDimension) < errorThreshold)
        return;
    float scalingFactor = desiredDimension / imageDimension;
    scalingFactor = (float)(Math.floor(scalingFactor * 100) * 0.01f);

    replaceImage(ImageUtilities.getScaledImage(
        image, scalingFactor, scalingFactor));
}

public synchronized void rotate(int degrees) {
    replaceImage(ImageUtilities.getRotatedImage(image, degrees));
}

private void replaceImage(RenderedOp newImage) {
    image.dispose();
    System.gc();
    image = newImage;
}
```
- **What it demonstrates**: "Creating a clean system requires the will to eliminate duplication, even in just a few lines of code."

## Reference Tables

| Rule | Priority | What it drives | Over-application risk |
|---|---|---|---|
| Runs all the tests | 1 | Verifiability; and *indirectly* small single-purpose classes, low coupling, DIP/DI/interfaces | — |
| Contains no duplication | 2 | Extraction, reuse in the small, TEMPLATE METHOD | Too many tiny methods |
| Expresses intent | 3 | Naming, small units, standard nomenclature, tests as documentation | Over-abstraction |
| Minimizes classes and methods | 4 (lowest) | Bounds rules 2–3 | Dogmatism in the other direction (interface-per-class) |

## Worked Example
**TEMPLATE METHOD against higher-level duplication.** Two accrual methods that are the same algorithm except for one step:

```java
public class VacationPolicy {
    public void accrueUSDivisionVacation() {
        // code to calculate vacation based on hours worked to date
        // ...
        // code to ensure vacation meets US minimums
        // ...
        // code to apply vaction to payroll record
        // ...
    }

    public void accrueEUDivisionVacation() {
        // code to calculate vacation based on hours worked to date
        // ...
        // code to ensure vacation meets EU minimums
        // ...
        // code to apply vaction to payroll record
        // ...
    }
}
```

The duplication here is not textual lines to extract — it is a shared *shape* with a variable step. TEMPLATE METHOD names the shape in the base class and leaves a hole:

```java
abstract public class VacationPolicy {
    public void accrueVacation() {
        calculateBaseVacationHours();
        alterForLegalMinimums();
        applyToPayroll();
    }

    private void calculateBaseVacationHours() { /* ... */ };
    abstract protected void alterForLegalMinimums();
    private void applyToPayroll() { /* ... */ };
}

public class USVacationPolicy extends VacationPolicy {
    @Override protected void alterForLegalMinimums() {
        // US specific logic
    }
}

public class EUVacationPolicy extends VacationPolicy {
    @Override protected void alterForLegalMinimums() {
        // EU specific logic
    }
}
```

The subclasses supply "the only bits of information that are not duplicated." Note that the algorithm's name and its three steps now sit at one level of abstraction — the same stepdown discipline from Ch 3, arrived at here by pursuing rule 2.

## Key Takeaways
1. Follow the four rules in priority order; they make good design emerge instead of requiring it up front.
2. Tests come first because testability *is* a design force — it drives small classes, low coupling, and dependency inversion.
3. Refactor continuously in the safety the tests provide: every few lines, ask whether the design just degraded.
4. Attack duplication in all its forms — identical lines, similar lines, and duplicated implementation of related facts.
5. Use TEMPLATE METHOD when two algorithms share a shape and differ in one step.
6. Reuse in the small is the prerequisite for reuse in the large.
7. Express intent with names, small units, standard pattern nomenclature, and tests as documentation — and above all, by actually trying.
8. Keep class and method counts low, but never at the cost of the first three rules.

## Connects To
- **Ch 1 (Clean Code)**: Ron Jeffries states Beck's rules of simple code — the same four, phrased slightly differently.
- **Ch 3 (Functions)**: DRY as "the root of all evil"; the vacation template is the stepdown rule applied.
- **Ch 9 (Unit Tests)**: rule 1 in practice; tests as documentation by example.
- **Ch 10 (Classes)**: SRP violations surfaced by small extractions; cohesion and coupling as the goals tests drive you toward.
- **Ch 11 (Systems)**: "use the simplest thing that can possibly work" at architecture scale.
- **[XPE]**: Beck, *Extreme Programming Explained*. **[GOF]**: TEMPLATE METHOD, COMMAND, VISITOR.
