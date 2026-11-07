package task11;
import parking.model.*; import parking.service.*; import evidence.Check;
import java.time.*; import java.math.*; import java.util.*;
public class Task11Demo {
 static final LocalDateTime TIME=LocalDateTime.of(2026,1,15,10,0);
 static final ParkingUser VISITOR=new ParkingUser("Visitor",ParkingUser.Role.VISITOR);
 static void fee(Vehicle v,long minutes,String expected) { Check.equal(v.calculateFee(minutes).toPlainString(),expected,"Fee "+v.getClass().getSimpleName()+" minutes="+minutes); }
 public static void main(String[] args) {
  fee(new Car("CA11"),0,"0.00");fee(new Car("CA11"),60,"30.00");fee(new Car("CA11"),61,"60.00");
  fee(new Car("CA11"),600,"300.00");fee(new Car("CA11"),601,"300.00");fee(new Car("CA11"),1440,"300.00");fee(new Car("CA11"),1441,"330.00");
  Check.rejects(()->new Car("CA11").calculateFee(-1),"Negative duration");
  Check.rejects(()->VehicleFactory.create("PLANE","PL11"),"Unknown type");
  Check.rejects(()->new Car(" "),"Blank registration");
  ParkingFacility p=new ParkingFacility(new int[]{5});
  p.enter(new TwoWheeler("TW11"),VISITOR,TIME);p.enter(new ElectricCar("EV11A"),VISITOR,TIME);
  p.enter(new Car("CA11A"),VISITOR,TIME);p.enter(new Car("CA11B"),VISITOR,TIME);
  var last=p.enter(new ElectricCar("EV11B"),VISITOR,TIME);
  Check.equal(last.getSlot(),4,"Last suitable free slot is charging bay");
  Check.equal(p.enter(new Car("FULL11"),VISITOR,TIME),null,"Full facility returns no ticket");
  Check.rejects(()->p.enter(new Car("CA11A"),VISITOR,TIME),"Duplicate registration rejected");
  Check.rejects(()->p.exit("CA11A",TIME.minusSeconds(1),0),"Exit before entry");
  Check.rejects(()->p.exit("EV11A",TIME.plusMinutes(130),10),"Charging requested in ordinary car bay");
  Check.equal(p.getOccupancy(),5,"Failed operations preserve occupancy");
  Check.equal(p.exit("TW11",TIME.plusMinutes(130),0).toPlainString(),"30.00","Two wheeler visitor");
  Check.equal(p.exit("EV11A",TIME.plusMinutes(130),0).toPlainString(),"90.00","EV ordinary bay parking only");
  Check.equal(p.exit("CA11A",TIME.plusMinutes(130),0).toPlainString(),"90.00","First car visitor");
  Check.equal(p.exit("CA11B",TIME.plusMinutes(130),0).toPlainString(),"90.00","Second car visitor");
  Check.equal(p.exit("EV11B",TIME.plusMinutes(130),10).toPlainString(),"210.00","Charging bay EV parking plus energy");
  Check.equal(p.getCollected().toPlainString(),"510.00","Hand total 30+90+90+90+210=510");
  Check.that(p.getOccupancy()==0 && p.invariantHolds(),"All slots and tickets released consistently");
  Check.rejects(()->p.exit("CA11A",TIME.plusHours(3),0),"Repeated exit");
  var staff=new ParkingUser("Staff",ParkingUser.Role.STAFF,new MonthlyPass(YearMonth.of(2026,1)));
  p.enter(new Car("STAFF11"),staff,TIME);Check.equal(p.exit("STAFF11",TIME.plusHours(3),0).toPlainString(),"0.00","Valid monthly pass parking free");
  var expired=new ParkingUser("Student",ParkingUser.Role.STUDENT,new MonthlyPass(YearMonth.of(2025,12)));
  p.enter(new Car("EXPIRED11"),expired,TIME);Check.equal(p.exit("EXPIRED11",TIME.plusHours(1),0).toPlainString(),"30.00","Expired pass charged normally");
  for(int[] size:new int[][]{{20},{50,50,50},{100,100,100,100,100},{2,4,1,7,3}}) {
   ParkingFacility scale=new ParkingFacility(size);int n=0;Vehicle[] types={new TwoWheeler("TWXX"),new Car("CAXX"),new ElectricCar("EVXX")};
   for(int f=0;f<size.length;f++) for(int s=0;s<size[f];s++) {
    Vehicle v=scale.slotKind(f,s)==Slot.Kind.TWO_WHEELER?new TwoWheeler("TW"+n):scale.slotKind(f,s)==Slot.Kind.CHARGING?new ElectricCar("EV"+n):new Car("CA"+n);
    Check.that(scale.enter(v,VISITOR,TIME)!=null,"Scale allocation "+Arrays.toString(size)+" entry="+n);n++;
   }
   Check.equal(scale.getOccupancy(),scale.capacity(),"Exact scale capacity "+scale.capacity());Check.that(scale.invariantHolds(),"Scale invariant");
  }
  // Repeated operations exercise release reuse and invariant preservation.
  ParkingFacility random=new ParkingFacility(new int[]{7,3,11}); Random rng=new Random(192372036);List<String> live=new ArrayList<>();
  for(int step=0;step<1000;step++) {
   if(!live.isEmpty() && rng.nextBoolean()) {String reg=live.remove(rng.nextInt(live.size()));random.exit(reg,TIME.plusHours(1),0);}
   else {String reg="R"+step;Vehicle v=switch(rng.nextInt(3)){case 0->new TwoWheeler(reg);case 1->new Car(reg);default->new ElectricCar(reg);};if(random.enter(v,VISITOR,TIME)!=null)live.add(reg);}
   if(!random.invariantHolds() || random.getOccupancy()!=live.size())throw new AssertionError("Random invariant at "+step);
  }
  Check.that(true,"1000 seeded enter exit operations preserve invariants");Check.summary();
 }
}
