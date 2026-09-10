# Chapter 5: Object-Oriented Programming

## Core Idea
Encapsulation, inheritance, and polymorphism are all older than OO — but OO made polymorphism **safe and convenient**, and that gives the architect **absolute control over the direction of every source code dependency in the system**.

## Frameworks Introduced
- **Dismantling the three magic words**:
  - **Encapsulation? No points.** C had *perfect* encapsulation — forward-declare the struct and functions in a header, implement them elsewhere, and users have no knowledge of the implementation whatsoever. C++ **broke** it, because the compiler needs each class's member variables in the header to know instance sizes; clients now *know* `x` and `y` exist, and renaming them forces recompilation. `public`/`private`/`protected` are "a hack necessitated by [that] technical need." Java and C# abolished the header/implementation split entirely, "thereby weakening encapsulation even more."
  - **Inheritance? Half a point.** It is "simply the redeclaration of a group of variables and functions within an enclosing scope," achievable in C by making `NamedPoint` a pure superset of `Point` with matching field order and upcasting the pointer. "In fact, such trickery is how C++ implements single inheritance." OO made the masquerade significantly more convenient (upcasting is implicit) and multiple inheritance much easier.
  - **Polymorphism? Also predates OO** — but this is where the real answer lives.
- **Polymorphism is an application of pointers to functions.** "Programmers have been using pointers to functions to achieve polymorphic behavior since Von Neumann architectures were first implemented in the late 1940s."
  - How C++ does it: every virtual function has a pointer in a **vtable**, all virtual calls go through it, and derivative constructors load their versions into the vtable of the object being created. "This simple trick is the basis for all polymorphism in OO."
- **What OO actually added: discipline on indirect transfer of control.** Explicit function pointers are *dangerous* — driven by manual conventions you must remember to initialize and to call through. "If any programmer fails to remember these conventions, the resulting bug can be devilishly hard to track down and eliminate." OO eliminates the conventions and therefore the danger.
- **Dependency Inversion**: place an interface between caller and callee, and the **source code dependency points opposite to the flow of control**.
  - "The fact that OO languages provide safe and convenient polymorphism means that **any source code dependency, no matter where it is, can be inverted**."
  - Consequence: "software architects working in systems written in OO languages have **absolute control over the direction of all source code dependencies** in the system. They are not constrained to align those dependencies with the flow of control."
- **Independent deployability → independent developability**: point the dependencies so the UI and database depend on the business rules; the business rules' source never mentions either. The three compile into separate deployment units (jars, DLLs, gems) with the same dependency structure. "When the source code in a component changes, only that component needs to be redeployed." And modules deployable independently can be developed independently by different teams.

## Key Concepts
- **The unsatisfying answers to "what is OO?"** — "The combination of data and function" implies `o.f()` differs from `f(o)`, "which is absurd. Programmers were passing data structures into functions long before 1966." "A way to model the real world" is "an evasive answer at best... It does not tell us what OO is."
- **Plugin architecture** — the IO devices become plugins to the copy program. UNIX made IO devices plugins because "we learned, in the late 1950s, that our programs should be device independent," after writing card-reading programs and then being handed magnetic tape. "**OO allows the plugin architecture to be used anywhere, for anything.**"
- **Why most programmers didn't extend the idea** to their own programs before OO: "because using pointers to functions was dangerous."
- **The interface is a source code contrivance.** "At runtime, the interface doesn't exist. HL1 simply calls F() within ML1" — albeit indirectly.

## Mental Models
- **Before polymorphism, the architect had no choices.** In a typical calling tree, `main` calls high-level functions, which call mid-level, which call low-level — and "source code dependencies inexorably followed the flow of control," because every caller had to `#include`/`import`/`using` the module containing the callee. "The flow of control was dictated by the behavior of the system, and the source code dependencies were dictated by that flow of control."
- **Any dependency in that tree can be turned around by inserting an interface between them.** That is the whole lever.
- **The architect's definition of OO**: "OO is the ability, through the use of polymorphism, to gain absolute control over every source code dependency in the system. It allows the architect to create a plugin architecture, in which modules that contain high-level policies are independent of modules that contain low-level details."

## Code Examples

Perfect encapsulation, in C:

```c
/* point.h */
struct Point;
struct Point* makePoint(double x, double y);
double distance(struct Point *p1, struct Point *p2);
```
```c
/* point.c */
#include "point.h"
#include <stdlib.h>
#include <math.h>

struct Point {
    double x,y;
};

struct Point* makepoint(double x, double y) {
    struct Point* p = malloc(sizeof(struct Point));
    p->x = x;
    p->y = y;
    return p;
}

double distance(struct Point* p1, struct Point* p2) {
    double dx = p1->x - p2->x;
    double dy = p1->y - p2->y;
    return sqrt(dx*dx+dy*dy);
}
```
- **What it demonstrates**: users of `point.h` have *no access whatsoever* to the members of `struct Point` and no knowledge of either implementation.

The C++ version, where encapsulation breaks:

```cpp
// point.h
class Point {
public:
    Point(double x, double y);
    double distance(const Point& p) const;
private:
    double x;
    double y;
};
```
- **What it demonstrates**: clients now know `x` and `y` exist. Rename them and `point.cc` must be recompiled.

Inheritance by masquerade, in C:

```c
/* namedPoint.c */
struct NamedPoint {
    double x,y;
    char* name;
};
```
```c
/* main.c */
int main(int ac, char** av) {
    struct NamedPoint* origin = makeNamedPoint(0.0, 0.0, "origin");
    struct NamedPoint* upperRight = makeNamedPoint(1.0, 1.0, "upperRight");
    printf("distance=%f\n",
           distance((struct Point*) origin, (struct Point*) upperRight));
}
```
- **What it demonstrates**: `NamedPoint` acts as a derivative of `Point` because it is a pure superset with the corresponding members in the same order. Note the explicit casts — "in a real OO language, such upcasting would be implicit."

## Worked Example
**The C copy program, and why it never needs to change.**

```c
#include <stdio.h>

void copy() {
    int c;
    while ((c=getchar()) != EOF)
        putchar(c);
}
```

`getchar()` reads from `STDIN` — but *which device* is `STDIN`? `putchar()` writes to `STDOUT` — which device is that? "These functions are polymorphic — their behavior depends on the type of `STDIN` and `STDOUT`." There are no interfaces in this C program, so how does the call reach the right device driver?

UNIX requires every IO device driver to provide five standard functions with identical signatures: `open`, `close`, `read`, `write`, `seek`. The `FILE` structure holds five function pointers:

```c
struct FILE {
    void (*open)(char* name, int mode);
    void (*close)();
    int (*read)();
    void (*write)(char);
    void (*seek)(long index, int mode);
};
```

Each driver defines those functions and loads their addresses into a `FILE`:

```c
#include "file.h"
void open(char* name, int mode) {/*...*/}
void close() {/*...*/};
int read() {int c;/*...*/ return c;}
void write(char c) {/*...*/}
void seek(long index, int mode) {/*...*/}

struct FILE console = {open, close, read, write, seek};
```

And `getchar()` is simply an indirect call:

```c
extern struct FILE* STDIN;

int getchar() {
    return STDIN->read();
}
```

**Now the payoff question.** Suppose a new IO device appears — copy data from a handwriting recognition device to a speech synthesizer. How must `copy` change?

"**We don't need any changes at all!** Indeed, we don't even need to recompile the copy program. Why? Because the source code of the copy program does not depend on the source code of the IO drivers. As long as those IO drivers implement the five standard functions defined by `FILE`, the copy program will be happy to use them."

The IO devices have become **plugins**. And the historical reason UNIX did this is the same reason architects do it now: programs written against card readers had to be rewritten when customers switched to magnetic tape. The plugin architecture was invented for IO device independence — OO's contribution is making the same technique safe enough to use *anywhere, for anything*.

**Turning the arrow around, at system scale.** Apply the inversion to the whole system and you can make the **database and the UI depend on the business rules** rather than the reverse. Then:

- The business rules' source code never mentions the UI or the database.
- The three compile into separate deployment units whose dependencies match the source dependencies.
- The business-rules component does not depend on the UI or database components.
- Business rules deploy independently; UI or database changes need not affect them.
- **Independent deployability** follows — change one component, redeploy only that component.
- **Independent developability** follows from that — separate teams can own separate components.

"That is power! That is the power that OO provides. That's what OO is really all about — at least from the architect's point of view."

## Reference Tables

| Claimed OO feature | Available pre-OO? | What OO actually added | Score |
|---|---|---|---|
| Encapsulation | Yes — perfect, in C | Nothing; C++ *weakened* it, Java/C# weakened it further | **No points** |
| Inheritance | Yes — by superset + field ordering + casting | Convenience: implicit upcasting, feasible multiple inheritance | **Half a point** |
| Polymorphism | Yes — function pointers since the late 1940s | **Safety and convenience**: no manual conventions to remember or forget | **The whole answer** |

## Key Takeaways
1. OO gave us nothing categorically new; it made one old thing — polymorphism — safe enough to use everywhere.
2. Polymorphism is function pointers with the manual conventions removed and the danger eliminated.
3. Safe polymorphism means **any** source code dependency can be inverted by inserting an interface.
4. Source code dependencies need not follow the flow of control; the architect chooses their direction.
5. Point the arrows so that details (UI, database) depend on policy (business rules) — never the reverse.
6. That arrangement makes details into plugins, which yields independent deployability and independent developability.
7. To an architect, that control *is* what OO is.

## Connects To
- **Ch 3 (Paradigm Overview)**: OO as discipline on indirect transfer of control.
- **Ch 11 (DIP)**: the principle stated formally.
- **Ch 17–19 (Boundaries, Boundary Anatomy, Policy and Level)**: polymorphism as the mechanism for crossing boundaries.
- **Ch 22 (The Clean Architecture)**: the Dependency Rule is this chapter's arrow, applied everywhere.
- **Ch 30–32 (The Database / The Web / Frameworks Are Details)**: what "plugin" means for each.
