# Task01


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

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 1`. Direct demo: `java -cp build/main task01.Task01Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
