# Bridge
*Object Structural · Also Known As: **Handle/Body** · GoF p. 151*

## Intent
> **Decouple an abstraction from its implementation so that the two can vary independently.**

## Motivation
"When an abstraction can have one of several possible implementations, the usual way to accommodate them is to use inheritance... But this approach isn't always flexible enough. **Inheritance binds an implementation to the abstraction permanently**, which makes it difficult to modify, extend, and reuse abstractions and implementations independently."

A portable `Window` with `XWindow` and `PMWindow` subclasses has **two drawbacks**:

1. **The combinatorial explosion.** "Imagine an `IconWindow` subclass... To support IconWindows for both platforms, we have to implement two new classes, `XIconWindow` and `PMIconWindow`. Worse, **we'll have to define two classes for every kind of window**. Supporting a third platform requires yet another new Window subclass for every kind of window."
2. **It makes client code platform-dependent.** "creating an `XWindow` object binds the Window abstraction to the X Window implementation, which makes the client code dependent on [it]. This, in turn, makes it **harder to port the client code**."

"Clients should be able to create a window **without committing to a concrete implementation**. Only the window implementation should depend on the platform."

The fix: two separate hierarchies — window interfaces (`Window`, `IconWindow`, `TransientWindow`) and platform implementations rooted at `WindowImp`. "We refer to the relationship between `Window` and `WindowImp` as a **bridge**, because it bridges the abstraction and its implementation, letting them vary independently."

## Applicability
Use Bridge when:
- "you want to **avoid a permanent binding** between an abstraction and its implementation... for example, when the implementation must be **selected or switched at run-time**."
- "**both** the abstractions and their implementations should be extensible by subclassing."
- "changes in the implementation of an abstraction should have **no impact on clients**; that is, their code should not have to be **recompiled**."
- **(C++)** "you want to **hide the implementation of an abstraction completely** from clients. In C++ the representation of a class is visible in the class interface."
- "you have a **proliferation of classes**... Rumbaugh uses the term '**nested generalizations**' to refer to such class hierarchies."
- "you want to **share an implementation among multiple objects** (perhaps using reference counting), and this fact should be hidden from the client." (Coplien's `String`/`StringRep`.)

## Participants
- **Abstraction** (`Window`) — defines the abstraction's interface; maintains a reference to an Implementor.
- **RefinedAbstraction** (`IconWindow`) — extends the interface defined by Abstraction.
- **Implementor** (`WindowImp`) — defines the interface for implementation classes. **"This interface doesn't have to correspond exactly to Abstraction's interface; in fact the two interfaces can be quite different. Typically the Implementor interface provides only primitive operations, and Abstraction defines higher-level operations based on these primitives."**
- **ConcreteImplementor** (`XWindowImp`, `PMWindowImp`) — implements the Implementor interface.

## Collaborations
- "Abstraction forwards client requests to its Implementor object."

## Consequences
1. **Decoupling interface and implementation.** "The implementation of an abstraction can be configured at run-time. **It's even possible for an object to change its implementation at run-time.**"
   - "Decoupling also **eliminates compile-time dependencies** on the implementation. Changing an implementation class doesn't require recompiling the Abstraction class and its clients. **This property is essential when you must ensure binary compatibility between different versions of a class library.**"
   - "this decoupling encourages **layering**... The high-level part of a system only has to know about Abstraction and Implementor."
2. **Improved extensibility.** "You can extend the Abstraction and Implementor hierarchies **independently**."
3. **Hiding implementation details from clients** — "like the sharing of implementor objects and the accompanying reference count mechanism."

## Implementation
1. **Only one Implementor.** "In situations where there's only one implementation, creating an abstract Implementor class isn't necessary. This is a **degenerate case**... Nevertheless, this separation is still useful when a change in the implementation of a class must not affect its existing clients — that is, **they shouldn't have to be recompiled, just relinked**."
   - "Carolan uses the term '**Cheshire Cat**' to describe this separation. In C++, the class interface of the Implementor class can be defined in a **private header file** that isn't provided to clients."
2. **Creating the right Implementor object** — three strategies:
   - **Abstraction decides in its constructor**, based on parameters. "If, for example, a collection class supports multiple implementations, the decision can be based on the **size** of the collection. A linked list implementation can be used for small collections and a hash table for larger ones."
   - **Choose a default and switch later** — "if the collection grows bigger than a certain threshold, then it **switches its implementation**."
   - **Delegate to a factory** ✅ — "a factory object whose sole duty is to encapsulate platform-specifics... **A benefit of this approach is that Abstraction is not coupled directly to any of the Implementor classes.**"
3. **Sharing implementors** — the Handle/Body idiom with reference counting:

```cpp
Handle& Handle::operator= (const Handle& other) {
    other._body->Ref();
    _body->Unref();

    if (_body->RefCount() == 0) {
        delete _body;
    }
    _body = other._body;

    return *this;
}
```
4. **Using multiple inheritance** — ⚠️ "a class can inherit publicly from Abstraction and privately from a ConcreteImplementor. **But because this approach relies on static inheritance, it binds an implementation permanently to its interface. Therefore you can't implement a true Bridge with multiple inheritance — at least not in C++.**"

## Sample Code

```cpp
class Window {
public:
    Window(View* contents);

    // requests handled by window
    virtual void DrawContents();
    virtual void Open();
    virtual void Close();
    virtual void Iconify();
    virtual void Deiconify();

    // requests forwarded to implementation
    virtual void SetOrigin(const Point& at);
    virtual void SetExtent(const Point& extent);
    virtual void Raise();
    virtual void Lower();

    virtual void DrawLine(const Point&, const Point&);
    virtual void DrawRect(const Point&, const Point&);
    virtual void DrawPolygon(const Point[], int n);
    virtual void DrawText(const char*, const Point&);
protected:
    WindowImp* GetWindowImp();
    View* GetView();
private:
    WindowImp* _imp;
    View* _contents;    // the window's contents
};
```
- Note the deliberate split in the comments: some requests the window **handles**, others it **forwards**.

The implementor's interface is *primitive* — `Device*` operations, not `Draw*`:

```cpp
class WindowImp {
public:
    virtual void ImpTop() = 0;
    virtual void ImpBottom() = 0;
    virtual void ImpSetExtent(const Point&) = 0;
    virtual void ImpSetOrigin(const Point&) = 0;

    virtual void DeviceRect(Coord, Coord, Coord, Coord) = 0;
    virtual void DeviceText(const char*, Coord, Coord) = 0;
    virtual void DeviceBitmap(const char*, Coord, Coord) = 0;
    // lots more functions for drawing on windows...
protected:
    WindowImp();
};
```

Refined abstractions vary along one axis:

```cpp
void ApplicationWindow::DrawContents () {
    GetView()->DrawOn(this);
}

void IconWindow::DrawContents() {
    WindowImp* imp = GetWindowImp();
    if (imp != 0) {
        imp->DeviceBitmap(_bitmapName, 0.0, 0.0);
    }
}
```
Other variations: "A `TransientWindow` may need to communicate with the window that created it during the dialog... A `PaletteWindow` always floats above other windows. An `IconDockWindow` holds `IconWindow`s and arranges them neatly."

The abstraction translates, the implementor executes:

```cpp
void Window::DrawRect (const Point& p1, const Point& p2) {
    WindowImp* imp = GetWindowImp();
    imp->DeviceRect(p1.X(), p1.Y(), p2.X(), p2.Y());
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

Obtaining the right implementor, lazily, from an abstract factory:

```cpp
WindowImp* Window::GetWindowImp () {
    if (_imp == 0) {
        _imp = WindowSystemFactory::Instance()->MakeWindowImp();
    }
    return _imp;
}
```
- "For simplicity, we've made it a **Singleton** and have let the `Window` class access the factory directly."

## Known Uses
- **ET++** — `WindowImp` is called `WindowPort`, with `XWindowPort` and `SunWindowPort`. The `Window` gets its implementor from an abstract factory called `WindowSystem`.
  - **A notable extension**: "The ET++ Window/WindowPort design **extends** the Bridge pattern in that the WindowPort also keeps **a reference back to the Window**. The WindowPort implementor class uses this reference to notify Window about WindowPort-specific events: the arrival of input events, window resizes, etc."
- **Coplien and Stroustrup** on Handle classes — "Their examples emphasize **memory management** issues like sharing string representations and support for variable-sized objects. **Our focus is more on supporting independent extension** of both an abstraction and its implementation."
- **libg++** — `Set` is the abstraction; `LinkedList` and `HashTable` are concrete implementors; `LinkedSet` and `HashSet` bridge between them. "This is an example of a **degenerate bridge**, because there's no abstract Implementor class."
- **NeXT AppKit `NXImage`/`NXImageRep`** — "The optimal display of an image depends on the properties of a display device, specifically its color capabilities and its resolution. **Without help from AppKit, developers would have to determine which implementation to use under various circumstances in every application.**" Subclasses include `NXEPSImageRep`, `NXCachedImageRep`, `NXBitMapImageRep`. "`NXImage` is even capable of **converting one implementation to another** if necessary. The interesting aspect of this Bridge variant is that **`NXImage` can store more than one `NXImageRep` implementation at a time**."

## Related Patterns
- "An **Abstract Factory** can create and configure a particular Bridge."
- "The **Adapter** pattern is geared toward making unrelated classes work together. **It is usually applied to systems *after* they're designed.** Bridge, on the other hand, is used **up-front** in a design to let abstractions and implementations vary independently."

## Connects To
- **Ch 2 (Case Study, §2.6)**: the same `Window`/`WindowImp` design, derived from the problem — including why Abstract Factory alone fails for window systems.
- **Ch 1**: causes of redesign #3 (platform dependence) and #4 (representation dependence).
- **Adapter** (similar structure, different intent and timing), **Abstract Factory**, **Singleton**
