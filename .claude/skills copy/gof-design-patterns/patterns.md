# The 23 Patterns — Index

Every pattern's verbatim **Intent**, its classification, its page in the book, and the chapter file holding the full treatment (Motivation, Applicability, Participants, Collaborations, Consequences, Implementation, Sample Code, Known Uses, Related Patterns).

## Classification (Table 1.1)

| | **Creational** | **Structural** | **Behavioral** |
|---|---|---|---|
| **Class scope** | Factory Method | Adapter (class) | Interpreter, Template Method |
| **Object scope** | Abstract Factory, Builder, Prototype, Singleton | Adapter (object), Bridge, Composite, Decorator, Facade, Flyweight, Proxy | Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Visitor |

**Scope** — class patterns use **inheritance** and are fixed at compile-time; object patterns use **composition** and can change at run-time.

---

## Creational Patterns *(ch03)*

| Pattern | Intent | File | p. |
|---|---|---|---|
| **Abstract Factory** | "Provide an interface for creating families of related or dependent objects without specifying their concrete classes." | [ch04](chapters/ch04-abstract-factory.md) | 87 |
| **Builder** | "Separate the construction of a complex object from its representation so that the same construction process can create different representations." | [ch05](chapters/ch05-builder.md) | 97 |
| **Factory Method** | "Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses." | [ch06](chapters/ch06-factory-method.md) | 107 |
| **Prototype** | "Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype." | [ch07](chapters/ch07-prototype.md) | 117 |
| **Singleton** | "Ensure a class only has one instance, and provide a global point of access to it." | [ch08](chapters/ch08-singleton.md) | 127 |

## Structural Patterns *(ch09)*

| Pattern | Intent | File | p. |
|---|---|---|---|
| **Adapter** | "Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces." | [ch10](chapters/ch10-adapter.md) | 139 |
| **Bridge** | "Decouple an abstraction from its implementation so that the two can vary independently." | [ch11](chapters/ch11-bridge.md) | 151 |
| **Composite** | "Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly." | [ch12](chapters/ch12-composite.md) | 163 |
| **Decorator** | "Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality." | [ch13](chapters/ch13-decorator.md) | 175 |
| **Facade** | "Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use." | [ch14](chapters/ch14-facade.md) | 185 |
| **Flyweight** | "Use sharing to support large numbers of fine-grained objects efficiently." | [ch15](chapters/ch15-flyweight.md) | 195 |
| **Proxy** | "Provide a surrogate or placeholder for another object to control access to it." | [ch16](chapters/ch16-proxy.md) | 207 |

## Behavioral Patterns *(ch17)*

| Pattern | Intent | File | p. |
|---|---|---|---|
| **Chain of Responsibility** | "Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it." | [ch18](chapters/ch18-chain-of-responsibility.md) | 223 |
| **Command** | "Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations." | [ch19](chapters/ch19-command.md) | 233 |
| **Interpreter** | "Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language." | [ch20](chapters/ch20-interpreter.md) | 243 |
| **Iterator** | "Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation." | [ch21](chapters/ch21-iterator.md) | 257 |
| **Mediator** | "Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly, and it lets you vary their interaction independently." | [ch22](chapters/ch22-mediator.md) | 273 |
| **Memento** | "Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later." | [ch23](chapters/ch23-memento.md) | 283 |
| **Observer** | "Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically." | [ch24](chapters/ch24-observer.md) | 293 |
| **State** | "Allow an object to alter its behavior when its internal state changes. The object will appear to change its class." | [ch25](chapters/ch25-state.md) | 305 |
| **Strategy** | "Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it." | [ch26](chapters/ch26-strategy.md) | 315 |
| **Template Method** | "Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure." | [ch27](chapters/ch27-template-method.md) | 325 |
| **Visitor** | "Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates." | [ch28](chapters/ch28-visitor.md) | 331 |

---

## Also Known As

| Pattern | Other names |
|---|---|
| Adapter | Wrapper |
| Command | Action, Transaction |
| Decorator | Wrapper |
| Memento | Token |
| Observer | Dependents, Publish-Subscribe |
| Prototype | *(none)* |
| State | Objects for States |
| Strategy | Policy |

**Rename history** (Ch 6.2): "Wrapper" → **Decorator**, "Glue" → **Facade**, "Solitaire" → **Singleton**, "Walker" → **Visitor**.

---

## Supporting material

- [chapters/ch01-introduction.md](chapters/ch01-introduction.md) — what a pattern is, the classification, "program to an interface, not an implementation", inheritance vs. composition, delegation, the 8 causes of redesign, how to select and use a pattern.
- [chapters/ch02-case-study-document-editor.md](chapters/ch02-case-study-document-editor.md) — Lexi: seven design problems solved with eight patterns, end to end.
- [chapters/ch03-creational-patterns.md](chapters/ch03-creational-patterns.md), [ch09](chapters/ch09-structural-patterns.md), [ch17](chapters/ch17-behavioral-patterns.md) — category introductions and their closing discussions.
- [chapters/ch29-behavioral-discussion.md](chapters/ch29-behavioral-discussion.md) — encapsulating variation, objects as arguments, Mediator vs. Observer, the sender/receiver decoupling spectrum.
- [chapters/ch30-conclusion.md](chapters/ch30-conclusion.md) — patterns as vocabulary, as documentation, as refactoring targets.
- [glossary.md](glossary.md) — the book's Appendix A definitions plus the Appendix B notation key.
- [cheatsheet.md](cheatsheet.md) — selection tables, confusable pairs, anti-patterns.
