package parking.model;
import java.time.*;
import java.util.Objects;
public final class MonthlyPass implements Pass {
    private final YearMonth month;
    public MonthlyPass(YearMonth month) { this.month=Objects.requireNonNull(month); }
    @Override public boolean covers(LocalDateTime in, LocalDateTime out) {
        return !out.isBefore(in) && YearMonth.from(in).equals(month) && YearMonth.from(out).equals(month);
    }
}
