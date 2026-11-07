package parking.model;
public class Car extends Vehicle {
    public Car(String registration) { super(registration); }
    @Override protected long hourlyRupees() { return 30; }
    @Override public Slot.Kind requiredSlot() { return Slot.Kind.CAR; }
}
