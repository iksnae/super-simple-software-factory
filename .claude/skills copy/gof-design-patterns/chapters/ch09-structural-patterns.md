# Chapter 4: Structural Patterns *(category introduction and discussion)*

## Core Idea
Structural patterns "are concerned with **how classes and objects are composed to form larger structures**." Class patterns use inheritance to compose interfaces or implementations; object patterns compose objects — and **"the added flexibility of object composition comes from the ability to change the composition at run-time, which is impossible with static class composition."**

## Frameworks Introduced
- **Structural class patterns** — "use inheritance to compose interfaces or implementations."
  - "consider how **multiple inheritance mixes two or more classes into one**. The result is a class that combines the properties of its parent classes. **This pattern is particularly useful for making independently developed class libraries work together.**"
  - The class form of **Adapter**: "an adapter makes one interface (the adaptee's) conform to another, thereby providing a **uniform abstraction of different interfaces**. A class adapter accomplishes this by **inheriting privately from an adaptee class**."
- **Structural object patterns** — "describe ways to **compose objects** to realize new functionality."

## Key Concepts
- **Composite** — "describes how to build a class hierarchy made up of classes for **two kinds of objects: primitive and composite**."
- **Proxy** — "a proxy acts as a convenient **surrogate or placeholder** for another object... It can act as a local representative for an object in a remote address space. It can represent a large object that should be **loaded on demand**. It might **protect access** to a sensitive object. Proxies provide a level of indirection to specific properties of objects. Hence they can **restrict, enhance, or alter** these properties."
- **Flyweight** — "defines a structure for **sharing** objects. Objects are shared for at least two reasons: **efficiency and consistency**. Flyweight focuses on sharing for **space efficiency**... **But objects can be shared only if they don't define context-dependent state.** Flyweight objects have no such state. Any additional information they need is passed to them when needed."
- **Facade** — "Whereas Flyweight shows how to make **lots of little objects**, Facade shows how to make **a single object represent an entire subsystem**. A facade is a representative for a set of objects. The facade carries out its responsibilities by **forwarding messages** to the objects it represents."
- **Bridge** — "separates an object's **abstraction from its implementation** so that you can vary them independently."
- **Decorator** — "composes objects **recursively** to allow an open-ended number of additional responsibilities... We can add two decorations simply by **nesting one Decorator object within another**... each Decorator object must **conform to the interface of its component** and must forward messages to it. The Decorator can do its job either **before or after** forwarding a message."

## Why the patterns look alike
"You may have noticed similarities between the structural patterns, especially in their participants and collaborations. This is so probably because structural patterns rely on the **same small set of language mechanisms** for structuring code and objects: single and multiple inheritance for class-based patterns, and object composition for object patterns. **But the similarities belie the different intents among these patterns.**"

## Worked Example

### Adapter versus Bridge
Both "promote flexibility by providing a level of indirection to another object. Both involve **forwarding requests to this object from an interface other than its own**."

| | **Adapter** | **Bridge** |
|---|---|---|
| Focus | "resolving **incompatibilities between two existing interfaces**" | "bridges an abstraction and its (potentially numerous) implementations" |
| Concern for evolution | "doesn't focus on how those interfaces are implemented, nor does it consider **how they might evolve independently**" | "provides a **stable interface** to clients even as it lets you vary the classes that implement it. It also **accommodates new implementations** as the system evolves" |
| Coupling | "The coupling is **unforeseen**" | "the user of a bridge understands **up-front** that an abstraction must have several implementations" |
| Timing | applied **after** design | applied **before** design |

> **"The Adapter pattern makes things work *after* they're designed; Bridge makes them work *before* they are."**

And the disclaimer: "That doesn't mean Adapter is somehow inferior to Bridge; **each pattern merely addresses a different problem**."

**Facade vs. Adapter**: "You might think of a facade as an adapter to a set of other objects. **But that interpretation overlooks the fact that a facade defines a *new* interface, whereas an adapter *reuses* an old interface.**"

### Composite versus Decorator versus Proxy

**Composite and Decorator** "have similar structure diagrams, reflecting the fact that both rely on **recursive composition**... This commonality might tempt you to think of a decorator object as a degenerate composite, **but that misses the point**."

| | **Decorator** | **Composite** |
|---|---|---|
| Intent | "add responsibilities to objects **without subclassing**. It avoids the explosion of subclasses" | "structuring classes so that **many related objects can be treated uniformly**, and multiple objects can be treated as one" |
| Focus | **embellishment** | **representation** |

"These intents are distinct but **complementary**. Consequently, the Composite and Decorator patterns are often used in concert. Both lead to the kind of design in which you can **build applications just by plugging objects together without defining any new classes**... **From the point of view of the Decorator pattern, a composite is a ConcreteComponent. From the point of view of the Composite pattern, a decorator is a Leaf.**"

**Decorator and Proxy** — "Both patterns describe how to provide a level of indirection to an object, and the implementations of both keep a reference to another object to which they forward requests. **Once again, however, they are intended for different purposes.**"

| | **Decorator** | **Proxy** |
|---|---|---|
| Where the functionality lives | "the component provides **only part** of the functionality, and one or more decorators furnish the rest" | "**the subject defines the key functionality**, and the proxy provides (or refuses) access to it" |
| Dynamic attach/detach | Yes | "**not concerned with attaching or detaching properties dynamically**" |
| Recursive composition | "**essential**" — because "an object's total functionality can't be determined at compile time" | "**not designed for** recursive composition"; Proxy "focuses on **one relationship** — between the proxy and its subject — and that relationship **can be expressed statically**" |
| Why you'd reach for it | open-ended responsibilities | "inconvenient or undesirable to access the subject directly because, for example, it lives on a **remote machine**, has **restricted access**, or is **persistent**" |

**On hybrids**, with characteristic honesty: "You might envision a **proxy-decorator** that adds functionality to a proxy, or a **decorator-proxy** that embellishes a remote object. Although such hybrids might be useful (**we don't have real examples handy**), they are divisible into patterns that are useful."

## Key Takeaways
1. Structural patterns look alike because they draw on the same few mechanisms — inheritance and composition. Intent is what separates them.
2. Object composition beats class composition where run-time change matters.
3. Adapter reuses an existing interface; Facade defines a new one.
4. Adapter is retrofitted; Bridge is planned. Neither is superior.
5. Composite is about representation; Decorator is about embellishment; they compose well, each seeing the other as its own base case.
6. Decorator supplies missing functionality open-endedly; Proxy guards access to functionality that already exists.
7. Flyweight makes many small objects affordable; Facade makes a whole subsystem look like one object.

## Connects To
- **Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy** — the seven patterns.
- **Ch 3 (Creational Patterns)** and **Ch 5 (Behavioral Patterns)** — the other two category chapters.
- **Ch 1**: the class/object scope distinction that separates class Adapter from object Adapter.
