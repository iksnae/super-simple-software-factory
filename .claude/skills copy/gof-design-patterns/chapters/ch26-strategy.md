# Strategy
*Object Behavioral · Also Known As: **Policy** · GoF p. 315*

## Intent
> **Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.**

## Motivation
"Many algorithms exist for breaking a stream of text into lines. **Hard-wiring all such algorithms into the classes that require them isn't desirable** for several reasons:"
- "Clients that need linebreaking **get more complex** if they include the linebreaking code."
- "Different algorithms will be appropriate at different times. **We don't want to support multiple linebreaking algorithms if we don't use them all.**"
- "It's **difficult to add new algorithms and vary existing ones** when linebreaking is an integral part of a client."

"An algorithm that's encapsulated in this way is called a **strategy**."

The three concrete compositors:
- **`SimpleCompositor`** — "determines linebreaks **one at a time**."
- **`TeXCompositor`** — "implements the TeX algorithm... tries to **optimize linebreaks globally**, that is, **one paragraph at a time**."
- **`ArrayCompositor`** — "selects breaks so that **each row has a fixed number of items**. It's useful for breaking a collection of icons into rows."

"**A `Composition` maintains a reference to a `Compositor` object.** Whenever a `Composition` reformats its text, it **forwards this responsibility** to its `Compositor` object. **The client of `Composition` specifies which `Compositor` should be used by installing the `Compositor` it desires into the `Composition`.**"

## Applicability
Use Strategy when:
- "**many related classes differ only in their behavior.** Strategies provide a way to configure a class with one of many behaviors."
- "you need **different variants of an algorithm** — for example, algorithms reflecting different **space/time trade-offs**."
- "an algorithm uses **data that clients shouldn't know about**. Use the Strategy pattern to avoid exposing complex, algorithm-specific data structures."
- "a class defines many behaviors, and these appear as **multiple conditional statements** in its operations. Instead of many conditionals, **move related conditional branches into their own Strategy class**."

## Participants
- **Strategy** (`Compositor`) — "declares an interface common to all supported algorithms. Context uses this interface to call the algorithm defined by a ConcreteStrategy."
- **ConcreteStrategy** (`SimpleCompositor`, `TeXCompositor`, `ArrayCompositor`) — "implements the algorithm using the Strategy interface."
- **Context** (`Composition`) — "is configured with a ConcreteStrategy object"; "maintains a reference to a Strategy object"; "**may define an interface that lets Strategy access its data**."

## Collaborations
- "A context **may pass all data required by the algorithm to the strategy** when the algorithm is called. **Alternatively, the context can pass itself as an argument** to Strategy operations. That lets the strategy **call back on the context** as required."
- "**Clients usually create and pass a ConcreteStrategy object to the context; thereafter, clients interact with the context exclusively.**"

## Consequences
1. **Families of related algorithms.** "Hierarchies of Strategy classes define a family of algorithms or behaviors for contexts to reuse. **Inheritance can help factor out common functionality of the algorithms.**"
2. **An alternative to subclassing.** "You can subclass a Context class directly to give it different behaviors. But **this hard-wires the behavior into Context**. It mixes the algorithm implementation with Context's, making Context harder to understand, maintain, and extend. **And you can't vary the algorithm dynamically.** You wind up with many related classes whose only difference is the algorithm or behavior they employ."
3. **Strategies eliminate conditional statements.** "When different behaviors are lumped into one class, **it's hard to avoid using conditional statements** to select the right behavior."

Without strategies:

```cpp
void Composition::Repair () {
    switch (_breakingStrategy) {
    case SimpleStrategy:
        ComposeWithSimpleCompositor();
        break;
    case TeXStrategy:
        ComposeWithTeXCompositor();
        break;
    // ...
    }
    // merge results with existing composition, if necessary
}
```

With:

```cpp
void Composition::Repair () {
    _compositor->Compose();
    // merge results with existing composition, if necessary
}
```
   - **The diagnostic**: "**Code containing many conditional statements often indicates the need to apply the Strategy pattern.**"
4. **A choice of implementations.** "The client can choose among strategies with **different time and space trade-offs**."
5. ⚠️ **Clients must be aware of different Strategies.** "a client **must understand how Strategies differ before it can select the appropriate one**. Clients might be exposed to implementation issues. **Therefore you should use the Strategy pattern only when the variation in behavior is relevant to clients.**"
6. ⚠️ **Communication overhead between Strategy and Context.** "The Strategy interface is shared by all ConcreteStrategy classes **whether the algorithms they implement are trivial or complex**. Hence it's likely that some ConcreteStrategies won't use all the information passed to them; **simple ConcreteStrategies may use none of it!** That means there will be times when **the context creates and initializes parameters that never get used**. If this is an issue, then you'll need **tighter coupling** between Strategy and Context."
7. ⚠️ **Increased number of objects.** "Sometimes you can reduce this overhead by implementing strategies as **stateless objects that contexts can share**. Any residual state is maintained by the context, which passes it in each request... **Shared strategies should not maintain state across invocations.** The **Flyweight** pattern describes this approach in more detail."

## Implementation
1. **Defining the Strategy and Context interfaces.** Two techniques with opposite trade-offs:

| Technique | Benefit | Cost |
|---|---|---|
| **"Take the data to the strategy"** — Context passes data in parameters | "keeps Strategy and Context **decoupled**" | "Context might pass data the Strategy **doesn't need**" |
| **Context passes itself** (or Strategy stores a reference to its context) | "the strategy can request **exactly what it needs**" | "Context must define a **more elaborate interface to its data**, which **couples Strategy and Context more closely**" |

   - "**The needs of the particular algorithm and its data requirements will determine the best technique.**"
2. **Strategies as template parameters.** "This technique is only applicable if (1) the Strategy can be **selected at compile-time**, and (2) it **does not have to be changed at run-time**."

```cpp
template <class AStrategy>
class Context {
    void Operation() { theStrategy.DoAlgorithm(); }
    // ...
private:
    AStrategy theStrategy;
};

class MyStrategy {
public:
    void DoAlgorithm();
};

Context<MyStrategy> aContext;
```
   - "With templates, **there's no need to define an abstract class** that defines the interface to the Strategy. Using Strategy as a template parameter also lets you **bind a Strategy to its Context statically, which can increase efficiency**."
3. **Making Strategy objects optional.** "Context checks to see if it has a Strategy object before accessing it. **If there isn't a strategy, then Context carries out default behavior.** The benefit is that **clients don't have to deal with Strategy objects at all unless they don't like the default behavior**."

## Sample Code
Based on InterViews' `Composition` and `Compositor`.

"Each component has an associated **natural size, stretchability, and shrinkability**. The **stretchability** defines how much the component can grow beyond its natural size; **shrinkability** is how much it can shrink."

```cpp
class Composition {
public:
    Composition(Compositor*);
    void Repair();
private:
    Compositor* _compositor;
    Component* _components;   // the list of components
    int _componentCount;      // the number of components
    int _lineWidth;           // the Composition's line width
    int* _lineBreaks;         // the position of linebreaks
                              // in components
    int _lineCount;           // the number of lines
};
```

"The `Compositor` interface lets the composition pass the compositor all the information it needs. **This is an example of 'taking the data to the strategy'**":

```cpp
class Compositor {
public:
    virtual int Compose(
        Coord natural[], Coord stretch[], Coord shrink[],
        int componentCount, int lineWidth, int breaks[]
    ) = 0;
protected:
    Compositor();
};
```

```cpp
void Composition::Repair () {
    Coord* natural;
    Coord* stretchability;
    Coord* shrinkability;
    int componentCount;
    int* breaks;

    // prepare the arrays with the desired component sizes
    // ...

    // determine where the breaks are:
    int breakCount;
    breakCount = _compositor->Compose(
        natural, stretchability, shrinkability,
        componentCount, _lineWidth, breaks
    );

    // lay out components according to breaks
    // ...
}
```

```cpp
class SimpleCompositor : public Compositor {
public:
    SimpleCompositor();

    virtual int Compose(
        Coord natural[], Coord stretch[], Coord shrink[],
        int componentCount, int lineWidth, int breaks[]
    );
    // ...
};

class TeXCompositor : public Compositor {
public:
    TeXCompositor();

    virtual int Compose(
        Coord natural[], Coord stretch[], Coord shrink[],
        int componentCount, int lineWidth, int breaks[]
    );
    // ...
};

class ArrayCompositor : public Compositor {
public:
    ArrayCompositor(int interval);

    virtual int Compose(
        Coord natural[], Coord stretch[], Coord shrink[],
        int componentCount, int lineWidth, int breaks[]
    );
    // ...
};
```
- ⚠️ **Consequence 6, made concrete**: "These classes **don't use all the information passed in `Compose`**. `SimpleCompositor` **ignores the stretchability**, taking only their natural widths into account. `TeXCompositor` **uses all** the information passed to it, whereas **`ArrayCompositor` ignores everything.**"

```cpp
Composition* quick  = new Composition(new SimpleCompositor);
Composition* slick  = new Composition(new TeXCompositor);
Composition* iconic = new Composition(new ArrayCompositor(100));
```

**The design warning that closes the section**: "`Compositor`'s interface is **carefully designed to support all layout algorithms that subclasses might implement**. You don't want to have to change this interface with every new subclass, because that will require changing existing subclasses. **In general, the Strategy and Context interfaces determine how well the pattern achieves its intent.**"

## Known Uses
- **ET++** and **InterViews** — "use strategies to encapsulate different linebreaking algorithms as we've described."
- **RTL System for compiler code optimization** — "strategies define different **register allocation schemes** (`RegisterAllocator`) and **instruction set scheduling policies** (`RISCscheduler`, `CISCscheduler`). This provides flexibility in targeting the optimizer for **different machine architectures**."
- **ET++SwapsManager** — a financial calculation engine. "`YieldCurve` calculates **discount factors**, which determine the present value of future cash flows. Both of these classes delegate some behavior to Strategy objects... **You can create new calculation engines by configuring `Instrument` and `YieldCurve` with the different ConcreteStrategy objects.**"
- **Booch components** — "use strategies as **template arguments**. The Booch collection classes support three different kinds of **memory allocation** strategies: **managed** (allocation out of a pool), **controlled** (allocations/deallocations are protected by locks), and **unmanaged** (the normal memory allocator)."

```cpp
UnboundedCollection<MyItemType*, Unmanaged>
```

- **RApp** (integrated circuit layout) — "**Routing algorithms** in RApp are defined as subclasses of an abstract `Router` class. **`Router` is a Strategy class.**"
- **Borland ObjectWindows** — "uses `Validator` objects to encapsulate **validation strategies**... **The client attaches a validator to a field if validation is required (an example of an optional strategy).** When the dialog is closed, the entry fields ask their validators to validate the data."

## Related Patterns
- "**Flyweight**: Strategy objects often make good flyweights."

## Connects To
- **Ch 2 (Case Study, §2.3)**: the `Composition`/`Compositor` formatting problem is where Lexi derives this pattern.
- **Ch 5 (Behavioral Patterns)**: Strategy "encapsulates **an algorithm**... makes it easy to specify and change the algorithm an object uses."
- **Ch 25 (State)**: the same structure, a different intent — Strategy's variants are chosen by the **client**; State's are driven by the object's own **state changes**.
- **Ch 27 (Template Method)**: the inheritance-based alternative for varying part of an algorithm.
- **Ch 15 (Flyweight)**: how stateless strategies get shared.
- **Ch 1**: cause of redesign #1 (creating an object by specifying a class explicitly) and #3 (dependence on algorithms).
