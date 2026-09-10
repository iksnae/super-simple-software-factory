# Chapter 13: Concurrency
*(by Brett L. Schuchert)*

> "Objects are abstractions of processing. Threads are abstractions of schedule." — James O. Coplien

## Core Idea
Concurrency is a decoupling strategy — it separates *what* gets done from *when* it gets done — and the only way to get it right is to treat concurrency as its own responsibility, isolate it behind SRP, and test it aggressively in configurations designed to make it fail.

## Frameworks Introduced
- **Concurrency Defense Principles** — the chapter's core sequence:
  - **Single Responsibility Principle**: concurrency design is complex enough to be a reason to change in its own right, so it deserves separation. Concurrency code has its own lifecycle of development, change, and tuning; its own (harder) challenges; and enough failure modes without the burden of surrounding application code.
    - *Recommendation: Keep your concurrency-related code separate from other code.*
  - **Corollary: Limit the Scope of Data** — the more places shared data can be updated, the more likely you forget to protect one (breaking everything that touches it), duplicate the guarding effort (violating DRY), and struggle to locate failures.
    - *Recommendation: Take data encapsulation to heart; severely limit the access of any data that may be shared.*
  - **Corollary: Use Copies of Data** — avoid sharing in the first place. Copy objects and treat them read-only, or collect results in per-thread copies and merge in a single thread. On the cost objection: "if using copies of objects allows the code to avoid synchronizing, the savings in avoiding the intrinsic lock will likely make up for the additional creation and garbage collection overhead."
  - **Corollary: Threads Should Be as Independent as Possible** — each thread in its own world, all required data from an unshared source, stored in local variables, so it behaves as if it were the only thread.
    - *Recommendation: Attempt to partition data into independent subsets that can be operated on by independent threads, possibly in different processors.*
- **Know Your Library**: use thread-safe collections, the executor framework for unrelated tasks, nonblocking solutions where possible — and know that several library classes are *not* thread safe.
- **Know Your Execution Models**: Producer-Consumer, Readers-Writers, Dining Philosophers. "Most concurrent problems you will likely encounter will be some variation of these three problems."
- **Beware Dependencies Between Synchronized Methods**: `synchronized` protects an individual method; more than one synchronized method on the same shared class may leave the system incorrect.
  - *Recommendation: Avoid using more than one method on a shared object.* When you must, use one of three corrections — **Client-Based Locking**, **Server-Based Locking**, or **Adapted Server**.
- **Keep Synchronized Sections Small**: locks create delays and overhead, so minimize the number of critical sections — but "extending synchronization beyond the minimal critical section increases contention and degrades performance." Naive programmers enlarge critical sections to reduce their count; that is the wrong trade.
- **Jiggling**: instrument code with calls that perturb execution order so latent failures surface early and often.

## Key Concepts
- **Bound Resources** — resources of fixed size or number used concurrently (database connections, fixed-size read/write buffers).
- **Mutual Exclusion** — only one thread accesses shared data or a shared resource at a time.
- **Starvation** — a thread or group prohibited from proceeding for an excessively long time or forever (e.g. always admitting fast threads first starves long-running ones).
- **Deadlock** — two or more threads each holding a resource the other needs; neither can finish.
- **Livelock** — threads in lockstep, each finding another "in the way," making no progress due to resonance.
- **Critical section** — any code that must be protected from simultaneous use for the program to be correct.
- **Correct shutdown is hard.** A parent waiting on children never finishes if one child deadlocks. A producer that receives the shutdown signal and exits quickly can leave its consumer blocked waiting for a message that will never come — unable even to receive the shutdown signal.
  - *Recommendation: Think about shut-down early and get it working early. It's going to take longer than you expect.*

## Mental Models
- **Concurrency is structural before it is fast.** Decoupling what from when makes the application look like many little collaborating computers rather than one big main loop.
- **Do not assume the container handles it.** The decoupling a servlet container provides "is far less than perfect"; you had better know what your container is doing and how to guard against concurrent update and deadlock.
- **Assume one-offs do not exist.** Threading bugs may appear once in a thousand or a million executions and get written off as cosmic rays or hardware glitches. "The longer these 'one-offs' are ignored, the more code is built on top of a potentially faulty approach."
- **Separate thread-aware from thread-ignorant code, and the testing problem becomes tractable.** POJOs that know nothing of threading can be tested outside the threaded environment, and they give you obvious places to instrument.
- **Testability from the Three Laws of TDD implies pluggability**, which is exactly the support you need to run threaded code across many configurations.

## Reference Tables

Myths, and the balanced version:

| Myth | Reality |
|---|---|
| Concurrency always improves performance | Only when there is a lot of wait time to share between threads or processors — "neither situation is trivial" |
| Design does not change when writing concurrent programs | A concurrent algorithm's design can be remarkably different; decoupling what from when has a huge effect on structure |
| Understanding concurrency isn't important inside a Web/EJB container | You must know what the container does and guard against concurrent update and deadlock |

| Balanced statement |
|---|
| Concurrency incurs overhead, in performance *and* in code written |
| Correct concurrency is complex, even for simple problems |
| Concurrency bugs aren't usually repeatable, so they get ignored as one-offs instead of the true defects they are |
| Concurrency often requires a fundamental change in design strategy |

Java 5 library classes worth knowing:

| Class | What it is |
|---|---|
| `ConcurrentHashMap` | Performs better than `HashMap` in nearly all situations; allows simultaneous concurrent reads and writes; supports composite operations that are otherwise not thread safe. **If Java 5 is the deployment environment, start here.** |
| `ReentrantLock` | A lock that can be acquired in one method and released in another |
| `Semaphore` | The classic semaphore — a lock with a count |
| `CountDownLatch` | A lock that waits for a number of events before releasing all waiting threads, giving them a fair chance to start at about the same time |

*Recommendation: become familiar with `java.util.concurrent`, `java.util.concurrent.atomic`, `java.util.concurrent.locks`.*

The three classic execution models:

| Model | Shape | Central difficulty |
|---|---|---|
| **Producer-Consumer** | Producers place work in a bound queue; consumers take it out; both signal each other | Producers wait for free space, consumers wait for content; the signalling is where it breaks |
| **Readers-Writers** | A shared resource read often, written occasionally | Balancing throughput against staleness and starvation. Make writers wait for zero readers → continuous readers starve the writers. Prioritize frequent writers → throughput suffers |
| **Dining Philosophers** | Threads competing for adjacent resources (forks), each needing two to proceed | Deadlock, livelock, throughput and efficiency degradation — the shape of many enterprise resource-contention problems |

Testing recommendations, in full:

| Recommendation | Why |
|---|---|
| Treat spurious failures as candidate threading issues | Threaded code makes things fail that "simply cannot fail" |
| Get your nonthreaded code working first | Never chase threading and non-threading bugs at once |
| Make your threaded code pluggable | Run with one thread, several, varied; real collaborators or test doubles; fast, slow, or variable doubles; configurable iteration counts |
| Make your threaded code tunable | Right thread count needs trial and error; consider changing it at runtime or self-tuning on throughput and utilization |
| Run with more threads than processors | Encourages task swapping, which exposes missing critical sections and deadlocks |
| Run on different platforms | Different OSes have different threading policies; the JVM does not even guarantee preemptive threading |
| Instrument your code to force failures | Only a few of thousands of possible pathways fail, so the probability of hitting one naturally is startlingly low |

## Code Examples

The trivial class that isn't (three outcomes from one line):

```java
public class X {
    private int lastIdUsed;

    public int getNextId() {
        return ++lastIdUsed;
    }
}
```
- **What it demonstrates**: with `lastIdUsed` at 42 and two threads calling `getNextId()`, you can get (43, 44), (44, 43), or — the surprising third result — **(43, 43)** with `lastIdUsed` left at 43. Working from the generated byte-code alone there are **12,870 possible execution paths** for two threads through that one line. Change `lastIdUsed` from `int` to `long` and it becomes **2,704,156**. Most produce valid results. Some don't.

Hand-coded jiggling:

```java
public synchronized String nextUrlOrNull() {
    if(hasNext()) {
        String url = urlGenerator.next();
        Thread.yield();  // inserted for testing.
        updateHasNext();
        return url;
    }
    return null;
}
```
- **What it demonstrates**: "If the code does break, it was not because you added a call to `yield()`. Rather, your code was broken and this simply made the failure evident."

Automated jiggling:

```java
public class ThreadJigglePoint {
    public static void jiggle() {
    }
}
```
```java
public synchronized String nextUrlOrNull() {
    if(hasNext()) {
        ThreadJiglePoint.jiggle();
        String url = urlGenerator.next();
        ThreadJiglePoint.jiggle();
        updateHasNext();
        ThreadJiglePoint.jiggle();
        return url;
    }
    return null;
}
```
- **What it demonstrates**: two implementations of `ThreadJigglePoint` — one that does nothing (production) and one that randomly chooses between sleeping, yielding, or falling through (test). Run the tests a thousand times with random jiggling and you may root out flaws; if they pass, "at least you can say you've done due diligence." IBM's **ConTest** does this with considerably more sophistication.

## Worked Example
**Why hand-instrumentation doesn't scale, and what to do instead.** The hand-coded `Thread.yield()` above works, and for a particularly thorny piece of code it may be exactly right. But the chapter lists its problems plainly:

- You have to manually find appropriate places to do this.
- How do you know where to put the call, and what kind of call to use?
- Leaving such code in production unnecessarily slows it down.
- It's a shotgun approach — "you may or may not find flaws. Indeed, the odds aren't with you."

What's actually needed is instrumentation active during testing but not in production, with configurations easily mixed between runs so that errors surface *in the aggregate* rather than in any single lucky run.

And here the design principle and the testing problem meet: "Clearly, if we divide our system up into POJOs that know nothing of threading and classes that control the threading, it will be easier to find appropriate places to instrument the code. Moreover, we could create many different test jigs that invoke the POJOs under different regimes of calls to `sleep`, `yield`, and so on."

That is the chapter's argument in miniature. Applying SRP to concurrency isn't a stylistic preference — it is what makes the code instrumentable, testable across configurations, and therefore debuggable at all. The `ThreadJigglePoint` pair (no-op for production, randomized for test) is the mechanism that falls out of having made that separation.

## Key Takeaways
1. Concurrency decouples what from when — adopt it for structure and throughput, knowing it costs performance overhead and additional code.
2. Apply SRP: keep concurrency-related code separate, small, and focused; make everything else a thread-ignorant POJO.
3. Severely limit shared data scope; prefer copies; make threads as independent as possible.
4. Learn `java.util.concurrent` and the three classic models — most real problems are variations of Producer-Consumer, Readers-Writers, or Dining Philosophers.
5. Avoid multiple synchronized methods on a shared object; if unavoidable, use client-based, server-based, or adapted-server locking.
6. Keep critical sections minimal — enlarging them to reduce their count increases contention.
7. Plan graceful shutdown early; it will take longer than you expect.
8. Never write off a spurious failure as a one-off.
9. Get nonthreaded code working first, then run threaded code pluggable, tunable, over-subscribed, on every target platform, with jiggling — as long as possible before production.

## Connects To
- **Appendix A (Concurrency II)**: the detailed tutorial — client/server example (p. 317), possible paths of execution (p. 321), digging deeper (p. 323), dependencies between methods (p. 329), increasing throughput (p. 333), deadlock (p. 335).
- **Ch 9 (Unit Tests)**: the Three Laws of TDD, and the testability that yields pluggability.
- **Ch 10 (Classes)** / **Ch 11 (Systems)**: SRP and POJO separation are the same moves at other scales.
- **Ch 4 (Comments)**: the `testConcurrentAddWidgets` race-condition comment is an "explanation of intent" example.
- **[Lea99]**: Doug Lea, *Concurrent Programming in Java*. **[PPP]**: SRP. **[PRAG]**: DRY.
