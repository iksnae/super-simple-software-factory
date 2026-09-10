# Facade
*Object Structural · GoF p. 185*

## Intent
> **Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.**

## Motivation
"Structuring a system into subsystems helps reduce complexity. A common design goal is to **minimize the communication and dependencies between subsystems**."

A compiler subsystem contains `Scanner`, `Parser`, `ProgramNode`, `BytecodeStream`, `ProgramNodeBuilder`. "Some specialized applications might need to access these classes directly. But **most clients of a compiler generally don't care about details like parsing and code generation; they merely want to compile some code.** For them, the powerful but low-level interfaces only complicate their task."

The `Compiler` class is the facade: "It **glues together the classes that implement compiler functionality without hiding them completely**. The compiler facade makes life easier for most programmers **without hiding the lower-level functionality from the few that need it**."

## Applicability
Use Facade when:
- "you want to provide a **simple interface to a complex subsystem**."
  - The reason subsystems get complex is telling: "**Most patterns, when applied, result in more and smaller classes.** This makes the subsystem more reusable and easier to customize, but it also becomes **harder to use for clients that don't need to customize it**. A facade can provide a simple default view... **Only clients needing more customizability will need to look beyond the facade.**"
- "there are **many dependencies between clients and the implementation classes** of an abstraction."
- "you want to **layer your subsystems**. Use a facade to define an entry point to each subsystem level. If subsystems are dependent, then you can simplify the dependencies between them by making them **communicate with each other solely through their facades**."

## Participants
- **Facade** (`Compiler`) — "knows which subsystem classes are responsible for a request"; delegates client requests to appropriate subsystem objects.
- **Subsystem classes** (`Scanner`, `Parser`, `ProgramNode`) — implement subsystem functionality; handle work assigned by the Facade; **"have no knowledge of the facade; that is, they keep no references to it."**

## Collaborations
- "Clients communicate with the subsystem by sending requests to Facade, which forwards them to the appropriate subsystem object(s). Although the subsystem objects perform the actual work, **the facade may have to do work of its own to translate its interface to subsystem interfaces**."

## Consequences
1. **It shields clients from subsystem components**, "reducing the number of objects that clients deal with."
2. **It promotes weak coupling between the subsystem and its clients.** "Often the components in a subsystem are strongly coupled. Weak coupling lets you vary the components of the subsystem without affecting its clients. Facades help layer a system... **They can eliminate complex or circular dependencies.**"
   - The compilation angle: "**Reducing compilation dependencies is vital in large software systems.** You want to save time by minimizing recompilation when subsystem classes change... A facade can also simplify **porting** systems to other platforms, because it's less likely that building one subsystem requires building all others."
3. **It doesn't prevent applications from using subsystem classes if they need to.** "Thus you can **choose between ease of use and generality**."

## Implementation
1. **Reducing client-subsystem coupling.** "making Facade an **abstract class with concrete subclasses** for different implementations of a subsystem... **This abstract coupling keeps clients from knowing which implementation of a subsystem is used.**"
   - "An alternative to subclassing is to **configure a Facade object with different subsystem objects**. To customize the facade, simply replace one or more of its subsystem objects."
2. **Public versus private subsystem classes.** "A subsystem is **analogous to a class** in that both have interfaces, and both encapsulate something — a class encapsulates state and operations, while a **subsystem encapsulates classes**."
   - "**The Facade class is part of the public interface, of course, but it's not the only part.** Other subsystem classes are usually public as well. For example, the classes `Parser` and `Scanner` in the compiler subsystem are part of the public interface."
   - "Making subsystem classes private would be useful, but **few object-oriented languages support it**. Both C++ and Smalltalk traditionally have had a global name space for classes. Recently, however, the C++ standardization committee added **name spaces** to the language, which will let you expose just the public subsystem classes."

## Sample Code

The subsystem — note that three other patterns are visible inside it:

```cpp
class Scanner {
public:
    Scanner(istream&);
    virtual ~Scanner();
    virtual Token& Scan();
private:
    istream& _inputStream;
};

class Parser {
public:
    Parser();
    virtual ~Parser();
    virtual void Parse(Scanner&, ProgramNodeBuilder&);
};
```
- "`Parser` calls back on `ProgramNodeBuilder` to build the parse tree incrementally. **These classes interact according to the Builder pattern.**"

```cpp
class ProgramNodeBuilder {
public:
    ProgramNodeBuilder();

    virtual ProgramNode* NewVariable(const char* variableName) const;
    virtual ProgramNode* NewAssignment(
        ProgramNode* variable, ProgramNode* expression) const;
    virtual ProgramNode* NewReturnStatement(ProgramNode* value) const;
    virtual ProgramNode* NewCondition(
        ProgramNode* condition,
        ProgramNode* truePart, ProgramNode* falsePart) const;
    // ...

    ProgramNode* GetRootNode();
private:
    ProgramNode* _node;
};
```
```cpp
class ProgramNode {
public:
    // program node manipulation
    virtual void GetSourcePosition(int& line, int& index);
    // ...

    // child manipulation
    virtual void Add(ProgramNode*);
    virtual void Remove(ProgramNode*);
    // ...

    virtual void Traverse(CodeGenerator&);
protected:
    ProgramNode();
};
```
- "**The `ProgramNode` hierarchy is an example of the Composite pattern.**"

```cpp
class CodeGenerator {
public:
    virtual void Visit(StatementNode*);
    virtual void Visit(ExpressionNode*);
    // ...
protected:
    CodeGenerator(BytecodeStream&);
protected:
    BytecodeStream& _output;
};
```
- "**The class `CodeGenerator` is a visitor.**" Subclasses include `StackMachineCodeGenerator` and `RISCCodeGenerator`.

```cpp
void ExpressionNode::Traverse (CodeGenerator& cg) {
    cg.Visit(this);

    ListIterator<ProgramNode*> i(_children);

    for (i.First(); !i.IsDone(); i.Next()) {
        i.CurrentItem()->Traverse(cg);
    }
}
```

**The facade** — the whole subsystem reduced to one method:

```cpp
class Compiler {
public:
    Compiler();
    virtual void Compile(istream&, BytecodeStream&);
};

void Compiler::Compile (istream& input, BytecodeStream& output) {
    Scanner scanner(input);
    ProgramNodeBuilder builder;
    Parser parser;

    parser.Parse(scanner, builder);

    RISCCodeGenerator generator(output);
    ProgramNode* parseTree = builder.GetRootNode();
    parseTree->Traverse(generator);
}
```

**And the design tension, stated honestly**: "This implementation **hard-codes the type of code generator** so that programmers aren't required to specify the target architecture. That might be reasonable if there's only ever one target architecture. If not... we might want to change the `Compiler` constructor to take a `CodeGenerator` parameter... The compiler facade can parameterize other participants such as `Scanner` and `ProgramNodeBuilder` as well, **which adds flexibility, but it also detracts from the Facade pattern's mission, which is to simplify the interface for the common case.**"

## Known Uses
- **ObjectWorks\Smalltalk compiler system** — the inspiration for the sample code.
- **ET++ `ProgrammingEnvironment`** — a facade over built-in browsing tools, defining `InspectObject` and `InspectClass`.
  - The clever part: "An ET++ application can also **forgo** built-in browsing support. In that case, `ProgrammingEnvironment` implements these requests as **null operations**; that is, they do nothing. Only the `ETProgrammingEnvironment` subclass implements these requests with operations that display the corresponding browsers. **The application has no knowledge of whether a browsing environment is available or not**; there's abstract coupling between the application and the browsing subsystem."
- **Choices operating system** — "uses facades to **compose many frameworks into one**." Key abstractions are processes, storage, and address spaces, each a subsystem implemented as a framework "that supports porting Choices to a variety of different hardware platforms." Two have facades: `FileSystemInterface` (storage) and `Domain` (address spaces).
  - "A `Domain` represents an address space. It provides a mapping between virtual addresses and offsets into memory objects, files, or backing store." Internally it uses `MemoryObject` (a data store), `MemoryObjectCache` ("actually a **Strategy** that localizes the caching policy"), and `AddressTranslation` ("encapsulates the address translation hardware").
  - "The `RepairFault` operation is called whenever a **page fault interrupt** occurs. The Domain finds the memory object at the address causing the fault and delegates `RepairFault` to the cache associated with that memory object. **Domains can be customized by changing their components.**"

## Related Patterns
- "**Abstract Factory** can be used with Facade to provide an interface for creating subsystem objects in a subsystem-independent way. Abstract Factory can also be used as **an alternative to Facade** to hide platform-specific classes."
- "**Mediator** is similar to Facade in that it abstracts functionality of existing classes. However, **Mediator's purpose is to abstract arbitrary communication between colleague objects**, often centralizing functionality that doesn't belong in any one of them. **A mediator's colleagues are aware of and communicate with the mediator**... In contrast, a facade merely abstracts the interface to subsystem objects to make them easier to use; **it doesn't define new functionality, and subsystem classes don't know about it**."
- "Usually only one Facade object is required. Thus **Facade objects are often Singletons**."

## Connects To
- **Ch 1**: "The Facade pattern describes how to represent complete subsystems as objects" (determining object granularity); cause of redesign #6 — tight coupling.
- **Ch 4 (Structural Patterns)**: "Whereas Flyweight shows how to make lots of little objects, Facade shows how to make **a single object represent an entire subsystem**."
- **Mediator** (the pattern most often confused with it), **Abstract Factory**, **Singleton**, **Builder**, **Composite**, **Visitor**, **Strategy**
