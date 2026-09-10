# Chapter 12: Components

## Core Idea
Components are **the units of deployment** — the smallest entities deployable as part of a system — and the fifty-year history of getting them to work is why "component plugin architecture can be the casual default as opposed to the herculean effort it once was."

## Frameworks Introduced
- **Component = granule of deployment.** Jar files in Java, gem files in Ruby, DLLs in .Net; aggregations of binary files in compiled languages, aggregations of source files in interpreted ones. "In all languages, they are the granule of deployment."
- **The invariant across all packaging choices**: components may be linked into a single executable, aggregated into an archive (a `.war`), or independently deployed as dynamically loaded plugins. "Regardless of how they are eventually deployed, **well-designed components always retain the ability to be independently deployable and, therefore, independently developable**."
- **Relocatable binaries** — the solution to memory fragmentation. The compiler emits code a smart loader can place anywhere, "instrumented with flags that told the loader which parts of the loaded data had to be altered to be loaded at the selected address. Usually this just meant adding the starting address to any memory reference addresses."
- **External references and external definitions** — the compiler emits function names as metadata: a *reference* where a program calls a library function, a *definition* where it defines one. "Then the loader could link the external references to the external definitions once it had determined where it had loaded those definitions. **And the linking loader was born.**"
- **Murphy's law of program size**: *"Programs will grow to fill all available compile and link time."*

## Key Concepts
- **The origin statement** — early programs declared the address at which they were loaded (`*200` in the PDP-8 example, meaning address 200₈). "In those days, programs were **not relocatable**." Deciding where a program lived in memory was one of the first decisions a programmer made.
- **Libraries were kept in source, not in binary** — programmers included the library's source with their application and compiled it all as one program. (Martin's footnote: "My first employer kept several dozen decks of the subroutine library source code on a shelf. When you wrote a new program, you simply grabbed one of those decks and slapped it onto the end of your deck.")
- **Why that broke** — devices were slow, memory expensive and limited; compilers needed several passes but couldn't hold all the source resident, so they re-read it from slow devices repeatedly. "Compiling a large program could take **hours**."
- **Segmentation and fragmentation** — separating the library, compiling it once, and loading its binary at a known address (say 2000₈) worked only while the application fit between 0000₈ and 1777₈. Applications outgrew that, so programmers split them into two address segments jumping around the library. Then the library outgrew *its* bounds and needed more space near 7000₈. "This fragmentation of programs and libraries necessarily continued as computer memory grew."
- **Separating linking from loading** — by the late 1960s–70s, linking loaders reading dozens or hundreds of binary libraries off tape and slow disks "could take more than an hour just to load the program." So the slow part became a separate application — the **linker** — producing a linked relocatable that a relocating loader could load quickly.
- **The 1980s repeat** — C programs of hundreds of thousands of lines; per-module compiles fast, all-module compiles slow, linking slower still. "Turnaround had again grown to an hour or more in many cases."
- **Moore beats Murphy** — "Along came Moore, and in the late 1980s, the two battled it out. **Moore won that battle.**" Disks shrank and sped up, RAM got cheap enough to cache much of disk, clock rates went from 1 MHz to 100 MHz. By the mid-1990s link time was shrinking faster than ambition could grow programs; in many cases link time fell to **seconds**.
  - Footnote worth keeping: "Moore's law: Computer speed, memory, and density double every 18 months. This law held from the 1950s to 2000, but then, **at least for clock rates, stopped cold**."

## Mental Models
- **Every era's workflow fix was defeated by growing ambition — until hardware outran it.** "Throughout the 1960s, 1970s, and 1980s, all the changes made to speed up workflow were thwarted by programmers' ambitions, and the size of the programs they wrote. They could not seem to escape from the hour-long turnaround times."
- **The plugin architecture wasn't invented; it became affordable.** Once linking took seconds, load-time linking was feasible again — the era of Active-X, shared libraries, and the beginnings of `.jar` files. "And so the component plugin architecture was born."
- **You already ship components as plugins routinely.** Drop a custom `.jar` in a folder to mod Minecraft; include the appropriate DLLs to plug Resharper into Visual Studio.

## Worked Example
**The PDP-8 program, and what it tells you about deployment.**

```
        *200
START,  CLA
        TAD    BUFR
        JMS    GETSTR
        CLA
        TAD    BUFR
        JMS    PUTSTR
        JMP    START

BUFR,   3000
GETSTR, 0
        DCA    PTR
NXTCH,  KSF
        JMP    -1
        KRB
        DCA    I PTR
        TAD    I PTR
        AND    K177
        ISZ    PTR
        TAD    MCR
        SZA
        JMP    NXTCH
K177,   177
MCR,    -15
```

A `GETSTR` subroutine that reads a string from the keyboard into a buffer, plus a small unit test program to exercise it. The line that matters architecturally is the first: **`*200`** tells the compiler to generate code loaded at address 200₈.

"This kind of programming is a foreign concept for most programmers today. They rarely have to think about where a program is loaded in the memory of the computer." The distance between that line and a modern `.jar` is the entire history of components — and the thing that changed is not the code but **who decides where it lives**. When the programmer decides, nothing is independently deployable. When the loader decides, everything can be.

**The sequence in full:**

| Era | Mechanism | What defeated it |
|---|---|---|
| Early | Origin statement; library source concatenated to your deck | Multi-pass compiles over slow devices; hours to compile |
| Next | Library compiled separately, loaded at a fixed known address | Applications outgrew their address range; fragmentation |
| Then | **Relocatable binaries** + linking loader | Programs grew; loading dozens of libraries off tape took over an hour |
| Then | **Linker** split out from loader | 1980s C programs; compile-link turnaround back to an hour |
| Mid-1990s | Moore's law outruns program growth; link time → seconds | — |
| Today | Dynamically linked `.jar`/DLL/shared-library plugins | — |

"It has taken 50 years, but we have arrived at a place where component plugin architecture can be the casual default."

## Key Takeaways
1. A component is whatever your platform's unit of deployment is — jar, gem, DLL, shared library.
2. However you package them, well-designed components stay independently deployable and therefore independently developable.
3. Relocatability plus external references/definitions is the technical foundation everything else rests on.
4. Programs grow to fill available compile and link time; only hardware ever broke that cycle.
5. The plugin architecture became the default because linking got cheap, not because the idea was new.

## Connects To
- **Ch 5 (OOP)**: independent deployability and developability as consequences of dependency inversion.
- **Ch 13 (Component Cohesion)**: which classes belong in which component.
- **Ch 14 (Component Coupling)**: how components may depend on one another.
- **Ch 27 (Services: Great and Small)**: what changes — and what doesn't — when components become services.
