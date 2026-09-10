# Chapter 25: Layers and Boundaries

## Core Idea
"Architectural boundaries exist **everywhere**" — far more of them than the tidy UI/business-rules/database triple suggests — so the architect must guess intelligently, then **watch** for the inflection point where implementing a boundary costs less than ignoring it.

## Frameworks Introduced
- **The API is owned by the *user*, not the implementer**: "`GameRules` communicates with `Language` through an API that **GameRules defines and Language implements**. `Language` communicates with `TextDelivery` using an API that **Language defines but TextDelivery implements**. The API is defined and owned by the user, rather than by the implementer."
  - "In each case, the API defined by those Boundary interfaces is owned by the **upstream** component."
- **Reciprocal boundary interfaces at each layer**: inside `GameRules` you find "polymorphic Boundary interfaces used by the code inside `GameRules` and implemented by the code inside the `Language` component" **and** "polymorphic Boundary interfaces used by `Language` and implemented by code inside `GameRules`." Same structure between `Language` and `TextDelivery`.
- **Data streams**: the component structure "divides the flow of data into two streams. The stream on the left is concerned with communicating with the user, and the stream on the right is concerned with data persistence. Both streams meet at the top at `GameRules`, which is the ultimate processor of the data that goes through both streams."
  - Not always two: adding networked multiplayer produces three. "As systems become more complex, the component structure may split into many such streams."
  - (Footnote: "In days long past, we would have called that top component the **Central Transform**." — Page-Jones, *Practical Guide to Structured Systems Design*, 2nd ed., 1988.)
- **The watchful-eye doctrine** — the chapter's operational answer:
  > "This is **not a one-time decision**. You don't simply decide at the start of a project which boundaries to implement and which to ignore. Rather, **you watch**. You pay attention as the system evolves. You note where boundaries may be required, and then carefully watch for the **first inkling of friction** because those boundaries don't exist. At that point, you weigh the costs of implementing those boundaries versus the cost of ignoring them — and **you review that decision frequently**. Your goal is to implement the boundaries **right at the inflection point where the cost of implementing becomes less than the cost of ignoring**."

## Key Concepts
- **Arrows point along source code dependencies, not data flow.** Martin's own footnote: "If you are confused by the direction of the arrows, remember that they point in the direction of **source code dependencies**, not in the direction of data flow."
- **Orient diagrams so all arrows point up** — which puts the highest-level policy (`GameRules`) at the top, "because `GameRules` is the component that contains the highest-level policies."
- **The honest scope disclaimer.** Martin flags it himself in a footnote: "it should be just as clear that we **would not** apply the clean architecture approach to something as trivial as this game. After all, the entire program can probably be written in 200 lines of code or less. In this case, we're using a simple program as **a proxy for a much larger system** with significant architectural boundaries."
- **The unresolved tension, stated as a tension**: "some very smart people have told us, over the years, that we should not anticipate the need for abstraction. This is the philosophy of YAGNI... **There is wisdom in this message, since over-engineering is often much worse than under-engineering.** On the other hand, when you discover that you truly do need an architectural boundary where none exists, the costs and risks can be very high to add such a boundary."
- **Retrofitting is expensive even with good practices**: boundaries ignored "are very expensive to add in later — **even in the presence of comprehensive test-suites and refactoring discipline**."

## Worked Example
**Hunt the Wumpus, and how many boundaries a 200-line game actually has.**

The 1972 text adventure: commands like `GO EAST` and `SHOOT WEST`; the computer replies with what the player sees, smells, hears, and experiences; the player hunts a Wumpus through caverns while avoiding traps and pits.

**Boundary 1 — language.** Keep the text UI but decouple it so the game can ship in different markets. "The game rules will communicate with the UI component using a **language-independent API**, and the UI will translate the API into the appropriate human language." With dependencies managed properly, "any number of UI components can reuse the same game rules. The game rules do not know, nor do they care, which human language is being used."

**Boundary 2 — persistence.** Game state might live in flash, in the cloud, or just in RAM. "In any of those cases, we don't want the game rules to know the details," so another API is created, with dependencies directed by the Dependency Rule.

At this point you have the familiar three-component picture and could stop. Martin doesn't: **"But have we really found all the significant architectural boundaries?"**

**Boundary 3 — delivery mechanism.** "Language is not the only axis of change for the UI. We also might want to vary the mechanism by which we communicate the text. For example, we might want to use a normal shell window, or text messages, or a chat application." That is a distinct axis of change, so it is a distinct potential boundary — an API isolating **language** from **communication mechanism**.

The structure that results:

| Abstract component (API) | Implemented by |
|---|---|
| `Language` | `English`, `Spanish` |
| `TextDelivery` | shell window, `SMS`, chat |
| `DataStorage` | `CloudData`, flash, RAM |

with `GameRules` on top, owning the APIs it consumes, and each layer owning the API the layer below implements.

**Reading the information flow.** "All input comes from the user through the `TextDelivery` component at the bottom left. That information rises through the `Language` component, getting translated into commands to `GameRules`. `GameRules` processes the user input and sends appropriate data down to `DataStorage` at the lower right. `GameRules` then sends output back down to `Language`, which translates the API back to the appropriate language and then delivers that language to the user through `TextDelivery`." Two streams — user communication on the left, persistence on the right — meeting at the top.

**Boundary 4 — splitting the streams.** Now look *inside* `GameRules` and it, too, divides:

- **MoveManagement** — "the mechanics of the map. They know how the caverns are connected, and which objects are located in each cavern. They know how to move the player from cavern to cavern, and how to determine the events that the player must deal with."
- **PlayerManagement** — "policies at an even higher level — policies that know the health of the player, and the cost or benefit of a particular event. These policies could cause the player to gradually lose health, or to gain health by discovering food."

The protocol between them is event-shaped: "The lower-level mechanics policy would **declare events** to this higher-level policy, such as `FoundFood` or `FellInPit`. The higher-level policy would then manage the state of the player" and eventually decide whether the player wins or loses.

Is *that* an architectural boundary? The answer depends on deployment, which is exactly the point. **Make it massively multiplayer**: `MoveManagement` runs locally on the player's computer, `PlayerManagement` runs on a server offering "a micro-service API to all the connected `MoveManagement` components." Now "**a full-fledged architectural boundary exists between `MoveManagement` and `PlayerManagement`**."

The same seam was latent in the single-player version. Deployment didn't create it; deployment made it worth paying for.

**Why the exercise matters.** "Why have I taken this absurdly simple program, which could be implemented in 200 lines of Kornshell, and extrapolated it out with all these crazy architectural boundaries? This example is intended to show that **architectural boundaries exist everywhere**. We, as architects, must be careful to recognize when they are needed. We also have to be aware that such boundaries, when fully implemented, are **expensive**."

And the closing, which refuses to resolve the tension into a rule: "**O Software Architect, you must see the future. You must guess — intelligently.** You must weigh the costs and determine where the architectural boundaries lie, and which should be fully implemented, and which should be partially implemented, and which should be ignored... **It takes a watchful eye.**"

## Key Takeaways
1. Three components (UI, rules, database) is sufficient for simple systems and wrong for most.
2. Every distinct axis of change is a candidate boundary — language, delivery mechanism, storage, and policy level are four in one toy game.
3. The consuming (upstream, higher-level) component defines and owns the API; the implementer conforms.
4. Full boundaries use reciprocal interfaces in both directions between adjacent layers.
5. Data flow splits into streams that meet at the highest-level policy; complex systems have several.
6. High-level policy itself subdivides — and a latent seam becomes a real boundary when deployment demands it.
7. YAGNI and retrofit cost are both real; neither wins by default.
8. Don't decide boundaries once. Watch for friction, re-evaluate frequently, and build at the cost-crossover point.

## Connects To
- **Ch 17 (Boundaries)**: axes of change as the criterion for where lines go.
- **Ch 22 (The Clean Architecture)**: the Dependency Rule this example obeys throughout.
- **Ch 24 (Partial Boundaries)**: the middle options available before the inflection point.
- **Ch 26 (The Main Component)**: the same Hunt the Wumpus implementation, seen from `main`.
- **Ch 27 (Services: Great and Small)**: whether the microservice boundary is the one you think it is.
- **Ch 19 (Policy and Level)**: the Central Transform, and level as distance from IO.
