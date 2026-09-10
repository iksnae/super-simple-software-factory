# Proxy
*Object Structural · Also Known As: **Surrogate** · GoF p. 207*

## Intent
> **Provide a surrogate or placeholder for another object to control access to it.**

## Motivation
"One reason for controlling access to an object is to **defer the full cost of its creation and initialization** until we actually need to use it." Large raster images are expensive to create, "but **opening a document should be fast**... This isn't necessary anyway, because not all of these objects will be visible at the same time."

**The two questions that produce the pattern**: "But **what do we put in the document in place of the image**? And **how can we hide the fact that the image is created on demand** so that we don't complicate the editor's implementation? This optimization shouldn't impact the rendering and formatting code."

"The proxy acts just like the image and takes care of instantiating it when it's required... The proxy also stores its **extent**, that is, its width and height. **The extent lets the proxy respond to requests for its size from the formatter without actually instantiating the image.**"

## Applicability
"Proxy is applicable whenever there is a need for a **more versatile or sophisticated reference to an object than a simple pointer**." Four kinds:

| Kind | Purpose | Example |
|---|---|---|
| **Remote proxy** | "provides a local representative for an object in a **different address space**" | NEXTSTEP's `NXProxy`; Coplien calls it an "**Ambassador**" |
| **Virtual proxy** | "creates **expensive objects on demand**" | `ImageProxy` |
| **Protection proxy** | "**controls access** to the original object... useful when objects should have different access rights" | `KernelProxies` in the Choices OS |
| **Smart reference** | "a replacement for a bare pointer that **performs additional actions** when an object is accessed" | reference counting (**smart pointers**); loading a persistent object on first reference; "checking that the real object is **locked** before it's accessed" |

## Participants
- **Proxy** (`ImageProxy`) — maintains a reference to the real subject; "provides an **interface identical to Subject's**"; "controls access to the real subject and **may be responsible for creating and deleting it**."
  - Per kind: remote proxies "**encode a request and its arguments**"; virtual proxies "may **cache additional information** about the real subject so that they can postpone accessing it"; protection proxies "**check that the caller has the access permissions** required."
- **Subject** (`Graphic`) — the common interface for RealSubject and Proxy.
- **RealSubject** (`Image`) — the real object the proxy represents.

## Collaborations
- "Proxy forwards requests to RealSubject **when appropriate, depending on the kind of proxy**."

## Consequences
"The Proxy pattern introduces a **level of indirection** when accessing an object."
1. "A remote proxy can **hide the fact that an object resides in a different address space**."
2. "A virtual proxy can perform **optimizations such as creating an object on demand**."
3. "Both protection proxies and smart references allow **additional housekeeping tasks** when an object is accessed."

**Copy-on-write** — "another optimization that the Proxy pattern can hide from the client... **Copying a large and complicated object can be an expensive operation. If the copy is never modified, then there's no need to incur this cost.**"
- The mechanism: "the subject must be **reference counted**. Copying the proxy will do nothing more than **increment this reference count**. Only when the client requests an operation that **modifies** the subject does the proxy actually copy it. In that case the proxy must also **decrement** the subject's reference count. When the reference count goes to zero, the subject gets deleted."

## Implementation
1. **Overloading the member access operator in C++.** "Overloading `operator->` lets you perform additional work whenever an object is dereferenced. This can be helpful for implementing some kinds of proxy; **the proxy behaves just like a pointer**."

```cpp
class Image;
extern Image* LoadAnImageFile(const char*);
    // external function

class ImagePtr {
public:
    ImagePtr(const char* imageFile);
    virtual ~ImagePtr();

    virtual Image* operator->();
    virtual Image& operator*();
private:
    Image* LoadImage();
private:
    Image* _image;
    const char* _imageFile;
};

ImagePtr::ImagePtr (const char* theImageFile) {
    _imageFile = theImageFile;
    _image = 0;
}

Image* ImagePtr::LoadImage () {
    if (_image == 0) {
        _image = LoadAnImageFile(_imageFile);
    }
    return _image;
}

Image* ImagePtr::operator-> () { return LoadImage(); }
Image& ImagePtr::operator*  () { return *LoadImage(); }
```
```cpp
ImagePtr image = ImagePtr("anImageFileName");
image->Draw(Point(50, 100));
    // (image.operator->())->Draw(Point(50, 100))
```
- ⚠️ **Two limits**: "the image proxy acts like a pointer, **but it's not declared to be a pointer to an Image**. That means you can't use it exactly like a real pointer... Hence **clients must treat `Image` and `ImagePtr` objects differently**."
- And the decisive one: "**Some proxies need to know precisely which operation is called, and overloading the member access operator doesn't work in those cases.**" For the Motivation's virtual proxy, "the image should be loaded at a specific time — namely **when the `Draw` operation is called** — and not whenever the image is referenced. Overloading the access operator doesn't allow this distinction."
- The consequence: "we must **manually implement each proxy operation**... **It's tedious to write this code again and again. So it's common to use a preprocessor to generate it automatically.**"

2. **Using `doesNotUnderstand:` in Smalltalk.** "Smalltalk calls `doesNotUnderstand: aMessage` when a client sends a message to a receiver that has no corresponding method. The Proxy class can redefine `doesNotUnderstand` so that the message is forwarded to its subject."
   - "To ensure that a request is forwarded... **you can define a Proxy class that doesn't understand any messages** — Smalltalk lets you do this by **defining Proxy as a class with no superclass**."
   - ⚠️ "The main disadvantage is that most Smalltalk systems have a few **special messages handled directly by the virtual machine**... The only one usually implemented in Object (and so can affect proxies) is the **identity operation `==`**. ... **You can't expect identity on proxies to mean identity on their real subjects.**" And: "`doesNotUnderstand:` was developed for **error handling, not for building proxies**, and so it's generally **not very fast**."
3. **Proxy doesn't always have to know the type of real subject.** "If a Proxy class can deal with its subject **solely through an abstract interface**, then there's no need to make a Proxy class for each RealSubject class... **But if Proxies are going to instantiate RealSubjects (such as in a virtual proxy), then they have to know the concrete class.**"
   - "Some proxies have to refer to their subject **whether it's on disk or in memory**. That means they must use some form of **address space-independent object identifiers**." (A file name, in the Motivation.)

## Sample Code

```cpp
class Graphic {
public:
    virtual ~Graphic();

    virtual void Draw(const Point& at) = 0;
    virtual void HandleMouse(Event& event) = 0;

    virtual const Point& GetExtent() = 0;

    virtual void Load(istream& from) = 0;
    virtual void Save(ostream& to) = 0;
protected:
    Graphic();
};
```
```cpp
class ImageProxy : public Graphic {
public:
    ImageProxy(const char* imageFile);
    virtual ~ImageProxy();

    virtual void Draw(const Point& at);
    virtual void HandleMouse(Event& event);

    virtual const Point& GetExtent();

    virtual void Load(istream& from);
    virtual void Save(ostream& to);
protected:
    Image* GetImage();
private:
    Image* _image;
    Point _extent;
    char* _fileName;
};

ImageProxy::ImageProxy (const char* fileName) {
    _fileName = strdup(fileName);
    _extent = Point::Zero;    // don't know extent yet
    _image = 0;
}

Image* ImageProxy::GetImage() {
    if (_image == 0) {
        _image = new Image(_fileName);
    }
    return _image;
}
```

The three behaviours in one class — **cache**, **instantiate**, **forward**:

```cpp
const Point& ImageProxy::GetExtent () {
    if (_extent == Point::Zero) {
        _extent = GetImage()->GetExtent();
    }
    return _extent;
}

void ImageProxy::Draw (const Point& at) {
    GetImage()->Draw(at);
}

void ImageProxy::HandleMouse (Event& event) {
    GetImage()->HandleMouse(event);
}

void ImageProxy::Save (ostream& to) {
    to << _extent << _fileName;
}

void ImageProxy::Load (istream& from) {
    from >> _extent >> _fileName;
}
```
- Note `Save`/`Load`: the proxy persists **the extent and the file name**, never the image — so a saved document reopens without loading a single image.

```cpp
TextDocument* text = new TextDocument;
// ...
text->Insert(new ImageProxy("anImageFileName"));
```

**Smalltalk generic proxy**, and a protection proxy in four lines:

```smalltalk
doesNotUnderstand: aMessage
    ^ self realSubject
        perform: aMessage selector
        withArguments: aMessage arguments
```
```smalltalk
doesNotUnderstand: aMessage
    (legalMessages includes: aMessage selector)
        ifTrue: [^ self realSubject
                    perform: aMessage selector
                    withArguments: aMessage arguments]
        ifFalse: [^ self error: 'Illegal operator']
```
- ⚠️ A trap worth noting: "If it isn't legal, then it will send `error:` to the proxy, which will result in an **infinite loop of errors** unless the proxy defines `error:`. Consequently, the definition of `error:` should be **copied from class Object** along with any methods it uses."

## Known Uses
- **ET++** text building block classes — the Motivation's virtual proxy.
- **NEXTSTEP `NXProxy`** — "local representatives for objects that may be distributed. A server creates proxies for remote objects when clients request them. On receiving a message, the proxy **encodes it along with its arguments** and forwards the encoded message to the remote subject."
- **McCullough** on Smalltalk proxies for remote objects; **Pascoe** on "**Encapsulators**" for side-effects on method calls and access control.

## Related Patterns
- "**Adapter**: An adapter provides a **different** interface to the object it adapts. In contrast, a proxy provides the **same** interface. However, **a proxy used for access protection might refuse to perform an operation** that the subject will perform, so its interface may be effectively a **subset** of the subject's."
- "**Decorator**: Although decorators can have similar implementations as proxies, decorators have a different purpose. **A decorator adds one or more responsibilities to an object, whereas a proxy controls access to an object.**"
- **How closely they resemble each other varies by kind**: "A **protection proxy** might be implemented **exactly like a decorator**. A **remote proxy** will not contain a direct reference to its real subject but only an **indirect** reference, such as 'host ID and local address on host.' A **virtual proxy** will start off with an indirect reference such as a file name **but will eventually obtain and use a direct reference**."

## Connects To
- **Ch 1**: cause of redesign #4 — dependence on object representations or implementations.
- **Ch 4 (Structural Patterns)**: "Proxies provide a level of indirection to specific properties of objects. Hence they can **restrict, enhance, or alter** these properties."
- **Ch 9 (Discussion of Structural Patterns)**: the full Composite vs. Decorator vs. Proxy comparison.
- **Adapter, Decorator, Iterator** (which "describes another kind of proxy"), **Factory Method** (Orbix generates proxy types with one)
