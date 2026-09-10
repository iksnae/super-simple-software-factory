# Chapter 29: Clean Embedded Architecture
*(by James Grenning)*

## Core Idea
"Although software does not wear out, **it can be destroyed from within by unmanaged dependencies on firmware and hardware**" — code is firmware not because of where it is stored but because of what it depends on, and a clean embedded architecture is one whose software is testable **off** the target hardware.

## Frameworks Introduced
- **The redefinition of firmware.** Doug Schmidt: *"Although software does not wear out, firmware and hardware become obsolete, thereby requiring software modifications."* Grenning's addition, and the chapter's thesis, is quoted above.
  - The standard definitions (Wikipedia, techterms, lifewire, webopedia) all locate firmware in ROM/EPROM/flash. "**These accepted definitions of firmware are wrong, or at least obsolete.** Firmware does not mean code lives in ROM. It's not firmware because of **where it is stored**; rather, it is firmware because of **what it depends on and how hard it is to change** as hardware evolves."
- **Non-embedded engineers write firmware too.** "You non-embedded developers essentially write firmware **whenever you bury SQL in your code** or when you **spread platform dependencies throughout your code**. Android app developers write firmware when they don't separate their business logic from the Android API."
- **The App-titude Test** — Kent Beck's three activities, with Grenning's commentary:
  1. *"First make it work."* — You are out of business if it doesn't work.
  2. *"Then make it right."* — Refactor so you and others can understand and evolve it.
  3. *"Then make it fast."* — Refactor for *needed* performance.
  - The observed pathology: embedded code "written with 'Make it work' in mind — and perhaps also with an **obsession for the 'Make it fast' goal, achieved by adding micro-optimizations at every opportunity**." Fred Brooks's "plan to throw one away" is the same advice: learn what works, then make a better solution.
  - "Getting an app to work is what I call the **App-titude test**... Programmers, embedded or not, who just concern themselves with getting their app to work are doing their products and employers a disservice."
- **The four abstraction layers**:
  - **HAL (Hardware Abstraction Layer)** — the boundary between software and firmware. "This is not a new idea: It has been in PCs since the days before Windows."
  - **PAL (Processor Abstraction Layer)** — isolates vendor C-extension register access. "Firmware above the PAL could be tested off-target, making it a little less firm."
  - **OSAL (Operating System Abstraction Layer)** — isolates software from the RTOS or embedded OS.
  - Each one "provides that **seam** or set of substitution points that facilitate off-target testing."
- **The HAL's API is defined by its consumer, at the consumer's level of abstraction.** "The HAL exists for the software that sits on top of it, and **its API should be tailored to that software's needs**."

## Key Concepts
- **The target-hardware bottleneck** — "When embedded code is structured without applying clean architecture principles and practices, you will often face the scenario in which you can test your code **only on the target**." Compounded by the realities: hardware developed concurrently with software (so there may be nowhere to run the code), and once it arrives, "the hardware will have its own defects, making software development progress even slower than usual."
- **Software/firmware intermingling is an anti-pattern.** "Code exhibiting this anti-pattern will resist changes. In addition, changes will be **dangerous, often leading to unintended consequences**. Full regression tests of the whole system will be needed for minor changes. If you have not created externally instrumented tests, expect to get bored with manual tests — and then you can expect new bug reports."
- **Vendor C extensions are not C.** "Some silicon providers add keywords to the C language to make accessing the registers and IO ports simple from C. **Unfortunately, once that is done, the code is no longer C.**" It "won't compile for another processor, or maybe even with a different compiler for the same processor."
- **Layers contain layers.** "It is more of a **repeating fractal pattern** than a limited set of predefined layers."
- **Header files as interface definitions** — "Limit header file contents to function declarations as well as the constants and struct names that are needed by the function. Don't clutter the interface header files with data structures, constants, and typedefs that are needed by only the implementation. **It's not just a matter of clutter: That clutter will lead to unwanted dependencies.**"
- **DRY conditional compilation** — "I recall one especially problematic case where the statement `#ifdef BOARD_V2` was mentioned **several thousand times** in a telecom application... If I see `#ifdef BOARD_V2` once, it's not really a problem. **Six thousand times is an extreme problem.**" With a HAL, "the hardware type would become a detail hidden under the HAL... we could use the linker or some form of runtime binding to connect the software to the hardware."

## Code Examples

**Passing the App-titude test** — one file's functions, in the order found:

```c
ISR(TIMER1_vect) { ... }
ISR(INT2_vect) { ... }
void btn_Handler(void) { ... }
float calc_RPM(void) { ... }
static char Read_RawData(void) { ... }
void Do_Average(void) { ... }
void Get_Next_Measurement(void) { ... }
void Zero_Sensor_1(void) { ... }
void Zero_Sensor_2(void) { ... }
void Dev_Control(char Activation) { ... }
char Load_FLASH_Setup(void) { ... }
void Save_FLASH_Setup(void) { ... }
void Store_DataSet(void) { ... }
float bytes2float(char bytes[4]) { ... }
void Recall_DataSet(void) { ... }
void Sensor_init(void) { ... }
void uC_Sleep(void) { ... }
```

Regrouped by concern, the mixture becomes obvious:

| Concern | Functions |
|---|---|
| **Domain logic** | `calc_RPM`, `Do_Average`, `Get_Next_Measurement`, `Zero_Sensor_1`, `Zero_Sensor_2` |
| **Hardware platform setup** | `ISR(TIMER1_vect)`, `ISR(INT2_vect)`, `uC_Sleep` |
| **Reacting to the on/off button** | `btn_Handler`, `Dev_Control` |
| **A/D input from hardware** | `Read_RawData` |
| **Persistent storage** | `Load_FLASH_Setup`, `Save_FLASH_Setup`, `Store_DataSet`, `bytes2float`, `Recall_DataSet` |
| **Doesn't do what its name implies** | `Sensor_init` |

"Virtually every bit of this code knows it is in a special microprocessor architecture, using 'extended' C constructs that tie the code to a particular tool chain and microprocessor. **There is no way for this code to have a long useful life** unless the product never needs to be moved to a different hardware environment. This application works: The engineer passed the App-titude test. **But the application can't be said to have a clean embedded architecture.**"

**The vendor header that traps you** (for the ACME family of DSPs — "you know, the ones used by Wile E. Coyote"):

```c
#ifndef _ACME_STD_TYPES
#define _ACME_STD_TYPES

#if defined(_ACME_X42)
typedef unsigned int    Uint_32;
typedef unsigned short  Uint_16;
typedef unsigned char   Uint_8;
typedef int             Int_32;
typedef short           Int_16;
typedef char            Int_8;
#elif defined(_ACME_A42)
typedef unsigned long   Uint_32;
typedef unsigned int    Uint_16;
typedef unsigned char   Uint_8;
typedef long            Int_32;
typedef int             Int_16;
typedef char            Int_8;
#else
#error <acmetypes.h> is not supported for this environment
#endif

#endif
```
- **What it demonstrates**: "You can't compile your code unless you include this header. If you use the header and define `_ACME_X42` or `_ACME_A42`, **your integers will be the wrong size if you try to test your code off-target**."

**The escape hatch — write your own `stdint.h`:**

```c
#ifndef _STDINT_H_
#define _STDINT_H_

#include <acmetypes.h>

typedef Uint_32 uint32_t;
typedef Uint_16 uint16_t;
typedef Uint_8  uint8_t;
typedef Int_32  int32_t;
typedef Int_16  int16_t;
typedef Int_8   int8_t;

#endif
```
- **What it demonstrates**: the ACME dependency now exists in exactly one file. "Having your embedded software and firmware use `stdint.h` helps keep your code clean and portable."

**Code that looks like C and isn't** (based on real code from the wild):

```c
void say_hi() {
    IE = 0b11000000;
    SBUF0 = (0x68);
    while(TI_0 == 0);
    TI_0 = 0;
    SBUF0 = (0x69);
    while(TI_0 == 0);
    TI_0 = 0;
    SBUF0 = (0x0a);
    while(TI_0 == 0);
    TI_0 = 0;
    SBUF0 = (0x0d);
    while(TI_0 == 0);
    TI_0 = 0;
    IE = 0b11010000;
}
```
- **What it demonstrates**: `0b11000000` binary notation isn't C. `IE` (interrupt enable bits), `SBUF0` (serial output buffer), and `TI_0` (serial transmit buffer empty interrupt) are micro-controller peripherals exposed as pseudo-globals. "Yes, this is convenient — **but it's not C.**" The rule: "A clean embedded architecture would use these device access registers directly in **very few places** and confine them **totally to the firmware**. **Anything that knows about these registers becomes firmware and is consequently bound to the silicon.**"

## Worked Example
**Raising the HAL's level of abstraction — the LED that means something.**

The chapter's most transferable idea is that a HAL is not a thin wrapper over hardware; **its abstraction level is set by what the application needs to say.**

*Level 0 — the hardware.* An LED is tied to a GPIO bit. The firmware could simply expose the GPIO bits.

*Level 1 — a low-level HAL.* `Led_TurnOn(5)`. Better than raw GPIO manipulation, but "that is a pretty **low-level** hardware abstraction layer." The application still has to know that LED 5 is the one it wants.

*Level 2 — a product-level HAL.* Ask what the LED is *indicating*. Suppose it indicates low battery power. Then the firmware (or board support package) provides `Led_TurnOn(5)`, and the HAL provides **`Indicate_LowBattery()`**.

"You can see the HAL **expressing services needed by the application**. You can also see that layers may contain layers... **The GPIO assignments are details that should be hidden from the software.**"

The same reasoning applied to storage: firmware can store bytes and arrays of bytes into flash. The application needs to store and read **name/value pairs**. "The software should not be concerned that the name/value pairs are stored in **flash memory, a spinning disk, the cloud, or core memory**. The HAL provides a service, and it does not reveal to the software how it does it."

**The RTOS version of the same argument.** A HAL may suffice for bare metal, but not with an RTOS or embedded Linux/Windows. The risks Grenning lists are commercial as much as technical: "what if your RTOS supplier is **bought by another company** and the royalties go up, or the quality goes down? What if your needs change and your RTOS does not have the capabilities that you now require?"

And the cost isn't a find-and-replace: "These won't just be simple syntactical changes due to the new OS's API, but will likely have to **adapt semantically** to the new OS's different capabilities and primitives."

With an OSAL, the migration inverts: "you would largely be writing a **new OSAL that is compatible with the old OSAL**. Which would you rather do: **modify a bunch of complex existing code, or write new code to a defined interface and behavior?** This is not a trick question. I choose the latter."

On the code-bloat objection: "the layer becomes the place where **much of the duplication around using an OS is isolated**. This duplication does not have to impose a big overhead. If you define an OSAL, you can also encourage your applications to have a common structure. You might provide message passing mechanisms, rather than having every thread handcraft its concurrency model."

## Reference Tables

| Layer | Separates | Hides |
|---|---|---|
| **HAL** | Software from firmware | GPIO assignments, flash vs. disk vs. cloud, board type |
| **PAL** | Firmware from processor | Vendor C extensions, register/IO-port pseudo-globals |
| **OSAL** | Software from the operating system | RTOS API and its semantics; concurrency model |

| Anti-pattern | Consequence |
|---|---|
| Software/firmware intermingled | Changes resisted and dangerous; full regression needed for minor changes; manual testing → new bug reports |
| Vendor extensions used throughout | Code no longer C; won't compile for another processor or even another compiler |
| `#ifdef BOARD_V2` repeated thousands of times | DRY violation at scale; hide the board type under the HAL and bind via linker or runtime instead |
| Implementation details in interface headers | Unwanted dependencies, not just clutter |

## Key Takeaways
1. Firmware is defined by dependency, not by storage location — and non-embedded developers write it whenever they bury SQL or platform APIs in business logic.
2. Passing the App-titude test ("make it work") is not the job; "make it right" is what buys a long useful life.
3. The target-hardware bottleneck is the concrete cost of skipping architecture in embedded work.
4. Add a HAL between software and firmware, a PAL under vendor C extensions, and an OSAL between software and the RTOS.
5. Set each abstraction layer's API at the *consumer's* level — `Indicate_LowBattery()`, not `Led_TurnOn(5)`; name/value pairs, not flash bytes.
6. Confine device registers and vendor extensions to as few files as possible; write your own `stdint.h` over the vendor header.
7. Keep interface headers to declarations plus what callers need; implementation details in headers become dependencies.
8. Replace mass conditional compilation with HAL interfaces plus link-time or runtime binding.
9. The test of the whole discipline: the software runs off-target, off-OS, without the hardware.

## Connects To
- **Ch 4 (Structured Programming)** and **Ch 28 (The Test Boundary)**: testability as the architectural goal.
- **Ch 11 (DIP)** and **Ch 17 (Boundaries)**: programming to interfaces and substitutability, applied to silicon.
- **Ch 30–32 (Details)**: "The hardware is a detail" is the same claim as "the database is a detail."
- **Ch 19 (Policy and Level)**: layers containing layers as a fractal of levels.
- **Clean Code, Ch 3 & 8**: DRY, and wrapping third-party APIs.
