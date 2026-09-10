# Chapter 10: ISP — The Interface Segregation Principle

## Core Idea
"It is harmful to depend on modules that contain more than you need" — a rule that looks like a static-typing quirk at source level and turns out to be an architectural one: **depending on something that carries baggage you don't need can cause you troubles that you didn't expect.**

## Frameworks Introduced
- **The core diagram**: an `OPS` class with `op1`, `op2`, `op3`, used by `User1`, `User2`, `User3` — each using exactly one operation.
  - In a language like Java, "the source code of `User1` will **inadvertently depend** on `op2` and `op3`, even though it doesn't call them. This dependence means that a change to the source code of `op2` in `OPS` will force `User1` to be recompiled and redeployed, **even though nothing that it cared about has actually changed**."
- **The fix**: segregate the operations into interfaces. `User1` then depends on `U1Ops` and `op1`, and **not** on `OPS`, so a change to `OPS` that `User1` doesn't care about causes no recompilation or redeployment.
- **ISP at architectural scale**: architect wants framework **F** in system **S**; F's authors bound it to database **D**. So S → F → D.
  - "Now suppose that D contains features that F does not use and, therefore, that S does not care about. **Changes to those features within D may well force the redeployment of F and, therefore, the redeployment of S.** Even worse, **a failure of one of the features within D may cause failures in F and S**."

## Key Concepts
- **Why the source-level version is language-dependent** — "Statically typed languages like Java force programmers to create declarations that users must `import`, or `use`, or otherwise include. It is these included declarations in source code that create the source code dependencies that force recompilation and redeployment."
- **Dynamic languages don't have the source-level problem** — in Ruby and Python "such declarations don't exist in source code. Instead, they are inferred at runtime. Thus there are no source code dependencies to force recompilation and redeployment. **This is the primary reason that dynamically typed languages create systems that are more flexible and less tightly coupled than statically typed languages.**"
- **And that is exactly the objection the chapter answers** — "This fact could lead you to conclude that the ISP is a **language** issue, rather than an **architecture** issue." Stepping back reveals the deeper concern, which holds "at a much higher, architectural level" regardless of typing discipline.
- **Two distinct costs of unneeded dependencies**: unnecessary **redeployment** (a change you don't care about forces a rebuild) and unnecessary **failure propagation** (a fault in a feature you never use takes you down).

## Mental Models
- **Distinguish the mechanism from the motivation.** The recompile-and-redeploy story is the mechanism, and it *is* language-specific. The motivation — don't take on more than you need — survives translation to any language and any scale, from a class's method set to a framework's transitive database dependency.
- **Read "what does this pull in?" before adopting a dependency.** The S → F → D chain is the everyday form: you evaluate the framework, and you inherit its database, its release cadence, and its outages.
- **Fan-in of unneeded features is a blast radius, not just build time.** The redeployment consequence is annoying; the failure-propagation consequence is the one that pages you.

## Reference Tables

| Level | Depending on more than you need | Consequence |
|---|---|---|
| Class / interface | `User1` depends on `OPS`, which has `op2`, `op3` | Change to `op2` forces `User1` recompile + redeploy |
| Framework / system | S depends on F, which is bound to D | Change in unused D features → redeploy F → redeploy S; **failure in unused D features → failures in F and S** |

| Language type | Source-code dependency created? | ISP still applies? |
|---|---|---|
| Statically typed (Java, C#) | Yes — via `import`/`use`/`include` declarations | Yes, at both source and architectural level |
| Dynamically typed (Ruby, Python) | No — inferred at runtime | Yes, at the architectural level |

## Key Takeaways
1. Don't depend on modules containing more than you need — at any scale.
2. Segregating operations into per-client interfaces removes dependencies on operations you never call.
3. The recompile/redeploy mechanism is specific to statically typed languages; the underlying harm is not.
4. Dynamic typing genuinely produces looser coupling at source level — and does not exempt you from ISP architecturally.
5. Unneeded transitive dependencies cost you both redeployment churn and inherited failure modes.
6. Evaluate a framework by what it drags in, not only by what it offers.

## Connects To
- **Ch 8 (OCP)**: `FinancialReportRequester` exists to prevent transitive dependencies — the same "don't depend on what you don't use" principle, applied for information hiding.
- **Ch 13 (Component Cohesion)**: the **Common Reuse Principle** — "We'll explore this idea in more detail when we discuss the Common Reuse Principle." (Note: the text points to Chapter 13's material; the chapter reference in the source reads "Chapter 13, 'Component Cohesion'.")
- **Ch 14 (Component Coupling)**: stability and the direction of dependencies between components.
- **Ch 32 (Frameworks Are Details)**: the S → F → D problem stated as a policy about frameworks.
