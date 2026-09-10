# Chapter 6: Objects and Data Structures

## Core Idea
Objects hide their data behind abstractions and expose functions that operate on it; data structures expose their data and have no meaningful functions — these are virtual opposites, and choosing the wrong one for the job is a design error, not a style preference.

## Frameworks Introduced
- **Data Abstraction**: hiding implementation is about abstractions, not about interposing a layer of functions between callers and variables.
  - When to use: designing any class's public surface.
  - How: "A class does not simply push its variables out through getters and setters. Rather it exposes abstract interfaces that allow its users to manipulate the essence of the data, without having to know its implementation." Serious thought goes into the best representation; "the worst option is to blithely add getters and setters."
- **Data/Object Anti-Symmetry** — the fundamental dichotomy:
  - *Procedural code (using data structures) makes it easy to add new functions without changing the existing data structures. OO code makes it easy to add new classes without changing existing functions.*
  - *Procedural code makes it hard to add new data structures because all the functions must change. OO code makes it hard to add new functions because all the classes must change.*
  - When to use: choosing between a polymorphic hierarchy and a procedural switch over plain structs.
  - How: ask which axis will change more — new types, or new operations. Objects for new types; data structures plus procedures for new operations.
- **The Law of Demeter**: a module should not know about the innards of the objects it manipulates. A method `f` of class `C` should only call methods of:
  - `C` itself
  - an object created by `f`
  - an object passed as an argument to `f`
  - an object held in an instance variable of `C`
  - …and must not invoke methods on objects *returned* by any of those. "Talk to friends, not to strangers."
- **Tell, don't ask (Hiding Structure)**: if `ctxt` is an object, tell it to do something rather than asking it about its internals.

## Key Concepts
- **Train wreck** — `ctxt.getOptions().getScratchDir().getAbsolutePath()`; chained calls that look like coupled train cars. Sloppy style, should be split up [G36].
- **Whether a train wreck violates Demeter depends on what the links are.** If `ctxt`, `Options`, and `ScratchDir` are *objects*, their innards should be hidden and this is a clear violation. If they are *data structures* with no behavior, they naturally expose their structure and Demeter does not apply. Accessor functions are what confuse the issue — written as `ctxt.options.scratchDir.absolutePath` nobody would even ask.
- **Hybrid** — half object, half data structure: significant functions *and* public variables or public accessors/mutators that effectively publish the private state. "The worst of both worlds" — hard to add functions *and* hard to add data structures. Indicative of a muddled design whose authors are unsure whether they need protection from functions or from types. (Related to *Feature Envy* from Fowler's *Refactoring*.)
- **DTO (Data Transfer Object)** — the quintessential data structure: public variables, no functions. Genuinely useful for database communication and socket message parsing; often the first of a series of translation stages from raw data to application objects.
- **Bean** — private variables with getters and setters. "The quasi-encapsulation of beans seems to make some OO purists feel better but usually provides no other benefit."
- **Active Record** — a DTO with navigational methods like `save` and `find`, usually a direct translation of a database table. The mistake is putting business rules into it, producing a hybrid. **The fix: treat the Active Record as a data structure and put the business rules in separate objects that hide their internal data** (which is probably an Active Record instance).

## Mental Models
- **"The idea that everything is an object is a myth."** Mature programmers know this. Sometimes you really do want simple data structures with procedures operating on them.
- **Don't sneer at procedural code reflexively.** Add `perimeter()` to the procedural `Geometry` class and no shape class changes, and no client of the shapes changes. Add a new shape and every `Geometry` function changes. The two conditions are diametrically opposed — neither style is universally better.
- **When you catch yourself asking an object for a path, ask what you were going to do with it.** The train-wreck example's real intent was to create a scratch file, so the answer was `ctxt.createScratchFileStream(classFileName)` — which lets `ctxt` keep its internals and removes the Demeter problem entirely.
- **VISITOR and dual-dispatch exist, but they cost.** They work around OO's difficulty adding functions, and "generally return the structure to that of a procedural program."

## Code Examples

Abstraction is not accessors (Listings 6-1 / 6-2):

```java
// Listing 6-1 — Concrete Point: implementation is visible, coordinates
// must be manipulated independently
public class Point {
    public double x;
    public double y;
}
```
```java
// Listing 6-2 — Abstract Point
public interface Point {
    double getX();
    double getY();
    void setCartesian(double x, double y);
    double getR();
    double getTheta();
    void setPolar(double r, double theta);
}
```
- **What it demonstrates**: you cannot tell whether the implementation is rectangular or polar — it might be neither — and yet it unmistakably represents a data structure. The methods also **enforce an access policy**: read coordinates independently, but set them together as an atomic operation. Listing 6-1 would still expose implementation even with private fields and single-variable getters/setters.

Abstraction chosen at the right level (Listings 6-3 / 6-4):

```java
// concrete: obviously just variable accessors
public interface Vehicle {
    double getFuelTankCapacityInGallons();
    double getGallonsOfGasoline();
}
```
```java
// abstract: no clue at all about the form of the data
public interface Vehicle {
    double getPercentFuelRemaining();
}
```

The two shape implementations (Listings 6-5 / 6-6):

```java
// Listing 6-5 — Procedural Shape: shapes are data, all behavior in Geometry
public class Square { public Point topLeft; public double side; }
public class Rectangle { public Point topLeft; public double height; public double width; }
public class Circle { public Point center; public double radius; }

public class Geometry {
    public final double PI = 3.141592653589793;

    public double area(Object shape) throws NoSuchShapeException {
        if (shape instanceof Square) {
            Square s = (Square)shape;
            return s.side * s.side;
        }
        else if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle)shape;
            return r.height * r.width;
        }
        else if (shape instanceof Circle) {
            Circle c = (Circle)shape;
            return PI * c.radius * c.radius;
        }
        throw new NoSuchShapeException();
    }
}
```
```java
// Listing 6-6 — Polymorphic Shapes: no Geometry class needed
public class Square implements Shape {
    private Point topLeft;
    private double side;
    public double area() { return side*side; }
}

public class Rectangle implements Shape {
    private Point topLeft;
    private double height;
    private double width;
    public double area() { return height * width; }
}

public class Circle implements Shape {
    private Point center;
    private double radius;
    public final double PI = 3.141592653589793;
    public double area() { return PI * radius * radius; }
}
```
- **What it demonstrates**: add `perimeter()` — 6-5 changes one class, 6-6 changes every class. Add `Triangle` — 6-5 changes every `Geometry` function, 6-6 changes nothing existing.

## Reference Tables

| | Objects | Data structures |
|---|---|---|
| Data | Hidden behind abstractions | Exposed |
| Functions | Operate on hidden data | None meaningful |
| Adding a new **type** | Easy — nothing existing changes | Hard — every function must change |
| Adding a new **function** | Hard — every class must change | Easy — nothing existing changes |
| Law of Demeter | Applies; navigating innards is a violation | Does not apply; structure is meant to be visible |
| Prefer when | The system will grow new data types | The system will grow new behaviors |

| Form | Shape | Verdict |
|---|---|---|
| DTO | Public variables, no functions | Useful — DB rows, socket messages, translation stages |
| Bean | Private variables, getters/setters | Quasi-encapsulation; usually no real benefit |
| Active Record | DTO + `save`/`find` | Fine as a data structure; putting business rules in it creates a hybrid |
| Hybrid | Real behavior + public state | Avoid — worst of both worlds |

## Worked Example
**From train wreck to a message.** The starting code, found in the Apache framework:

```java
final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();
```

The conventional fix is to split the chain:

```java
Options opts = ctxt.getOptions();
File scratchDir = opts.getScratchDir();
final String outputDir = scratchDir.getAbsolutePath();
```

But this does not answer the design question — the containing module still knows that `ctxt` has options, which have a scratch directory, which has an absolute path. That is a lot of navigation knowledge for one function.

If those are real objects, the two "hiding" attempts both fail: `ctxt.getAbsolutePathOfScratchDirectoryOption()` leads to an explosion of methods on `ctxt`, and `ctxt.getScratchDirectoryOption().getAbsolutePath()` only works if the option is a data structure. "Neither option feels good."

So Martin asks what the path was *for*. Many lines further down in the same module:

```java
String outFile = outputDir + "/" + className.replace('.', '/') + ".class";
FileOutputStream fout = new FileOutputStream(outFile);
BufferedOutputStream bos = new BufferedOutputStream(fout);
```

(He notes in passing that dots, slashes, file extensions, and `File` objects mixed together is itself an admixture of abstraction levels [G34][G6].) The intent was to create a scratch file with a given name — so tell `ctxt` to do exactly that:

```java
BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
```

`ctxt` keeps its internals, the caller stops navigating objects it should not know about, and the Demeter violation disappears rather than being reformatted.

## Key Takeaways
1. Getters and setters are not encapsulation. Ask what abstraction expresses the *essence* of the data, then expose that.
2. Objects and data structures are opposites; pick by which axis of change you expect — new types or new operations.
3. Not everything should be an object. Procedural code with data structures is the right answer when behaviors grow faster than types.
4. Law of Demeter violations are about objects, not about dot counting; whether a chain is a violation depends on whether the links are objects or data structures.
5. When you want a value out of an object, ask what you intended to do with it, and send that as a message instead.
6. Hybrids — real behavior plus exposed state — are the worst of both worlds; they signal that the designer never decided which they were building.
7. Keep Active Records as data structures and put business rules in separate objects that hide them.

## Connects To
- **Ch 3 (Functions)**: burying a `switch` in a factory is the OO answer to the same anti-symmetry described here.
- **Ch 10 (Classes)**: hiding structure and keeping variables private is the cohesion argument at class scale.
- **Ch 11 (Systems)**: DTOs as translation stages between infrastructure and application objects.
- **Ch 17**: [G36] avoid transitive navigation, [G34] abstraction levels, [G6] code at wrong level of abstraction.
- **Refactoring (Fowler)**: Feature Envy — the smell hybrids induce in their clients.
