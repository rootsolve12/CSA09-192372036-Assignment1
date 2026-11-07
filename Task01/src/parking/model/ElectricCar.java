package parking.model;
import java.math.BigDecimal;
public class ElectricCar extends Car implements Chargeable {
    public ElectricCar(String registration) { super(registration); }
    @Override public BigDecimal chargingFee(int kWh) {
        if (kWh < 0) throw new IllegalArgumentException("Negative energy");
        return rupees(kWh);
    }
    private BigDecimal rupees(int kWh) { return Chargeable.rupeesPerKWh().multiply(BigDecimal.valueOf(kWh)); }
}
