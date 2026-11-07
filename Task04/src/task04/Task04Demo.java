package task04;
import parking.model.*; import evidence.Check; import java.time.*;
public class Task04Demo {
 static final class Draft {
  Vehicle vehicle; LocalDateTime entered;
  void setVehicle(Vehicle v){if(v==null)throw new IllegalArgumentException();vehicle=v;}
  void setEntered(LocalDateTime t){if(t==null)throw new IllegalArgumentException();entered=t;}
  boolean valid(){return vehicle!=null&&entered!=null;}
 }
 static ParkingTicket issue(Vehicle v,LocalDateTime t){return new ParkingTicket(v,t,0,1);}
 public static void main(String[] args) {
  var c=new Car("TN04DD44");var now=LocalDateTime.of(2026,1,15,10,0);
  var first=new ParkingTicket(c,now,0,1);var copy=first.duplicateReceipt();var next=issue(c,now);
  Check.equal(copy.getId(),first.getId(),"Receipt copy preserves identity");
  Check.that(copy!=first && copy.getVehicle()==first.getVehicle(),"Immutable shallow copy shares immutable identity fields");
  Check.that(next.getId()!=first.getId(),"Static factory issues fresh identity");
  Check.equal(first.getUser().getRole(),ParkingUser.Role.VISITOR,"Overloaded constructor chains to canonical constructor");
  Check.rejects(()->new ParkingTicket(c,now,-1,0),"Invalid constructor position");
  Draft draft=new Draft(); Check.that(!draft.valid(),"Default then setters temporarily incomplete");draft.setVehicle(c);draft.setEntered(now);Check.that(draft.valid(),"Setters complete draft");Check.summary();
 }
}
