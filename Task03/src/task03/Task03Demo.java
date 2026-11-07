package task03;
import parking.model.*; import parking.service.*; import evidence.Check;
import java.time.*; import java.util.*;
public class Task03Demo {
 public static void main(String[] args) {
  Car c=new Car("TN03CC33"); long[] minutes={0,1,60,61,600,601,1440,1441};
  String[] fees={"0.00","30.00","30.00","60.00","300.00","300.00","300.00","330.00"};
  for(int i=0;i<minutes.length;i++) Check.equal(c.calculateFee(minutes[i]).toPlainString(),fees[i],"Slab minutes="+minutes[i]);
  ParkingFacility p=new ParkingFacility(new int[]{2,1}); var u=new ParkingUser("V",ParkingUser.Role.VISITOR);var now=LocalDateTime.of(2026,1,15,10,0);
  p.enter(c,u,now); Check.equal(p.enter(new Car("TN03DD44"),u,now),null,"No suitable car space");
  Check.that(p.invariantHolds(),"Full car capacity leaves state valid");
  Deque<Integer> free=new ArrayDeque<>();free.push(2);free.push(1);free.push(0);
  int s=free.pop(); Check.equal(s,0,"Free stack allocation");free.push(s);Check.equal(free.size(),3,"Free stack release");
  Check.summary();
 }
}
