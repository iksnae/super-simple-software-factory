# Appendix A: Concurrency II
*(the detailed tutorial behind Chapter 13)*

## Core Idea
The mechanics under the concurrency rules: how many execution paths one line of Java really has, why `++` is not atomic, why server-based locking beats client-based locking, the four conditions of deadlock and how to break each, and why testing threaded code needs instrumentation rather than more iterations.

## Frameworks Introduced
- **Isolate the threading policy into one class** — the client/server example's `process` function carried four responsibilities: socket connection management, client processing, threading policy, and server shutdown policy. Splitting them means a change of thread strategy touches less code and pollutes nothing else, and every other responsibility becomes testable without threads.
- **The four conditions of deadlock** — mutual exclusion, lock & wait, no preemption, circular wait. **All four must hold. Break any one and deadlock is impossible.**
- **Server-based locking over client-based locking** — five reasons, listed below.
- **Monte Carlo Testing** — make tests tunable, run them repeatedly on a test server with randomly varying tuning values, log the conditions of every failure. Start early so continuous integration runs them.
- **Instrumentation over iteration count** — IBM's **ConTest** instruments classes so non-thread-safe code fails sooner. Measured effect: failure rate went from ~1 in 10,000,000 iterations to ~1 in 30. Observed loop counts after instrumentation: 13, 23, 0, 54, 16, 14, 6, 69, 107, 49, 2.

## Key Concepts
- **Frame** — every method invocation requires one; holds the return address, parameters, and local variables. The standard call-stack technique.
- **Local variable** — anything defined in the method's scope. Every non-static method has at least `this`.
- **Operand stack** — LIFO structure where JVM instruction parameters are placed.
- **Atomic operation** — any uninterruptable operation. Assignment to a **32-bit** value is atomic per the Java Memory Model. Assignment to a **64-bit** value is *not* — the JVM spec requires two 32-bit assignments, and another thread can slip between them. (It may happen to be atomic on a particular processor; the spec doesn't promise it.)
- **`++` is not atomic** — "It is a common misconception that the ++ (pre- or post-increment) operator is atomic, and it clearly is not."
- **CAS (Compare and Swap)** — a modern-processor atomic operation. Analogous to **optimistic locking** in databases, where `synchronized` is **pessimistic locking**. Verifies the variable still holds its last known value; if so it writes, if not it retries.
- **Callable vs. Runnable** — a `Callable` looks like a `Runnable` but can return a result, "which is a common need in multithreaded solutions."
- **Future** — handy when code must run multiple independent operations and wait for them; `result.get()` blocks until the future completes.
- **Non-thread-safe classes** — `SimpleDateFormat`, database connections, containers in `java.util`, servlets.
- **Method-level safety does not compose** — "some collection classes have individual methods that are thread-safe. However, any operation that involves calling more than one method is not."
- **TANSTAAFL** — there ain't no such thing as a free lunch. Every deadlock strategy costs something: starvation, CPU burn, or reduced responsiveness.

## Reference Tables

### Execution paths through one line of Java

Formula for N sequential instructions (no loops or conditionals) across T threads:

**paths = (T × N)! / (N!^T)**

| Case | Paths |
|---|---|
| N=2, T=2 | 6 |
| N=2, T=3 | 90 |
| N=3, T=3 | 1,680 |
| `return ++lastIdUsed;` (8 byte-codes), 2 threads | **12,870** |
| same, with `lastIdUsed` as `long` (2 ops per read/write) | **2,704,156** |
| after adding `synchronized` | **2** (and N! in the general case) |

### The four deadlock conditions and how to break them

| Condition | What it means | How to break it | Cost |
|---|---|---|---|
| **Mutual Exclusion** | Resources can't be used by multiple threads at once *and* are limited in number (DB connections, files open for write, record locks, semaphores) | Use simultaneously-usable resources (`AtomicInteger`); increase resource count to ≥ competing threads; check all resources are free before seizing any | "Most resources are limited in number and don't allow simultaneous use," and the second resource's identity often depends on operating on the first |
| **Lock & Wait** | A thread holds what it has until it has everything it needs | Refuse to wait — check each resource before seizing, release everything and start over if one is busy | **Starvation** (low CPU utilization) and **livelock** (high, useless CPU utilization). "As inefficient as this strategy sounds, it's better than nothing... it can almost always be implemented if all else fails." |
| **No Preemption** | A thread can't take a resource from another | Request mechanism: ask the owner to release; if the owner is also waiting, it releases everything and starts over | Fewer startovers than breaking lock & wait, but "managing all those requests can be tricky" |
| **Circular Wait** (the deadly embrace) | T1 holds R1 and wants R2; T2 holds R2 and wants R1 | **The most common approach**: a global ordering of resources that all threads allocate in | Acquisition order may not match use order (resources locked longer than necessary); sometimes ordering is infeasible because resource 2's ID comes from operating on resource 1 |

### Client-based vs. server-based locking

| | Client-based | Server-based |
|---|---|---|
| Where the lock lives | Every client wraps calls in `synchronized` | Inside the server's API |
| Duplication | Violates DRY — every client repeats it | None |
| Risk | "All it takes is for one programmer to forget to lock properly" | Single point of correctness |
| Performance | Always paid | Can swap in a non-thread-safe server for single-threaded deployment, avoiding all overhead |
| Policy | Scattered across clients | One place |
| Shared-variable scope | Client is aware of them | Hidden in the server; fewer places to look when things break |
| When you must use it | Non-thread-safe third-party tools you can't change | Default choice |
| When you don't own the server | — | Use an ADAPTER to add locking, or better, use thread-safe collections with extended interfaces |

## Code Examples

Threading policy isolated behind one interface:

```java
public interface ClientScheduler {
    void schedule(ClientRequestProcessor requestProcessor);
}
```
```java
public class ThreadPerRequestScheduler implements ClientScheduler {
    public void schedule(final ClientRequestProcessor requestProcessor) {
        Runnable runnable = new Runnable() {
            public void run() {
                requestProcessor.process();
            }
        };
        Thread thread = new Thread(runnable);
        thread.start();
    }
}
```
```java
// switching to the Java 5 Executor framework = write one class, plug it in
public class ExecutorClientScheduler implements ClientScheduler {
    Executor executor;

    public ExecutorClientScheduler(int availableThreads) {
        executor = Executors.newFixedThreadPool(availableThreads);
    }

    public void schedule(final ClientRequestProcessor requestProcessor) {
        Runnable runnable = new Runnable() {
            public void run() {
                requestProcessor.process();
            }
        };
        executor.execute(runnable);
    }
}
```

Nonblocking update — the `AtomicInteger` rewrite:

```java
// blocking: acquires a lock even when no second thread is competing
public class ObjectWithValue {
    private int value;
    public void synchronized incrementValue() { ++value; }
    public int getValue() { return value; }
}
```
```java
// nonblocking: "the performance of this class will nearly always beat
// the previous version... the cases where it will be slower are
// virtually nonexistent."
public class ObjectWithValue {
    private AtomicInteger value = new AtomicInteger(0);
    public void incrementValue() { value.incrementAndGet(); }
    public int getValue() { return value.get(); }
}
```

CAS, logically:

```java
int variableBeingSet;

void simulateNonBlockingSet(int newValue) {
    int currentValue;
    do {
        currentValue = variableBeingSet;
    } while(currentValue != compareAndSwap(currentValue, newValue));
}

int synchronized compareAndSwap(int currentValue, int newValue) {
    if(variableBeingSet == currentValue) {
        variableBeingSet = newValue;
        return currentValue;
    }
    return variableBeingSet;
}
```

Composite operations on thread-safe collections — three fixes:

```java
// broken: each method is thread-safe, the pair is not
if(!hashTable.containsKey(someKey)) {
    hashTable.put(someKey, new SomeValue());
}
```
```java
// 1. client-based locking
synchronized(map) {
    if(!map.containsKey(key))
        map.put(key, value);
}
```
```java
// 2. server-based locking via an ADAPTER
public class WrappedHashtable<K, V> {
    private Map<K, V> map = new Hashtable<K, V>();

    public synchronized void putIfAbsent(K key, V value) {
        if (map.containsKey(key))
            map.put(key, value);
    }
}
```
```java
// 3. thread-safe collections, which provide the composite operation
ConcurrentHashMap<Integer, String> map = new ConcurrentHashMap<Integer, String>();
map.putIfAbsent(key, value);
```

Keep the critical section small:

```java
public class PageIterator {
    private PageReader reader;
    private URLIterator urls;

    public synchronized String getNextPageOrNull() {
        if (urls.hasNext())
            getPageFor(urls.next());
        else
            return null;
    }

    public String getPageFor(String url) {
        return reader.getPageFor(url);
    }
}
```
- **What it demonstrates**: the `synchronized` block holds only the critical section deep inside `PageIterator`; each thread uses its own `PageReader`. "It is always better to synchronize as little as possible as opposed to synchronizing as much as possible."

Throughput arithmetic: with 1s I/O per page and 0.5s parse, single-threaded is 1.5s × N (13 pages ≈ 19.5s). Three threads overlap process-bound parsing with I/O-bound reading, fully utilizing the processor — each one-second read overlaps two parses, giving **2 pages/second, three times the single-threaded throughput**.

## Worked Example
**Why two threads calling `++` once each can both get 94.** The method:

```java
public class IdGenerator {
    int lastIdUsed;

    public int incrementValue() {
        return ++lastIdUsed;
    }
}
```

Starting at 93, three outcomes are possible: (94, 95), (95, 94), and — surprisingly — **(94, 94) with `lastIdUsed` left at 94.** The byte-code explains it. `resetId()`'s `value = 0` compiles to three instructions:

| Mnemonic | Effect | Operand stack after |
|---|---|---|
| `ALOAD 0` | Load variable 0 — `this` | `this` |
| `ICONST_0` | Push constant 0 | `this, 0` |
| `PUTFIELD lastId` | Store 0 into the field of the object one below the top | *empty* |

These are effectively atomic: a thread can be interrupted between them, but nothing another thread does can touch the constant on the stack or the `this` reference below it. Ten threads running them have 4.38679733629e+24 possible orderings and exactly one possible outcome — because they all assign the same constant. (This holds for `long`s here too, for the same reason.)

`++lastId` compiles to eight:

| Mnemonic | Effect | Operand stack after |
|---|---|---|
| `ALOAD 0` | Load `this` | `this` |
| `DUP` | Copy top of stack | `this, this` |
| `GETFIELD lastId` | Read the field onto the stack | `this, 42` |
| `ICONST_1` | Push 1 | `this, 42, 1` |
| `IADD` | Add top two | `this, 43` |
| `DUP_X1` | Duplicate 43 before `this` | `43, this, 43` |
| `PUTFIELD value` | Store 43 into the field | `43` |
| `IRETURN` | Return top of stack | *empty* |

Now the interleaving: Thread 1 executes the first three instructions — through `GETFIELD`, so **42 is sitting on its operand stack** — and is preempted. Thread 2 runs the whole method, incrementing `lastId` to 43 and returning 43. Thread 1 resumes; its stack still holds the stale 42. It adds one, gets 43, stores it, and returns 43. **One increment is lost.**

Adding `synchronized` fixes it, and collapses 12,870 paths to 2.

"An intimate understanding of byte-code is not necessary... If you can understand this one example, it should demonstrate the possibility of multiple threads stepping on each other, which is enough knowledge." What you *do* need to know: where shared objects and values are, which code can cause concurrent read/update issues, and how to guard against them.

**The `IntegerIterator` bug that only strikes on the last iteration.**

```java
public class IntegerIterator implements Iterator<Integer> {
    private Integer nextValue = 0;

    public synchronized boolean hasNext() { return nextValue < 100000; }

    public synchronized Integer next() {
        if (nextValue == 100000)
            throw new IteratorPastEndException();
        return nextValue++;
    }

    public synchronized Integer getNextValue() { return nextValue; }
}
```

Every method is synchronized, and the class is still broken for shared use, because **the client calls two methods**. Thread 1 asks `hasNext()` → true, and is preempted. Thread 2 asks `hasNext()` → still true, calls `next()`, which returns a value and has the side effect of making `hasNext()` false. Thread 1 resumes believing `hasNext()` is true, calls `next()`, and throws.

"This is especially subtle because the only time this causes a fault is during the final iteration... This is the kind of bug that happens long after a system has been in production, and it is hard to track down."

Three options: tolerate the failure ("rather like cleaning up memory leaks by rebooting at midnight"), client-based locking, or server-based locking. The server-based fix changes the API to be multithread-aware:

```java
public class IntegerIteratorServerLocked {
    private Integer nextValue = 0;

    public synchronized Integer getNextOrNull() {
        if (nextValue < 100000)
            return nextValue++;
        else
            return null;
    }
}
```
```java
while (true) {
    Integer nextValue = iterator.getNextOrNull();
    if (next == null) break;
    // do something with nextValue
}
```

(Footnote worth keeping: "the `Iterator` interface is inherently not thread-safe. It was never designed to be used by multiple threads, so this should come as no surprise.")

**Chicago, winter of 1971 — why client-based locking blows.** A multi-terminal time-sharing system ran accounting software for Local 705 of the truckers' union: dozens of data-entry clerks 50 miles from the machine, on dedicated phone lines and 600bps half-duplex modems. About once a day a terminal would "lock up" — no pattern by terminal or time, sometimes several at once, sometimes days of nothing.

The only fix at first was a reboot, which required calling headquarters and getting every clerk to stop. If someone was mid-task for an hour, the locked terminal stayed locked.

Weeks of debugging found the mechanism: a ring-buffer counter had gotten out of sync with its pointer. The pointer said empty, the counter said full — so nothing could be displayed *and* nothing could be added. Knowing the mechanism didn't reveal the cause, so they hacked around it: a trap function, triggered by throwing a front-panel switch, that scanned for a ring buffer both empty and full and reset it. Later, when weekend shifts made walking into the computer room impractical, they added a scheduler task to check every buffer once a minute — the displays unclogged before the Local could even phone in.

Several more weeks of reading monolithic assembly listings — no search tools, no cross references — finally found it. They had done the arithmetic and knew the lock-up frequency was consistent with **a single unprotected use of the ring buffer**. Hundreds of use sites, one programmer who forgot to lock one of them.

"I learned an important lesson that cold Chicago winter of 1971. Client-based locking really blows."

**Why the obvious threading test doesn't work.** To prove `takeNextId()` broken: remember `nextId`, run two threads that each call it once, verify `nextId` went up by two, and loop until it doesn't.

```java
@Test
public void twoThreadsShouldFailEventually() throws Exception {
    final ClassWithThreadingProblem classWithThreadingProblem =
        new ClassWithThreadingProblem();

    Runnable runnable = new Runnable() {
        public void run() {
            classWithThreadingProblem.takeNextId();
        }
    };

    for (int i = 0; i < 50000; ++i) {
        int startingId = classWithThreadingProblem.lastId;
        int expectedResult = 2 + startingId;

        Thread t1 = new Thread(runnable);
        Thread t2 = new Thread(runnable);
        t1.start();
        t2.start();
        t1.join();
        t2.join();

        int endingId = classWithThreadingProblem.lastId;

        if (endingId != expectedResult)
            return;   // proved the code is broken
    }

    fail("Should have exposed a threading issue but it did not.");
}
```

Note the inverted logic: **this test passing means the production code is broken.** The test failing means it couldn't prove brokenness — either the code is fine or there weren't enough iterations.

It sets up the right conditions and still almost never fires. Detecting the problem needed **over one million** iterations, and even at a loop count of 1,000,000 across ten executions it occurred **once**. Reliable failure would need well over a hundred million — and a test tuned to fail on one machine must be retuned for another machine, OS, or JVM version.

"And this is a simple problem. If we cannot demonstrate broken code easily with this problem, how will we ever detect truly complex problems?" That is the case for Monte Carlo testing, running on every target platform under varying load, and — most effectively — instrumentation.

## Key Takeaways
1. One line of Java is not one operation: `return ++lastIdUsed;` is eight byte-codes and 12,870 two-thread paths; `synchronized` reduces that to 2.
2. 32-bit assignment is atomic; 64-bit assignment and `++` are not.
3. Prefer nonblocking atomics (`AtomicInteger`, CAS) over `synchronized` — optimistic beats pessimistic almost always, even under moderate-to-high contention.
4. Thread-safe methods do not compose into thread-safe operations; use the collection's own composite operations (`putIfAbsent`) or wrap.
5. Prefer server-based locking: less duplication, one policy, one place to look, and it can be swapped out entirely for single-threaded deployment.
6. Deadlock needs all four conditions; break the cheapest one, and global resource ordering is usually it.
7. Every deadlock strategy has a cost — starvation, CPU burn, or held-too-long resources. TANSTAAFL.
8. Isolate the threading policy in one class so it can be tuned and swapped; this is what makes experimentation possible at all.
9. Iteration counts cannot find rare interleavings. Instrument the code (ConTest) and vary conditions instead.

## Connects To
- **Ch 13 (Concurrency)**: this appendix is the tutorial that chapter points to at pages 317, 321, 323, 329, 333, and 335.
- **Ch 8 (Boundaries)**: ADAPTER for a server you don't own.
- **Ch 9 (Unit Tests)**: the inverted test above, and why FIRST's "Repeatable" matters across platforms.
- **Ch 10 (Classes)** / **Ch 11 (Systems)**: SRP applied to the four responsibilities of the server's `process` function.
- **[Lea99]**: Doug Lea, *Concurrent Programming in Java: Design Principles and Patterns* — the recommended next book.
