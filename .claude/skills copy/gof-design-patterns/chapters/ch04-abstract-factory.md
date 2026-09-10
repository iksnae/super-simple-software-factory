# Abstract Factory
*Object Creational · Also Known As: **Kit** · GoF p. 87*

## Intent
> **Provide an interface for creating families of related or dependent objects without specifying their concrete classes.**

## Motivation
A UI toolkit supporting Motif and Presentation Manager. "To be portable across look-and-feel standards, an application should not hard-code its widgets for a particular look and feel. **Instantiating look-and-feel-specific classes of widgets throughout the application makes it hard to change the look and feel later.**"

An abstract `WidgetFactory` declares an operation returning a new widget object per abstract widget class. "Clients call these operations to obtain widget instances, but **clients aren't aware of the concrete classes they're using**... In other words, clients only have to commit to an interface defined by an abstract class, not a particular concrete class."

And the second, less obvious benefit: "A `WidgetFactory` also **enforces dependencies** between the concrete widget classes. A Motif scroll bar should be used with a Motif button and a Motif text editor, and that constraint is enforced automatically as a consequence of using a `MotifWidgetFactory`."

## Applicability
Use Abstract Factory when:
- "a system should be **independent of how its products are created**, composed, and represented."
- "a system should be **configured with one of multiple families** of products."
- "a family of related product objects is designed to be used together, and you need to **enforce this constraint**."
- "you want to provide a **class library of products**, and you want to reveal just their interfaces, not their implementations."

## Participants
- **AbstractFactory** (`WidgetFactory`) — declares an interface for operations that create abstract product objects.
- **ConcreteFactory** (`MotifWidgetFactory`, `PMWidgetFactory`) — implements the operations to create concrete product objects.
- **AbstractProduct** (`Window`, `ScrollBar`) — declares an interface for a type of product object.
- **ConcreteProduct** (`MotifWindow`, `MotifScrollBar`) — defines a product object to be created by the corresponding concrete factory; implements the AbstractProduct interface.
- **Client** — uses only interfaces declared by AbstractFactory and AbstractProduct.

## Collaborations
- "Normally **a single instance of a ConcreteFactory class is created at run-time**. This concrete factory creates product objects having a particular implementation. To create different product objects, clients should use a different concrete factory."
- "AbstractFactory **defers creation of product objects to its ConcreteFactory subclass**."

## Consequences
1. **It isolates concrete classes.** "Product class names are isolated in the implementation of the concrete factory; **they do not appear in client code**."
2. **It makes exchanging product families easy.** "The class of a concrete factory appears **only once** in an application — that is, where it's instantiated... Because an abstract factory creates a complete family of products, **the whole product family changes at once**."
3. **It promotes consistency among products.** "When product objects in a family are designed to work together, it's important that an application use objects from only one family at a time."
4. **Supporting new kinds of products is difficult.** ⚠️ "**The AbstractFactory interface fixes the set of products that can be created.** Supporting new kinds of products requires extending the factory interface, which involves changing the AbstractFactory class **and all of its subclasses**."

## Implementation
1. **Factories as singletons.** "An application typically needs only one instance of a ConcreteFactory per product family. So it's usually best implemented as a **Singleton**."
2. **Creating the products.** The most common way is "to define a **factory method** for each product... While this implementation is simple, **it requires a new concrete factory subclass for each product family, even if the product families differ only slightly**."
   - **Prototype-based alternative**: "If many product families are possible, the concrete factory can be implemented using the **Prototype** pattern. The concrete factory is initialized with a prototypical instance of each product in the family, and it creates a new product by cloning its prototype. The Prototype-based approach **eliminates the need for a new concrete factory class for each new product family**."
   - **Class-based variation** (Smalltalk, Objective C — languages with first-class classes): "You can think of a class in these languages as a **degenerate factory that creates only one kind of product**." Store the classes rather than prototypes. "This approach takes advantage of language characteristics, whereas the pure Prototype-based approach is language-independent."
3. **Defining extensible factories.** Replace one operation per product with a single `Make` operation taking a parameter identifying the kind of object. "A more flexible but **less safe** design."
   - The unavoidable cost: "**All products are returned to the client with the same abstract interface** as given by the return type. The client will not be able to differentiate or make safe assumptions about the class of a product... Although the client could perform a downcast, that's not always feasible or safe, because the downcast can fail. **This is the classic trade-off for a highly flexible and extensible interface.**"

## Sample Code

```cpp
class MazeFactory {
public:
    MazeFactory();

    virtual Maze* MakeMaze() const
        { return new Maze; }
    virtual Wall* MakeWall() const
        { return new Wall; }
    virtual Room* MakeRoom(int n) const
        { return new Room(n); }
    virtual Door* MakeDoor(Room* r1, Room* r2) const
        { return new Door(r1, r2); }
};
```

`CreateMaze` now takes the factory as a parameter — every `new` replaced by a factory call:

```cpp
Maze* MazeGame::CreateMaze (MazeFactory& factory) {
    Maze* aMaze = factory.MakeMaze();
    Room* r1 = factory.MakeRoom(1);
    Room* r2 = factory.MakeRoom(2);
    Door* aDoor = factory.MakeDoor(r1, r2);

    aMaze->AddRoom(r1);
    aMaze->AddRoom(r2);

    r1->SetSide(North, factory.MakeWall());
    r1->SetSide(East, aDoor);
    r1->SetSide(South, factory.MakeWall());
    r1->SetSide(West, factory.MakeWall());

    r2->SetSide(North, factory.MakeWall());
    r2->SetSide(East, factory.MakeWall());
    r2->SetSide(South, factory.MakeWall());
    r2->SetSide(West, aDoor);

    return aMaze;
}
```

Two families, each overriding only what differs:

```cpp
class EnchantedMazeFactory : public MazeFactory {
public:
    EnchantedMazeFactory();

    virtual Room* MakeRoom(int n) const
        { return new EnchantedRoom(n, CastSpell()); }
    virtual Door* MakeDoor(Room* r1, Room* r2) const
        { return new DoorNeedingSpell(r1, r2); }
protected:
    Spell* CastSpell() const;
};
```
```cpp
Wall* BombedMazeFactory::MakeWall () const {
    return new BombedWall;
}

Room* BombedMazeFactory::MakeRoom(int n) const {
    return new RoomWithABomb(n);
}
```
```cpp
MazeGame game;
BombedMazeFactory factory;
game.CreateMaze(factory);
```

**Two notes GoF flags about this implementation**: "Notice that the `MazeFactory` is just a **collection of factory methods**. This is the most common way to implement the Abstract Factory pattern. Also note that **`MazeFactory` is not an abstract class**; thus it acts as **both the AbstractFactory and the ConcreteFactory**. This is another common implementation for simple applications."

**On downcasting**: "If `RoomWithABomb` had to access a subclass-specific member of `BombedWall`, then it would have to cast a reference to its walls from `Wall*` to `BombedWall*`. **This downcasting is safe as long as the argument is in fact a `BombedWall`, which is guaranteed to be true if walls are built solely with a `BombedMazeFactory`.**" And for dynamic languages: "Using Abstract Factory to build walls helps prevent these run-time errors by ensuring that only certain kinds of walls can be created."

The Smalltalk class-based version, where a new family is a different dictionary rather than a new subclass:

```smalltalk
make: partName
    (partCatalog at: partName) new
```
```smalltalk
createMazeFactory
    ^ (MazeFactory new
        addPart: Wall named: #wall;
        addPart: Room named: #room;
        addPart: Door named: #door;
        yourself)
```
```smalltalk
createMazeFactory
    ^ (MazeFactory new
        addPart: Wall named: #wall;
        addPart: EnchantedRoom named: #room;
        addPart: DoorNeedingSpell named: #door;
        yourself)
```

## Known Uses
- **InterViews** uses the **"Kit" suffix** to denote AbstractFactory classes — `WidgetKit` and `DialogKit` for look-and-feel-specific UI objects, plus a `LayoutKit` that "generates different composition objects depending on the layout desired. For example, a layout that is conceptually horizontal may require different composition objects depending on the document's orientation (portrait or landscape)."
- **ET++** uses it for portability across window systems (X Windows, SunView). The `WindowSystem` abstract base class declares `MakeWindow`, `MakeFont`, `MakeColor`; "At run-time, ET++ creates an instance of a concrete `WindowSystem` subclass that creates concrete system resource objects."

## Related Patterns
- Often implemented with **Factory Method**, but can also be implemented using **Prototype**.
- "A concrete factory is often a **singleton**."

## Connects To
- **Ch 2 (Case Study)**: `GUIFactory` for look-and-feel independence — and why it *fails* for window systems (use **Bridge** there).
- **Ch 3 (Creational Patterns)**: "Abstract Factory doesn't offer much of an improvement [over Factory Method]... only if there were already a GraphicsFactory class hierarchy."
- **Factory Method, Prototype, Singleton, Builder**
