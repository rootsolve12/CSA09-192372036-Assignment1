package parking.extension;
import parking.model.Vehicle; import java.math.BigDecimal; import java.time.*;
public final class PeakVanRule implements PricingRule {
 @Override public BigDecimal quote(Vehicle vehicle,LocalDateTime in,LocalDateTime out) {
  if(!(vehicle instanceof DeliveryVan))throw new IllegalArgumentException("Van rule requires van");
  long minutes=Vehicle.billableMinutes(in,out);long blocks=minutes/60+(minutes%60==0?0:1);
  // Entry-anchored started hours: each block uses its start time. Daily car cap
  // deliberately does not apply to vans. Full 24-hour runs always include 8 peak blocks.
  long days=blocks/24, remainder=blocks%24;
  BigDecimal fee=BigDecimal.valueOf(days).multiply(new BigDecimal("960.00"));
  LocalDateTime block=in;
  for(long i=0;i<remainder;i++,block=block.plusHours(1))
   fee=fee.add(BigDecimal.valueOf(block.getHour()>=9 && block.getHour()<17?60:30));
  return fee.setScale(2);
 }
}
