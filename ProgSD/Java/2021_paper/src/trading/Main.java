package trading;

public class Main {
    public static void main(String[] args) {
        // Initialize a new Trade object
        Trade trade = new Trade(3, 2, Goods.BREAD);
        
        // Create instances of Trader and Citizen
        Trader trader = new Trader();
        Citizen citizen = new Citizen(10); // Citizen with 10 gems

        // Perform the trade operation
        try {
            trade.execute(trader, citizen);
            System.out.println("Trade successful!");
        } catch (IllegalArgumentException e) {
            System.out.println("Trade failed: " + e.getMessage());
        }

        // Print updated trades after execution
        System.out.println("Updated trades offered by the trader:");
        for (Trade t : trader.getTrades()) {
            System.out.println(t);
        }
    }
}
