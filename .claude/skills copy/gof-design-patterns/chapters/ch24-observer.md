# Observer
*Object Behavioral · Also Known As: **Dependents**, **Publish-Subscribe** · GoF p. 293*

## Intent
> **Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.**

## Motivation
"A common side-effect of partitioning a system into a collection of cooperating classes is the need to **maintain consistency between related objects**. You don't want to achieve consistency by making the classes tightly coupled, because that reduces their reusability."

The spreadsheet/bar-chart example: "Both a spreadsheet object and bar chart object can depict information in the **same application data object** using different presentations. **The spreadsheet and the bar chart don't know about each other, thereby letting you reuse only the one you need. But they behave as though they do.** When the user changes the information in the spreadsheet, the bar chart reflects the changes immediately, and vice versa."

"The key objects in this pattern are **subject** and **observer**. A subject may have any number of dependent observers. All observers are notified whenever the subject undergoes a change in state. **In response, each observer will query the subject to synchronize its state with the subject's state.**"

"This kind of interaction is also known as **publish-subscribe**. The subject is the publisher of notifications. **It sends out these notifications without having to know who its observers are.**"

## Applicability
Use Observer in any of these situations:
- "When an abstraction has **two aspects, one dependent on the other**. Encapsulating these aspects in separate objects lets you vary and reuse them independently."
- "When a change to one object requires changing others, and **you don't know how many objects need to be changed**."
- "When an object should be able to **notify other objects without making assumptions about who these objects are**."

## Participants
- **Subject** — "knows its observers. Any number of Observer objects may observe a subject"; "provides an interface for **attaching and detaching** Observer objects."
- **Observer** — "defines an **updating interface** for objects that should be notified of changes in a subject."
- **ConcreteSubject** (`ClockTimer`) — stores state of interest; "sends a notification to its observers **when its state changes**."
- **ConcreteObserver** (`DigitalClock`) — maintains a reference to a ConcreteSubject; "stores state that should stay consistent with the subject's"; implements the Observer updating interface.

## Collaborations
- "ConcreteSubject notifies its observers whenever a change occurs that could make its observers' state **inconsistent with its own**."
- "After being informed of a change, a ConcreteObserver object **may query the subject** for information."
- ⚠️ "**`Notify` is not always called by the subject. It can be called by an observer or by another kind of object entirely.**" Also: "the Observer object that **initiates** the change request **postpones its update until it gets a notification** from the subject."

## Consequences
"The Observer pattern lets you **vary subjects and observers independently**. You can reuse subjects without reusing their observers, and vice versa. It lets you **add observers without modifying the subject** or other observers."

1. **Abstract coupling between Subject and Observer.** "All a subject knows is that it has a list of observers, each conforming to the simple interface of the abstract Observer class. **The subject doesn't know the concrete class of any observer.**"
   - The layering argument: "**A lower-level subject can communicate and inform a higher-level observer, thereby keeping the system's layering intact.** If Subject and Observer are lumped together, then the resulting object must either **span two layers (and violate the layering)**, or be forced to live in one layer or the other (which might compromise the layering abstraction)."
2. **Support for broadcast communication.** "Unlike an ordinary request, the notification that a subject sends **needn't specify its receiver**... The subject doesn't care how many interested objects exist; its only responsibility is to notify its observers. **It's up to the observer to handle or ignore a notification.**"
3. ⚠️ **Unexpected updates.** "Because observers have **no knowledge of each other's presence**, they can be **blind to the ultimate cost of changing the subject**. A seemingly innocuous operation on the subject may cause a **cascade of updates** to observers and their dependent objects. Moreover, dependency criteria that aren't well-defined or maintained usually lead to **spurious updates, which can be hard to track down**."
   - "This problem is aggravated by the fact that **the simple update protocol provides no details on what changed in the subject**. Without additional protocol to help observers discover what changed, they may be forced to **work hard to deduce the changes**."

## Implementation
1. **Mapping subjects to their observers.** Storing references explicitly is simplest, "however, such storage may be too expensive when there are **many subjects and few observers**. One solution is to **trade space for time by using an associative look-up** (e.g., a hash table)... On the other hand, this approach **increases the cost of accessing the observers**."
2. **Observing more than one subject.** "It's necessary to **extend the `Update` interface** in such cases to let the observer know **which** subject is sending the notification. The subject can simply **pass itself as a parameter**."
3. **Who triggers the update?** Two options with a real trade-off:

| Option | Advantage | Disadvantage |
|---|---|---|
| **(a) State-setting operations on Subject call `Notify`** | "clients don't have to remember to call `Notify`" | "several consecutive operations will cause **several consecutive updates**, which may be inefficient" |
| **(b) Clients responsible for calling `Notify`** | "the client can wait to trigger the update until **after a series of state changes**, avoiding needless intermediate updates" | "clients have an added responsibility... **errors more likely, since clients might forget to call `Notify`**" |

4. ⚠️ **Dangling references to deleted subjects.** "One way to avoid dangling references is to make the subject **notify its observers as it is deleted** so that they can reset their reference to it. **In general, simply deleting the observers is not an option**, because other objects may reference them, or they may be observing other subjects as well."
5. ⚠️ **Making sure Subject state is self-consistent before notification.** "**This self-consistency rule is easy to violate unintentionally when Subject subclass operations call inherited operations.**"

```cpp
void MySubject::Operation (int newValue) {
    BaseClassSubject::Operation(newValue);  // trigger notification

    _myInstVar += newValue;                 // update subclass state (too late!)
}
```
   - The fix: "**send notifications from template methods** (Template Method (325)) in abstract Subject classes. Define a primitive operation for subclasses to override, and **make `Notify` the last operation in the template method**."

```cpp
void Text::Cut (TextRange r) {
    ReplaceRange(r);  // redefined in subclasses
    Notify();
}
```
   - "By the way, **it's always a good idea to document which Subject operations trigger notifications**."

6. **Avoiding observer-specific update protocols: the push and pull models.**

| Model | What the subject sends | Trade-off |
|---|---|---|
| **Push** | "detailed information about the change, **whether they want it or not**" | "**assumes subjects know something about their observers' needs**... might make observers less reusable, because Subject classes make assumptions about Observer classes that might not always be true" |
| **Pull** | "**nothing but the most minimal notification**, and observers ask for details explicitly thereafter" | "**emphasizes the subject's ignorance of its observers**"; but "may be inefficient, because Observer classes must ascertain what changed without help from the Subject" |

7. **Specifying modifications of interest explicitly.** "extend the subject's registration interface to allow registering observers **only for specific events of interest**." One way uses the notion of **aspects**:

```cpp
void Subject::Attach(Observer*, Aspects interest);
void Observer::Update(Subject*, Aspect& interest);
```

8. **Encapsulating complex update semantics — the `ChangeManager`.** "When the dependency relationship between subjects and observers is particularly complex, an object that maintains these relationships might be required... **if an operation involves changes to several interdependent subjects, you might have to ensure that their observers are notified only after all the subjects have been modified to avoid notifying observers more than once.**"
   - Its three responsibilities: "(a) It **maps a subject to its observers** and provides an interface to maintain this mapping. **This eliminates the need for subjects to maintain references to their observers and vice versa.** (b) It defines a particular **update strategy**. (c) It **updates all dependent observers** at the request of a subject."
   - Two specializations: "**`SimpleChangeManager` is naive in that it always updates all observers of each subject.** In contrast, **`DAGChangeManager` handles directed-acyclic graphs of dependencies**... preferable when an observer observes more than one subject. In that case, a change in two or more subjects might cause **redundant updates**. The `DAGChangeManager` ensures the observer receives just one update."
   - "**`ChangeManager` is an instance of the Mediator (273) pattern.** In general there is only one `ChangeManager`, and it is known globally. **The Singleton (127) pattern would be useful here.**"
9. **Combining the Subject and Observer classes.** "Class libraries written in languages that **lack multiple inheritance** (like Smalltalk) generally don't define separate Subject and Observer classes but **combine their interfaces in one class**... In Smalltalk, the Subject and Observer interfaces are defined in **the root class `Object`**, making them available to all classes."

## Sample Code

```cpp
class Subject;

class Observer {
public:
    virtual ~Observer();
    virtual void Update(Subject* theChangedSubject) = 0;
protected:
    Observer();
};
```
- "This implementation supports **multiple subjects for each observer**. The subject passed to the `Update` operation lets the observer determine which subject changed."

```cpp
class Subject {
public:
    virtual ~Subject();

    virtual void Attach(Observer*);
    virtual void Detach(Observer*);
    virtual void Notify();
protected:
    Subject();
private:
    List<Observer*> *_observers;
};

void Subject::Attach (Observer* o) {
    _observers->Append(o);
}

void Subject::Detach (Observer* o) {
    _observers->Remove(o);
}

void Subject::Notify () {
    ListIterator<Observer*> i(_observers);

    for (i.First(); !i.IsDone(); i.Next()) {
        i.CurrentItem()->Update(this);
    }
}
```

```cpp
class ClockTimer : public Subject {
public:
    ClockTimer();

    virtual int GetHour();
    virtual int GetMinute();
    virtual int GetSecond();

    void Tick();
};

void ClockTimer::Tick () {
    // update internal time-keeping state
    // ...
    Notify();
}
```
- "`Tick` gets called by an **internal timer at regular intervals** to provide an accurate time base."

```cpp
class DigitalClock : public Widget, public Observer {
public:
    DigitalClock(ClockTimer*);
    virtual ~DigitalClock();

    virtual void Update(Subject*);  // overrides Observer operation
    virtual void Draw();            // overrides Widget operation;
                                    // defines how to draw the digital clock
private:
    ClockTimer* _subject;
};

DigitalClock::DigitalClock (ClockTimer* s) {
    _subject = s;
    _subject->Attach(this);
}

DigitalClock::~DigitalClock () {
    _subject->Detach(this);
}
```
- **Attach in the constructor, detach in the destructor** — the observer manages its own registration lifetime.

```cpp
void DigitalClock::Update (Subject* theChangedSubject) {
    if (theChangedSubject == _subject) {
        Draw();
    }
}

void DigitalClock::Draw () {
    // get the new values from the subject
    int hour = _subject->GetHour();
    int minute = _subject->GetMinute();
    // etc.

    // draw the digital clock
}
```
- Note the **pull model** in action: `Update` carries no data; `Draw` queries the subject for what it needs.

```cpp
ClockTimer* timer = new ClockTimer;
AnalogClock* analogClock = new AnalogClock(timer);
DigitalClock* digitalClock = new DigitalClock(timer);
```
- "Whenever the timer ticks, the two clocks will be updated and will redisplay themselves appropriately." Neither clock knows the other exists.

## Known Uses
- **Smalltalk Model/View/Controller (MVC)** — "**the first and perhaps best-known example.** MVC's `Model` class plays the role of Subject, while `View` is the base class for observers."
- **Smalltalk, ET++, THINK class library** — "provide a **general dependency mechanism by putting Subject and Observer interfaces in the parent class for all other classes** in the system."
- **InterViews** — "defines `Observer` and `Observable` (for subjects) classes explicitly."
- **Andrew Toolkit** — "calls them '**view**' and '**data object**.'"
- **Unidraw** — "splits graphical editor objects into `View` (for observers) and `Subject` parts."

## Related Patterns
- "**Mediator**: By encapsulating complex update semantics, the `ChangeManager` acts as mediator between subjects and observers."
- "**Singleton**: The `ChangeManager` may use the Singleton pattern to make it unique and globally accessible."

## Connects To
- **Ch 5 (Behavioral Patterns)**: Observer "defines and maintains a **dependency** between objects. The classic example is in Smalltalk Model/View/Controller."
- **Ch 2 (Case Study)**: MVC and the separation of presentation from data.
- **Ch 22 (Mediator)**: the `ChangeManager`; and the reverse direction — "colleagues can communicate with the mediator using the Observer pattern."
- **Ch 27 (Template Method)**: the self-consistency fix in Implementation issue 5.
- **Mediator, Singleton, Template Method**
