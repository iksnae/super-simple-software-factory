# Chapter 18: Boundary Anatomy

## Core Idea
A boundary crossing at runtime is "nothing more than a function on one side of the boundary calling a function on the other side and passing along some data" — **the whole trick is managing the source code dependencies**, and the four available boundary forms differ enormously in what a crossing costs.

## Frameworks Introduced
- **Why source code dependencies are what matter**: "when one source code module changes, other source code modules may have to be changed or recompiled, and then redeployed. **Managing and building firewalls against this change is what boundaries are all about.**"
- **The two crossing directions**:
  - **Low-level client → higher-level service**: the simplest possible crossing. "Both the runtime dependency and the compile-time dependency point in the same direction, toward the higher-level component." The `Client` calls `f()` on the `Service`, passing `Data`. **The definition of the `Data` is on the called side of the boundary.**
  - **High-level client → lower-level service**: "dynamic polymorphism is used to invert the dependency against the flow of control. The runtime dependency opposes the compile-time dependency." The high-level `Client` calls `f()` on `ServiceImpl` through the `Service` interface; **all dependencies cross the boundary from right to left toward the higher-level component**, and **the definition of the data structure is on the calling side**.
- **The universal segregation rule**, restated at every scale: "Source code dependencies point in the same direction across the boundary, and always toward the higher-level component."
  - For **local processes**: "the source code of the higher-level processes must not contain the names, or physical addresses, or registry lookup keys of lower-level processes."
  - For **services**: "The source code of higher-level services must not contain any specific physical knowledge (e.g., a URI) of any lower-level service."
  - In both cases: "the architectural goal is for lower-level processes to be plugins to higher-level processes."

## Key Concepts
- **The monolith's boundaries are real even though invisible.** "The fact that the boundaries are not visible during the deployment of a monolith does not mean that they are not present and meaningful. Even when statically linked into a single executable, the ability to **independently develop and marshal the various components for final assembly** is immensely valuable."
- **Monoliths depend on dynamic polymorphism to work at all.** "Without OO, or an equivalent form of polymorphism, architects must fall back on the dangerous practice of using pointers to functions... Most architects find prolific use of pointers to functions to be too risky, so **they are forced to abandon any kind of component partitioning**." (This is why OO became such an important paradigm.)
  - Footnote on the alternative: "Static polymorphism (e.g., generics or templates) can sometimes be a viable means of dependency management in monolithic systems, especially in languages like C++. However, **the decoupling afforded by generics cannot protect you from the need for recompilation and redeployment** the way dynamic polymorphism can."
- **Threads are not boundaries.** "Threads are not architectural boundaries or units of deployment, but rather a way to organize the schedule and order of execution. They may be wholly contained within a component, or spread across many components."
- **A local process is an uber-component.** "The process consists of lower-level components that manage their dependencies through dynamic polymorphism." Each local process may itself be a statically linked monolith or a set of dynamically linked deployment components — and several processes may share the same components, either compiled in or dynamically linked.
- **Services are location-independent by assumption.** "Services do not depend on their physical location. Two communicating services may, or may not, operate in the same physical processor or multicore. **The services assume that all communications take place over the network.**"
- **Real systems mix boundary strategies.** "A service is often just a facade for a set of interacting local processes. A service, or a local process, will almost certainly be either a monolith composed of source code components or a set of dynamically linked deployment components. This means that the boundaries in a system will often be **a mixture of local chatty boundaries and boundaries that are more concerned with latency**."

## Reference Tables

The four boundary forms, ordered by strength:

| Boundary | Physical form | Communication mechanism | Cost of crossing | Chattiness | Components delivered as |
|---|---|---|---|---|---|
| **Monolith** (source-level) | None — "a disciplined segregation of functions and data within a single processor and a single address space" | Function calls | Very fast, very inexpensive | **Can be very chatty** | Source code (deployment requires compilation and static linking) |
| **Deployment component** | DLL, jar, Ruby Gem, UNIX shared library | Function calls | Very inexpensive; possible one-time hit for dynamic linking or runtime loading | **Can still be very chatty** | Binary or equivalent deployable form |
| **Local process** | A process started from the command line or equivalent system call; same processor(s), **separate address spaces** | Sockets, mailboxes, message queues; sometimes shared memory partitions | OS calls, data marshaling and decoding, interprocess context switches — **moderately expensive** | **Should be carefully limited** | Either form |
| **Service** | A process assumed to communicate only over the network | Network | **Very slow** — "turnaround times can range from tens of milliseconds to seconds"; must deal with high latency | **Avoid chatting where possible** | Either form |

Deployment forms: a monolith is "a statically linked C or C++ project, a set of Java class files bound together into an executable jar file, a set of .NET binaries bound into a single .EXE." Deployment-level assembly "is simply the gathering of these deployable units together in some convenient form, such as a WAR file, or even just a directory."

**Deployment components are monoliths with one exception**: "The functions generally all exist in the same processor and address space. The strategies for segregating the components and managing their dependencies are the same." (Footnote: "Although static polymorphism is not an option in this case.")

## Worked Example
**Reading the two crossing diagrams — and why the data structure moves.**

The detail that repays attention in this chapter is *where the data definition lives*, because it flips between the two cases.

**Case 1 — flow of control and dependencies agree (Figure 18.1).** A low-level `Client` calls `f()` on a higher-level `Service`, passing an instance of `Data`. Control crosses left to right; the compile-time dependency also points right, toward the higher-level component. Since the caller must know the service's signature, **the `Data` definition sits on the called side** — the client imports it along with the service.

**Case 2 — flow of control and dependencies oppose (Figure 18.2).** Now a *high-level* `Client` needs a *lower-level* service. Control still crosses left to right, but a dependency pointing that way would make policy depend on detail. So the `Service` interface is introduced and `ServiceImpl` implements it. Now **all dependencies cross right to left, toward the higher-level component** — and because the high-level side owns the interface, it also owns the data contract: **the data structure definition sits on the calling side**.

That is the same move as Chapter 17's `DatabaseInterface` living in the `BusinessRules` component, expressed at the granularity of a single call. The interface *and its data structures* belong to the higher level; the implementation belongs to the lower.

**What a monolith buys even with no visible boundary.** "Even in a monolithic, statically linked executable, this kind of disciplined partitioning can greatly aid the job of developing, testing, and deploying the project. **Teams can work independently of each other on their own components without treading on each other's toes.** High-level components remain independent of lower-level details."

And the trade-off that comes with it: because crossings are just function calls, "communications across source-level decoupled boundaries **can be very chatty**." That freedom is exactly what makes a later migration to processes or services expensive — the chattiness that was free at one mode is ruinous at another. Which is why Chapter 16 recommends pushing decoupling to the point where a service *could* be formed, while leaving components in one address space.

## Key Takeaways
1. A runtime crossing is just a function call; the architectural work is entirely in the source code dependencies.
2. When control flows from low to high level, dependencies agree with it and the data definition lives on the called side.
3. When control flows from high to low level, invert with polymorphism — dependencies and the data definition both go to the calling (higher-level) side.
4. Monoliths have real boundaries; independent development and assembly is the value, not physical separation.
5. Dynamic polymorphism is what makes monolithic partitioning safe; without it, architects give up partitioning entirely.
6. Threads organize scheduling, not architecture — they are neither boundaries nor deployment units.
7. Crossing cost rises steeply: function call → dynamic-link call → IPC/context switch → network round trip. Limit chattiness accordingly.
8. Higher-level code must never name a lower-level process, address, registry key, or URI.
9. Expect a real system to mix all four forms, with chatty local boundaries inside latency-sensitive remote ones.

## Connects To
- **Ch 5 (OOP)**: dynamic polymorphism as the safe replacement for function pointers.
- **Ch 11 (DIP)**: the inversion applied in the high-to-low crossing.
- **Ch 16 (Independence)**: the three decoupling modes these boundary forms implement.
- **Ch 17 (Boundaries)**: where to draw the lines that this chapter shows you how to cross.
- **Ch 27 (Services: Great and Small)**: the cost and value of the strongest boundary, examined.
