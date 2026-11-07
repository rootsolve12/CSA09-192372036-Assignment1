package parking.model;
import java.math.BigDecimal;
public interface Chargeable {
    BigDecimal chargingFee(int kWh);
    default String chargingUnit() { return "kWh"; }
    static BigDecimal rupeesPerKWh() { return new BigDecimal("12.00"); }
}
