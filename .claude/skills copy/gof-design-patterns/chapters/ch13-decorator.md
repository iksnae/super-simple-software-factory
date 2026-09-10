# Decorator
*Object Structural · Also Known As: **Wrapper** · GoF p. 175*

## Intent
> **Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.**

## Motivation
"Sometimes we want to add responsibilities to **individual objects, not to an entire class**."

"One way to add responsibilities is with inheritance. **Inheriting a border from another class puts a border around every subclass instance.** This is inflexible, however, because the choice of border is made **statically**. A client can't control how and when to decorate the component."

"A more flexible approach is to **enclose the component in another object** that adds the border. The enclosing object is called a **decorator**. The decorator **conforms to the interface of the component it decorates so that its presence is transparent** to the component's clients... **Transparency lets you nest decorators recursively**, thereby allowing an unlimited number of added responsibilities."

Decorators may also add operations of their own: "`ScrollDecorator`'s `ScrollTo` operation lets other objects scroll the interface **if they know there happens to be a `ScrollDecorator`** in the interface. The important aspect of this pattern is that it lets decorators appear **anywhere** a `VisualComponent` can."

## Applicability
Use Decorator:
- "to add responsibilities to individual objects **dynamically and transparently**, that is, without affecting other objects."
- "for responsibilities that can be **withdrawn**."
- "when **extension by subclassing is impractical**. Sometimes a large number of independent extensions are possible and would produce an **explosion of subclasses** to support every combination. Or **a class definition may be hidden or otherwise unavailable for subclassing**."

## Participants
- **Component** (`VisualComponent`) — defines the interface for objects that can have responsibilities added dynamically.
- **ConcreteComponent** (`TextView`) — defines an object to which additional responsibilities can be attached.
- **Decorator** — maintains a reference to a Component object and defines an interface **conforming to Component's**.
- **ConcreteDecorator** (`BorderDecorator`, `ScrollDecorator`) — adds responsibilities to the component.

## Collaborations
- "Decorator forwards requests to its Component object. It may optionally perform additional operations **before and after** forwarding."

## Consequences
**Two benefits:**
1. **More flexibility than static inheritance.** "responsibilities can be added and removed **at run-time** simply by attaching and detaching them. In contrast, inheritance requires creating a new class for each additional responsibility (e.g., `BorderedScrollableTextView`, `BorderedTextView`)."
   - "Decorators also make it easy to **add a property twice**. For example, to give a `TextView` a **double border**, simply attach two `BorderDecorator`s. **Inheriting from a Border class twice is error-prone at best.**"
2. **Avoids feature-laden classes high up in the hierarchy.** "Decorator offers a **pay-as-you-go** approach... Instead of trying to support all foreseeable features in a complex, customizable class, you can define a simple class and add functionality incrementally... **an application needn't pay for features it doesn't use**... Extending a complex class tends to expose details unrelated to the responsibilities you're adding."

**Two liabilities:**
3. ⚠️ **A decorator and its component aren't identical.** "A decorator acts as a transparent enclosure. But **from an object identity point of view, a decorated component is not identical to the component itself**. Hence you shouldn't rely on object identity when you use decorators."
4. ⚠️ **Lots of little objects.** "systems composed of lots of little objects that all look alike. The objects differ only in **the way they are interconnected**, not in their class or in the value of their variables. Although these systems are easy to customize by those who understand them, **they can be hard to learn and debug**."

## Implementation
1. **Interface conformance.** "A decorator object's interface must conform to the interface of the component it decorates. ConcreteDecorator classes must therefore inherit from a common class (at least in C++)."
2. **Omitting the abstract Decorator class.** "There's no need to define an abstract Decorator class **when you only need to add one responsibility**. That's often the case when you're dealing with an **existing class hierarchy** rather than designing a new one."
3. **Keeping Component classes lightweight.** "it should focus on **defining an interface, not on storing data**... otherwise the complexity of the Component class might make the decorators **too heavyweight to use in quantity**."
4. **Changing the skin of an object versus changing its guts** — the key comparison with Strategy:

| | **Decorator** | **Strategy** |
|---|---|---|
| Metaphor | Changes the **skin** | Changes the **guts** |
| Component's awareness | "the component **doesn't have to know anything about its decorators**; the decorators are transparent to the component" | "the component itself **knows about possible extensions**. So it has to reference and maintain the corresponding strategies" |
| Interface constraint | "a decorator's interface **must conform to the component's**" | "a strategy can have its **own specialized interface**... which means the strategy can be **lightweight even if the Component class is heavyweight**" |
| Extension cost | Add a new decorator class | "might require **modifying the component** to accommodate new extensions" |
| When to prefer | Component is lightweight | "Component class is **intrinsically heavyweight**, thereby making the Decorator pattern too costly to apply" |

- **The real-world case**: "In **MacApp 3.0** and **Bedrock**, graphical components (called 'views') maintain a list of '**adorner**' objects that can attach additional adornments like borders... **MacApp and Bedrock must use this approach because the View class is heavyweight. It would be too expensive to use a full-fledged View just to add a border.**"
- And the same mechanism for events: "a view maintains a list of '**behavior**' objects that can modify and intercept events. The view gives each of the registered behavior objects a chance to handle the event before nonregistered behaviors, **effectively overriding them**."

## Sample Code

```cpp
class VisualComponent {
public:
    VisualComponent();

    virtual void Draw();
    virtual void Resize();
    // ...
};
```
```cpp
class Decorator : public VisualComponent {
public:
    Decorator(VisualComponent*);

    virtual void Draw();
    virtual void Resize();
    // ...
private:
    VisualComponent* _component;
};

void Decorator::Draw () {
    _component->Draw();
}

void Decorator::Resize () {
    _component->Resize();
}
```
- "For **each** operation in `VisualComponent`'s interface, `Decorator` defines a default implementation that passes the request on."

```cpp
class BorderDecorator : public Decorator {
public:
    BorderDecorator(VisualComponent*, int borderWidth);

    virtual void Draw();
private:
    void DrawBorder(int);
private:
    int _width;
};

void BorderDecorator::Draw () {
    Decorator::Draw();
    DrawBorder(_width);
}
```
- "The subclass **inherits all other operation implementations** from `Decorator`."

Composing them:

```cpp
Window* window = new Window;
TextView* textView = new TextView;

window->SetContents(textView);
```
```cpp
window->SetContents(
    new BorderDecorator(
        new ScrollDecorator(textView), 1
    )
);
```
- "Because `Window` accesses its contents through the `VisualComponent` interface, **it's unaware of the decorator's presence**. You, as the client, **can still keep track of the text view** if you have to interact with it directly, for example, when you need to invoke operations that aren't part of the `VisualComponent` interface. **Clients that rely on the component's identity should refer to it directly as well.**"

## Known Uses
- **UI toolkits** — InterViews, ET++, ObjectWorks\Smalltalk.
- **More exotic applications**:
  - **`DebuggingGlyph`** (InterViews) — "prints out debugging information **before and after** it forwards a layout request to its component. This trace information can be used to analyze and debug the layout behavior of objects in a complex composition."
  - **`PassivityWrapper`** (ParcPlace Smalltalk) — "can **enable or disable** user interactions with the component."
- **ET++ streams** — the demonstration that Decorator is "by no means limited to graphical user interfaces." A `Stream` abstract class with `MemoryStream` and `FileStream` subclasses, plus the desire to **compress** stream data (run-length encoding, Lempel-Ziv) and **reduce it to 7-bit ASCII** for transmission.
  - The mechanism: "`Stream` maintains an internal buffer and provides operations for storing data (`PutInt`, `PutString`). Whenever the buffer is full, `Stream` calls the abstract operation **`HandleBufferFull`**... `StreamDecorator` subclasses override `HandleBufferFull` and perform additional actions before calling `StreamDecorator`'s `HandleBufferFull`."

```cpp
Stream* aStream = new CompressingStream(
    new ASCII7Stream(
        new FileStream("aFileName")
    )
);
aStream->PutInt(12);
aStream->PutString("aString");
```

## Related Patterns
- "**Adapter**: A decorator only changes an object's **responsibilities, not its interface**; an adapter will give an object a **completely new interface**."
- "**Composite**: A decorator can be viewed as a **degenerate composite with only one component**. However, a decorator **adds additional responsibilities** — it isn't intended for object aggregation."
- "**Strategy**: A decorator lets you change the **skin** of an object; a strategy lets you change the **guts**."

## Connects To
- **Ch 1 (MVC)**: Decorator adds scrolling to a view.
- **Ch 2 (Case Study, §2.4)**: `MonoGlyph` and transparent enclosure — the pattern derived from the problem, including why embellishment composes exactly one child.
- **Ch 1**: causes of redesign #7 (extending by subclassing) and #8 (can't alter classes).
- **Adapter, Composite, Strategy, Proxy**
