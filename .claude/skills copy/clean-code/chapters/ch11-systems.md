# Chapter 11: Systems
*(by Dr. Kevin Dean Wampler)*

## Core Idea
Separate constructing a system from using it, keep domain logic in POJOs, and weave cross-cutting concerns in noninvasively — then the architecture can grow incrementally and be test-driven just like the code.

## Frameworks Introduced
- **Separate Constructing a System from Using It**: the startup process, where application objects are constructed and dependencies wired, is a distinct concern from the runtime logic that takes over afterward.
  - When to use: any application with more than trivial setup.
  - How: modularize the startup process separately from runtime logic, and adopt a **global, consistent strategy for resolving major dependencies**.
- **Separation of Main**: move all construction into `main` or modules called by `main`; design the rest of the system assuming everything is already built and wired.
  - How: dependency arrows cross the `main`/application barrier in one direction only — pointing *away* from `main`. The application has no knowledge of `main` or of the construction process.
- **ABSTRACT FACTORY** [GOF]: when the application must control *when* an object is created (e.g. `LineItem` instances added to an `Order`), give it a factory interface while keeping the construction details on the `main` side of the line.
- **Dependency Injection (DI)**: the application of Inversion of Control to dependency management. IoC moves secondary responsibilities from an object to objects dedicated to that purpose, thereby supporting SRP.
  - How: the class takes **no direct steps** to resolve its dependencies — it is completely passive, offering setter methods or constructor arguments for injection. An authoritative mechanism (`main` or a special-purpose container) instantiates and wires, driven by configuration or a construction module.
  - Boundary case: **JNDI lookups are only a partial DI** — the invoking object doesn't control what is returned, but it still *actively resolves* the dependency.
- **Aspect-Oriented Programming (AOP)**: a general-purpose approach to restoring modularity for cross-cutting concerns. Modular constructs called **aspects** specify which points in the system have their behavior modified, via a succinct declarative or programmatic mechanism, applied **noninvasively** (no manual editing of target source).
- **Test Drive the System Architecture**: if domain logic is POJOs decoupled from architecture concerns, you can evolve the architecture from simple to sophisticated, adopting technologies on demand — no Big Design Up Front needed.
- **Optimize Decision Making**: give responsibilities to the most qualified people, and **postpone decisions until the last possible moment**. "A premature decision is a decision made with suboptimal knowledge."
- **Systems Need Domain-Specific Languages**: small scripting languages or APIs that let code read like structured prose a domain expert might write, minimizing the communication gap between a domain concept and its implementation.

## Key Concepts
- **Cross-cutting concern** — persistence, transactions, security, caching, failover: concerns that cut across the natural object boundaries of a domain. "In principle, you can reason about your persistence strategy in a modular, encapsulated way. Yet, in practice, you have to spread essentially the same code across many objects. The problem is the fine-grained intersection of these domains."
- **POJO (Plain-Old Java Object)** — purely focused on its domain, no dependencies on enterprise frameworks or other domains. Conceptually simpler and easier to test drive.
- **LAZY INITIALIZATION/EVALUATION** — has real merits (no construction overhead until used, faster startup, never returns null) but hard-codes a dependency you cannot compile without, complicates testing, mixes construction with runtime processing (a small SRP break), and assumes one type is right for every context. One occurrence is not a problem; the scatter of many such idioms *is*. "Don't forget that lazy instantiation/evaluation is just an optimization and perhaps premature!"
- **BDUF (Big Design Up Front)** — designing everything before implementing anything. Not to be confused with the good practice of up-front design. **Harmful** because it inhibits adapting to change: psychological resistance to discarding prior effort, plus the way architecture choices bias later design thinking.
- **The "Russian doll" of DECORATORs** [GOF] — in Spring, a `Bank` domain object proxied by a DAO, itself proxied by a JDBC data source. The client thinks it calls `getAccounts()` on a `Bank`; it is talking to the outermost of a set of nested decorators.
- **Standards** — make it easier to reuse ideas and components, recruit experienced people, encapsulate good ideas, and wire things together. But creating them can take longer than industry will wait, and some lose touch with adopters' real needs. Teams used EJB2 *because it was a standard* when lighter designs would have sufficed.
- **A good API should largely disappear from view** most of the time, leaving the team's creative effort on the user stories. If it doesn't, architectural constraints inhibit delivery of value.

## Mental Models
- **Think of a system as a city.** No one manages every detail; teams own water, power, traffic, law enforcement. It works because of appropriate levels of abstraction and modularity that let components function without anyone understanding the whole.
- **Construction is a different process from use.** A hotel under construction has a crane bolted to the outside and people in hard hats; a year later, glass walls and a different population. Software should show the same phase separation.
- **Cities grow from towns, which grow from settlements.** Nobody can justify a six-lane highway through a small town. "It is a myth that we can get systems 'right the first time.'" Implement today's stories, then refactor and expand for tomorrow's.
- **Software's physics permits what building architecture cannot.** A physical structure can't take radical change once construction is underway; software can, *if* its concerns are effectively separated — so BDUF is mandatory for buildings and harmful for software.
- **Going incremental is not going rudderless.** Keep expectations of scope, goals, schedule, and general structure — while maintaining the ability to change course as circumstances evolve.
- **Use the simplest thing that can possibly work**, whether designing systems or individual modules.

## Reference Tables

The three aspect-or-aspect-like mechanisms in Java:

| Mechanism | Strength | Drawback |
|---|---|---|
| **Java Proxies** | Fine for simple cases — wrapping method calls in individual objects or classes | JDK dynamic proxies work only with interfaces (classes need CGLIB/ASM/Javassist); high code volume and complexity make clean code hard; **no way to specify system-wide execution points of interest**, so not a true AOP solution |
| **Pure Java AOP frameworks** (Spring AOP, JBoss AOP) | Tools handle the proxy boilerplate; you write POJOs and declare infrastructure; covers **80–90%** of cases where aspects are useful | XML can be verbose and hard to read |
| **AspectJ** | Most full-featured; first-class language support for aspects as modularity constructs | Must adopt new tools, language constructs, and idioms (partly mitigated by the Java 5 annotation form and Spring's support) |

EJB2 vs. EJB3, the chapter's before/after:

| | EJB2 | EJB3 |
|---|---|---|
| Coupling | Business logic tightly coupled to the container; must subclass container types | POJO with annotations |
| Lifecycle | Many required, usually empty, methods (`ejbActivate`, `ejbPassivate`, `ejbLoad`, `ejbStore`, `ejbRemove`…) | None |
| Testing | Must mock a heavyweight container, or deploy to a real server | Test-drives directly |
| Reuse outside the architecture | Effectively impossible | Straightforward |
| Inheritance | One bean cannot inherit from another; DTOs proliferate with copy boilerplate | Ordinary Java |
| Configuration | XML deployment descriptors for O/R mapping, transactions, security | Annotations, movable to XML if a pure POJO is wanted |

## Code Examples

The idiom that mixes construction with use:

```java
public Service getService() {
    if (service == null)
        service = new MyServiceImpl(...);  // Good enough default for most cases?
    return service;
}
```
- **What it demonstrates**: hard-coded dependency on `MyServiceImpl` and everything its constructor requires — unresolvable at compile time even if never used at runtime. And the comment gives away the real problem: "Why does the class with this method have to know the global context?"

EJB2's invasiveness (Listing 11-2, abridged):

```java
public abstract class Bank implements javax.ejb.EntityBean {
    // Business logic...
    public abstract String getStreetAddr1();
    public abstract Collection getAccounts();
    public void addAccount(AccountDTO accountDTO) {
        InitialContext context = new InitialContext();
        AccountHomeLocal accountHome = context.lookup("AccountHomeLocal");
        AccountLocal account = accountHome.create(accountDTO);
        Collection accounts = getAccounts();
        accounts.add(account);
    }

    // EJB container logic
    public abstract void setId(Integer id);
    public Integer ejbCreate(Integer id) { ... }
    public void ejbPostCreate(Integer id) { ... }
    // The rest had to be implemented but were usually empty:
    public void setEntityContext(EntityContext ctx) {}
    public void unsetEntityContext() {}
    public void ejbActivate() {}
    public void ejbPassivate() {}
    public void ejbLoad() {}
    public void ejbStore() {}
    public void ejbRemove() {}
}
```

The same object in EJB3 (Listing 11-5):

```java
@Entity
@Table(name = "BANKS")
public class Bank implements java.io.Serializable {
    @Id @GeneratedValue(strategy=GenerationType.AUTO)
    private int id;

    @Embeddable // An object 'inlined' in Bank's DB row
    public class Address {
        protected String streetAddr1;
        protected String streetAddr2;
        protected String city;
        protected String state;
        protected String zipCode;
    }

    @Embedded
    private Address address;

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER, mappedBy="bank")
    private Collection<Account> accounts = new ArrayList<Account>();

    public void addAccount(Account account) {
        account.setBank(this);
        accounts.add(account);
    }
}
```

Spring wiring, and the two lines of framework-specific Java that keep the application decoupled:

```xml
<beans>
  <bean id="appDataSource"
        class="org.apache.commons.dbcp.BasicDataSource"
        destroy-method="close"
        p:driverClassName="com.mysql.jdbc.Driver"
        p:url="jdbc:mysql://localhost:3306/mydb"
        p:username="me"/>
  <bean id="bankDataAccessObject"
        class="com.example.banking.persistence.BankDataAccessObject"
        p:dataSource-ref="appDataSource"/>
  <bean id="bank"
        class="com.example.banking.model.Bank"
        p:dataAccessObject-ref="bankDataAccessObject"/>
</beans>
```
```java
XmlBeanFactory bf =
    new XmlBeanFactory(new ClassPathResource("app.xml", getClass()));
Bank bank = (Bank) bf.getBean("bank");
```
- **What it demonstrates**: the verbose XML policy is still simpler than the proxy and aspect logic it replaces, and because so little Spring-specific Java is needed, the application is almost completely decoupled from Spring — eliminating EJB2's tight-coupling problems.

## Worked Example
**The JDK proxy, and why it doesn't scale to an architecture.** To add persistence to `Bank` without touching its logic, you separate the abstraction, the POJO, and the handler:

```java
// The abstraction of a bank.
public interface Bank {
    Collection<Account> getAccounts();
    void setAccounts(Collection<Account> accounts);
}

// The 'Plain Old Java Object' (POJO) implementing the abstraction.
public class BankImpl implements Bank {
    private List<Account> accounts;

    public Collection<Account> getAccounts() {
        return accounts;
    }

    public void setAccounts(Collection<Account> accounts) {
        this.accounts = new ArrayList<Account>();
        for (Account account: accounts) {
            this.accounts.add(account);
        }
    }
}

// 'InvocationHandler' required by the proxy API.
public class BankProxyHandler implements InvocationHandler {
    private Bank bank;

    public BankHandler (Bank bank) {
        this.bank = bank;
    }

    public Object invoke(Object proxy, Method method, Object[] args)
            throws Throwable {
        String methodName = method.getName();
        if (methodName.equals("getAccounts")) {
            bank.setAccounts(getAccountsFromDatabase());
            return bank.getAccounts();
        } else if (methodName.equals("setAccounts")) {
            bank.setAccounts((Collection<Account>) args[0]);
            setAccountsToDatabase(bank.getAccounts());
            return null;
        } else {
            ...
        }
    }

    protected Collection<Account> getAccountsFromDatabase() { ... }
    protected void setAccountsToDatabase(Collection<Account> accounts) { ... }
}

// Somewhere else...
Bank bank = (Bank) Proxy.newProxyInstance(
    Bank.class.getClassLoader(),
    new Class[] { Bank.class },
    new BankProxyHandler(new BankImpl()));
```

It works, and `BankImpl` stays clean. But note what it cost: string-comparing method names through the reflection API, a fan of `else if` branches, and considerable ceremony — for two methods. That volume and complexity "make it hard to create clean code," and byte-manipulation libraries are no easier. The decisive limitation is architectural rather than aesthetic: proxies give no mechanism for specifying **system-wide execution points of interest**, which is what a real AOP solution requires. AOP is sometimes confused with the interception and wrapping techniques used to implement it; its actual value is "the ability to specify systemic behaviors in a concise and modular way." That is why the pure-Java AOP frameworks, which automate this boilerplate, are the practical answer for most teams.

**The chapter's recap, stated as a definition:**
> An optimal system architecture consists of modularized domains of concern, each of which is implemented with Plain Old Java (or other) Objects. The different domains are integrated together with minimally invasive Aspects or Aspect-like tools. This architecture can be test-driven, just like the code.

## Key Takeaways
1. Construction and use are different phases; wire everything in `main` (or a container) and let the application assume it was built correctly.
2. Convenient setup idioms like lazy initialization scatter the global setup strategy across the application — that scatter, not any single occurrence, is the defect.
3. Use DI so classes stay passive about their dependencies; use ABSTRACT FACTORY when the application must control creation timing.
4. Cross-cutting concerns need aspect-like tooling; proxies alone can't express system-wide behavior.
5. Write domain logic as POJOs and add infrastructure declaratively — that is what makes the architecture testable and evolvable.
6. Architecture can grow incrementally. BDUF is harmful; start naively simple and decoupled, and add infrastructure as you scale.
7. Postpone decisions to the last responsible moment so you decide with the most knowledge.
8. Adopt standards only when they add demonstrable value, and raise the abstraction level with DSLs where the domain warrants it.
9. An invasive architecture obscures domain logic, which hides bugs, slows stories, and destroys the benefits of TDD.

## Connects To
- **Ch 6 (Objects and Data Structures)**: DTOs, and the EJB2 habit of redundant struct-like types with copy boilerplate.
- **Ch 10 (Classes)**: SRP, DIP, and testable decoupling at class scale; this chapter is the same argument at system scale.
- **Ch 12 (Emergence)**: "the simplest thing that can possibly work" and test-driven design as the mechanism.
- **Ch 3 (Functions)**: DSLs as the language whose verbs are functions and nouns are classes.
- **[GOF]**: ABSTRACT FACTORY, DECORATOR. **[Fowler]**: IoC containers and DI. **[Spring]/[JBoss]/[AspectJ]**: the tooling. **[Alexander]**: patterns as a domain language.
