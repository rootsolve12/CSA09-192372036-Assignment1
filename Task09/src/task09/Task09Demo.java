package task09;
import parking.model.*; import evidence.Check;
public class Task09Demo {
 interface Identified { String identifier(); }
 static final class FleetEV extends ElectricCar implements Identified {
  FleetEV(String reg){super(reg);}
  @Override public String identifier(){return getRegistration();}
 }
 public static void main(String[] args) {
  FleetEV ev=new FleetEV("FLEET09");
  Check.that(java.lang.reflect.Modifier.isAbstract(Vehicle.class.getModifiers()),"Vehicle is abstract");
  Check.that(ev instanceof Chargeable && ev instanceof Identified,"One class implements multiple capabilities");
  Check.equal(ev.chargingUnit(),"kWh","Interface default method inherited");
  Check.equal(Chargeable.rupeesPerKWh().toPlainString(),"12.00","Interface static utility");
  Check.equal(ev.identifier(),"FLEET09","Superclass stores constructor initialized state");Check.summary();
 }
}
