# Chapter 23: Presenters and Humble Objects

## Core Idea
The **Humble Object pattern** splits hard-to-test behavior from easy-to-test behavior — and because that split usually lands exactly on an architectural boundary, "the Clean Architecture in the last chapter was **full of** Humble Object implementations."

## Frameworks Introduced
- **The Humble Object pattern** (Meszaros, *xUnit Patterns*, p. 695): "originally identified as a way to help unit testers to separate behaviors that are hard to test from behaviors that are easy to test. The idea is very simple: **Split the behaviors into two modules or classes.** One of those modules is **humble**; it contains all the hard-to-test behaviors stripped down to their barest essence. The other module contains all the testable behaviors that were stripped out of the humble object."
- **Presenter and View** — the canonical instance. GUIs are hard to unit test "because it is very difficult to write tests that can see the screen and check that the appropriate elements are displayed there. However, **most of the behavior of a GUI is, in fact, easy to test**."
  - **The View is the humble object.** "The code in this object is kept as simple as possible. It moves data into the GUI but **does not process that data**."
  - **The Presenter is the testable object.** "Its job is to accept data from the application and format it for presentation so that the View can simply move it to the screen."
- **The completeness rule for a View Model**: "**Anything and everything that appears on the screen, and that the application has some kind of control over, is represented in the View Model as a string, or a boolean, or an enum.** Nothing is left for the View to do other than to load the data from the View Model into the screen. Thus the View is humble."
- **Testability as an architectural signal**: "It has long been known that testability is an attribute of good architectures. The Humble Object pattern is a good example, because **the separation of the behaviors into testable and non-testable parts often defines an architectural boundary**."

## Key Concepts
- **Database Gateways** (Fowler, *Patterns of Enterprise Application Architecture*, p. 466): "polymorphic interfaces that contain methods for every create, read, update, or delete operation that can be performed by the application on the database."
  - Example: needing the last names of all users who logged in yesterday means `UserGateway` gets a method named **`getLastNamesOfUsersWhoLoggedInAfter`** taking a `Date` and returning a list of last names.
  - "We do not allow SQL in the use cases layer; instead, we use gateway interfaces that have appropriate methods. Those gateways are implemented by classes in the database layer. **That implementation is the humble object.**"
  - And the asymmetry: "The interactors, in contrast, are **not** humble because they encapsulate application-specific business rules. Although they are not humble, those interactors are **testable**, because the gateways can be replaced with appropriate stubs and test-doubles."
- **"There is no such thing as an object relational mapper (ORM)."** The argument: "Objects are not data structures. At least, they are not data structures **from their users' point of view**. The users of an object cannot see the data, since it is all private. Those users see only the public methods of that object. So, from the user's point of view, an object is simply **a set of operations**."
  - "A data structure, in contrast, is a set of public data variables that have no implied behavior. ORMs would be better named '**data mappers**,' because they load data into data structures from relational database tables."
  - Placement: "In the database layer of course. Indeed, ORMs form another kind of Humble Object boundary between the gateway interfaces and the database."
- **Service Listeners** — the same pattern at a service boundary. "The application will load data into simple data structures and then pass those structures across the boundary to modules that properly format the data and send it to external services. On the input side, the service listeners will receive data from the service interface and format it into a simple data structure that can be used by the application."

## Reference Tables

Humble Object instances across the architecture:

| Boundary | Humble (hard to test) | Testable | What crosses |
|---|---|---|---|
| GUI | **View** — moves data to the screen, processes nothing | **Presenter** — formats application data for display | View Model (strings, booleans, enums) |
| Database | **Gateway implementation** — "simply uses SQL, or whatever the interface to the database is" | **Interactor** — application-specific business rules | Gateway interface method calls and results |
| ORM | **Data mapper** — loads relational rows into data structures | The gateway interfaces above it | Data structures |
| External services | **Service listener / sender** — formats and transmits | The application | Simple data structures |

What the Presenter puts into the View Model:

| Application hands the Presenter… | Presenter produces… |
|---|---|
| A `Date` object | A properly formatted string in the appropriate field |
| A `Currency` object | A string "with the appropriate decimal places and currency markers" |
| A negative currency value that should display red | "A simple boolean flag in the View model... set appropriately" |
| Every button on the screen | Its name, as a string |
| Buttons that should be greyed out | "An appropriate boolean flag" |
| Every menu item | Its name, as a string |
| Radio buttons, check boxes, text fields | Names loaded "into appropriate strings and booleans" |
| Tables of numbers | "Tables of properly formatted strings" |

## Worked Example
**Why the View ends up with nothing to do.**

Start from the testing problem: you cannot readily write a unit test that looks at a screen and confirms the right pixels are lit. But almost everything you'd *want* to assert about a GUI isn't pixels — it's decisions. Is the total formatted with two decimals and a currency marker? Is it red because it's negative? Is the Submit button disabled? Are the menu items named correctly? All of those are assertions about *values*, and values are trivially testable.

So the pattern splits along exactly that line. Every decision moves to the Presenter; only the mechanical transfer stays in the View.

Trace a single field. The application has a negative currency amount to display:

1. The application hands the Presenter a `Currency` object. It does not format it — formatting is a presentation decision.
2. The Presenter formats it into a string with the right decimal places and currency markers, and writes that string into the View Model.
3. The Presenter also evaluates "should this be red?" — it's negative, so it sets a boolean flag in the View Model.
4. The View reads the string, reads the flag, and puts the text on screen in the indicated colour. **It makes no decision whatsoever.**

Now the test writes itself: hand the Presenter a `Currency` of −42.00, assert the View Model string is `"($42.00)"` (or whatever the format demands) and the negative flag is `true`. No screen required. The only untested code is the four-line View, which contains nothing capable of being wrong in an interesting way.

**The same shape, three more times.** The chapter's point is that this is not a GUI trick:

- The **database gateway** implementation is humble in the same sense — it holds SQL and nothing else, so there is nothing to test in it; the interactor above it holds all the rules and is fully testable against a stubbed gateway.
- The **ORM** is humble between the gateway interfaces and the database, doing pure data mapping.
- The **service listener** is humble at the network edge, converting between wire formats and simple data structures.

"At each architectural boundary, we are likely to find the Humble Object pattern **lurking somewhere nearby**. The communication across that boundary will almost always involve some kind of simple data structure, and the boundary will frequently divide something that is hard to test from something that is easy to test. The use of this pattern at architectural boundaries **vastly increases the testability of the entire system**."

## Key Takeaways
1. Split hard-to-test from easy-to-test behavior; strip the humble half to its barest essence.
2. Views move data; Presenters make every formatting and enablement decision.
3. If anything on screen is under application control, it belongs in the View Model as a string, boolean, or enum.
4. Database gateways are polymorphic CRUD interfaces; their SQL implementations are the humble objects.
5. Interactors aren't humble — they're testable because gateways can be stubbed.
6. ORMs are data mappers, belong in the database layer, and form their own humble boundary.
7. Service listeners apply the same pattern at the network edge.
8. Where you find a testability seam, you have usually found an architectural boundary.

## Connects To
- **Ch 22 (The Clean Architecture)**: the Presenter/ViewModel/View sequence in the typical scenario.
- **Ch 20 (Business Rules)**: request and response models as the simple structures crossing these boundaries.
- **Ch 18 (Boundary Anatomy)**: what crosses a boundary and in which direction.
- **Ch 28 (The Test Boundary)**: testability as a first-class architectural concern.
- **Ch 30 (The Database Is a Detail)**: the gateway/ORM placement argued further.
- **Clean Code, Ch 6**: objects hide data and expose behavior; data structures expose data and have none — the distinction underlying "there is no such thing as an ORM."
