# Chapter 16: Independence

## Core Idea
A good architecture supports use cases, operation, development, and deployment simultaneously — by decoupling **horizontal layers** and **vertical use cases**, and by leaving the **decoupling mode** itself (source / deployment / service) as a deferred option that can move in either direction over the system's life.

## Frameworks Introduced
- **Decoupling layers (horizontal)**: apply SRP and CCP to the intent of the system to separate what changes for different reasons.
  - "User interfaces change for reasons that have nothing to do with business rules. Use cases have elements of both."
  - **Two kinds of business rules, changing at different rates**: those "closely tied to the application" (validation of input fields) versus those "more closely associated with the domain" (calculation of interest on an account, counting of inventory).
  - "The database, the query language, and even the schema are technical details that have nothing to do with the business rules or the UI."
  - Result: "the system divided into decoupled horizontal layers — the UI, application-specific business rules, application-independent business rules, and the database."
- **Decoupling use cases (vertical)**: "The use case for adding an order to an order entry system almost certainly will change at a different rate, and for different reasons, than the use case that deletes an order."
  - Use cases are "narrow vertical slices that cut through the horizontal layers." Each uses some UI, some application-specific rules, some application-independent rules, and some database functionality. "We keep the use cases separate down the vertical height of the system."
  - The payoff: "If you also group the UI and database in support of those use cases, so that each use case uses a different aspect of the UI and database, then **adding new use cases will be unlikely to affect older ones**."
- **True vs. false (accidental) duplication** — the trap architects fall into out of fear of duplication.
  - **True duplication**: "every change to one instance necessitates the same change to every duplicate."
  - **False/accidental**: "If two apparently duplicated sections of code evolve along different paths — if they change at different rates, and for different reasons — then they are not true duplicates. Return to them in a few years, and you'll find that they are very different from each other."
  - "Resist the temptation to commit the sin of **knee-jerk elimination of duplication**. Make sure the duplication is real."
- **The three decoupling modes**:
  1. **Source level** — control dependencies between source modules so changes don't force recompilation of others (e.g. Ruby Gems). All components in one address space, communicating by function calls, a single executable. "People often call this a **monolithic structure**."
  2. **Deployment level** — control dependencies between deployable units (jars, DLLs, shared libraries) so a source change doesn't force others to be rebuilt and redeployed. Components may still share an address space and use function calls, or live in other processes using IPC, sockets, or shared memory. "The important thing here is that the decoupled components are partitioned into independently deployable units."
  3. **Service level** — reduce dependencies to data structures, communicating solely through network packets, "such that every execution unit is entirely independent of source and binary changes to others."
- **Conway's Law**: *"Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."*

## Key Concepts
- **Architecture supports use cases mainly by making them visible.** "The most important thing a good architecture can do to support behavior is to **clarify and expose that behavior** so that the intent of the system is visible at the architectural level. A shopping cart application with a good architecture will **look like a shopping cart application**... Developers will not have to hunt for behaviors, because those behaviors will be first-class elements visible at the top level."
- **Operation is where architecture bites hard** — 100,000 customers per second, or big-data-cube queries in milliseconds, force real structural choices: an array of small services running in parallel across servers; lightweight threads sharing one process's address space; a few processes in isolated address spaces; or "a simple monolithic program running in a single process."
- **And even that is a deferrable option.** "A system that is written as a monolith, and that **depends on** that monolithic structure, cannot easily be upgraded to multiple processes, multiple threads, or micro-services should the need arise." An architecture that isolates components and "does not assume the means of communication between those components" can move across that spectrum as needs change.
- **Independent developability** — "So long as the layers and use cases are decoupled, the architecture of the system will support the organization of the teams, irrespective of whether they are organized as **feature teams, component teams, layer teams**, or some other variation."
- **Independent deployability** — "if the decoupling is done well, then it should be possible to **hot-swap** layers and use cases in running systems. Adding a new use case could be as simple as adding a few new jar files or services to the system while leaving the rest alone."
- **The goal for deployment is "immediate deployment."** "A good architecture does not rely on dozens of little configuration scripts and property file tweaks. It does not require manual creation of directories or files that must be arranged just so."

## Mental Models
- **You will not know the targets, and they will move.** "Most of the time we don't know what all the use cases are, nor do we know the operational constraints, the team structure, or the deployment requirements. Worse, even if we did know them, they will inevitably change as the system moves through its life cycle. In short, **the goals we must meet are indistinct and inconstant. Welcome to the real world.**"
  - Which is why the deferral strategy is not laziness: "Some principles of architecture are relatively inexpensive to implement and can help balance those concerns, **even when you don't have a clear picture of the targets you have to hit**."
- **Similar-looking screens are the classic false duplicate.** "Most likely it is accidental. As time goes by, the odds are that those two screens will diverge and eventually look very different. For this reason, care must be taken to avoid unifying them. Otherwise, **separating them later will be a challenge**."
- **The view model is worth the copying.** When a database record's data structure resembles a screen view's, the temptation is to pass the record straight to the UI. "Be careful: This duplication is almost certainly accidental. Creating the separate view model is not a lot of effort, and it will help you keep the layers properly decoupled."
- **Decoupling for use cases pays for operations too** — separate what runs at high throughput from what runs at low, put UI and database on different servers, replicate the high-bandwidth pieces. But only if the *mode* is right: "To run in separate servers, the separated components cannot depend on being together in the same address space."

## Reference Tables

| Mode | Boundary is… | Communication | Cost |
|---|---|---|---|
| **Source level** | Source module dependencies | Function calls, one address space, one executable (monolith) | Cheapest; may suffice for the whole project lifetime |
| **Deployment level** | Jars, DLLs, shared libraries, Gems | Function calls, or IPC/sockets/shared memory across processes | Moderate; independent rebuild and redeploy |
| **Service level** | Network packets between execution units | Data structures over a network | "Expensive, both in development time and in system resources" |

## Worked Example
**Choosing a decoupling mode — and Martin's actual recommendation.**

"What is the best mode to use? The answer is that **it's hard to know which mode is best during the early phases of a project**. Indeed, as the project matures, the optimal mode may change."

He walks through the popular default and rejects it:

> "One solution (which seems to be popular at the moment) is to simply decouple at the service level by default. A problem with this approach is that it is expensive and **encourages coarse-grained decoupling**. No matter how 'micro' the micro-services get, the decoupling is not likely to be fine-grained enough.
>
> Another problem with service-level decoupling is that it is expensive, both in development time and in system resources. Dealing with service boundaries where none are needed is a waste of effort, memory, and cycles. And, yes, I know that the last two are cheap — **but the first is not**."

His preference, stated plainly:

> "My preference is to **push the decoupling to the point where a service could be formed, should it become necessary; but then to leave the components in the same address space as long as possible.** This leaves the option for a service open."

The progression that follows:

1. **Start at source level.** "That may be good enough for the duration of the project's lifetime."
2. **If deployment or development issues arise**, push some of the decoupling to deployment level — "at least for a while."
3. **As development, deployment, and operational issues increase**, "carefully choose which deployable units to turn into services, and gradually shift the system in that direction."
4. **And expect to reverse.** "Over time, the operational needs of the system may decline. What once required decoupling at the service level may now require only deployment-level or even source-level decoupling."

The summary requirement on the architecture: "A good architecture will allow a system to be **born as a monolith**, deployed in a single file, but then to grow into a set of independently deployable units, and then all the way to independent services and/or micro-services. Later, as things change, it should allow for **reversing that progression** and sliding all the way back down into a monolith. A good architecture **protects the majority of the source code from those changes**."

Note the honesty of the caveat: "I'm not saying that the change of decoupling modes should be a trivial configuration option (though sometimes that is appropriate). What I'm saying is that the decoupling mode of a system is one of those things that is likely to change with time, and **a good architect foresees and appropriately facilitates those changes**."

## Key Takeaways
1. Decouple horizontally by layer (UI, application-specific rules, application-independent rules, database) and vertically by use case.
2. Adding a use case should not disturb existing ones — that is the test of whether the vertical decoupling worked.
3. Architecture makes behavior *visible*; the intent of the system should be readable from its structure.
4. Operational structure (monolith / threads / processes / services) is itself an option to leave open.
5. Conway's Law means the architecture must give independent teams independent components, whatever their organizing axis.
6. Beware accidental duplication: similar screens, similar queries, and record-shaped view models are usually false duplicates.
7. Prefer the cheapest decoupling mode that keeps the more expensive one available, and expect the right mode to change — in both directions.

## Connects To
- **Ch 7 (SRP) / Ch 13 (CCP)**: the separation criteria used to find the layers.
- **Ch 15 (What Is Architecture?)**: the four life-cycle concerns, introduced.
- **Ch 17 (Boundaries)** and **Ch 18 (Boundary Anatomy)**: where the lines go and what crossing them costs.
- **Ch 21 (Screaming Architecture)**: "A shopping cart application will look like a shopping cart application," developed in full.
- **Ch 22 (The Clean Architecture)**: the layer set this chapter derives.
- **Ch 27 (Services: Great and Small)**: the service-level mode examined skeptically.
