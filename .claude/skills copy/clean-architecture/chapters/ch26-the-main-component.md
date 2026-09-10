# Chapter 26: The Main Component

## Core Idea
`Main` is "the **ultimate detail** — the lowest-level policy," the dirtiest component in the system, whose job is to create everything and then hand control to the high-level abstractions — and treating it as a **plugin** makes configuration management straightforward.

## Frameworks Introduced
- **What Main is**: "In every system, there is at least one component that creates, coordinates, and oversees the others."
  - "It is the initial entry point of the system. **Nothing, other than the operating system, depends on it.** Its job is to create all the Factories, Strategies, and other global facilities, and then hand control over to the high-level abstract portions of the system."
- **Where the DI framework goes, and where it stops**: "It is in this `Main` component that dependencies should be injected by a Dependency Injection framework. **Once they are injected into `Main`, `Main` should distribute those dependencies normally, without using the framework.**"
- **Main as a plugin**: "Think of `Main` as a plugin to the application — a plugin that sets up the initial conditions and configurations, gathers all the outside resources, and then hands control over to the high-level policy of the application."
  - "Since it is a plugin, it is possible to have **many `Main` components, one for each configuration** of your application. For example, you could have a `Main` plugin for **Dev**, another for **Test**, and yet another for **Production**. You could also have a `Main` plugin for **each country** you deploy to, or each **jurisdiction**, or each **customer**."
  - "When you think about `Main` as a plugin component, sitting behind an architectural boundary, **the problem of configuration becomes a lot easier to solve**."
- **"Think of `Main` as the dirtiest of all the dirty components."**

## Key Concepts
- **Main holds the strings the system shouldn't know.** In the Hunt the Wumpus example, `Main` "loads up all the strings that we don't want the main body of the code to know about" — cavern environments, shapes, types, and adornments.
- **Passing a class name by string is deliberate.** `Main` calls `HtwFactory.makeGame("htw.game.HuntTheWumpusFacade", new Main())` — "It passes in the name of the class... because **that class is even dirtier than `Main`**. This prevents changes in that class from causing `Main` to recompile/redeploy."
- **Main does the mechanical work and defers the meaning.** It creates the input stream, holds the main loop, interprets simple input commands, "but then **defers all processing to other, higher-level components**." It also creates the map.
- **Placement**: "`Main` is a dirty low-level module in the **outermost circle** of the clean architecture. It loads everything up for the high-level system, and then hands control over to it."

## Code Examples

The strings `Main` owns so the rest of the system doesn't have to:

```java
public class Main implements HtwMessageReceiver {
    private static HuntTheWumpus game;
    private static int hitPoints = 10;
    private static final List<String> caverns = new ArrayList<>();

    private static final String[] environments = new String[]{
        "bright", "humid", "dry", "creepy", "ugly", "foggy", "hot",
        "cold", "drafty", "dreadful"
    };

    private static final String[] shapes = new String[] {
        "round", "square", "oval", "irregular", "long", "craggy",
        "rough", "tall", "narrow"
    };

    private static final String[] cavernTypes = new String[] {
        "cavern", "room", "chamber", "catacomb", "crevasse", "cell",
        "tunnel", "passageway", "hall", "expanse"
    };

    private static final String[] adornments = new String[] {
        "smelling of sulfur", "with engravings on the walls",
        "with a bumpy floor", "", "littered with garbage",
        "spattered with guano", "with piles of Wumpus droppings",
        "with bones scattered around", "with a corpse on the floor",
        "that seems to vibrate", "that feels stuffy",
        "that fills you with dread"
    };
```

The main function — factory creation by class name, the input loop, and dispatch to higher-level components:

```java
    public static void main(String[] args) throws IOException {
        game = HtwFactory.makeGame("htw.game.HuntTheWumpusFacade", new Main());
        createMap();
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        game.makeRestCommand().execute();
        while (true) {
            System.out.println(game.getPlayerCavern());
            System.out.println("Health: " + hitPoints
                + " arrows: " + game.getQuiver());
            HuntTheWumpus.Command c = game.makeRestCommand();
            System.out.println(">");
            String command = br.readLine();
            if (command.equalsIgnoreCase("e"))
                c = game.makeMoveCommand(EAST);
            else if (command.equalsIgnoreCase("w"))
                c = game.makeMoveCommand(WEST);
            else if (command.equalsIgnoreCase("n"))
                c = game.makeMoveCommand(NORTH);
            else if (command.equalsIgnoreCase("s"))
                c = game.makeMoveCommand(SOUTH);
            else if (command.equalsIgnoreCase("r"))
                c = game.makeRestCommand();
            else if (command.equalsIgnoreCase("sw"))
                c = game.makeShootCommand(WEST);
            else if (command.equalsIgnoreCase("se"))
                c = game.makeShootCommand(EAST);
            else if (command.equalsIgnoreCase("sn"))
                c = game.makeShootCommand(NORTH);
            else if (command.equalsIgnoreCase("ss"))
                c = game.makeShootCommand(SOUTH);
            else if (command.equalsIgnoreCase("q"))
                return;
            c.execute();
        }
    }
```

Map creation, also `Main`'s job:

```java
    private static void createMap() {
        int nCaverns = (int) (Math.random() * 30.0 + 10.0);
        while (nCaverns-- > 0)
            caverns.add(makeName());

        for (String cavern : caverns) {
            maybeConnectCavern(cavern, NORTH);
            maybeConnectCavern(cavern, SOUTH);
            maybeConnectCavern(cavern, EAST);
            maybeConnectCavern(cavern, WEST);
        }

        String playerCavern = anyCavern();
        game.setPlayerCavern(playerCavern);
        game.setWumpusCavern(anyOther(playerCavern));
        game.addBatCavern(anyOther(playerCavern));
        game.addBatCavern(anyOther(playerCavern));
        game.addBatCavern(anyOther(playerCavern));
        game.addPitCavern(anyOther(playerCavern));
        game.addPitCavern(anyOther(playerCavern));
        game.addPitCavern(anyOther(playerCavern));
        game.setQuiver(5);
    }
    // much code removed…
}
```

## Worked Example
**Reading `Main` as a deliberate accumulation of dirt.**

Every questionable thing in this class is there *on purpose*, and each one is dirt that the rest of the system therefore doesn't carry:

| What `Main` does | What it keeps out of the system |
|---|---|
| Holds four string arrays of cavern prose | The game rules never contain a word of English |
| `makeGame("htw.game.HuntTheWumpusFacade", …)` — a class named by **string** | A compile-time dependency on an even dirtier class; changes there don't recompile `Main` |
| Constructs `BufferedReader` over `System.in` | Higher-level components never touch an input stream |
| A chain of ten `equalsIgnoreCase` branches | Command-string parsing stays at the very edge; the game receives `Command` objects |
| `createMap()` with `Math.random()` and cavern wiring | Randomized world generation stays out of the rules; the rules are handed a configured map |
| `implements HtwMessageReceiver` | The game pushes messages outward without knowing where they render |

Notice the shape: `Main` reads a raw string, converts it into a `Command` object, and calls `c.execute()`. That is the entire loop. Every decision of consequence has been converted into a call on a higher-level abstraction, which is what "hands control over to it" means concretely.

**Why "many Mains" is the practical payoff.** Because nothing depends on `Main` and `Main` sits outside the boundary, it can be swapped wholesale. Dev, Test, and Production differ in exactly the things `Main` owns — which resources to gather, which factories to build, which strings and settings to load. Per-country, per-jurisdiction, and per-customer variants are the same idea at a different axis. Configuration stops being a cross-cutting concern threaded through the application and becomes **a choice of which plugin to load**.

## Key Takeaways
1. `Main` is the lowest-level policy and the ultimate detail; only the OS depends on it.
2. Its job is creation and wiring — factories, strategies, global facilities — then handing over control.
3. Let the DI framework operate in `Main` only; distribute dependencies normally from there on.
4. Deliberately concentrate dirt in `Main`: strings, streams, parsing, randomness, class names.
5. Naming a dirtier class by string breaks the compile-time dependency on it.
6. Treat `Main` as a plugin behind an architectural boundary — then have as many as you have configurations.
7. Environment, country, jurisdiction, and customer differences become separate `Main`s rather than conditionals inside the system.

## Connects To
- **Ch 11 (DIP)**: "DIP violations cannot be entirely removed, but they can be gathered into a small number of concrete components" — `main` is that component.
- **Ch 22 (The Clean Architecture)**: `Main` in the outermost circle.
- **Ch 25 (Layers and Boundaries)**: the same Hunt the Wumpus system, viewed as boundaries.
- **Ch 32 (Frameworks Are Details)**: keeping the DI framework at arm's length from the application.
- **Clean Code, Ch 11**: separating construction from use; all wiring in `main`.
