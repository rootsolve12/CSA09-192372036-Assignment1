package parking.service;
import parking.model.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;
public class ParkingFacility {
    private final Slot[][] slots;
    private final ParkingTicket[] active;
    private int occupancy;
    private BigDecimal collected = new BigDecimal("0.00");
    public ParkingFacility(int[] perFloor) {
        if(perFloor==null || perFloor.length==0) throw new IllegalArgumentException("No floors");
        slots=new Slot[perFloor.length][];
        int total=0;
        for(int f=0; f<perFloor.length; f++) {
            if(perFloor[f]<=0) throw new IllegalArgumentException("Empty floor");
            total=Math.addExact(total,perFloor[f]);
            slots[f]=new Slot[perFloor[f]];
            for(int s=0;s<perFloor[f];s++)
                slots[f][s]=new Slot(f,s, s%5==0 ? Slot.Kind.TWO_WHEELER : s%5==4 ? Slot.Kind.CHARGING : Slot.Kind.CAR);
        }
        active=new ParkingTicket[total];
    }
    public ParkingTicket enter(Vehicle vehicle, ParkingUser user, LocalDateTime time) {
        Objects.requireNonNull(vehicle); Objects.requireNonNull(user); Objects.requireNonNull(time);
        if(find(vehicle.getRegistration())!=null) throw new IllegalArgumentException("Duplicate registration");
        for(Slot[] floor:slots) for(Slot slot:floor) {
            if(!slot.isFree() || !slot.accepts(vehicle)) continue;
            ParkingTicket t=new ParkingTicket(vehicle,user,time,slot.getFloor(),slot.getNumber());
            int index=0; while(active[index]!=null) index++;
            slot.occupy(vehicle); active[index]=t; occupancy++;
            return t;
        }
        return null;
    }
    public ParkingTicket find(String registration) {
        if(registration==null) return null;
        String key=registration.trim().toUpperCase(Locale.ROOT);
        for(ParkingTicket t:active) if(t!=null && t.getVehicle().getRegistration().equals(key)) return t;
        return null;
    }
    protected BigDecimal parkingQuote(ParkingTicket ticket, LocalDateTime out) {
        return ticket.getVehicle().calculateFee(ticket.getEntered(),out);
    }
    public BigDecimal exit(String registration, LocalDateTime out, int kWh) {
        ParkingTicket t=find(registration);
        if(t==null) throw new IllegalArgumentException("No active ticket");
        Objects.requireNonNull(out);
        Vehicle.billableMinutes(t.getEntered(),out);
        if(kWh<0 || (kWh>0 && (!(t.getVehicle() instanceof Chargeable) || slots[t.getFloor()][t.getSlot()].getKind()!=Slot.Kind.CHARGING)))
            throw new IllegalArgumentException("Invalid charging request");
        BigDecimal fee=parkingQuote(t,out);
        Pass pass=t.getUser().getPass();
        if(pass!=null && pass.covers(t.getEntered(),out)) fee=new BigDecimal("0.00");
        if(t.getVehicle() instanceof Chargeable c) fee=fee.add(c.chargingFee(kWh));
        // Validation and quoting complete before any state changes.
        slots[t.getFloor()][t.getSlot()].release();
        for(int i=0;i<active.length;i++) if(active[i]==t) { active[i]=null; break; }
        occupancy--; collected=collected.add(fee);
        return fee;
    }
    public Slot.Kind slotKind(int floor,int slot) {
        if(floor<0 || floor>=slots.length || slot<0 || slot>=slots[floor].length)
            throw new IllegalArgumentException("Invalid slot position");
        return slots[floor][slot].getKind();
    }
    public int getOccupancy() { return occupancy; }
    public int capacity() { return active.length; }
    public int floors() { return slots.length; }
    public BigDecimal getCollected() { return collected; }
    public boolean invariantHolds() {
        int occupied=0,tickets=0; Set<String> registrations=new HashSet<>();
        for(Slot[] floor:slots) for(Slot slot:floor) if(!slot.isFree()) occupied++;
        for(ParkingTicket t:active) if(t!=null) {
            tickets++;
            if(!registrations.add(t.getVehicle().getRegistration()) ||
              !t.getVehicle().getRegistration().equals(slots[t.getFloor()][t.getSlot()].getRegistration())) return false;
        }
        return occupancy==occupied && occupied==tickets && occupancy>=0 && occupancy<=active.length;
    }
}
