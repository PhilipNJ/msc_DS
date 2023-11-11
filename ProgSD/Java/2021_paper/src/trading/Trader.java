package trading;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Trader {
	
	private List<Trade> trades;
	
	public Trader() {
        trades = new ArrayList<>();
        addRandomTrade();
    }
	
	public List<Trade> getTrades(){
		return trades;
	}
	
	public void addRandomTrade() {
		Random rand = new Random();
		int gems = rand.nextInt(6);
		int amount = rand.nextInt(6);
		Goods goods = Goods.values()[rand.nextInt(Goods.values().length)];
		
		Trade newTrade = new Trade(gems, amount, goods);
		trades.add(newTrade);
	}
	
}


