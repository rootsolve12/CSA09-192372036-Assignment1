# Task07


## Aim and theory
TwoWheeler and Car override hourlyRupees and requiredSlot; ElectricCar overrides the charging capability. Vehicle.calculateFee is a template using the virtual hourly rate. The full design therefore specializes rate behaviour without duplicating the cap algorithm. EBike in Task12 overrides calculateFee(long) for a flat rate.
@Override lets the compiler catch wrong signatures. An override cannot narrow access; primitive return types must match, reference returns may be covariant, and checked exceptions cannot be broadened. Static methods are hidden rather than overridden; final methods cannot be overridden. Registration and ticket fields are final. Vehicle.equals/hashCode are final so subtypes cannot break the shared registration-identity contract; final does not make all referenced objects immutable by itself.
Vehicle.toString gives class and normalized registration. equals accepts any Vehicle with the same registration, and hashCode uses exactly that key. Car and ElectricCar with the same plate compare true symmetrically and deduplicate in HashSet. This is correct here because the plate is the unique vehicle identity; concurrent category records for one plate are not allowed, and enter rejects duplicate active plates. A different system with category-specific identity would need a redesigned equality contract; it must not override only one side and break symmetry.

## Alternative and complexity
A single switch on category can select rates and then use one shared billing function; Task07Demo executes a short-stay example. Adding a category edits the central switch/enum and often its input factory, whereas polymorphic rate behaviour needs a new subclass plus registration/composition-root change. Do not claim every switch costs O(k): integer/enum tables may be O(1), sparse cases or string matching have implementation-dependent behaviour. A linear if/else chain can take O(k) comparisons. Virtual dispatch is O(1) in this model. Both store O(n) vehicle state and O(k) type/rule definitions, with different maintenance coupling rather than a guaranteed timing advantage. The switch sample deliberately compares the shared uncapped short-stay range only.

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 7`. Direct demo: `java -cp build/main task07.Task07Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
