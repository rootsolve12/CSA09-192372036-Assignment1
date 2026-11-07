# Task02


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

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 2`. Direct demo: `java -cp build/main task02.Task02Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
