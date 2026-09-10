# Chapter 2: A Case Study — Designing a Document Editor

## Core Idea
Eight patterns applied to one WYSIWYG editor, **Lexi**, each arriving as the answer to a stated design problem — and every one of them is an instance of the same move: **encapsulate the concept that varies**.

## Frameworks Introduced
- **The seven design problems** (each culminating in a pattern):
  1. **Document structure** — "The choice of internal representation for the document affects nearly every aspect of Lexi's design."
  2. **Formatting** — arranging text and graphics into lines and columns.
  3. **Embellishing the user interface** — scroll bars, borders, drop shadows that "are likely to change as Lexi's user interface evolves."
  4. **Supporting multiple look-and-feel standards** — Motif, Presentation Manager.
  5. **Supporting multiple window systems** — "Different look-and-feel standards are usually implemented on different window systems."
  6. **User operations** — "a uniform mechanism both for accessing this scattered functionality and for undoing its effects."
  7. **Spelling checking and hyphenation** — "How can we minimize the number of classes we have to modify to add a new analytical operation?"
- **Recursive composition** — "building increasingly complex elements out of simpler ones." Tile characters and graphics into a line; lines into a column; columns into a page. Represent it "by devoting an object to each important element... not just the visible elements like the characters and graphics but **the invisible, structural elements as well** — the lines and the column."
- **Transparent enclosure** — combines "(1) single-child (or single-component) composition and (2) compatible interfaces. Clients generally can't tell whether they're dealing with the component or its enclosure... But the enclosure can also **augment** the component's behavior by doing work of its own before and/or after delegating an operation."
- **Intersection vs. union of functionality** — the two extremes for spanning multiple platforms, both rejected:
  - *Intersection*: "our Window interface winds up being only as powerful as the **least capable** window system."
  - *Union*: "the resulting interface may well be **huge and incoherent**. Besides, we'll have to change it... anytime a vendor revises its window system interface."
  - The answer falls between: "a convenient interface that supports the **most popular** windowing features."
- **Traversal vs. traversal actions** — separate them, "because different analyses often require the same kind of traversal. Hence we can reuse the same set of iterators for different analyses."

## Key Concepts
- **Glyph** — the abstract class for everything that can appear in a document. Three responsibilities: "(1) how to draw themselves, (2) what space they occupy, and (3) their children and parent."
- **Why an object per character** — "we promote flexibility at the finest levels... We can treat text and graphics uniformly with respect to how they are drawn, formatted, and embedded within each other." (Footnote: most contemporary editors don't do this for efficiency reasons; Calder demonstrated it is feasible, and **Flyweight** would recover the storage.)
- **Use `Child()` internally, not the data structure** — "That way you won't have to modify operations like `Draw` that iterate through the children when you change the data structure from, say, an array to a linked list."
- **The subclass explosion**, twice over: `BorderedComposition`, `ScrollableComposition`, `BorderedScrollableComposition` — "In the extreme, we end up with a class for every possible combination of embellishments." And for window systems, implementation-specific subclasses of every `Window` class produce "another subclass explosion problem."
- **Why the border contains the glyph, not vice versa** — "keeps the border-drawing code entirely in the `Border` class, leaving other classes alone." And `Border` must subclass `Glyph` because "**clients shouldn't care whether glyphs have borders or not**."
- **Why embellishment composes exactly one child** — "putting a border around something implies that 'something' is singular. We could assign a meaning to embellishing more than one object at a time, but then we'd have to mix many kinds of composition in with the notion of embellishment: row embellishment, column embellishment... **it's better to use existing classes for composition and add new classes to embellish the result**."
- **Why Abstract Factory doesn't work for window systems** — it worked for widgets because "we would define the concrete widget glyph classes for each look-and-feel standard," giving a common abstract product per widget kind. With existing vendor hierarchies, "it's highly unlikely these hierarchies are compatible in any way. Hence we won't have a common abstract product class for each kind of widget — **and the Abstract Factory pattern won't work without those crucial classes**."
- **Window vs. WindowImp, the design-audience split** — "**Window's interface caters to the applications programmer, while WindowImp caters to window systems.**" WindowImp's interface "can more closely reflect what window systems actually provide, **warts and all**."
- **Why parameterize `MenuItem` with an object, not a function** — three reasons: "(1) It doesn't address the undo/redo problem. (2) It's hard to associate state with a function... (3) Functions are hard to extend, and it's hard to reuse parts of them."
- **`Reversible`** — undoability determined at run time. "If the net effect of executing a command was nothing, then there's no need for a corresponding undo request." A user repeating a spurious font change "shouldn't have to perform exactly the same number of undo operations to get back to the last meaningful operation."
- **Discretionary glyph** — inserted by the hyphenation visitor: "has one of two possible appearances depending on whether or not it is the last character on a line. If it's the last character, then the discretionary looks like a hyphen; if it's not at the end of a line, then the discretionary has no appearance whatsoever."

## Code Examples

Transparent enclosure — total delegation, then augmentation:

```cpp
void MonoGlyph::Draw (Window* w) {
    _component->Draw(w);
}
```
```cpp
void Border::Draw (Window* w) {
    MonoGlyph::Draw(w);
    DrawBorder(w);
}
```
- **What it demonstrates**: `Border::Draw` **extends** the parent operation rather than replacing it — "which would omit the call to `MonoGlyph::Draw`."

Abstracting object creation — the one-line change that removes a platform name:

```cpp
ScrollBar* sb = new MotifScrollBar;          // hard-codes the look and feel
ScrollBar* sb = guiFactory->CreateScrollBar(); // no longer anything mentioning Motif
```
- **What it demonstrates**: "As far as clients are concerned, the effect is the same as calling the `MotifScrollBar` constructor directly. But there's a crucial difference: **There's no longer anything in the code that mentions Motif by name.**" And the danger of not doing it: "miss just one, and you could end up with a **Motif menu in the middle of your Mac application**."

Selecting the factory at startup:

```cpp
GUIFactory* guiFactory;
const char* styleName = getenv("LOOK_AND_FEEL");
// user or environment supplies this at startup
if (strcmp(styleName, "Motif") == 0) {
    guiFactory = new MotifFactory;
} else if (strcmp(styleName, "Presentation_Manager") == 0) {
    guiFactory = new PMFactory;
} else {
    guiFactory = new DefaultGUIFactory;
}
```
More sophisticated: "maintain a **registry** that maps strings to factory objects. That lets you register instances of new factory subclasses without modifying existing code... And you don't have to link all platform-specific factories into the application. That's important, because **it might not be possible to link a MotifFactory on a platform that doesn't support Motif**."

Bridge — one abstraction, two wildly different implementations:

```cpp
void Rectangle::Draw (Window* w) {
    w->DrawRect(_x0, _y0, _x1, _y1);
}

void Window::DrawRect (Coord x0, Coord y0, Coord x1, Coord y1) {
    _imp->DeviceRect(x0, y0, x1, y1);
}
```
```cpp
void XWindowImp::DeviceRect (Coord x0, Coord y0, Coord x1, Coord y1) {
    int x = round(min(x0, x1));
    int y = round(min(y0, y1));
    int w = round(abs(x0 - x1));
    int h = round(abs(y0 - y1));
    XDrawRectangle(_dpy, _winid, _gc, x, y, w, h);
}
```
```cpp
void PMWindowImp::DeviceRect (Coord x0, Coord y0, Coord x1, Coord y1) {
    Coord left   = min(x0, x1);
    Coord right  = max(x0, x1);
    Coord bottom = min(y0, y1);
    Coord top    = max(y0, y1);

    PPOINTL point[4];
    point[0].x = left;  point[0].y = top;
    point[1].x = right; point[1].y = top;
    point[2].x = right; point[2].y = bottom;
    point[3].x = left;  point[3].y = bottom;

    if ((GpiBeginPath(_hps, 1L) == false) ||
        (GpiSetCurrentPosition(_hps, &point[3]) == false) ||
        (GpiPolyLine(_hps, 4L, point) == GPI_ERROR) ||
        (GpiEndPath(_hps) == false)) {
        // report error
    } else {
        GpiStrokePath(_hps, 1L, 0L);
    }
}
```
- **What it demonstrates**: "Why is this so different from the X version? Well, **PM doesn't have an operation for drawing rectangles explicitly** as X does. Instead, PM has a more general interface for specifying vertices of multisegment shapes (called a path)." The variation is absorbed entirely below `Window`.

Iterator — client code that knows nothing of the representation:

```cpp
Glyph* g;
Iterator<Glyph*>* i = g->CreateIterator();
for (i->First(); !i->IsDone(); i->Next()) {
    Glyph* child = i->CurrentItem();
    // do something with current child
}
```
```cpp
Iterator<Glyph*>* Row::CreateIterator () {
    return new ListIterator<Glyph*>(_children);
}
```
`CreateIterator` returns a `NullIterator` by default — "a degenerate iterator for glyphs that have no children... `NullIterator`'s `IsDone` operation always returns true."

The type-test code that Visitor exists to avoid:

```cpp
void SpellingChecker::Check (Glyph* glyph) {
    Character* c;
    Row* r;
    Image* i;

    if (c = dynamic_cast<Character*>(glyph)) {
        // analyze the character
    } else if (r = dynamic_cast<Row*>(glyph)) {
        // prepare to analyze r's children
    } else if (i = dynamic_cast<Image*>(glyph)) {
        // do nothing
    }
}
```
- **What it demonstrates**: "This code is pretty ugly. It relies on fairly esoteric capabilities like type-safe casts. It's hard to extend as well... **In fact, this is the kind of code that object-oriented languages were intended to eliminate.**"

Double dispatch, which replaces it:

```cpp
void GlyphSubclass::CheckMe (SpellingChecker& checker) {
    checker.CheckGlyphSubclass(this);
}
```
- **What it demonstrates**: "when `CheckMe` is called, **the specific Glyph subclass is known** — after all, we're in one of its operations."

## Worked Example
**The seven problems, and the pattern each one produces.**

| § | Problem | The constraint that forces the design | Pattern |
|---|---|---|---|
| 2.2 | Document structure | Treat text and graphics **uniformly**; "our implementation shouldn't have to distinguish between single elements and groups of elements" — the tenth element of line five "could be a single character or an intricate diagram" | **Composite** |
| 2.3 | Formatting | Formatting quality vs. speed is a run-time trade-off; "adding a new formatting algorithm shouldn't require modifying existing glyphs" | **Strategy** |
| 2.4 | Embellishment | Add/remove borders and scroll bars **at run time**; inheritance yields a class per combination | **Decorator** |
| 2.5 | Look and feel | Cannot hard-code `new MotifScrollBar`; must swap an entire widget family | **Abstract Factory** |
| 2.6 | Window systems | Vendor hierarchies are incompatible, so no common abstract product exists; must separate the logical window from its implementation | **Bridge** |
| 2.7 | User operations | Same operation reachable from menu, button, and accelerator; unlimited undo/redo | **Command** |
| 2.8 | Analysis | Many analyses over one stable glyph hierarchy; must not expand the `Glyph` interface per analysis | **Iterator** + **Visitor** |

**Two of these deserve tracing in full.**

**Undo, built from a command history.** Adding `Unexecute` to `Command` gives one level. Arbitrary levels come from a list of executed commands with a "present" line marking the most recently executed one. Undo calls `Unexecute` on the command at the present line and moves the line **left**; redo calls `Execute` on the command to the right and moves the line **right**. "By simply repeating this procedure we get multiple levels of undo. The number of levels is limited only by the length of the command history... Thus the user can effectively **go back and forth in time** as needed to recover from errors."

**Why the Glyph interface must not grow per analysis.** The naive route is an abstract operation on `Glyph` for each analysis, with a default implementation in `Glyph` to limit the damage. The chapter concedes that helps — and then names the real cost: "**even if a default implementation reduces the number of changes, an insidious problem remains: Glyph's interface expands with every new analytical capability. Over time the analytical operations will start to obscure the basic Glyph interface.** It becomes hard to see that a glyph's main purpose is to define and structure objects that have appearance and shape — **that interface gets lost in the noise**."

Visitor's resolution: give every analysis class the same interface, rename `CheckMe` to `Accept` taking a `Visitor&`, and "adding a new analysis requires just defining a new subclass of visitor — **we don't have to touch any of the glyph classes**."

And the pattern's cost, stated plainly rather than hidden: "whenever you add a subclass to the structure, you'll also have to **update all your visitor interfaces**... adding a new Glyph subclass called Foo will require changing Visitor and all its subclasses to include a `VisitFoo` operation. But given our design constraints, we're much more likely to add a new kind of analysis to Lexi than a new kind of Glyph."

That is the decisive question the chapter leaves you with: **"Which class hierarchies change most often?"**

## Key Takeaways
1. Every one of the eight patterns arrives from the same move — encapsulate the concept that varies.
2. Recursive composition needs objects for the *invisible* structural elements too, and compatible interfaces via inheritance.
3. Transparent enclosure = single-child composition + matching interface; it lets embellishments be added, removed, and reordered at run time.
4. Composition order is a design choice with visible consequences (border inside scroller vs. scroller inside border).
5. Abstract Factory requires that you own the abstract product classes; where vendors own incompatible hierarchies, use Bridge instead.
6. An interface serving application programmers and one serving platforms are different interfaces — split the hierarchies.
7. Parameterize with objects rather than functions when you need state, extension, and undo.
8. Separate traversal from the actions performed during traversal; iterators become reusable across analyses.
9. Before choosing Visitor, ask which hierarchy changes more often — the elements or the operations.

## Connects To
- **Ch 1**: the two principles and the "encapsulate what varies" theme this chapter demonstrates eight times.
- **Composite, Strategy, Decorator, Abstract Factory, Bridge, Command, Iterator, Visitor**: the eight catalog entries, each of which references this case study.
- **Flyweight**: named in a footnote as the way to recover the storage cost of an object per character.
- **Singleton**: named as the way to manage the well-known `guiFactory` instance.
