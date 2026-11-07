# Task10


## Aim and theory
Packages: parking.model contains domain classes/capabilities; parking.service coordinates operations and original factory; task01..task12 contain executable evidence; parking.extension holds the Day-4 additions. Private fields prevent caller mutation. Constructors/getters are public where clients need them; the Vehicle constructor and rate method are protected for subclass use. Package-private members in small demo helper classes stay local. Public facade methods validate all positions, time and charging input before mutating state.
Tickets and vehicles are immutable through the public API, so no setter is provided for identity or entry time. Task10 includes DurationInput as a separate explicit validating-setter example: a rejected negative update leaves its earlier value 61 intact. Slot is mutable through guarded occupy/release, but facility-owned Slot references are never exposed. The deliberately illegal private field read is stored as input/IllegalAccess.java.txt, compiled separately and EXPECTED to fail; the actual compiler diagnostic and nonzero exit are saved in results/private-access-rejected.txt. It is not a failed normal build.
Integer wrappers support generic collection keys and autoboxing, e.g. free-slot stacks. == compares wrapper identity; use equals or unbox after a null check. The demo explicitly constructs distinct wrappers solely to avoid relying on configurable integer caches (the legacy constructor is marked for removal and suppressed in that small demonstration). Null unboxing would throw NullPointerException; the demo validates absence before unboxing.

## Alternative and complexity
Public fields plus caller-side checks allow any forgotten caller to write a negative duration or mismatched ticket/slot. A single validating setter or constructor centralizes the rule. For a bounded numeric check, both take O(1) per update and O(1) extra working memory; with m callers, public-field design may repeat the validation in O(m) source locations, a maintenance cost rather than O(m) runtime per single update. String format checks cost O(L) for input length L; registrations are bounded to 20 characters here.

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 10`. Direct demo: `java -cp build/main task10.Task10Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
