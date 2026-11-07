# Task03


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

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 3`. Direct demo: `java -cp build/main task03.Task03Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
