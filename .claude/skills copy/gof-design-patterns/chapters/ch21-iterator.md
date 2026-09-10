# Iterator
*Object Behavioral · Also Known As: **Cursor** · GoF p. 257*

## Intent
> **Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.**

## Motivation
"An aggregate object such as a list should give you a way to access its elements **without exposing its internal structure**. Moreover, you might want to traverse the list in different ways... **But you probably don't want to bloat the List interface with operations for different traversals**, even if you could anticipate the ones you will need. **You might also need to have more than one traversal pending on the same list.**"

"The key idea in this pattern is to **take the responsibility for access and traversal out of the list object and put it into an iterator object**... An iterator object is responsible for keeping track of the current element; that is, **it knows which elements have been traversed already**."

**The step to polymorphic iteration**: "Notice that the iterator and the list are coupled, and **the client must know that it is a list that's traversed** as opposed to some other aggregate structure. Hence the client commits to a particular aggregate structure. **It would be better if we could change the aggregate class without changing client code.**"

The remaining problem: "Since we want to write code that's independent of the concrete List subclasses, **we cannot simply instantiate a specific class**. Instead, **we make the list objects responsible for creating their corresponding iterator**." — `CreateIterator` is "an example of a **factory method**... The Factory Method approach gives rise to two class hierarchies, one for lists and another for iterators. **The `CreateIterator` factory method 'connects' the two hierarchies.**"

## Applicability
Use Iterator:
- "to access an aggregate object's contents **without exposing its internal representation**."
- "to support **multiple traversals** of aggregate objects."
- "to provide a **uniform interface for traversing different aggregate structures** (that is, to support polymorphic iteration)."

## Participants
- **Iterator** — defines an interface for accessing and traversing elements.
- **ConcreteIterator** — implements the interface; **"keeps track of the current position in the traversal."**
- **Aggregate** — defines an interface for creating an Iterator object.
- **ConcreteAggregate** — returns an instance of the proper ConcreteIterator.

## Consequences
1. **It supports variations in the traversal of an aggregate.** "code generation and semantic checking involve traversing parse trees. Code generation may traverse the parse tree **inorder or preorder**. Iterators make it easy to change the traversal algorithm: **just replace the iterator instance with a different one**."
2. **Iterators simplify the Aggregate interface.** "Iterator's traversal interface **obviates the need for a similar interface in Aggregate**."
3. **More than one traversal can be pending on an aggregate.** "An iterator keeps track of its own traversal state."

## Implementation
"The trade-offs often depend on the control structures your language provides. **Some languages (CLU, for example) even support this pattern directly.**"

1. **Who controls the iteration?** — **external** (client-controlled) vs. **internal** (iterator-controlled).

| | **External iterator** | **Internal iterator** |
|---|---|---|
| Client's job | "must advance the traversal and **request the next element explicitly**" | "the client **hands an internal iterator an operation to perform**, and the iterator applies that operation to every element" |
| Flexibility | "**more flexible**... It's easy to compare two collections for equality with an external iterator, for example, but it's **practically impossible with internal iterators**" | "**easier to use, because they define the iteration logic for you**" |
| Language dependence | — | "**especially weak in a language like C++** that does not provide anonymous functions, closures, or continuations like Smalltalk and CLOS" |

(Footnote: "Booch refers to external and internal iterators as **active and passive** iterators. The terms describe **the role of the client**, not the level of activity in the iterator.")

2. **Who defines the traversal algorithm?** "The aggregate might define the traversal algorithm and use the iterator to store **just the state** of the iteration. We call this kind of iterator a **cursor**, since it merely points to the current position."
   - The trade-off: "If the iterator is responsible for the traversal algorithm, then it's easy to use different iteration algorithms on the same aggregate... **On the other hand, the traversal algorithm might need to access the private variables of the aggregate. If so, putting the traversal algorithm in the iterator violates the encapsulation of the aggregate.**"
   - (Footnote: "Cursors are a simple example of the **Memento** pattern.")

3. ⚠️ **How robust is the iterator?** "**It can be dangerous to modify an aggregate while you're traversing it.** If elements are added or deleted, **you might end up accessing an element twice or missing it completely**. A simple solution is to copy the aggregate and traverse the copy, but that's too expensive to do in general."
   - "A **robust iterator** ensures that insertions and removals won't interfere with traversal, **and it does it without copying the aggregate**. Most rely on **registering the iterator with the aggregate**. On insertion or removal, the aggregate either adjusts the internal state of iterators it has produced, or it maintains information internally to ensure proper traversal."

4. **Additional Iterator operations.** "The minimal interface consists of `First`, `Next`, `IsDone`, and `CurrentItem`." Useful additions: `Previous` for ordered aggregates; **`SkipTo`** for sorted or indexed collections, which "positions the iterator to an object matching specific criteria."
   - (Footnote: "We can make this interface even smaller by **merging `Next`, `IsDone`, and `CurrentItem` into a single operation** that advances to the next object and returns it. If the traversal is finished, then this operation returns a special value (0, for instance).")

5. **Using polymorphic iterators in C++.** "**Polymorphic iterators have their cost.** They require the iterator object to be **allocated dynamically** by a factory method. Hence they should be used **only when there's a need for polymorphism**. Otherwise use concrete iterators, which can be allocated on the stack."
   - ⚠️ "another drawback: **the client is responsible for deleting them**. This is error-prone... **That's especially likely when there are multiple exit points in an operation. And if an exception is triggered, the iterator object will never be freed.**"
   - "**The Proxy pattern provides a remedy.** We can use a **stack-allocated proxy** as a stand-in for the real iterator. The proxy deletes the iterator in its destructor... **This is an application of the well-known C++ technique 'resource allocation is initialization.'**"

6. **Iterators may have privileged access.** "An iterator can be viewed as an **extension of the aggregate** that created it... We can express this close relationship in C++ by making the iterator a **friend** of its aggregate."
   - ⚠️ "**such privileged access can make defining new traversals difficult, since it'll require changing the aggregate interface to add another friend**. To avoid this problem, the Iterator class can include **protected operations** for accessing important but publicly unavailable members."

7. **Iterators for composites.** "**External iterators can be difficult to implement over recursive aggregate structures** like those in Composite, because a position in the structure may span many levels of nested aggregates. Therefore an external iterator has to **store a path** through the Composite."
   - "Sometimes it's easier just to use an **internal iterator**. It can record the current position simply by **calling itself recursively, thereby storing the path implicitly in the call stack**."
   - "If the nodes in a Composite have an interface for moving from a node to its siblings, parents, and children, then a **cursor-based iterator** may offer a better alternative."

8. **Null iterators.** "A `NullIterator` is a **degenerate iterator** that's helpful for handling boundary conditions. By definition, a `NullIterator` is always done with traversal; **its `IsDone` operation always evaluates to true**."
   - "At each point in the traversal, we ask the current element for an iterator for its children. Aggregate elements return a concrete iterator as usual. **But leaf elements return an instance of `NullIterator`. That lets us implement traversal over the entire structure in a uniform way.**"

## Sample Code

```cpp
template <class Item>
class Iterator {
public:
    virtual void First() = 0;
    virtual void Next() = 0;
    virtual bool IsDone() const = 0;
    virtual Item CurrentItem() const = 0;
protected:
    Iterator();
};
```
```cpp
template <class Item>
class ListIterator : public Iterator<Item> {
public:
    ListIterator(const List<Item>* aList);

    virtual void First();
    virtual void Next();
    virtual bool IsDone() const;
    virtual Item CurrentItem() const;
private:
    const List<Item>* _list;
    long _current;
};

template <class Item>
void ListIterator<Item>::First () { _current = 0; }

template <class Item>
void ListIterator<Item>::Next () { _current++; }

template <class Item>
bool ListIterator<Item>::IsDone () const {
    return _current >= _list->Count();
}

template <class Item>
Item ListIterator<Item>::CurrentItem () const {
    if (IsDone()) {
        throw IteratorOutOfBounds;
    }
    return _list->Get(_current);
}
```
- Note the design choice: "The `List` class provides a reasonably efficient way to support iteration **through its public interface**... **So there's no need to give iterators privileged access**; that is, the iterator classes are **not friends of `List`**."
- "The implementation of `ReverseListIterator` is identical, except its `First` operation positions `_current` to the **end** of the list, and `Next` **decrements** `_current`."

Client code written against the abstraction, reusable across both directions:

```cpp
void PrintEmployees (Iterator<Employee*>& i) {
    for (i.First(); !i.IsDone(); i.Next()) {
        i.CurrentItem()->Print();
    }
}
```
```cpp
ListIterator<Employee*> forward(employees);
ReverseListIterator<Employee*> backward(employees);

PrintEmployees(forward);
PrintEmployees(backward);
```

Polymorphic iteration via a factory method:

```cpp
template <class Item>
class AbstractList {
public:
    virtual Iterator<Item>* CreateIterator() const = 0;
    // ...
};

template <class Item>
Iterator<Item>* List<Item>::CreateIterator () const {
    return new ListIterator<Item>(this);
}
```
- "An alternative would be to define a general **mixin class `Traversable`**... Aggregate classes can mix in `Traversable` to support polymorphic iteration."

**The cleanup proxy** — the reason this pattern's Sample Code is memorable:

```cpp
template <class Item>
class IteratorPtr {
public:
    IteratorPtr(Iterator<Item>* i): _i(i) { }
    ~IteratorPtr() { delete _i; }

    Iterator<Item>* operator->() { return _i; }
    Iterator<Item>& operator*() { return *_i; }
private:
    // disallow copy and assignment to avoid
    // multiple deletions of _i:
    IteratorPtr(const IteratorPtr&);
    IteratorPtr& operator=(const IteratorPtr&);
private:
    Iterator<Item>* _i;
};
```
```cpp
AbstractList<Employee*>* employees;
// ...
IteratorPtr<Employee*> iterator(employees->CreateIterator());
PrintEmployees(*iterator);
```
- "`IteratorPtr` is **always allocated on the stack**. C++ automatically takes care of calling its destructor... **The members of `IteratorPtr` are all implemented inline; thus they can incur no overhead.**"
- (Footnote: "You can ensure this at compile-time just by **declaring private `new` and `delete` operators**. An accompanying implementation isn't needed.")

**An internal iterator**, and the two ways to parameterize it: "(1) **Pass in a pointer to a function** (global or static), or (2) **rely on subclassing**."
- "Neither option is perfect. Often you want to **accumulate state during the iteration, and functions aren't well-suited to that**; we would have to use static variables. An Iterator subclass provides us with a convenient place to store the accumulated state... **But creating a subclass for every different traversal is more work.**"

```cpp
template <class Item>
class ListTraverser {
public:
    ListTraverser(List<Item>* aList);
    bool Traverse();
protected:
    virtual bool ProcessItem(const Item&) = 0;
private:
    ListIterator<Item> _iterator;
};

template <class Item>
bool ListTraverser<Item>::Traverse () {
    bool result = false;

    for (_iterator.First(); !_iterator.IsDone(); _iterator.Next()) {
        result = ProcessItem(_iterator.CurrentItem());
        if (result == false) {
            break;
        }
    }
    return result;
}
```
```cpp
class PrintNEmployees : public ListTraverser<Employee*> {
public:
    PrintNEmployees(List<Employee*>* aList, int n) :
        ListTraverser<Employee*>(aList),
        _total(n), _count(0) { }
protected:
    bool ProcessItem(Employee* const&);
private:
    int _total;
    int _count;
};

bool PrintNEmployees::ProcessItem (Employee* const& e) {
    _count++;
    e->Print();
    return _count < _total;
}
```
- "**Note how the client doesn't specify the iteration loop. The entire iteration logic can be reused. This is the primary benefit of an internal iterator.** It's a bit more work than an external iterator, though, because we have to define a new class."
- (Footnote: "The `Traverse` operation in these examples is a **Template Method** with primitive operations `TestItem` and `ProcessItem`.")

## Known Uses
- **Booch components** — "the queue iterator is implemented in terms of the **abstract `Queue` class interface**. This variation has the advantage that **you don't need a factory method**... However, it requires the interface of the abstract `Queue` class to be **powerful enough to implement the iterator efficiently**."
- **Smalltalk** — "Iterators don't have to be defined as explicitly... The standard collection classes define an internal iterator method **`do:`**, which takes a block (i.e., closure)... `ReadStream` is essentially an Iterator, and it can act as an external iterator for all the sequential collections. **There are no standard external iterators for nonsequential collections such as `Set` and `Dictionary`.**"
- **ET++** — polymorphic iterators and the cleanup Proxy. **Unidraw** — cursor-based iterators.
- **ObjectWindows 2.0** — "The ObjectWindow iteration syntax relies on **overloading the postincrement operator `++`** to advance the iteration."

## Related Patterns
- "**Composite**: Iterators are often applied to recursive structures such as Composites."
- "**Factory Method**: Polymorphic iterators rely on factory methods to instantiate the appropriate Iterator subclass."
- "**Memento** is often used in conjunction with the Iterator pattern. **An iterator can use a memento to capture the state of an iteration.** The iterator stores the memento internally."

## Connects To
- **Ch 2 (Case Study, §2.8)**: the glyph iterators, `NullIterator`, and `PreorderIterator` — the pattern derived from the problem.
- **Ch 1**: cause of redesign #5 — algorithmic dependencies.
- **Composite, Factory Method, Memento, Proxy, Template Method**
