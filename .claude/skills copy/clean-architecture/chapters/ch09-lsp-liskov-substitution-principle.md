# Chapter 9: LSP — The Liskov Substitution Principle

## Core Idea
LSP started as a rule about inheritance and has "morphed into a broader principle of software design that pertains to interfaces and implementations" — because **a simple violation of substitutability can pollute a system's architecture with a significant amount of extra mechanism**.

## Frameworks Introduced
- **Liskov's 1988 definition of a subtype**:
  > "What is wanted here is something like the following **substitution property**: If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2, then S is a subtype of T."
  > — Barbara Liskov, "Data Abstraction and Hierarchy," *SIGPLAN Notices* 23, 5 (May 1988)
- **The test for a violation**: does the *user's* behavior depend on which subtype it has? "Since the behavior of the User depends on the types it uses, those types are not substitutable."
- **LSP applies to any well-defined interface, not just inheritance**: a Java-style interface implemented by several classes; several Ruby classes sharing method signatures; **a set of services that all respond to the same REST interface**. "In all of these situations, and more, the LSP is applicable because there are users who depend on well-defined interfaces, and on the substitutability of the implementations of those interfaces."
- **The architectural diagnostic**: "The best way to understand the LSP from an architectural viewpoint is to look at what happens to the architecture of a system when the principle is **violated**."

## Key Concepts
- **A conforming design** — a `License` class with `calcFee()`, called by a Billing application, and two subtypes `PersonalLicense` and `BusinessLicense` using different fee algorithms. "This design conforms to the LSP because the behavior of the Billing application does not depend, in any way, on which of the two subtypes it uses."
- **The Square/Rectangle problem** — the canonical violation. `Square` is not a proper subtype of `Rectangle` "because the height and width of the `Rectangle` are independently mutable; in contrast, the height and width of the `Square` must change together."
- **The only defense is a type check, which is itself the proof of violation** — "The only way to defend against this kind of LSP violation is to add mechanisms to the User (such as an `if` statement) that detects whether the `Rectangle` is, in fact, a `Square`."
- **Cost of violation at architectural scale** — special-case code, hardcoded vendor names in business logic, "an opportunity for all kinds of horrible and mysterious errors, not to mention **security breaches**," and eventually a whole configuration-driven mechanism that exists solely to paper over non-substitutable interfaces.

## Code Examples

The Square/Rectangle failure, in four lines:

```java
Rectangle r = …
r.setW(5);
r.setH(2);
assert(r.area() == 10);
```
- **What it demonstrates**: "If the `…` code produced a `Square`, then the assertion would fail." The User believes it is talking to a `Rectangle` and is entitled to assume width and height are independent.

The special case no architect should accept:

```java
if (driver.getDispatchUri().startsWith("acme.com"))…
```

## Worked Example
**The taxi aggregator, and the abbreviated field that cost an architecture.**

The system aggregates many taxi dispatch services. Customers use the website to find the most appropriate taxi regardless of company; once they choose, the system dispatches the taxi via a RESTful service. The dispatch URI is part of the driver record in the driver database — the system picks a driver, reads that driver's URI, and uses it.

Driver Bob's dispatch URI:

```
purplecab.com/driver/Bob
```

The system appends the dispatch information and sends it with a PUT:

```
purplecab.com/driver/Bob
    /pickupAddress/24 Maple St.
    /pickupTime/153
    /destination/ORD
```

"Clearly, this means that all the dispatch services, for all the different companies, must conform to the same REST interface. They must treat the `pickupAddress`, `pickupTime`, and `destination` fields **identically**."

**Then Acme happens.** "Now suppose the Acme taxi company hired some programmers who didn't read the spec very carefully. They abbreviated the `destination` field to just `dest`." And Acme cannot simply be dropped: "Acme is the largest taxi company in our area, and Acme's CEO's ex-wife is our CEO's new wife, and … Well, you get the picture."

**Attempt 1 — the `if` statement.** Construct Acme dispatch requests by different rules. "But, of course, no architect worth his or her salt would allow such a construction to exist in the system. Putting the word 'acme' into the code itself creates an opportunity for all kinds of horrible and mysterious errors, not to mention security breaches."

**Why it doesn't even hold.** "What if Acme became even more successful and bought the Purple Taxi company? What if the merged company maintained the separate brands and the separate websites, but unified all of the original companies' systems? Would we have to add another `if` statement for 'purple'?"

**Attempt 2 — the mechanism you actually end up building.** A dispatch-command creation module driven by a configuration database keyed by dispatch URI:

| URI | Dispatch Format |
|---|---|
| Acme.com | `/pickupAddress/%s/pickupTime/%s/dest/%s` |
| `*.*` | `/pickupAddress/%s/pickupTime/%s/destination/%s` |

"And so our architect has had to add a **significant and complex mechanism** to deal with the fact that the interfaces of the restful services are not all substitutable."

The lesson is about proportionality: one careless abbreviation by a third party — three characters — forced a new configuration store, a new command-construction module, and a permanent operational surface, none of which delivers any customer value.

## Key Takeaways
1. Substitutability is defined by the *user's* behavior being unchanged, not by structural similarity between types.
2. Square/Rectangle fails because a supertype's contract (independently mutable dimensions) is broken by the subtype.
3. Needing an `if` to detect which subtype you have *is* the violation, not a fix for it.
4. LSP extends beyond inheritance to Java interfaces, duck-typed classes, and REST services alike.
5. Violations at architectural scale don't produce a small bug — they produce permanent extra mechanism.
6. Hardcoding a vendor's name into business logic is never the answer; it doesn't survive the first merger.

## Connects To
- **Ch 5 (OOP)**: polymorphism is only usable as a boundary mechanism if implementations are substitutable.
- **Ch 8 (OCP)**: non-substitutable implementations force modification of existing code — the OCP failure.
- **Ch 17–18 (Boundaries, Boundary Anatomy)**: what a boundary contract has to guarantee.
- **Ch 27 (Services: Great and Small)**: the same substitutability question at service granularity.
