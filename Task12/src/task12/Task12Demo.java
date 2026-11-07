package task12;
import parking.model.*; import parking.extension.*; import evidence.Check;
import java.time.*; import java.util.*; import java.math.*;
public class Task12Demo {
 static final LocalDateTime DATE=LocalDateTime.of(2026,1,15,9,0);
 static final ParkingUser VISITOR=new ParkingUser("Visitor",ParkingUser.Role.VISITOR);
 static class Shuttle extends Car { Shuttle(String reg){super(reg);} }
 public static void main(String[] args) {
  var p=new ExtendedFacility(new int[]{20,30,15,40,25},Map.of(DeliveryVan.class,new PeakVanRule()));
  Check.equal(p.floors(),5,"Five jagged floors");Check.equal(p.capacity(),130,"Unequal floor total");
  p.enter(new EBike("EB12"),VISITOR,DATE);Check.equal(p.exit("EB12",DATE.plusHours(7),0).toPlainString(),"20.00","E bike flat fee");
  Check.equal(new EBike("EB00").calculateFee(0).toPlainString(),"0.00","Zero minute e bike");
  PeakVanRule rule=new PeakVanRule();var van=new DeliveryVan("VAN12");
  for(int hour:new int[]{8,9,16,17}) {var in=DATE.withHour(hour);Check.equal(rule.quote(van,in,in.plusHours(1)).toPlainString(),hour==9||hour==16?"60.00":"30.00","Van boundary hour="+hour);}
  var in=DATE.withHour(8).withMinute(30);Check.equal(rule.quote(van,in,in.plusHours(2)).toPlainString(),"90.00","Cross peak boundary uses 08:30 and 09:30 block starts");
  Check.equal(rule.quote(van,DATE,DATE.plusHours(24)).toPlainString(),"960.00","24 hours equals 8 peak plus 16 off peak");
  Check.equal(rule.quote(van,DATE,DATE.plusHours(49)).toPlainString(),"1980.00","Two full days plus peak block");
  p.enter(van,VISITOR,DATE);Check.equal(p.exit("VAN12",DATE.plusHours(2),0).toPlainString(),"120.00","Facility dispatches van pricing strategy");
  var passUser=new ParkingUser("Day visitor",ParkingUser.Role.VISITOR,new OneDayPass(DATE.toLocalDate()));
  p.enter(new Car("DAY12"),passUser,DATE);Check.equal(p.exit("DAY12",DATE.plusHours(5),0).toPlainString(),"0.00","One day visitor pass");
  p.enter(new Car("EX12"),passUser,DATE);Check.equal(p.exit("EX12",DATE.plusDays(1),0).toPlainString(),"300.00","Day pass fails when exit date differs");
  var withShuttle=new ExtendedFacility(new int[]{5},Map.of(Shuttle.class,(v,a,b)->new BigDecimal("15.00")));
  withShuttle.enter(new Shuttle("SH12"),VISITOR,DATE);Check.equal(withShuttle.exit("SH12",DATE.plusMinutes(5),0).toPlainString(),"15.00","Further vehicle and rule added without editing existing model");
  Check.that(p.invariantHolds()&&withShuttle.invariantHolds(),"Extended facilities preserve invariants");
  // Compare optimized van quote against a direct per-block oracle over many boundaries.
  for(int hour=0;hour<24;hour++)for(int length:new int[]{0,1,59,60,61,480,1440,1501,2940}) {
   var a=DATE.withHour(hour).withMinute(45);int blocks=length/60+(length%60==0?0:1);long expected=0;
   for(int b=0;b<blocks;b++){int h=a.plusHours(b).getHour();expected+=h>=9&&h<17?60:30;}
   if(rule.quote(van,a,a.plusMinutes(length)).compareTo(BigDecimal.valueOf(expected))!=0)throw new AssertionError("Van oracle mismatch");
  }
  Check.that(true,"216 van duration and boundary cases match independent block oracle");Check.summary();
 }
}
