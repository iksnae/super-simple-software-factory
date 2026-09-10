---
name: gof-design-patterns
description: The complete Gang of Four catalog — all 23 design patterns from Gamma, Helm, Johnson & Vlissides with verbatim intents, applicability, participants, consequences, implementation trade-offs, and C++/Smalltalk sample code. Use when choosing between patterns, naming a design, distinguishing confusable pairs (Strategy vs State, Adapter vs Bridge vs Decorator vs Proxy, Mediator vs Observer), evaluating whether a pattern's indirection is worth its cost, or reading a codebase that already uses them.
---

# Design Patterns (Gang of Four)

Gamma, Helm, Johnson, Vlissides · Addison-Wesley, 1994.

## Start here

**Choosing a pattern?** → [cheatsheet.md](cheatsheet.md) — pick by what varies, pick by cause of redesign, and the confusable-pair table.

**Need one pattern's full treatment?** → [patterns.md](patterns.md) — all 23 intents with links to their chapter files.

**Term or notation?** → [glossary.md](glossary.md).

## The two principles everything rests on

1. **"Program to an interface, not an implementation."**
2. **"Favor object composition over class inheritance."**

Inheritance is **white-box reuse**: compile-time, and "**inheritance breaks encapsulation**" because a subclass depends on its parent's internals. Composition is **black-box reuse**: run-time, defined only through interfaces, and it keeps each class focused on one task. The cost of composition is more objects and more indirection.

## The catalog

| | **Creational** — object creation | **Structural** — composition of classes/objects | **Behavioral** — assignment of responsibility and communication |
|---|---|---|---|
| **Class** | Factory Method | Adapter (class) | Interpreter, Template Method |
| **Object** | Abstract Factory, Builder, Prototype, Singleton | Adapter (object), Bridge, Composite, Decorator, Facade, Flyweight, Proxy | Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Visitor |

**Scope**: class patterns use inheritance and are fixed at compile-time; object patterns use composition and can change at run-time.

## What varies — the fastest way in

Name the thing that changes, then look it up:

- **families of products** → Abstract Factory · **how a composite is built** → Builder · **which subclass is instantiated** → Factory Method · **which class is instantiated** → Prototype · **the sole instance** → Singleton
- **an object's interface** → Adapter · **a subsystem's interface** → Facade · **an implementation** → Bridge · **structure and composition** → Composite · **responsibilities, without subclassing** → Decorator · **storage cost** → Flyweight · **how an object is accessed or where it lives** → Proxy
- **who fulfills a request** → Chain of Responsibility · **when and how it's fulfilled** → Command · **a grammar** → Interpreter · **traversal** → Iterator · **who interacts with whom** → Mediator · **what private state is stored outside an object** → Memento · **how many depend on one, and how they stay current** → Observer · **an object's states** → State · **an algorithm** → Strategy · **the steps of an algorithm** → Template Method · **operations applied without changing the classes** → Visitor

Full table with the book's exact wording: [cheatsheet.md §1](cheatsheet.md).

## Reading a pattern

Every pattern is described in thirteen sections. Four carry the decisions:

- **Intent** — one or two sentences; the pattern's identity.
- **Applicability** — the situations that justify it. **Read this before adopting a pattern.**
- **Consequences** — benefits *and* liabilities. "The Consequences sections are most helpful when evaluating a pattern's benefits and liabilities."
- **Implementation** — the trade-offs you'll actually face (push vs. pull, who owns traversal, who defines transitions, when to copy).

The other nine: Pattern Name and Classification · Also Known As · Motivation · Structure · Participants · Collaborations · Sample Code · Known Uses · Related Patterns.

## The warning that comes with the catalog

> "**Design patterns should not be applied indiscriminately. Often they achieve flexibility and variability by introducing additional levels of indirection, and that can complicate a design and/or cost you some performance. A design pattern should only be applied when the flexibility it affords is actually needed.**" *(Ch 1)*

Common failure modes, and each pattern's named liability: [cheatsheet.md §5](cheatsheet.md).

## Files

```
SKILL.md              this file
patterns.md           all 23 intents, classification, links
cheatsheet.md         selection tables, confusable pairs, anti-patterns
glossary.md           Appendix A definitions + Appendix B notation
chapters/
  ch01-introduction.md                  what a pattern is; the two principles;
                                        inheritance vs composition; 8 causes of redesign
  ch02-case-study-document-editor.md    Lexi: 7 problems, 8 patterns, end to end
  ch03-creational-patterns.md           category intro + discussion
  ch04..ch08                            Abstract Factory, Builder, Factory Method,
                                        Prototype, Singleton
  ch09-structural-patterns.md           category intro + discussion
  ch10..ch16                            Adapter, Bridge, Composite, Decorator,
                                        Facade, Flyweight, Proxy
  ch17-behavioral-patterns.md           category intro
  ch18..ch28                            Chain of Responsibility, Command, Interpreter,
                                        Iterator, Mediator, Memento, Observer, State,
                                        Strategy, Template Method, Visitor
  ch29-behavioral-discussion.md         encapsulating variation; objects as arguments;
                                        Mediator vs Observer; sender/receiver decoupling
  ch30-conclusion.md                    patterns as vocabulary, documentation,
                                        and refactoring targets
```

## How to apply one *(Ch 1)*

Read it through with attention to **Applicability** and **Consequences** → study Structure, Participants, Collaborations → read the Sample Code → **name your classes after the participants** (`TeXLayoutStrategy`, not `Algorithm2`) → define the classes → name the operations consistently → implement.

## Two things worth knowing about the book itself

- The catalog "**just documents existing designs**." Its contribution is a **shared vocabulary**: "Let's use an Observer here," "Let's make a Strategy out of these classes."
- Patterns are **targets for refactoring**: "Using these patterns early in the life of a design prevents later refactorings. But even if you don't see how to apply a pattern until after you've built your system, **the pattern can still show you how to change it**."
