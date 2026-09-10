# Chain of Responsibility
*Object Behavioral · GoF p. 223*

## Intent
> **Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it.**

## Motivation
A context-sensitive help facility. "The help that's provided depends on the part of the interface that's selected **and its context**; for example, a button widget in a dialog box might have different help information than a similar button in the main window. **If no specific help information exists for that part of the interface, then the help system should display a more general help message about the immediate context** — the dialog box as a whole."

"Hence it's natural to organize help information according to its **generality — from the most specific to the most general**."

**The problem**: "the object that ultimately provides the help **isn't known explicitly** to the object (e.g., the button) that initiates the help request."

**The mechanism**: "The first object in the chain receives the request and either handles it or forwards it to the next candidate... The object that made the request has **no explicit knowledge of who will handle it — we say the request has an implicit receiver**."

The worked scenario: the user clicks help on a "Print" button. "neither `aPrintButton` nor `aPrintDialog` handles the request; **it stops at `anApplication`, which can handle it or ignore it**."

Note the design freedom in the Handler class: "`HelpHandler` can be the **parent class** for candidate object classes, or it can be defined as a **mixin class**."

## Applicability
Use Chain of Responsibility when:
- "**more than one object may handle a request, and the handler isn't known a priori.** The handler should be ascertained automatically."
- "you want to issue a request to one of several objects **without specifying the receiver explicitly**."
- "the set of objects that can handle a request should be **specified dynamically**."

## Participants
- **Handler** (`HelpHandler`) — defines an interface for handling requests; *(optional)* implements the successor link.
- **ConcreteHandler** (`PrintButton`, `PrintDialog`) — "handles requests it is responsible for"; can access its successor; "**if the ConcreteHandler can handle the request, it does so; otherwise it forwards the request to its successor**."
- **Client** — initiates the request to a ConcreteHandler object on the chain.

## Collaborations
- "When a client issues a request, the request **propagates along the chain** until a ConcreteHandler object takes responsibility for handling it."

## Consequences
1. **Reduced coupling.** "An object only has to know that a request will be handled '**appropriately**.' Both the receiver and the sender have no explicit knowledge of each other, and **an object in the chain doesn't have to know about the chain's structure**."
   - "Instead of objects maintaining references to **all** candidate receivers, they keep a **single reference to their successor**."
2. **Added flexibility in assigning responsibilities to objects.** "You can add or change responsibilities for handling a request by **adding to or otherwise changing the chain at run-time**. You can combine this with subclassing to specialize handlers statically."
3. ⚠️ **Receipt isn't guaranteed.** "Since a request has no explicit receiver, **there's no guarantee it'll be handled** — the request can **fall off the end of the chain** without ever being handled. A request can also go unhandled when the chain is not configured properly."

## Implementation
1. **Implementing the successor chain** — two ways: **define new links**, or **use existing links**.
   - "often you can use existing object references to form the successor chain. For example, **parent references in a part-whole hierarchy** can define a part's successor. A widget structure might already have such links."
   - The trade-off: "Using existing links works well when the links support the chain you need. **It saves you from defining links explicitly, and it saves space.** But if the structure doesn't reflect the chain of responsibility your application requires, then you'll have to **define redundant links**."
2. **Connecting successors.** "the Handler not only defines the interface for the requests but usually **maintains the successor as well**. That lets the handler provide a **default implementation** of `HandleRequest` that forwards the request to the successor (if any). If a ConcreteHandler subclass isn't interested in the request, **it doesn't have to override the forwarding operation**."

```cpp
class HelpHandler {
public:
    HelpHandler(HelpHandler* s) : _successor(s) { }
    virtual void HandleHelp();
private:
    HelpHandler* _successor;
};

void HelpHandler::HandleHelp () {
    if (_successor) {
        _successor->HandleHelp();
    }
}
```
3. **Representing requests** — three options, in increasing flexibility and decreasing safety:

| Representation | Trade-off |
|---|---|
| **Hard-coded operation** (`HandleHelp`) | "convenient and safe, but you can forward **only the fixed set of requests** that the Handler class defines" |
| **Request code parameter** (integer or string) | "supports an open-ended set of requests. The only requirement is that sender and receiver **agree on how the request should be encoded**." But: "requires **conditional statements** for dispatching... there's **no type-safe way to pass parameters**, so they must be packed and unpacked manually" |
| **Request objects** | "bundle request parameters... new kinds of requests can be defined by subclassing. **Handlers must know the kind of request** to access these parameters" |

```cpp
void Handler::HandleRequest (Request* theRequest) {
    switch (theRequest->GetKind()) {
    case Help:
        // cast argument to appropriate type
        HandleHelp((HelpRequest*) theRequest);
        break;
    case Print:
        HandlePrint((PrintRequest*) theRequest);
        // ...
        break;
    default:
        // ...
        break;
    }
}
```
```cpp
void ExtendedHandler::HandleRequest (Request* theRequest) {
    switch (theRequest->GetKind()) {
    case Preview:
        // handle the Preview request
        break;
    default:
        // let Handler handle other requests
        Handler::HandleRequest(theRequest);
    }
}
```
- "In this way, subclasses effectively **extend (rather than override)** the `HandleRequest` operation."
4. **Automatic forwarding in Smalltalk.** "`doesNotUnderstand`... can be overridden to forward the message to an object's successor. Thus it isn't necessary to implement forwarding manually; **the class handles only the request in which it's interested, and it relies on `doesNotUnderstand` to forward all others**."

## Sample Code

The example deliberately mixes both link strategies: "We'll use **existing parent references** in the widget hierarchy to propagate requests between widgets, and we'll define **a reference in the Handler class** to propagate help requests between nonwidgets."

```cpp
typedef int Topic;
const Topic NO_HELP_TOPIC = -1;

class HelpHandler {
public:
    HelpHandler(HelpHandler* = 0, Topic = NO_HELP_TOPIC);
    virtual bool HasHelp();
    virtual void SetHandler(HelpHandler*, Topic);
    virtual void HandleHelp();
private:
    HelpHandler* _successor;
    Topic _topic;
};

HelpHandler::HelpHandler (HelpHandler* h, Topic t)
    : _successor(h), _topic(t) { }

bool HelpHandler::HasHelp () {
    return _topic != NO_HELP_TOPIC;
}

void HelpHandler::HandleHelp () {
    if (_successor != 0) {
        _successor->HandleHelp();
    }
}
```

Every widget is a handler — "since **all user interface elements can have help associated with them**. (We could have used a mixin-based implementation just as well.)"

```cpp
class Widget : public HelpHandler {
protected:
    Widget(Widget* parent, Topic t = NO_HELP_TOPIC);
private:
    Widget* _parent;
};

Widget::Widget (Widget* w, Topic t) : HelpHandler(w, t) {
    _parent = w;
}
```

The handler idiom, repeated identically at each level — *do I have help? if not, delegate*:

```cpp
void Button::HandleHelp () {
    if (HasHelp()) {
        // offer help on the button
    } else {
        HelpHandler::HandleHelp();
    }
}

void Dialog::HandleHelp () {
    if (HasHelp()) {
        // offer help on the dialog
    } else {
        HelpHandler::HandleHelp();
    }
}
```
```cpp
class Application : public HelpHandler {
public:
    Application(Topic t) : HelpHandler(0, t) { }
    virtual void HandleHelp();
    // application-specific operations...
};

void Application::HandleHelp () {
    // show a list of help topics
}
```
- "**The application is not a widget**, so `Application` is subclassed directly from `HelpHandler`." At the end of the chain it "can supply information on the application in general, or it can offer a list of different help topics."

Building the chain — specific to general, right to left:

```cpp
const Topic PRINT_TOPIC = 1;
const Topic PAPER_ORIENTATION_TOPIC = 2;
const Topic APPLICATION_TOPIC = 3;

Application* application = new Application(APPLICATION_TOPIC);
Dialog* dialog = new Dialog(application, PRINT_TOPIC);
Button* button = new Button(dialog, PAPER_ORIENTATION_TOPIC);
```
```cpp
button->HandleHelp();
```
- "Note that **any `HelpHandler` class could be made the successor of `Dialog`**. Moreover, **its successor could be changed dynamically**. So no matter where a dialog is used, you'll get the proper context-dependent help information for it."

## Known Uses
- **Event handling in class libraries** — "They use different names for the Handler class, but the idea is the same: When the user clicks the mouse or presses a key, an event gets generated and passed along the chain."

| Library | Name for the Handler |
|---|---|
| MacApp, ET++ | `EventHandler` |
| Symantec TCL | `Bureaucrat` |
| NeXT AppKit | `Responder` |

- **Unidraw** — `Command` objects encapsulating requests to `Component` and `ComponentView`. "A component or a component view may **forward command interpretation to its parent**, which may in turn forward it to its parent, and so on, thereby forming a chain of responsibility."
- **ET++ graphical update** — "A graphical object calls `InvalidateRect` whenever it must update a part of its appearance. **A graphical object can't handle `InvalidateRect` by itself, because it doesn't know enough about its context.** For example, a graphical object can be enclosed in objects like `Scrollers` or `Zoomers` that transform its coordinate system... Therefore the default implementation forwards the request to the enclosing container. **The last object in the forwarding chain is a `Window` instance. By the time `Window` receives the request, the invalidation rectangle is guaranteed to be transformed properly.**"

## Related Patterns
- "Chain of Responsibility is often applied in conjunction with **Composite**. There, **a component's parent can act as its successor**."

## Connects To
- **Ch 5 (Behavioral Patterns)**: "Chain of Responsibility provides even looser coupling [than Mediator]... **The number of candidates is open-ended, and you can select which candidates participate in the chain at run-time.**"
- **Ch 1**: causes of redesign #2 (dependence on specific operations), #6 (tight coupling), #7 (extending by subclassing).
- **Ch 12 (Composite)**: explicit parent references "help support the Chain of Responsibility pattern."
- **Composite, Command**
