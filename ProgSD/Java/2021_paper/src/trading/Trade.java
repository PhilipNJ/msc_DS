package trading;

import java.util.Objects;

public class Trade {
	private  int gems;
	private int amount;
	private  Goods goods;
	
	public Trade(int gems, int amount, Goods goods) {
		  
		this.gems = gems;
		this.amount = amount;
		this.goods = goods;
	}

	public  int getGems() {
		return gems;
	}
	public int getAmount() {
		return amount;
	}
	public  Goods getGoods() {
		return goods;
	}

	@Override
	public int hashCode() {
		return Objects.hash(amount, gems, goods);
	}
	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Trade other = (Trade) obj;
		return amount == other.amount && gems == other.gems && goods == other.goods;
		
	}

	@Override
	public String toString() {
		return gems + " gems for " + amount+ " " + goods;
	}	
	
	public void execute(Trader trader, Citizen citizen) {
		if (!trader.getTrades().contains(this)) {
			throw new IllegalArgumentException();
		} 
		
		boolean tradeSuccessful = citizen.executeTrade(this);
		
		if (tradeSuccessful) {
			trader.addRandomTrade();
		}
		
			
	}
}
