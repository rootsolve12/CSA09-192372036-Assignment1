package parking.model;
import java.time.LocalDateTime;
public interface Pass { boolean covers(LocalDateTime in, LocalDateTime out); }
