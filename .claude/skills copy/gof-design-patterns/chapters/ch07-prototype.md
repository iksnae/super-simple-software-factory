# Prototype
*Object Creational · GoF p. 117*

## Intent
> **Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.**

## Motivation
A music score editor built by customizing a graphical editor framework. The framework provides abstract `Graphic` and `Tool` classes and a `GraphicTool` subclass for tools that create graphical objects.

**The problem**: "The classes for notes and staves are specific to our application, but the `GraphicTool` class belongs to the **framework**. `GraphicTool` doesn't know how to create instances of our music classes... We could subclass `GraphicTool` for each kind of music object, but **that would produce lots of subclasses that differ only in the kind of music object they instantiate**."

The solution: "making `GraphicTool` create a new `Graphic` by copying or '**cloning**' an instance of a `Graphic` subclass. We call this instance a **prototype**... If all Graphic subclasses support a `Clone` operation, then the GraphicTool can clone any kind of Graphic."

**And then the second reduction**, which is the pattern's real power: "We have separate classes for whole notes and half notes, but **that's probably unnecessary**. Instead they could be **instances of the same class initialized with different bitmaps and durations**. A tool for creating whole notes becomes just a `GraphicTool` whose prototype is a `MusicalNote` initialized to be a whole note. **This can reduce the number of classes in the system dramatically.**"

## Applicability
Use Prototype when a system should be independent of how its products are created, composed, and represented; **and**
- "when the classes to instantiate are **specified at run-time**, for example, by dynamic loading; or"
- "to avoid building a **class hierarchy of factories that parallels the class hierarchy of products**; or"
- "when instances of a class can have one of only a **few different combinations of state**. It may be more convenient to install a corresponding number of prototypes and clone them rather than instantiating the class manually, each time with the appropriate state."

## Participants
- **Prototype** (`Graphic`) — declares an interface for cloning itself.
- **ConcretePrototype** (`Staff`, `WholeNote`, `HalfNote`) — implements an operation for cloning itself.
- **Client** (`GraphicTool`) — creates a new object by asking a prototype to clone itself.

## Collaborations
- "A client asks a prototype to clone itself." (That is the entire collaboration.)

## Consequences
Shares with Abstract Factory and Builder: "It **hides the concrete product classes from the client**, thereby reducing the number of names clients know about."

1. **Adding and removing products at run-time.** "Prototypes let you incorporate a new concrete product class into a system simply by **registering a prototypical instance** with the client... a client can **install and remove prototypes at run-time**."
2. **Specifying new objects by varying values.** "You effectively define new kinds of objects by instantiating existing classes and registering the instances as prototypes... **This kind of design lets users define new 'classes' without programming.** In fact, cloning a prototype is similar to instantiating a class."
3. **Specifying new objects by varying structure.** Circuit editors build circuits out of subcircuits. "We simply add this subcircuit as a prototype to the palette of available circuit elements. **As long as the composite circuit object implements `Clone` as a deep copy**, circuits with different structures can be prototypes."
4. **Reduced subclassing.** "Factory Method often produces a hierarchy of Creator classes that parallels the product class hierarchy... **Hence you don't need a Creator class hierarchy at all.** This benefit applies primarily to languages like C++ that don't treat classes as first-class objects. Languages that do, like Smalltalk and Objective C, derive less benefit, since **class objects already act like prototypes** in these languages."
5. **Configuring an application with classes dynamically.** "An application that wants to create instances of a dynamically loaded class **won't be able to reference its constructor statically**. Instead, the run-time environment creates an instance of each class automatically when it's loaded, and it **registers the instance with a prototype manager**." (ET++ has such a run-time system.)

⚠️ **The main liability**: "each subclass of Prototype **must implement the `Clone` operation, which may be difficult**. For example, adding `Clone` is difficult when the classes under consideration **already exist**. Implementing `Clone` can be difficult when their internals include objects that **don't support copying or have circular references**."

## Implementation
**Language context first**: "Prototype is particularly useful with **static languages like C++**, where classes are not objects... It's **less important in languages like Smalltalk or Objective C** that provide what amounts to a prototype (i.e., a class object)... This pattern is **built into prototype-based languages like Self**, in which all object creation happens by cloning a prototype."

1. **Using a prototype manager.** "When the number of prototypes in a system isn't fixed... keep a **registry** of available prototypes... A prototype manager is an **associative store** that returns the prototype matching a given key... **This lets clients extend and take inventory on the system without writing code.**"
2. **Implementing the `Clone` operation** — "the hardest part of the Prototype pattern... particularly tricky when object structures contain **circular references**."
   - **Shallow vs. deep copy**: "Smalltalk provides an implementation of `copy` inherited by all subclasses of Object. C++ provides a copy constructor. **But these facilities don't solve the 'shallow copy versus deep copy' problem.**"
   - "A **shallow copy** is simple and often sufficient... The default copy constructor in C++ does a memberwise copy, which means **pointers will be shared** between the copy and the original. But cloning prototypes with complex structures usually requires a **deep copy**, because the clone and the original must be independent. **Cloning forces you to decide what if anything will be shared.**"
   - **A shortcut**: "If objects in the system provide `Save` and `Load` operations, then you can use them to provide a default implementation of `Clone` simply by **saving the object and loading it back immediately**."
3. **Initializing clones.** "You generally **can't pass these values in the `Clone` operation**, because their number will vary between classes of prototypes... **Passing parameters in the `Clone` operation precludes a uniform cloning interface.**" Use existing setters, or introduce an `Initialize` operation. "Beware of deep-copying `Clone` operations — **the copies may have to be deleted** (either explicitly or within `Initialize`) before you reinitialize them."

## Sample Code

A factory you never subclass — you re-parameterize it:

```cpp
class MazePrototypeFactory : public MazeFactory {
public:
    MazePrototypeFactory(Maze*, Wall*, Room*, Door*);

    virtual Maze* MakeMaze() const;
    virtual Room* MakeRoom(int) const;
    virtual Wall* MakeWall() const;
    virtual Door* MakeDoor(Room*, Room*) const;
private:
    Maze* _prototypeMaze;
    Room* _prototypeRoom;
    Wall* _prototypeWall;
    Door* _prototypeDoor;
};
```
```cpp
Wall* MazePrototypeFactory::MakeWall () const {
    return _prototypeWall->Clone();
}

Door* MazePrototypeFactory::MakeDoor (Room* r1, Room* r2) const {
    Door* door = _prototypeDoor->Clone();
    door->Initialize(r1, r2);
    return door;
}
```

Changing the maze type is now a change of *arguments*, not of *classes*:

```cpp
MazeGame game;
MazePrototypeFactory simpleMazeFactory(
    new Maze, new Wall, new Room, new Door
);
Maze* maze = game.CreateMaze(simpleMazeFactory);
```
```cpp
MazePrototypeFactory bombedMazeFactory(
    new Maze, new BombedWall, new RoomWithABomb, new Door
);
```

What a prototype must supply — `Clone`, a copy constructor, and often `Initialize`:

```cpp
class Door : public MapSite {
public:
    Door();
    Door(const Door&);

    virtual void Initialize(Room*, Room*);
    virtual Door* Clone() const;

    virtual void Enter();
    Room* OtherSideFrom(Room*);
private:
    Room* _room1;
    Room* _room2;
};

Door::Door (const Door& other) {
    _room1 = other._room1;
    _room2 = other._room2;
}

void Door::Initialize (Room* r1, Room* r2) {
    _room1 = r1;
    _room2 = r2;
}

Door* Door::Clone () const {
    return new Door(*this);
}
```
```cpp
BombedWall::BombedWall (const BombedWall& other) : Wall(other) {
    _bomb = other._bomb;
}

Wall* BombedWall::Clone () const {
    return new BombedWall(*this);
}
```
- **The covariance note**: "Although `BombedWall::Clone` **returns a `Wall*`**, its implementation returns a pointer to a new instance of a subclass... We define `Clone` like this in the base class to ensure that clients that clone the prototype don't have to know about their concrete subclasses. **Clients should never need to downcast the return value of `Clone`.**"

In Smalltalk, the whole thing collapses to `copy`:

```smalltalk
make: partName
    (partCatalog at: partName) copy
```

## Known Uses
- **Sketchpad** (Ivan Sutherland, 1963) — "Perhaps the first example of the Prototype pattern."
- **ThingLab** — "the first widely known application of the pattern in an object-oriented language, where users could **form a composite object and then promote it to a prototype** by installing it in a library of reusable objects."
- **Coplien** gives "a much more complete description," with C++ idioms, examples, and variations.
- **etgdb** — an ET++-based debugger front-end. "Etgdb does **not** have a set of `DebuggerAdaptor` classes hard-coded into it. Instead, it **reads the name of the adaptor to use from an environment variable**, looks for a prototype with the specified name in a global table, and then clones the prototype." (`GdbAdaptor` for GNU gdb, `SunDbxAdaptor` for Sun's dbx.)
- **Mode Composer** — its "interaction technique library" stores prototypes; "**any** interaction technique created by the Mode Composer can be used as a prototype by placing it in this library."
- **Unidraw** — the music editor example is based on it.

## Related Patterns
- "Prototype and **Abstract Factory** are **competing patterns** in some ways... They can also be used together, however. **An Abstract Factory might store a set of prototypes** from which to clone and return product objects."
- "Designs that make heavy use of the **Composite** and **Decorator** patterns often can benefit from Prototype as well."

## Connects To
- **Ch 3 (Creational Patterns)**: Prototype judged "probably the best" for the drawing editor — "it only requires implementing a `Clone` operation on each `Graphics` class... and `Clone` can be used for purposes other than pure instantiation (e.g., a **Duplicate** menu operation)."
- **Abstract Factory** (Prototype-based factories), **Factory Method** (which Prototype avoids subclassing for), **Composite**, **Decorator**, **Singleton** (a prototype manager is often one)
