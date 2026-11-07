package parking.model;
import java.math.BigDecimal;
import java.time.*;
import java.util.*;
public abstract class Vehicle {
    private final String registration;
    protected Vehicle(String registration) {
        if (registration == null || !registration.trim().matches("[A-Za-z0-9-]{2,20}"))
            throw new IllegalArgumentException("Registration must contain 2 to 20 letters digits or hyphens");
        this.registration = registration.trim().toUpperCase(Locale.ROOT);
    }
    public final String getRegistration() { return registration; }
    protected abstract long hourlyRupees();
    public abstract Slot.Kind requiredSlot();
    public BigDecimal calculateFee(long minutes) {
        if (minutes < 0) throw new IllegalArgumentException("Negative duration");
        long fullDays = minutes / 1440;
        long remainder = minutes % 1440;
        long hours = remainder / 60 + (remainder % 60 == 0 ? 0 : 1);
        BigDecimal rate = BigDecimal.valueOf(hourlyRupees());
        return rate.multiply(BigDecimal.valueOf(fullDays).multiply(BigDecimal.TEN)
                .add(BigDecimal.valueOf(Math.min(hours, 10)))).setScale(2);
    }
    public BigDecimal calculateFee(LocalDateTime in, LocalDateTime out) {
        return calculateFee(billableMinutes(in, out));
    }
    public static long billableMinutes(LocalDateTime in, LocalDateTime out) {
        Objects.requireNonNull(in); Objects.requireNonNull(out);
        Duration d = Duration.between(in, out);
        if (d.isNegative()) throw new IllegalArgumentException("Exit before entry");
        return d.toMinutes() + (d.getSeconds() % 60 != 0 || d.getNano() != 0 ? 1 : 0);
    }
    @Override public final boolean equals(Object other) {
        return other instanceof Vehicle v && registration.equals(v.registration);
    }
    @Override public final int hashCode() { return registration.hashCode(); }
    @Override public String toString() { return getClass().getSimpleName()+"("+registration+")"; }
}
