# Chapter 11: DIP — The Dependency Inversion Principle

## Core Idea
"The most flexible systems are those in which source code dependencies refer only to **abstractions**, not to **concretions**" — and the curved line separating abstract from concrete in the DIP diagram becomes, later in the book, **the architectural boundary** and **the Dependency Rule**.

## Frameworks Introduced
- **DIP stated**: in a statically typed language, `use`/`import`/`include` statements should refer only to source modules containing interfaces, abstract classes, or other abstract declarations. "Nothing concrete should be depended on." The same rule applies in Ruby and Python, where a concrete module is harder to define — "it is any module in which the functions being called are **implemented**."
- **The realistic qualification**: "treating this idea as a rule is unrealistic, because software systems must depend on many concrete facilities." Java's `String` is concrete and it would be absurd to force it to be abstract.
  - The distinction that matters is **volatility**, not concreteness: `String` "is very stable. Changes to that class are very rare and tightly controlled." So "we tend to ignore the stable background of operating system and platform facilities when it comes to DIP. We tolerate those concrete dependencies because we know we can rely on them not to change."
  - "**It is the volatile concrete elements of our system that we want to avoid depending on.** Those are the modules that we are actively developing, and that are undergoing frequent change."
- **Stable Abstractions** — the asymmetry that makes interfaces the safer thing to depend on:
  - "Every change to an abstract interface corresponds to a change to its concrete implementations. Conversely, changes to concrete implementations do not always, or even usually, require changes to the interfaces that they implement. **Therefore interfaces are less volatile than implementations.**"
  - And designers actively work to keep it that way: "They try to find ways to add functionality to implementations without making changes to the interfaces. This is Software Design 101."
- **The four coding practices** DIP boils down to:
  1. **Don't refer to volatile concrete classes.** Refer to abstract interfaces instead. Applies in all languages, static or dynamic. "It also puts severe constraints on the creation of objects and generally enforces the use of **Abstract Factories**."
  2. **Don't derive from volatile concrete classes.** "In statically typed languages, inheritance is the strongest, and most rigid, of all the source code relationships; consequently, it should be used with great care. In dynamically typed languages, inheritance is less of a problem, but it is still a dependency — and caution is always the wisest choice."
  3. **Don't override concrete functions.** "Concrete functions often require source code dependencies. When you override those functions, you do not eliminate those dependencies — indeed, you **inherit** them. To manage those dependencies, you should make the function abstract and create multiple implementations."
  4. **Never mention the name of anything concrete and volatile.** "This is really just a restatement of the principle itself."
- **Abstract Factory for object creation**: "in virtually all languages, the creation of an object requires a source code dependency on the concrete definition of that object" — so creation needs special handling.

## Key Concepts
- **The curved line is an architectural boundary.** "It separates the abstract from the concrete. **All source code dependencies cross that curved line pointing in the same direction, toward the abstract side.**"
- **Two components, one line**: the **abstract** component contains all the high-level business rules of the application; the **concrete** component contains all the implementation details those business rules manipulate.
- **Why it's called *inversion***: "the flow of control crosses the curved line in the opposite direction of the source code dependencies. The source code dependencies are **inverted against the flow of control**."
- **DIP violations cannot be eliminated, only concentrated.** The concrete component in the diagram contains a dependency and therefore violates DIP. "**This is typical.** DIP violations cannot be entirely removed, but they can be gathered into a small number of concrete components and kept separate from the rest of the system."
- **`main` is where you put them.** "Most systems will contain at least one such concrete component — often called `main` because it contains the `main` function." `main` instantiates `ServiceFactoryImpl`, places it in a global variable of type `ServiceFactory`, and the Application accesses the factory through that global.

## Mental Models
- **Ask "is it volatile?", not "is it concrete?"** Depending on `java.lang.String` is fine and always will be. Depending on the module your teammate is actively rewriting is the problem DIP addresses.
- **Interfaces are stable *by construction*, not by luck.** The reason interfaces change less often is structural — implementation changes rarely propagate upward — and good designers deliberately widen that gap.
- **Concentrate impurity rather than pursuing purity.** The goal isn't a DIP-clean system; it's a system whose DIP violations live in one small, clearly labeled place.
- **Overriding a concrete function inherits its dependencies.** This is the non-obvious one: you can't shed a dependency by overriding — you take it on. Make the function abstract instead.

## Worked Example
**The Abstract Factory, and what the curved line is doing.**

The problem: the `Application` uses `ConcreteImpl` through the `Service` interface — good, no dependency on the implementation. But the `Application` must somehow **create** instances of `ConcreteImpl`, and creating an object requires a source code dependency on its concrete definition. That single requirement would drag the concretion back across the boundary.

The structure that avoids it:

1. `Application` depends on the `Service` interface (abstract).
2. `Application` also depends on the `ServiceFactory` interface (abstract) and calls its `makeSvc` method.
3. `ServiceFactoryImpl` derives from `ServiceFactory` and lives on the concrete side.
4. `ServiceFactoryImpl.makeSvc()` instantiates `ConcreteImpl` and **returns it as a `Service`**.

Now trace the two arrows in opposite directions:

- **Source code dependencies**: `ServiceFactoryImpl` → `ServiceFactory`, and `ConcreteImpl` → `Service`. Both cross the curved line **toward the abstract side**. The `Application` names nothing concrete.
- **Flow of control**: `Application` → `makeSvc` → `ServiceFactoryImpl` → `new ConcreteImpl` → method calls on `ConcreteImpl`. Runtime control crosses the line **toward the concrete side**.

That opposition is the whole principle, and the name follows from it.

**Where the leftover impurity goes.** Something must eventually name `ServiceFactoryImpl`, and that something is `main` — "the function that is invoked by the operating system when the application is first started up." `main` instantiates the factory implementation and hands it to the rest of the system through a global of the abstract type. The rest of the system stays clean; one component is knowingly dirty.

**What this becomes later.** "As we move forward in this book and cover higher-level architectural principles, the DIP will show up again and again. It will be **the most visible organizing principle in our architecture diagrams**. The curved line will become the architectural boundaries in later chapters. The way the dependencies cross that curved line in one direction, and toward more abstract entities, will become a new rule that we will call **the Dependency Rule**."

## Reference Tables

| Thing | Depend on it? | Why |
|---|---|---|
| `java.lang.String` and platform facilities | **Yes** | Concrete but extremely stable; changes are rare and tightly controlled |
| Interfaces / abstract classes | **Yes** | Less volatile than implementations, by construction |
| Volatile concrete classes you're actively developing | **No** | Frequent change propagates to everything naming them |
| Concrete classes as base classes | **No** | Inheritance is the strongest and most rigid source relationship |
| Concrete functions, via override | **No** | You inherit their dependencies rather than escaping them |

## Key Takeaways
1. Depend on abstractions; the practical target is *volatile* concretions, not all concretions.
2. Interfaces change less often than implementations — that asymmetry is what makes DIP work.
3. Four rules: don't refer to, don't derive from, don't override, don't name anything concrete and volatile.
4. Object creation is where DIP is hardest; Abstract Factory is the standard answer.
5. Source dependencies and flow of control run in opposite directions across the boundary — hence "inversion."
6. You cannot remove all DIP violations; gather them into `main` and keep them away from everything else.
7. The curved line here is the same line that becomes the Dependency Rule of the Clean Architecture.

## Connects To
- **Ch 5 (OOP)**: safe polymorphism is what makes any dependency invertible in the first place.
- **Ch 8 (OCP)**: DIP is step two of the OCP recipe — organizing the dependencies after separating concerns.
- **Ch 17–19 (Boundaries, Boundary Anatomy, Policy and Level)**: the curved line becomes a real boundary.
- **Ch 22 (The Clean Architecture)**: the Dependency Rule.
- **Ch 26 (The Main Component)**: `main` as the designated concrete component.
- **Clean Code, Ch 10 & 11**: DIP at class scale, and separating construction from use.
