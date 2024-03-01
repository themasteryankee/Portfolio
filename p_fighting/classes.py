
class Stat:
    def __init__(self, name, level, exp):
        self.name = name
        self.level = level
        self.exp = exp

class Item:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Potion(Item):
    def __init__(self, name, heal):
        super().__init__(name, "Potion")
        self.heal = heal

class Weapon(Item):
    def __init__(self, name, damage):
        super().__init__(name, "Weapon")
        self.damage = damage

class Inventory:
    def __init__(self):
        self.items = [None] * 5

    def add_item(self, item):
        for i in range(len(self.items)):
            if self.items[i] is None:
                self.items[i] = item
                break
        else:
            print("Inventory is full")

class Weapon_Slot:
    def __init__(self):
        self.wep = None

    def add_wep(self, weapon):
        if isinstance(weapon, Weapon):
            if self.wep is None:
                self.wep = weapon
                return True
            else:
                print("A weapon already equipped.")
                return False
        else:
            print("That item cannot be equipped.")

    def remove_wep(self, inventory):
        self.flag = True
        if self.wep is not None:
            for i in range(len(inventory.items)):
                if inventory.items[i] is None:
                    inventory.items[i] = self.wep
                    self.wep = None
                    print("Weapon unequipped.")
                    self.flag = False
                    break
            if self.flag == True:
                print("Inventory is full.")


class Player:
    def __init__(self, name, weapon):
        self.name = name
        self.stats = {"HP": Stat("HP", 15, 0),
                      "Attack": Stat("Attack", 1, 0),
                      "Strength": Stat("Strength", 1, 0),
                      "Defense": Stat("Defense", 1, 0)}
        self.combat = self.calculate_combat()
        self.inventory = Inventory()
        self.weapon = Weapon_Slot()

    def calculate_combat(self):
        cmb = round(0.25 * (self.stats["Defense"].level + self.stats["HP"].level + ((self.stats["Attack"].level + self.stats["Strength"].level) / 2)))
        return cmb

class Enemy:
    def __init__(self, name, hp_level, attack_level, strength_level, def_level):
        self.name = name
        self.stats = {"HP": Stat("HP", hp_level, 0),
                      "Attack": Stat("Attack", attack_level, 0),
                      "Strength": Stat("Strength", strength_level, 0),
                      "Defense": Stat("Defense", def_level, 0)}
        self.combat = self.calculate_combat()
    def calculate_combat(self):
        cmb = round(0.25 * (self.stats["Defense"].level + self.stats["HP"].level + ((self.stats["Attack"].level + self.stats["Strength"].level) / 2)))
        return cmb
