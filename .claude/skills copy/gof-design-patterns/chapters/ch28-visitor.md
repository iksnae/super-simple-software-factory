# Visitor
*Object Behavioral · GoF p. 331*

## Intent
> **Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.**

## Motivation
A compiler representing programs as abstract syntax trees needs "operations for **type-checking, code optimization, flow analysis, checking for variables being assigned values before they're used**, and so on. Moreover, we could use the abstract syntax trees for **pretty-printing, program restructuring, code instrumentation, and computing various metrics**."

⚠️ **The problem**: "distributing all these operations across the various node classes leads to a system that's **hard to understand, maintain, and change**. It will be confusing to have type-checking code mixed with pretty-printing code or flow analysis code. Moreover, **adding a new operation usually requires recompiling all of these classes.**"

The observation that makes Visitor viable: "**The set of node classes depends on the language being compiled, of course, but it doesn't change much for a given language.**"

The mechanism: "package related operations from each class in a separate object, called a **visitor**, and pass it to elements of the abstract syntax tree as it's traversed. **When an element 'accepts' the visitor, it sends a request to the visitor that encodes the element's class.** It also includes the element as an argument."

The before/after: "a compiler that didn't use visitors might type-check by calling `TypeCheck` on its abstract syntax tree... **What used to be the `TypeCheck` operation in class `AssignmentNode` is now the `VisitAssignment` operation on `TypeCheckingVisitor`.**"

**Two hierarchies, not one**: "you define **two class hierarchies**: one for the **elements** being operated on (the `Node` hierarchy) and one for the **visitors** that define operations on the elements (the `NodeVisitor` hierarchy). **You create a new operation by adding a new subclass to the visitor class hierarchy.** As long as the grammar doesn't change... **we can add new functionality simply by defining new `NodeVisitor` subclasses.**"

## Applicability
Use Visitor when:
- "an object structure contains **many classes of objects with differing interfaces**, and you want to perform operations on these objects that **depend on their concrete classes**."
- "**many distinct and unrelated operations** need to be performed on objects in an object structure, and you want to **avoid 'polluting' their classes** with these operations... **When the object structure is shared by many applications, use Visitor to put operations in just those applications that need them.**"
- "**the classes defining the object structure rarely change, but you often want to define new operations** over the structure. **Changing the object structure classes requires redefining the interface to all visitors, which is potentially costly. If the object structure classes change often, then it's probably better to define the operations in those classes.**"

## Participants
- **Visitor** (`NodeVisitor`) — "declares a `Visit` operation for **each class of ConcreteElement**. **The operation's name and signature identifies the class that sends the `Visit` request**... Then the visitor can access the element directly through its particular interface."
- **ConcreteVisitor** (`TypeCheckingVisitor`) — "implements each operation declared by Visitor. **ConcreteVisitor provides the context for the algorithm and stores its local state. This state often accumulates results during the traversal** of the structure."
- **Element** (`Node`) — "defines an `Accept` operation that takes a visitor as an argument."
- **ConcreteElement** (`AssignmentNode`, `VariableRefNode`) — implements `Accept`.
- **ObjectStructure** (`Program`) — "can **enumerate its elements**"; "may provide a high-level interface to allow the visitor to visit its elements"; "**may either be a composite** (see Composite (163)) **or a collection** such as a list or a set."

## Collaborations
- "A client... must **create a ConcreteVisitor object and then traverse the object structure**, visiting each element with the visitor."
- "When an element is visited, **it calls the Visitor operation that corresponds to its class. The element supplies itself as an argument** to this operation to let the visitor access its state."

## Consequences
1. **Visitor makes adding new operations easy.** "You can define a new operation over an object structure simply by adding a new visitor. **In contrast, if you spread functionality over many classes, then you must change each class to define a new operation.**"
2. **A visitor gathers related operations and separates unrelated ones.** "Unrelated sets of behavior are partitioned in their own visitor subclasses... **Any algorithm-specific data structures can be hidden in the visitor.**"
3. ⚠️ **Adding new ConcreteElement classes is hard.** "**Each new ConcreteElement gives rise to a new abstract operation on Visitor and a corresponding implementation in every ConcreteVisitor class.** Sometimes a default implementation can be provided in Visitor that can be inherited by most of the ConcreteVisitors, but **this is the exception rather than the rule**."
   - **The decision rule**: "the key consideration in applying the Visitor pattern is **whether you are mostly likely to change the algorithm applied over an object structure or the classes of objects that make up the structure**. The Visitor class hierarchy can be difficult to maintain when new ConcreteElement classes are added frequently. In such cases, **it's probably easier just to define operations on the classes that make up the structure. If the Element class hierarchy is stable, but you are continually adding operations or changing algorithms, then the Visitor pattern will help you manage the changes.**"
4. **Visiting across class hierarchies.** "An **iterator** can visit the objects in a structure as it traverses them by calling their operations. **But an iterator can't work across object structures with different types of elements.**"

```cpp
template <class Item>
class Iterator {
    // ...
    Item CurrentItem() const;
};
```
   - "This implies that **all elements the iterator can visit have a common parent class `Item`**. **Visitor does not have this restriction. It can visit objects that don't have a common parent class.**"

```cpp
class Visitor {
public:
    // ...
    void VisitMyType(MyType*);
    void VisitYourType(YourType*);
};
```
   - "**`MyType` and `YourType` do not have to be related through inheritance at all.**"
5. **Accumulating state.** "Without a visitor, this state would be passed as **extra arguments** to the operations that perform the traversal, or they might appear as **global variables**."
6. ⚠️ **Breaking encapsulation.** "Visitor's approach **assumes that the ConcreteElement interface is powerful enough to let visitors do their job**. As a result, **the pattern often forces you to provide public operations that access an element's internal state, which may compromise its encapsulation.**"

## Implementation

```cpp
class Visitor {
public:
    virtual void VisitElementA(ElementA*);
    virtual void VisitElementB(ElementB*);

    // and so on for other concrete elements
protected:
    Visitor();
};
```
```cpp
class Element {
public:
    virtual ~Element();
    virtual void Accept(Visitor&) = 0;
protected:
    Element();
};

class ElementA : public Element {
public:
    ElementA();
    virtual void Accept(Visitor& v) { v.VisitElementA(this); }
};

class ElementB : public Element {
public:
    ElementB();
    virtual void Accept(Visitor& v) { v.VisitElementB(this); }
};
```
- "**Thus the operation that ends up getting called depends on both the class of the element and the class of the visitor.**"
- GoF's footnote on naming: "We could use **function overloading** to give these operations the same simple name, like `Visit`... On the one hand, it **reinforces the fact that each operation involves the same analysis**, albeit on a different argument. On the other hand, that might make **what's going on at the call site less obvious**."

A composite element traverses its children *before* visiting itself:

```cpp
class CompositeElement : public Element {
public:
    virtual void Accept(Visitor&);
private:
    List<Element*>* _children;
};

void CompositeElement::Accept (Visitor& v) {
    ListIterator<Element*> i(_children);

    for (i.First(); !i.IsDone(); i.Next()) {
        i.CurrentItem()->Accept(v);
    }
    v.VisitCompositeElement(this);
}
```

1. **Double dispatch.** "In **single-dispatch** languages, **two criteria** determine which operation will fulfill a request: **the name of the request and the type of receiver**... '**Double-dispatch**' simply means the operation that gets executed depends on the kind of request and the types of **two receivers**. **`Accept` is a double-dispatch operation. Its meaning depends on two types: the Visitor's and the Element's.**"
   - "**This is the key to the Visitor pattern**: The operation that gets executed depends on both the type of Visitor and the type of Element it visits. **Instead of binding operations statically into the Element interface, you can consolidate the operations in a Visitor and use `Accept` to do the binding at run-time.** Extending the Element interface amounts to defining **one new Visitor subclass rather than many new Element subclasses**."
   - The language footnote: "double-dispatch is just a special case of **multiple dispatch**... (**CLOS** actually supports multiple dispatch.) **Languages that support double- or multiple dispatch lessen the need for the Visitor pattern.**"
2. **Who is responsible for traversing the object structure?** "We can put responsibility for traversal in any of **three places: in the object structure, in the visitor, or in a separate iterator object**."

| Location | Notes |
|---|---|
| **The object structure** (most common) | "A collection will simply iterate over its elements, calling `Accept` on each. **A composite will commonly traverse itself by having each `Accept` operation traverse the element's children** and call `Accept` on each recursively." |
| **An iterator** | ⚠️ "**an internal iterator will not cause double-dispatching** — it will call an operation on the **visitor** with an element as an argument as opposed to calling an operation on the **element** with the visitor as an argument. But it's easy to use the Visitor pattern with an internal iterator if the operation on the visitor **simply calls the operation on the element without recursing**." |
| **The visitor** | ⚠️ "you'll end up **duplicating the traversal code in each ConcreteVisitor for each aggregate ConcreteElement**. The main reason to put the traversal strategy in the visitor is to implement a **particularly complex traversal, one that depends on the results of the operations on the object structure**." |

## Sample Code
### 1. Equipment pricing and inventory (traversal in the structure)
Reusing the `Equipment` classes from **Composite**.

```cpp
class Equipment {
public:
    virtual ~Equipment();

    const char* Name() { return _name; }

    virtual Watt Power();
    virtual Currency NetPrice();
    virtual Currency DiscountPrice();

    virtual void Accept(EquipmentVisitor&);
protected:
    Equipment(const char*);
private:
    const char* _name;
};
```
```cpp
class EquipmentVisitor {
public:
    virtual ~EquipmentVisitor();

    virtual void VisitFloppyDisk(FloppyDisk*);
    virtual void VisitCard(Card*);
    virtual void VisitChassis(Chassis*);
    virtual void VisitBus(Bus*);

    // and so on for other concrete subclasses of Equipment
protected:
    EquipmentVisitor();
};
```
- "**All of the virtual functions do nothing by default.**"

```cpp
void FloppyDisk::Accept (EquipmentVisitor& visitor) {
    visitor.VisitFloppyDisk(this);
}

void Chassis::Accept (EquipmentVisitor& visitor) {
    for (
        ListIterator<Equipment*> i(_parts);
        !i.IsDone();
        i.Next()
    ) {
        i.CurrentItem()->Accept(visitor);
    }
    visitor.VisitChassis(this);
}
```

```cpp
class PricingVisitor : public EquipmentVisitor {
public:
    PricingVisitor();

    Currency& GetTotalPrice();

    virtual void VisitFloppyDisk(FloppyDisk*);
    virtual void VisitCard(Card*);
    virtual void VisitChassis(Chassis*);
    virtual void VisitBus(Bus*);
    // ...
private:
    Currency _total;
};

void PricingVisitor::VisitFloppyDisk (FloppyDisk* e) {
    _total += e->NetPrice();
}

void PricingVisitor::VisitChassis (Chassis* e) {
    _total += e->DiscountPrice();
}
```
- "**`PricingVisitor` chooses the appropriate pricing policy for a class of equipment by dispatching to the corresponding member function.** What's more, **we can change the pricing policy of an equipment structure just by changing the `PricingVisitor` class.**" (Net price for simple equipment, **discount** price for composites.)

```cpp
class InventoryVisitor : public EquipmentVisitor {
public:
    InventoryVisitor();

    Inventory& GetInventory();

    virtual void VisitFloppyDisk(FloppyDisk*);
    virtual void VisitCard(Card*);
    virtual void VisitChassis(Chassis*);
    virtual void VisitBus(Bus*);
    // ...
private:
    Inventory _inventory;
};

void InventoryVisitor::VisitFloppyDisk (FloppyDisk* e) {
    _inventory.Accumulate(e);
}

void InventoryVisitor::VisitChassis (Chassis* e) {
    _inventory.Accumulate(e);
}
```
```cpp
Equipment* component;
InventoryVisitor visitor;

component->Accept(visitor);
cout << "Inventory " << component->Name() << visitor.GetInventory();
```

### 2. Regular-expression matching (traversal in the *visitor*)
The Interpreter chapter's Smalltalk matcher, rewritten as a visitor. "**It is responsible for the traversal because its traversal algorithm is irregular. The biggest irregularity is that a `RepeatExpression` will repeatedly traverse its component.**"

```smalltalk
accept: aVisitor
    aVisitor visitSequence: self
```
```smalltalk
visitSequence: sequenceExp
    inputState := sequenceExp expression1 accept: self.
    sequenceExp expression2 accept: self.

visitRepeat: repeatExp
    | finalState |
    finalState := inputState copy.
    [inputState isEmpty] whileFalse:
        [inputState := repeatExp repetition accept: self.
         finalState addAll: inputState].
    ^ finalState

visitAlternation: alternateExp
    | finalState originalState |
    originalState := inputState.
    finalState := alternateExp alternative1 accept: self.
    inputState := originalState.
    finalState addAll: (alternateExp alternative2 accept: self).
    ^ finalState

visitLiteral: literalExp
    | finalState tStream |
    finalState := Set new.
    inputState do: [:stream |
        tStream := stream copy.
        (tStream nextAvailable: literalExp components size)
            = literalExp components
                ifTrue: [finalState add: tStream]].
    ^ finalState
```
- "Its methods are **essentially the same as the `match:` methods of the expression classes in the Interpreter pattern** except they replace the argument named `inputState` with the expression node being matched." The visitor holds `inputState` as an **instance variable** instead — Consequence 5 (accumulating state) in practice.

## Known Uses
- **Smalltalk-80 compiler** — "has a Visitor class called `ProgramNodeEnumerator`. **It's used primarily for algorithms that analyze source code.** It isn't used for code generation or pretty-printing, although it could be."
- **IRIS Inventor** (3-D graphics) — "Inventor does this using visitors called '**actions**.' There are different visitors for **rendering, event handling, searching, filing, and determining bounding boxes**."
  - Its escape from Consequence 3: "To make adding new nodes easier, Inventor implements a **double-dispatch scheme for C++**. The scheme relies on **run-time type information and a two-dimensional table in which rows represent visitors and columns represent node classes. The cells store a pointer to the function bound to the visitor and node class.**"
- **Fresco Application Toolkit** — "**Mark Linton coined the term 'Visitor'** in the X Consortium's Fresco Application Toolkit specification."

## Related Patterns
- "**Composite**: Visitors can be used to apply an operation over an object structure defined by the Composite pattern."
- "**Interpreter**: Visitor may be applied to do the interpretation."

## Connects To
- **Ch 5 (Behavioral Patterns)**: Visitor encapsulates behavior "that would otherwise be **distributed across classes**."
- **Ch 12 (Composite)**: the `Equipment` structure the sample code visits.
- **Ch 20 (Interpreter)**: "**If you keep creating new ways of interpreting an expression, then consider using the Visitor pattern** to avoid changing the grammar classes"; and the Boolean example's claim that `Evaluate`, `Replace`, and `Copy` "**can all be refactored into a separate 'interpreter' visitor**."
- **Ch 21 (Iterator)**: the alternative traversal mechanism, and its common-parent-class limitation.
- **Composite, Interpreter, Iterator**
