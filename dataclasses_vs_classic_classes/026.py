import random
from dataclasses import dataclass, field

from typing import Protocol


@dataclass
class Item:
    name: str
    description: str


class Consumable(Item):
    def consume(self):
        ...


@dataclass
class Weapon(Item):
    damage: int
    durability: int = field(default_factory=lambda: random.randint(1, 10))

@dataclass
class Armor(Item):
    defense: int
    durability: int = field(default_factory=lambda: random.randint(1, 10))



from enum import Enum


class PotionType(Enum):
    HEALTH = "health"
    MANA = "mana"
    STRENGTH = "strength"
    PERCEPTION = "perception"
    DEXTERITY = "dexterity"
    INTELLIGENCE = "intelligence"
    CHARISMA = "charisma"
    LUCK = "luck"


@dataclass
class Potion(Item):
    potion_type: PotionType
    amount: int

    def consume(self):
        print(f"Drinking potion of {self.potion_type} and gaining {self.amount} {self.potion_type}.")
        return self.amount

class CharacterClass(Enum):
    KNIGHT = "Knight"
    MAGE = "Mage"
    ROGUE = "Rogue"
    ARCHER = "Archer"
    CLERIC = "Cleric"
    WARRIOR = "Warrior"
    ASSASSIN = "Assassin"
    BERSERKER = "Berserker"
    PALADIN = "Paladin"
    NECROMANCER = "Necromancer"
    DRUID = "Druid"
    BARD = "Bard"
    MONK = "Monk"
    RANGER = "Ranger"
    SORCERER = "Sorcerer"
    WARLOCK = "Warlock"
    WIZARD = "Wizard"
    BARBARIAN = "Barbarian"
    ARTIFICER = "Artificer"
    BLOODHUNTER = "Blood Hunter"
    GRUNT = "Grunt" # For enemies or basic characters

@dataclass
class Character:
    name: str
    character_class: str
    strength: int = field(default_factory=lambda: random.randint(1, 10))
    perception: int = field(default_factory=lambda: random.randint(1, 10))
    dexterity: int = field(default_factory=lambda: random.randint(1, 10))
    intelligence: int = field(default_factory=lambda: random.randint(1, 10))
    charisma: int = field(default_factory=lambda: random.randint(1, 10))
    luck: int = field(default_factory=lambda: random.randint(1, 10))
    level: int = 1
    health: int = 100
    attack: int = 10
    defense: int = 5
    inventory: list[Item | Consumable] = None

    def use_consumable(self, consumable: Consumable):
        if consumable in self.inventory:
            if isinstance(consumable, Potion):
                healed_amount = consumable.consume()
                self.health += healed_amount
                print(f"{self.name} healed for {healed_amount}. Current health: {self.health}")
                self.inventory.remove(consumable)
            else:
                print(f"{consumable.name} is not a consumable item.")
        else:
            print(f"{self.name} does not have a {consumable.name} in their inventory.")

    def __post_init__(self):
        if self.inventory is None:
            self.inventory = []
        self.character_class = self.character_class.value if isinstance(self.character_class, CharacterClass) else self.character_class
        self._apply_class_bonuses()

    def _apply_class_bonuses(self):
        if self.character_class == CharacterClass.KNIGHT.value:
            self.strength += 2
            self.defense += 1
            self.health += 10
        elif self.character_class == CharacterClass.MAGE.value:
            self.intelligence += 3
            self.attack += 2 # For spell power
            self.health -= 5
        elif self.character_class == CharacterClass.ROGUE.value:
            self.dexterity += 3
            self.perception += 1
            self.attack += 1
        elif self.character_class == CharacterClass.ARCHER.value:
            self.dexterity += 2
            self.perception += 2
            self.attack += 1
        elif self.character_class == CharacterClass.CLERIC.value:
            self.charisma += 2
            self.intelligence += 1
            self.health += 5
        elif self.character_class == CharacterClass.WARRIOR.value:
            self.strength += 3
            self.defense += 2
            self.health += 15
        elif self.character_class == CharacterClass.ASSASSIN.value:
            self.dexterity += 4
            self.luck += 1
            self.attack += 2
            self.health -= 10
        elif self.character_class == CharacterClass.BERSERKER.value:
            self.strength += 4
            self.health += 20
            self.defense -= 1 # Less defense for more offense
        elif self.character_class == CharacterClass.PALADIN.value:
            self.strength += 1
            self.charisma += 2
            self.defense += 2
            self.health += 10
        elif self.character_class == CharacterClass.NECROMANCER.value:
            self.intelligence += 3
            self.charisma += 1
            self.health -= 5
        elif self.character_class == CharacterClass.DRUID.value:
            self.charisma += 2
            self.perception += 1
            self.health += 5
        elif self.character_class == CharacterClass.BARD.value:
            self.charisma += 2
            self.luck += 1
            self.attack += 1
        elif self.character_class == CharacterClass.MONK.value:
            self.charisma += 2
            self.strength += 1
            self.health += 5
        elif self.character_class == CharacterClass.RANGER.value:
            self.dexterity += 3
            self.perception += 2
            self.attack += 1
        elif self.character_class == CharacterClass.SORCERER.value:
            self.intelligence += 4
            self.luck += 1
            self.attack += 2
        elif self.character_class == CharacterClass.WARLOCK.value:
            self.charisma += 3
            self.luck += 2
            self.health -= 10
        elif self.character_class == CharacterClass.WIZARD.value:
            self.intelligence += 4
            self.luck += 1
            self.attack += 2
        elif self.character_class == CharacterClass.BARBARIAN.value:
            self.strength += 4
            self.defense += 2
            self.health += 20
        elif self.character_class == CharacterClass.ARTIFICER.value:
            self.intelligence += 3
            self.luck += 1
            self.attack += 1
        elif self.character_class == CharacterClass.BLOODHUNTER.value:
            self.strength += 3
            self.dexterity += 1
            self.health += 10
        elif self.character_class == CharacterClass.GRUNT.value:
            self.strength += 1
            self.health += 5


    def take_damage(self, amount: int):
        damage_taken = max(0, amount - self.defense)
        self.health -= damage_taken
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} took {amount} damage. Health: {self.health}")

    def attack_enemy(self, enemy: 'Character'):
        print(f"{self.name} attacks {enemy.name} for {self.attack} damage!")
        enemy.take_damage(self.attack)

    def add_item(self, item: Item):
        self.inventory.append(item)
        print(f"{self.name} picked up a {item}.")

    def display_info(self):
        print(f"--- {self.name} ---")
        print(f"Class: {self.character_class}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Inventory: {', '.join(item.name for item in self.inventory) if self.inventory else 'Empty'}")


def main():
    # Create characters
    hero = Character(name="Arthur", character_class="Knight")
    goblin = Character(name="Goblin", character_class="Grunt", health=30, attack=5, defense=2)

    # Display initial info
    hero.display_info()
    goblin.display_info()

    print("\n--- Battle Start ---")
    hero.attack_enemy(goblin)
    goblin.attack_enemy(hero)

    hero.attack_enemy(goblin)

    print("\n--- After Battle ---")
    hero.display_info()
    goblin.display_info()

    # Item interaction
    sword = Weapon(name="Sword of Power",
                   description="A mighty sword.",
                   damage=3)
    potion = Potion(name="Healing Potion",
                    description="Restores health.",
                    amount=2,
                    potion_type=PotionType.HEALTH)

    hero.add_item(sword)
    hero.add_item(potion)
    hero.display_info()


if __name__ == "__main__":
    main()
