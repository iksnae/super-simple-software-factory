# Template Method
*Class Behavioral · GoF p. 325*

## Intent
> **Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure.**

## Motivation
An application framework with `Application` and `Document` classes. "Applications built with the framework can subclass `Application` and `Document` to suit specific needs" — `DrawApplication`/`DrawDocument`, `SpreadsheetApplication`/`SpreadsheetDocument`.

```cpp
void Application::OpenDocument (const char* name) {
    if (!CanOpenDocument(name)) {
        // cannot handle this document
        return;
    }

    Document* doc = DoCreateDocument();

    if (doc) {
        _docs->AddDocument(doc);
        AboutToOpenDocument(doc);
        doc->Open();
        doc->DoRead();
    }
}
```

"We call `OpenDocument` a **template method**. A template method **defines an algorithm in terms of abstract operations that subclasses override** to provide concrete behavior."

Who supplies which step:
- `Application` subclasses define **`CanOpenDocument`** (can this be opened?) and **`DoCreateDocument`** (create the Document).
- `Document` classes define **`DoRead`** (read the document).
- **`AboutToOpenDocument`** is a notification "that lets `Application` subclasses know when the document is about to be opened, **in case they care**" — a hook.

**The bargain**: "By defining some of the steps of an algorithm using abstract operations, **the template method fixes their ordering, but it lets `Application` and `Document` subclasses vary those steps** to suit their needs."

## Applicability
Use Template Method:
- "to implement the **invariant parts of an algorithm once** and leave it up to subclasses to implement the behavior that can vary."
- "when **common behavior among subclasses should be factored and localized in a common class to avoid code duplication**. This is a good example of '**refactoring to generalize**'... **You first identify the differences in the existing code and then separate the differences into new operations. Finally, you replace the differing code with a template method that calls one of these new operations.**"
- "to **control subclasses extensions**. You can define a template method that calls '**hook**' operations at specific points, thereby **permitting extensions only at those points**."

## Participants
- **AbstractClass** (`Application`) — "defines abstract **primitive operations** that concrete subclasses define to implement steps of an algorithm"; "implements a **template method defining the skeleton** of an algorithm."
- **ConcreteClass** (`MyApplication`) — "implements the primitive operations to carry out subclass-specific steps of the algorithm."

## Collaborations
- "ConcreteClass relies on AbstractClass to implement the **invariant steps** of the algorithm."

## Consequences
"Template methods are a **fundamental technique for code reuse**. They are particularly important in **class libraries**, because they are the means for factoring out common behavior in library classes."

**The Hollywood Principle**: "Template methods lead to an **inverted control structure** that's sometimes referred to as '**the Hollywood principle**,' that is, '**Don't call us, we'll call you.**' This refers to how **a parent class calls the operations of a subclass and not the other way around**."

**The five kinds of operation a template method calls:**

| Kind | Notes |
|---|---|
| **Concrete operations** | "either on the ConcreteClass or on client classes" |
| **Concrete AbstractClass operations** | "operations that are **generally useful to subclasses**" |
| **Primitive operations** | "i.e., **abstract** operations" — must be overridden |
| **Factory methods** | see Factory Method (107) |
| **Hook operations** | "provide **default behavior that subclasses can extend if necessary**. **A hook operation often does nothing by default.**" |

⚠️ **The documentation obligation**: "It's important for template methods to **specify which operations are hooks (may be overridden) and which are abstract operations (must be overridden)**. To reuse an abstract class effectively, **subclass writers must understand which operations are designed for overriding**."

## Worked Example
**Turning a fragile override into a controlled hook.**

The usual way to extend a parent operation:

```cpp
void DerivedClass::Operation () {
    ParentClass::Operation();
    // DerivedClass extended behavior
}
```

⚠️ "**Unfortunately, it's easy to forget to call the inherited operation.**"

The fix: "**transform such an operation into a template method to give the parent control over how subclasses extend it.** The idea is to **call a hook operation from a template method in the parent class**. Then subclasses can override this hook operation":

```cpp
void ParentClass::Operation () {
    // ParentClass behavior
    HookOperation();
}

void ParentClass::HookOperation () { }

void DerivedClass::HookOperation () {
    // derived class extension
}
```

The parent's behavior can no longer be skipped, and the extension point is explicit rather than conventional. This is the same mechanism Observer recommends for guaranteeing self-consistency before `Notify` (Observer, Implementation issue 5).

## Implementation
1. **Using C++ access control.** "the primitive operations that a template method calls can be declared **protected** members. This ensures that they are **only called by the template method**. Primitive operations that **must** be overridden are declared **pure virtual**. **The template method itself should not be overridden; therefore you can make the template method a nonvirtual member function.**"
2. **Minimizing primitive operations.** "An important goal... is to **minimize the number of primitive operations that a subclass must override** to flesh out the algorithm. **The more operations that need overriding, the more tedious things get for clients.**"
3. **Naming conventions.** "You can **identify the operations that should be overridden by adding a prefix to their names**. For example, the **MacApp** framework prefixes template method names with '**Do-**': `DoCreateDocument`, `DoRead`, and so forth."

## Sample Code
From NeXT's AppKit. "`View` enforces the invariant that its subclasses can draw into a view **only after it becomes the 'focus'**, which requires certain drawing state (for example, colors and fonts) to be set up properly."

```cpp
void View::Display () {
    SetFocus();
    DoDisplay();
    ResetFocus();
}
```
- "`Display` calls `SetFocus` **before** `DoDisplay` to set up the drawing state; `Display` calls `ResetFocus` **afterwards** to release the drawing state."
- "**To maintain the invariant, the view's clients always call `Display`, and `View` subclasses always override `DoDisplay`.**"

```cpp
void View::DoDisplay () { }

void MyView::DoDisplay () {
    // render the view's contents
}
```
- The whole pattern in five lines: the setup/teardown pair **cannot be forgotten**, because the subclass never controls the surrounding sequence.

## Known Uses
- "Template methods are **so fundamental that they can be found in almost every abstract class**."
- **Wirfs-Brock et al.** "provide a good overview and discussion of template methods."

## Related Patterns
- "**Factory Methods** are often called by template methods. In the Motivation example, the factory method `DoCreateDocument` is called by the template method `OpenDocument`."
- "**Strategy**: **Template methods use inheritance to vary *part* of an algorithm. Strategies use delegation to vary the *entire* algorithm.**"

## Connects To
- **Ch 5 (Behavioral Patterns)**: one of only two behavioral **class** patterns — "**the simpler and more common of the two.** A template method is an abstract definition of an algorithm... **Each step invokes either an abstract operation or a primitive operation.**"
- **Ch 6 (Factory Method)**: `DoCreateDocument` is exactly the Factory Method's motivating example.
- **Ch 24 (Observer)**: use a template method so `Notify` fires last, after the subclass has finished updating its state.
- **Ch 26 (Strategy)**: inheritance vs. delegation for varying behavior.
- **Ch 1**: "**Inheritance vs. Composition**" and the white-box reuse discussion — Template Method is white-box reuse in its purest form.
