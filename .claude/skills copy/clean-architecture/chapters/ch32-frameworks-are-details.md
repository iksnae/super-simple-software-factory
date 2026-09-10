# Chapter 32: Frameworks Are Details

## Core Idea
"Frameworks are not architectures — though some try to be." The relationship between you and a framework author is **an asymmetric marriage**: you make a huge long-term commitment, and the author makes none. **Don't marry the framework.**

## Frameworks Introduced
- **Why framework authors can't have your interests at heart**: "Most framework authors offer their work for free because they want to be helpful to the community. They want to give back. This is laudable. **However, regardless of their high-minded motives, those authors do not have your best interests at heart. They can't, because they don't know you, and they don't know your problems.** Framework authors know their own problems, and the problems of their coworkers and friends. And they write their frameworks to solve **those** problems — not yours."
  - The fair concession: "your problems will likely overlap with those other problems quite a bit. If this were not the case, frameworks would not be so popular. To the extent that such overlap exists, frameworks can be very useful indeed."
- **The Asymmetric Marriage**: "You must make a huge commitment to the framework, but **the framework author makes no commitment to you whatsoever**."
  - What the documentation asks of you: "the author, and other users of that framework, advise you on how to integrate your software with the framework. Typically, this means **wrapping your architecture around that framework**. The author recommends that you **derive from the framework's base classes**, and import the framework's facilities into your business objects. **The author urges you to couple your application to the framework as tightly as possible.**"
  - Why that's rational for the author and not for you: "**For the framework author, coupling to his or her own framework is not a risk. The author wants to couple to that framework, because the author has absolute control over that framework.** What's more, the author wants you to couple to the framework, because **once coupled in this way, it is very hard to break away**. Nothing feels more validating to a framework author than a bunch of users willing to inextricably derive from the author's base classes."
  - The summary: "In effect, the author is asking you to **marry** the framework... And yet, under no circumstances will the author make a corresponding commitment to you. It's a **one-directional marriage**. You take on all the risk and burden; the framework author takes on nothing at all."
- **The Solution — use it, don't couple to it**:
  - "Oh, you can use the framework — just **don't couple to it. Keep it at arm's length.** Treat the framework as a detail that belongs in one of the outer circles of the architecture. **Don't let it into the inner circles.**"
  - "**If the framework wants you to derive your business objects from its base classes, say no!** Derive **proxies** instead, and keep those proxies in components that are **plugins** to your business rules."
  - "Don't let frameworks into your core code. Instead, integrate them into components that plug in to your core code, **following the Dependency Rule**."

## Key Concepts
- **The four risks, in full**:
  1. "**The architecture of the framework is often not very clean.** Frameworks tend to violate the Dependency Rule. They ask you to inherit their code into your business objects — **your Entities!** They want their framework coupled into that innermost circle. Once in, that framework isn't coming back out. The wedding ring is on your finger; and it's going to stay there."
  2. "The framework may help you with some early features of your application. However, **as your product matures, it may outgrow the facilities of the framework**. If you've put on that wedding ring, you'll find the framework fighting you more and more as time passes."
  3. "**The framework may evolve in a direction that you don't find helpful.** You may be stuck upgrading to new versions that don't help you. You may even find old features, which you made use of, **disappearing or changing** in ways that are difficult for you to keep up with."
  4. "**A new and better framework may come along** that you wish you could switch to."
- **Some marriages are unavoidable — but they are still decisions.** "If you are using C++, for example, you will likely have to marry **STL** — it's hard to avoid. If you are using Java, you will almost certainly have to marry the **standard library**. That's normal — **but it should still be a decision.** You must understand that when you marry a framework to your application, **you will be stuck with that framework for the rest of the life cycle of that application**. For better or for worse, in sickness and in health, for richer, for poorer, forsaking all others, you will be using that framework. **This is not a commitment to be entered into lightly.**"
- **Date before you marry**: "When faced with a framework, try not to marry it right away. See if there aren't ways to **date it for a while** before you take the plunge. Keep the framework behind an architectural boundary if at all possible, for as long as possible. **Perhaps you can find a way to get the milk without buying the cow.**"

## Worked Example
**Spring, done wrong and done right.**

The chapter's one concrete example is deliberately chosen from a framework Martin approves of, which makes the point sharper — the problem isn't bad frameworks, it's coupling.

**The framework is good.** "Maybe you like Spring. **Spring is a good dependency injection framework.** Maybe you use Spring to auto-wire your dependencies. **That's fine**..."

**The coupling is not.** "...but you should not sprinkle `@autowired` annotations **all throughout your business objects**. **Your business objects should not know about Spring.**"

**The fix, in one sentence.** "Instead, you can use Spring to inject dependencies into your **`Main` component**. It's OK for `Main` to know about Spring since **`Main` is the dirtiest, lowest-level component in the architecture**."

Notice what this costs and what it buys. It costs you the convenience of annotating business objects directly. It buys you: business objects that compile and run with no Spring on the classpath; unit tests with no container; and a migration path to a different DI framework — or none at all — that touches exactly one component.

**The general form of the escape.** When a framework demands inheritance from its base classes, the answer is a **proxy**: a class in an outer, plugin component that derives from the framework's base class and delegates to your untouched business object. Your Entity never names the framework; the framework never reaches the innermost circle; and the Dependency Rule holds.

That is the same shape as every other detail in the book — the database behind a gateway, the web behind a use-case boundary, the hardware behind a HAL. The framework goes on the outside, with a thin adapter facing inward.

## Reference Tables

| Party | Commitment | Risk |
|---|---|---|
| **You** | Huge, long-term; often architectural | All of it |
| **Framework author** | None whatsoever | None — they control the framework |

| Framework demand | Correct response |
|---|---|
| "Derive your business objects from our base classes" | Say no. Derive **proxies** in a plugin component |
| "Annotate your domain objects" (`@autowired` etc.) | Confine the framework to `Main`; distribute dependencies normally from there |
| "Import our facilities into your entities" | Keep the framework in an outer circle; integrate via components that plug into your core |
| An unavoidable framework (STL, the Java standard library) | Marry it — **as a conscious decision**, understanding it is for the application's whole life cycle |

## Key Takeaways
1. Frameworks are not architectures, and their authors — however well-intentioned — solved their problems, not yours.
2. The relationship is asymmetric: your commitment is total, theirs is zero, and tight coupling serves them, not you.
3. Four risks: unclean framework architecture, outgrowing it, unwanted evolution, and a better alternative arriving.
4. Frameworks tend to violate the Dependency Rule by design — they want to be inside your Entities.
5. Use frameworks; don't couple to them. Keep them in outer circles as plugins behind an architectural boundary.
6. When a framework demands inheritance, derive proxies in plugin components instead.
7. Confine DI frameworks to `Main`; business objects should not know they exist.
8. Some frameworks must be married — make it an explicit, informed decision, not a default.
9. Date before you marry: keep the option open for as long as possible.

## Connects To
- **Ch 21 (Screaming Architecture)**: "frameworks are tools to be used, not architectures to be conformed to"; view each one with a jaded eye.
- **Ch 26 (The Main Component)**: `Main` as the designated home for the DI framework and all other dirt.
- **Ch 22 (The Clean Architecture)**: the Dependency Rule frameworks routinely violate.
- **Ch 10 (ISP)**: the S → F → D problem — a framework dragging its own dependencies into your system.
- **Ch 30–31**: the database and the web, the other two details.
- **Clean Code, Ch 8**: wrapping third-party APIs, and learning tests.
