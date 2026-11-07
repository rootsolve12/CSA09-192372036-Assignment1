package parking.extension;
import parking.model.*; import parking.service.ParkingFacility;
import java.math.BigDecimal; import java.time.*; import java.util.*;
public final class ExtendedFacility extends ParkingFacility {
 private final Map<Class<? extends Vehicle>,PricingRule> rules;
 public ExtendedFacility(int[] sizes,Map<Class<? extends Vehicle>,PricingRule> rules) {
  super(sizes);this.rules=Map.copyOf(rules);
 }
 @Override protected BigDecimal parkingQuote(ParkingTicket ticket,LocalDateTime out) {
  Vehicle vehicle=ticket.getVehicle(); PricingRule rule=rules.get(vehicle.getClass());
  return rule==null?super.parkingQuote(ticket,out):rule.quote(vehicle,ticket.getEntered(),out);
 }
}
