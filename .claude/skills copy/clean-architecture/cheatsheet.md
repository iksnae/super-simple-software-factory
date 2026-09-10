# Cheatsheet — Clean Architecture

## The one rule
**Source code dependencies must point only inward, toward higher-level policies.**
Nothing in an inner circle may name anything in an outer circle — not a class, not a function, not a variable, **not a data format**.

## The circles (schematic, not mandatory)

| Circle | Contains | Changes when | Key constraint |
|---|---|---|---|
| Frameworks & Drivers | DB, web framework, tools | Externals change | Glue code only. "The web is a detail. The database is a detail." |
| Interface Adapters | Controllers, Presenters, Views, gateway impls, ORMs | External formats change | **All SQL lives here.** MVC lives entirely here |
| Use Cases | Application-specific rules | The application's operation changes | Unaffected by DB, UI, frameworks |
| Entities | Enterprise-wide Critical Business Rules | Almost never | "No operational change to any particular application should affect the entity layer" |

## Decision rules

**Where does a boundary go?** → On an **axis of change**. Components on either side change at different rates for different reasons. That's the SRP telling you where to draw.

**Which way does the arrow point?** → **Toward what you want to protect.** "If component A should be protected from changes in component B, then component B should depend on component A."

**Is this thing a detail?** → Ask whether policy's *behavior* changes if you swap it. Database, web, UI, framework, OS, hardware, processor: all details. The **data model** is not.

**Should I depend on this concrete thing?** → Ask "is it **volatile**?", not "is it concrete?" `java.lang.String` is fine forever. The module your teammate is rewriting is not.

**Higher or lower level?** → **Distance from inputs and outputs.** Entities are higher than use cases because they're reusable across applications and further from IO.

**Which decoupling mode?** → The cheapest one that keeps the next one reachable. Push the design to where a service *could* be formed, then leave components in one address space as long as possible. Expect to move — in both directions.

**Framework: use or marry?** → Use. Keep it in an outer circle, behind proxies. Confine DI frameworks to `main`. Marry only when unavoidable (STL, the standard library), and make it an explicit decision.

**Full boundary or partial?** → Watch for friction where a boundary is absent; build at the inflection point where implementing costs less than ignoring. Review that judgment frequently.

**Is this duplication real?** → Will every change to one require the same change to the other? If they'll diverge — similar screens, a record-shaped view model — it's **accidental**, and unifying it makes later separation hard.

**Should this be `public`?** → Almost certainly not. The fewer public types, the fewer possible dependencies — and the compiler becomes your architecture enforcer.

**Should this method be static?** → Nonstatic by default. Static only when all data comes from arguments *and* you'll never want polymorphism.

## SOLID, in one line each

| | Principle | Statement |
|---|---|---|
| **S** | Single Responsibility | A module should be responsible to **one, and only one, actor** (not "do one thing") |
| **O** | Open-Closed | Open for extension, closed for modification — achieved by SRP separation + DIP dependency ordering |
| **L** | Liskov Substitution | Implementations must be substitutable without changing the *user's* behavior |
| **I** | Interface Segregation | Don't depend on modules containing more than you need |
| **D** | Dependency Inversion | Depend on abstractions; avoid **volatile** concretions |

## Component principles

| Cohesion (which classes go together) | | |
|---|---|---|
| **REP** | The granule of reuse is the granule of release | Inclusive — bigger components |
| **CCP** | Gather classes that change for the same reasons at the same times (SRP for components) | Inclusive — bigger components |
| **CRP** | Don't force users to depend on things they don't need (ISP for components) | Exclusive — smaller components |

**Tension**: focus on REP+CRP → simple changes hit too many components. Focus on CCP+REP → too many unneeded releases. Projects start on the right (sacrificing reuse, favoring developability) and slide left as others begin consuming them.

| Coupling (how components may relate) | |
|---|---|
| **ADP** | Allow no cycles in the dependency graph |
| **SDP** | Depend in the direction of stability (I decreases along edges) |
| **SAP** | A component should be as abstract as it is stable |

**SDP + SAP = DIP for components** — with shades of gray that class-level DIP doesn't allow.

## Metrics

| Metric | Formula | Read as |
|---|---|---|
| **I** | `Fan-out / (Fan-in + Fan-out)` | 0 = maximally stable (responsible, independent); 1 = maximally unstable (irresponsible, dependent) |
| **A** | `Na / Nc` | 0 = no abstractions; 1 = nothing but abstractions |
| **D** | `\|A + I − 1\|` | 0 = on the Main Sequence; near 1 = investigate |

Use D statistically: mean and variance near zero for a conforming design; variance sets control limits. Plot D per component over releases; a threshold around **0.1** catches drift.

**Zone of Pain** (0,0) — stable *and* concrete. **Database schemas** live here. Harmless only if nonvolatile (`String`).
**Zone of Uselessness** (1,1) — abstract with no dependents. Abstractions nobody implemented.

## Tells & smells

| You see… | You probably have… |
|---|---|
| Top-level packages named `web`, `services`, `repositories` | An architecture that screams the framework, not the domain |
| Database rows or Entities passed across a boundary | An inner circle that now knows about an outer one |
| `@autowired` on business objects | A framework married into the innermost circle |
| A controller injecting a repository | A "relaxed" layer skip that a clean acyclic graph won't catch |
| Everything marked `public` | Packages used as folders; all four organizational styles collapsed into one |
| A test class per production class | Structural coupling — tests pinning shape, not behavior |
| Tests that need the web server or the database | Business rules not separated from delivery and persistence |
| `#ifdef BOARD_V2` in thousands of places | Hardware type that belongs under a HAL |
| A new field in a shared record breaking many services | The decoupling fallacy — services coupled by data |
| One feature requiring changes to every service | Functional decomposition meeting a cross-cutting concern |
| Unit tests dragging in dozens of libraries | Cycles in the component dependency graph |
| Vendor C extensions outside the firmware layer | Software that has quietly become firmware |

## Thresholds & defaults

| Thing | Guidance |
|---|---|
| Cost of change | Should track **scope**, not **shape** |
| Deployment | Goal is "immediate deployment" — a **single action**, no config-script archaeology |
| Number of circles | Four is schematic; use what you need. The Dependency Rule doesn't flex |
| Default decoupling mode | Source level; escalate only under real deployment/development/operational pressure |
| DI framework reach | `main` only |
| Public types per component | Ideally **one** interface |
| `main` components | As many as you have configurations — Dev, Test, Prod, per country, per customer |

## The value argument (for when you have to make it)
1. Software has two values: **behavior** (urgent, sometimes important) and **structure** (important, never urgent).
2. Extremes settle it: works-but-unchangeable → **useless**; broken-but-changeable → **continually useful**.
3. Eisenhower: architecture occupies quadrants 1–2; behavior occupies 1 and 3. The standard error is promoting quadrant 3 to quadrant 1.
4. Managers cannot evaluate architecture's importance — that's what developers were hired for.
5. "If architecture comes last... it means the software development team did not fight hard enough for what they knew was necessary."

## The three paradigms, as removals
- **Structured** — discipline on *direct* transfer of control (removes `goto`) → algorithmic foundation of modules
- **OO** — discipline on *indirect* transfer of control (removes function pointers) → **crossing architectural boundaries**
- **Functional** — discipline on *assignment* (removes mutation) → location of and access to data

"Software is composed of sequence, selection, iteration, and indirection. Nothing more. Nothing less."
