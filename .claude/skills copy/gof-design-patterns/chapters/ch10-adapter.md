# Adapter
*Class **and** Object Structural · Also Known As: **Wrapper** · GoF p. 139*

## Intent
> **Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.**

## Motivation
"Sometimes a toolkit class that's designed for reuse isn't reusable **only because its interface doesn't match** the domain-specific interface an application requires."

A drawing editor with an abstract `Shape` class. `LineShape` and `PolygonShape` are easy; "a `TextShape` subclass that can display and edit text is considerably more difficult to implement, since even basic text editing involves complicated screen update and buffer management." Meanwhile a toolkit already has a sophisticated `TextView`.

**Why not just change `TextView`?** "that isn't an option unless we have the toolkit's source code. **Even if we did, it wouldn't make sense to change `TextView`; the toolkit shouldn't have to adopt domain-specific interfaces just to make one application work.**"

Two ways to adapt, which are the two versions of the pattern: "(1) by **inheriting** `Shape`'s interface and `TextView`'s implementation or (2) by **composing** a `TextView` instance within a `TextShape`."

**Adapters often add what's missing**: "The user should be able to 'drag' every `Shape` object to a new location interactively, but `TextView` isn't designed to do that. `TextShape` can add this missing functionality by implementing `Shape`'s `CreateManipulator` operation."

## Applicability
Use Adapter when:
- "you want to use an existing class, and **its interface does not match the one you need**."
- "you want to create a **reusable class that cooperates with unrelated or unforeseen classes**."
- **(object adapter only)** "you need to use several existing subclasses, but it's impractical to adapt their interface by subclassing every one. An object adapter can adapt the interface of its parent class."

## Participants
- **Target** (`Shape`) — defines the domain-specific interface that Client uses.
- **Client** (`DrawingEditor`) — collaborates with objects conforming to the Target interface.
- **Adaptee** (`TextView`) — defines an existing interface that needs adapting.
- **Adapter** (`TextShape`) — adapts the interface of Adaptee to the Target interface.

## Collaborations
- "Clients call operations on an Adapter instance. In turn, the adapter calls Adaptee operations that carry out the request."

## Consequences

| | **Class adapter** (multiple inheritance) | **Object adapter** (composition) |
|---|---|---|
| Adaptee coverage | "commits to a **concrete Adaptee class**. As a consequence, a class adapter **won't work when we want to adapt a class and all its subclasses**" | "lets a **single Adapter work with many Adaptees** — the Adaptee itself and all of its subclasses. The Adapter can also **add functionality to all Adaptees at once**" |
| Overriding Adaptee behavior | "lets Adapter **override** some of Adaptee's behavior, since Adapter is a subclass of Adaptee" | "makes it **harder to override** Adaptee behavior. It will require subclassing Adaptee and making Adapter refer to the subclass" |
| Indirection | "introduces only **one object**, and no additional pointer indirection is needed" | one extra object and one extra hop |

Other issues:
1. **How much adapting does Adapter do?** "There is a **spectrum** of possible work, from simple interface conversion — for example, changing the names of operations — to **supporting an entirely different set of operations**. The amount of work Adapter does depends on how similar the Target interface is to Adaptee's."
2. **Pluggable adapters.** "A class is more reusable when you **minimize the assumptions other classes must make to use it**. By building interface adaptation into a class, you **eliminate the assumption that other classes see the same interface**." (ObjectWorks\Smalltalk's term.)
   - The `TreeDisplay` example: "in a directory hierarchy, children might be accessed with a `GetSubdirectories` operation, whereas in an inheritance hierarchy, the corresponding operation might be called `GetSubclasses`. A reusable `TreeDisplay` widget must be able to display both kinds of hierarchies even if they use different interfaces."
3. **Two-way adapters to provide transparency.** "A potential problem with adapters is that **they aren't transparent to all clients**. An adapted object no longer conforms to the Adaptee interface, so it can't be used as is wherever an Adaptee object can."
   - The Unidraw/QOCA example: Unidraw has `StateVariable`, QOCA has `ConstraintVariable`, and each system must see the other's. The solution is `ConstraintStateVariable`, "a subclass of **both**... **Multiple inheritance is a viable solution in this case because the interfaces of the adapted classes are substantially different.** The two-way class adapter conforms to both of the adapted classes and can work in either system."

## Implementation
1. **Class adapters in C++** — "Adapter would inherit **publicly from Target and privately from Adaptee**. Thus Adapter would be a **subtype of Target but not of Adaptee**."
2. **Pluggable adapters.** The common first step for all three approaches: "**find a 'narrow' interface for Adaptee**, that is, the smallest subset of operations that lets us do the adaptation. A narrow interface consisting of only a couple of operations is easier to adapt than an interface with dozens."

| Approach | How | Notes |
|---|---|---|
| **(a) Abstract operations** | Define abstract operations for the narrow interface in `TreeDisplay`; subclasses implement them (`DirectoryTreeDisplay`) | Requires a subclass per adaptation |
| **(b) Delegate objects** | `TreeDisplay` forwards requests to a delegate; "can use a different adaptation strategy by **substituting a different delegate**" | In dynamic languages "this approach only requires an interface for registering the delegate." **NEXTSTEP uses this approach heavily to reduce subclassing.** In C++, put the narrow interface in an abstract `TreeAccessorDelegate` and mix it in — "**easier than introducing a new `TreeDisplay` subclass** and implementing its operations individually" |
| **(c) Parameterized adapters** | Parameterize the adapter with **blocks**, one per request | "The block construct supports **adaptation without subclassing**" |

```smalltalk
directoryDisplay :=
    (TreeDisplay on: treeRoot)
        getChildrenBlock: [:node | node getSubdirectories]
        createGraphicNodeBlock: [:node | node createGraphicNode].
```

## Sample Code

The mismatch: `Shape` uses a bounding box of opposing corners; `TextView` uses origin, height, and width. And `Shape` has `CreateManipulator`, which "`TextView` has no equivalent operation" for.

```cpp
class Shape {
public:
    Shape();
    virtual void BoundingBox(Point& bottomLeft, Point& topRight) const;
    virtual Manipulator* CreateManipulator() const;
};

class TextView {
public:
    TextView();
    void GetOrigin(Coord& x, Coord& y) const;
    void GetExtent(Coord& width, Coord& height) const;
    virtual bool IsEmpty() const;
};
```

**Class adapter** — "the key to class adapters is to use **one inheritance branch to inherit the interface and another branch to inherit the implementation**."

```cpp
class TextShape : public Shape, private TextView {
public:
    TextShape();

    virtual void BoundingBox(Point& bottomLeft, Point& topRight) const;
    virtual bool IsEmpty() const;
    virtual Manipulator* CreateManipulator() const;
};

void TextShape::BoundingBox (Point& bottomLeft, Point& topRight) const {
    Coord bottom, left, width, height;

    GetOrigin(bottom, left);
    GetExtent(width, height);

    bottomLeft = Point(bottom, left);
    topRight = Point(bottom + height, left + width);
}

bool TextShape::IsEmpty () const {
    return TextView::IsEmpty();
}

Manipulator* TextShape::CreateManipulator () const {
    return new TextManipulator(this);
}
```
- Three kinds of adapting in one class: `BoundingBox` **converts**, `IsEmpty` **forwards directly**, `CreateManipulator` is written **from scratch** because the Adaptee has nothing to offer. (Footnote: "`CreateManipulator` is an example of a **Factory Method**.")

**Object adapter** — same operations, a pointer instead of a base class:

```cpp
class TextShape : public Shape {
public:
    TextShape(TextView*);

    virtual void BoundingBox(Point& bottomLeft, Point& topRight) const;
    virtual bool IsEmpty() const;
    virtual Manipulator* CreateManipulator() const;
private:
    TextView* _text;
};

TextShape::TextShape (TextView* t) {
    _text = t;
}

void TextShape::BoundingBox (Point& bottomLeft, Point& topRight) const {
    Coord bottom, left, width, height;

    _text->GetOrigin(bottom, left);
    _text->GetExtent(width, height);

    bottomLeft = Point(bottom, left);
    topRight = Point(bottom + height, left + width);
}

bool TextShape::IsEmpty () const {
    return _text->IsEmpty();
}
```
- **The verdict**: "The object adapter requires a little more effort to write, but **it's more flexible**. For example, the object adapter version of `TextShape` will work equally well with **subclasses** of `TextView` — the client simply passes an instance of a `TextView` subclass to the constructor."

## Known Uses
- **ET++Draw** — reuses ET++'s text editing classes via a `TextShape` adapter (the Motivation example).
- **InterViews 2.6** — `Interactor` (scroll bars, buttons, menus) and `Graphic` (lines, circles, polygons, splines) "have graphical appearances, but they have different interfaces and implementations (**they share no common parent class**)." The object adapter `GraphicBlock`, a subclass of `Interactor` containing a `Graphic`, "lets a `Graphic` instance be **displayed, scrolled, and zoomed** within an Interactor structure."
- **ObjectWorks\Smalltalk `PluggableAdaptor`** — `ValueModel` defines a `value`/`value:` interface, but "application writers access the value with more domain-specific names like `width` and `width:`, and they shouldn't have to subclass `ValueModel`." `PluggableAdaptor` "can be parameterized with **blocks** for getting and setting the desired value... **also lets you pass in the selector names directly** for syntactic convenience. It converts these selectors into the corresponding blocks automatically."
- **ObjectWorks\Smalltalk `TableAdaptor`** — "can adapt a sequence of objects to a tabular presentation. The table displays one object per row."
- **NeXT AppKit `NXBrowser`** — "uses a delegate object for accessing and adapting the data."
- **Meyer's "Marriage of Convenience"** — "a form of class adapter... how a `FixedStack` class adapts the implementation of an `Array` class to the interface of a `Stack` class."

## Related Patterns
- **Bridge** "has a structure similar to an object adapter, but Bridge has a **different intent**: it is meant to **separate an interface from its implementation** so that they can be varied easily and independently. **An adapter is meant to change the interface of an existing object.**"
- **Decorator** "enhances another object **without changing its interface**. A decorator is thus **more transparent** to the application than an adapter is. As a consequence, Decorator supports **recursive composition**, which isn't possible with pure adapters."
- **Proxy** "defines a representative or surrogate for another object and **does not change its interface**."

## Connects To
- **Ch 4 (Structural Patterns)**: "A class adapter accomplishes this by inheriting **privately** from an adaptee class."
- **Ch 1**: cause of redesign #8 — inability to alter classes conveniently.
- **Bridge, Decorator, Proxy, Facade** (the four patterns most often confused with it)
