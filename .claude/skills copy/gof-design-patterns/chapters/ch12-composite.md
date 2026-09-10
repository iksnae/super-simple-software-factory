# Composite
*Object Structural · GoF p. 163*

## Intent
> **Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.**

## Motivation
Drawing editors and schematic capture systems let users group components into larger components, recursively.

**The problem with the naive design**: "Code that uses these classes must **treat primitive and container objects differently, even if most of the time the user treats them identically**. Having to distinguish these objects makes the application more complex."

"The key to the Composite pattern is **an abstract class that represents both primitives and their containers**." `Graphic` declares `Draw` plus "operations that all composite objects share, such as operations for accessing and managing its children." `Line`, `Rectangle`, and `Text` are primitives — "Since primitive graphics have no child graphics, **none of these subclasses implements child-related operations**." And `Picture` "implements `Draw` to call `Draw` on its children... **Because the `Picture` interface conforms to the `Graphic` interface, `Picture` objects can compose other `Picture`s recursively.**"

## Applicability
Use Composite when:
- "you want to represent **part-whole hierarchies** of objects."
- "you want clients to be able to **ignore the difference** between compositions of objects and individual objects."

## Participants
- **Component** (`Graphic`) — declares the interface for objects in the composition; implements default behavior common to all classes; declares an interface for accessing and managing children; *(optional)* defines an interface for accessing a component's **parent**.
- **Leaf** (`Rectangle`, `Line`, `Text`) — represents leaf objects; **has no children**.
- **Composite** (`Picture`) — defines behavior for components having children; stores child components; implements child-related operations.
- **Client** — manipulates objects in the composition through the Component interface.

## Collaborations
- "If the recipient is a **Leaf**, then the request is handled **directly**. If the recipient is a **Composite**, then it usually **forwards requests to its child components**, possibly performing additional operations before and/or after forwarding."

## Consequences
- **Defines class hierarchies of primitive and composite objects.** "Wherever client code expects a primitive object, it can also take a composite object."
- **Makes the client simple.** "Clients normally don't know (and shouldn't care) whether they're dealing with a leaf or a composite... it avoids having to write **tag-and-case-statement-style functions** over the classes that define the composition."
- **Makes it easier to add new kinds of components.** "Newly defined Composite or Leaf subclasses work **automatically** with existing structures and client code."
- ⚠️ **Can make your design overly general.** "The disadvantage of making it easy to add new components is that it makes it **harder to restrict** the components of a composite. Sometimes you want a composite to have only certain components. With Composite, **you can't rely on the type system to enforce those constraints for you. You'll have to use run-time checks instead.**"

## Implementation
1. **Explicit parent references.** "simplifies moving up the structure and deleting a component. Parent references also help support the **Chain of Responsibility** pattern."
   - **The invariant**: "all children of a composite have as their parent the composite that in turn has them as children. The easiest way to ensure this is to **change a component's parent only when it's being added or removed** from a composite. If this can be implemented once in the `Add` and `Remove` operations of the Composite class, then it can be inherited by all the subclasses, and the invariant will be maintained automatically."
2. **Sharing components.** "when a component can have **no more than one parent**, sharing components becomes difficult. A possible solution is for children to store multiple parents. But that can lead to **ambiguities as a request propagates up** the structure. The **Flyweight** pattern shows how to rework a design to **avoid storing parents altogether**."
3. **Maximizing the Component interface.** "the Component class should define as many common operations for Composite and Leaf classes as possible."
   - The tension: "this goal will sometimes conflict with the principle of class hierarchy design that says **a class should only define operations that are meaningful to its subclasses**."
   - The resolution by reframing: "**if we view a Leaf as a Component that never has children**, then we can define a default operation for child access in the Component class that never returns any children."
4. **Declaring the child management operations** — **the pattern's central trade-off**:

| | Child management at **Component** (root) | Child management at **Composite** only |
|---|---|---|
| Gain | **Transparency** — "you can treat all components uniformly" | **Safety** — "any attempt to add or remove objects from leaves will be caught at compile-time in a statically typed language" |
| Cost | "clients may try to do **meaningless things** like add and remove objects from leaves" | "you lose transparency, because **leaves and composites have different interfaces**" |

**"We have emphasized transparency over safety in this pattern."**

If you choose safety, `GetComposite` avoids a type-unsafe cast:

```cpp
class Composite;

class Component {
public:
    // ...
    virtual Composite* GetComposite() { return 0; }
};

class Composite : public Component {
public:
    void Add(Component*);
    // ...
    virtual Composite* GetComposite() { return this; }
};

class Leaf : public Component {
    // ...
};
```
```cpp
Composite* aComposite = new Composite;
Leaf* aLeaf = new Leaf;
Component* aComponent;
Composite* test;

aComponent = aComposite;
if (test = aComponent->GetComposite()) {
    test->Add(new Leaf);
}

aComponent = aLeaf;
if (test = aComponent->GetComposite()) {
    test->Add(new Leaf);   // will not add leaf
}
```
- "Of course, **the problem here is that we don't treat all components uniformly**. We have to revert to testing for different types before taking the appropriate action."

**And if you choose transparency**, `Component::Add` must do *something*: "You could make it **do nothing**, but that ignores an important consideration; that is, **an attempt to add something to a leaf probably indicates a bug**. In that case, the `Add` operation produces garbage. You could make it **delete its argument**, but that might not be what clients expect. **Usually it's better to make `Add` and `Remove` fail by default (perhaps by raising an exception).**"

5. **Should Component implement a list of Components?** "putting the child pointer in the base class **incurs a space penalty for every leaf**, even though a leaf never has children. This is worthwhile only if there are relatively few children in the structure."
6. **Child ordering.** "ordering may reflect front-to-back ordering. If Composites represent parse trees, then compound statements can be instances of a Composite whose children must be ordered to reflect the program." **Iterator** can guide the interface design.
7. **Caching to improve performance.** "the `Picture` class could cache the **bounding box** of its children. During drawing or selection, this cached bounding box lets the Picture avoid drawing or searching when its children aren't visible." ⚠️ "Changes to a component will require **invalidating the caches of its parents**. This works best when components know their parents."
8. **Who should delete components?** "In languages without garbage collection, it's usually best to make a **Composite responsible for deleting its children** when it's destroyed. An exception... is when Leaf objects are **immutable and thus can be shared**."
9. **What's the best data structure?** "linked lists, trees, arrays, and hash tables... In fact, **it isn't even necessary to use a general-purpose data structure at all.** Sometimes composites have a variable for each child" — see **Interpreter**.

## Sample Code

Equipment hierarchies: "a chassis can contain drives and planar boards, a bus can contain cards, and a cabinet can contain chassis, buses, and so forth."

```cpp
class Equipment {
public:
    virtual ~Equipment();

    const char* Name() { return _name; }

    virtual Watt Power();
    virtual Currency NetPrice();
    virtual Currency DiscountPrice();

    virtual void Add(Equipment*);
    virtual void Remove(Equipment*);
    virtual Iterator<Equipment*>* CreateIterator();
protected:
    Equipment(const char*);
private:
    const char* _name;
};
```
- "The default implementation for [`CreateIterator`] returns a **`NullIterator`**, which iterates over the empty set."

```cpp
class CompositeEquipment : public Equipment {
public:
    virtual ~CompositeEquipment();

    virtual Watt Power();
    virtual Currency NetPrice();
    virtual Currency DiscountPrice();

    virtual void Add(Equipment*);
    virtual void Remove(Equipment*);
    virtual Iterator<Equipment*>* CreateIterator();
protected:
    CompositeEquipment(const char*);
private:
    List<Equipment*> _equipment;
};
```

The recursive default — a composite's price is the sum of its children's:

```cpp
Currency CompositeEquipment::NetPrice () {
    Iterator<Equipment*>* i = CreateIterator();
    Currency total = 0;

    for (i->First(); !i->IsDone(); i->Next()) {
        total += i->CurrentItem()->NetPrice();
    }
    delete i;
    return total;
}
```
- (Footnote: "It's easy to forget to delete the iterator once you're done with it. The **Iterator** pattern shows how to guard against such bugs.")

Assembling a PC — leaves and composites added through one interface:

```cpp
Cabinet* cabinet = new Cabinet("PC Cabinet");
Chassis* chassis = new Chassis("PC Chassis");

cabinet->Add(chassis);

Bus* bus = new Bus("MCA Bus");
bus->Add(new Card("16Mbs Token Ring"));

chassis->Add(bus);
chassis->Add(new FloppyDisk("3.5in Floppy"));

cout << "The net price is " << chassis->NetPrice() << endl;
```

## Known Uses
- "Examples of the Composite pattern can be found in **almost all object-oriented systems**."
- **Smalltalk MVC** — "The original `View` class... was a Composite, and nearly every user interface toolkit or framework has followed in its steps, including **ET++** (VObjects) and **InterViews** (Styles, Graphics, Glyphs)."
  - A historical note: "the original `View` of Model/View/Controller had a set of subviews; in other words, **`View` was both the Component class and the Composite class**. Release 4.0 of Smalltalk-80 revised MVC with a `VisualComponent` class that has subclasses `View` and `CompositeView`."
- **RTL Smalltalk compiler framework** — `RTLExpression` for parse trees; `RegisterTransfer` for SSA form, with leaf subclasses for "primitive assignments that perform an operation on two registers"; "an assignment with a **source register but no destination**, which indicates that the register is used after a routine returns"; and "an assignment with a **destination but no source**, which indicates that the register is assigned before the routine starts." `RegisterTransferSet` is the Composite.
- **Finance** — "a portfolio aggregates individual assets. You can support complex aggregations of assets by implementing a portfolio as a Composite that conforms to the interface of an individual asset."
- **Command** — "describes how Command objects can be composed and sequenced with a **MacroCommand** Composite class."

## Related Patterns
- "Often the **component-parent link** is used for a **Chain of Responsibility**."
- "**Decorator** is often used with Composite. When decorators and composites are used together, they will usually have a **common parent class**. So decorators will have to support the Component interface with operations like `Add`, `Remove`, and `GetChild`."
- "**Flyweight** lets you share components, but **they can no longer refer to their parents**."
- "**Iterator** can be used to traverse composites."
- "**Visitor** localizes operations and behavior that would otherwise be distributed across Composite and Leaf classes."

## Connects To
- **Ch 1 (MVC)**: nested views as Composite.
- **Ch 2 (Case Study, §2.2)**: recursive composition of glyphs — the pattern derived from the problem.
- **Ch 1**: cause of redesign #7 — extending functionality by subclassing.
- **Decorator, Flyweight, Iterator, Visitor, Chain of Responsibility, Interpreter, Command**
