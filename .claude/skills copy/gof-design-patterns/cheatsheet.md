# Cheatsheet — Selecting and Applying Patterns

## 1. Pick by what varies *(Table 1.2)*

| Pattern | Aspect(s) that can vary |
|---|---|
| **Abstract Factory** | families of product objects |
| **Builder** | how a composite object gets created |
| **Factory Method** | subclass of object that is instantiated |
| **Prototype** | class of object that is instantiated |
| **Singleton** | the sole instance of a class |
| **Adapter** | interface to an object |
| **Bridge** | implementation of an object |
| **Composite** | structure and composition of an object |
| **Decorator** | responsibilities of an object without subclassing |
| **Facade** | interface to a subsystem |
| **Flyweight** | storage costs of objects |
| **Proxy** | how an object is accessed; its location |
| **Chain of Responsibility** | object that can fulfill a request |
| **Command** | when and how a request is fulfilled |
| **Interpreter** | grammar and interpretation of a language |
| **Iterator** | how an aggregate's elements are accessed, traversed |
| **Mediator** | how and which objects interact with each other |
| **Memento** | what private information is stored outside an object, and when |
| **Observer** | number of objects that depend on another object; how the dependent objects stay up to date |
| **State** | states of an object |
| **Strategy** | an algorithm |
| **Template Method** | steps of an algorithm |
| **Visitor** | operations that can be applied to object(s) without changing their class(es) |

## 2. Pick by the cause of redesign *(Ch 1)*

| Symptom | Patterns |
|---|---|
| Creating an object by specifying a class explicitly | Abstract Factory, Factory Method, Prototype |
| Dependence on specific operations | Chain of Responsibility, Command |
| Dependence on hardware and software platform | Abstract Factory, Bridge |
| Dependence on object representations or implementations | Abstract Factory, Bridge, Memento, Proxy |
| Algorithmic dependencies | Builder, Iterator, Strategy, Template Method, Visitor |
| Tight coupling | Abstract Factory, Bridge, Chain of Responsibility, Command, Facade, Mediator, Observer |
| Extending functionality by subclassing | Bridge, Chain of Responsibility, Composite, Decorator, Observer, Strategy |
| Inability to alter classes conveniently | Adapter, Decorator, Visitor |

## 3. Confusable pairs — the distinguishing question

| Pair | Ask |
|---|---|
| **Strategy vs. State** | Who chooses the object? **The client** (Strategy) or **the object's own state transitions** (State)? Structurally identical; the intent differs. |
| **Strategy vs. Template Method** | Vary the **whole** algorithm by delegation (Strategy), or **part** of it by inheritance (Template Method)? |
| **Adapter vs. Bridge** | Adapter fixes an **existing** interface mismatch after the fact. Bridge is designed **up front** so abstraction and implementation vary independently. |
| **Adapter vs. Decorator vs. Proxy** | Adapter **changes** the interface. Decorator **keeps** it and adds responsibilities. Proxy **keeps** it and controls access. |
| **Decorator vs. Composite** | Decorator has exactly one component and adds behavior; Composite aggregates many and adds nothing. Decorator is "a degenerate composite". |
| **Facade vs. Mediator** | Facade's protocol is **unidirectional** (clients → subsystem). Mediator's is **multidirectional** — it enables cooperation colleagues can't provide themselves. |
| **Mediator vs. Observer** | Centralize the protocol in one object (Mediator, easier to read) or distribute it across Subject/Observer (Observer, easier to reuse)? |
| **Abstract Factory vs. Builder** | Abstract Factory makes **families of products**, returning the product immediately. Builder constructs **one complex object step by step**, returning it at the end. |
| **Composite vs. Interpreter** | Same tree structure. It's Interpreter only when **you think of the class hierarchy as defining a language**. |
| **Iterator vs. Visitor** | Iterator needs a **common element type**; Visitor does not, and dispatches per concrete class. |
| **Command vs. Memento** | Both are tokens passed and used later. Command's execution is **polymorphic**; Memento's interface is so narrow it usually has **no polymorphic operations at all**. |

## 4. How to apply a pattern *(Ch 1, seven steps)*
1. "Read the pattern once through for an overview. **Pay particular attention to the Applicability and Consequences sections** to ensure the pattern is right for your problem."
2. "Study the **Structure, Participants, and Collaborations** sections."
3. "Look at the **Sample Code** section... Studying the code helps you learn how to implement the pattern."
4. "**Choose names for pattern participants that are meaningful in the application context.** The names for participants in design patterns are usually too abstract to appear directly in an application. Nevertheless, it's useful to **incorporate the participant name into the name that appears in the application**" — e.g. `SimpleLayoutStrategy`, `TeXLayoutStrategy`.
5. "**Define the classes.** Declare their interfaces, establish their inheritance relationships, and define the instance variables."
6. "**Define application-specific names for operations** in the pattern... be consistent in your naming conventions" — e.g. a consistent `Create-` prefix for factory methods.
7. "**Implement the operations** to carry out the responsibilities and collaborations in the pattern."

## 5. Anti-patterns

### The book's own warning
> "**Design patterns should not be applied indiscriminately. Often they achieve flexibility and variability by introducing additional levels of indirection, and that can complicate a design and/or cost you some performance. A design pattern should only be applied when the flexibility it affords is actually needed.** The Consequences sections are most helpful when evaluating a pattern's benefits and liabilities." *(Ch 1)*

### Practical failure modes
| Anti-pattern | Why it fails |
|---|---|
| **Applying patterns everywhere** (pattern obsession) | YAGNI. Indirection you don't need is cost without benefit. |
| **Stacking patterns** (Factory + Builder + Proxy on one object) | Complexity without benefit; each layer must earn its indirection separately. |
| **Not understanding the pattern before using it** | Cargo cult programming — the structure appears without the forces it resolves. |
| **Choosing a pattern by name, not problem** | The same name means different things in different libraries; match the **Applicability** section, not the label. |
| **Over-engineering simple problems with patterns** | Sometimes direct code is clearer. |

### Named liabilities, per pattern
| Pattern | The cost the book names |
|---|---|
| **Abstract Factory** | "Supporting new kinds of products is difficult" — extending the factory interface changes every subclass. |
| **Singleton** | A global point of access; hides dependencies and complicates testing and subclassing. |
| **Composite** | "It makes your design overly general" — it's hard to restrict which components a composite may hold, so type safety moves to run-time. |
| **Decorator** | "Lots of little objects"; a decorator and its component are **not identical**, so identity checks break. |
| **Flyweight** | Run-time cost of computing or transmitting extrinsic state may outweigh the storage saved. |
| **Mediator** | "It centralizes control" — the mediator can become a monolith harder to maintain than the interactions it replaced. |
| **Memento** | Expensive if state is large or checkpoints are frequent; the caretaker pays storage costs it can't see. |
| **Observer** | Unexpected updates — a cascade of dependent updates with no protocol saying what changed. |
| **Strategy** | Clients must understand how strategies differ; the shared interface passes data simple strategies never use. |
| **Chain of Responsibility** | "Receipt isn't guaranteed" — a request can fall off the end of the chain unhandled. |
| **Visitor** | "Adding new ConcreteElement classes is hard"; often forces public accessors that break element encapsulation. |
| **Interpreter** | "Complex grammars are hard to maintain" — at least one class per rule. |

## 6. The two foundational principles *(Ch 1)*
1. **"Program to an interface, not an implementation."**
2. **"Favor object composition over class inheritance."**

Inheritance is **white-box reuse** (compile-time, breaks encapsulation, "inheritance breaks encapsulation" when a subclass depends on parent internals). Composition is **black-box reuse** (run-time, defined only through interfaces, keeps each class focused on one task).
