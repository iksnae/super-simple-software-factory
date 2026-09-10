# Glossary — *Design Patterns: Elements of Reusable Object-Oriented Software*

Definitions marked with a quote are the book's own (Appendix A, Glossary). Entries without quotes are terms used throughout the catalog, defined from the chapter in which they appear.

## A
- **abstract class** — "A class whose primary purpose is to define an **interface**. An abstract class **defers some or all of its implementation to subclasses**. An abstract class cannot be instantiated."
- **abstract coupling** — "Given a class A that maintains a reference to an abstract class B, class A is said to be abstractly coupled to B. We call this abstract coupling because **A refers to a type of object, not a concrete object**." (Central to Observer, Bridge, Strategy.)
- **abstract operation** — "An operation that declares a signature but doesn't implement it. In C++, an abstract operation corresponds to a **pure virtual member function**."
- **abstract syntax tree** — the object structure built by **Interpreter** and traversed by **Visitor**; an instance of **Composite**.
- **acquaintance relationship** — "A class that refers to another class has an acquaintance with that class." (Weaker than aggregation; drawn as an arrow with no diamond.)
- **aggregate object** — "An object that's composed of subobjects. The subobjects are called the aggregate's **parts**, and **the aggregate is responsible for them**."
- **aggregation relationship** — "The relationship of an aggregate object to its parts."
- **aspect** (Observer) — a named event category an observer registers interest in, so the subject notifies only observers that care.

## B
- **black-box reuse** — "A style of reuse based on **object composition**. Composed objects **reveal no internal details to each other** and are thus analogous to 'black boxes.'"

## C
- **class** — "defines an object's interface and implementation. It specifies the object's internal representation and defines the operations the object can perform."
- **class diagram** — "A diagram that depicts classes, their internal structure and operations, and the **static** relationships between them." (OMT notation; Appendix B.)
- **class operation** — "An operation targeted to a class and not to an individual object. In C++, class operations are called **static member functions**."
- **class pattern** (scope) — a pattern dealing with relationships between classes, established through **inheritance**, and therefore **fixed at compile-time**.
- **concrete class** — "A class having no abstract operations. It can be instantiated."
- **constructor** — "In C++, an operation that is automatically invoked to initialize new instances."
- **coupling** — "The degree to which software components depend on each other."

## D
- **delegation** — "An implementation mechanism in which an object **forwards or delegates** a request to another object. The delegate carries out the request **on behalf of** the original object." (The receiver is passed to the delegate so it can refer back.)
- **design pattern** — "**systematically names, motivates, and explains a general design that addresses a recurring design problem** in object-oriented systems. It describes the problem, the solution, when to apply the solution, and its consequences."
- **destructor** — "In C++, an operation that is automatically invoked to finalize an object that is about to be deleted."
- **double dispatch** — the operation executed depends on **two** receiver types, not one. `Accept` in **Visitor** is the canonical example.
- **dynamic binding** — "The **run-time** association of a request to an object and one of its operations. In C++, only **virtual functions** are dynamically bound."

## E
- **encapsulation** — "The result of hiding a representation and implementation in an object. The representation is **not visible and cannot be accessed directly** from outside the object."
- **extrinsic state** (Flyweight) — state that **depends on and varies with** the flyweight's context; cannot be shared, so it is passed in on each operation.

## F
- **factory method** — an operation that creates an object, which subclasses override to decide the class instantiated.
- **framework** — "A set of cooperating classes that makes up a **reusable design for a specific class of software**. A framework provides architectural guidance by partitioning the design into abstract classes and defining their responsibilities and collaborations. **A developer customizes the framework to a particular application by subclassing and composing instances of framework classes.**"
- **friend class** — "In C++, a class that has the same access rights to the operations and data of a class as that class itself." (Used by Memento and State to keep the wide interface private.)

## H
- **hook operation** — a template-method step providing **default behavior a subclass may extend**; often does nothing by default. Contrast **primitive operation** (must be overridden).
- **Hollywood Principle** — "**Don't call us, we'll call you**" — the inverted control structure of **Template Method**, where the parent class calls subclass operations.

## I
- **inheritance** — "A relationship that defines one entity in terms of another. **Class inheritance combines interface inheritance and implementation inheritance.** Interface inheritance defines a new interface in terms of one or more existing interfaces. Implementation inheritance defines a new implementation in terms of one or more existing implementations."
- **instance variable** — "A piece of data that defines part of an object's representation. C++ uses the term **data member**."
- **interaction diagram** — "A diagram that shows the **flow of requests** between objects." (From Objectory and the Booch method.)
- **interface** — "The set of all **signatures** defined by an object's operations. The interface describes the set of requests to which an object can respond."
- **internal iterator** / **external iterator** — an internal iterator controls the iteration itself and is handed the operation to apply; an external iterator gives the client control of advancing. (Iterator.)
- **intrinsic state** (Flyweight) — state **independent of context**, therefore shareable across all uses of the flyweight.

## M
- **metaclass** — "Classes are objects in Smalltalk. A metaclass is **the class of a class object**."
- **mixin class** — "A class designed to be **combined with other classes through inheritance**. Mixin classes are usually abstract."

## N
- **null object** — a do-nothing subclass returned instead of a null reference, so clients need no conditional (used in Chain of Responsibility and Composite discussions).

## O
- **object** — "A run-time entity that packages both data and the procedures that operate on that data."
- **object composition** — "Assembling or composing objects to get more complex behavior." The mechanism behind **black-box reuse**.
- **object diagram** — "A diagram that depicts a particular **object structure at run-time**."
- **object pattern** (scope) — a pattern dealing with object relationships, which are **dynamic and can be changed at run-time**.
- **object reference** — "A value that identifies another object."
- **operation** — "An object's data can be manipulated only by its operations. An object performs an operation when it receives a **request**. In C++, operations are called **member functions**. Smalltalk uses the term **method**."
- **overriding** — "Redefining an operation (inherited from a parent class) in a subclass."

## P
- **parameterized type** — "A type that leaves some constituent types unspecified. The unspecified types are supplied as parameters at the point of use. In C++, parameterized types are called **templates**."
- **parent class** — "The class from which another class inherits. Synonyms are **superclass** (Smalltalk), **base class** (C++), and **ancestor class**."
- **polymorphism** — "The ability to **substitute objects of matching interface for one another at run-time**."
- **primitive operation** — an abstract step a template method calls, which subclasses **must** override.
- **private inheritance** — "In C++, a class inherited **solely for its implementation**."
- **protocol** — "Extends the concept of an interface to include the **allowable sequences of requests**."
- **prototype** — an instance used as a template: new objects are made by **cloning** it.
- **pull model** / **push model** (Observer) — pull: the subject sends a minimal notification and observers query for details. Push: the subject sends detailed change information whether or not observers need it.

## R
- **receiver** — "The target object of a request."
- **refactoring** — reorganizing a design: "tearing apart classes into special- and general-purpose components, moving operations up or down the class hierarchy, and rationalizing the interfaces of classes." Patterns are **targets for refactoring**.
- **request** — "An object performs an operation when it receives a corresponding request from another object. A common synonym for request is **message**."

## S
- **signature** — "An operation's signature defines its **name, parameters, and return value**."
- **subclass** — "A class that inherits from another class. In C++, a subclass is called a **derived class**."
- **subsystem** — "An independent group of classes that collaborate to fulfill a set of responsibilities." (What **Facade** fronts.)
- **subtype** — "A type is a subtype of another if **its interface contains the interface of the other type**."
- **supertype** — "The parent type from which a type inherits."

## T
- **template method** — an operation defining the **skeleton of an algorithm**, with steps deferred to subclasses; it fixes the ordering while letting the steps vary.
- **toolkit** — "A collection of classes that provides useful functionality but **does not define the design of an application**." (Contrast **framework**, which does.)
- **type** — "The name of a particular interface."

## W
- **white-box reuse** — "A style of reuse based on **class inheritance**. A subclass reuses the interface and implementation of its parent class, but **it may have access to otherwise private aspects of its parent**."

## Notation quick reference *(Appendix B)*
- **Class inheritance** — a **triangle** connecting subclass to parent.
- **Aggregation ("part-of")** — an arrowheaded line with a **diamond at the base**; the arrow points to the class aggregated.
- **Acquaintance** — an arrowheaded line **without** the diamond.
- **"Creates"** — a **dashed** arrowheaded line (an addition to OMT); the arrow points to the class instantiated.
- **"More than one"** — a **filled circle** at the head of a reference.
- **Abstract class or operation** — shown in **slanted (italic) type**.
- **Client shown in gray** — the pattern has no Client participant, but showing it clarifies who interacts with the pattern (e.g. Proxy). A black Client means it *is* a participant (e.g. Flyweight).
