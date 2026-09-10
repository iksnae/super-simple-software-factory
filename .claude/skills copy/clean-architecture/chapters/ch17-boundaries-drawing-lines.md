# Chapter 17: Boundaries — Drawing Lines

## Core Idea
Software architecture is **the art of drawing lines** that restrict what one side may know about the other — drawn "where there is an axis of change," to keep premature decisions from polluting the core business logic.

## Frameworks Introduced
- **What saps people-power**: "the goal of an architect is to minimize the human resources required to build and maintain the required system. What is it that saps this kind of people-power? **Coupling — and especially coupling to premature decisions.**"
- **Which decisions are premature**: "Decisions that have nothing to do with the business requirements — the use cases — of the system. These include decisions about frameworks, databases, web servers, utility libraries, dependency injection, and the like."
  - "A good system architecture is one in which decisions like these are rendered **ancillary and deferrable**... A good system architecture allows those decisions to be made at the latest possible moment, without significant impact."
- **Draw lines between things that matter and things that don't**: "The GUI doesn't matter to the business rules... The database doesn't matter to the GUI... The database doesn't matter to the business rules."
- **The database behind an interface**: `BusinessRules` use a `DatabaseInterface`; `DatabaseAccess` implements it and drives the actual `Database`. The boundary is drawn **across the inheritance relationship, just below the `DatabaseInterface`**.
  - The critical consequence of arrow direction: "The `Database` knows about the `BusinessRules`. The `BusinessRules` do not know about the `Database`. This implies that the `DatabaseInterface` classes live in the `BusinessRules` component, while the `DatabaseAccess` classes live in the `Database` component."
  - Stated as an asymmetry: "**the `Database` does not matter to the `BusinessRules`, but the `Database` cannot exist without the `BusinessRules`.**" If that seems strange — "The `Database` component contains the code that translates the calls made by the `BusinessRules` into the query language of the database. **It is that translation code that knows about the `BusinessRules`.**"
- **The IO is irrelevant.** "Developers and customers often get confused about what the system is. They see the GUI, and think that the GUI *is* the system."
  - The video game argument: your experience is dominated by screen, mouse, buttons, sounds — "You forget that behind that interface there is a model... **that model does not need the interface**. It would happily execute its duties, modeling all the events in the game, without the game ever being displayed on the screen."
- **Plugin Architecture**: the database and GUI decisions together form the pattern used by systems that allow third-party plugins. "The history of software development technology is the story of how to conveniently create plugins to establish a scalable and maintainable system architecture."
- **The rule for where lines go**: "**Boundaries are drawn where there is an axis of change.** The components on one side of the boundary change at different rates, and for different reasons, than the components on the other side. ... **This is simply the Single Responsibility Principle again. The SRP tells us where to draw our boundaries.**"

## Key Concepts
- **Plugins make replacement practical, not necessarily trivial.** "If the initial deployment of our system was web-based, then writing the plugin for a client-server UI could be challenging. It is likely that some of the communications between the business rules and the new UI would have to be reworked. Even so, by starting with the presumption of a plugin structure, we have at very least made such a change **practical**."
- **Three-tier is not an architecture.** Martin's footnote: "The word 'architecture' appears in quotes here because three-tier is not an architecture; **it's a topology**. It's exactly the kind of decision that a good architecture strives to defer."
- **Nothing is wrong with services per se.** On company W: "There's nothing intrinsically wrong with a software system that is structured around services. The error at W was the **premature adoption and enforcement** of a suite of tools that promised SoA."
- **The final recipe**: "partition the system into components. Some of those components are core business rules; others are plugins... Then arrange the code in those components such that the arrows between them point in one direction — **toward the core business**." Recognizable as **DIP** and the **Stable Abstractions Principle**: "Dependency arrows are arranged to point from lower-level details to higher-level abstractions."

## Worked Example
**Company P: the server farm that never existed.**

In the 1980s, P's founders wrote a simple monolithic desktop application, grew it through the 1990s into a popular GUI product. Then the web arrived, customers clamored, and P hired "a bunch of hotshot twenty-something Java programmers" to webify it.

"The Java guys had dreams of server farms dancing in their heads, so they adopted a rich three-tiered 'architecture'... There would be servers for the GUI, servers for the middleware, and servers for the database. **Of course.**"

The premature decision: every domain object would have **three instantiations** — GUI tier, middleware tier, database tier — living on different machines, with a rich system of inter-processor and inter-tier communication. Method invocations between tiers became objects, serialized and marshaled across the wire.

Now cost out adding one field to one record:

- The field must be added to classes in **all three tiers**
- …and to several **inter-tier messages**
- Data travels both directions, so **four message protocols** must be designed
- Each protocol has a sending and receiving side, so **eight protocol handlers**
- Total: **three executables**, each with three updated business objects, four new messages, and eight new handlers

Plus, at runtime, "all the object instantiations, all the serializations, all the marshaling and de-marshaling, all the building and parsing of messages, all the socket communications, timeout managers, retry scenarios, and all the other extra stuff that you have to do just to get one simple thing done."

The two twists that make it a warning rather than a mistake:

1. **They never had a server farm during development.** They ran all three executables in three processes on one machine — for several years — paying every serialization cost with no distribution benefit, "because they were convinced that their architecture was right."
2. **They never sold one either.** "Every system they ever deployed was a single server... in anticipation of a server farm that never existed, and never would."

"The tragedy is that the architects, by making a premature decision, **multiplied the development effort enormously**." And Martin notes P is composite: "I've seen it many times and in many places. Indeed, P is a superposition of all those places."

**Company W: worse than P.** A local business managing fleets of company cars hired an "Architect" whose "middle name" was control, and who determined the operation needed "a full-blown, enterprise-scale, service-oriented ARCHITECTURE." A huge domain model, a suite of services to manage the domain objects, "and put all the developers on a path to Hell."

To add a contact person's name, address, and phone number to a sales record:

1. Go to the `ServiceRegistry`, ask for the service ID of the `ContactService`
2. Send a `CreateContact` message — "of course, this message had dozens of fields that all had to have valid data in them — **data to which the programmer had no access**, since all the programmer had was a name, address, and phone number"
3. Fake the missing data
4. Jam the new contact's ID into the sales record
5. Send `UpdateContact` to the `SaleRecordService`

Testing anything meant firing up every necessary service one by one, plus the message bus, plus the BPel server — then absorbing propagation delays "as these messages bounced from service to service, and waited in queue after queue." Adding a feature meant the coupling between services, "the sheer volume of WSDLs that needed changing, and all the redeployments those changes necessitated."

"Hell starts to seem like a nice place by comparison." The cost: "sheer person-hours — person-hours in droves — flushed down the SoA vortex."

**FitNesse: the success.** Martin and his son Micah started FitNesse in 2001 — a simple wiki wrapping Ward Cunningham's FIT acceptance-testing tool. Before Maven "solved" the jar problem, Martin insisted on **"Download and Go"**: never require more than one jar. That rule drove the decisions.

**Decision 1 — write their own web server.** "This might sound absurd. Even in 2001 there were plenty of open source web servers." But "a bare-bones web server is a very simple piece of software to write and it allowed us to **postpone any web framework decision until much later**." (Footnote: "Many years later we were able to slip the Velocity framework into FitNesse.")

**Decision 2 — avoid thinking about a database.** MySQL was in the back of their minds, but they "purposely delayed that decision by employing a design that made the decision irrelevant. That design was simply to put an interface between all data accesses and the data repository itself" — the `WikiPage` interface, providing everything needed to find, fetch, and save pages.

The timeline that followed:

| Period | What they used | What they built |
|---|---|---|
| First ~3 months | `MockWikiPage` — data access methods stubbed out | Wiki text → HTML translation (needed no storage at all) |
| Next ~1 year | `InMemoryPage` — a hash table of wiki pages in RAM | Page creation, linking, wiki formatting, running FIT tests. **The whole first version worked** — it just couldn't save anything |
| Then | `FileSystemWikiPage` — hash tables written to flat files | Persistence, plus continued feature work |
| 3 months later | Flat files judged good enough | "We **deferred that decision into nonexistence** and never looked back" |
| Later | `MySqlWikiPage`, written by a customer | "He came back **a day later** with the whole system working in MySQL" |

The postscript is honest: "We used to bundle that option with FitNesse, but nobody else ever used it, so eventually we dropped it. Even the customer who wrote the derivative eventually dropped it."

What the boundary actually bought: "The fact that we did not have a database running for 18 months of development meant that, for 18 months, we did not have **schema issues, query issues, database server issues, password issues, connection time issues**, and all the other nasty issues that raise their ugly heads when you fire up a database. It also meant that **all our tests ran fast**, because there was no database to slow them down."

**The plugin argument: ReSharper and Visual Studio.** Two teams, two companies, two countries — JetBrains in Russia, Microsoft in Redmond. "It's hard to imagine two development teams that are more separate."

"Which team can damage the other? Which team is immune to the other? **The dependency structure tells the story.** The source code of ReSharper depends on the source code of Visual Studio. Thus there is nothing that the ReSharper team can do to disturb the Visual Studio team. But the Visual Studio team could completely disable the ReSharper team if they so desired."

"That's a deeply asymmetric relationship, and it is one that we desire to have in our own systems... Arranging our systems into a plugin architecture creates **firewalls across which changes cannot propagate**."

## Key Takeaways
1. Boundaries restrict knowledge; they exist to keep premature decisions out of the business rules.
2. Premature decisions are the ones unrelated to use cases: frameworks, databases, web servers, DI containers.
3. The database goes behind an interface owned by the business rules — the database knows about them, never the reverse.
4. IO is irrelevant. The GUI is not the system; the model runs perfectly well with nothing on screen.
5. Treat every replaceable concern as a plugin; that makes substitution practical even when it isn't trivial.
6. Plugin structure creates firewalls: changes on the plugin side cannot propagate into the core.
7. Draw lines on axes of change — which is the SRP, telling you where the boundaries go.
8. Point every arrow toward the core business: DIP and SAP, applied to whole components.

## Connects To
- **Ch 7 (SRP)**: the axis of change that locates the line.
- **Ch 11 (DIP)** / **Ch 14 (SAP)**: the arrow direction, stated as principles.
- **Ch 15 (What Is Architecture?)**: deferral of details, and the device-independence stories.
- **Ch 18 (Boundary Anatomy)**: what crossing a boundary costs at each mode.
- **Ch 30 (The Database Is a Detail)**: "as we shall see in another chapter, this idea is misguided" — the database-as-business-rules belief, answered.
- **Ch 5 (OOP)**: plugins as the payoff of dependency inversion.
