# Task09


## Aim and theory
Vehicle is abstract because it owns constructor-validated state and shared billing/identity logic but cannot choose a concrete rate or slot type. hourlyRupees and requiredSlot are abstract. Chargeable is an interface because charging is an optional capability and should coexist with Car inheritance. Pass is another independent behaviour. Task09's FleetEV also implements Identified, proving multiple interface behaviours without multiple class inheritance. Chargeable.chargingUnit() is a default method and rupeesPerKWh() is a static utility; default methods do not give an interface per-object instance fields.

## Alternative and complexity
If Vehicle were an interface, it could declare getRegistration/rate methods and default fee logic, but not instance fields or constructors. Every implementation would need to store/validate registration or delegate to a separate identity object. equals/hashCode/toString cannot be default interface implementations overriding Object; each concrete class or a helper/base class would provide them. If Chargeable were an abstract class, ElectricCar could not extend both Car and Chargeable; it would need composition or a different hierarchy. A class can implement many interfaces but extend only one class. Both interface and class virtual calls are modeled O(1); there is no guaranteed performance win from swapping them. Space is determined by actual fields/delegate objects, not by an interface declaration alone: fixed schema O(1) per vehicle, O(n) for n vehicles.

## Compile and run
From repository root: `python3 tools/compile.py`, then `python3 tools/run.py 9`. Direct demo: `java -cp build/main task09.Task09Demo`. See results/compiler.txt and execution.txt for actual evidence, and screenshots/ for captured compiler/output views.
