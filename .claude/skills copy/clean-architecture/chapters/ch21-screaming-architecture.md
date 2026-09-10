# Chapter 21: Screaming Architecture

## Core Idea
Building plans scream "HOME" or "LIBRARY" — so a software system's top-level structure should scream **what the system is for**, not which framework built it. "If your architecture is based on frameworks, then it cannot be based on your use cases."

## Frameworks Introduced
- **The blueprint test**: "When you look at the top-level directory structure, and the source files in the highest-level package, do they scream 'Health Care System,' or 'Accounting System,' or 'Inventory Management System'? Or do they scream '**Rails**,' or '**Spring/Hibernate**,' or '**ASP**'?"
- **The theme of an architecture** — from Ivar Jacobson's *Object Oriented Software Engineering*, whose subtitle is **A Use Case Driven Approach**: "software architectures are structures that support the use cases of the system. Just as the plans for a house or a library scream about the use cases of those buildings, so should the architecture of a software application scream about the use cases of the application."
- **Frameworks are tools, not architectures**: "Architectures are not (or should not be) about frameworks. Architectures should not be **supplied** by frameworks. Frameworks are tools to be used, not architectures to be conformed to."
- **The skeptical stance toward frameworks**: "Look at each framework with a jaded eye. View it skeptically. Yes, it might help, **but at what cost?** Ask yourself how you should use it, and **how you should protect yourself from it**. Think about how you can preserve the use-case emphasis of your architecture. **Develop a strategy that prevents the framework from taking over that architecture.**"
- **The testability corollary**: "If your system architecture is all about the use cases, and if you have kept your frameworks at arm's length, then you should be able to unit-test all those use cases **without any of the frameworks in place**. You shouldn't need the web server running to run your tests. You shouldn't need the database connected to run your tests."

## Key Concepts
- **The house analogy, precisely applied**: "The first concern of the architect is to make sure that the house is **usable** — not to ensure that the house is made of bricks. Indeed, the architect takes pains to ensure that the homeowner can make decisions about the exterior material (bricks, stone, or cedar) **later**, after the plans ensure that the use cases are met."
- **The web is not an architecture.** "The web is a delivery mechanism — an IO device — and your application architecture should treat it as such... You should be able to deliver it as a console app, or a web app, or a thick client app, or even a web service app, **without undue complication or change to the fundamental architecture**."
- **Why framework advocacy is systematically biased**: "Framework authors often believe very deeply in their frameworks. The examples they write for how to use their frameworks are told from the point of view of a **true believer**. Other authors who write about the framework also tend to be **disciples of the true belief**... Often they assume an all-encompassing, all-pervading, let-the-framework-do-everything position. **This is not the position you want to take.**"
- **What "testable in situ" requires**: "Your Entity objects should be plain old objects that have no dependencies on frameworks or databases or other complications. Your use case objects should coordinate your Entity objects. Finally, all of them together should be testable in situ, without any of the complications of frameworks."

## Worked Example
**The two blueprints, and then yours.**

**A single-family residence.** The plans show "a front entrance, a foyer leading to a living room, and perhaps a dining room. There will likely be a kitchen a short distance away, close to the dining room. Perhaps there is a dinette area next to the kitchen, and probably a family room close to that." No ambiguity: "The architecture would scream: **'HOME.'**"

**A library.** "A grand entrance, an area for check-in/out clerks, reading areas, small conference rooms, and gallery after gallery capable of holding bookshelves for all the books in the library." That architecture screams **"LIBRARY."**

Note what neither blueprint tells you: the exterior material. Brick, stone, or cedar is deferred until the use cases are satisfied — which is precisely the relationship a software architecture should have with Rails, Spring, Hibernate, Tomcat, and MySQL.

**The conversation that proves it worked.** Martin's closing scene is the practical test of the whole chapter. New programmers open the repository of a health care system, and their first impression should be *"Oh, this is a health care system."* They should be able to learn all the use cases of the system **and still not know how it is delivered**. So they come to you and say:

> "We see some things that look like models — but where are the views and controllers?"

And the correct answer is:

> "Oh, those are details that needn't concern us at the moment. **We'll decide about them later.**"

That exchange is the deliverable. If a new hire can enumerate the use cases before discovering the delivery mechanism, the architecture screams the right word.

## Key Takeaways
1. Your top-level structure should announce the domain, not the framework.
2. Architecture supports use cases (Jacobson); a framework-shaped architecture cannot be use-case-shaped.
3. Frameworks are tools to be used skeptically and defended against — ask how to protect yourself from each one.
4. The web is an IO device and a deferrable decision; the same system should be deliverable as console, thick client, or service.
5. The test of success: use cases run in unit tests with no web server and no database.
6. A new programmer should learn what the system *does* long before learning how it is *delivered*.

## Connects To
- **Ch 15 (What Is Architecture?)** and **Ch 17 (Boundaries)**: deferring framework, database, and web decisions.
- **Ch 16 (Independence)**: "A shopping cart application with a good architecture will look like a shopping cart application" — the same claim, stated as a use-case visibility requirement.
- **Ch 20 (Business Rules)**: Entities as plain objects, use cases coordinating them.
- **Ch 22 (The Clean Architecture)**: the structure that delivers this property.
- **Ch 31–32 (The Web Is a Detail / Frameworks Are Details)**: each of this chapter's claims argued at length.
- **Ch 34 (The Missing Chapter)**: what a screaming directory structure actually looks like on disk.
