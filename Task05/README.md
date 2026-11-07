# Task05


## Aim and theory
Separate class-wide identity from per-facility occupancy, and explain Java reference passing and GC.
ParkingTicket.NEXT is private static final AtomicLong. final fixes the counter reference, not its changing numeric value. ticketsIssued() is a static query. Overflow is checked before increment. A static initialization expression initializes the counter; an explicit static block is unnecessary without multi-step configuration. Occupancy and money collected remain instance fields because north and south facilities have independent state. A global occupancy display could aggregate facilities, but treating each instance's occupancy as static would mix them.
The demo issues distinct north/south ticket IDs and proves leaving north does not reduce south occupancy. A method receives a COPY of a reference value: reassigning its Car parameter does not reassign the caller variable. Facility.enter returns a ticket reference. Slot release and removal from the active array remove facility reachability; a caller's receipt reference can still keep the ticket alive. Only after all strong references disappear is the object eligible for GC. The demo does not claim to observe or force a GC event; System.gc would not guarantee one.

## Alternative and complexity
One static counter uses O(1) counter state across k facility instances; each of n tickets still stores an O(1) ID, total O(n). An instance counter needs O(k) counter state and can issue the same raw number at both gates. Prefix with a stable unique facility ID for a composite (facility,localSequence) key, or use a durable shared sequence/UUID. Generation is O(1) in this in-memory implementation. AtomicLong prevents duplicate increments but DOES NOT make the rest of ParkingFacility thread-safe. The sequence resets when the process restarts; cross-restart uniqueness requires durable storage and is a stated limitation.

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 5`. Direct demo: `java -cp build/main task05.Task05Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
