# Factory Method
*Class Creational · Also Known As: **Virtual Constructor** · GoF p. 107*

## Intent
> **Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.**

## Motivation
A framework for applications presenting multiple documents. `Application` and `Document` are both abstract; clients subclass them (`DrawingApplication`, `DrawingDocument`). `Application` manages Documents and creates them "when the user selects Open or New from a menu."

**The dilemma, stated exactly**: "the `Application` class only knows **when** a new document should be created, not **what kind** of Document to create. This creates a dilemma: **The framework must instantiate classes, but it only knows about abstract classes, which it cannot instantiate.**"

The resolution: "It **encapsulates the knowledge of which Document subclass to create and moves this knowledge out of the framework**." Application subclasses redefine an abstract `CreateDocument` operation. "We call `CreateDocument` a factory method because it's responsible for '**manufacturing**' an object."

## Applicability
Use Factory Method when:
- "a class **can't anticipate** the class of objects it must create."
- "a class wants its **subclasses to specify** the objects it creates."
- "classes delegate responsibility to one of several helper subclasses, and you want to **localize the knowledge of which helper subclass is the delegate**."

## Participants
- **Product** (`Document`) — defines the interface of objects the factory method creates.
- **ConcreteProduct** (`MyDocument`) — implements the Product interface.
- **Creator** (`Application`) — declares the factory method returning a Product; "may also define a **default implementation** that returns a default ConcreteProduct"; may call the factory method to create a Product.
- **ConcreteCreator** (`MyApplication`) — overrides the factory method to return an instance of a ConcreteProduct.

## Consequences
"Factory methods **eliminate the need to bind application-specific classes into your code**. The code only deals with the Product interface; therefore it can work with any user-defined ConcreteProduct classes."

⚠️ **The cost**: "clients might have to **subclass the Creator class just to create a particular ConcreteProduct object**. Subclassing is fine when the client has to subclass the Creator class anyway, but otherwise **the client now must deal with another point of evolution**."

1. **Provides hooks for subclasses.** "Creating objects inside a class with a factory method is **always more flexible** than creating an object directly." Example: `Document::CreateFileDialog` gives a reasonable default that a subclass can override — "In this case the factory method is **not abstract** but provides a reasonable default implementation."
2. **Connects parallel class hierarchies.** "Parallel class hierarchies result when a class delegates some of its responsibilities to a separate class."
   - The example: interactively manipulable graphical figures. The manipulation state "is needed only during manipulation; therefore it needn't be kept in the figure object. Moreover, **different figures behave differently** — stretching a line figure might have the effect of moving an endpoint, whereas stretching a text figure may change its line spacing."
   - So `Figure::CreateManipulator` lets clients obtain the right `Manipulator`. And the hierarchies need not match one-for-one: "the Figure class may implement `CreateManipulator` to return a **default** Manipulator instance, and Figure subclasses may simply inherit that default. The Figure classes that do so need no corresponding Manipulator subclass — hence **the hierarchies are only partially parallel**."
   - "Notice how the factory method **defines the connection between the two class hierarchies. It localizes knowledge of which classes belong together.**"

## Implementation
1. **Two major varieties**:
   - **Abstract Creator, no implementation** — "requires subclasses to define an implementation, because there's no reasonable default. It gets around the dilemma of having to instantiate unforeseeable classes."
   - **Concrete Creator with a default** — "uses the factory method primarily for **flexibility**. It's following a rule that says, '**Create objects in a separate operation so that subclasses can override the way they're created.**'"
   - "It's also possible to have an abstract class that defines a default implementation, but this is less common."
2. **Parameterized factory methods** — one factory method creating multiple kinds of product, selected by a parameter.
   - **Unidraw's use**: reconstructing objects saved on disk. "When Unidraw saves an object to disk, it writes out the **class identifier** first and then its instance variables. When it reconstructs the object from disk, it reads the class identifier first... `Create` looks up the constructor for the corresponding class and uses it to instantiate the object. Last, `Create` calls the object's `Read` operation."
3. **Language-specific variants**:
   - **Smalltalk** — "often use a method that returns the **class** of the object to be instantiated... The result is an even **later binding** for the type of ConcreteProduct." An even more flexible approach: "store the class to be created as a **class variable** of Application. That way you don't have to subclass Application to vary the product."
   - **C++** — "Factory methods in C++ are always virtual functions and are often pure virtual. **Just be careful not to call factory methods in the Creator's constructor — the factory method in the ConcreteCreator won't be available yet.**" The fix is **lazy initialization**.
4. **Using templates to avoid subclassing** — "the client supplies just the product class — **no subclassing of Creator is required**."
5. **Naming conventions** — "It's good practice to use naming conventions that make it clear you're using factory methods. For example, **MacApp** always declares the abstract operation as `Class* DoMakeClass()`."

## Code Examples

Parameterized factory method, and a subclass that *rearranges* the mapping:

```cpp
class Creator {
public:
    virtual Product* Create(ProductId);
};

Product* Creator::Create (ProductId id) {
    if (id == MINE)  return new MyProduct;
    if (id == YOURS) return new YourProduct;
    // repeat for remaining products...
    return 0;
}
```
```cpp
Product* MyCreator::Create (ProductId id) {
    if (id == YOURS)  return new MyProduct;
    if (id == MINE)   return new YourProduct;
        // N.B.: switched YOURS and MINE
    if (id == THEIRS) return new TheirProduct;

    return Creator::Create(id); // called if all others fail
}
```
- **What it demonstrates**: "**Notice that the last thing this operation does is call `Create` on the parent class.** That's because `MyCreator::Create` handles only YOURS, MINE, and THEIRS differently than the parent class... Hence `MyCreator` **extends** the kinds of products created, and it **defers responsibility** for creating all but a few products to its parent."

Lazy initialization, avoiding the constructor trap:

```cpp
class Creator {
public:
    Product* GetProduct();
protected:
    virtual Product* CreateProduct();
private:
    Product* _product;
};

Product* Creator::GetProduct () {
    if (_product == 0) {
        _product = CreateProduct();
    }
    return _product;
}
```

Templates instead of subclasses:

```cpp
class Creator {
public:
    virtual Product* CreateProduct() = 0;
};

template <class TheProduct>
class StandardCreator : public Creator {
public:
    virtual Product* CreateProduct();
};

template <class TheProduct>
Product* StandardCreator<TheProduct>::CreateProduct () {
    return new TheProduct;
}
```
```cpp
StandardCreator<MyProduct> myCreator;
```

## Sample Code

```cpp
class MazeGame {
public:
    Maze* CreateMaze();

    // factory methods:
    virtual Maze* MakeMaze() const
        { return new Maze; }
    virtual Room* MakeRoom(int n) const
        { return new Room(n); }
    virtual Wall* MakeWall() const
        { return new Wall; }
    virtual Door* MakeDoor(Room* r1, Room* r2) const
        { return new Door(r1, r2); }
};
```
```cpp
Maze* MazeGame::CreateMaze () {
    Maze* aMaze = MakeMaze();
    Room* r1 = MakeRoom(1);
    Room* r2 = MakeRoom(2);
    Door* theDoor = MakeDoor(r1, r2);

    aMaze->AddRoom(r1);
    aMaze->AddRoom(r2);

    r1->SetSide(North, MakeWall());
    r1->SetSide(East, theDoor);
    r1->SetSide(South, MakeWall());
    r1->SetSide(West, MakeWall());

    r2->SetSide(North, MakeWall());
    r2->SetSide(East, MakeWall());
    r2->SetSide(South, MakeWall());
    r2->SetSide(West, theDoor);
}
```
```cpp
class BombedMazeGame : public MazeGame {
public:
    BombedMazeGame();

    virtual Wall* MakeWall() const
        { return new BombedWall; }
    virtual Room* MakeRoom(int n) const
        { return new RoomWithABomb(n); }
};
```
- **Compare with Abstract Factory**: the same maze variants, but the varying knowledge lives in **subclasses of the game** rather than in a **separate factory object** passed as a parameter. This is the two-ways-to-parameterize distinction from the chapter introduction.

## Known Uses
- "Factory methods **pervade toolkits and frameworks**." The document example is typical in **MacApp** and **ET++**; the manipulator example is from **Unidraw**.
- **Smalltalk-80 MVC** — a subtle one worth noting: "Class `View`... has a method `defaultController` that creates a controller, and **this might appear to be a factory method**. But subclasses of View specify the class of their default controller by defining `defaultControllerClass`... **So `defaultControllerClass` is the real factory method**, that is, the method that subclasses should override."
- **Smalltalk-80 `Behavior::parserClass`** — "This enables a class to use a **customized parser for its source code**. For example, a client can define a class `SQLParser` to analyze the source code of a class with embedded SQL statements."
- **Orbix ORB** (IONA) — "uses Factory Method to generate an appropriate type of **proxy** when an object requests a reference to a remote object. Factory Method makes it easy to replace the default proxy with one that uses **client-side caching**."

## Related Patterns
- **Abstract Factory** "is often implemented with factory methods."
- "Factory methods are usually called within **Template Methods**. In the document example above, `NewDocument` is a template method."
- "**Prototypes** don't require subclassing Creator. However, they often require an `Initialize` operation on the Product class... **Factory Method doesn't require such an operation.**"

## Connects To
- **Ch 3 (Creational Patterns)**: "Factory Method makes a design more customizable and only a little more complicated. Other design patterns require new classes, whereas Factory Method only requires a new **operation**."
- **Ch 1 (MVC)**: Factory Method specifies a view's default controller class.
- **Abstract Factory, Prototype, Template Method, Proxy**
