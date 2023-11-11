package superhero;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public final class GameCharacter {
	String name;
	int cost;
	Set<Power> powers;
	private static Set<GameCharacter> characters;

	
	public GameCharacter(String name, int cost, Power... powers) {

		this.name = name;
		this.cost = cost;
		this.powers = new HashSet<>();
		for (Power power : powers) {
            this.powers.add(power);
        }

	}


	public String getName() {
		return name;
	}


	public int getCost() {
		return cost;
	}


	public Set<Power> getPowers() {
        return new HashSet<>(powers);
    }


	@Override
	public int hashCode() {
		return Objects.hash(cost, name, powers);
	}


	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		GameCharacter other = (GameCharacter) obj;
		return cost == other.cost && Objects.equals(name, other.name) && powers == other.powers;
	}


	@Override
	public String toString() {
		return "GameCharacter"+ name +"to provide" + powers;
	}
	
	public Set<GameCharacter> chooseCharacters(Power... neededPowers) {
        Set<Power> powersSet = new HashSet<>();
        for (Power power : neededPowers) {
            powersSet.add(power);
        }

        Set<GameCharacter> chosenCharacters = new HashSet<>();
        for (GameCharacter character : characters) {
            Set<Power> characterPowers = character.getPowers();
            if (characterPowers.containsAll(powersSet)) {
                chosenCharacters.add(character);
                powersSet.removeAll(characterPowers);
                if (powersSet.isEmpty()) {
                    return chosenCharacters;
                }
            }
        }

        // If no set of characters can provide all the required powers, return null
        return null;
    }
}
