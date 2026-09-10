# Chapter 33: Case Study — Video Sales

## Core Idea
A worked application of the whole book: identify actors and use cases, partition components so **a change to one actor does not affect any other**, point every dependency toward higher-level policy — then keep deployment grouping as a decision you can revise later.

## Frameworks Introduced
- **The process, in order**: "Our first step in determining the initial architecture of the system is to **identify the actors and use cases**."
- **Actors are the sources of change** (SRP applied at system scale): "According to the Single Responsibility Principle, these four actors will be the **four primary sources of change** for the system. Every time some new feature is added, or some existing feature is changed, that step will be taken to serve one of these actors. Therefore we want to partition the system such that **a change to one actor does not affect any of the other actors**."
- **Abstract use cases**: "An abstract use case is one that **sets a general policy that another use case will flesh out**." `View Catalog as Viewer` and `View Catalog as Purchaser` both inherit from an abstract `View Catalog`.
  - The judgment behind it: "it was **not strictly necessary** for me to create that abstraction. I could have left the abstract use case out of the diagram without compromising any of the features of the overall product. On the other hand, these two use cases are so similar that I thought it wise to **recognize the similarity and find a way to unify it early in the analysis**."
  - (Footnote: "This is my own notation for 'abstract' use cases. It would have been more standard to use a UML stereotype such as `<<abstract>>`, but I don't find adhering to such standards very useful nowadays.")
- **Two dimensions of separation** — the chapter's summary of what the diagram encodes:
  1. "the separation of **actors** based on the Single Responsibility Principle"
  2. "the **Dependency Rule**"
  - "The goal of both is to separate components that change for different reasons, and at different rates. **The different reasons correspond to the actors; the different rates correspond to the different levels of policy.**"

## Key Concepts
- **Arrow semantics in the diagram**: "the **using** relationships (open arrows) point **with** the flow of control, and the **inheritance** relationships (closed arrows) point **against** the flow of control. This depicts our use of the **Open-Closed Principle** to make sure that the dependencies flow in the right direction, and that changes to low-level details do not ripple upward to affect high-level policies."
- **Flow of control vs. dependencies**: "The flow of control proceeds from **right to left**. Input occurs at the controllers, and that input is processed into a result by the interactors. The presenters then format the results, and the views display those presentations. Notice that the arrows do **not** all flow from the right to the left. In fact, **most of them point from left to right.** This is because the architecture is following the Dependency Rule."
- **Handling the abstract use case in components**: special `Catalog View` and `Catalog Presenter` components — "I assume that those views and presenters will be coded into **abstract classes** within those components, and that the inheriting components will contain view and presenter classes that will inherit from those abstract classes."
- **The scope disclaimer, stated honestly**: "The use cases shown are **not a complete list**. For example, you won't find log-in or log-out use cases. The reason for this omission is simply to manage the size of the problem in this book."

## Worked Example
**The product.** Software for a website that sells videos — "reminiscent of cleancoders.com, the site where I sell my software tutorial videos."

The requirements, compactly:

- Videos are sold on the web to **individuals** and to **businesses**.
- Individuals pay one price to **stream** and a higher price to **download** and own permanently.
- Business licenses are **streaming only**, purchased in batches with **quantity discounts**.
- "Individuals typically act as **both the viewers and the purchasers**. Businesses, in contrast, often have people who **buy** the videos that **other people** will watch."
- **Video authors** supply video files, written descriptions, and ancillary files — exams, problems, solutions, source code, and other materials.
- **Administrators** add new video series, add and delete videos within series, and establish prices for various licenses.

**The four actors**, which the requirements above already separate:

| Actor | What they change the system to do |
|---|---|
| **Viewer** | Watch videos; view the catalog as a viewer |
| **Purchaser** | Buy licenses (individual or batch); view the catalog as a purchaser |
| **Author** | Supply videos, descriptions, and ancillary materials |
| **Administrator** | Manage series, videos, and pricing |

Notice why the Viewer/Purchaser split is real rather than pedantic: for individuals they're the same person, but for businesses **one person buys what another person watches**. That is two actors with two independent reasons to change, and SRP says they get separate components even though they look alike today.

**The component architecture.** Double lines are architectural boundaries. The familiar four categories — **views, presenters, interactors, controllers** — appear, "**broken up by their corresponding actors**." That is the two-dimensional partition: one axis is architectural layer, the other is actor.

"Each of the components represents a **potential** `.jar` file or `.dll` file. Each of those components will contain the views, presenters, interactors, and controllers that have been allocated to it."

**The deployment question, and the answer that matters most.**

> "Would I really break the system up into all these components, and deliver them as `.jar` or `.dll` files? **Yes and no.** I would certainly break the **compile and build environment** up this way, so that I could build independent deliverables like that. I would also **reserve the right to combine** all those deliverables into a smaller number of deliverables if necessary."

Three groupings he names, from finest to coarsest:

| Grouping | Deliverables |
|---|---|
| By layer | **Five** jars — views, presenters, interactors, controllers, utilities |
| Layer-pairs | **Two** jars — views + presenters in one; interactors + controllers + utilities in the other |
| "Even more primitive" | **Two** jars — views + presenters in one; everything else in the other |

"Keeping these options open will allow us to **adapt the way we deploy the system based on how the system changes over time**." And in the conclusion: "Once you have structured the code this way, you can **mix and match** how you want to actually deploy the system. You can group the components into deployable deliverables in any way that makes sense, and **easily change that grouping when conditions change**."

This is Chapter 16's decoupling-mode argument made concrete. The *source structure* is fine-grained and permanent; the *deployment structure* is coarse-grained and revisable. You pay the design cost once and buy the ability to slide between monolith and many-deliverable packaging without touching the code.

## Key Takeaways
1. Start by identifying actors and use cases — actors are the primary sources of change (SRP at system scale).
2. Partition so a change serving one actor cannot affect another; that is the first dimension of separation.
3. The second dimension is the Dependency Rule: all dependencies cross boundaries toward higher-level policy.
4. Reasons for change map to actors; rates of change map to levels of policy.
5. Unify genuinely similar use cases with an abstract use case, implemented as abstract view/presenter classes that concrete components inherit.
6. Using relationships follow the flow of control; inheritance relationships oppose it — that is OCP doing its job.
7. Structure the build environment finely; choose the deployment grouping separately and change it as conditions change.

## Connects To
- **Ch 7 (SRP)**: actors as the definition of a responsibility.
- **Ch 8 (OCP)**: the inheritance arrows opposing control flow.
- **Ch 16 (Independence)**: decoupling modes and the freedom to regroup deliverables.
- **Ch 22 (The Clean Architecture)**: views, presenters, interactors, controllers, and the Dependency Rule.
- **Ch 20 (Business Rules)**: use cases as the unit of application-specific policy.
- **Ch 34 (The Missing Chapter)**: what these components look like as packages and directories.
