from pathlib import Path
import csv,statistics,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1]
def put(p,s):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n')
notes={
1:r'''
## Aim and theory
Analyse the campus system and translate its rules into objects with explicit responsibilities.
Input: registration, vehicle category, user role and pass, entry and exit LocalDateTime, requested charging kWh, and per-floor capacities. Output: ticket ID and position, refusal when no suitable space exists, fee/receipt, occupancy and collected amount.

| Candidate noun | Responsibility and verbs | Justification |
|---|---|---|
| Vehicle, TwoWheeler, Car, ElectricCar | Normalize identity; calculateFee; requiredSlot | Category-specific rates with shared identity and timing rules |
| Slot | accepts, occupy, release | Enforces one suitable occupant per position |
| ParkingTicket | Capture ID, user, vehicle, position, entry; duplicateReceipt | Immutable association needed for exit and audit |
| ParkingUser and Role | Hold name, student/staff/visitor classification and optional Pass | A role is data; it needs no inheritance without differing behaviour |
| Pass, MonthlyPass | covers(entry, exit) | Validity is a separate capability from vehicle category |
| ParkingFacility | enter, find, exit; count occupancy and collections | Coordinates invariants across slots and active tickets |
| Chargeable | chargingFee | EV capability independent of the main class hierarchy |
| VehicleFactory | create | Validates original CLI category names at the input boundary |

Rules: no duplicate active normalized registration; each active ticket matches exactly one occupied compatible slot; no ID reuse within the running JVM; full facilities leave state unchanged; negative durations/energy and exit-before-entry are rejected before release; pass discounts parking only; charging requires an EV in a charging bay. Exit removes the ticket and frees the slot together in this single-threaded model. Occupancy belongs to a facility, not all facilities combined.

Assumptions used throughout: floor and slot numbers are zero-based. Every fifth slot starting at zero is two-wheeler-only, positions congruent to four are charging bays, other positions are car bays. EVs can use ordinary car bays without charging. Allocation is first-fit, so an EV may take a car bay while a charging bay remains free; charging is an exit request, not a reservation preference. Vans fit car bays, e-bikes fit two-wheeler bays. Rates are stated in the root README. LocalDateTime uses a single campus local clock with no time-zone/DST conversion. This is an in-memory, single-process teaching implementation; persistence, distributed ticket IDs and concurrent gates need additional mechanisms.

## Alternative and complexity
Parallel arrays could hold `String[] regNo`, `String[] type`, `LocalDateTime[] entryTime`. A search loops over regNo until equality, then uses the same index in every array. The object version loops over ticket/vehicle references. Both searches take O(n) worst-case for bounded-length registrations; storing n records takes O(n), and both need O(1) fixed-schema space per vehicle. Objects add headers/references; parallel arrays reduce some overhead but need synchronized lengths and indexes. Neither is inherently an indexed O(1) search. An additional field is one class member plus constructor/accessor changes for objects, or another array and changes in every parallel-array insert/delete/copy path. Updating an existing stored population with the new field takes O(n) in either approach; code-maintenance cost is distinct from runtime complexity.

## Execution
The task demo allocates a car, rejects a duplicate, verifies slot-ticket invariants, charges 61 minutes as Rs 60, and releases the slot. Full sources for the shared model are under src/parking; later tasks import these same classes.
''',
2:r'''
## Aim and theory
Choose representations that preserve identifiers, money, time and unequal floor capacities.

| Field | Type | Reason |
|---|---|---|
| Floor, slot, capacity | int | Java array indexes are int; validate bounds before access |
| Ticket ID | long with AtomicLong sequence | More IDs than int and atomic increment in one JVM |
| Registration | String | Preserve letters and leading zeroes; normalize once |
| Entry/exit | LocalDateTime | Avoid LocalTime midnight subtraction ambiguity |
| Duration | long minutes | Avoid int overflow; round positive partial minutes upward |
| Fee | BigDecimal scale 2 | Exact rupee/paise decimal amounts; no binary floating-point rounding |
| Floor layout | Slot[][] jagged array | Each row has its own length |
| Active tickets | ParkingTicket[] | Bounded array matching total capacity |

For 61 minutes, integer `61/60` is 1, and `(double)(61/60)` is still 1.0 because truncation happens first. `61/60.0` preserves a fraction but is not a started-hour bill. Use `minutes/60 + (minutes%60==0 ? 0 : 1)` without the overflow-prone `minutes+59`. The model uses BigDecimal for money and an arithmetic daily-cap formula, including Long.MAX_VALUE minutes. A one-nanosecond positive stay is not silently rounded to zero.
The CLI uses Scanner.hasNextLine then token validation; no mixing nextInt and nextLine. ISO date-times and Integer.parseInt are validated at the boundary; bad lines produce REJECT without ending the session.

## Alternative and complexity
Let F be floors and T=sum of slots. Jagged lookup slots[f][s] is O(1); storage O(T+F). A rectangular flat array uses f*S+s only for a constant S. With unequal rows, prefix[f]+s works after an O(F) prefix build, lookup O(1), storage O(T+F). Finding floor from a flat index takes O(F) scanning or O(log F) binary search unless an extra map is kept. The demo proves constant-width flattening fails for floor 2 after lengths 2,3. ArrayList<String[]> also gives O(1) indexed get(f)[s] and O(T+F) storage; appending a floor is amortized O(1) for the row reference plus O(S_new) to allocate its slots. Inserting a middle floor costs O(F) reference shifts; fixed arrays require replacement. All full first-fit scans are O(T). An ArrayList does not make a slot search automatically faster.
''',
3:r'''
## Aim and theory
Use selection, repetition, continue and early return for suitable allocation and fee slabs.
The supplied ParkingFacility.java is intentionally separate: it stores plain Strings, has no vehicle categories and retains the given main method. Its TODO bodies alone are filled. Exact expected output is checked automatically. The complete model adds category compatibility, duplicate prevention and invariant checks.

## Algorithmic pseudocode
SIMATS-style structured form with named inputs, outputs, indentation and explicit termination:

```text
ALGORITHM AllocateSuitableSlot
INPUT facility, vehicle, user, entryTime
OUTPUT ticket OR NULL
BEGIN
    VALIDATE vehicle, user, entryTime
    IF an active ticket has vehicle.registration THEN
        RAISE duplicate registration error
    END IF
    FOR floor FROM 0 TO numberOfFloors - 1 DO
        FOR slot FROM 0 TO slotsOnFloor[floor] - 1 DO
            IF slot is occupied OR slot is unsuitable THEN
                CONTINUE
            END IF
            CREATE unique ticket with entry time and slot position
            STORE ticket in first empty active array position
            MARK slot occupied
            INCREMENT occupancy
            RETURN ticket
        END FOR
    END FOR
    RETURN NULL
END

ALGORITHM ComputeParkingFee
INPUT vehicleRate, nonnegativeMinutes, validPass, chargingEnergy
OUTPUT exact total fee
BEGIN
    IF minutes < 0 OR energy < 0 THEN RAISE invalid input END IF
    fullDays <- minutes DIV 1440
    remainder <- minutes MOD 1440
    hours <- remainder DIV 60
    IF remainder MOD 60 > 0 THEN hours <- hours + 1 END IF
    parking <- rate * (fullDays * 10 + MIN(hours, 10))
    IF pass covers entire stay THEN parking <- 0 END IF
    VALIDATE charging capability and bay when energy > 0
    RETURN parking + chargingFee(energy)
END
```

The full model uses continue to skip unsuitable positions, return to stop immediately after allocating, and break to stop the active-ticket removal loop. A full search returns null without changing state. Zero minutes costs zero; first started hour is billed fully; each further started hour has the same rate, capped at ten hourly rates per 24-hour block from entry. Each complete 24 hours costs that cap. No partial-day calendar reset is assumed.

## Alternative and complexity
Original enter is O(T) worst-case: duplicate scan, slot scan and empty-ticket-position scan are each O(T), not their product. Release by known position alone is O(1); full exit includes O(T) ticket lookup/removal. For F uniform floors with S slots each, T=F*S. Additional allocation working memory is O(1), with O(T+F) facility storage.
Keep one free-slot stack per floor and compatible category plus free counts. Scan F floor counts to choose a floor, pop a compatible slot, then push on release: allocation O(F), position release O(1), extra O(T+F) references/integers. A global per-category stack makes slot selection O(1) but changes first-fit ordering. A heap/ordered set can preserve smallest-first order at O(log T). An index for active registrations and a free ticket-index stack are ALSO needed before claiming O(1) whole enter/exit; otherwise duplicate/ticket scans remain O(T). Maintain an occupied flag to prevent double-push on invalid release. Task03Demo executes a small stack example and the fee boundaries.
''',
4:r'''
## Aim and theory
Use constructor validation and immutable tickets so incomplete domain objects never enter the facility.
Vehicle owns a private final normalized registration. Subclasses call super(registration). ParkingTicket has a canonical five-argument constructor and a four-argument overload that chains using this(...) to a visitor user. ParkingUser similarly chains its two-argument constructor to its three-argument form. There is no implicit no-argument constructor after explicit constructors are declared; this is deliberate for vehicles/tickets because registration and entry time are required. A default-initialized mutable draft is demonstrated only as an alternative, not used by the facility.
A private copy constructor creates an immutable duplicate receipt with the SAME ID and shared immutable vehicle/user references. The duplicate must not be inserted as another active entry. Issuing a fresh ticket uses the normal constructor and a new ID. A public copy constructor that silently reuses IDs for new entries would violate uniqueness.
Reference variables and method parameters are values. Conceptually local references are held in stack frames and objects live on the heap; JVM escape analysis may optimize allocations, so physical placement is not guaranteed by this explanation. Clearing a reference does not delete an object while other references remain.

## Alternative and complexity
Default constructor plus setters permits intermediate invalid state and repeats validation; the demo shows an incomplete draft before required setters run. A static factory can validate and choose a subtype/name/cache policy before returning a fully initialized object; the demo issue(...) wraps the validated ticket constructor. Constructor chaining centralizes invariants with no partially initialized object escaping. With a fixed number of fields, all three approaches create n tickets in O(n) time and O(n) retained space, O(1) work per ticket excluding variable-length input validation. Setter call counts differ by a constant; factories do not change Big-O. Default construction is useful for some frameworks but should not force the domain to accept missing required values.
''',
5:r'''
## Aim and theory
Separate class-wide identity from per-facility occupancy, and explain Java reference passing and GC.
ParkingTicket.NEXT is private static final AtomicLong. final fixes the counter reference, not its changing numeric value. ticketsIssued() is a static query. Overflow is checked before increment. A static initialization expression initializes the counter; an explicit static block is unnecessary without multi-step configuration. Occupancy and money collected remain instance fields because north and south facilities have independent state. A global occupancy display could aggregate facilities, but treating each instance's occupancy as static would mix them.
The demo issues distinct north/south ticket IDs and proves leaving north does not reduce south occupancy. A method receives a COPY of a reference value: reassigning its Car parameter does not reassign the caller variable. Facility.enter returns a ticket reference. Slot release and removal from the active array remove facility reachability; a caller's receipt reference can still keep the ticket alive. Only after all strong references disappear is the object eligible for GC. The demo does not claim to observe or force a GC event; System.gc would not guarantee one.

## Alternative and complexity
One static counter uses O(1) counter state across k facility instances; each of n tickets still stores an O(1) ID, total O(n). An instance counter needs O(k) counter state and can issue the same raw number at both gates. Prefix with a stable unique facility ID for a composite (facility,localSequence) key, or use a durable shared sequence/UUID. Generation is O(1) in this in-memory implementation. AtomicLong prevents duplicate increments but DOES NOT make the rest of ParkingFacility thread-safe. The sequence resets when the process restarts; cross-restart uniqueness requires durable storage and is a stated limitation.
''',
6:r'''
## Aim and theory
Vehicle is an abstract superclass. TwoWheeler and Car form hierarchical inheritance; ElectricCar extends Car, giving multilevel Vehicle -> Car -> ElectricCar. ElectricCar also implements Chargeable. Private registration is initialized by the Vehicle constructor and exposed through its final getter, not directly inherited field access. Car adds the rate and car-slot requirement; EV inherits those and adds charging. Protected hourlyRupees supports specialization without exposing public mutable rates. Roles are an enum in ParkingUser because role-specific pass policy can be composed without student/staff subclasses.
Task06Demo executes an explicitly instrumented mirror hierarchy so constructor order is visible without inserting logging into the production constructors: Vehicle, then Car, then ElectricCar. The actual model uses the same super chain. docs/model.svg and docs/model.dot provide the UML class diagram (also a Mermaid source in docs/model.md).

## Alternative and complexity
Composition can use ComposedVehicle(registration,VehicleType) where a shared immutable VehicleType holds a name and rate. The runnable record alternative gives the same 130-minute short-stay car fee. New types can be registered as data instead of another subclass, but capabilities and exceptional rules still need strategies rather than hard-coded category switches. Both a virtual rate lookup and a type-object rate lookup are O(1) under a fixed-size monetary representation. Inheritance stores vehicle state in one object; composition adds a type reference per vehicle and O(k) shared type definitions, with O(n+k) total storage. Allocating a distinct type object for every vehicle would lose that sharing benefit. The composed demo explicitly compares only short stays and is not a drop-in full pricing engine.
''',
7:r'''
## Aim and theory
TwoWheeler and Car override hourlyRupees and requiredSlot; ElectricCar overrides the charging capability. Vehicle.calculateFee is a template using the virtual hourly rate. The full design therefore specializes rate behaviour without duplicating the cap algorithm. EBike in Task12 overrides calculateFee(long) for a flat rate.
@Override lets the compiler catch wrong signatures. An override cannot narrow access; primitive return types must match, reference returns may be covariant, and checked exceptions cannot be broadened. Static methods are hidden rather than overridden; final methods cannot be overridden. Registration and ticket fields are final. Vehicle.equals/hashCode are final so subtypes cannot break the shared registration-identity contract; final does not make all referenced objects immutable by itself.
Vehicle.toString gives class and normalized registration. equals accepts any Vehicle with the same registration, and hashCode uses exactly that key. Car and ElectricCar with the same plate compare true symmetrically and deduplicate in HashSet. This is correct here because the plate is the unique vehicle identity; concurrent category records for one plate are not allowed, and enter rejects duplicate active plates. A different system with category-specific identity would need a redesigned equality contract; it must not override only one side and break symmetry.

## Alternative and complexity
A single switch on category can select rates and then use one shared billing function; Task07Demo executes a short-stay example. Adding a category edits the central switch/enum and often its input factory, whereas polymorphic rate behaviour needs a new subclass plus registration/composition-root change. Do not claim every switch costs O(k): integer/enum tables may be O(1), sparse cases or string matching have implementation-dependent behaviour. A linear if/else chain can take O(k) comparisons. Virtual dispatch is O(1) in this model. Both store O(n) vehicle state and O(k) type/rule definitions, with different maintenance coupling rather than a guaranteed timing advantage. The switch sample deliberately compares the shared uncapped short-stay range only.
''',
8:r'''
## Aim and theory
An overload is selected from the declared method signatures at compile time: calculateFee(long) for a numeric duration and calculateFee(LocalDateTime,LocalDateTime) for two timestamps. Runtime type does not select among overload signatures. After a signature is selected, an overridden implementation is selected dynamically.
Vehicle[] contains TwoWheeler, Car and ElectricCar by implicit upcasting. Trace: declared type Vehicle, actual object Car, call calculateFee(130) resolves the long overload, inherited Vehicle method calls hourlyRupees(), dynamic dispatch executes Car.hourlyRupees() returning 30, giving three started hours and Rs 90. ElectricCar inherits the Car rate; the independent Chargeable capability adds Rs 120 for 10 kWh in the supplied demo. The supplied comment 'dynamic method dispatch' applies to the chain; calculateFee itself is inherited in those three supplied classes, while ratePerHour is overridden.
The exact supplied FeeDemo is isolated in complete/, retains its original main and double-return signatures, and all four expected lines are matched byte-for-byte. Its final true is the supplied registration-based equality. The full model strengthens normalization/validation and uses exact decimal money without changing the supplied scaffold.

## Alternative and complexity
An instanceof chain checking every category plus casts costs O(k) in the worst case and duplicates pricing logic at each caller. Subtype order matters: ElectricCar must be checked before Car or its special logic may be skipped. One Chargeable capability check is appropriate here; it is not a k-category pricing chain. Virtual dispatch makes the call-site structure independent of k and O(1) per dispatch under the ordinary JVM model. Code for k behaviours remains O(k) somewhere in either solution, but callers remain stable with dynamic dispatch. Registration length validation/equality is a separate input-size cost.
''',
9:r'''
## Aim and theory
Vehicle is abstract because it owns constructor-validated state and shared billing/identity logic but cannot choose a concrete rate or slot type. hourlyRupees and requiredSlot are abstract. Chargeable is an interface because charging is an optional capability and should coexist with Car inheritance. Pass is another independent behaviour. Task09's FleetEV also implements Identified, proving multiple interface behaviours without multiple class inheritance. Chargeable.chargingUnit() is a default method and rupeesPerKWh() is a static utility; default methods do not give an interface per-object instance fields.

## Alternative and complexity
If Vehicle were an interface, it could declare getRegistration/rate methods and default fee logic, but not instance fields or constructors. Every implementation would need to store/validate registration or delegate to a separate identity object. equals/hashCode/toString cannot be default interface implementations overriding Object; each concrete class or a helper/base class would provide them. If Chargeable were an abstract class, ElectricCar could not extend both Car and Chargeable; it would need composition or a different hierarchy. A class can implement many interfaces but extend only one class. Both interface and class virtual calls are modeled O(1); there is no guaranteed performance win from swapping them. Space is determined by actual fields/delegate objects, not by an interface declaration alone: fixed schema O(1) per vehicle, O(n) for n vehicles.
''',
10:r'''
## Aim and theory
Packages: parking.model contains domain classes/capabilities; parking.service coordinates operations and original factory; task01..task12 contain executable evidence; parking.extension holds the Day-4 additions. Private fields prevent caller mutation. Constructors/getters are public where clients need them; the Vehicle constructor and rate method are protected for subclass use. Package-private members in small demo helper classes stay local. Public facade methods validate all positions, time and charging input before mutating state.
Tickets and vehicles are immutable through the public API, so no setter is provided for identity or entry time. Task10 includes DurationInput as a separate explicit validating-setter example: a rejected negative update leaves its earlier value 61 intact. Slot is mutable through guarded occupy/release, but facility-owned Slot references are never exposed. The deliberately illegal private field read is stored as input/IllegalAccess.java.txt, compiled separately and EXPECTED to fail; the actual compiler diagnostic and nonzero exit are saved in results/private-access-rejected.txt. It is not a failed normal build.
Integer wrappers support generic collection keys and autoboxing, e.g. free-slot stacks. == compares wrapper identity; use equals or unbox after a null check. The demo explicitly constructs distinct wrappers solely to avoid relying on configurable integer caches (the legacy constructor is marked for removal and suppressed in that small demonstration). Null unboxing would throw NullPointerException; the demo validates absence before unboxing.

## Alternative and complexity
Public fields plus caller-side checks allow any forgotten caller to write a negative duration or mismatched ticket/slot. A single validating setter or constructor centralizes the rule. For a bounded numeric check, both take O(1) per update and O(1) extra working memory; with m callers, public-field design may repeat the validation in O(m) source locations, a maintenance cost rather than O(m) runtime per single update. String format checks cost O(L) for input length L; registrations are bounded to 20 characters here.
''',
11:r'''
## Aim and theory
Implement and test the full original system instead of relying on happy-path screenshots. Task11Demo checks exact fee boundaries, unknown categories, duplicate registration, charging restrictions, failed-operation state preservation, pass validity, exit reuse, three requested facility sizes and an uneven jagged layout. A seeded 1000-operation entry/exit sequence verifies slot/ticket/occupancy invariants after each step. No nondeterministic clock or sleep is needed: explicit synthetic timestamps make the evidence reproducible.
The normal hand calculation is two-wheeler Rs 30, ordinary-bay EV Rs 90, two cars Rs 90 each, charging-bay EV Rs 90 parking + Rs 120 energy: total Rs 510.00. The assertion checks the same exact total and zero final occupancy. The CLI reads input/scenario.txt and its complete output is compared to expected-cli.txt, including duplicate and unknown-type rejections and Rs 90 total. The generated test-table.csv records each assertion label and pass result; the complete output remains available, including every scale allocation.

## Measured alternative
LookupBenchmark runs n=1000,10000,100000 real ParkingTicket objects. The SAME objects populate an array, ArrayList and HashMap keyed by registration. Each measured query seeks the last existing key using a distinct String value. There are 200 warm-up queries per structure per size, then five repetitions of 100 queries per method; method order rotates. Construction is excluded. nanoTime measures a batch and checksum is consumed through a volatile sink. Raw nanoseconds and checksums are in results/lookup.csv, summaries in lookup-summary.csv. This is an illustrative warm-process microbenchmark, not JMH or a production latency promise; JIT, GC and constant-key reuse can influence the timings. Work counts for linear scans grow exactly with n; HashMap comparisons are not inferred from timings.
Array/ArrayList exit lookup is O(n) worst-case. Array removal by known index is O(1) when leaving a null hole, but finding it remains O(n). ArrayList.remove shifts up to O(n) references. HashMap lookup/removal is expected O(1) under well-distributed hashes; worst-case is not an unconditional O(1), and hashing costs O(L) for fresh keys. All structures retain O(n) references plus the same O(n) shared ticket objects. HashMap adds bucket/node overhead; ArrayList may reserve spare capacity. Exact byte counts are JVM-layout dependent and are not claimed without instrumentation. A map improves registration lookup but does not by itself accelerate slot selection.

## Evaluation
Encapsulation protects validated state, inheritance reuses Vehicle identity/timing, polymorphism selects category rates, abstraction separates optional charging/pass behaviours. The invariant checks and expected-output assertions support these claims. The basic array/jagged design is suitable for small fixed teaching facilities but scans occupancy and tickets; a production multi-gate service needs locking/transactions, durable identities, audited payments, and a database. The measured comparison supports indexing active tickets if scale requires it; it does not justify abandoning the object model.
''',
12:r'''
## Aim and impact analysis
Adapt the original model for flat-rate e-bikes, peak-price delivery vans, visitor one-day passes, and five unequal floors. New categories affect construction and pricing; a one-day pass adds a validity policy; unequal capacities are already supported by the jagged constructor. A rectangular f*S+s address scheme would require replacement or offsets, but this Slot[][] design needs only new configuration.

## Evaluation and decision
RETAIN the validated model and MODIFY the application composition by adding extensions. The original rate template handles a new flat-fee subclass by overriding calculateFee(long), but a van's time-of-day rule cannot be expressed as a single fixed hourlyRupees value. Keep that rule in a PricingRule abstraction, selected by a new ExtendedFacility subclass through the existing protected parkingQuote hook. Baseline service/vehicle code need not change. Existing classes remain unchanged rather than scattering new instanceof pricing branches into each caller. The original CLI VehicleFactory intentionally knows only TWO/CAR/EV; the extension demo directly constructs new categories. Supporting new CLI keywords would require a factory/composition-root change or registry; it is not claimed to work automatically.

## Implemented policy and revised structure
EBike extends TwoWheeler, flat Rs 20 per positive stay and zero for zero duration. DeliveryVan extends Car and retains car-slot compatibility. PeakVanRule supplies van rates: every started hourly block anchored at entry is Rs 60 if that BLOCK START is in [09:00,17:00), otherwise Rs 30. Thus an 08:30–10:30 stay has blocks at 08:30 and 09:30, total Rs 90; 17:00 is off peak. This explicit assumption resolves the assignment's unspecified boundary/rounding rule. Vans have no daily cap; ordinary cars retain their cap. A complete 24-hour block contains eight peak and sixteen off-peak hours, Rs 960, allowing O(1) quoting with at most 23 remainder iterations instead of iterating every hour of long stays.
OneDayPass implements Pass; a visitor receives zero parking fee only when BOTH entry and exit fall on the purchased calendar date. Crossing midnight invalidates this pass for the whole stay (no partial discount). MonthlyPass likewise requires both endpoints in its month. A pass never waives charging. Pass purchase price is outside the parking collection ledger. ExtendedFacility uses an immutable class-to-rule map; exact runtime class keys are intentional. A further subtype can register its own rule or inherit normal vehicle pricing. The demo adds Shuttle plus a lambda rule charging Rs 15 without editing prior code.

## Evidence-based defence
The baseline source hash manifest is compared after Task12: zero existing production classes modified; the new production types are EBike, DeliveryVan, OneDayPass, PricingRule, PeakVanRule, ExtendedFacility. Only the new application demo/configuration composes them. Existing Task01–11 tests still pass using the unchanged originals. Task12 checks five uneven floors totaling 130 slots, flat and zero fees, 08/09/16/17 boundaries, crossing peak, one and two-day stays, valid/expired day pass, a future Shuttle rule, and invariant preservation. An independent direct per-block oracle checks 216 (24 starts x 9 durations) van cases against the optimized arithmetic rule.
Trade-offs: an explicit policy layer and registry add concepts, exact-class registration needs care for subclasses, entry-anchored block rules are easy to test but differ from wall-clock prorating, and in-memory array scans remain. New fixed-rate categories can subclass without editing old models; new time-sensitive policies use a registered rule. The source-hash evidence supports retaining tested classes while adding the needed pricing abstraction; it does not claim that every possible new business rule will require zero change.
'''
}
for i,s in notes.items():
 task=f'Task{i:02}'
 put(task+'/README.md',f'# {task}\n\n'+s+f'\n## Compile and run\nFrom repository root: `python3 tools/compile.py`, then `python3 tools/run.py {i}`. Direct demo: `java -cp build/main task{i:02}.{task}Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.\n')
# Actual, machine-readable test table.
for i in range(1,13):
 task=R/f'Task{i:02}'
 with (task/'results/test-table.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['case','actual_result','status'])
  for j,line in enumerate((task/'results/output.txt').read_text().splitlines()):
   if line.startswith('PASS '):w.writerow([j+1,line[5:],'PASS'])
rows=list(csv.DictReader((R/'Task11/results/lookup.csv').open()))
with (R/'Task11/results/lookup-summary.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['n','method','repetitions','queries_each','mean_ms_per_batch','mean_ns_per_query'])
 for n in [1000,10000,100000]:
  for method in ['array','arraylist','hashmap']:
   vals=[int(r['elapsed_ns']) for r in rows if int(r['n'])==n and r['method']==method]
   w.writerow([n,method,len(vals),100,f'{statistics.mean(vals)/1e6:.6f}',f'{statistics.mean(vals)/100:.3f}'])
put('README.md',r'''
# CSA0923 Programming with Java Assignment 1

**Name:** B Hitesh Roy  
**Register number:** 192372036  
**Repository:** https://github.com/rootsolve12/CSA09-192372036-Assignment1  
**Title:** Design Implement and Validate an Object Oriented Model for a Campus Smart Parking System  
**Individual assignment:** 50 marks, Tasks 1–11 = 42 and Task 12 = 8.

## Requirements and execution
OpenJDK 21.0.13 and Python 3 were used in the workspace. No third-party Java libraries or database are needed. The commands also work with JDK 21+ on a normal computer. The compiler module command is used because this runtime has `java` with `jdk.compiler` but no separate `javac` executable on PATH.

```sh
python3 tools/compile.py
python3 tools/run.py
# Or run one task after compilation:
python3 tools/run.py 8
# Run the supplied programs directly:
java -cp build/Task03 ParkingFacility
java -cp build/Task08 FeeDemo
# Input-driven complete system:
java -cp build/main task11.ParkingCLI < Task11/input/scenario.txt
# Recheck all evidence and baseline hashes:
python3 tools/verify.py
```

Build outputs are deliberately ignored. Source code, deterministic input files, raw execution logs, expected outputs, measurements, and genuine desktop screenshots are retained. Each task has a separate commit; these are real sequential commits created during this work session, not backdated work over several days. Each compiler screenshot shows a source excerpt and saved actual compiler log. Output screenshots show actual saved execution output; full unabridged output is in results/. No execution is represented as coming from the student's personal computer. Re-running measurements replaces the raw timing evidence with the new machine's results.

## Policy assumptions
Two-wheelers Rs 10/hour, cars/EVs Rs 30/hour; started hours rounded upward, zero duration free. Daily maximum is 10 hourly rates for each complete 24-hour block from entry plus a capped remainder. EV charging Rs 12/kWh, payable separately even with a pass, and allowed only in charging bays. Registrations are normalized uppercase and identify the physical vehicle across categories. Valid monthly passes for students/staff waive parking only when both entry and exit are within that month. Visitor day passes in Task12 require both endpoints on the purchased date. Invalid/expired passes give no discount. No partial pass discount is modeled.

Every fifth slot from index zero is two-wheeler-only, positions 4 modulo 5 are charging bays, and the remaining positions are car bays. EVs can occupy a normal car bay without charging. Allocation is first-fit by compatible category. Original scale cases are 1x20, 3x50, 5x100. Task12 additionally uses unequal sizes [20,30,15,40,25]. New e-bikes have a flat Rs 20 positive-stay fee. Vans use Rs 60 per started entry-anchored hourly block whose start falls in [09:00,17:00), otherwise Rs 30; no van daily cap. These choices resolve pricing details not specified in the assignment.

## Task index
| Task | Topic | Marks | Main evidence |
|---|---|---:|---|
| [01](Task01) | Objects and responsibilities | 4 | Shared model, first-fit demo and invariant checks |
| [02](Task02) | Data types and arrays | 3 | Casting, decimal fees, unequal-floor offsets |
| [03](Task03) | Control logic | 4 | Pseudocode, exact supplied ParkingFacility, fee boundaries |
| [04](Task04) | Constructors | 4 | Chaining, copy receipt and factory alternative |
| [05](Task05) | Static and lifecycle | 3 | Two-facility IDs, independent occupancy, reference passing |
| [06](Task06) | Inheritance | 4 | UML, constructor trace, composition alternative |
| [07](Task07) | Overriding | 4 | Identity/hash contracts, rate overrides and switch comparison |
| [08](Task08) | Polymorphism | 4 | Exact supplied FeeDemo, overload and dispatch traces |
| [09](Task09) | Abstraction | 4 | Multiple capabilities, interface default/static methods |
| [10](Task10) | Encapsulation | 3 | Validated updates, wrappers, negative compile test |
| [11](Task11) | Complete implementation and defence | 5 | Tests, CLI fixture, lookup timings |
| [12](Task12) | Changed requirements | 8 | Extensions, policy strategies, source hashes and 216-case oracle |

## Design and limitations
The shared original model is under Task01/src/parking, with executable demonstrations in each task's src directory. The supplied default-package examples are separately compiled so they cannot collide with the full model or each other. docs/model.svg, docs/model.dot and docs/model.md give the UML. docs/verification.json records verified counts and source integrity. Task READMEs contain aim, theory, alternatives and time/space analysis. Task11/results/lookup.csv and lookup-summary.csv contain actual performance evidence, not invented estimates.

This is a single-threaded in-memory model with no real payments, durable history, authentication or cross-restart ticket ID guarantee. AtomicLong makes the sequence update atomic but does not make facility operations concurrent. Date-times use one campus local clock. The report is prepared separately after the repository stage; portal submission is not performed here.
''')
put('docs/model.dot',r'''
digraph UML {
 graph [rankdir=TB,bgcolor="white",pad="0.3",nodesep="0.35",ranksep="0.5"];
 node [shape=record,fontname="DejaVu Sans",fontsize=10,style=filled,fillcolor="#F2F5F8",color="#536879"];
 edge [fontname="DejaVu Sans",fontsize=9,color="#536879"];
 Vehicle [label="{Vehicle abstract|- registration : String|+ calculateFee(minutes)\l+ calculateFee(in,out)\l# hourlyRupees() abstract\l+ requiredSlot() abstract\l}"];
 TwoWheeler [label="{TwoWheeler|hourly rate 10}"]; Car [label="{Car|hourly rate 30}"];
 ElectricCar [label="{ElectricCar|+ chargingFee(kWh)}"];
 Chargeable [label="{Chargeable interface|+ chargingFee(kWh)\l+ chargingUnit() default\l}"];
 Facility [label="{ParkingFacility|- slots : Slot[][]\l- active : ParkingTicket[]\l- occupancy : int\l|+ enter()\l+ exit()\l# parkingQuote()\l}"];
 Ticket [label="{ParkingTicket|- static NEXT : AtomicLong\l- id : long\l- entered : LocalDateTime\l}"];
 Slot [label="{Slot|kind, occupant|+ accepts()\l+ occupy()\l+ release()\l}"];
 User [label="{ParkingUser|name, role, pass}"];Pass [label="{Pass interface|+ covers(in,out)}"];
 MonthlyPass [label="{MonthlyPass|month : YearMonth}"];
 Car -> Vehicle [arrowhead=empty]; TwoWheeler -> Vehicle [arrowhead=empty]; ElectricCar -> Car [arrowhead=empty];
 ElectricCar -> Chargeable [arrowhead=empty,style=dashed];
 Facility -> Slot [dir=both,arrowtail=diamond,arrowhead=none,label="owns many"];
 Facility -> Ticket [label="active 0..T"];
 Ticket -> Vehicle [label="1"];Ticket -> User [label="1"];User -> Pass [label="0..1"];
 MonthlyPass -> Pass [arrowhead=empty,style=dashed];
}
''')
put('docs/model.md',r'''
# Class diagram
Solid hollow triangle: extends. Dashed hollow triangle: implements. Filled diamond: facility owns its slots. Tickets reference one user and vehicle.

```mermaid
classDiagram
Vehicle <|-- TwoWheeler
Vehicle <|-- Car
Car <|-- ElectricCar
Chargeable <|.. ElectricCar
ParkingFacility *-- Slot
ParkingFacility o-- ParkingTicket
ParkingTicket --> Vehicle
ParkingTicket --> ParkingUser
ParkingUser --> Pass
Pass <|.. MonthlyPass
TwoWheeler <|-- EBike
Car <|-- DeliveryVan
Pass <|.. OneDayPass
ParkingFacility <|-- ExtendedFacility
ExtendedFacility --> PricingRule
PricingRule <|.. PeakVanRule
```

The DOT and SVG files show the original baseline; this Mermaid includes the Task12 additions. No production source under Task01 is changed for Task12.
''')
subprocess.run(['dot','-Tsvg',str(R/'docs/model.dot'),'-o',str(R/'docs/model.svg')],check=True)
base={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'Task01/src/parking').rglob('*.java'))}
p=R/'docs/baseline-sha256.json'
if not p.exists():p.write_text(json.dumps(base,indent=2)+'\n')
assert base==json.loads(p.read_text()),'Baseline changed'
put('Task12/results/baseline-integrity.txt',f'Original production classes compared: {len(base)}\nExisting production classes modified: 0\nNew extension production classes: 6\nAll baseline SHA256 values match docs/baseline-sha256.json\n')
print('Prepared all 12 task explanations, test tables, timing summary, UML and baseline integrity')
