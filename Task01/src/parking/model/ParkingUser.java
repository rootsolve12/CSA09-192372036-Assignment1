package parking.model;
import java.util.Objects;
public final class ParkingUser {
    public enum Role { STUDENT, STAFF, VISITOR }
    private final String name;
    private final Role role;
    private final Pass pass;
    public ParkingUser(String name, Role role) { this(name, role, null); }
    public ParkingUser(String name, Role role, Pass pass) {
        if(name==null || name.isBlank()) throw new IllegalArgumentException("Blank name");
        this.name=name; this.role=Objects.requireNonNull(role);
        if(role==Role.VISITOR && pass instanceof MonthlyPass)
            throw new IllegalArgumentException("Monthly passes are for staff and students");
        this.pass=pass;
    }
    public String getName() { return name; }
    public Role getRole() { return role; }
    public Pass getPass() { return pass; }
}
