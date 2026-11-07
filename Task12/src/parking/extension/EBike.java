package parking.extension;
import parking.model.TwoWheeler; import java.math.BigDecimal;
public final class EBike extends TwoWheeler {
 public EBike(String registration){super(registration);}
 @Override public BigDecimal calculateFee(long minutes) {
  if(minutes<0)throw new IllegalArgumentException("Negative duration");
  return new BigDecimal(minutes==0?"0.00":"20.00");
 }
}
