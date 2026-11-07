# Task08


## Aim and theory
An overload is selected from the declared method signatures at compile time: calculateFee(long) for a numeric duration and calculateFee(LocalDateTime,LocalDateTime) for two timestamps. Runtime type does not select among overload signatures. After a signature is selected, an overridden implementation is selected dynamically.
Vehicle[] contains TwoWheeler, Car and ElectricCar by implicit upcasting. Trace: declared type Vehicle, actual object Car, call calculateFee(130) resolves the long overload, inherited Vehicle method calls hourlyRupees(), dynamic dispatch executes Car.hourlyRupees() returning 30, giving three started hours and Rs 90. ElectricCar inherits the Car rate; the independent Chargeable capability adds Rs 120 for 10 kWh in the supplied demo. The supplied comment 'dynamic method dispatch' applies to the chain; calculateFee itself is inherited in those three supplied classes, while ratePerHour is overridden.
The exact supplied FeeDemo is isolated in complete/, retains its original main and double-return signatures, and all four expected lines are matched byte-for-byte. Its final true is the supplied registration-based equality. The full model strengthens normalization/validation and uses exact decimal money without changing the supplied scaffold.

## Alternative and complexity
An instanceof chain checking every category plus casts costs O(k) in the worst case and duplicates pricing logic at each caller. Subtype order matters: ElectricCar must be checked before Car or its special logic may be skipped. One Chargeable capability check is appropriate here; it is not a k-category pricing chain. Virtual dispatch makes the call-site structure independent of k and O(1) per dispatch under the ordinary JVM model. Code for k behaviours remains O(k) somewhere in either solution, but callers remain stable with dynamic dispatch. Registration length validation/equality is a separate input-size cost.

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 8`. Direct demo: `java -cp build/main task08.Task08Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
