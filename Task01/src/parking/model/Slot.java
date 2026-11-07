package parking.model;
import java.util.Objects;
public final class Slot {
    public enum Kind { TWO_WHEELER, CAR, CHARGING }
    private final int floor, number;
    private final Kind kind;
    private Vehicle occupant;
    public Slot(int floor, int number, Kind kind) {
        if (floor < 0 || number < 0) throw new IllegalArgumentException("Negative slot position");
        this.floor=floor; this.number=number; this.kind=Objects.requireNonNull(kind);
    }
    public boolean accepts(Vehicle v) {
        Objects.requireNonNull(v);
        return kind == v.requiredSlot() || (kind == Kind.CHARGING && v instanceof Chargeable);
    }
    public void occupy(Vehicle vehicle) {
        if (occupant != null || !accepts(vehicle)) throw new IllegalStateException("Occupied or unsuitable slot");
        occupant=vehicle;
    }
    public void release() {
        if (occupant == null) throw new IllegalStateException("Slot already free");
        occupant=null;
    }
    public boolean isFree() { return occupant==null; }
    public int getFloor() { return floor; }
    public int getNumber() { return number; }
    public Kind getKind() { return kind; }
    public String getRegistration() { return occupant==null ? null : occupant.getRegistration(); }
}
