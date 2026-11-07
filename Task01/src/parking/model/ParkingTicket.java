package parking.model;
import java.time.LocalDateTime;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicLong;
public final class ParkingTicket {
    private static final AtomicLong NEXT = new AtomicLong();
    private final long id;
    private final Vehicle vehicle;
    private final ParkingUser user;
    private final int floor, slot;
    private final LocalDateTime entered;
    public ParkingTicket(Vehicle vehicle, ParkingUser user, LocalDateTime entered, int floor, int slot) {
        this.vehicle=Objects.requireNonNull(vehicle); this.user=Objects.requireNonNull(user);
        this.entered=Objects.requireNonNull(entered);
        if(floor<0 || slot<0) throw new IllegalArgumentException("Negative slot");
        this.floor=floor; this.slot=slot;
        id=NEXT.updateAndGet(n -> { if(n==Long.MAX_VALUE) throw new IllegalStateException("Ticket IDs exhausted"); return n+1; });
    }
    public ParkingTicket(Vehicle vehicle, LocalDateTime entered, int floor, int slot) {
        this(vehicle, new ParkingUser("Visitor", ParkingUser.Role.VISITOR), entered, floor, slot);
    }
    private ParkingTicket(ParkingTicket original) {
        id=original.id; vehicle=original.vehicle; user=original.user;
        entered=original.entered; floor=original.floor; slot=original.slot;
    }
    /** Duplicate immutable receipt, never a new active parking entry. */
    public ParkingTicket duplicateReceipt() { return new ParkingTicket(this); }
    public long getId() { return id; }
    public Vehicle getVehicle() { return vehicle; }
    public ParkingUser getUser() { return user; }
    public int getFloor() { return floor; }
    public int getSlot() { return slot; }
    public LocalDateTime getEntered() { return entered; }
    public static long ticketsIssued() { return NEXT.get(); }
}
