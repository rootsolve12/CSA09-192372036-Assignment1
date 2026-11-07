package evidence;
import java.util.Objects;
public final class Check {
    private static int count;
    public static void that(boolean ok,String label) {
        if(!ok) throw new AssertionError(label);
        count++; System.out.println("PASS "+label);
    }
    public static void equal(Object actual,Object expected,String label) {
        that(Objects.equals(actual,expected),label+" actual="+actual+" expected="+expected);
    }
    public static void rejects(Runnable action,String label) {
        try { action.run(); } catch(IllegalArgumentException | IllegalStateException e) {
            that(true,label+" rejected="+e.getMessage()); return;
        }
        throw new AssertionError("Expected rejection: "+label);
    }
    public static void summary() { System.out.println("CHECKS PASSED "+count); }
}
