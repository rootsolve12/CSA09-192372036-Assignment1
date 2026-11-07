package parking.model;
public class TwoWheeler extends Vehicle {
    public TwoWheeler(String registration) { super(registration); }
    @Override protected long hourlyRupees() { return 10; }
    @Override public Slot.Kind requiredSlot() { return Slot.Kind.TWO_WHEELER; }
}
