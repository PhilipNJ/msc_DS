package superhero;

import java.util.HashSet;
import java.util.Set;

public class Player {
	private final Set<GameCharacter> characters;
	
	public Player() {
        this.characters = new HashSet<>();
    }
	
	public void addCharacter(GameCharacter character) {
        characters.add(character);
    }
	
	public Set<GameCharacter> getCharacters() {
		return new HashSet<>(characters);
	}
}
