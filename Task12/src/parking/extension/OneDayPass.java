package parking.extension;
import parking.model.Pass; import java.time.*; import java.util.Objects;
public final class OneDayPass implements Pass {
 private final LocalDate date;
 public OneDayPass(LocalDate date){this.date=Objects.requireNonNull(date);}
 @Override public boolean covers(LocalDateTime in,LocalDateTime out) {
  return !out.isBefore(in) && in.toLocalDate().equals(date) && out.toLocalDate().equals(date);
 }
}
