# Builder
*Object Creational · GoF p. 97*

## Intent
> **Separate the construction of a complex object from its representation so that the same construction process can create different representations.**

## Motivation
An RTF reader that must convert to many text formats. "**The problem, however, is that the number of possible conversions is open-ended.** So it should be easy to add a new conversion without modifying the reader."

Configure the `RTFReader` with a `TextConverter`. "Whenever the `RTFReader` recognizes an RTF token (either plain text or an RTF control word), it issues a request to the `TextConverter` to convert the token. **TextConverter objects are responsible both for performing the data conversion and for representing the token in a particular format.**"

The subclasses differ dramatically in how much they do: "an `ASCIIConverter` **ignores requests to convert anything except plain text**. A `TeXConverter`, on the other hand, will implement operations for **all** requests in order to produce a TeX representation that captures all the stylistic information. A `TextWidgetConverter` will produce a complex user interface object that lets the user see and edit the text."

Vocabulary: "**Each converter class is called a builder in the pattern, and the reader is called the director.**"

## Applicability
Use Builder when:
- "the algorithm for creating a complex object should be **independent of the parts** that make up the object and how they're assembled."
- "the construction process must allow **different representations** for the object that's constructed."

## Participants
- **Builder** (`TextConverter`) — specifies an abstract interface for creating parts of a Product object.
- **ConcreteBuilder** (`ASCIIConverter`, `TeXConverter`, `TextWidgetConverter`) — constructs and assembles parts by implementing the Builder interface; **defines and keeps track of the representation it creates**; provides an interface for retrieving the product (`GetASCIIText`, `GetTextWidget`).
- **Director** (`RTFReader`) — constructs an object using the Builder interface.
- **Product** (`ASCIIText`, `TeXText`, `TextWidget`) — the complex object under construction.

## Collaborations
- "The client creates the **Director** object and configures it with the desired **Builder** object."
- "Director **notifies the builder** whenever a part of the product should be built."
- "Builder handles requests from the director and **adds parts to the product**."
- "**The client retrieves the product from the builder.**" (Note: from the *builder*, not the director.)

## Consequences
1. **It lets you vary a product's internal representation.** "Because the product is constructed through an abstract interface, all you have to do to change the product's internal representation is **define a new kind of builder**."
2. **It isolates code for construction and representation.** "Clients needn't know anything about the classes that define the product's internal structure; such classes don't appear in Builder's interface... **The code is written once; then different Directors can reuse it** to build Product variants from the same set of parts." Example: "we could define a reader for a format other than RTF, say, an **SGMLReader**, and use the same TextConverters."
3. **It gives you finer control over the construction process.** "Unlike creational patterns that construct products **in one shot**, the Builder pattern constructs the product **step by step under the director's control**. Only when the product is finished does the director retrieve it from the builder."

## Implementation
1. **Assembly and construction interface.** "A model where the results of construction requests are simply **appended** to the product is usually sufficient." But sometimes you need access to parts constructed earlier — the maze builder "lets you add a door between existing rooms." For bottom-up parse trees, "the builder would **return child nodes to the director, which then would pass them back** to the builder to build the parent nodes."
2. **Why no abstract class for products?** "In the common case, the products produced by the concrete builders **differ so greatly in their representation that there is little to gain** from giving different products a common parent class... Because the client usually configures the director with the proper concrete builder, **the client is in a position to know which concrete subclass of Builder is in use** and can handle its products accordingly."
3. **Empty methods as default in Builder.** "In C++, the build methods are **intentionally not declared pure virtual**... They're defined as empty methods instead, letting clients override only the operations they're interested in."

## Sample Code

```cpp
class MazeBuilder {
public:
    virtual void BuildMaze() { }
    virtual void BuildRoom(int room) { }
    virtual void BuildDoor(int roomFrom, int roomTo) { }

    virtual Maze* GetMaze() { return 0; }
protected:
    MazeBuilder();
};
```

```cpp
Maze* MazeGame::CreateMaze (MazeBuilder& builder) {
    builder.BuildMaze();

    builder.BuildRoom(1);
    builder.BuildRoom(2);
    builder.BuildDoor(1, 2);

    return builder.GetMaze();
}
```
- **What it demonstrates**: "Notice how the builder **hides the internal representation of the Maze** — that is, the classes that define rooms, doors, and walls — and how these parts are assembled... Someone might guess that there are classes for representing rooms and doors, but **there is no hint of one for walls**."

Reuse of the same builder interface for a different construction algorithm:

```cpp
Maze* MazeGame::CreateComplexMaze (MazeBuilder& builder) {
    builder.BuildRoom(1);
    // ...
    builder.BuildRoom(1001);

    return builder.GetMaze();
}
```

A concrete builder that keeps the product in progress:

```cpp
class StandardMazeBuilder : public MazeBuilder {
public:
    StandardMazeBuilder();

    virtual void BuildMaze();
    virtual void BuildRoom(int);
    virtual void BuildDoor(int, int);

    virtual Maze* GetMaze();
private:
    Direction CommonWall(Room*, Room*);
    Maze* _currentMaze;
};
```
```cpp
void StandardMazeBuilder::BuildRoom (int n) {
    if (!_currentMaze->RoomNo(n)) {
        Room* room = new Room(n);
        _currentMaze->AddRoom(room);

        room->SetSide(North, new Wall);
        room->SetSide(South, new Wall);
        room->SetSide(East, new Wall);
        room->SetSide(West, new Wall);
    }
}

void StandardMazeBuilder::BuildDoor (int n1, int n2) {
    Room* r1 = _currentMaze->RoomNo(n1);
    Room* r2 = _currentMaze->RoomNo(n2);
    Door* d = new Door(r1, r2);

    r1->SetSide(CommonWall(r1, r2), d);
    r2->SetSide(CommonWall(r2, r1), d);
}
```

**Why not put this in `Maze` itself?** "We could have put all the `StandardMazeBuilder` operations in `Maze` and let each `Maze` build itself. But making `Maze` smaller makes it easier to understand and modify... **Most importantly, separating the two lets you have a variety of MazeBuilders, each using different classes for rooms, walls, and doors.**"

**The builder that builds nothing** — the clearest demonstration that the director's algorithm is genuinely independent of the product:

```cpp
class CountingMazeBuilder : public MazeBuilder {
public:
    CountingMazeBuilder();

    virtual void BuildMaze();
    virtual void BuildRoom(int);
    virtual void BuildDoor(int, int);
    virtual void AddWall(int, Direction);

    void GetCounts(int&, int&) const;
private:
    int _doors;
    int _rooms;
};

void CountingMazeBuilder::BuildRoom (int) { _rooms++; }
void CountingMazeBuilder::BuildDoor (int, int) { _doors++; }
```
- **What it demonstrates**: "This builder **doesn't create a maze at all**; it just counts the different kinds of components that would have been created." Same director, same calls, no product.

## Known Uses
- **ET++** — the RTF converter application; its text building block uses a builder to process RTF.
- **Smalltalk-80**, where Builder is common:
  - "The **Parser** class in the compiler subsystem is a Director that takes a `ProgramNodeBuilder` object as an argument... When the parser is done, it asks the builder for the parse tree it built."
  - "**ClassBuilder** is a builder that Classes use to create subclasses for themselves. In this case **a Class is both the Director and the Product**."
  - "**ByteCodeStream** is a builder that creates a compiled method as a byte array... a nonstandard use of the Builder pattern, because the complex object it builds is encoded as a byte array, not as a normal Smalltalk object."
- **Service Configurator** (Adaptive Communications Environment) — builds network service components linked into a server at run time; the components are described in a configuration language parsed by an LALR(1) parser, and "**the parser is the Director**."

## Related Patterns
- **Abstract Factory** "is similar to Builder in that it too may construct complex objects. **The primary difference is that the Builder pattern focuses on constructing a complex object step by step.** Abstract Factory's emphasis is on families of product objects (either simple or complex). **Builder returns the product as a final step**, but as far as the Abstract Factory pattern is concerned, the product gets returned immediately."
- "A **Composite** is what the builder often builds."

## Connects To
- **Ch 3 (Creational Patterns)**: "Builder has the factory object building a complex product incrementally using a correspondingly complex protocol"; "Builder can use one of the other patterns to implement which components get built."
- **Ch 1**: cause of redesign #5 — algorithmic dependencies.
- **Abstract Factory, Composite**
