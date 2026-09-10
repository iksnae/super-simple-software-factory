# Interpreter
*Class Behavioral · GoF p. 243*

## Intent
> **Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language.**

## Motivation
"**If a particular kind of problem occurs often enough, then it might be worthwhile to express instances of the problem as sentences in a simple language.** Then you can build an interpreter that solves the problem by interpreting these sentences."

Regular expressions are the example: "Rather than building custom algorithms to match each pattern against strings, search algorithms could **interpret a regular expression** that specifies a set of strings to match."

**The core mapping**: "The Interpreter pattern uses **a class to represent each grammar rule**. Symbols on the right-hand side of the rule are **instance variables** of these classes."

```
expression ::= literal | alternation | sequence | repetition | '(' expression ')'
alternation ::= expression '|' expression
sequence ::= expression '&' expression
repetition ::= expression '*'
literal ::= 'a' | 'b' | 'c' | ... { 'a' | 'b' | 'c' | ... }*
```

Five classes: abstract `RegularExpression` plus `LiteralExpression`, `AlternationExpression`, `SequenceExpression`, `RepetitionExpression`. "Every regular expression defined by this grammar is represented by an **abstract syntax tree** made up of instances of these classes" — e.g. `raining & (dogs | cats)*`.

"`Interpret` takes as an argument **the context** in which to interpret the expression. The context contains the input string and information on **how much of it has been matched so far**."

## Applicability
"Use the Interpreter pattern when **there is a language to interpret, and you can represent statements in the language as abstract syntax trees**." It works best when:
- **"the grammar is simple."** "For complex grammars, **the class hierarchy for the grammar becomes large and unmanageable**. Tools such as **parser generators** are a better alternative in such cases. They can interpret expressions **without building abstract syntax trees**, which can save space and possibly time."
- **"efficiency is not a critical concern."** "The most efficient interpreters are usually **not implemented by interpreting parse trees directly** but by first translating them into another form. For example, regular expressions are often transformed into **state machines**. But even then, **the translator can be implemented by the Interpreter pattern**, so the pattern is still applicable."

## Participants
- **AbstractExpression** (`RegularExpression`) — declares an abstract `Interpret` operation common to all nodes.
- **TerminalExpression** (`LiteralExpression`) — implements `Interpret` for terminal symbols. "**An instance is required for every terminal symbol in a sentence.**"
- **NonterminalExpression** (`AlternationExpression`, `RepetitionExpression`, `SequenceExpression`) — "**one such class is required for every rule** R ::= R₁R₂…Rₙ"; maintains instance variables of type AbstractExpression for each symbol; "`Interpret` typically **calls itself recursively** on the variables representing R₁ through Rₙ."
- **Context** — "contains information that's **global to the interpreter**."
- **Client** — "builds (or is given) an abstract syntax tree"; invokes `Interpret`.

## Collaborations
- "Each NonterminalExpression node defines `Interpret` in terms of `Interpret` on each subexpression. **The `Interpret` operation of each TerminalExpression defines the base case in the recursion.**"
- "The `Interpret` operations at each node **use the context to store and access the state** of the interpreter."

## Consequences
1. **It's easy to change and extend the grammar.** "Because the pattern uses classes to represent grammar rules, **you can use inheritance to change or extend the grammar**."
2. **Implementing the grammar is easy, too.** "Classes defining nodes in the abstract syntax tree have **similar implementations**. These classes are easy to write, and often **their generation can be automated**."
3. ⚠️ **Complex grammars are hard to maintain.** "The Interpreter pattern defines **at least one class for every rule** in the grammar (grammar rules defined using BNF **may require multiple classes**). Hence grammars containing many rules can be hard to manage."
4. **Adding new ways to interpret expressions.** "you can support **pretty printing or type-checking** an expression by defining a new operation on the expression classes. **If you keep creating new ways of interpreting an expression, then consider using the Visitor pattern** to avoid changing the grammar classes."

## Implementation
"The Interpreter and **Composite** patterns share many implementation issues."
1. **Creating the abstract syntax tree.** ⚠️ "**The Interpreter pattern doesn't explain how to create an abstract syntax tree. In other words, it doesn't address parsing.**" The tree "can be created by a table-driven parser, by a hand-crafted (usually recursive descent) parser, **or directly by the client**."
2. **Defining the `Interpret` operation.** "**You don't have to define `Interpret` in the expression classes.** If it's common to create a new interpreter, then it's better to use the **Visitor** pattern... a grammar for a programming language will have many operations — **type-checking, optimization, code generation** — [so] it will be more likely to use a visitor."
3. **Sharing terminal symbols with the Flyweight pattern.** "Grammars whose sentences contain **many occurrences of a terminal symbol** might benefit from sharing a single copy. Grammars for computer programs are good examples — **each program variable will appear in many places**."
   - Why it fits: "**Terminal nodes generally don't store information about their position in the abstract syntax tree. Parent nodes pass them whatever context they need** during interpretation. Hence there is a distinction between shared (intrinsic) state and passed-in (extrinsic) state."

## Sample Code

### 1. Smalltalk regular-expression matcher
The state being threaded is subtler than it first appears: "This current state is characterized by **a set of input streams** representing the set of inputs that the regular expression could have accepted so far. (This is roughly equivalent to recording all states that the equivalent finite state automata would be in.)"

Why a *set* is required: for `'a' repeat & 'abc'` matching `"aabc"`, "matching the input against the subexpression `'a' repeat` would yield **two input streams**, one having matched one character, and the other having matched two. **Only the stream that has accepted one character will match the remaining `abc`.**"

```smalltalk
match: inputState
    ^ expression2 match: (expression1 match: inputState).
```
```smalltalk
match: inputState
    | finalState |
    finalState := alternative1 match: inputState.
    finalState addAll: (alternative2 match: inputState).
    ^ finalState
```
```smalltalk
match: inputState
    | aState finalState |
    aState := inputState.
    finalState := inputState copy.
    [aState isEmpty] whileFalse:
        [aState := repetition match: aState.
         finalState addAll: aState].
    ^ finalState
```
```smalltalk
match: inputState
    | finalState tStream |
    finalState := Set new.
    inputState do: [:stream |
        tStream := stream copy.
        (tStream nextAvailable: components size) = components
            ifTrue: [finalState add: tStream]].
    ^ finalState
```
- "**The `nextAvailable:` message advances the input stream. This is the only `match:` operation that advances the stream.** Notice how the state that's returned contains a **copy** of the input stream, thereby ensuring that matching a literal never changes the input stream. **This is important because each alternative of an `AlternationExpression` should see identical copies of the input stream.**"

**Using the host compiler as the parser** — instead of writing one, define the grammar's operators as methods:

```smalltalk
& aNode
    ^ SequenceExpression new
        expression1: self expression2: aNode asRExp

repeat
    ^ RepetitionExpression new repetition: self

| aNode
    ^ AlternationExpression new
        alternative1: self alternative2: aNode asRExp

asRExp
    ^ self
```
- "That lets us use the **built-in Smalltalk compiler as if it were a parser for regular expressions**."
- And a scope observation: "If we defined these operations **higher up in the class hierarchy** (`SequenceableCollection`...), then they would also be defined for classes such as `Array` and `OrderedCollection`. **This would let regular expressions match sequences of any kind of object.**"

### 2. C++ Boolean expressions

```cpp
class BooleanExp {
public:
    BooleanExp();
    virtual ~BooleanExp();

    virtual bool Evaluate(Context&) = 0;
    virtual BooleanExp* Replace(const char*, BooleanExp&) = 0;
    virtual BooleanExp* Copy() const = 0;
};

class Context {
public:
    bool Lookup(const char*) const;
    void Assign(VariableExp*, bool);
};
```
```cpp
bool VariableExp::Evaluate (Context& aContext) {
    return aContext.Lookup(_name);
}

BooleanExp* VariableExp::Copy () const {
    return new VariableExp(_name);
}

BooleanExp* VariableExp::Replace (const char* name, BooleanExp& exp) {
    if (strcmp(name, _name) == 0) {
        return exp.Copy();
    } else {
        return new VariableExp(_name);
    }
}
```
```cpp
bool AndExp::Evaluate (Context& aContext) {
    return
        _operand1->Evaluate(aContext) &&
        _operand2->Evaluate(aContext);
}

BooleanExp* AndExp::Copy () const {
    return new AndExp(_operand1->Copy(), _operand2->Copy());
}

BooleanExp* AndExp::Replace (const char* name, BooleanExp& exp) {
    return new AndExp(
        _operand1->Replace(name, exp),
        _operand2->Replace(name, exp)
    );
}
```
```cpp
BooleanExp* expression;
Context context;

VariableExp* x = new VariableExp("X");
VariableExp* y = new VariableExp("Y");

expression = new OrExp(
    new AndExp(new Constant(true), x),
    new AndExp(y, new NotExp(x))
);

context.Assign(x, false);
context.Assign(y, true);

bool result = expression->Evaluate(context);
```
```cpp
VariableExp* z = new VariableExp("Z");
NotExp not_z(z);

BooleanExp* replacement = expression->Replace("Y", not_z);
context.Assign(z, true);

result = replacement->Evaluate(context);
```

## Worked Example
**What counts as "interpreting" — and why the answer is a matter of perspective.**

The Boolean example carries the chapter's most interesting argument. Three operations are defined on `BooleanExp`, and only one of them looks like an interpreter:

- **`Evaluate`** — "fits our idea of what an interpreter should do most closely — that is, it **interprets a program or expression and returns a simple result**."
- **`Replace`** — "can be viewed as an interpreter as well. It's an interpreter whose **context is the name of the variable being replaced along with the expression that replaces it**, and whose **result is a new expression**." Note also what it demonstrates: "**Replace shows how the Interpreter pattern can be used for more than just evaluating expressions. In this case, it manipulates the expression itself.**"
- **`Copy`** — "can be thought of as an interpreter **with an empty context**."

"It may seem a little strange to consider `Replace` and `Copy` to be interpreters, because these are just basic operations on trees. **The examples in Visitor illustrate how all three operations can be refactored into a separate 'interpreter' visitor, thus showing that the similarity is deep.**"

**And then the boundary of the pattern:**

> "The Interpreter pattern is **more than just an operation distributed over a class hierarchy that uses the Composite pattern**. We consider `Evaluate` an interpreter because **we think of the `BooleanExp` class hierarchy as representing a language**. Given a similar class hierarchy for representing **automotive part assemblies**, it's unlikely we'd consider operations like `Weight` and `Copy` as interpreters even though they are distributed over a class hierarchy that uses the Composite pattern — **we just don't think of automotive parts as a language. It's a matter of perspective; if we started publishing grammars of automotive parts, then we could consider operations on those parts to be ways of interpreting the language.**"

That is the practical test for whether you have an Interpreter or merely a Composite with a recursive operation.

## Known Uses
- "widely used in **compilers implemented with object-oriented languages**, as the Smalltalk compilers are."
- **SPECTalk** — "uses the pattern to interpret **descriptions of input file formats**."
- **QOCA** constraint-solving toolkit — "uses it to **evaluate constraints**."
- The scope caveat: "Considered in its most general form, **nearly every use of the Composite pattern will also contain the Interpreter pattern. But the Interpreter pattern should be reserved for those cases in which you want to think of the class hierarchy as defining a language.**"

## Related Patterns
- "**Composite**: The abstract syntax tree **is** an instance of the Composite pattern."
- "**Flyweight** shows how to share terminal symbols within the abstract syntax tree."
- "**Iterator**: The interpreter can use an Iterator to traverse the structure."
- "**Visitor** can be used to maintain the behavior in each node in the abstract syntax tree **in one class**."

## Connects To
- **Ch 5 (Behavioral Patterns)**: one of only two behavioral **class** patterns.
- **Ch 12 (Composite)**: "Sometimes composites have a variable for each child... See Interpreter for an example."
- **Composite, Flyweight, Iterator, Visitor**
