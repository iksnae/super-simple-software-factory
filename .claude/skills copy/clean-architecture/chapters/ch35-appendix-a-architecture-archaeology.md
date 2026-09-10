# Appendix A: Architecture Archaeology

## Core Idea
A 45-year autobiographical tour "to unearth the principles of good architecture" — the projects that produced the book's rules, including the ones where Martin got it wrong and learned the rule by paying for it.

## Frameworks Introduced
- **The reusable-framework law** — the appendix's most quoted lesson, learned the expensive way at ETS:
  > "**You can't make a reusable framework until you first make a usable framework. Reusable frameworks require that you build them in concert with several reusing applications.**"
- **Great architectures can cause great failures** — learned at Rational, on ROSE:
  > "Great architectures sometimes lead to great failures. **Architecture must be flexible enough to adapt to the size of the problem.** Architecting for the enterprise, when all you really need is a cute little desktop tool, is a recipe for failure."
- **Dependency direction decides survival.** ROSE "was composed of layers, with a strictly enforced dependency rule. **That rule is not the rule that I have described in this book.** We did not point our dependencies toward high-level policies. Rather, we pointed our dependencies in the more traditional direction of flow control. The GUI pointed at the representation, which pointed at the manipulation rules, which pointed at the database. **In the end, it was this failure to direct our dependencies toward policy that aided the eventual demise of the product.**"

## Key Concepts
- **Where SOLID came from.** Two years of Usenet/Netnews debates about C++ and OO, conducted to relieve the frustrations of a failing startup: "For two years, I relieved the frustrations that were building at work by debating with hundreds of folks on Usenet about the best language features and the best principles of design. After a while, I even started making a certain amount of sense. **It was in one of those debates that the foundations of the SOLID principles were laid.**"
- **The books that formed the view**: Stroustrup's *The C++ Programming Language* and *The ARM*; Rebecca Wirfs-Brock's *Designing Object Oriented Software* (responsibility-driven design); Peter Coad's *OOA/OOD/OOP*; Adele Goldberg's *Smalltalk-80*; Coplien's *Advanced C++ Programming Styles and Idioms*; and "perhaps most significantly of all, **Object Oriented Design with Applications by Grady Booch**."
- **Where "Uncle Bob" came from.** Billy Vogel, an engineer at Clear Communications who nicknamed everyone, probably referencing J. R. "Bob" Dobbs. Martin tolerated it, then found he missed it after leaving — "So I made the mistake of putting 'Uncle Bob' in my email and Netnews signatures. And the name stuck. **Eventually I realized that it was a pretty good brand.**"
- **Object-oriented databases as a cautionary fad.** The idealistic promise: "The database stores objects, not tables. The database was supposed to look like RAM. When you accessed an object, it simply appeared in memory... **It was like magic.**" The delivery: "That database was probably our biggest practical mistake. We wanted the magic, but what we got was **a big, slow, intrusive, expensive third-party framework that made our lives hell** by impeding our progress on just about every level."
- **Over-architecture as the *bigger* mistake.** "The biggest mistake, in fact, was **over-architecture**. There were many more layers than I have described here, and each had its own brand of communications overhead. This served to significantly reduce the productivity of the team." The outcome: "after many man-years of work, immense struggles, and two tepid releases, **the whole tool was scrapped and replaced with a cute little application written by a small team in Wisconsin**."

## Worked Example
**Clear Communications: the startup with no time for architecture.**

1988, ex-Teradyne employees; the product monitors T1 line quality, "a huge monitor with a map of the United States crisscrossed by T1 lines flashing red if they were degrading." Sun Sparcstations, X-Windows, C, UNIX.

Martin's account of the working conditions and the self-assessment are worth quoting exactly:

> "This was a startup. We worked 70 to 80 hours per week. We had the vision. We had the motivation. We had the will. We had the energy. We had the expertise. We had equity. We had dreams of being millionaires. **We were full of shit.**
>
> The C code poured out of every orifice of our bodies. We slammed it here, and shoved it there. We constructed huge castles in the air... We wrote a full seven-layer ISO communications stack from scratch — right down to the data link layer.
>
> We wrote GUI code. GOOEY CODE! OMG! We wrote GOOOOOEY code. I personally wrote **a 3000-line C function named `gi()`**; its name stood for Graphic Interpreter. It was a masterpiece of goo...
>
> **Architecture? Are you joking? This was a startup. We didn't have time for architecture. Just code, dammit! Code for your very lives!**
>
> So we coded. And we coded. And we coded. But, after three years, **what we failed to do was sell**."

The failure was commercial rather than technical — "the market was not particularly interested in our grand vision" — which is precisely why the story matters: the heroic pace bought nothing that the market wanted, and left behind code nobody could adapt when it turned out the vision needed changing.

**ETS and the Architects Registry Exam: the framework that had to be built twice.**

The contract: NCARB's registration exam for building architects, automated. ETS decomposed it into **18 test vignettes**, each needing a CAD-like GUI application plus a separate scoring application — **36 applications** in total.

The observation was correct: "The 18 GUI apps all used similar gestures and mechanisms. The 18 scoring applications all used the same mathematical techniques." So Martin and Jim Newkirk proposed a reusable framework, selling it to ETS on the promise "that we'd spend a long time working on the first application, but then **the rest would just pop out every few weeks**."

Martin flags the reader's reaction in advance: "At this point you should be face-palming or banging your head on this book. Those of you who are old enough may remember the '**reuse**' promise of OO. We were all convinced, back then, that if you just wrote good clean object-oriented C++ code, you would just naturally produce lots and lots of reusable code."

**Attempt 1.** Two people, full time, one year, building *Vignette Grande* — the most complicated of the batch — with an eye toward reuse. Result: **45,000 lines of framework and 6,000 lines of application.** Delivered; ETS contracted for the other 17 "post-haste"; three more developers recruited.

"But something went wrong. **We found that the reusable framework we had created was not particularly reusable.** It did not fit well into the new applications being written. **There were subtle frictions that just didn't work.**"

They went back to ETS to say the 45,000-line framework needed rewriting. "I don't need to tell you that ETS was not particularly happy with this news."

**Attempt 2.** Set the old framework aside and write **four vignettes simultaneously**, "borrow[ing] ideas and code from the old framework but rework[ing] them so that they fit into all four **without modification**." Another year. Result: another 45,000-line framework, plus four vignettes of 3,000–6,000 lines each.

And this time the dependency structure was right, though they didn't have the vocabulary yet:

- "the relationship between the GUI applications and the framework **followed the Dependency Rule**. The vignettes were **plugins** to the framework. All the high-level GUI policy was in the framework. The vignette code was just glue."
- Scoring inverted it: "The high-level scoring policy was in the **vignette**. The scoring framework plugged into the scoring vignette."
- "Of course, both of these applications were **statically linked C++** applications, so the notion of plugin was nowhere in our minds. **And yet, the way the dependencies ran was consistent with the Dependency Rule.**"

**The outcome.** "Having delivered those four applications, we began on the next four. And this time **they started popping out the back end every few weeks, just as we had predicted**. The delay had cost us nearly a year on our schedule, so we hired another programmer to speed the process along. We met our dates and our commitments. Our customer was happy. We were happy. Life was good."

The difference between the two attempts is exactly one variable: attempt 1 generalized from **one** application, attempt 2 generalized from **four simultaneously**. Hence the law.

**Hardware as context (the Union Accounting System, late 1960s).** A GE Datanet 30 for Teamsters Local 705: discrete transistors, some vacuum tubes, **16K × 18 bits** of core with a ~7 microsecond cycle time ("today we would say that it had a clock rate of **142 kHz**"), 7-track tape drives, and a ~20 MB disk with **36-inch, 3/8-inch-thick platters**, each with its own pneumatically actuated seek arm, seek time about half a second to a second. "When this beast was turned on, it sounded like a jet engine. The floor would rumble and shake until it got up to speed."

The detail that explains a generation's habits: "These computers did not come with operating systems. They didn't even come with file systems. **What you got was an assembler.** If you needed to store data on the disk, you stored data on the disk. Not in a file. Not in a directory. You figured out which track, platter, and sector to put the data into, and then you operated the disk to put the data there. **Yes, that means we wrote our own disk driver.**"

(Two footnotes worth keeping: the machine shipped in a semi-trailer alongside a household of furniture, hit a bridge at speed, and "the computer was fine, but it slid forward and crushed the furniture into splinters." And on the disk: metal shavings dropping from the cabinet led to a maintenance visit and "stories about how these disks, if not repaired, could tear loose from their moorings, plow through concrete block walls, and embed themselves into cars in the parking lot.")

## Reference Tables

The projects, and what each taught:

| Project | Era | Lesson |
|---|---|---|
| **Union Accounting System** (GE Datanet 30) | Late 1960s | No OS, no file system — you wrote the disk driver; the origin of the physical-addressing story in Ch 15 |
| **Laser Trim / Aluminum Die-Cast Monitoring** | 1970s | Early embedded and monitoring work |
| **4-TEL / SAC / BOSS / pCCU / DLU/DRU / VRS** | 1970s–80s | Includes "The Grand Redesign in the Sky" and "The Schedule Trap" |
| **Clear Communications** | 1988–1990 | Heroics without architecture; a 3000-line `gi()`; three years, no sales |
| **Netnews debates** | 1988–1990 | **The foundations of SOLID** |
| **ROSE at Rational** | 1990–1991 | Real layered architecture — but dependencies pointed with control flow, not toward policy. Over-architecture and an OO database killed it |
| **ETS / Architects Registry Exam** | Early 1990s | You can't build a reusable framework from one application; the Dependency Rule discovered in practice |

## Key Takeaways
1. A reusable framework must be grown alongside **several** reusing applications; generalizing from one produces "subtle frictions."
2. Architecture must be sized to the problem — enterprise architecture on a desktop tool is a recipe for failure.
3. Layers alone are not enough; if dependencies follow control flow instead of pointing at policy, the product still dies.
4. Over-architecture has a measurable cost: every extra layer adds communications overhead and reduces productivity.
5. "No time for architecture" startups can code for three years and fail on the market, not the code.
6. Chasing a technology because it is magical (OO databases) buys "a big, slow, intrusive, expensive third-party framework."
7. The Dependency Rule can be obeyed without plugins, dynamic linking, or even the vocabulary for it — in statically linked C++.
8. SOLID came out of two years of public argument, not out of a project plan.

## Connects To
- **Ch 1 (What Is Design and Architecture?)**: the Grand Redesign in the Sky, seen here in the wild.
- **Ch 15 (What Is Architecture?)**: the physical-addressing and device-independence stories come from these projects.
- **Ch 22 (The Clean Architecture)**: the Dependency Rule that ROSE lacked and ETS accidentally obeyed.
- **Ch 30 (The Database Is a Detail)**: the T1-monitoring RDBMS anecdote is from Clear Communications.
- **Ch 32 (Frameworks Are Details)**: the OO database as the asymmetric marriage, before Martin had a name for it.
- **Part III (Design Principles)**: SOLID, whose origin story is here.
