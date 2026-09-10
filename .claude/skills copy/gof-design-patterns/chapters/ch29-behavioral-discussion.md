# Discussion of Behavioral Patterns *(end of Chapter 5)*

## Core Idea
The eleven behavioral patterns are not eleven unrelated tricks. They divide along a few axes: **what variation gets encapsulated**, **whether an object is passed as an argument**, and **whether communication is centralized or distributed**.

## Encapsulating Variation
"When an aspect of a program **changes frequently**, these patterns define an object that encapsulates that aspect... **the pattern derives its name from that object**."

| Pattern | What the object encapsulates |
|---|---|
| **Strategy** | "an algorithm" |
| **State** | "a state-dependent behavior" |
| **Mediator** | "the protocol between objects" |
| **Iterator** | "the way you access and traverse the components of an aggregate" |

"Most patterns have **two kinds of objects**: the new object(s) that encapsulate the aspect, and the existing object(s) that use the new ones. **Usually the functionality of new objects would be an integral part of the existing objects were it not for the pattern.** For example, **code for a Strategy would probably be wired into the strategy's Context**, and code for a State would be implemented directly in the state's Context."

GoF's footnote extends the theme past this chapter: "**Abstract Factory, Builder, and Prototype all encapsulate knowledge about how objects are created. Decorator encapsulates responsibility that can be added to an object. Bridge separates an abstraction from its implementation**, letting them vary independently."

⚠️ **The exception**: "**not all object behavioral patterns partition functionality like this**. For example, **Chain of Responsibility deals with an arbitrary number of objects (i.e., a chain), all of which may already exist in the system**... **Not all define static communication relationships between classes.** Chain of Responsibility prescribes communication between an **open-ended** number of objects."

## Objects as Arguments
- **Visitor** — "A Visitor object is the argument to a polymorphic `Accept` operation on the objects it visits. **The visitor is never considered a part of those objects**, even though the conventional alternative to the pattern is to distribute Visitor code across the object structure classes."
- **Command** and **Memento** — "objects that act as **magic tokens** to be passed around and invoked at a later time... **In Command, the token represents a request; in Memento, it represents the internal state of an object at a particular time.** In both cases, the token can have a complex internal representation, **but the client is never aware of it**."
- ⚠️ The difference between the two tokens: "**Polymorphism is important in the Command pattern**, because executing the Command object is a polymorphic operation. In contrast, **the Memento interface is so narrow that a memento can only be passed as a value. So it's likely to present no polymorphic operations at all to its clients.**"

## Should Communication Be Encapsulated or Distributed?
"**Mediator and Observer are competing patterns.** The difference is that **Observer *distributes* communication** by introducing Observer and Subject objects, whereas **a Mediator object *encapsulates* the communication** between other objects."

"In the Observer pattern, **there is no single object that encapsulates a constraint**. Instead, the Observer and the Subject must **cooperate** to maintain the constraint... **The Mediator pattern centralizes rather than distributes. It places the responsibility for maintaining a constraint squarely in the mediator.**"

The verdict, stated as experience rather than rule:

| | Observer | Mediator |
|---|---|---|
| **Reusability** | "**We've found it easier to make reusable Observers and Subjects than to make reusable Mediators.**" Promotes "partitioning and loose coupling... **finer-grained classes that are more apt to be reused**" | Harder to reuse — the mediator encodes one specific protocol |
| **Comprehensibility** | ⚠️ "Observers and subjects are usually **connected shortly after they're created, and it's hard to see how they are connected later** in the program... **the indirection that Observer introduces will still make a system harder to understand**" | "**it's easier to understand the flow of communication in Mediator than in Observer**" |

⚠️ **The language dependency**: "**Observers in Smalltalk can be parameterized with messages to access the Subject state, and so they are even more reusable than they are in C++.** This makes Observer more attractive than Mediator in Smalltalk. **Thus a Smalltalk programmer will often use Observer where a C++ programmer would use Mediator.**"

## Decoupling Senders and Receivers
"**Command, Observer, Mediator, and Chain of Responsibility address how you can decouple senders and receivers, but with different trade-offs.**"

| Pattern | Mechanism | Trade-off |
|---|---|---|
| **Command** | "a Command object defines the **binding** between a sender and receiver"; "provides a simple interface for issuing the request (the `Execute` operation)" | "**lets the sender work with different receivers**... you can reuse the Command object to parameterize a receiver with different senders." ⚠️ "**nominally requires a subclass for each sender-receiver connection**, although the pattern describes implementation techniques that avoid subclassing" |
| **Observer** | "defines an **interface for signaling changes** in subjects" | "a **looser** sender-receiver binding than Command, since a subject may have **multiple observers, and their number can vary at run-time**"; "**best for decoupling objects when there are data dependencies between them**" |
| **Mediator** | "objects refer to each other **indirectly** through a Mediator object" | "**can reduce subclassing**, because it centralizes communication behavior in one class instead of distributing it among subclasses." ⚠️ "Because this interface is fixed, the Mediator **might have to implement its own dispatching scheme**... **ad hoc dispatching schemes often decrease type safety**" |
| **Chain of Responsibility** | "passing the request along a **chain of potential receivers**" | ⚠️ "**may also require a custom dispatching scheme. Hence it has the same type-safety drawbacks as Mediator.**" Best "**if the chain is already part of the system's structure**, and one of several objects may be in a position to handle the request"; "the chain can be **changed or extended easily**" |

## Summary — patterns compose
"**With few exceptions, behavioral design patterns complement and reinforce each other.**"

Within the chapter:
- "A class in a **chain of responsibility** will probably include at least one application of **Template Method**. The template method can use primitive operations to determine **whether the object should handle the request** and to **choose the object to forward to**."
- "The chain can use the **Command** pattern to represent requests as objects."
- "**Interpreter** can use the **State** pattern to define **parsing contexts**."
- "An **iterator** can traverse an aggregate, and a **visitor** can apply an operation to each element in the aggregate."

Across chapters, all on one **Composite** structure:
- "use a **visitor** to perform operations on components of the composition"
- "use **Chain of Responsibility** to let components **access global properties through their parent**"
- "use **Decorator** to **override these properties on parts** of the composition"
- "use the **Observer** pattern to **tie one object structure to another**"
- "use the **State** pattern to let a component change its behavior as its state changes"
- "The composition itself might be **created using Builder**, and it might be **treated as a Prototype** by some other part of the system."

**The closing claim**: "**Well-designed object-oriented systems are just like this — they have multiple patterns embedded in them — but not because their designers necessarily thought in these terms. Composition at the pattern level rather than the class or object levels lets us achieve the same synergy with greater ease.**"

## Key Takeaways
1. Ask **what varies** first; the behavioral pattern is usually named after the object you would create to hold that variation.
2. Command and Memento are both tokens passed around and used later — but Command is polymorphic and Memento is opaque and passed by value.
3. Mediator and Observer solve the same problem in opposite directions: centralize the protocol, or distribute it. Reuse favors Observer; comprehensibility favors Mediator.
4. Command, Observer, Mediator, and Chain of Responsibility form a spectrum of sender/receiver decoupling — tightest binding to loosest, with type safety decreasing as the dispatching gets more ad hoc.
5. Fixed sender/receiver interfaces push systems toward custom dispatching schemes; that is where type safety is lost, in both Mediator and Chain of Responsibility.
6. Real systems layer several patterns on one structure. Compose at the pattern level, not the class level.

## Connects To
- **Ch 17 (Behavioral Patterns intro)**: the category's class/object split and the encapsulation table.
- **Ch 22 (Mediator)** and **Ch 24 (Observer)**: the competing pair analyzed here.
- **Ch 18 (Chain of Responsibility)**, **Ch 19 (Command)**, **Ch 23 (Memento)**, **Ch 27 (Template Method)**.
- **Ch 30 (Conclusion)**: the book's closing argument about a shared design vocabulary.
