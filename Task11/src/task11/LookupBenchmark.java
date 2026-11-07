package task11;
import parking.model.*; import java.time.*; import java.util.*; import java.io.*;
public class LookupBenchmark {
 static volatile long sink;
 static ParkingTicket scan(ParkingTicket[] a,String key){for(var t:a)if(t.getVehicle().getRegistration().equals(key))return t;return null;}
 static ParkingTicket scan(List<ParkingTicket> a,String key){for(var t:a)if(t.getVehicle().getRegistration().equals(key))return t;return null;}
 public static void main(String[] args) {
  System.out.println("n,method,repeat,queries,elapsed_ns,comparisons_per_last_hit,checksum");
  for(int n:new int[]{1000,10000,100000}) {
   ParkingTicket[] array=new ParkingTicket[n];List<ParkingTicket> list=new ArrayList<>(n);Map<String,ParkingTicket> map=new HashMap<>();
   for(int i=0;i<n;i++){var t=new ParkingTicket(new Car("REG"+i),LocalDateTime.of(2026,1,15,10,0),0,i);array[i]=t;list.add(t);map.put(t.getVehicle().getRegistration(),t);}
   String key=new String("REG"+(n-1));int queries=100;
   for(int warm=0;warm<200;warm++){sink=scan(array,key).getId();sink=scan(list,key).getId();sink=map.get(key).getId();}
   for(int repeat=1;repeat<=5;repeat++) for(int off=0;off<3;off++) {
    int method=(off+repeat)%3;long checksum=0,start=System.nanoTime();
    for(int q=0;q<queries;q++){ParkingTicket t=switch(method){case 0->scan(array,key);case 1->scan(list,key);default->map.get(key);};checksum+=t.getId();}
    long ns=System.nanoTime()-start;sink=checksum;
    System.out.println(n+","+new String[]{"array","arraylist","hashmap"}[method]+","+repeat+","+queries+","+ns+","+(method==2?"NA":n)+","+checksum);
   }
  }
 }
}
