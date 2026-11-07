package task06;
import parking.model.*; import evidence.Check; import java.util.*;
public class Task06Demo {
 static final List<String> trace=new ArrayList<>();
 static class TraceVehicle { TraceVehicle(){trace.add("Vehicle constructor");} }
 static class TraceCar extends TraceVehicle { TraceCar(){super();trace.add("Car constructor");} }
 static class TraceElectricCar extends TraceCar { TraceElectricCar(){super();trace.add("ElectricCar constructor");} }
 record VehicleType(String name,long rate) { }
 record ComposedVehicle(String registration,VehicleType type) {
  long fee(int minutes){if(minutes<0)throw new IllegalArgumentException();return (minutes/60+(minutes%60==0?0:1))*type.rate();}
 }
 public static void main(String[] args) {
  new TraceElectricCar();System.out.println("Constructor trace (instrumented mirror hierarchy): "+trace);
  Check.equal(String.join(" > ",trace),"Vehicle constructor > Car constructor > ElectricCar constructor","Superclass constructors run first");
  Vehicle ev=new ElectricCar("TN06FF66");Check.that(ev instanceof Car && ev instanceof Chargeable,"Multilevel inheritance and independent capability");
  Check.equal(ev.getRegistration(),"TN06FF66","Superclass initialized registration through super");
  var type=new VehicleType("Car",30);var composed=new ComposedVehicle("TN06GG77",type);
  Check.equal(composed.fee(130),90L,"Composition alternative matches short-stay rate");
  Check.summary();
 }
}
