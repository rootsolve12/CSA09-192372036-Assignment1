# Task06


## Aim and theory
Vehicle is an abstract superclass. TwoWheeler and Car form hierarchical inheritance; ElectricCar extends Car, giving multilevel Vehicle -> Car -> ElectricCar. ElectricCar also implements Chargeable. Private registration is initialized by the Vehicle constructor and exposed through its final getter, not directly inherited field access. Car adds the rate and car-slot requirement; EV inherits those and adds charging. Protected hourlyRupees supports specialization without exposing public mutable rates. Roles are an enum in ParkingUser because role-specific pass policy can be composed without student/staff subclasses.
Task06Demo executes an explicitly instrumented mirror hierarchy so constructor order is visible without inserting logging into the production constructors: Vehicle, then Car, then ElectricCar. The actual model uses the same super chain. docs/model.svg and docs/model.dot provide the UML class diagram (also a Mermaid source in docs/model.md).

## Alternative and complexity
Composition can use ComposedVehicle(registration,VehicleType) where a shared immutable VehicleType holds a name and rate. The runnable record alternative gives the same 130-minute short-stay car fee. New types can be registered as data instead of another subclass, but capabilities and exceptional rules still need strategies rather than hard-coded category switches. Both a virtual rate lookup and a type-object rate lookup are O(1) under a fixed-size monetary representation. Inheritance stores vehicle state in one object; composition adds a type reference per vehicle and O(k) shared type definitions, with O(n+k) total storage. Allocating a distinct type object for every vehicle would lose that sharing benefit. The composed demo explicitly compares only short stays and is not a drop-in full pricing engine.

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 6`. Direct demo: `java -cp build/main task06.Task06Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
