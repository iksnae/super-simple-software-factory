# Singleton
*Object Creational · GoF p. 127*

## Intent
> **Ensure a class only has one instance, and provide a global point of access to it.**

## Motivation
"Although there can be many printers in a system, there should be only one **printer spooler**. There should be only one **file system** and one **window manager**. A digital filter will have one **A/D converter**. An accounting system will be dedicated to serving one company."

The key insight about why a global variable is insufficient: "**A global variable makes an object accessible, but it doesn't keep you from instantiating multiple objects.**"

So: "make the class itself responsible for keeping track of its sole instance. The class can ensure that no other instance can be created (**by intercepting requests to create new objects**), and it can provide a way to access the instance."

## Applicability
Use Singleton when:
- "there must be **exactly one instance** of a class, and it must be accessible to clients from a **well-known access point**."
- "when the sole instance should be **extensible by subclassing**, and clients should be able to use an extended instance **without modifying their code**."

## Participants
- **Singleton** — "defines an `Instance` operation that lets clients access its unique instance. **`Instance` is a class operation** (that is, a class method in Smalltalk and a static member function in C++)"; may be responsible for creating its own unique instance.

## Collaborations
- "Clients access a Singleton instance **solely** through Singleton's `Instance` operation."

## Consequences
1. **Controlled access to sole instance.** "Because the Singleton class encapsulates its sole instance, it can have **strict control over how and when** clients access it."
2. **Reduced name space.** "An improvement over global variables. It avoids polluting the name space."
3. **Permits refinement of operations and representation.** "The Singleton class **may be subclassed**, and it's easy to configure an application with an instance of this extended class... **at run-time**."
4. **Permits a variable number of instances.** "The pattern makes it easy to **change your mind and allow more than one instance**... **Only the operation that grants access to the Singleton instance needs to change.**"
5. **More flexible than class operations.** "Another way to package a singleton's functionality is to use class operations... But both of these language techniques make it **hard to change a design to allow more than one instance**. Moreover, **static member functions in C++ are never virtual, so subclasses can't override them polymorphically**."

## Implementation

### 1. Ensuring a unique instance

```cpp
class Singleton {
public:
    static Singleton* Instance();
protected:
    Singleton();
private:
    static Singleton* _instance;
};
```
```cpp
Singleton* Singleton::_instance = 0;

Singleton* Singleton::Instance () {
    if (_instance == 0) {
        _instance = new Singleton;
    }
    return _instance;
}
```

- **Lazy initialization** — "the value it returns isn't created and stored until it's first accessed."
- **The protected constructor is the enforcement**: "**A client that tries to instantiate `Singleton` directly will get an error at compile-time.** This ensures that only one instance can ever get created."
- **And the pointer enables subclassing**: "since `_instance` is a **pointer** to a Singleton object, the `Instance` member function can **assign a pointer to a subclass** of Singleton to this variable."

**Why not just a global or static object?** GoF gives three reasons plus a liability:
- (a) "We **can't guarantee that only one instance** of a static object will ever be declared."
- (b) "We might **not have enough information to instantiate every singleton at static initialization time**. A singleton might require values that are computed later in the program's execution."
- (c) "**C++ doesn't define the order in which constructors for global objects are called across translation units.** This means that **no dependencies can exist between singletons**; if any do, then errors are inevitable."
- Plus: "it forces **all singletons to be created whether they are used or not**. Using a static member function avoids all of these problems."

**Smalltalk** — override `new` to prevent instantiation:

```smalltalk
new
    self error: 'cannot create new object'

default
    SoleInstance isNil ifTrue: [SoleInstance := super new].
    ^ SoleInstance
```

### 2. Subclassing the Singleton class
"The main issue is not so much defining the subclass but **installing its unique instance** so that clients will be able to use it."

Three approaches, each with a stated limit:

| Approach | How | Limitation |
|---|---|---|
| **Conditional in `Instance`** | Decide which singleton in the parent's `Instance` operation (e.g. from an environment variable) | "**hard-wires the set of possible Singleton classes**" |
| **Move `Instance` to the subclass** | Take the implementation out of the parent and put it in the subclass; "lets a C++ programmer decide the class of singleton at **link-time**... but keeps it hidden from the clients" | "fixes the choice of singleton class at link-time, which makes it **hard to choose the singleton class at run-time**" |
| **Registry of singletons** ✅ | "the Singleton classes can **register their singleton instance by name** in a well-known registry" | Requires that instances get created in order to register |

"**Neither** [of the first two] **approach is flexible enough in all cases.**"

```cpp
class Singleton {
public:
    static void Register(const char* name, Singleton*);
    static Singleton* Instance();
protected:
    static Singleton* Lookup(const char* name);
private:
    static Singleton* _instance;
    static List<NameSingletonPair>* _registry;
};
```
```cpp
Singleton* Singleton::Instance () {
    if (_instance == 0) {
        const char* singletonName = getenv("SINGLETON");
        // user or environment supplies this at startup

        _instance = Lookup(singletonName);
        // Lookup returns 0 if there's no such singleton
    }
    return _instance;
}
```
- **This inverts the responsibility**: "**No longer is the Singleton class responsible for creating the singleton.** Instead, its primary responsibility is to make the singleton object of choice **accessible** in the system."

**The registration bootstrap problem**, stated with unusual candour: registering in the constructor means "the constructor won't get called unless someone instantiates the class, **which echoes the problem the Singleton pattern is trying to solve!**" The C++ workaround is a static instance:

```cpp
static MySingleton theSingleton;
```
"The static object approach still has a potential drawback — namely that **instances of all possible Singleton subclasses must be created, or else they won't get registered**."

## Sample Code

```cpp
class MazeFactory {
public:
    static MazeFactory* Instance();

    // existing interface goes here
protected:
    MazeFactory();
private:
    static MazeFactory* _instance;
};
```
```cpp
MazeFactory* MazeFactory::_instance = 0;

MazeFactory* MazeFactory::Instance () {
    if (_instance == 0) {
        _instance = new MazeFactory;
    }
    return _instance;
}
```

Selecting the subclass by environment variable:

```cpp
MazeFactory* MazeFactory::Instance () {
    if (_instance == 0) {
        const char* mazeStyle = getenv("MAZESTYLE");

        if (strcmp(mazeStyle, "bombed") == 0) {
            _instance = new BombedMazeFactory;
        } else if (strcmp(mazeStyle, "enchanted") == 0) {
            _instance = new EnchantedMazeFactory;
        // ... other possible subclasses
        } else { // default
            _instance = new MazeFactory;
        }
    }
    return _instance;
}
```
- ⚠️ "Note that **`Instance` must be modified whenever you define a new subclass** of `MazeFactory`. That might not be a problem in this application, **but it might be for abstract factories defined in a framework**." The remedy: the registry approach, plus dynamic linking to "keep the application from having to load all the subclasses that are not used."

**Why here at all**: "the Maze application needs only one instance of a maze factory, and that instance should be available to code that builds any part of the maze... **we make the maze object globally accessible without resorting to global variables**."

## Known Uses
- **Smalltalk-80** — "the set of changes to the code, which is `ChangeSet current`."
- **Smalltalk metaclasses** — "A more subtle example... A metaclass is the class of a class, and **each metaclass has one instance**. Metaclasses do not have names (except indirectly through their sole instance), but they keep track of their sole instance and will not normally create another."
- **InterViews** — `Session` and `WidgetKit`. "`Session` defines the application's main event dispatch loop, stores the user's database of stylistic preferences, and manages connections to one or more physical displays." `WidgetKit::instance()` "determines the particular `WidgetKit` subclass that's instantiated based on an environment variable that `Session` defines."

## Related Patterns
- "Many patterns can be implemented using the Singleton pattern. See **Abstract Factory**, **Builder**, and **Prototype**."

## Connects To
- **Ch 2 (Case Study)**: "There's even a design pattern, Singleton, for managing well-known, one-of-a-kind objects like this" — the `guiFactory` variable.
- **Ch 3 (Creational Patterns)**: Singleton "can ensure there's only one maze per game and that all game objects have ready access to it — **without resorting to global variables or functions**."
- **Abstract Factory** (concrete factories are often singletons), **Prototype** (a prototype manager is often one)
