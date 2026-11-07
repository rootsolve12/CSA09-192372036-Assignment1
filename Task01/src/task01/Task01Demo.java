package task01;
import parking.model.*; import parking.service.*; import evidence.Check;
import java.time.*;
public class Task01Demo {
 public static void main(String[] args) {
  ParkingFacility p=new ParkingFacility(new int[]{5,10});
  var t=p.enter(new Car("TN01AB1111"),new ParkingUser("Visitor",ParkingUser.Role.VISITOR),LocalDateTime.of(2026,1,15,10,0));
  Check.that(t!=null && t.getFloor()==0 && t.getSlot()==1,"First suitable free car slot");
  Check.rejects(()->p.enter(new Car("tn01ab1111"),t.getUser(),t.getEntered()),"Duplicate registration");
  Check.that(p.invariantHolds(),"One active ticket per occupied slot");
  Check.equal(p.exit("TN01AB1111",t.getEntered().plusMinutes(61),0).toPlainString(),"60.00","Visitor fee output");
  Check.equal(p.getOccupancy(),0,"Release on exit");
  Check.that(p.invariantHolds(),"Invariants after release"); Check.summary();
 }
}
