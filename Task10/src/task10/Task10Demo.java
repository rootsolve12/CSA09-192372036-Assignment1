package task10;
import parking.model.*; import parking.service.*; import evidence.Check;
public class Task10Demo {
 static final class DurationInput {
  private int minutes;
  public void setMinutes(int minutes){if(minutes<0)throw new IllegalArgumentException("Negative duration");this.minutes=minutes;}
  public int getMinutes(){return minutes;}
 }
 @SuppressWarnings("removal")
 public static void main(String[] args) {
  DurationInput d=new DurationInput();d.setMinutes(61);Check.equal(d.getMinutes(),61,"Validated setter");
  Check.rejects(()->d.setMinutes(-1),"Negative update");Check.equal(d.getMinutes(),61,"Failed update preserves state");
  ParkingFacility p=new ParkingFacility(new int[]{5});Check.rejects(()->p.slotKind(-1,0),"Negative floor");Check.rejects(()->p.slotKind(0,5),"Past last slot");
  // Explicit construction ensures distinct wrapper identities independently of cache settings.
  Integer a=new Integer(128),b=new Integer(128);Check.that(a!=b && a.equals(b),"Wrapper == compares identity, equals compares value");
  Integer missing=null;Check.rejects(()->{if(missing==null)throw new IllegalArgumentException("Missing wrapper before unboxing");int x=missing;},"Null wrapper guarded");
  Check.summary();
 }
}
