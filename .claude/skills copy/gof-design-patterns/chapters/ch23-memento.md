# Memento
*Object Behavioral · Also Known As: **Token** · GoF p. 283*

## Intent
> **Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.**

## Motivation
"Sometimes it's necessary to record the internal state of an object. This is required when implementing **checkpoints and undo mechanisms** that let users back out of tentative operations or recover from errors."

The bind: "objects normally **encapsulate** some or all of their state, making it inaccessible to other objects and impossible to save externally. **Exposing this state would violate encapsulation, which can compromise the application's reliability and extensibility.**"

The graphical-editor example — rectangles connected by a line that stays connected when either is moved. A `ConstraintSolver` "records connections as they are made and generates mathematical equations that describe them," then rearranges the graphics.

⚠️ **Why naive undo fails**: "An obvious way to undo a move operation is to store the **original distance moved** and move the object back an equivalent distance. However, **this does not guarantee all objects will appear where they did before**. Suppose there is some **slack** in the connection. In that case, simply moving the rectangle back to its original location won't necessarily achieve the desired effect."

"In general, the `ConstraintSolver`'s **public interface might be insufficient to allow precise reversal of its effects** on other objects. The undo mechanism must work more closely with `ConstraintSolver` to reestablish previous state, but **we should also avoid exposing the `ConstraintSolver`'s internals** to the undo mechanism."

The resolution: "A memento is an object that stores a snapshot of the internal state of another object — the memento's **originator**... **Only the originator can store and retrieve information from the memento — the memento is 'opaque' to other objects.**"

**The four-step undo sequence:**
1. "The editor requests a memento from the `ConstraintSolver` as a **side-effect of the move operation**."
2. "The `ConstraintSolver` creates and returns a memento, an instance of a class `SolverState`... [containing] data structures that describe the current state of the `ConstraintSolver`'s internal equations and variables."
3. "Later when the user undoes the move operation, the editor gives the `SolverState` **back** to the `ConstraintSolver`."
4. "Based on the information in the `SolverState`, the `ConstraintSolver` changes its internal structures to return its equations and variables to their **exact previous state**."

## Applicability
Use Memento when:
- "a **snapshot** of (some portion of) an object's state must be saved so that it can be restored to that state later, **and**"
- "a **direct interface to obtaining the state would expose implementation details** and break the object's encapsulation."

## Participants
- **Memento** (`SolverState`) — "stores internal state of the Originator object. The memento may store **as much or as little** of the originator's internal state as necessary **at its originator's discretion**."
  - ⚠️ **The two-interface rule**: "Mementos have effectively **two interfaces**. **Caretaker sees a narrow interface** — it can only pass the memento to other objects. **Originator, in contrast, sees a wide interface**, one that lets it access all the data necessary to restore itself. Ideally, only the originator that produced the memento would be permitted to access the memento's internal state."
- **Originator** (`ConstraintSolver`) — creates a memento containing a snapshot of its current internal state; uses the memento to restore its internal state.
- **Caretaker** (the undo mechanism) — "is responsible for the memento's **safekeeping**"; "**never operates on or examines the contents of a memento**."

## Collaborations
- "A caretaker requests a memento from an originator, **holds it for a time**, and passes it back to the originator."
- "Sometimes the caretaker **won't** pass the memento back to the originator, because the originator might never need to revert to an earlier state."
- "**Mementos are passive. Only the originator that created a memento will assign or retrieve its state.**"

## Consequences
1. **Preserving encapsulation boundaries.** "Memento avoids exposing information that only an originator should manage but that must be stored nevertheless outside the originator."
2. **It simplifies Originator.** "In other encapsulation-preserving designs, Originator keeps the versions of internal state that clients have requested. That puts **all the storage management burden on Originator**. Having clients manage the state they ask for simplifies Originator and keeps clients from having to notify originators when they're done."
3. ⚠️ **Using mementos might be expensive.** "Mementos might incur considerable overhead if Originator must **copy large amounts of information**... or if clients create and return mementos to the originator **often enough**. **Unless encapsulating and restoring Originator state is cheap, the pattern might not be appropriate.**"
4. ⚠️ **Defining narrow and wide interfaces.** "It may be **difficult in some languages** to ensure that only the originator can access the memento's state."
5. ⚠️ **Hidden costs in caring for mementos.** "A caretaker is responsible for **deleting** the mementos it cares for. However, **the caretaker has no idea how much state is in the memento.** Hence an otherwise lightweight caretaker might incur large storage costs."

## Implementation
1. **Language support.** "Ideally the implementation language will support **two levels of static protection**. C++ lets you do this by making the **Originator a friend of Memento** and making Memento's **wide interface private**. Only the narrow interface should be declared public."

```cpp
class State;

class Originator {
public:
    Memento* CreateMemento();
    void SetMemento(const Memento*);
    // ...
private:
    State* _state;  // internal data structures
    // ...
};

class Memento {
public:
    // narrow public interface
    virtual ~Memento();
private:
    // private members accessible only to Originator
    friend class Originator;
    Memento();
    void SetState(State*);
    State* GetState();
    // ...
private:
    State* _state;
};
```

2. **Storing incremental changes.** "When mementos get created and passed back to their originator **in a predictable sequence**, then Memento can save just the **incremental change** to the originator's internal state."
   - "undoable commands in a history list can use mementos... **The history list defines a specific order in which commands can be undone and redone. That means mementos can store just the incremental change that a command makes rather than the full state of every object they affect.**"
   - Applied to the example: "the constraint solver can store only those internal structures that change to keep the line connecting the rectangles, **as opposed to storing the absolute positions** of these objects."

## Sample Code
`MoveCommand` objects (see **Command**) (un)do a translation. "The command stores its **target**, the **distance moved**, and an instance of `ConstraintSolverMemento`."

```cpp
class Graphic;  // base class for graphical objects in the graphical editor

class MoveCommand {
public:
    MoveCommand(Graphic* target, const Point& delta);
    void Execute();
    void Unexecute();
private:
    ConstraintSolverMemento* _state;
    Point _delta;
    Graphic* _target;
};
```
```cpp
class ConstraintSolver {
public:
    static ConstraintSolver* Instance();

    void Solve();
    void AddConstraint(
        Graphic* startConnection, Graphic* endConnection
    );
    void RemoveConstraint(
        Graphic* startConnection, Graphic* endConnection
    );

    ConstraintSolverMemento* CreateMemento();
    void SetMemento(ConstraintSolverMemento*);
private:
    // nontrivial state and operations for enforcing
    // connectivity semantics
};

class ConstraintSolverMemento {
public:
    virtual ~ConstraintSolverMemento();
private:
    friend class ConstraintSolver;
    ConstraintSolverMemento();

    // private constraint solver state
};
```
- "**`ConstraintSolver` is a Singleton (127).**"

```cpp
void MoveCommand::Execute () {
    ConstraintSolver* solver = ConstraintSolver::Instance();
    _state = solver->CreateMemento();  // create a memento
    _target->Move(_delta);
    solver->Solve();
}

void MoveCommand::Unexecute () {
    ConstraintSolver* solver = ConstraintSolver::Instance();
    _target->Move(-_delta);
    solver->SetMemento(_state);        // restore solver state
    solver->Solve();
}
```
- Note the ordering: "`Execute` acquires a `ConstraintSolverMemento` **before** it moves the graphic. `Unexecute` moves the graphic back, **sets the constraint solver's state to the previous state, and finally tells the constraint solver to solve** the constraints."

## Worked Example
**Memento as an iteration mechanism — Dylan collections.**

"Collections in Dylan provide an **iteration interface that reflects the Memento pattern**. Dylan's collections have the notion of a '**state**' object, which is a memento that represents the state of the iteration. **Each collection can represent the current state of the iteration in any way it chooses; the representation is completely hidden from clients.**"

```cpp
template <class Item>
class Collection {
public:
    Collection();

    IterationState* CreateInitialState();
    void Next(IterationState*);
    bool IsDone(const IterationState*) const;
    Item CurrentItem(const IterationState*) const;
    IterationState* Copy(const IterationState*) const;

    void Append(const Item&);
    void Remove(const Item&);
    // ...
};
```
- `CreateInitialState` returns an initialized state object. `Next` "effectively increments the iteration index." `Copy` "returns a copy of the given state object. **This is useful for marking a point in an iteration.**"

```cpp
class ItemType {
public:
    void Process();
    // ...
};

Collection<ItemType*> aCollection;
IterationState* state;

state = aCollection.CreateInitialState();

while (!aCollection.IsDone(state)) {
    aCollection.CurrentItem(state)->Process();
    aCollection.Next(state);
}

delete state;
```
- ⚠️ GoF's own footnote on this code: "our example **deletes the state object at the end** of the iteration. But `delete` **won't get called if `ProcessItem` throws an exception, thus creating garbage.** This is a problem in C++ but not in Dylan, which has garbage collection."

**Two benefits of memento-based iteration:**
1. "**More than one state can work on the same collection.** (The same is true of the Iterator pattern.)"
2. "**It doesn't require breaking a collection's encapsulation to support iteration.** The memento is only interpreted by the collection itself; no one else has access to it. Other approaches to iteration require breaking encapsulation by making **iterator classes friends of their collection classes**. **The situation is reversed in the memento-based implementation: `Collection` is a friend of the `IterationState`.**"

## Known Uses
- **Unidraw's `CSolver`** — the source of the sample code's connectivity support.
- **Dylan collections** — the memento-based iteration interface above.
- **QOCA constraint-solving toolkit** — "stores **incremental** information in mementos. Clients can obtain a memento that characterizes the current solution to a system of constraints. **The memento contains only those constraint variables that have changed since the last solution.** Usually only a small subset of the solver's variables changes for each new solution."
  - ⚠️ The constraint that incrementality imposes: "This subset is enough to return the solver to the **preceding** solution; reverting to **earlier** solutions requires restoring mementos from the intervening solutions. **Hence you can't set mementos in any order; QOCA relies on a history mechanism to revert to earlier solutions.**"

## Related Patterns
- "**Command**: Commands can use mementos to maintain state for undoable operations."
- "**Iterator**: Mementos can be used for iteration as described earlier."

## Connects To
- **Ch 19 (Command)**: Implementation issue 3 — "**Errors can accumulate as commands are executed, unexecuted, and reexecuted** repeatedly so that an application's state eventually diverges from original values... The Memento pattern can be applied to give the command access to this information without exposing the internals of other objects."
- **Ch 21 (Iterator)**: the external-iterator alternative that keeps the traversal state in the client rather than in an iterator object.
- **Ch 8 (Singleton)**: `ConstraintSolver` in the sample code.
- **Command, Iterator, Singleton**
