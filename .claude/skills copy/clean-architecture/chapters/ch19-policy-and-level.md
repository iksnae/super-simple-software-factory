# Chapter 19: Policy and Level

## Core Idea
"A computer program is a detailed description of the policy by which inputs are transformed into outputs" — and **level is the distance from the inputs and outputs**, which is what source code dependencies should be coupled to, *not* the flow of data.

## Frameworks Introduced
- **Software systems are statements of policy.** In nontrivial systems that policy breaks into many smaller statements: how business rules are calculated, how reports are formatted, how input data is validated.
- **Grouping rule**: "Policies that change for the same reasons, and at the same times, are at the **same level** and belong together in the same component. Policies that change for different reasons, or at different times, are at **different levels** and should be separated."
- **The architecture is a DAG of levels**: "The nodes of the graph are the components that contain policies at the same level. The directed edges are the dependencies between those components. They connect components that are at different levels."
  - Those edges are **source code, compile-time dependencies** — `import` in Java, `using` in C#, `require` in Ruby. "They are the dependencies that are necessary for the compiler to function."
  - "In every case, **low-level components are designed so that they depend on high-level components**."
- **The strict definition of level**: *"the distance from the inputs and outputs."*
  - "The farther a policy is from both the inputs and the outputs of the system, the higher its level. The policies that manage input and output are the **lowest-level** policies in the system."
  - (Footnote: Meilir Page-Jones called the highest-level component the **"Central Transform"** in *The Practical Guide to Structured Systems Design*, 2nd ed., Yourdon Press, 1988.)
- **Decouple dependencies from data flow, couple them to level**: "Note that the data flows and the source code dependencies do not always point in the same direction. This, again, is part of the art of software architecture. **We want source code dependencies to be decoupled from data flow and coupled to level.**"

## Key Concepts
- **Change frequency correlates with level, inversely.** "Higher-level policies — those that are farthest from the inputs and outputs — tend to change **less frequently, and for more important reasons**, than lower-level policies. Lower-level policies — those that are closest to the inputs and outputs — tend to change **frequently, and with more urgency, but for less important reasons**."
- **Which is exactly why the arrows must point up-level**: "Keeping these policies separate, with all source code dependencies pointing in the direction of the higher-level policies, reduces the impact of change. **Trivial but urgent changes at the lowest levels of the system have little or no impact on the higher, more important, levels.**"
- **Lower-level components are plugins to higher-level ones.** "The `Encryption` component knows nothing of the `IODevices` component; the `IODevices` component depends on the `Encryption` component."

## Code Examples

The intuitive version, which is the wrong architecture:

```java
function encrypt() {
    while(true)
        writeChar(translate(readChar()));
}
```
- **What it demonstrates**: "This is incorrect architecture because the high-level `encrypt` function depends on the lower-level `readChar` and `writeChar` functions." It reads naturally, follows the data flow exactly, and inverts the dependency structure you want.

## Worked Example
**The encryption program, and why the obvious code is backwards.**

The system: read characters from an input device, translate them using a table, write the translated characters to an output device. Three pieces — reader, translator, writer.

**Locating the levels.** By the strict definition, level is distance from inputs and outputs. The reader sits *on* the input; the writer sits *on* the output. **`Translate` is the highest-level component** because it is farthest from both.

**The trap.** Data flows reader → translate → writer, so the natural single-line implementation nests the calls in exactly that order. But that makes `encrypt` — high-level policy — name `readChar` and `writeChar`, which are the lowest-level things in the system. The data flow was allowed to dictate the source code dependencies.

**The correction.** Introduce `CharReader` and `CharWriter` interfaces owned by the high-level side. Draw a border around `Encrypt` plus those two interfaces: **all dependencies crossing that border point inward**. `ConsoleReader` and `ConsoleWriter` become concrete classes on the outside — "they are low level because they are close to the inputs and outputs."

**What that buys.** "This structure decouples the high-level encryption policy from the lower-level input/output policies. This makes the encryption policy **usable in a wide range of contexts**. When changes are made to the input and output policies, they are not likely to affect the encryption policy."

**And the probability argument that justifies the effort.** "Even in the trivial example of the encryption program, it is far more likely that the **IO devices will change** than that the **encryption algorithm will change**. If the encryption algorithm does change, it will likely be for a more substantive reason than a change to one of the IO devices."

That asymmetry — frequent trivial change at the edges, rare important change at the center — is the whole justification for pointing every arrow inward, and it holds at every scale from this three-component toy to a full enterprise system.

**The chapter's closing exercise.** "At this point, this discussion of policies has involved a mixture of the Single Responsibility Principle, the Open-Closed Principle, the Common Closure Principle, the Dependency Inversion Principle, the Stable Dependencies Principle, and the Stable Abstractions Principle. **Look back and see if you can identify where each principle was used, and why.**"

A reading of that exercise:
- **SRP / CCP** — grouping policies that change for the same reasons at the same times into one component.
- **OCP** — the high-level `Encrypt` unit is closed to changes in IO devices while remaining open to new ones.
- **DIP** — `CharReader`/`CharWriter` interfaces invert the dependency that the data flow would have imposed.
- **SDP** — dependencies run toward the more stable (higher-level, less frequently changing) `Encryption` component.
- **SAP** — that stable component is the one expressed as abstractions, so its stability doesn't make it rigid.

## Key Takeaways
1. All software is policy; architecture is the separation and regrouping of policies by how they change.
2. Level = distance from inputs and outputs. IO policies are always lowest; the central transform is highest.
3. Source code dependencies must follow *level*, never data flow — the two frequently disagree.
4. The naturally-written nested call chain usually encodes exactly the wrong dependency direction.
5. High-level policy changes rarely and importantly; low-level policy changes often and urgently. Point the arrows so the urgent noise can't reach the important core.
6. The result is a DAG of components with lower levels plugging into higher ones.

## Connects To
- **Ch 8 (OCP)**: the hierarchy of protection based on level.
- **Ch 11 (DIP)** / **Ch 14 (SDP, SAP)**: the principles this chapter composes.
- **Ch 17–18 (Boundaries, Boundary Anatomy)**: crossing between levels.
- **Ch 20 (Business Rules)**: why Entities are higher level than use cases.
- **Ch 22 (The Clean Architecture)**: concentric circles ordered exactly by this definition of level.
