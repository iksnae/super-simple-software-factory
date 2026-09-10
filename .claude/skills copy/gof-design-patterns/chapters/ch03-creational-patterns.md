# Chapter 3: Creational Patterns *(category introduction and discussion)*

## Core Idea
Creational patterns "abstract the instantiation process," making a system "independent of how its objects are created, composed, and represented" — and they all do it by **removing explicit references to concrete classes from the code that needs to instantiate them**.

## Frameworks Introduced
- **Class vs. object creational**: "A **class** creational pattern uses **inheritance** to vary the class that's instantiated, whereas an **object** creational pattern will **delegate instantiation to another object**."
- **The two recurring themes**: "First, they all **encapsulate knowledge about which concrete classes the system uses**. Second, they **hide how instances of these classes are created and put together**. All the system at large knows about the objects is their interfaces as defined by abstract classes."
- **Why they matter more over time**: "Creational patterns become important as systems evolve to depend more on object composition than class inheritance. As that happens, emphasis shifts away from hard-coding a fixed set of behaviors toward defining a smaller set of fundamental behaviors that can be composed into any number of more complex ones. Thus **creating objects with particular behaviors requires more than simply instantiating a class**."
- **Two ways to parameterize a system by the classes it creates**:
  1. **Subclass the creator** → **Factory Method**. "The main drawback of this approach is that **it can require creating a new subclass just to change the class of the product. Such changes can cascade.** For example, when the product creator is itself created by a factory method, then you have to override its creator as well."
  2. **Compose with a factory object** → **Abstract Factory**, **Builder**, **Prototype**. "All three involve creating a new 'factory object' whose responsibility is to create product objects."
     - **Abstract Factory** — "the factory object producing objects of **several classes**."
     - **Builder** — "the factory object **building a complex product incrementally** using a correspondingly complex protocol."
     - **Prototype** — "the factory object building a product by **copying a prototype object**. In this case, **the factory object and the prototype are the same object**, because the prototype is responsible for returning the product."

## Key Concepts
- **Competitors and complements**: "there are cases when either Prototype or Abstract Factory could be used profitably. At other times they are complementary: **Builder can use one of the other patterns** to implement which components get built. **Prototype can use Singleton** in its implementation."
- **Flexibility, not brevity**: "The creational patterns show how to make this design **more flexible, not necessarily smaller**."
- **The evolution path**: "Often, designs **start out using Factory Method and evolve toward the other creational patterns** as the designer discovers where more flexibility is needed. Knowing many design patterns gives you more choices when trading off one design criterion against another."
- **When Factory Method isn't needed**: "People often use Factory Method as the standard way to create objects, but **it isn't necessary when the class that's instantiated never changes** or when instantiation takes place in an operation that subclasses can easily override, such as an initialization operation."

## Code Examples

**The shared maze example.** A maze is a set of rooms; a room knows its neighbors, which may be another room, a wall, or a door.

```cpp
enum Direction {North, South, East, West};

class MapSite {
public:
    virtual void Enter() = 0;
};
```
`Enter`'s "meaning depends on what you're entering. If you enter a room, then your location changes. If you try to enter a door, then one of two things happen: If the door is open, you go into the next room. **If the door is closed, then you hurt your nose.**"

```cpp
class Room : public MapSite {
public:
    Room(int roomNo);
    MapSite* GetSide(Direction) const;
    void SetSide(Direction, MapSite*);
    virtual void Enter();
private:
    MapSite* _sides[4];
    int _roomNumber;
};

class Wall : public MapSite {
public:
    Wall();
    virtual void Enter();
};

class Door : public MapSite {
public:
    Door(Room* = 0, Room* = 0);
    virtual void Enter();
    Room* OtherSideFrom(Room*);
private:
    Room* _room1;
    Room* _room2;
    bool _isOpen;
};

class Maze {
public:
    Maze();
    void AddRoom(Room*);
    Room* RoomNo(int) const;
};
```

**The inflexible baseline** — the member function every creational pattern will improve:

```cpp
Maze* MazeGame::CreateMaze () {
    Maze* aMaze = new Maze;
    Room* r1 = new Room(1);
    Room* r2 = new Room(2);
    Door* theDoor = new Door(r1, r2);

    aMaze->AddRoom(r1);
    aMaze->AddRoom(r2);

    r1->SetSide(North, new Wall);
    r1->SetSide(East, theDoor);
    r1->SetSide(South, new Wall);
    r1->SetSide(West, new Wall);

    r2->SetSide(North, new Wall);
    r2->SetSide(East, new Wall);
    r2->SetSide(South, new Wall);
    r2->SetSide(West, theDoor);

    return aMaze;
}
```
- **What it demonstrates**: "**The real problem with this member function isn't its size but its inflexibility.** It hard-codes the maze layout. Changing the layout means changing this member function, either by overriding it — which means reimplementing the whole thing — or by changing parts of it — which is error-prone and doesn't promote reuse."

**The test case**: an *enchanted* maze game with `DoorNeedingSpell` ("a door that can be locked and opened subsequently only with a spell") and `EnchantedRoom` ("a room that can have unconventional items in it, like magic keys or spells"). "In this case, **the biggest barrier to change lies in hard-coding the classes that get instantiated**."

## Reference Tables

How each pattern changes `CreateMaze`:

| If `CreateMaze`… | You change classes by… | Pattern |
|---|---|---|
| calls **virtual functions** instead of constructor calls | subclassing `MazeGame` and redefining those virtual functions | **Factory Method** |
| is **passed an object as a parameter** to use for creating rooms, walls, and doors | passing a different parameter | **Abstract Factory** |
| is **passed an object that can create a maze in its entirety**, with operations for adding rooms, doors, and walls | using inheritance to change parts of the maze or the way it's built | **Builder** |
| is **parameterized by prototypical** room, door, and wall objects that it copies | replacing those prototypical objects with different ones | **Prototype** |
| — | ensuring one maze per game with ready access, "without resorting to global variables or functions" | **Singleton** |

## Worked Example
**The drawing-editor comparison — the same problem solved three ways, and the ranking.**

Parameterizing a `GraphicTool` by the class of `Graphic` it produces:

| Approach | What you build | Assessment |
|---|---|---|
| **Factory Method** | "a subclass of `GraphicTool` will be created for each subclass of `Graphic` in the palette. `GraphicTool` will have a `NewGraphic` operation that each subclass will redefine." | "**easiest to use at first**. It's easy to define a new subclass... and the instances of `GraphicTool` are created only when the palette is defined. The main disadvantage here is that **`GraphicTool` subclasses proliferate, and none of them does very much**." |
| **Abstract Factory** | "a class hierarchy of `GraphicsFactories`, one for each `Graphic` subclass. Each factory creates just one product: `CircleFactory` will create `Circle`s, `LineFactory` will create `Line`s." | "**doesn't offer much of an improvement**, because it requires an equally large `GraphicsFactory` class hierarchy. Abstract Factory would be preferable to Factory Method **only if there were already a `GraphicsFactory` class hierarchy** — either because the compiler provides it automatically (as in Smalltalk or Objective C) or because it's needed in another part of the system." |
| **Prototype** | "each subclass of `Graphics` will implement the `Clone` operation, and a `GraphicTool` will be parameterized with a prototype of the `Graphic` it creates." | "**probably the best** for the drawing editor framework, because it only requires implementing a `Clone` operation on each `Graphics` class. That **reduces the number of classes**, and `Clone` can be used for purposes other than pure instantiation (e.g., a **Duplicate** menu operation)." |

The generalizable lesson: **Abstract Factory is only cheap if the factory hierarchy already exists for another reason.** Otherwise you have merely relocated the class proliferation from tools to factories.

And the trade-off summary: "**Factory Method makes a design more customizable and only a little more complicated.** Other design patterns require new classes, whereas Factory Method only requires a new **operation**... Designs that use Abstract Factory, Prototype, or Builder are **even more flexible than those that use Factory Method, but they're also more complex**."

## Key Takeaways
1. All five encapsulate which concrete classes are used and how instances get created and assembled.
2. Class creational patterns vary the instantiated class by inheritance; object creational ones delegate to another object.
3. Factory Method costs one operation; the others cost new classes — and buy more flexibility.
4. Factory Method's subclass requirement can cascade when the creator is itself created by a factory method.
5. Abstract Factory produces families; Builder assembles incrementally; Prototype copies — and in Prototype the factory and the prototype are the same object.
6. Prefer Prototype when `Clone` is cheap to add and has independent uses; prefer Abstract Factory when the factory hierarchy already exists.
7. Start with Factory Method and evolve toward the others as real flexibility needs appear.

## Connects To
- **Abstract Factory, Builder, Factory Method, Prototype, Singleton**: the five patterns, all illustrated with the maze.
- **Ch 1**: "Creating an object by specifying a class explicitly" is cause of redesign #1.
- **Ch 2 (Case Study)**: Abstract Factory for look-and-feel independence.
- **Ch 4–5**: the structural and behavioral category chapters.
