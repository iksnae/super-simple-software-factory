# Mediator
*Object Behavioral · GoF p. 273*

## Intent
> **Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly, and it lets you vary their interaction independently.**

## Motivation
"Object-oriented design encourages the distribution of behavior among objects. Such distribution can result in an object structure with many connections; **in the worst case, every object ends up knowing about every other**."

**The paradox**: "**Though partitioning a system into many objects generally enhances reusability, proliferating interconnections tend to reduce it again.** Lots of interconnections make it less likely that an object can work without the support of others — **the system acts as though it were monolithic**. Moreover, it can be difficult to change the system's behavior in any significant way, since behavior is distributed among many objects. **As a result, you may be forced to define many subclasses to customize the system's behavior.**"

The dialog box example: "a button gets **disabled** when a certain entry field is empty. Selecting an entry in a **list box** might change the contents of an entry field. Conversely typing text into the entry field might automatically **select** one or more corresponding entries in the list box."

**And the reuse failure that follows**: "Different dialog boxes will have different dependencies between widgets. So even though dialogs display the **same kinds of widgets, they can't simply reuse stock widget classes**; they have to be customized to reflect dialog-specific dependencies. **Customizing them individually by subclassing will be tedious, since many classes are involved.**"

The solution: "A mediator is responsible for **controlling and coordinating** the interactions of a group of objects... **The objects only know the mediator, thereby reducing the number of interconnections.**"

**The four-step interaction** when a list box selection changes:
1. "The list box tells its director that it's changed."
2. "The director gets the selection from the list box."
3. "The director passes the selection to the entry field."
4. "Now that the entry field contains some text, the director **enables button(s)** for initiating an action (e.g., 'demibold,' 'oblique')."

"**Widgets communicate with each other only indirectly, through the director.** They don't have to know about each other; all they know is the director. Furthermore, **because the behavior is localized in one class, it can be changed or replaced by extending or replacing that class**."

## Applicability
Use Mediator when:
- "a set of objects communicate in **well-defined but complex** ways. The resulting interdependencies are **unstructured and difficult to understand**."
- "**reusing an object is difficult** because it refers to and communicates with many other objects."
- "a behavior that's distributed between several classes should be **customizable without a lot of subclassing**."

## Participants
- **Mediator** (`DialogDirector`) — defines an interface for communicating with Colleague objects.
- **ConcreteMediator** (`FontDialogDirector`) — "implements cooperative behavior by coordinating Colleague objects"; **knows and maintains its colleagues**.
- **Colleague classes** (`ListBox`, `EntryField`) — "each Colleague class **knows its Mediator object**"; "each colleague **communicates with its mediator whenever it would have otherwise communicated with another colleague**."

## Collaborations
- "Colleagues send and receive requests from a Mediator object. **The mediator implements the cooperative behavior by routing requests between the appropriate colleague(s).**"

## Consequences
1. **It limits subclassing.** "Changing this behavior requires subclassing **Mediator only**; Colleague classes can be reused as is."
2. **It decouples colleagues.** "You can vary and reuse Colleague and Mediator classes independently."
3. **It simplifies object protocols.** "A mediator replaces **many-to-many** interactions with **one-to-many** interactions between the mediator and its colleagues. One-to-many relationships are easier to understand, maintain, and extend."
4. **It abstracts how objects cooperate.** "Making mediation an independent concept and encapsulating it in an object lets you **focus on how objects interact apart from their individual behavior**."
5. ⚠️ **It centralizes control.** "**The Mediator pattern trades complexity of interaction for complexity in the mediator.** Because a mediator encapsulates protocols, it can become more complex than any individual colleague. **This can make the mediator itself a monolith that's hard to maintain.**"

## Implementation
1. **Omitting the abstract Mediator class.** "There's no need to define an abstract Mediator class when colleagues **work with only one mediator**."
2. **Colleague-Mediator communication** — two approaches:
   - **Observer**: "Colleague classes act as **Subjects**, sending notifications to the mediator whenever they change state. The mediator responds by propagating the effects of the change to other colleagues."
   - **A specialized notification interface**: "**Smalltalk/V for Windows uses a form of delegation: when communicating with the mediator, a colleague passes itself as an argument, allowing the mediator to identify the sender.**" (This is what the Sample Code does.)

## Sample Code

```cpp
class DialogDirector {
public:
    virtual ~DialogDirector();

    virtual void ShowDialog();
    virtual void WidgetChanged(Widget*) = 0;
protected:
    DialogDirector();
    virtual void CreateWidgets() = 0;
};
```
```cpp
class Widget {
public:
    Widget(DialogDirector*);
    virtual void Changed();
    virtual void HandleMouse(MouseEvent& event);
    // ...
private:
    DialogDirector* _director;
};

void Widget::Changed () {
    _director->WidgetChanged(this);
}
```
- **The whole colleague-side protocol is those three lines.** "The widget **passes a reference to itself** as an argument to `WidgetChanged` to let the director identify the widget that changed."

```cpp
void Button::HandleMouse (MouseEvent& event) {
    // ...
    Changed();
}
```

```cpp
class FontDialogDirector : public DialogDirector {
public:
    FontDialogDirector();
    virtual ~FontDialogDirector();

    virtual void WidgetChanged(Widget*);
protected:
    virtual void CreateWidgets();
private:
    Button* _ok;
    Button* _cancel;
    ListBox* _fontList;
    EntryField* _fontName;
};

void FontDialogDirector::CreateWidgets () {
    _ok = new Button(this);
    _cancel = new Button(this);
    _fontList = new ListBox(this);
    _fontName = new EntryField(this);

    // fill the listBox with the available font names
    // assemble the widgets in the dialog
}
```

**All of the dialog's interaction logic, in one method:**

```cpp
void FontDialogDirector::WidgetChanged (Widget* theChangedWidget) {
    if (theChangedWidget == _fontList) {
        _fontName->SetText(_fontList->GetSelection());
    } else if (theChangedWidget == _ok) {
        // apply font change and dismiss dialog
        // ...
    } else if (theChangedWidget == _cancel) {
        // dismiss dialog
    }
}
```
- ⚠️ **And GoF names the cost immediately**: "**The complexity of `WidgetChanged` increases proportionally with the complexity of the dialog.** Large dialogs are undesirable for other reasons, of course, but **mediator complexity might mitigate the pattern's benefits in other applications**."

## Known Uses
- **ET++** and **THINK C** — "use director-like objects in dialogs as mediators between widgets."
- **Smalltalk/V for Windows** — "the application architecture... is based on a mediator structure. An application consists of a `Window` containing a set of **panes**... **These panes can be used without subclassing.** An application developer only subclasses from **`ViewManager`**, a class that's responsible for doing inter-pane coordination... **Panes don't refer to each other directly.**"
  - The event mechanism: "A pane generates an **event** when it wants to get information from the mediator or when it wants to inform the mediator that something significant happened. An event defines a **symbol** (e.g., `#select`)... To handle the event, the view manager **registers a method selector** with the pane."

```smalltalk
self addSubpane: (ListPane new
    paneName: 'myListPane';
    owner: self;
    when: #select perform: #listSelect:).
```

- **`ChangeManager`** (from the Observer pattern) — "mediates between subjects and observers to **avoid redundant updates**. When an object changes, it notifies the `ChangeManager`, which in turn coordinates the update by notifying the object's dependents."
- **Unidraw's `CSolver`** — "enforces **connectivity constraints** between 'connectors.' Objects in graphical editors can appear to **stick to one another**... useful in applications that maintain connectivity automatically, like **diagram editors and circuit design systems**. `CSolver` is a mediator between connectors. It solves the connectivity constraints and updates the connectors' positions."

## Related Patterns
- "**Facade** differs from Mediator in that it abstracts a subsystem of objects to provide a more convenient interface. **Its protocol is unidirectional**; that is, Facade objects make requests of the subsystem classes but not vice versa. In contrast, **Mediator enables cooperative behavior that colleague objects don't or can't provide, and the protocol is multidirectional.**"
- "Colleagues can communicate with the mediator using the **Observer** pattern."

## Connects To
- **Ch 5 (Behavioral Patterns)**: "**Peers could maintain explicit references to each other, but that would increase their coupling. In the extreme, every object would know about every other.** The Mediator pattern avoids this by introducing a mediator object between peers."
- **Ch 1**: cause of redesign #6 — tight coupling.
- **Facade** (the pattern most often confused with it), **Observer**
