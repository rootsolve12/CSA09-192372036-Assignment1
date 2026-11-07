package task11;
import parking.model.*; import parking.service.*; import java.time.*; import java.util.*;
/** Deterministic line-oriented input; see input/scenario.txt. */
public class ParkingCLI {
 public static void main(String[] args) {
  ParkingFacility p=new ParkingFacility(new int[]{5,5});var visitor=new ParkingUser("CLI visitor",ParkingUser.Role.VISITOR);
  try(Scanner sc=new Scanner(System.in)) {
   while(sc.hasNextLine()) {
    String line=sc.nextLine().trim();if(line.isEmpty()||line.startsWith("#"))continue;
    String[] a=line.split("\\s+");
    try {
     switch(a[0]) {
      case "ENTER" -> { if(a.length!=4)throw new IllegalArgumentException("ENTER type registration ISO-date-time");var t=p.enter(VehicleFactory.create(a[1],a[2]),visitor,LocalDateTime.parse(a[3]));System.out.println(t==null?"FULL":"ALLOCATED "+t.getFloor()+","+t.getSlot()); }
      case "EXIT" -> { if(a.length!=4)throw new IllegalArgumentException("EXIT registration ISO-date-time kWh");System.out.println("FEE "+p.exit(a[1],LocalDateTime.parse(a[2]),Integer.parseInt(a[3]))); }
      case "STATUS" -> System.out.println("OCCUPANCY "+p.getOccupancy()+" TOTAL "+p.getCollected());
      default -> throw new IllegalArgumentException("Unknown command");
     }
    } catch(RuntimeException e){System.out.println("REJECT "+e.getMessage());}
   }
  }
 }
}
