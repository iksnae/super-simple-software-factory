# Chapter 6: Conclusion

## Core Idea
The book's own claim about itself: "it doesn't present any algorithms or programming techniques that **haven't been used before**... **it just documents existing designs**." The value is not novelty — it is a **named, shared vocabulary** that makes design discussable, teachable, and criticizable.

"**Cataloging design patterns is important. It gives us standard names and definitions for the techniques we use. If we don't study design patterns in software, we won't be able to improve them, and it'll be harder to come up with new ones.**"

## 6.1 What to Expect from Design Patterns

### A common design vocabulary
"Studies of expert programmers... have shown that knowledge and experience **isn't organized simply around syntax but in larger conceptual structures** such as algorithms, data structures and idioms, and plans for fulfilling a particular goal."

"**Design patterns make a system seem less complex by letting you talk about it at a higher level of abstraction than that of a design notation or programming language.**"

"Once you've absorbed the design patterns in this book, **your design vocabulary will almost certainly change**. You'll find yourself saying things like, '**Let's use an Observer here**,' or, '**Let's make a Strategy out of these classes.**'"

### A documentation and learning aid
"**People learning object-oriented programming often complain that the systems they're working with use inheritance in convoluted ways and that it's difficult to follow the flow of control. In large part this is because they do not understand the design patterns in the system.**"

"**Learning these patterns will help a novice act more like an expert.**"

"Having a common vocabulary means **you don't have to describe the whole design pattern; you can just name it** and expect your reader to know it. A reader who doesn't know the patterns will have to look them up at first, **but that's still easier than reverse-engineering**."

The authors' own modest usage: "we use the patterns in **arguably naive ways**. We use them to **pick names for classes**, to **think about and teach good design**, and to **describe designs in terms of the sequence of design patterns we applied**... **But patterns are a big help even without sophisticated tools.**"

### An adjunct to existing methods
"A design method typically defines a set of notations... along with a set of rules that govern how and when to use each notation... **But they haven't been able to capture the experience of expert designers.**"

"Design patterns provide a way to describe **more of the 'why' of a design and not just record the results of your decisions**. The **Applicability, Consequences, and Implementation** sections of the design patterns help guide you in the decisions you have to make."

⚠️ **On analysis-to-design**: "Despite many claims that promise a smooth transition from object-oriented analysis to design, **in practice the transition is anything but smooth. A flexible and reusable design will contain objects that aren't in the analysis model.** The programming language and class libraries you use affect the design. **Analysis models often must be redesigned to make them reusable.** Many of the design patterns in the catalog address these issues, **which is why we call them design patterns.**"

"A full-fledged design method requires more kinds of patterns than just design patterns. There can also be **analysis patterns, user interface design patterns, or performance-tuning patterns**."

### A target for refactoring
Brian Foote's three phases of object-oriented software lifecycle:

| Phase | What happens | Dominant reuse |
|---|---|---|
| **Prototyping** | "a flurry of activity... rapid prototyping and incremental changes, until it meets an initial set of requirements and reaches **adolescence**"; "class hierarchies that **closely reflect entities in the initial problem domain**" | "**white-box reuse by inheritance**" |
| **Expansionary** | "New requirements usually add new classes and operations and perhaps whole class hierarchies" | inheritance |
| **Consolidating** (refactoring) | "tearing apart classes into **special- and general-purpose components**, moving operations up or down the class hierarchy, and **rationalizing the interfaces** of classes" | "**black-box reuse replaces white-box reuse**" |

⚠️ **Why expansion cannot continue**: "Eventually the software will become **too inflexible and arthritic** for further change. **The class hierarchies will no longer match any problem domain. Instead they'll reflect many problem domains, and classes will define many unrelated operations and instance variables.**"

"**This cycle is unavoidable.** But good designers are aware of the changes that can prompt refactorings... **A thorough requirements analysis will highlight those requirements that are likely to change during the life of the software, and a good design will be robust to them.**"

**The pattern/refactoring relationship, stated plainly**: "**Our design patterns capture many of the structures that result from refactoring. Using these patterns early in the life of a design prevents later refactorings. But even if you don't see how to apply a pattern until after you've built your system, the pattern can still show you how to change it. Design patterns thus provide targets for your refactorings.**"

## 6.2 A Brief History
- "The catalog began as a part of **Erich's Ph.D. thesis**. Roughly half of the current patterns were in his thesis." Richard joined by OOPSLA '91, John soon after, Ralph by OOPSLA '92.
- **The renames**: "'**Wrapper**' became '**Decorator**,' '**Glue**' became '**Facade**,' '**Solitaire**' became '**Singleton**,' and '**Walker**' became '**Visitor**.'"
- "**Noticing that something is a pattern is the easy part**... it's easy to spot patterns when you look at enough systems. **But finding patterns is much easier than describing them.**"
- ⚠️ The problem that reshaped the book: "**the only ones who could understand the patterns were those who had already used them.**" The fix: "We **expanded the average size of a pattern from less than 2 to more than 10 pages** by including a **detailed motivating example and sample code**. We also started examining the **trade-offs** and the various ways of implementing the pattern."
- **The hardest part**: "It's easiest to see a pattern **as a solution**... **It's harder to see when it is appropriate** — to characterize the problems it solves and the context in which it's the best solution. **In general, it's easier to see what someone is doing than to know why, and the 'why' for a pattern is the problem it solves.**"

## 6.3 The Pattern Community

### Alexander's pattern languages
**Likenesses**: "Both are based on **observing existing systems** and looking for patterns in them. Both have **templates** for describing patterns... Both rely on **natural language and lots of examples** rather than formal languages, and both give **rationales** for each pattern."

**The four differences**:
1. "People have been making buildings for **thousands of years**... **We have been making software systems for a relatively short time, and few are considered classics.**"
2. "**Alexander gives an order in which his patterns should be used; we have not.**"
3. "Alexander's patterns emphasize **the problems** they address, whereas design patterns describe **the solutions** in more detail."
4. "**Alexander claims his patterns will generate complete buildings. We do not claim that our patterns will generate complete programs.**"

"The Alexandrian point of view has helped us focus on **design trade-offs — the different 'forces' that help shape a design**. His influence made us work harder to understand the **applicability and consequences** of our patterns. **It also kept us from worrying about defining a formal representation of patterns**... at this stage **it's more important to explore the space of design patterns than to formalize it**."

⚠️ **The disclaimer**: "**From Alexander's point of view, the patterns in this book do not form a pattern language**... **our catalog is just a collection of related patterns; we can't pretend it's a pattern language.** In fact, **we think it's unlikely that there will ever be a complete pattern language for software.** ... **Design patterns are just a part of a larger pattern language for software.**"

### Patterns in software
- **OOPSLA '91 workshop** led by Bruce Anderson, "dedicated to developing a **handbook for software architects**" — which led to "**the first conference on Pattern Languages of Programs held in August 1994**."
- Predecessors in cataloging software knowledge: **Knuth's *The Art of Computer Programming*** ("one of the first attempts... though he focused on describing algorithms. **Even so, the task proved too great to finish.**"), the **Graphics Gems** series, the DoD's **Domain Specific Software Architecture** program.
- **Coplien's *Advanced C++: Programming Styles and Idioms*** — "**more C++-specific** than our design patterns, and his book contains lots of **lower-level patterns**."
- **Kent Beck** — "one of the first people in the software community to advocate Christopher Alexander's work"; a Smalltalk-patterns column in *The Smalltalk Report* from 1993.

## 6.4 An Invitation
Three instructions to the reader:
1. "**Use them and look for other patterns that fit the way you design**... Develop your vocabulary of patterns, and use it **when you talk with other people about your designs**."
2. "**Be a critical consumer**... One of the great things about patterns is that **they move design decisions out of the realm of vague intuition. They let authors be explicit about the trade-offs they make. This makes it easier to see what is wrong with their patterns and to argue with them. Take advantage of that.**"
3. "**Look for patterns you use, and write them down.** Make them a part of your documentation... **finding relevant patterns is nearly impossible if you don't have practical experience.** Feel free to write your own catalog of patterns... **but make sure someone else helps you beat them into shape!**"

## 6.5 A Parting Thought
"**The best designs will use many design patterns that dovetail and intertwine to produce a greater whole.**" Quoting Alexander:

> "It is possible to make buildings by **stringing together patterns, in a rather loose way**. A building made like this, is **an assembly of patterns. It is not dense. It is not profound.** But it is also possible to put patterns together in such a way that **many patterns overlap in the same physical space**: the building is **very dense; it has many meanings captured in a small space; and through this density, it becomes profound.**"

## Key Takeaways
1. The catalog's contribution is **naming**, not invention — and naming is what makes design improvable and teachable.
2. Patterns encode the **"why"** (Applicability, Consequences, Implementation), which is the part design methods and notations leave out.
3. Software cycles through prototyping → expansion → consolidation; expansion always ends in class hierarchies that match no domain. Refactoring is not optional.
4. Patterns are **targets for refactoring**: apply them early to prevent it, or apply them late to direct it.
5. Judge a pattern by its stated forces and trade-offs, and argue with it. That is the point of writing them down.
6. Density is the goal — many overlapping patterns in one design, not a string of them applied in sequence.

## Connects To
- **Ch 1 (Introduction)**: white-box vs. black-box reuse, the causes of redesign, and "program to an interface, not an implementation" — the refactoring cycle here is the same argument from the other end.
- **Ch 29 (Discussion of Behavioral Patterns)**: "composition at the pattern level rather than the class or object levels" is the same closing claim.
- **Ch 2 (Case Study)**: the worked example of a design accumulating many overlapping patterns.
- **glossary.md**: the book's Appendix A definitions.
