package parking.service;
import parking.model.*;
import java.util.Locale;
public final class VehicleFactory {
    private VehicleFactory() { }
    public static Vehicle create(String type,String registration) {
        if(type==null) throw new IllegalArgumentException("Unknown vehicle type");
        return switch(type.toUpperCase(Locale.ROOT)) {
            case "TWO" -> new TwoWheeler(registration);
            case "CAR" -> new Car(registration);
            case "EV" -> new ElectricCar(registration);
            default -> throw new IllegalArgumentException("Unknown vehicle type: "+type);
        };
    }
}
