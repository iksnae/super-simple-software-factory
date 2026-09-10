# Chapter 27: Services — Great and Small

## Core Idea
Services are "just function calls across process and/or platform boundaries" — the supposed decoupling and independent-deployability benefits are largely illusory — and **architectural boundaries do not fall between services; they run *through* them, dividing them into components.**

## Frameworks Introduced
- **Services are not an architecture.** "The architecture of a system is defined by boundaries that separate high-level policy from low-level detail and follow the Dependency Rule. Services that simply separate application behaviors are **little more than expensive function calls**, and are not necessarily architecturally significant."
  - The analogy: in a monolith, architecture is defined by "certain function calls that cross architectural boundaries and follow the Dependency Rule. Many other functions in those systems, however, simply separate one behavior from another and are **not** architecturally significant. So it is with services."
  - The concession: "This is not to say that all services should be architecturally significant. There are often substantial benefits to creating services that separate functionality across processes and platforms — whether they obey the Dependency Rule or not."
- **The Decoupling Fallacy**: services are decoupled "at the level of individual variables" and that's about it.
  - "They can still be coupled by **shared resources** within a processor, or on the network. What's more, they are **strongly coupled by the data they share**."
  - Concretely: "if a new field is added to a data record that is passed between services, then **every service that operates on the new field must be changed**. The services must also strongly agree about the interpretation of the data in that field."
  - On well-defined interfaces: "that's certainly true — but it is no less true for functions. **Service interfaces are no more formal, no more rigorous, and no better defined than function interfaces.**"
- **The Fallacy of Independent Development and Deployment**:
  - "History has shown that large enterprise systems can be built from monoliths and component-based systems **as well as** service-based systems. Thus services are not the only option for building scalable systems."
  - "The decoupling fallacy means that services cannot always be independently developed, deployed, and operated. **To the extent that they are coupled by data or behavior, the development, deployment, and operation must be coordinated.**"
- **Component-Based Services**: "Services do not need to be little monoliths. Services can, instead, be designed using the SOLID principles, and given a component structure so that new components can be added to them **without changing the existing components within the service**."
  - "Think of a service in Java as a set of abstract classes in one or more jar files. Think of each new feature or feature extension as another jar file that contains classes that extend the abstract classes in the first jar files. **Deploying a new feature then becomes not a matter of redeploying the services, but rather a matter of simply adding the new jar files to the load paths** of those services. In other words, adding new features conforms to the Open-Closed Principle."
- **The chapter's central correction**: "**Architectural boundaries do not fall between services. Rather, those boundaries run through the services, dividing them into components.** ... Those services do not define the architectural boundaries of the system; instead, the components within the services do."

## Key Concepts
- **Cross-cutting concerns are the real problem.** "Every software system must face this problem, whether service oriented or not. **Functional decompositions... are very vulnerable to new features that cut across all those functional behaviors.**"
- **The one-service-per-programmer footnote**, deadpan: "Therefore the number of micro-services will be roughly equal to the number of programmers."
- **The final taxonomy**: "A service might be a **single component**, completely surrounded by an architectural boundary. Alternatively, a service might be **composed of several components** separated by architectural boundaries. In rare cases, clients and services may be so coupled as to have **no architectural significance whatever**." (Footnote: "We hope they are rare. Unfortunately, experience suggests otherwise.")
- **Architecture is not physical**: "The architecture of a system is defined by the boundaries drawn within that system, and by the dependencies that cross those boundaries. **That architecture is not defined by the physical mechanisms by which elements communicate and execute.**"

## Worked Example
**The Kitty Problem — one feature, every service.**

The system is the taxi aggregator from Chapter 9: it knows many taxi providers in a city and lets customers order rides, selecting on pickup time, cost, luxury, and driver experience. Wanting scalability, the architects built it from many small microservices, and split the staff into small teams each owning a few services:

| Service | Responsibility |
|---|---|
| `TaxiUI` | Deals with customers ordering taxis from mobile devices |
| `TaxiFinder` | Examines the inventories of the various `TaxiSuppliers`, determines candidate taxis, deposits them into a short-term data record attached to the user |
| `TaxiSelector` | Takes the user's criteria — cost, time, luxury — and chooses an appropriate taxi from the candidates |
| `TaxiDispatcher` | Orders the chosen taxi |

A year in, everything is running smoothly. Then marketing arrives with **kitten delivery**:

- Users order kittens delivered to homes or businesses.
- The company sets up **kitten collection points** across the city.
- On an order, a nearby taxi collects a kitten from a collection point and delivers it.
- **One taxi supplier has agreed** to participate; others may follow; others may decline.
- **Some drivers are allergic** to cats and must never be selected for this service.
- **Some customers are allergic**, so "a vehicle that has been used to deliver kittens within the last 3 days should not be selected for customers who declare such allergies."

Now cost it out against the service diagram: "**How many of those services will have to change to implement this feature? All of them.**"

Trace why. `TaxiUI` needs a kitten-ordering flow. `TaxiFinder` must know which suppliers participate and must track collection points. `TaxiSelector` must exclude cat-allergic drivers and, for allergic customers, exclude vehicles used for kittens in the last three days. `TaxiDispatcher` must route via a collection point. Every service touched; every team coordinated.

"In other words, **the services are all coupled, and cannot be independently developed, deployed, and maintained**." The promised benefit evaporates on contact with the first genuinely cross-cutting feature — because the decomposition was **functional**, and the new feature cuts across functions.

**Objects to the rescue.** How would a component-based architecture have absorbed this? "Careful consideration of the SOLID design principles would have prompted us to create a set of classes that could be **polymorphically extended** to handle new features."

The structure: classes roughly corresponding to the original services, with boundaries and dependencies following the Dependency Rule. Then:

- "Much of the logic of the original services is **preserved within the base classes** of the object model."
- "That portion of the logic that was specific to rides has been extracted into a **`Rides` component**."
- "The new feature for kittens has been placed into a **`Kittens` component**."
- Both override the abstract base classes "using a pattern such as **Template Method or Strategy**."
- Both follow the Dependency Rule, and "the classes that implement those features are **created by factories under the control of the UI**."

The result: "when the Kitty feature is implemented, the `TaxiUI` must change. **But nothing else needs to be changed.** Rather, a new jar file, or Gem, or DLL is added to the system and dynamically loaded at runtime. Thus the Kitty feature is decoupled, and independently developable and deployable."

**And you can have both.** The obvious question — can services be built this way? — gets an unambiguous yes. Keep the services, give each one an internal component design following the Dependency Rule, and new features arrive as new derivative classes in their own components. The services survive; the boundaries move inside them.

## Reference Tables

| Claimed service benefit | Reality |
|---|---|
| Strongly decoupled | Only at the level of individual variables. Still coupled by shared resources and, decisively, **by shared data** |
| Well-defined interfaces | True — and "no more formal, no more rigorous, and no better defined than function interfaces" |
| Independent development and deployment | Only where they are not coupled by data or behavior; a cross-cutting feature forces coordination across all of them |
| Required for scalability | No — monoliths and component-based systems have delivered large enterprise systems too |

| Decomposition style | Response to a cross-cutting feature |
|---|---|
| **Functional** (service per behavior) | Every service changes; deployment must be carefully coordinated |
| **Polymorphic / component-based** | One new component added; only the UI changes; loaded dynamically at runtime |

## Key Takeaways
1. A service is an expensive function call across a process or platform boundary — not, by itself, an architecture.
2. Services are coupled by the data they exchange; adding a field to a shared record ripples through every consumer.
3. Independent deployability holds only where there is no data or behavior coupling, which cross-cutting features destroy.
4. Functional decomposition — whether into services or functions — is uniquely vulnerable to cross-cutting features.
5. The object-oriented answer is polymorphic extension: new behavior arrives as a new component, not as edits everywhere.
6. Design each service with an internal component architecture obeying the Dependency Rule; deploy features by adding jars to the load path (OCP).
7. Architectural boundaries run *through* services, not between them.
8. Architecture is defined by boundaries and dependency direction, never by the physical communication mechanism.

## Connects To
- **Ch 9 (LSP)**: the same taxi aggregator, illustrating a substitutability violation.
- **Ch 13 (CCP)**: "The Kitty Problem" is cited there as the illustration of changes scattered across components.
- **Ch 16 (Independence)**: service-level decoupling as one mode among three, and why not to default to it.
- **Ch 18 (Boundary Anatomy)**: the cost of the service boundary.
- **Ch 22 (The Clean Architecture)**: the Dependency Rule that services must obey internally.
- **Ch 8 (OCP)**: adding features by adding code, not changing it.
