# Chapter 3: Paradigm Overview

## Core Idea
Each of the three programming paradigms **removes** a capability rather than adding one — and the three removals map directly onto the three big concerns of architecture.

## Frameworks Introduced
- **Structured programming imposes discipline on direct transfer of control.** (Dijkstra, 1968 — the second paradigm adopted, though not the first invented.) Unrestrained `goto` is harmful; `if/then/else` and `do/while/until` replace it.
- **Object-oriented programming imposes discipline on indirect transfer of control.** (Dahl and Nygaard, 1966.) They noticed the ALGOL function-call stack frame could be moved to the heap, letting a function's local variables outlive the call — the function became a constructor, the locals became instance variables, the nested functions became methods. Polymorphism followed "through the disciplined use of function pointers."
- **Functional programming imposes discipline upon assignment.** (Alonzo Church, λ-calculus, 1936 — invented first, adopted last; foundation of LISP, McCarthy, 1958.) Immutability means values of symbols do not change: effectively no assignment statement. Most functional languages permit alteration, "but only under very strict discipline."

## Key Concepts
- **Every paradigm is negative.** "Each of the paradigms removes capabilities from the programmer. None of them adds new capabilities... The paradigms tell us what **not** to do, more than they tell us what to do."
- **Three removals**: `goto` statements, function pointers, and assignment.
- **Why there are probably no more** — "Is there anything left to take away? Probably not." Further evidence: all three were discovered within the ten years from **1958 to 1968**, and no new paradigm has appeared in the many decades since.

## Mental Models
- **Map paradigm to architectural concern.** Each removal serves a distinct architectural purpose:
  - **Polymorphism** (OO) → the mechanism for **crossing architectural boundaries**
  - **Functional programming** → discipline on **the location of and access to data**
  - **Structured programming** → the **algorithmic foundation of modules**
- **These align with the three big concerns of architecture**: *function*, *separation of components*, and *data management*.

## Reference Tables

| Paradigm | Discovered | By | Discipline imposed | Taken away | Architectural role |
|---|---|---|---|---|---|
| Structured | 1968 (adopted first) | Dijkstra | Direct transfer of control | `goto` | Algorithmic foundation of modules |
| Object-oriented | 1966 | Dahl & Nygaard | Indirect transfer of control | Function pointers | Crossing architectural boundaries |
| Functional | 1936 (adopted last) | Church (via LISP, McCarthy 1958) | Assignment | Assignment | Location of and access to data |

## Key Takeaways
1. Paradigms constrain; they do not empower. Each tells you what not to do.
2. The three of them remove `goto`, function pointers, and assignment — likely everything there is to remove.
3. The 1958–1968 window and the silence since is the empirical argument that the set is closed.
4. Architecture uses all three: structured for module internals, OO for boundary crossings, functional for data.

## Connects To
- **Ch 4 (Structured Programming)**: the full story of Dijkstra, proofs, and falsifiability.
- **Ch 5 (Object-Oriented Programming)**: what OO actually is — and the answer is polymorphism, i.e. dependency inversion.
- **Ch 6 (Functional Programming)**: immutability and its architectural consequences.
- **Part V (Architecture)**: where the three concerns — function, separation, data — are addressed directly.
