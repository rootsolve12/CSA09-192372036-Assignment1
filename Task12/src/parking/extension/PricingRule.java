package parking.extension;
import parking.model.Vehicle; import java.math.BigDecimal; import java.time.LocalDateTime;
@FunctionalInterface
public interface PricingRule { BigDecimal quote(Vehicle vehicle,LocalDateTime in,LocalDateTime out); }
