package task08;
import parking.model.*; import evidence.Check; import java.time.*;
public class Task08Demo {
 public static void main(String[] args) {
  Vehicle[] parked={new TwoWheeler("TW08"),new Car("CA08"),new ElectricCar("EV08")};
  String[] fees={"30.00","90.00","90.00"};
  for(int i=0;i<parked.length;i++) {
   Vehicle v=parked[i];System.out.println("Declared=Vehicle actual="+v.getClass().getSimpleName()+" calculateFee -> rate override");
   Check.equal(v.calculateFee(130).toPlainString(),fees[i],"Runtime dispatch "+v.getClass().getSimpleName());
  }
  var in=LocalDateTime.of(2026,1,15,10,0);
  Check.equal(parked[1].calculateFee(in,in.plusMinutes(130)),parked[1].calculateFee(130),"Compile time overload selection gives equal fees");
  Check.equal(((Chargeable)parked[2]).chargingFee(10).toPlainString(),"120.00","Capability dispatch");Check.summary();
 }
}
