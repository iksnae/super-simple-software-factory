# Command
*Object Behavioral · Also Known As: **Action**, **Transaction** · GoF p. 233*

## Intent
> **Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.**

## Motivation
"Sometimes it's necessary to issue requests to objects **without knowing anything about the operation being requested or the receiver** of the request."

The toolkit designer's bind: "the toolkit can't implement the request explicitly in the button or menu, because **only applications that use the toolkit know what should be done on which object**. As toolkit designers we have no way of knowing the receiver of the request or the operations that will carry it out."

"The Command pattern lets toolkit objects make requests of unspecified application objects by **turning the request itself into an object**... Concrete Command subclasses specify a **receiver-action pair** by storing the receiver as an instance variable and by implementing `Execute` to invoke the request."

Two contrasting commands show the range:
- **`PasteCommand`** — "receiver is the `Document` object it is supplied upon instantiation. The `Execute` operation invokes `Paste` on the receiving `Document`." A pure binding.
- **`OpenCommand`** — "prompts the user for a document name, creates a corresponding `Document` object, adds the document to the receiving application, and opens the document." Substantially more work.
- **`MacroCommand`** — "a concrete Command subclass that simply executes a sequence of Commands. **MacroCommand has no explicit receiver, because the commands it sequences define their own receiver.**"

**The payoff**: "An application can provide **both a menu and a push button interface to a feature just by making them share an instance of the same concrete Command subclass**. We can replace commands dynamically, which would be useful for implementing **context-sensitive menus**. We can also support **command scripting** by composing commands into larger ones. All of this is possible because **the object that issues a request only needs to know how to issue it; it doesn't need to know how the request will be carried out.**"

## Applicability
Use Command when you want to:
- **"parameterize objects by an action to perform."** "You can express such parameterization in a procedural language with a **callback** function... **Commands are an object-oriented replacement for callbacks.**"
- **"specify, queue, and execute requests at different times."** "A Command object can have a **lifetime independent of the original request**. If the receiver can be represented in an address space-independent way, then you can **transfer a command object to a different process and fulfill the request there**."
- **"support undo."** "Executed commands are stored in a **history list**. Unlimited-level undo and redo is achieved by traversing this list backwards and forwards calling `Unexecute` and `Execute`."
- **"support logging changes so that they can be reapplied in case of a system crash."** "By augmenting the Command interface with **load and store** operations, you can keep a persistent log... **Recovering from a crash involves reloading logged commands from disk and reexecuting them.**"
- **"structure a system around high-level operations built on primitive operations."** "Such a structure is common in information systems that support **transactions**. A transaction encapsulates a set of changes to data... Commands have a common interface, letting you **invoke all transactions the same way**."

## Participants
- **Command** — declares an interface for executing an operation.
- **ConcreteCommand** (`PasteCommand`, `OpenCommand`) — "defines a **binding between a Receiver object and an action**"; implements `Execute` by invoking operation(s) on Receiver.
- **Client** (`Application`) — creates a ConcreteCommand and **sets its receiver**.
- **Invoker** (`MenuItem`) — asks the command to carry out the request.
- **Receiver** (`Document`, `Application`) — knows how to perform the operations. **"Any class may serve as a Receiver."**

## Collaborations
- Client creates the ConcreteCommand and specifies its receiver → Invoker stores it → Invoker calls `Execute` → ConcreteCommand invokes operations on its receiver.
- "**When commands are undoable, ConcreteCommand stores state for undoing the command *prior to* invoking `Execute`.**"

## Consequences
1. "Command **decouples the object that invokes the operation from the one that knows how to perform it**."
2. "Commands are **first-class objects**. They can be manipulated and extended like any other object."
3. "You can assemble commands into a **composite command**... In general, composite commands are an instance of the **Composite** pattern."
4. "It's **easy to add new Commands**, because you don't have to change existing classes."

## Implementation
1. **How intelligent should a command be?** "A command can have a **wide range of abilities**. At one extreme it merely defines a **binding** between a receiver and the actions... At the other extreme it **implements everything itself without delegating to a receiver at all**."
   - When the far extreme is right: "when you want to define commands that are **independent of existing classes**, when **no suitable receiver exists**, or when a command **knows its receiver implicitly**. For example, a command that creates another application window may be just as capable of creating the window as any other object."
   - "Somewhere in between these extremes are commands that have enough knowledge to **find their receiver dynamically**."
2. **Supporting undo and redo.** A ConcreteCommand may need to store: "the **Receiver** object... the **arguments** to the operation performed on the receiver, and **any original values in the receiver that can change** as a result of handling the request. **The receiver must provide operations that let the command return the receiver to its prior state.**"
   - "To support **one level** of undo, an application needs to store only the command that was executed last. For **multiple-level** undo and redo, the application needs a **history list**, where the maximum length of the list determines the number of undo/redo levels."
   - ⚠️ **The copying subtlety**: "An undoable command **might have to be copied** before it can be placed on the history list. That's because the command object that carried out the original request, say, from a `MenuItem`, will perform other requests at later times."
     - "For example, a `DeleteCommand` that deletes selected objects must store **different sets of objects each time it's executed**. Therefore the `DeleteCommand` object must be copied following execution... **If the command's state never changes on execution, then copying is not required** — only a reference need be placed on the history list. **Commands that must be copied before being placed on the history list act as prototypes.**"
3. ⚠️ **Avoiding error accumulation in the undo process.** "**Hysteresis** can be a problem in ensuring a reliable, semantics-preserving undo/redo mechanism. **Errors can accumulate as commands are executed, unexecuted, and reexecuted repeatedly so that an application's state eventually diverges from original values.** It may be necessary therefore to store more information in the command... **The Memento pattern can be applied** to give the command access to this information without exposing the internals of other objects."
4. **Using C++ templates.** "For commands that (1) **aren't undoable** and (2) **don't require arguments**, we can use C++ templates to avoid creating a Command subclass for every kind of action and receiver."

## Sample Code

```cpp
class Command {
public:
    virtual ~Command();
    virtual void Execute() = 0;
protected:
    Command();
};
```

The two ends of the intelligence spectrum:

```cpp
class OpenCommand : public Command {
public:
    OpenCommand(Application*);
    virtual void Execute();
protected:
    virtual const char* AskUser();
private:
    Application* _application;
    char* _response;
};

void OpenCommand::Execute () {
    const char* name = AskUser();

    if (name != 0) {
        Document* document = new Document(name);
        _application->Add(document);
        document->Open();
    }
}
```
```cpp
class PasteCommand : public Command {
public:
    PasteCommand(Document*);
    virtual void Execute();
private:
    Document* _document;
};

void PasteCommand::Execute () {
    _document->Paste();
}
```

The template that eliminates trivial subclasses — a member-function pointer plus a receiver:

```cpp
template <class Receiver>
class SimpleCommand : public Command {
public:
    typedef void (Receiver::* Action)();

    SimpleCommand(Receiver* r, Action a) :
        _receiver(r), _action(a) { }

    virtual void Execute();
private:
    Action _action;
    Receiver* _receiver;
};

template <class Receiver>
void SimpleCommand<Receiver>::Execute () {
    (_receiver->*_action)();
}
```
```cpp
MyClass* receiver = new MyClass;
// ...
Command* aCommand =
    new SimpleCommand<MyClass>(receiver, &MyClass::Action);
// ...
aCommand->Execute();
```
- ⚠️ "Keep in mind that **this solution only works for simple commands**. More complex commands that keep track of not only their receivers but also arguments and/or undo state require a Command subclass."

The composite command:

```cpp
class MacroCommand : public Command {
public:
    MacroCommand();
    virtual ~MacroCommand();

    virtual void Add(Command*);
    virtual void Remove(Command*);

    virtual void Execute();
private:
    List<Command*>* _cmds;
};

void MacroCommand::Execute () {
    ListIterator<Command*> i(_cmds);

    for (i.First(); !i.IsDone(); i.Next()) {
        Command* c = i.CurrentItem();
        c->Execute();
    }
}

void MacroCommand::Add (Command* c) { _cmds->Append(c); }
void MacroCommand::Remove (Command* c) { _cmds->Remove(c); }
```
- ⚠️ **The ordering rule**: "should the `MacroCommand` implement an `Unexecute` operation, then its subcommands must be **unexecuted in reverse order** relative to `Execute`'s implementation."
- "The `MacroCommand` is also responsible for **deleting** its subcommands."

## Known Uses
- **Lieberman (1985)** — "Perhaps the first example of the Command pattern."
- **MacApp** — "**popularized the notion of commands for implementing undoable operations**."
- **InterViews** — "defines an `Action` abstract class... also defines an **`ActionCallback` template, parameterized by action method, that can instantiate command subclasses automatically**."
- **THINK class library** — "Commands in THINK are called '**Tasks**.' Task objects are passed along a **Chain of Responsibility** for consumption."
- **Unidraw** — "unique in that its command objects **can behave like messages**. A Unidraw command may be sent to another object for interpretation, and **the result of the interpretation varies with the receiving object**. Moreover, the receiver may delegate the interpretation to another object, typically the receiver's parent... **The receiver of a Unidraw command is thus computed rather than stored.**"
- **Coplien's functors** — "objects that are functions... He achieves a degree of transparency by **overloading the function call operator**. **The Command pattern is different; its focus is on maintaining a binding between a receiver and a function (i.e., action), not just maintaining a function.**"

## Related Patterns
- "A **Composite** can be used to implement MacroCommands."
- "A **Memento** can keep state the command requires to undo its effect."
- "A command that must be copied before being placed on the history list acts as a **Prototype**."

## Connects To
- **Ch 2 (Case Study, §2.7)**: Lexi's commands, the `Reversible` operation, and the command-history diagram — the pattern derived from the problem.
- **Ch 1**: causes of redesign #2 (dependence on specific operations) and #6 (tight coupling).
- **Ch 5 (Behavioral Patterns)**: Command "encapsulates a request in an object so that it can be passed as a parameter, stored on a history list, or manipulated in other ways."
- **Composite, Memento, Prototype, Chain of Responsibility**
