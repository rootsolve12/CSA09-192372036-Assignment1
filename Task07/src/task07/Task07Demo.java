package task07;
import parking.model.*; import evidence.Check; import java.util.*;
public class Task07Demo {
 static long switchFee(String type,int minutes) {
  long rate=switch(type){case "TWO"->10;case "CAR","EV"->30;default->throw new IllegalArgumentException();};
  return (minutes/60+(minutes%60==0?0:1))*rate;
 }
 public static void main(String[] args) {
  Vehicle c=new Car("tn07gg77"), ev=new ElectricCar("TN07GG77");
  Check.that(c.equals(ev)&&ev.equals(c)&&c.hashCode()==ev.hashCode(),"Registration identity across categories");
  Set<Vehicle> set=new HashSet<>();set.add(c);set.add(ev);Check.equal(set.size(),1,"HashSet equality contract");
  Check.that(!c.equals(null)&&!c.equals("TN07GG77"),"Equality rejects null and unrelated type");
  Check.equal(c.toString(),"Car(TN07GG77)","Readable Object override");
  Check.equal(new TwoWheeler("TWO77").calculateFee(130).toPlainString(),"30.00","Overridden rate changes template result");
  Check.equal(switchFee("CAR",130),90L,"Switch alternative short-stay comparison");Check.summary();
 }
}
