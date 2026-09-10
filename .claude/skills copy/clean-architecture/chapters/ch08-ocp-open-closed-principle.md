# Chapter 8: OCP — The Open-Closed Principle

## Core Idea
"A software artifact should be open for extension but closed for modification" (Meyer, 1988) — and at the architectural level this means partitioning the system into components and arranging them in a **dependency hierarchy that protects higher-level components from changes in lower-level ones**.

## Frameworks Introduced
- **The OCP, stated**: "the behavior of a software artifact ought to be extendible, without having to modify that artifact."
  - Why it is the point of the whole discipline: "This is the most fundamental reason that we study software architecture. Clearly, **if simple extensions to the requirements force massive changes to the software, then the architects of that software system have engaged in a spectacular failure**."
- **The two-step recipe**: minimize changed code — ideally to **zero** — by
  1. **properly separating the things that change for different reasons** (SRP), then
  2. **organizing the dependencies between those things properly** (DIP).
- **The protection rule** — the sentence Martin repeats for emphasis:
  > **If component A should be protected from changes in component B, then component B should depend on component A.**
- **Hierarchy of protection based on level**: Interactors are the highest-level concept and the most protected; Views are among the lowest and least protected; Presenters are higher than Views but lower than Controller or Interactor.
  - "Architects separate functionality based on **how, why, and when it changes**, and then organize that separated functionality into a hierarchy of components."
- **Directional Control**: interfaces exist in the design specifically to point dependencies the right way. `FinancialDataGateway` sits between `FinancialReportGenerator` and `FinancialDataMapper` "to invert the dependency that would otherwise have pointed from the Interactor component to the Database component." Same for `FinancialReportPresenter` and the two View interfaces.
- **Information Hiding**: `FinancialReportRequester` serves a different purpose — protecting the `FinancialReportController` from knowing too much about the Interactor's internals. Without it, the Controller would have **transitive dependencies** on the `FinancialEntities`.
  - "Transitive dependencies are a violation of the general principle that **software entities should not depend on things they don't directly use**."

## Key Concepts
- **Why the Interactor is privileged** — "Because it contains the business rules. The Interactor contains the highest-level policies of the application. All the other components are dealing with peripheral concerns. The Interactor deals with the central concern."
- **Level is relative, and nests** — "Even though the Controller is peripheral to the Interactor, it is nevertheless **central to the Presenters and Views**. And while the Presenters might be peripheral to the Controller, they are **central to the Views**."
- **Reading the diagram's notation** — `<I>` marks interfaces, `<DS>` marks data structures; open arrowheads are *using* relationships, closed arrowheads are *implements* or *inheritance* relationships.
- **All dependencies are source code dependencies** — "An arrow pointing from class A to class B means that the source code of class A mentions the name of class B, and class B mentions nothing about class A." `FinancialDataMapper` knows about `FinancialDataGateway` through an implements relationship; `FinancialGateway` knows nothing at all about `FinancialDataMapper`.
- **Every boundary is crossed in one direction only** — "each double line is crossed in one direction only. This means that all component relationships are unidirectional... These arrows point toward the components that we want to protect from change."

## Mental Models
- **Ask "how much old code must change?" as the design question.** Not "can this be done" — anything can be done. A good architecture's answer is *ideally zero*.
- **Complexity that exists to orient dependencies is not accidental complexity.** "If you recoiled in horror from the class design shown earlier, look again. Much of the complexity in that diagram was intended to make sure that the dependencies between the components pointed in the correct direction."
- **Protection is bidirectional in intent, asymmetric in mechanism.** The first priority is protecting the Interactor from the Controller — but the Controller is *also* protected from the Interactor, by hiding the Interactor's internals behind an interface.
- **OCP is normally taught as a class-and-module principle**, and "takes on even greater significance when we consider the level of architectural components."

## Reference Tables

The component hierarchy from the thought experiment, most protected first:

| Component | Level | Protected from | Contains |
|---|---|---|---|
| **Interactor** | Highest | Database, Controller, Presenters, Views — *anything* | The business rules; the highest-level policies |
| **Controller** | High | Presenters, Views | Request handling |
| **Presenters** | Middle | Views | Formatting decisions |
| **Views** | Lowest | (nothing) | Screen/print rendering |
| **Database** | Detail | — | Storage mechanism |

Interfaces and what each one is *for*:

| Interface | Purpose |
|---|---|
| `FinancialDataGateway` | Invert the dependency that would otherwise run Interactor → Database |
| `FinancialReportPresenter` | Invert the dependency from the Interactor toward presentation |
| The two View interfaces | Invert the dependency from Presenters toward Views |
| `FinancialReportRequester` | **Information hiding** — keep the Controller from acquiring transitive dependencies on `FinancialEntities` |

## Worked Example
**The financial summary, and the report that should cost zero.**

The starting system displays a financial summary on a web page: the data scrolls, and negative numbers render in **red**.

The stakeholders now ask for the same information as a report printed on a black-and-white printer — properly paginated, with page headers, page footers, and column labels, and negative numbers surrounded by **parentheses**.

"Clearly, some new code must be written. But **how much old code will have to change?**"

**Step 1 — apply SRP to find the seam.** "The essential insight here is that generating the report involves two separate responsibilities: **the calculation of the reported data**, and **the presentation of that data** into a web- and printer-friendly form."

That yields a data-flow view: an analysis procedure inspects the financial data and produces *reportable data*, which two reporter processes then format appropriately. Note that the difference between red-text and parenthesized-negatives lives entirely on the presentation side — the calculation is identical.

**Step 2 — organize the dependencies so the seam holds.** Separation alone doesn't protect anything; the arrows have to point correctly, or a change in presentation still propagates into calculation. So the processes are partitioned into classes and the classes grouped into components:

- **Controller** (upper left)
- **Interactor** (upper right) — the business rules
- **Database** (lower right)
- **Presenters and Views** (lower left — four components)

**Step 3 — read the result.** Every component boundary is crossed in one direction only, and every arrow points toward what is being protected. The Interactor sits at the top of the hierarchy: "Changes to the Database, or the Controller, or the Presenters, or the Views, will have **no impact on the Interactor**."

So the answer to the original question — how much old code changes to add a printed report — is: **a new Presenter and a new View**. The calculation, the Controller, the Interactor, and the Database are untouched. That is what "closed for modification" buys, and the several interfaces that looked like ceremony are exactly what purchased it.

## Key Takeaways
1. OCP is the reason architecture exists: extensions to requirements should not force massive change.
2. Achieve it in two moves — separate by reason-for-change (SRP), then orient the dependencies (DIP).
3. To protect A from B, make **B depend on A**. That single sentence is the operational rule.
4. Interfaces in the design are dependency-direction tools, not decoration; the resulting complexity is purchased deliberately.
5. Hide internals as well as inverting dependencies — transitive dependencies violate "don't depend on what you don't use."
6. Level determines protection: business rules highest and most protected, views lowest and least.
7. Boundaries are unidirectional; every arrow points at what must not change.

## Connects To
- **Ch 7 (SRP)**: step one of the recipe — separate what changes for different reasons.
- **Ch 10 (ISP)** and **Ch 14 (Component Coupling, Common Reuse Principle)**: "don't depend on things you don't use," which the `FinancialReportRequester` interface enforces.
- **Ch 11 (DIP)**: step two — the mechanism for pointing the arrows.
- **Ch 19 (Policy and Level)**: the notion of "level" defined precisely.
- **Ch 22 (The Clean Architecture)**: this thought experiment's component layout *is* the clean architecture, in miniature.
- **Clean Code, Ch 10**: OCP applied to a class — the `Sql` refactoring into a set of closed classes.
