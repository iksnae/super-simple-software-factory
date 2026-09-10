# Chapter 34: The Missing Chapter
*(by Simon Brown)*

## Core Idea
"Your best design intentions can be destroyed in a flash if you don't consider the intricacies of the implementation strategy" — and the decisive detail is **access modifiers**: mark everything `public` and all four organizational styles collapse into the same thing. **Use the compiler to enforce your architecture.**

## Frameworks Introduced
- **The four ways to organize code**:
  1. **Package by layer** — horizontal slicing "based on what it does from a technical perspective." One package for web, one for business logic, one for persistence. "In a 'strict layered architecture,' layers should depend only on the next adjacent lower layer."
  2. **Package by feature** — vertical slicing "based on related features, domain concepts, or aggregate roots (to use domain-driven design terminology)." All types in one package named for the concept.
  3. **Ports and adapters** — an **'inside'** (domain) and an **'outside'** (infrastructure). "The major rule here is that the 'outside' depends on the 'inside' — **never** the other way around."
  4. **Package by component** (Brown's own) — "bundling **all** of the responsibilities related to a single coarse-grained component into a single Java package... taking a **service-centric view** of a software system."
- **Brown's definition of a component**, distinguished from Martin's: Martin — "Components are the units of deployment... In Java, they are jar files." Brown — "**A grouping of related functionality behind a nice clean interface, which resides inside an execution environment like an application.**"
  - From the **C4 software architecture model**: "a software system is made up of one or more **containers** (e.g., web applications, mobile apps, stand-alone applications, databases, file systems), each of which contains one or more **components**, which in turn are implemented by one or more **classes** (or code). **Whether each component resides in a separate jar file is an orthogonal concern.**"
- **Organization versus encapsulation** — the chapter's pivot: "if you make all types in your Java application `public`, the packages are simply an **organization mechanism** (a grouping, like folders), rather than being used for **encapsulation**. Since public types can be used from anywhere in a code base, **you can effectively ignore the packages** because they provide very little real value."
  - The consequence: "**all four architectural approaches presented earlier in this chapter are exactly the same when we overuse this designation.** ... Conceptually the approaches are very different, but **syntactically they are identical**."
  - And the sting: "This is a neat trick, and of course nobody would ever make all of their Java types public. **Except when they do. And I've seen it.**"

## Key Concepts
- **The `public` reflex**: "It's almost as if we, as developers, instinctively use the `public` keyword without thinking. **It's in our muscle memory.** If you don't believe me, take a look at the code samples for books, tutorials, and open source frameworks on GitHub."
- **Relaxed layered architecture** — layers "allowed to skip around their adjacent neighbor(s)." Sometimes intended (CQRS), often not: "bypassing the business logic layer is undesirable, especially if that business logic is responsible for ensuring **authorized access to individual records**."
- **The enforcement problem**: many teams say "We enforce this principle through good discipline and code reviews, because we trust our developers." Brown's reply: "This confidence is great to hear, but **we all know what happens when budgets and deadlines start looming ever closer**."
  - Static analysis (NDepend, Structure101, Checkstyle) with rules like `types in package **/web should not access types in **/data` "is a little crude, but it can do the trick." Still: "**The problem with both approaches is that they are fallible, and the feedback loop is longer than it should be.** If left unchecked, this practice can turn a code base into a '**big ball of mud**.' I'd personally like to use the **compiler** to enforce my architecture if at all possible."
- **Naming on the inside uses the ubiquitous domain language** — `OrdersRepository` becomes simply `Orders`. "We talk about 'orders' when we're having a discussion about the domain, not the 'orders repository.'"
- **Layered architecture doesn't scream anything.** "Put the code for two layered architectures, from two very different business domains, side by side and they will likely look **eerily similar**: web, services, and repositories."
- **Java's packages aren't hierarchical for access purposes**: "although we tend to think of packages as being hierarchical, **it's not possible to create access restrictions based on a package and subpackage relationship**. Any hierarchy that you create is in the name of those packages, and the directory structure on disk, only."

## Reference Tables

The running example — a "view orders" use case in an online book store:

| Type | Role |
|---|---|
| `OrdersController` | A web controller, "something like a Spring MVC controller," handling web requests |
| `OrdersService` | Interface defining the 'business logic' related to orders |
| `OrdersServiceImpl` | The implementation (footnote: "arguably a horrible way to name a class, but as we'll see later, perhaps it doesn't really matter") |
| `OrdersRepository` | Interface defining access to persistent order information |
| `JdbcOrdersRepository` | Implementation of the repository interface |

**What can be made package-protected under each style** — the payoff of applying access modifiers properly:

| Style | Must be `public` | Can be package-protected |
|---|---|---|
| **Package by layer** | `OrdersService`, `OrdersRepository` (inbound dependencies from other packages) | `OrdersServiceImpl`, `JdbcOrdersRepository` — "Nobody needs to know about them; they are an implementation detail" |
| **Package by feature** | `OrdersController` — "the sole entry point into the package" | Everything else. **Caveat**: "nothing else in the code base, outside of this package, can access information related to orders unless they go through the controller. This may or may not be desirable" |
| **Ports and adapters** | `OrdersService`, `Orders` | Implementation classes, "dependency injected at runtime" |
| **Package by component** | `OrdersComponent` interface only | Everything else — "**There's now no way that code outside this package can use the `OrdersRepository` interface or implementation directly, so we can rely on the compiler to enforce this architectural principle**" |

"The fewer public types you have, the smaller the number of potential dependencies." (Footnote: "Unless you cheat and use Java's reflection mechanism, but please don't do that!") The .NET equivalent is `internal`, "although you would need to create a separate assembly for every component."

## Worked Example
**The new hire who broke the architecture in an afternoon — without breaking a single rule.**

The setup: a strict layered architecture, dependency arrows all pointing downward, a clean acyclic graph. "The big problem here is that **we can cheat by introducing some undesirable dependencies, yet still create a nice, acyclic dependency graph.**"

The story:

1. Someone new joins the team and is given another orders-related use case. "Since the person is new, he wants to make a big impression and get this use case implemented **as quickly as possible**."
2. "After sitting down with a cup of coffee for a few minutes, the newcomer discovers an existing `OrdersController` class, so he decides that's where the code for the new orders-related web page should go."
3. "But it needs some orders data from the database. The newcomer has an epiphany: '**Oh, there's an `OrdersRepository` interface already built, too. I can simply dependency-inject the implementation into my controller. Perfect!**'"
4. "After a few more minutes of hacking, the web page is working."

Now inspect the result. **The dependency arrows still point downward.** The graph is still acyclic. Every rule the team wrote down has been followed. And yet "the `OrdersController` is now additionally **bypassing the `OrdersService`** for some use cases" — which, if `OrdersService` is where record-level authorization lives, is a security hole introduced by a well-meaning new hire in under an hour.

"While the new use case works, it's perhaps not implemented in the way that we were expecting. **I see this happen a lot with teams that I visit as a consultant, and it's usually revealed when teams start to visualize what their code base really looks like — often for the first time.**"

The question that follows is the whole chapter: you need a principle like *"Web controllers should never access repositories directly."* **"The question, of course, is enforcement."** Discipline fails under deadline. Static analysis works but is crude and slow. The compiler is immediate and unarguable — *if* your types aren't all `public`.

**Package by component, applied.** Bundle the business logic and persistence code for orders into one package with a single public `OrdersComponent` interface. "If you're writing code that needs to do something with **orders**, there's just **one place to go** — the `OrdersComponent`. Inside the component, the separation of concerns is still maintained, so the business logic is separate from data persistence, but **that's a component implementation detail that consumers don't need to know about**."

And note the relationship to microservices: "This is akin to what you might end up with if you adopted a micro-services or Service-Oriented Architecture — a separate `OrdersService` that encapsulates everything related to handling orders. **The key difference is the decoupling mode. You can think of well-defined components in a monolithic application as being a stepping stone to a micro-services architecture.**"

Now the new hire physically cannot reach `OrdersRepository`. Not because a reviewer caught it, not because a build step flagged it — because the code does not compile.

## Other Decoupling Modes
- **Module systems** (OSGi, Java 9 modules): "you can make a distinction between types that are `public` and types that are **published**. For example, you could create an `Orders` module where all of the types are marked as public, but **publish only a small subset** of those types for external consumption."
- **Separate source code trees.** For ports and adapters, three trees: business/domain (`OrdersService`, `OrdersServiceImpl`, `Orders`), web (`OrdersController`), and persistence (`JdbcOrdersRepository`). "The latter two source code trees have a compile-time dependency on the business and domain code, which itself **doesn't know anything about** the web or the data persistence code." Ideally repeated per component — "**This is very much an idealistic solution, though**, because there are real-world performance, complexity, and maintenance issues associated with breaking up your source code in this way."
- **Two trees (domain / infrastructure)** — simpler, and it carries a named trap:
  - **The "Périphérique anti-pattern of ports and adapters."** "The city of Paris, France, has a ring road called the Boulevard Périphérique, which allows you to **circumnavigate Paris without entering the complexities of the city**. Having all of your infrastructure code in a single source code tree means that it's potentially possible for infrastructure code in one area of your application (e.g., a web controller) to **directly call code in another area** (e.g., a database repository), **without navigating through the domain**. This is especially true if you've forgotten to apply appropriate access modifiers."

## Key Takeaways
1. Package by layer is a fine start and stops scaling; it also reveals nothing about the business domain.
2. Package by feature makes the domain visible but, in Brown's view, is still suboptimal.
3. Ports and adapters splits inside from outside, with the outside always depending on the inside.
4. Package by component bundles business logic and persistence behind one public interface — a monolithic stepping stone to microservices.
5. A clean acyclic dependency graph does not prevent a controller from reaching straight into a repository.
6. Discipline and code review fail under deadline; static analysis is crude with a slow feedback loop; **the compiler is immediate**.
7. Overusing `public` makes packages folders rather than encapsulation, and makes all four styles syntactically identical.
8. Minimize public types; use `internal` in .NET, module systems' *published* distinction, or separate source trees.
9. Watch for the Périphérique anti-pattern when all infrastructure shares one tree.
10. Be pragmatic: weigh team size, skill level, solution complexity, time, and budget — and watch for coupling in data models too.

## Connects To
- **Ch 12 (Components)**: Martin's deployment-unit definition, which Brown deliberately contrasts with his own.
- **Ch 14 (Component Coupling)**: acyclic dependency graphs — and why acyclicity alone is insufficient.
- **Ch 16 (Independence)**: decoupling modes, source-level through service-level.
- **Ch 21 (Screaming Architecture)**: why "web, services, repositories" screams nothing.
- **Ch 22 (The Clean Architecture)**: the inside/outside split this chapter implements on disk.
- **Ch 27 (Services: Great and Small)**: components as the stepping stone to microservices.
