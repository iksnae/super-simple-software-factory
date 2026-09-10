# Chapter 5: Behavioral Patterns *(category introduction)*

## Core Idea
Behavioral patterns "are concerned with **algorithms and the assignment of responsibilities between objects**" — and describe "not just patterns of objects or classes but also **the patterns of communication between them**."

## Frameworks Introduced
- **What behavioral patterns do for comprehension**: "These patterns characterize **complex control flow that's difficult to follow at run-time**. They **shift your focus away from flow of control** to let you concentrate just on the way objects are interconnected."
- **Behavioral *class* patterns** — "use **inheritance** to distribute behavior between classes." There are only two:
  - **Template Method** — "the simpler and more common of the two. A template method is an **abstract definition of an algorithm**. It defines the algorithm step by step. **Each step invokes either an abstract operation or a primitive operation.** A subclass fleshes out the algorithm by defining the abstract operations."
  - **Interpreter** — "represents a **grammar as a class hierarchy** and implements an **interpreter as an operation** on instances of these classes."
- **Behavioral *object* patterns** — "use object composition rather than inheritance."
  - **The peer-coupling problem**: "Some describe how a group of peer objects cooperate to perform a task that no single object can carry out by itself. **An important issue here is how peer objects know about each other. Peers could maintain explicit references to each other, but that would increase their coupling. In the extreme, every object would know about every other.**"
  - **Mediator** "avoids this by introducing a mediator object between peers. **The mediator provides the indirection needed for loose coupling.**"
  - **Chain of Responsibility** "provides **even looser coupling**. It lets you send requests to an object **implicitly** through a chain of candidate objects. Any candidate may fulfill the request depending on run-time conditions. **The number of candidates is open-ended, and you can select which candidates participate in the chain at run-time.**"
  - **Observer** "defines and maintains a **dependency** between objects. The classic example is in Smalltalk Model/View/Controller, where all views of the model are notified whenever the model's state changes."

## Reference Table

The patterns that **encapsulate behavior in an object and delegate requests to it**:

| Pattern | What it encapsulates | Effect |
|---|---|---|
| **Strategy** | an algorithm | "makes it easy to **specify and change** the algorithm an object uses" |
| **Command** | a request | "so that it can be **passed as a parameter, stored on a history list**, or manipulated in other ways" |
| **State** | the states of an object | "so that the object can **change its behavior when its state object changes**" |
| **Visitor** | behavior "that would otherwise be **distributed across classes**" | new operations without changing element classes |
| **Iterator** | "the way you **access and traverse** objects in an aggregate" | traversal independent of representation |

The full set, by scope:

| Scope | Patterns |
|---|---|
| **Class** | Interpreter, Template Method |
| **Object** | Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Visitor |

## Key Takeaways
1. Behavioral patterns are about responsibility assignment and inter-object communication, not just structure.
2. They make hard-to-follow run-time control flow tractable by describing the interconnections instead.
3. Only two are class-scoped — Template Method and Interpreter — and both use inheritance to distribute behavior.
4. Peer-to-peer references couple objects combinatorially; Mediator centralizes the indirection, Chain of Responsibility loosens it further with implicit receivers.
5. A large sub-family works by encapsulating *some one thing* in an object: an algorithm, a request, a state, an operation, a traversal.

## Connects To
- **Ch 3 (Creational)** and **Ch 4 (Structural)**: the other category chapters.
- **Ch 29 (Discussion of Behavioral Patterns)**: encapsulating variation, objects as arguments, communication decoupling, and the receiver/sender comparison.
- **Ch 1**: the purpose/scope classification (Table 1.1).
