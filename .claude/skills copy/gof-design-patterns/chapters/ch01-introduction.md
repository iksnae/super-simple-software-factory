# Chapter 1: Introduction

## Core Idea
Expert designers "do not solve every problem from first principles" — they reuse solutions that worked before. A design pattern **names, abstracts, and identifies the key aspects of a common design structure** so that experience can be reused instead of rediscovered.

## Frameworks Introduced
- **Christopher Alexander's definition**, which GoF adopts: "Each pattern describes a problem which occurs over and over again in our environment, and then describes the core of the solution to that problem, in such a way that you can use this solution a million times over, without ever doing it the same way twice." GoF's solutions are "expressed in terms of objects and interfaces instead of walls and doors, but at the core of both kinds of patterns is **a solution to a problem in a context**."
- **The four essential elements of a pattern**:
  1. **Pattern name** — "a handle we can use to describe a design problem, its solutions, and consequences in a word or two. Naming a pattern immediately increases our design vocabulary. It lets us design at a higher level of abstraction." *"Finding good names has been one of the hardest parts of developing our catalog."*
  2. **Problem** — when to apply the pattern; the context; sometimes a list of preconditions.
  3. **Solution** — "the elements that make up the design, their relationships, responsibilities, and collaborations." Not a concrete design — "a pattern is like a template that can be applied in many different situations."
  4. **Consequences** — "the results and trade-offs of applying the pattern... Though consequences are often unvoiced when we describe design decisions, they are **critical for evaluating design alternatives**."
- **The two principles of reusable object-oriented design** — the book's spine:
  - **"Program to an interface, not an implementation."** "Don't declare variables to be instances of particular concrete classes. Instead, commit only to an interface defined by an abstract class."
  - **"Favor object composition over class inheritance."**
- **Two classification criteria**: **purpose** (what the pattern does — creational, structural, behavioral) and **scope** (whether it applies primarily to **classes**, via inheritance, fixed at compile time, or to **objects**, changeable at run time). "Almost all patterns use inheritance to some extent. So the only patterns labeled 'class patterns' are those that focus on class relationships. Note that **most patterns are in the Object scope**."

## Key Concepts
- **What a design pattern is *not***: "not about designs such as linked lists and hash tables that can be encoded in classes and reused as is. Nor are they complex, domain-specific designs for an entire application or subsystem."
- **Nothing here is new**: "We have included only designs that have been **applied more than once in different systems**... They are either part of the folklore of the object-oriented community or are elements of some successful object-oriented systems."
- **What the book omits**: "no patterns dealing with concurrency or distributed programming or real-time programming... no application domain-specific patterns."
- **Class vs. type** — "An object's **class** defines how the object is implemented... an object's **type** only refers to its interface." Class inheritance is "a mechanism for code and representation sharing"; interface inheritance (subtyping) "describes when an object can be used in place of another." Many patterns depend on the distinction: Chain of Responsibility objects need a common type but usually not a common implementation; Command, Observer, State, and Strategy "are often implemented with abstract classes that are pure interfaces."
- **White-box vs. black-box reuse** — inheritance is white-box ("the internals of parent classes are often visible to subclasses"); composition is black-box ("no internal details of objects are visible").
- **"Inheritance breaks encapsulation"** [Sny86] — "parent classes often define at least part of their subclasses' physical representation... any change in the parent's implementation will force the subclass to change." One cure: "inherit only from abstract classes, since they usually provide little or no implementation."
- **Delegation** — "two objects are involved in handling a request: a receiving object delegates operations to its delegate... the receiver passes itself to the delegate." A `Window` *has* a `Rectangle` rather than *being* one, and "can become circular at run-time simply by replacing its Rectangle instance with a Circle instance."
  - The cost: "Dynamic, highly parameterized software is **harder to understand** than more static software... Delegation is a good design choice only when it simplifies more than it complicates. **Delegation works best when it's used in highly stylized ways — that is, in standard patterns.**"
- **Aggregation vs. acquaintance** — aggregation "implies that one object **owns or is responsible for** another" and that both "have identical lifetimes"; acquaintance implies an object "merely **knows of**" another. "Ultimately, acquaintance and aggregation are determined **more by intent than by explicit language mechanisms**."
- **Run-time vs. compile-time structure** — "An object-oriented program's run-time structure often bears little resemblance to its code structure... Trying to understand one from the other is like trying to understand the dynamism of living ecosystems from the static taxonomy of plants and animals." Therefore "**the system's run-time structure must be imposed more by the designer than the language**."
- **Application vs. toolkit vs. framework** — a **toolkit** is "a set of related and reusable classes designed to provide useful, general-purpose functionality... the object-oriented equivalent of subroutine libraries," emphasizing **code reuse**. A **framework** is "a set of cooperating classes that make up a reusable design for a specific class of software," emphasizing **design reuse**, and it "dictates the architecture of your application."
  - **Inversion of control**: "When you use a toolkit... you write the main body of the application and call the code you want to reuse. When you use a framework, **you reuse the main body and write the code it calls**."
  - Difficulty ranking: "If applications are hard to design, and toolkits are harder, then **frameworks are hardest of all**."

## Reference Tables

### Table 1.1 — Design pattern space

| Scope | Creational | Structural | Behavioral |
|---|---|---|---|
| **Class** | Factory Method | Adapter (class) | Interpreter, Template Method |
| **Object** | Abstract Factory, Builder, Prototype, Singleton | Adapter (object), Bridge, Composite, Decorator, Facade, Flyweight, Proxy | Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Visitor |

### The thirteen-section template
Pattern Name and Classification · **Intent** · Also Known As · **Motivation** · **Applicability** · **Structure** · **Participants** · **Collaborations** · **Consequences** · **Implementation** · **Sample Code** · **Known Uses** ("at least two examples from different domains") · **Related Patterns**

### Table 1.2 — What each pattern lets you vary

| Pattern | Aspect(s) that can vary |
|---|---|
| Abstract Factory | families of product objects |
| Builder | how a composite object gets created |
| Factory Method | subclass of object that is instantiated |
| Prototype | class of object that is instantiated |
| Singleton | the sole instance of a class |
| Adapter | interface to an object |
| Bridge | implementation of an object |
| Composite | structure and composition of an object |
| Decorator | responsibilities of an object without subclassing |
| Facade | interface to a subsystem |
| Flyweight | storage costs of objects |
| Proxy | how an object is accessed; its location |
| Chain of Responsibility | object that can fulfill a request |
| Command | when and how a request is fulfilled |
| Interpreter | grammar and interpretation of a language |
| Iterator | how an aggregate's elements are accessed, traversed |
| Mediator | how and which objects interact with each other |
| Memento | what private information is stored outside an object, and when |
| Observer | number of objects that depend on another object; how the dependents stay up to date |
| State | states of an object |
| Strategy | an algorithm |
| Template Method | steps of an algorithm |
| Visitor | operations applicable to object(s) without changing their class(es) |

### The eight causes of redesign, and the patterns that address them

| # | Cause | Patterns |
|---|---|---|
| 1 | **Creating an object by specifying a class explicitly** — commits you to an implementation instead of an interface | Abstract Factory, Factory Method, Prototype |
| 2 | **Dependence on specific operations** — commits you to one way of satisfying a request | Chain of Responsibility, Command |
| 3 | **Dependence on hardware and software platform** | Abstract Factory, Bridge |
| 4 | **Dependence on object representations or implementations** | Abstract Factory, Bridge, Memento, Proxy |
| 5 | **Algorithmic dependencies** — algorithms likely to change should be isolated | Builder, Iterator, Strategy, Template Method, Visitor |
| 6 | **Tight coupling** — "leads to monolithic systems... a dense mass that's hard to learn, port, and maintain" | Abstract Factory, Bridge, Chain of Responsibility, Command, Facade, Mediator, Observer |
| 7 | **Extending functionality by subclassing** — fixed overhead per class, deep knowledge of the parent required, "explosion of classes" | Bridge, Chain of Responsibility, Composite, Decorator, Observer, Strategy |
| 8 | **Inability to alter classes conveniently** — no source, or too many subclasses to modify | Adapter, Decorator, Visitor |

## Worked Example
**Smalltalk MVC, read as three patterns.** The clearest short demonstration of what "pattern" means. MVC has three object kinds: the **Model** (the application object), the **View** (its screen presentation), and the **Controller** (how the UI reacts to input). "Before MVC, user interface designs tended to lump these objects together."

Now extract the general designs hiding inside it:

1. **Model ↔ View is Observer.** MVC "decouples views and models by establishing a subscribe/notify protocol." A model with three views — spreadsheet, histogram, pie chart — notifies them all when its data changes. "Taken at face value, this example reflects a design that decouples views from models. But the design is applicable to a **more general problem: decoupling objects so that changes to one can affect any number of others without requiring the changed object to know details of the others**." That is **Observer**.

2. **Nested views is Composite.** A control panel of buttons is a complex view containing nested button views; `CompositeView` is a subclass of `View`, so "a composite view can be used wherever a view can be used, but it also contains and manages nested views." Generalized: "whenever we want to **group objects and treat the group like an individual object**." That is **Composite**.

3. **View ↔ Controller is Strategy.** "A view uses an instance of a Controller subclass to implement a particular response strategy; to implement a different strategy, simply replace the instance with a different kind of controller. It's even possible to change a view's controller at run-time... a view can be disabled so that it doesn't accept input simply by giving it a controller that ignores input events." A Strategy "is an object that represents an algorithm."

MVC also uses **Factory Method** (to specify a view's default controller class) and **Decorator** (to add scrolling), "but the main relationships in MVC are given by the Observer, Composite, and Strategy design patterns."

**Six ways to find the right pattern (§1.7)**:
1. Consider **how design patterns solve design problems** (§1.6).
2. **Scan Intent sections** — all 23 intents are listed in §1.4; narrow with the Table 1.1 classification.
3. **Study how patterns interrelate** (Figure 1.1).
4. **Study patterns of like purpose** — each catalog chapter opens with introductory comments and closes with a comparison section.
5. **Examine a cause of redesign** — the eight causes above.
6. **Consider what should be variable in your design** — "the opposite of focusing on the causes of redesign... The focus here is on **encapsulating the concept that varies**." Use Table 1.2.

**Seven steps to apply one (§1.8)**:
1. Read it once through, paying "particular attention to the **Applicability and Consequences** sections."
2. Study **Structure, Participants, and Collaborations**.
3. Look at **Sample Code**.
4. **Choose meaningful participant names** — pattern names "are usually too abstract to appear directly in an application," but incorporate them: `SimpleLayoutStrategy`, `TeXLayoutStrategy`.
5. **Define the classes** — interfaces, inheritance, instance variables; identify existing classes the pattern affects.
6. **Define application-specific operation names** — be consistent, e.g. a `Create-` prefix for factory methods.
7. **Implement the operations** to carry out the responsibilities and collaborations.

**And how *not* to use them**: "Design patterns should not be applied indiscriminately. Often they achieve flexibility and variability by **introducing additional levels of indirection**, and that can complicate a design and/or cost you some performance. **A design pattern should only be applied when the flexibility it affords is actually needed.**"

## Key Takeaways
1. A pattern has four elements: name, problem, solution, consequences — and the consequences are what let you evaluate alternatives.
2. Naming is the point. A shared vocabulary lets you design and argue at a higher level of abstraction.
3. Program to an interface, not an implementation; favor object composition over class inheritance.
4. Classify by purpose (creational/structural/behavioral) and scope (class/object); most patterns are object-scope.
5. Distinguish class from type, and implementation inheritance from interface inheritance — many patterns depend on it.
6. Inheritance breaks encapsulation and is fixed at compile time; composition preserves it and is changeable at run time.
7. Delegation makes composition as powerful as inheritance, at the cost of comprehensibility — use it in stylized ways.
8. Run-time structure is imposed by the designer, not revealed by the code.
9. Find a pattern via intents, relationships, causes of redesign, or by asking what should be variable.
10. Patterns buy flexibility with indirection. Apply one only when you actually need the flexibility.

## Connects To
- **Ch 2 (Case Study)**: eight patterns applied to one real design, in sequence.
- **Ch 3–5**: the catalog, organized by the purpose classification defined here.
- **Ch 6 (Conclusion)**: what to expect from design patterns.
- **Observer, Composite, Strategy, Factory Method, Decorator**: the five patterns inside MVC.
