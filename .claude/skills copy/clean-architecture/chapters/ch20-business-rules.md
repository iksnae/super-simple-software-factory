# Chapter 20: Business Rules

## Core Idea
Business rules are "rules or procedures that make or save the business money" — and they split into **Entities** (Critical Business Rules that would exist even with no computer) and **use cases** (application-specific rules that only make sense inside an automated system), with use cases depending on Entities and never the reverse.

## Frameworks Introduced
- **Critical Business Rules**: rules that "would make or save the business money, **irrespective of whether they were implemented on a computer**. They would make or save money even if they were executed manually."
  - "The fact that a bank charges N% interest for a loan is a business rule that makes the bank money. It doesn't matter if a computer program calculates the interest, or if a clerk with an abacus calculates the interest."
- **Critical Business Data**: the data those rules require — "the data that would exist even if the system were not automated." For a loan: balance, interest rate, payment schedule.
- **Entity** (Ivar Jacobson's term): "an object within our computer system that embodies a small set of critical business rules operating on Critical Business Data. The Entity object either contains the Critical Business Data or has very easy access to that data. The interface of the Entity consists of the functions that implement the Critical Business Rules that operate on that data."
  - Because critical rules and critical data "are inextricably bound, they are a good candidate for an object."
  - **Not an OO requirement**: "You don't need to use an object-oriented language to create an Entity. All that is required is that you **bind the Critical Business Data and the Critical Business Rules together in a single and separate software module**."
- **Use case**: "a description of the way that an automated system is used. It specifies the input to be provided by the user, the output to be returned to the user, and the processing steps involved in producing that output. A use case describes **application-specific** business rules as opposed to the Critical Business Rules within the Entities."
  - "Use cases contain the rules that specify how and when the Critical Business Rules within the Entities are invoked. **Use cases control the dance of the Entities.**"
  - A use case is an object with one or more functions implementing the application-specific rules, plus data elements: input data, output data, and references to the Entities it interacts with.
- **Request and Response Models**: "The use case class accepts simple request data structures for its input, and returns simple response data structures as its output. **These data structures are not dependent on anything.** They do not derive from standard framework interfaces such as `HttpRequest` and `HttpResponse`. They know nothing of the web, nor do they share any of the trappings of whatever user interface might be in place."
  - Why it matters: "If the request and response models are not independent, then the use cases that depend on them will be **indirectly bound** to whatever dependencies the models carry with them."

## Key Concepts
- **The Entity is pure business and nothing else.** "This class stands alone as a representative of the business. It is **unsullied with concerns about databases, user interfaces, or third-party frameworks**. It could serve the business in any system, irrespective of how that system was presented, or how the data was stored, or how the computers in that system were arranged."
- **Use cases hide the delivery mechanism.** "From the use case, it is **impossible to tell whether the application is delivered on the web, or on a thick client, or on a console, or is a pure service**. This is very important. Use cases do not describe how the system appears to the user... How the data gets in and out of the system is irrelevant to the use cases."
- **Why Entities are *higher* level than use cases** — the counterintuitive ordering, explained via Chapter 19's definition:
  - "Use cases are **specific to a single application** and, therefore, are **closer to the inputs and outputs** of that system. Entities are **generalizations that can be used in many different applications**, so they are **farther from the inputs and outputs**."
  - Therefore: "Use cases depend on Entities; Entities do not depend on use cases." And: "**Entities have no knowledge of the use cases that control them.**"
- **Don't put Entity references in request/response models.** "You might think this makes sense because the Entities and the request/response models share so much data. **Avoid this temptation!** The purpose of these two objects is very different. Over time they will change for very different reasons, so tying them together in any way violates the Common Closure and Single Responsibility Principles. The result would be **lots of tramp data, and lots of conditionals** in your code."

## Reference Tables

| | Entity | Use case |
|---|---|---|
| Contains | Critical Business Rules + Critical Business Data | Application-specific business rules |
| Would exist without a computer? | **Yes** — a clerk with an abacus would apply them | **No** — "they make sense only as part of an automated system" |
| Scope | Generalization usable across many applications | Specific to a single application |
| Level | **Higher** (farther from IO) | **Lower** (closer to IO) |
| Dependency direction | Knows nothing of use cases | Depends on Entities |
| Example | A `Loan` with balance, rate, schedule, and the rules operating on them | "Don't show the payment estimation screen until contact info is validated and the credit score is confirmed ≥ 500" |

## Worked Example
**The loan, at two levels.**

**The Entity.** A `Loan` holds three pieces of Critical Business Data — loan balance, interest rate, payment schedule — and presents three related Critical Business Rules at its interface. The interest calculation is the archetype: the bank charges N% whether a program or a clerk computes it. The rule and the data it needs go into one module, and that module knows nothing about how loans are stored, displayed, or transmitted.

**The use case.** A bank officer creates a new loan. The bank decides it does not want loan officers offering payment estimates until they have "gathered, and validated, contact information and ensured that the candidate's credit score is 500 or higher." So the system "will not proceed to the payment estimation screen until the contact information screen has been filled out and verified, and the credit score has been confirmed to be greater than the cutoff."

Notice what kind of rule that is. It makes the bank money — it prevents officers wasting time on unqualified applicants — but **it would be meaningless without an automated system**. There is no "payment estimation screen" for a clerk with an abacus. That is precisely the line between the two categories.

And notice what the use case description *contains*: inputs from the user, outputs to the user, processing steps, and a reference to the `Customer` **entity**, "which contains the Critical Business Rules that govern the relationship between the bank and its customers." The use case orchestrates; the Entity rules.

What the use case description conspicuously **omits**: whether the screen is a web page, a desktop window, a console prompt, or an API response. It "does not describe the user interface other than to informally specify the data coming in from that interface, and the data going back out."

**Why the layering runs the way it does.** The instinct is that "use case" sounds application-level and "entity" sounds like a database row, so surely the entity is the lower-level detail. Chapter 19's definition settles it: level is distance from IO. The credit-score-before-estimate rule exists only because of screens, so it sits near the inputs and outputs. The interest calculation would survive the deletion of every screen, every database, and the computer itself — so it sits at the center. Dependencies point inward: use case → Entity.

## Key Takeaways
1. Critical Business Rules and Critical Business Data would exist without any computer; bind them together into an Entity.
2. An Entity needs no OO language — only a single, separate module holding the rules and the data they operate on.
3. Use cases are application-specific rules that exist only because the system is automated; they orchestrate Entities.
4. A use case must not reveal its delivery mechanism — web, thick client, console, or service must be indistinguishable from it.
5. Entities are higher level than use cases, because they are further from inputs and outputs and reusable across applications.
6. Request and response models must depend on nothing — no `HttpRequest`, no framework base types, and no Entity references.
7. "Business rules are the reason a software system exists... They are **the family jewels**" — they should be the most independent and reusable code in the system, with lesser concerns plugged into them.

## Connects To
- **Ch 19 (Policy and Level)**: the distance-from-IO definition that orders Entities above use cases.
- **Ch 11 (DIP)**: the dependency direction between use cases and Entities.
- **Ch 13 (CCP) / Ch 7 (SRP)**: why request/response models must not reference Entities.
- **Ch 22 (The Clean Architecture)**: Entities and Use Cases as the inner two circles.
- **Ch 23 (Presenters and Humble Objects)**: what happens to the response model on its way to a screen.
- **Ch 30–32 (Details)**: the "baser concerns" the business rules must stay unsullied by.
