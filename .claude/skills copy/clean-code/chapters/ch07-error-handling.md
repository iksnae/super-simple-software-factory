# Chapter 7: Error Handling
*(by Michael Feathers)*

## Core Idea
Error handling is important, but if it obscures logic it's wrong — treat it as a separate concern that can be read and reasoned about independently of the main algorithm.

## Frameworks Introduced
- **Use Exceptions Rather Than Return Codes**: error codes clutter the caller, who must check immediately after every call — and it is easy to forget.
  - When to use: any operation that can fail.
  - How: throw from the method that detects the error; catch at a level that can do something about it. This separates two tangled concerns — the algorithm and the error handling — so each can be understood alone.
- **Write Your Try-Catch-Finally Statement First**: exceptions define a scope, and `try` blocks behave like transactions — the `catch` must leave the program in a consistent state no matter what happens inside.
  - When to use: writing any code that can throw.
  - How: start with the `try-catch-finally` skeleton, driven by a test that forces the exception. Then build the rest of the logic inside the `try` by TDD, pretending nothing goes wrong.
- **Use Unchecked Exceptions**: "The debate is over."
  - Why: checked exceptions violate the **Open/Closed Principle**. A `throws` clause added at a low level cascades a signature change up through every intervening method to the catch, forcing rebuilds and redeployments of modules that care about nothing that changed. Encapsulation breaks, because every function in the path of a throw must know about a low-level exception's details.
  - Exception to the rule: checked exceptions can be useful when writing a **critical library** where callers must catch. In general application development, the dependency cost outweighs the benefit.
  - Evidence: C#, C++, Python, and Ruby have no checked exceptions, and robust software is written in all of them.
- **Provide Context with Exceptions**: a stack trace tells you where, not what was being attempted.
  - How: create informative messages naming the operation that failed and the type of failure; pass enough information for the `catch` to log usefully.
- **Define Exception Classes in Terms of a Caller's Needs**: classify by **how they will be caught**, not by source or by type.
  - How: wrap the third-party API and translate its exception zoo into one exception type. "Often a single exception class is fine for a particular area of code. The information sent with the exception can distinguish the errors. Use different classes only if there are times when you want to catch one exception and allow the other one to pass through."
- **SPECIAL CASE PATTERN** [Fowler]: create a class or configure an object that handles the special case, so client code never deals with the exceptional behavior.
- **Don't Return Null / Don't Pass Null**: returning null foists work on callers; passing null is worse.

## Key Concepts
- **Wrapping third-party APIs is a best practice** — it minimizes dependency (you can switch libraries later), makes third-party calls easy to mock in tests, and frees you from a vendor's API design choices.
- **Pushing error detection to the edges** — wrap external APIs to throw your own exceptions, define a handler above your code for aborted computation. The bulk of your code then reads as a clean unadorned algorithm.
- **The problem with null-checked code is that it has too many null checks, not too few.** One missing check sends the application spinning; a `NullPointerException` from the depths of an application has no good response.
- **Forbid passing null by default.** In most languages there is no good way to handle an accidentally-passed null: a new `InvalidArgumentException` still needs a handler with no good course of action, and assertions document the contract but still fail at runtime. Making null-in-arguments forbidden means a null there is a known signal of a defect.

## Mental Models
- **Think of a `try` block as a transaction scope.** Define the scope first; then the question "what must be true after this, no matter what went wrong?" has a place to live.
- **Ask "how will this be caught?" when designing exception types**, not "where did this come from?" Most handling work is the same regardless of cause — record the error and make sure you can proceed — so duplicate catch clauses signal that the classification is wrong.
- **When an exception is being used for a routine business alternative, it's the wrong tool.** Meals-or-per-diem is not an error; it is normal flow with two branches, and SPECIAL CASE moves it into the type system.
- **Prefer an empty collection over null.** Java's `Collections.emptyList()` returns a predefined immutable list for exactly this.

## Code Examples

Error codes vs. exceptions (Listings 7-1 / 7-2):

```java
// Listing 7-1 — the algorithm is buried in state checks
public void sendShutDown() {
    DeviceHandle handle = getHandle(DEV1);
    // Check the state of the device
    if (handle != DeviceHandle.INVALID) {
        // Save the device status to the record field
        retrieveDeviceRecord(handle);
        // If not suspended, shut down
        if (record.getStatus() != DEVICE_SUSPENDED) {
            pauseDevice(handle);
            clearDeviceWorkQueue(handle);
            closeDevice(handle);
        } else {
            logger.log("Device suspended.  Unable to shut down");
        }
    } else {
        logger.log("Invalid handle for: " + DEV1.toString());
    }
}
```
```java
// Listing 7-2 — shutdown algorithm and error handling are now separable
public void sendShutDown() {
    try {
        tryToShutDown();
    } catch (DeviceShutDownError e) {
        logger.log(e);
    }
}

private void tryToShutDown() throws DeviceShutDownError {
    DeviceHandle handle = getHandle(DEV1);
    DeviceRecord record = retrieveDeviceRecord(handle);
    pauseDevice(handle);
    clearDeviceWorkQueue(handle);
    closeDevice(handle);
}

private DeviceHandle getHandle(DeviceID id) {
    ...
    throw new DeviceShutDownError("Invalid handle for: " + id.toString());
    ...
}
```

Wrapping to collapse an exception zoo:

```java
// before — three catch clauses doing the same work
ACMEPort port = new ACMEPort(12);
try {
    port.open();
} catch (DeviceResponseException e) {
    reportPortError(e);
    logger.log("Device response exception", e);
} catch (ATM1212UnlockedException e) {
    reportPortError(e);
    logger.log("Unlock exception", e);
} catch (GMXError e) {
    reportPortError(e);
    logger.log("Device response exception");
} finally { … }
```
```java
// after — one exception type, defined by how the caller needs to catch it
LocalPort port = new LocalPort(12);
try {
    port.open();
} catch (PortDeviceFailure e) {
    reportError(e);
    logger.log(e.getMessage(), e);
} finally { … }

public class LocalPort {
    private ACMEPort innerPort;

    public LocalPort(int portNumber) {
        innerPort = new ACMEPort(portNumber);
    }

    public void open() {
        try {
            innerPort.open();
        } catch (DeviceResponseException e) {
            throw new PortDeviceFailure(e);
        } catch (ATM1212UnlockedException e) {
            throw new PortDeviceFailure(e);
        } catch (GMXError e) {
            throw new PortDeviceFailure(e);
        }
    }
}
```

Null-return elimination:

```java
// before
List<Employee> employees = getEmployees();
if (employees != null) {
    for(Employee e : employees) {
        totalPay += e.getPay();
    }
}
```
```java
// after
List<Employee> employees = getEmployees();
for(Employee e : employees) {
    totalPay += e.getPay();
}

public List<Employee> getEmployees() {
    if( .. there are no employees .. )
        return Collections.emptyList();
}
```

## Worked Example
**Building a try-catch scope test-first.** The task is to read serialized objects from a file. Start with a test that asserts the failure mode:

```java
@Test(expected = StorageException.class)
public void retrieveSectionShouldThrowOnInvalidFileName() {
    sectionStore.retrieveSection("invalid - file");
}
```

The test drives a stub that does not yet throw, so it fails:

```java
public List<RecordedGrip> retrieveSection(String sectionName) {
    // dummy return until we have a real implementation
    return new ArrayList<RecordedGrip>();
}
```

Make it pass by actually touching the file and translating the failure:

```java
public List<RecordedGrip> retrieveSection(String sectionName) {
    try {
        FileInputStream stream = new FileInputStream(sectionName)
    } catch (Exception e) {
        throw new StorageException("retrieval error", e);
    }
    return new ArrayList<RecordedGrip>();
}
```

Green, so now refactor — narrow the catch to what the constructor actually throws:

```java
public List<RecordedGrip> retrieveSection(String sectionName) {
    try {
        FileInputStream stream = new FileInputStream(sectionName);
        stream.close();
    } catch (FileNotFoundException e) {
        throw new StorageException("retrieval error', e);
    }
    return new ArrayList<RecordedGrip>();
}
```

The transaction scope now exists. All remaining logic goes between the `FileInputStream` creation and the `close`, written by ordinary TDD and free to assume nothing goes wrong. The general recipe: *write tests that force exceptions, then add handler behavior to satisfy them* — that ordering builds the `try` scope first and keeps its transactional character intact.

**The Special Case that removes a catch.** Billing rule: expensed meals count toward the total; otherwise the employee gets a per diem.

```java
// exception used for a normal business branch
try {
    MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
    m_total += expenses.getTotal();
} catch(MealExpensesNotFound e) {
    m_total += getMealPerDiem();
}
```

Change the DAO to *always* return a `MealExpenses`, returning a per-diem implementation when there are none:

```java
public class PerDiemMealExpenses implements MealExpenses {
    public int getTotal() {
        // return the per diem default
    }
}
```

```java
MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
m_total += expenses.getTotal();
```

The special case is encapsulated in an object, and the client stops branching entirely.

## Key Takeaways
1. Throw exceptions instead of returning error codes; the caller's logic stops being interleaved with checks it can forget.
2. Write the `try-catch-finally` first, driven by a test that forces the exception — the scope is a transaction boundary.
3. Prefer unchecked exceptions; checked ones violate OCP and cascade signature changes up the call stack. Reserve them for critical libraries.
4. Give exceptions enough context to name the failed operation and its failure mode.
5. Design exception classes around how callers will catch them; duplicate catch bodies mean you have the wrong taxonomy.
6. Wrap third-party APIs — for dependency isolation, mockability, and an API you actually like.
7. Use SPECIAL CASE objects to keep normal-flow alternatives out of the error path.
8. Don't return null (return an empty collection or a special case) and don't pass null (forbid it by default).

## Connects To
- **Ch 3 (Functions)**: "Prefer Exceptions to Returning Error Codes," "Extract Try/Catch Blocks," and "Error Handling Is One Thing" — the mechanics; this chapter is the strategy.
- **Ch 8 (Boundaries)**: wrapping third-party APIs is the same move applied to whole interfaces rather than just exceptions.
- **Ch 17**: [G32]/[G31] and the error-handling heuristics; also "don't return null."
- **Refactoring (Fowler)**: SPECIAL CASE pattern.
- **PPP (Martin)**: Open/Closed Principle, the basis of the checked-exception argument.
