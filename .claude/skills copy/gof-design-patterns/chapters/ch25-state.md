# State
*Object Behavioral · Also Known As: **Objects for States** · GoF p. 305*

## Intent
> **Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.**

## Motivation
"Consider a class `TCPConnection` that represents a network connection. A `TCPConnection` object can be in one of several different states: **Established, Listening, Closed**. When a `TCPConnection` object receives requests from other objects, it **responds differently depending on its current state**. For example, the effect of an `Open` request depends on whether the connection is in its `Closed` state or its `Established` state."

"The key idea in this pattern is to introduce an **abstract class called `TCPState`** to represent the states of the network connection. The `TCPState` class declares an interface common to all classes that represent different operational states. **Subclasses of `TCPState` implement state-specific behavior.**"

"`TCPConnection` maintains a state object... and **delegates all state-specific requests to this state object**. **Whenever the connection changes state, the `TCPConnection` object changes the state object it uses.** When the connection goes from established to closed, `TCPConnection` will replace its `TCPEstablished` instance with a `TCPClosed` instance."

## Applicability
Use State in either of these cases:
- "An object's behavior **depends on its state**, and it must change its behavior at run-time depending on that state."
- "Operations have **large, multipart conditional statements** that depend on the object's state. This state is usually represented by one or more **enumerated constants**. **Often, several operations will contain this same conditional structure.** The State pattern puts each branch of the conditional in a separate class."

## Participants
- **Context** (`TCPConnection`) — "defines the interface of interest to clients"; "maintains an instance of a ConcreteState subclass that defines the **current** state."
- **State** (`TCPState`) — "defines an interface for encapsulating the behavior associated with a particular state of the Context."
- **ConcreteState subclasses** (`TCPEstablished`, `TCPListen`, `TCPClosed`) — "each subclass implements a behavior associated with a state of the Context."

## Collaborations
- "Context delegates state-specific requests to the current ConcreteState object."
- "A context **may pass itself as an argument** to the State object handling the request. This lets the State object access the context if necessary."
- "Context is the **primary interface for clients**. Clients can configure a context with State objects. **Once a context is configured, its clients don't have to deal with the State objects directly.**"
- ⚠️ "**Either Context or the ConcreteState subclasses can decide which state succeeds another** and under what circumstances." (See Implementation issue 1.)

## Consequences
1. **It localizes state-specific behavior and partitions behavior for different states.** "Because all state-specific code lives in a State subclass, **new states and transitions can be added easily by defining new subclasses**."
   - The alternative it replaces: "use **data values** to define internal states and have Context operations check the data explicitly. But then we'd have **look-alike conditional or case statements scattered throughout Context's implementation**. Adding a new state could require changing several operations."
   - ⚠️ The cost it introduces: "the pattern **distributes behavior for different states across several State subclasses**. This **increases the number of classes and is less compact** than a single class. **But such distribution is actually good if there are many states**, which would otherwise necessitate large conditional statements."
   - "**Like long procedures, large conditional statements are undesirable. They're monolithic and tend to make the code less explicit**... The logic that determines the state transitions doesn't reside in monolithic `if` or `switch` statements but instead is **partitioned between the State subclasses**. **Encapsulating each state transition and action in a class elevates the idea of an execution state to full object status.**"
2. **It makes state transitions explicit.** "When an object defines its current state solely in terms of internal data values, its **state transitions have no explicit representation; they only show up as assignments to some variables**."
   - "State objects can **protect the Context from inconsistent internal states**, because **state transitions are atomic from the Context's perspective — they happen by rebinding one variable** (the Context's State object variable), **not several**."
3. **State objects can be shared.** "If State objects have **no instance variables** — that is, the state they represent is **encoded entirely in their type** — then contexts can share a State object. When states are shared in this way, they are essentially **flyweights** (see Flyweight (195)) **with no intrinsic state, only behavior**."

## Implementation
1. ⚠️ **Who defines the state transitions?** "The State pattern **does not specify** which participant defines the criteria for state transitions. **If the criteria are fixed, then they can be implemented entirely in the Context.** It is generally **more flexible and appropriate, however, to let the State subclasses themselves specify their successor state** and when to make the transition. This requires adding an interface to the Context that lets State objects **set the Context's current state explicitly**."
   - The trade: "Decentralizing the transition logic makes it easy to modify or extend the logic by defining new State subclasses. **A disadvantage of decentralization is that one State subclass will have knowledge of at least one other, which introduces implementation dependencies between subclasses.**"
2. **A table-based alternative.** Cargill's approach: "**He uses tables to map inputs to state transitions.** For each state, a table maps every possible input to a succeeding state. In effect, this approach **converts conditional code (and virtual functions, in the case of the State pattern) into a table look-up.**"

| | Table-driven |
|---|---|
| **Advantage** | "**regularity**: You can change the transition criteria by **modifying data instead of changing program code**" |
| ⚠️ | "A table look-up is often **less efficient** than a (virtual) function call" |
| ⚠️ | "Putting transition logic into a uniform, tabular format makes the **transition criteria less explicit and therefore harder to understand**" |
| ⚠️ | "It's usually **difficult to add actions** to accompany the state transitions. The table-driven approach captures the states and their transitions, but it must be augmented to perform arbitrary computation on each transition" |

   - **The distinction to remember**: "**The State pattern models state-specific *behavior*, whereas the table-driven approach focuses on defining state *transitions*.**"
3. **Creating and destroying State objects.** Two strategies:

| Strategy | Preferable when |
|---|---|
| **Create on demand, destroy after** | "the states that will be entered **aren't known at run-time**, and contexts change state **infrequently**"; "avoids creating objects that won't be used, which is important if the State objects **store a lot of information**" |
| **Create ahead of time, never destroy** | "state changes occur **rapidly**... **Instantiation costs are paid once up-front, and there are no destruction costs at all.** This approach might be inconvenient, though, because **the Context must keep references to all states that might be entered**" |

4. **Using dynamic inheritance.** "Changing the behavior for a particular request could be accomplished by **changing the object's class at run-time, but this is not possible in most object-oriented programming languages**. Exceptions include **Self** and other **delegation-based languages**... **Changing the delegation target at run-time effectively changes the inheritance structure.**"

## Sample Code
A simplified TCP protocol.

```cpp
class TCPOctetStream;
class TCPState;

class TCPConnection {
public:
    TCPConnection();

    void ActiveOpen();
    void PassiveOpen();
    void Close();

    void Send();
    void Acknowledge();
    void Synchronize();

    void ProcessOctet(TCPOctetStream*);
private:
    friend class TCPState;
    void ChangeState(TCPState*);
private:
    TCPState* _state;
};
```

```cpp
class TCPState {
public:
    virtual void Transmit(TCPConnection*, TCPOctetStream*);
    virtual void ActiveOpen(TCPConnection*);
    virtual void PassiveOpen(TCPConnection*);
    virtual void Close(TCPConnection*);
    virtual void Synchronize(TCPConnection*);
    virtual void Acknowledge(TCPConnection*);
    virtual void Send(TCPConnection*);
protected:
    void ChangeState(TCPConnection*, TCPState*);
};
```
- "**The class `TCPState` duplicates the state-changing interface of `TCPConnection`.** Each `TCPState` operation takes a `TCPConnection` instance as a parameter, letting `TCPState` access data from `TCPConnection` and change the connection's state."

```cpp
TCPConnection::TCPConnection () {
    _state = TCPClosed::Instance();
}

void TCPConnection::ChangeState (TCPState* s) {
    _state = s;
}

void TCPConnection::ActiveOpen () {
    _state->ActiveOpen(this);
}

void TCPConnection::PassiveOpen () {
    _state->PassiveOpen(this);
}

void TCPConnection::Close () {
    _state->Close(this);
}

void TCPConnection::Acknowledge () {
    _state->Acknowledge(this);
}

void TCPConnection::Synchronize () {
    _state->Synchronize(this);
}
```
- Every Context operation is **one line of delegation**. The constructor picks the initial state.

```cpp
void TCPState::Transmit (TCPConnection*, TCPOctetStream*) { }
void TCPState::ActiveOpen (TCPConnection*) { }
void TCPState::PassiveOpen (TCPConnection*) { }
void TCPState::Close (TCPConnection*) { }
void TCPState::Synchronize (TCPConnection*) { }

void TCPState::ChangeState (TCPConnection* t, TCPState* s) {
    t->ChangeState(s);
}
```
- "`TCPState` implements **default behavior for all requests** delegated to it" — empty bodies mean an invalid request in a given state is simply ignored. "**`TCPState` is declared a friend of `TCPConnection`** to give it privileged access to this operation."

```cpp
class TCPEstablished : public TCPState {
public:
    static TCPState* Instance();

    virtual void Transmit(TCPConnection*, TCPOctetStream*);
    virtual void Close(TCPConnection*);
};

class TCPListen : public TCPState {
public:
    static TCPState* Instance();

    virtual void Send(TCPConnection*);
    // ...
};

class TCPClosed : public TCPState {
public:
    static TCPState* Instance();

    virtual void ActiveOpen(TCPConnection*);
    virtual void PassiveOpen(TCPConnection*);
    // ...
};
```
- "`TCPState` subclasses **maintain no local state, so they can be shared**, and only one instance of each is required... **This makes each `TCPState` subclass a Singleton** (see Singleton (127))." Each subclass declares **only the operations valid in that state**.

```cpp
void TCPClosed::ActiveOpen (TCPConnection* t) {
    // send SYN, receive SYN, ACK, etc.

    ChangeState(t, TCPEstablished::Instance());
}

void TCPClosed::PassiveOpen (TCPConnection* t) {
    ChangeState(t, TCPListen::Instance());
}

void TCPEstablished::Close (TCPConnection* t) {
    // send FIN, receive ACK of FIN

    ChangeState(t, TCPListen::Instance());
}

void TCPEstablished::Transmit (
    TCPConnection* t, TCPOctetStream* o
) {
    t->ProcessOctet(o);
}

void TCPListen::Send (TCPConnection* t) {
    // send SYN, receive SYN, ACK, etc.

    ChangeState(t, TCPEstablished::Instance());
}
```
- **The punchline**: "After performing state-specific work, these operations call `ChangeState`... **`TCPConnection` itself doesn't know a thing about the TCP connection protocol; it's the `TCPState` subclasses that define each state transition and action in TCP.**"

## Worked Example
**Drawing-editor tools as states.**

"Most popular interactive drawing programs provide '**tools**' for performing operations by direct manipulation... **The user thinks of this activity as picking up a tool and wielding it, but in reality the editor's behavior changes with the current tool**: When a drawing tool is active we create shapes; when the selection tool is active we select shapes; and so forth."

The construction: "define an **abstract `Tool` class** from which to define subclasses that implement tool-specific behavior. **The drawing editor maintains a current `Tool` object and delegates requests to it. It replaces this object when the user chooses a new tool**, causing the behavior of the drawing editor to change accordingly."

- **HotDraw** — "the `DrawingController` class forwards the requests to the current `Tool` object."
- **Unidraw** — "the corresponding classes are `Viewer` and `Tool`."
- Why it pays: "**It allows clients to define new kinds of tools easily.**"

Note the mapping to the participants: `DrawingController` is the **Context**, `Tool` is the **State**, and each concrete tool is a **ConcreteState** — the same structure as `TCPConnection`/`TCPState`, in a domain that looks nothing like a network protocol.

## Known Uses
- **Johnson and Zweig** — "characterize the State pattern and its application to **TCP connection protocols**."
- **HotDraw** and **Unidraw** — the tool palettes described above.
- **Coplien's Envelope-Letter idiom** — "a technique for **changing an object's class at run-time**. **The State pattern is more specific, focusing on how to deal with an object whose behavior depends on its state.**"

## Related Patterns
- "The **Flyweight** pattern explains when and how State objects can be shared."
- "State objects are often **Singletons**."

## Connects To
- **Ch 5 (Behavioral Patterns)**: State "encapsulates the states of an object so that the object can **change its behavior when its state object changes**."
- **Ch 26 (Strategy)**: structurally identical — a Context delegating to a swappable object. The difference is intent: Strategy varies an **algorithm** chosen by the client; State varies **behavior driven by the object's own state**, and the state objects typically drive their own transitions.
- **Ch 15 (Flyweight)**, **Ch 8 (Singleton)**: how stateless ConcreteStates get shared.
- **Ch 1**: cause of redesign #3 — dependence on object representations/implementations expressed as conditionals.
