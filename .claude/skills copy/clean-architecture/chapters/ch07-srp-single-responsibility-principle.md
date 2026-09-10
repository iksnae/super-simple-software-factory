# Chapter 7: SRP — The Single Responsibility Principle

## Core Idea
**A module should be responsible to one, and only one, actor** — not "a module should do one thing," which is a different (and lower-level) principle that SRP is constantly confused with because of its "particularly inappropriate name."

## Frameworks Introduced
- **The three progressive statements of SRP**:
  1. "A module should have one, and only one, **reason to change**." (the historical form)
  2. "A module should be responsible to one, and only one, **user or stakeholder**." (closer — the reasons to change *are* the people)
  3. "A module should be responsible to one, and only one, **actor**." (final — because more than one person usually wants the same change; an *actor* is that group)
- **What SRP is not**: "A function should do one, and only one, thing. We use that principle when we are refactoring large functions into smaller functions; we use it at the lowest levels. But it is **not** one of the SOLID principles — it is not the SRP."
- **Module** = a source file, most of the time. Where languages don't use source files, "a module is just a cohesive set of functions and data structures." And "that word 'cohesive' implies the SRP. **Cohesion is the force that binds together the code responsible to a single actor.**"
- **The rule that follows from both symptoms**: *separate the code that different actors depend on.*
- **SRP as an active corollary to Conway's Law**: "The best structure for a software system is heavily influenced by the social structure of the organization that uses it so that each software module has one, and only one, reason to change."

## Key Concepts
- **Actor** — one or more people who require the same change. The unit SRP is actually about.
- **Symptom 1: Accidental Duplication** — code that different actors depend on placed in close proximity, so a change made for one actor silently corrupts another's behavior.
- **Symptom 2: Merges** — many methods responsible to different actors in one source file means different teams check it out and collide. "Merges are risky affairs. Our tools are pretty good nowadays, but no tool can deal with every merge case. In the end, there is always risk."
- **All other symptoms have the same shape**: "they all involve multiple people changing the same source file for different reasons."
- **The class-as-scope answer to the "one function per class" objection** — the number of functions needed to calculate pay, generate a report, or save data "is likely to be large in each case. Each of those classes would have many private methods in them. Each of the classes that contain such a family of methods is **a scope**. Outside of that scope, no one knows that the private members of the family exist."

## Mental Models
- **Trace each method to a reporting line, not to a subject-matter topic.** In the `Employee` example the split isn't payroll-vs-reporting-vs-persistence as *topics* — it's CFO vs. COO vs. CTO as *organizations*. That's what makes it an actor question.
- **DRY can hurt you when the duplication is only accidental.** The developers in the example were being careful *not* to duplicate code — extracting `regularHours()` was textbook. The extraction was wrong because the two callers answer to different actors, and the code only *looked* the same.
- **SRP reappears twice more, renamed.** At the component level it becomes the **Common Closure Principle**. At the architectural level it becomes the **Axis of Change** responsible for creating **Architectural Boundaries**.

## Reference Tables

The three solutions, and what each costs:

| Solution | Shape | Trade-off |
|---|---|---|
| **Separate data from functions** (Fig 7.3) | `EmployeeData` — a plain data structure with no methods — shared by three classes, each holding only its own code. The three classes are not allowed to know about each other | Accidental duplication is impossible. But developers now have three classes to instantiate and track |
| **Facade** (Fig 7.4) | An `EmployeeFacade` containing very little code, responsible for instantiating and delegating to the three | Restores a single entry point; adds one more type |
| **Facade with the important rule retained** (Fig 7.5) | Keep the most important method in the original `Employee` class and use that class as a facade for the lesser functions | For developers who "prefer to keep the most important business rules closer to the data" |

## Worked Example
**The `Employee` class, and the report that was quietly wrong for months.**

An `Employee` class in a payroll application with three methods:

| Method | Specified by | Reports to |
|---|---|---|
| `calculatePay()` | the accounting department | the **CFO** |
| `reportHours()` | the human resources department | the **COO** |
| `save()` | the database administrators | the **CTO** |

Three methods, three actors, one class. "By putting the source code for these three methods into a single `Employee` class, the developers have coupled each of these actors to the others. This coupling can cause the actions of the CFO's team to affect something that the COO's team depends on."

Now the failure, step by step:

1. `calculatePay()` and `reportHours()` share an algorithm for calculating non-overtime hours. The developers, **careful not to duplicate code**, extract it into `regularHours()`.
2. The CFO's team decides non-overtime hours need to be calculated differently. The COO's team in HR does *not* want that tweak — they use non-overtime hours for a different purpose.
3. A developer is assigned the change, finds the convenient `regularHours()` called by `calculatePay()`, and **does not notice it is also called by `reportHours()`**.
4. The change is made and carefully tested. The CFO's team validates the new behavior. The system deploys.
5. "Of course, the COO's team doesn't know that this is happening. The HR personnel continue to use the reports generated by the `reportHours()` function — but now they contain **incorrect numbers**."
6. "Eventually the problem is discovered, and the COO is livid because the bad data has cost his budget **millions of dollars**."

Note what did *not* go wrong: nobody was careless, the tests passed, the reviewer approved, and the person who asked for the change got exactly what they asked for. The defect was structural — two actors' code sharing a function.

**The merge version of the same defect.** The CTO's DBAs decide the `Employee` table needs a simple schema change. Independently, the COO's HR clerks need the hours report reformatted. Two developers, possibly from two different teams, check out `Employee` and collide. "In our example, the merge puts both the CTO and the COO at risk. It's not inconceivable that the CFO could be affected as well."

## Key Takeaways
1. SRP is about **actors**, not about doing one thing. The name misleads; the content is organizational.
2. Cohesion is the force binding code that answers to a single actor — that's the definition, not a vague quality.
3. Accidental duplication is the trap: code that looks identical but serves different actors must not be shared.
4. Merge conflicts on a file are evidence of an SRP violation, not just a workflow annoyance.
5. Fix it by moving functions into separate classes; use a Facade if the instantiation burden matters.
6. Classes with families of private methods are scopes, so "one public function per class" is not the outcome.
7. SRP is Conway's Law made actionable: mirror the social structure of the organization that uses the system.

## Connects To
- **Ch 8 (OCP)**: separating things that change for different reasons is step one of the OCP thought experiment.
- **Ch 13 (Component Cohesion)**: the **Common Closure Principle** — SRP for components.
- **Ch 16–17 (Independence, Boundaries)**: the **Axis of Change** and where boundaries get drawn.
- **Ch 34 (The Missing Chapter)**: what this looks like in packages and directories.
- **Clean Code, Ch 10**: SRP at class scale, with the 25-word test and cohesion metrics.
