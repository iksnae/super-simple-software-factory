# Flyweight
*Object Structural · GoF p. 195*

## Intent
> **Use sharing to support large numbers of fine-grained objects efficiently.**

## Motivation
"Some applications could benefit from using objects throughout their design, but a naive implementation would be **prohibitively expensive**."

Document editors use objects for tables and figures "but usually **stop short of using an object for each character**, even though doing so would promote flexibility at the finest levels." The reason: "Even moderate-sized documents may require **hundreds of thousands** of character objects."

**The definition**: "A **flyweight** is a shared object that can be used in multiple contexts simultaneously. The flyweight acts as an independent object in each context — **it's indistinguishable from an instance of the object that's not shared**. Flyweights **cannot make assumptions about the context** in which they operate."

**The key concept**:
- **Intrinsic state** — "stored in the flyweight; it consists of information that's **independent of the flyweight's context**, thereby making it sharable."
- **Extrinsic state** — "**depends on and varies with the flyweight's context** and therefore can't be shared. **Client objects are responsible for passing extrinsic state to the flyweight when it needs it.**"

For a character: "The **character code is intrinsic** state, while [coordinate position and typographic style] are **extrinsic**."

**The arithmetic that makes it work**: "A document in which all characters appear in the same font and color will allocate on the order of **100 character objects** (roughly the size of the ASCII character set) **regardless of the document's length**. And since most documents use no more than 10 different font-color combinations, this number won't grow appreciably in practice. **An object abstraction thus becomes practical for individual characters.**"

## Applicability
"The Flyweight pattern's effectiveness depends **heavily** on how and where it's used. Apply the Flyweight pattern when **all** of the following are true:"
- "An application uses a **large number** of objects."
- "**Storage costs are high** because of the sheer quantity of objects."
- "**Most object state can be made extrinsic.**"
- "**Many groups of objects may be replaced by relatively few shared objects** once extrinsic state is removed."
- "The application **doesn't depend on object identity**. Since flyweight objects may be shared, **identity tests will return true for conceptually distinct objects**."

## Participants
- **Flyweight** (`Glyph`) — "declares an interface through which flyweights can **receive and act on extrinsic state**."
- **ConcreteFlyweight** (`Character`) — implements the interface and adds storage for intrinsic state. "**A ConcreteFlyweight object must be sharable. Any state it stores must be intrinsic.**"
- **UnsharedConcreteFlyweight** (`Row`, `Column`) — "**not all Flyweight subclasses need to be shared. The Flyweight interface enables sharing; it doesn't enforce it.** It's common for UnsharedConcreteFlyweight objects to have ConcreteFlyweight objects as children."
- **FlyweightFactory** — "creates and manages flyweight objects... **supplies an existing instance or creates one, if none exists**."
- **Client** — maintains a reference to flyweights; **computes or stores the extrinsic state**.

## Collaborations
- "Intrinsic state is stored in the ConcreteFlyweight object; extrinsic state is stored or computed by Client objects."
- "**Clients should not instantiate ConcreteFlyweights directly.** Clients must obtain ConcreteFlyweight objects **exclusively from the FlyweightFactory** to ensure they are shared properly."

## Consequences
"Flyweights may introduce **run-time costs** associated with transferring, finding, and/or computing extrinsic state, especially if it was formerly stored as intrinsic state. However, such costs are **offset by space savings**, which increase as more flyweights are shared."

Storage savings are a function of:
- "the **reduction in the total number of instances** that comes from sharing"
- "the **amount of intrinsic state per object**"
- "whether extrinsic state is **computed or stored**"

**"The greatest savings occur when the objects use substantial quantities of both intrinsic and extrinsic state, and the extrinsic state can be computed rather than stored. Then you save on storage in two ways: Sharing reduces the cost of intrinsic state, and you trade extrinsic state for computation time."**

⚠️ **The structural consequence with Composite**: "A consequence of sharing is that **flyweight leaf nodes cannot store a pointer to their parent**. Rather, the parent pointer is passed to the flyweight as part of its extrinsic state. **This has a major impact on how the objects in the hierarchy communicate with each other.**"

## Implementation
1. **Removing extrinsic state.** "The pattern's applicability is determined largely by how easy it is to identify extrinsic state and remove it... **Removing extrinsic state won't help reduce storage costs if there are as many different kinds of extrinsic state as there are objects before sharing.** Ideally, extrinsic state can be **computed from a separate object structure**, one with far smaller storage requirements."
   - The document-editor technique: "store a **map of typographic information in a separate structure**... The map keeps track of **runs** of characters with the same typographic attributes. When a character draws itself, it receives its typographic attributes **as a side-effect of the draw traversal**."
2. **Managing shared objects.** "FlyweightFactory objects often use an **associative store**... Sharability also implies some form of **reference counting or garbage collection**... However, **neither is necessary if the number of flyweights is fixed and small** (e.g., flyweights for the ASCII character set). In that case, the flyweights are worth keeping around permanently."

## Sample Code

Every operation takes a `GlyphContext` — that parameter *is* the pattern:

```cpp
class Glyph {
public:
    virtual ~Glyph();

    virtual void Draw(Window*, GlyphContext&);

    virtual void SetFont(Font*, GlyphContext&);
    virtual Font* GetFont(GlyphContext&);

    virtual void First(GlyphContext&);
    virtual void Next(GlyphContext&);
    virtual bool IsDone(GlyphContext&);
    virtual Glyph* Current(GlyphContext&);

    virtual void Insert(Glyph*, GlyphContext&);
    virtual void Remove(GlyphContext&);
protected:
    Glyph();
};
```
```cpp
class Character : public Glyph {
public:
    Character(char);

    virtual void Draw(Window*, GlyphContext&);
private:
    char _charcode;
};
```
- The `Character` flyweight stores **one byte**.

```cpp
class GlyphContext {
public:
    GlyphContext();
    virtual ~GlyphContext();

    virtual void Next(int step = 1);
    virtual void Insert(int quantity = 1);

    virtual Font* GetFont();
    virtual void SetFont(Font*, int span = 1);
private:
    int _index;
    BTree* _fonts;
};
```
- "`GlyphContext` acts as a **repository of extrinsic state**. It maintains a **compact mapping** between a glyph and its font in different contexts."
- "`GlyphContext` must be kept informed of the current position **during traversal**. `GlyphContext::Next` increments `_index` as the traversal proceeds. Glyph subclasses that have children (e.g. `Row` and `Column`) **must implement `Next` so that it calls `GlyphContext::Next`** at each point in the traversal."

**The BTree of font runs** — "Each node in the tree is labeled with the length of the string for which it gives font information. **Leaves in the tree point to a font, while interior nodes break the string into substrings**, one for each child."

```cpp
GlyphContext gc;
Font* times12 = new Font("Times-Roman-12");
Font* timesItalic12 = new Font("Times-Italic-12");
// ...

gc.SetFont(times12, 6);
```
```cpp
gc.Insert(6);
gc.SetFont(timesItalic12, 6);
```
- "When the `GlyphContext` is queried for the font of the current glyph, it **descends the BTree, adding up indices** as it goes until it finds the font for the current index. **Because the frequency of font changes is relatively low, the tree stays small relative to the size of the glyph structure.** This keeps storage costs down without an inordinate increase in look-up time."
- (Footnote: "Look-up time in this scheme is **proportional to the font change frequency**. Worst-case performance occurs when a font change occurs on every character, but that's unusual in practice.")

**The factory** — sharing only what's worth sharing:

```cpp
const int NCHARCODES = 128;

class GlyphFactory {
public:
    GlyphFactory();
    virtual ~GlyphFactory();

    virtual Character* CreateCharacter(char);
    virtual Row* CreateRow();
    virtual Column* CreateColumn();
    // ...
private:
    Character* _character[NCHARCODES];
};

GlyphFactory::GlyphFactory () {
    for (int i = 0; i < NCHARCODES; ++i) {
        _character[i] = 0;
    }
}

Character* GlyphFactory::CreateCharacter (char c) {
    if (!_character[c]) {
        _character[c] = new Character(c);
    }
    return _character[c];
}

Row* GlyphFactory::CreateRow () { return new Row; }
Column* GlyphFactory::CreateColumn () { return new Column; }
```
- "**We only share `Character` objects**; composite glyphs are far less plentiful, and their important state (i.e., their children) is **intrinsic anyway**."
- And a forward-compatibility argument for routing unshared creation through the factory too: "We could omit these operations and let clients instantiate unshared glyphs directly. However, **if we decide to make these glyphs sharable later, we'll have to change client code that creates them.**"

## Known Uses
- **InterViews 3.0** — where "the concept of flyweight objects was first described and explored as a design technique." Its proof of concept was the document editor **Doc**.
  - Doc's variation: "The editor builds one `Glyph` instance for **each character in a particular style**; hence a character's intrinsic state consists of the character code **and its style information** (an index into a style table). That means **only position is extrinsic, making Doc fast**." (Footnote: the Sample Code above instead makes style extrinsic, "leaving the character code as the only intrinsic state.")
  - **The measurement**: "In a typical case, a document containing **180,000 characters required allocation of only 480 character objects**."
- **ET++** — flyweights for look-and-feel independence. "A widget delegates all its layout and drawing behavior to a separate `Layout` object. **Changing the `Layout` object changes the look and feel, even at run-time.**"
  - The problem flyweight solves here: "using separate layout objects **doubles the number of user interface objects**... To avoid this overhead, `Layout` objects are implemented as flyweights. **They make good flyweights because they deal mostly with defining behavior**, and it's easy to pass them what little extrinsic state they need."
  - "The `Layout` objects are created and managed by `Look` objects. **The `Look` class is an Abstract Factory**... For each look-and-feel standard there is a corresponding `Look` subclass (`MotifLook`, `OpenLook`)."
  - And the pattern-composition note: "By the way, **`Layout` objects are essentially strategies. They are an example of a strategy object implemented as a flyweight.**"

## Related Patterns
- "often combined with **Composite** to implement a logically hierarchical structure in terms of a **directed-acyclic graph with shared leaf nodes**."
- "It's often best to implement **State** and **Strategy** objects as flyweights."

## Connects To
- **Ch 1**: "the Flyweight pattern describes how to support **huge numbers of objects at the finest granularities**" (determining object granularity).
- **Ch 2 (Case Study)**: named in a footnote as the way to recover the storage cost of one object per character in Lexi.
- **Ch 12 (Composite)**: "Flyweight lets you share components, but they can no longer refer to their parents."
- **Composite, State, Strategy, Abstract Factory**
