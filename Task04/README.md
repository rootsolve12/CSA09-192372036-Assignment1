# Task04


## Aim and theory
Use constructor validation and immutable tickets so incomplete domain objects never enter the facility.
Vehicle owns a private final normalized registration. Subclasses call super(registration). ParkingTicket has a canonical five-argument constructor and a four-argument overload that chains using this(...) to a visitor user. ParkingUser similarly chains its two-argument constructor to its three-argument form. There is no implicit no-argument constructor after explicit constructors are declared; this is deliberate for vehicles/tickets because registration and entry time are required. A default-initialized mutable draft is demonstrated only as an alternative, not used by the facility.
A private copy constructor creates an immutable duplicate receipt with the SAME ID and shared immutable vehicle/user references. The duplicate must not be inserted as another active entry. Issuing a fresh ticket uses the normal constructor and a new ID. A public copy constructor that silently reuses IDs for new entries would violate uniqueness.
Reference variables and method parameters are values. Conceptually local references are held in stack frames and objects live on the heap; JVM escape analysis may optimize allocations, so physical placement is not guaranteed by this explanation. Clearing a reference does not delete an object while other references remain.

## Alternative and complexity
Default constructor plus setters permits intermediate invalid state and repeats validation; the demo shows an incomplete draft before required setters run. A static factory can validate and choose a subtype/name/cache policy before returning a fully initialized object; the demo issue(...) wraps the validated ticket constructor. Constructor chaining centralizes invariants with no partially initialized object escaping. With a fixed number of fields, all three approaches create n tickets in O(n) time and O(n) retained space, O(1) work per ticket excluding variable-length input validation. Setter call counts differ by a constant; factories do not change Big-O. Default construction is useful for some frameworks but should not force the domain to accept missing required values.

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 4`. Direct demo: `java -cp build/main task04.Task04Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
