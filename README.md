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
