# Chapter 6: Functional Programming

## Core Idea
**Variables in functional languages do not vary** — and since every race condition, deadlock, and concurrent update problem is caused by mutable variables, immutability is an architectural concern, made practicable by segregating mutability and, at the limit, by event sourcing.

## Frameworks Introduced
- **Immutability and Architecture**: "All race conditions, deadlock conditions, and concurrent update problems are due to mutable variables. You cannot have a race condition or a concurrent update problem if no variable is ever updated. You cannot have deadlocks without mutable locks."
  - Is immutability practicable? "Affirmative, **if you have infinite storage and infinite processor speed**. Lacking those infinite resources, the answer is a bit more nuanced. Yes, immutability can be practicable, **if certain compromises are made**."
- **Segregation of Mutability**: split the application (or its services) into immutable and mutable components. The immutable ones work purely functionally; they communicate with components that permit state mutation.
  - Protect the mutable side with **transactional memory** — treating variables in memory the way a database treats records on disk, with a transaction- or retry-based scheme.
  - **The architect's directive**: "push as much processing as possible into the immutable components, and drive as much code as possible **out** of those components that must allow mutation."
- **Event Sourcing**: store the *transactions*, not the *state*. When state is needed, apply all transactions from the beginning of time.
  - Shortcuts are allowed: compute and save state every midnight, then apply only the transactions since midnight.
  - Consequences: "nothing ever gets deleted or updated from such a data store. As a consequence, our applications are **not CRUD; they are just CR**. Also, because neither updates nor deletions occur in the data store, **there cannot be any concurrent update issues**."
  - "If we have enough storage and enough processor power, we can make our applications entirely immutable — and, therefore, entirely functional."
  - The disarming closer: "If this still sounds absurd, it might help if you remembered that **this is precisely the way your source code control system works.**"

## Key Concepts
- **Mutable variable** — one that changes state during execution. In the Java squares program that's `i`, the loop control variable. The Clojure version has none: `x` is initialized, never modified.
- **Atom (Clojure)** — a variable permitted to mutate "under very disciplined conditions that are enforced by the `swap!` function." `swap!` takes the atom and a function computing the new value.
- **Compare and swap, as `swap!` implements it** — read `counter`, pass it to `inc`; when `inc` returns, lock `counter` and compare it to the value passed in. Same → store the result and release the lock. Different → release the lock and **retry from the beginning**.
- **The atom's limit** — "adequate for simple applications. Unfortunately, it cannot completely safeguard against concurrent updates and deadlocks when multiple dependent variables come into play. In those instances, more elaborate facilities can be used."
- **Receding hardware limits** — "The more memory we have, and the faster our machines are, the less we need mutable state." Processors execute billions of instructions per second; offline storage has grown so fast "that we now consider trillions of bytes to be small."

## Mental Models
- **Immutability is a concurrency strategy, not a stylistic preference.** An architect wants systems robust in the presence of multiple threads and processors; removing mutation removes the entire failure class rather than defending against it.
- **The practical question is never "pure or impure" but "where is the boundary?"** Well-structured applications are segregated into components that mutate and components that don't, with disciplines protecting the ones that do.
- **Event sourcing sounds absurd until you notice you already use it.** Version control stores the transactions, not the state — and reconstructs state on demand.

## Code Examples

The same problem, two paradigms — squares of the first 25 integers:

```java
public class Squint {
    public static void main(String args[]) {
        for (int i=0; i<25; i++)
            System.out.println(i*i);
    }
}
```
```clojure
(println (take 25 (map (fn [x] (* x x)) (range))))
```
```clojure
(println                    ;___________________ Print
  (take 25                  ;_________________ the first 25
    (map (fn [x] (* x x))   ;__ squares
      (range))))            ;___________ of Integers
```

Reading it from the inside out:
- `(range)` returns a **never-ending** list of integers starting at 0
- `map` applies the anonymous squaring function to each element, producing a never-ending list of squares
- `take` returns a new list of only the first 25
- `println` prints it

"If you find yourself terrified by the concept of never-ending lists, don't worry. Only the first 25 elements of those never-ending lists are actually created. That's because **no element of a never-ending list is evaluated until it is accessed**."

- **What it demonstrates**: the Java version's `i` is a mutable variable changing state throughout execution. The Clojure version has no mutable variable at all. That single difference is the chapter's whole architectural lever.

Disciplined mutation, when you need it:

```clojure
(def counter (atom 0))  ; initialize counter to 0
(swap! counter inc)     ; safely increment counter.
```

## Worked Example
**The bank balance, and why storing nothing but transactions is not absurd.**

A banking application maintains customer account balances, mutating them as deposits and withdrawals execute. Now invert it: **store only the transactions**. When anyone asks for a balance, add up every transaction for that account from the beginning of time. No mutable variables anywhere.

The obvious objection: transaction count grows without bound, and the processing to total them becomes intolerable. Making this work *forever* would demand infinite storage and infinite processing power.

Martin's answer is to reject the "forever" framing: "**perhaps we don't have to make the scheme work forever.** And perhaps we have enough storage and enough processing power to make the scheme work for the reasonable lifetime of the application."

From there the compromises are ordinary engineering:
- **Snapshot** — compute and save state at midnight; afterward only replay transactions since then.
- **Storage** — you need a lot, and offline storage has grown fast enough that you have a lot.
- **The structural payoff** — nothing is ever deleted or updated. The application becomes **CR instead of CRUD**, and with no updates and no deletions in the store, *concurrent update issues cannot occur*.

The final move is to point out the existence proof already on every developer's machine: source control works exactly this way.

## Reference Tables

| Approach | What's stored | Mutability | Concurrency exposure |
|---|---|---|---|
| Conventional CRUD | Current state | Full | Race conditions, concurrent updates, deadlock |
| Segregated mutability | State, in isolated components | Confined; protected by transactional memory | Limited to the mutable components |
| Event sourcing | Transactions only (CR) | None | **None** — no updates, no deletions |

## Key Takeaways
1. Functional programming's discipline is on assignment; its architectural payoff is the elimination of an entire class of concurrency bugs.
2. Full immutability requires infinite resources — so the real work is choosing where the mutable boundary sits.
3. Segregate mutable from immutable components and protect the mutable side with transactional memory.
4. Push processing *into* the immutable components and code *out of* the mutable ones.
5. Event sourcing removes mutation entirely by storing transactions instead of state; snapshots keep it affordable.
6. CR instead of CRUD means concurrent update problems are structurally impossible, not merely guarded against.

## The chapter's closing summary (Part II's conclusion)
- **Structured programming** is discipline imposed upon **direct transfer of control**.
- **Object-oriented programming** is discipline imposed upon **indirect transfer of control**.
- **Functional programming** is discipline imposed upon **variable assignment**.

"Each of these three paradigms has taken something away from us... None of them has added to our power or our capabilities. What we have learned over the last half-century is **what not to do**."

And the unwelcome fact that follows: "Software is **not** a rapidly advancing technology. The rules of software are the same today as they were in 1946... The tools have changed, and the hardware has changed, but the essence of software remains the same. Software... is composed of **sequence, selection, iteration, and indirection. Nothing more. Nothing less.**"

## Connects To
- **Ch 3 (Paradigm Overview)**: functional programming as discipline on the location of and access to data.
- **Ch 5 (OOP)**: indirection — the fourth element of the closing summary — is what polymorphism buys.
- **Ch 20 (Business Rules)** / **Ch 30 (The Database Is a Detail)**: event sourcing reframes what "the database" even holds.
- **Clean Code, Ch 13 & Appendix A**: the concurrency problems this paradigm removes rather than manages.
