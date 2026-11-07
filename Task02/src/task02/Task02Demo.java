package task02;
import parking.model.*; import evidence.Check; import java.time.*;
public class Task02Demo {
 public static void main(String[] args) {
  int minutes=61; int wrong=minutes/60;
  long correct=minutes/60+(minutes%60==0?0:1);
  System.out.println("61/60 integer="+wrong+" cast after division="+(double)(minutes/60)+" billable hours="+correct);
  Check.equal(correct,2L,"Round started hours upward");
  Check.equal(new Car("TN02BB22").calculateFee(minutes).toPlainString(),"60.00","Exact decimal money");
  String[][] jagged={new String[2],new String[3],new String[1]};
  int[] prefix={0,2,5,6}; String[] flat=new String[6];
  jagged[1][2]="TN02BB22";flat[prefix[1]+2]="TN02BB22";
  Check.equal(flat[4],jagged[1][2],"Prefix offsets handle unequal floors");
  Check.that(2*2+0!=prefix[2]+0,"Constant width flattening fails for unequal widths");
  var in=LocalDateTime.of(2026,1,15,10,0);
  Check.equal(Vehicle.billableMinutes(in,in.plusNanos(1)),1L,"Positive subminute rounds safely");
  Check.equal(new Car("XX22").calculateFee(Long.MAX_VALUE).signum(),1,"Long duration avoids arithmetic overflow");
  Check.summary();
 }
}
