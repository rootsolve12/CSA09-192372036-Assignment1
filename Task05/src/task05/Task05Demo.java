package task05;
import parking.model.*; import parking.service.*; import evidence.Check; import java.time.*;
public class Task05Demo {
 static void reassign(Car c){c=new Car("LOCAL99");}
 public static void main(String[] args) {
  var n=new ParkingFacility(new int[]{5});var s=new ParkingFacility(new int[]{5});var now=LocalDateTime.of(2026,1,15,10,0);var u=new ParkingUser("V",ParkingUser.Role.VISITOR);
  var a=n.enter(new Car("NORTH1"),u,now);var b=s.enter(new Car("SOUTH1"),u,now);
  Check.that(a.getId()!=b.getId(),"Shared static sequence across two facilities");
  Check.equal(ParkingTicket.ticketsIssued(),2L,"Class counter counts issued tickets");
  n.exit("NORTH1",now.plusMinutes(30),0);
  Check.equal(n.getOccupancy(),0,"North occupancy is instance state");Check.equal(s.getOccupancy(),1,"South occupancy remains one");
  Car c=new Car("ORIGINAL1");reassign(c);Check.equal(c.getRegistration(),"ORIGINAL1","Java passes reference value by value");
  Check.equal(a.getVehicle().getRegistration(),"NORTH1","Caller still holds exited ticket");
  a=null;System.out.println("Exited ticket can become GC eligible after last caller reference is cleared; GC timing not asserted.");Check.summary();
 }
}
