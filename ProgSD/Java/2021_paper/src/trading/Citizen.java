package trading;
import java.util.HashMap;
import java.util.Map;

public class Citizen {
	private int gems;
	private Map<Goods, Integer> inventory;
	
	public Citizen(int gems) {
	
		this.gems = gems;
		inventory = new HashMap<>();
		for (Goods goods : Goods.values()) {
			inventory.put(goods,0);
		}
	}
	
	public int getGems() {
		return this.gems;
	}
	
	public int getAmount (Goods goods) {
		return inventory.get(goods);
		
	}
	
	public boolean executeTrade (Trade trade) {
		if (this.gems< trade.getGems()) {
			return false;
		} else {
			this.gems -= trade.getGems();
			inventory.put(trade.getGoods(), inventory.get(trade.getGoods()) + trade.getAmount());
			
			return true;
					
		}
		
	}

}
