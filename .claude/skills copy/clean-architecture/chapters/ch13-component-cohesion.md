# Chapter 13: Component Cohesion

## Core Idea
Three principles decide which classes belong in which component — **REP**, **CCP**, **CRP** — and they deliberately pull against each other, so the architect's real job is finding a position in the tension triangle that suits the project's *current* stage, knowing that position will move.

## Frameworks Introduced
- **REP — The Reuse/Release Equivalence Principle**: *"The granule of reuse is the granule of release."*
  - "People who want to reuse software components cannot, and will not, do so unless those components are tracked through a release process and are given **release numbers**."
  - Two reasons, not one: without release numbers there's no way to ensure reused components are compatible with each other — *and* "software developers need to know when new releases are coming, and which changes those new releases will bring." Developers routinely see a release, read the changes, and decide to **stay on the old one**. So "the release process must produce the appropriate notifications and release documentation so that users can make informed decisions."
  - Design consequence: the classes and modules in a component "must belong to a cohesive group... there must be some overarching theme or purpose that those modules all share," and they should be **releasable together** under one version number, one release tracking, one set of release documentation.
- **CCP — The Common Closure Principle**: *"Gather into components those classes that change for the same reasons and at the same times. Separate into different components those classes that change at different times and for different reasons."*
  - **This is the SRP restated for components.** SRP: a class should not contain multiple reasons to change. CCP: a component should not have multiple reasons to change.
  - "For most applications, **maintainability is more important than reusability**." If code must change, you want all the changes in one component. "If changes are confined to a single component, then we need to redeploy only the one changed component. Other components that don't depend on the changed component do not need to be revalidated or redeployed."
  - Its link to OCP: "it is 'closure' in the OCP sense of the word that the CCP addresses... Because **100% closure is not attainable, closure must be strategic**. We design our classes such that they are closed to the most common kinds of changes that we expect or have experienced." CCP amplifies this by gathering into one component the classes closed to the *same types* of changes.
- **CRP — The Common Reuse Principle**: *"Don't force users of a component to depend on things they don't need."*
  - Classes that tend to be **reused together** belong in the same component. "Classes are seldom reused in isolation. More typically, reusable classes collaborate with other classes that are part of the reusable abstraction." Expect lots of intra-component dependencies. Canonical example: a container class and its associated iterators.
  - But its real force is exclusionary: "the CRP tells us more about which classes **shouldn't** be together than about which classes should be together. The CRP says that classes that are not tightly bound to each other should not be in the same component."
  - The mechanism: using one class from a component still creates a full dependency on that component. Every change to the used component likely forces changes in the using one — "Even if no changes are necessary to the using component, it will likely still need to be **recompiled, revalidated, and redeployed**. This is true even if the using component doesn't care about the change."
  - So: "we want to make sure that the classes that we put into a component are **inseparable** — that it is impossible to depend on some and not on the others."
- **The unifying sound bites**:
  - SRP + CCP: *"Gather together those things that change at the same times and for the same reasons. Separate those things that change at different times or for different reasons."*
  - ISP + CRP: *"Don't depend on things you don't need."* — "The CRP is the generic version of the ISP. The ISP advises us not to depend on classes that have methods we don't use. The CRP advises us not to depend on components that have classes we don't use."

## Key Concepts
- **REP is admittedly weak advice.** "Saying that something should 'make sense' is just a way of waving your hands in the air and trying to sound authoritative. The advice is weak because it is hard to precisely explain the glue that holds the classes and modules together into a single component."
  - And why it's kept anyway: "**violations are easy to detect — they don't 'make sense.'** If you violate the REP, your users will know, and they won't be impressed with your architectural skills."
  - "The weakness of this principle is more than compensated for by the strength of the next two principles. Indeed, the CCP and the CRP strongly define this principle, but in a **negative** sense."
- **Inclusive vs. exclusive principles** — REP and CCP are **inclusive**: both tend to make components *larger*. CRP is **exclusive**: it drives components *smaller*. "It is the tension between these principles that good architects seek to resolve."
- **Cohesion is not what we used to think it was** — "We once thought that cohesion was simply the attribute that a module performs one, and only one, function. However, the three principles of component cohesion describe a much more complex variety of cohesion."

## Reference Tables

| Principle | Statement | Effect on size | Related to |
|---|---|---|---|
| **REP** | The granule of reuse is the granule of release | Inclusive (larger) | Release process, versioning |
| **CCP** | Gather classes that change for the same reasons at the same times | Inclusive (larger) | **SRP** for components; OCP's "closure" |
| **CRP** | Don't force users to depend on things they don't need | Exclusive (smaller) | **ISP**, generalized |

The tension diagram (credited to Tim Ottinger) — each edge is the **cost of abandoning the principle on the opposite vertex**:

| Focus on… | Neglecting… | Cost |
|---|---|---|
| REP + CRP | CCP | "Too many components are impacted when simple changes are made" |
| CCP + REP | CRP | "Too many unneeded releases" are generated |
| CCP + CRP | REP | Reuse suffers — where most projects deliberately start |

## Worked Example
**Where to stand in the triangle, and why it moves.**

"A good architect finds a position in that tension triangle that meets the **current** concerns of the development team, but is also aware that those concerns will change over time."

Concretely:

- **Early in a project**, "the CCP is much more important than the REP, because **developability is more important than reuse**." The team is changing things constantly; what matters is that a change lands in one component and only that component gets redeployed. Nobody outside the project is consuming these components yet, so release discipline buys nothing.
- **So projects start on the right-hand side of the triangle**, where "the only sacrifice is reuse."
- **As the project matures and other projects begin to draw from it**, it "will slide over to the left" — release equivalence starts to matter because real external consumers now need version numbers, compatibility guarantees, and change notifications.

The conclusion Martin draws is the useful one: "the component structure of a project can vary with time and maturity. **It has more to do with the way that project is developed and used, than with what the project actually does.**"

And therefore the partitioning is never finished: "Balancing these forces with the needs of the application is nontrivial. Moreover, the balance is almost always **dynamic**. That is, the partitioning that is appropriate today might not be appropriate next year. As a consequence, the composition of the components will likely **jitter and evolve** with time as the focus of the project changes from developability to reusability."

## Key Takeaways
1. Three cohesion principles, and they conflict by design — REP and CCP grow components, CRP shrinks them.
2. REP: if you want a component reused, it must be released — versioned, tracked, documented, announced.
3. CCP is SRP for components: one reason to change, so that one change means one redeployment.
4. Maintainability usually outranks reusability, which is why CCP dominates early.
5. CRP is ISP generalized: depending on a component means depending on *everything* in it, so put only inseparable classes together.
6. Position in the tension triangle is a function of project maturity, not of subject matter — and it should be expected to move.
7. Cohesion is not "does one thing"; it is a balance of reuse, closure, and dependency economics.

## Connects To
- **Ch 7 (SRP)**: CCP is its component-level form.
- **Ch 8 (OCP)**: strategic closure is what CCP gathers.
- **Ch 10 (ISP)**: CRP is its generic version; both reduce to "don't depend on things you don't need."
- **Ch 14 (Component Coupling)**: how the components you've formed may depend on each other.
- **Ch 27 (Services: Great and Small)**: "The Kitty Problem," cited here as the illustration of changes distributed across many components.
