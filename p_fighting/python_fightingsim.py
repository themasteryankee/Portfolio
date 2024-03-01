import random
import os
from classes import Stat, Item, Potion, Weapon, Weapon_Slot, Inventory, Player, Enemy

def main():
    username = input("What is your name?\n")
    myPlayer = Player(username, None)
    main_menu(myPlayer)

def main_menu(myPlayer):
    #Main menu options
    options = ["1", "2", "3", "4", "5"]
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        option = input("=======================\n"
                       "       Main Menu\n"
                       "=======================\n"
                       "    1)Start Fight\n"
                       "-----------------------\n"
                       "    2)Train\n"
                       "-----------------------\n"
                       "    3)Check Stats\n"
                       "-----------------------\n"
                       "    4)Item Creator\n"
                       "-----------------------\n"
                       "    5)View Inventory\n"
                       "-----------------------\n")
        if option not in options:
            continue
        elif option == options[0]:
            fight(myPlayer)
        elif option == options[1]:
            train_menu(myPlayer)
        elif option == options[2]:
            check_stats(myPlayer)
        elif option == options[3]:
            create_item(myPlayer)
        elif option == options[4]:
            view_inv(myPlayer)

def train_menu(myPlayer):
    options = ["1", "2", "3", "4"]
    #Variables to pass stat classes to train function
    attack = myPlayer.stats["Attack"]
    strength = myPlayer.stats["Strength"]
    defense = myPlayer.stats["Defense"]
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        option = input("=======================\n"
                    "     Train a Skill\n"
                    "=======================\n"
                    "    1)Train Attack\n"
                    "-----------------------\n"
                    "    2)Train Stength\n"
                    "-----------------------\n"
                    "    3)Train Defense\n"
                    "-----------------------\n"
                    "    4)Main Menu\n"
                    "-----------------------\n")
        if option not in options:
            continue
        elif option == options[0]:
            train(myPlayer, attack)
        elif option == options[1]:
            train(myPlayer, strength)
        elif option == options[2]:
            train(myPlayer, defense)
        elif option == options[3]:
            return

def fight(myPlayer):
    #Fight loop bool and action lists for player and enemy
    fighting = True
    p_actions = ["1", "2", "3", "4"]
    e_actions = ["Attack", "Defend"]

    #Initialize player's hp and enemy's hp for fight
    current_hp = myPlayer.stats["HP"].level
    enemy_hp = random.randint(myPlayer.stats["HP"].level - 2, myPlayer.stats["HP"].level + 1)

    #Initialize enemy's random stats
    if myPlayer.stats["Attack"].level <= 3:
        enemy_attack_min = 1
    else:
        enemy_attack_min = myPlayer.stats["Attack"].level - 2
    if myPlayer.stats["Strength"].level <= 3:
        enemy_strength_min = 1
    else:
        enemy_strength_min = myPlayer.stats["Strength"].level - 2
    if myPlayer.stats["Defense"].level <= 3:
        enemy_def_min = 1
    else:
        enemy_def_min = myPlayer.stats["Defense"].level - 2

    enemy_attack = random.randint(enemy_attack_min, myPlayer.stats["Attack"].level + 1)
    enemy_strength = random.randint(enemy_strength_min, myPlayer.stats["Strength"].level + 1)
    enemy_defense = random.randint(enemy_def_min, myPlayer.stats["Defense"].level + 1)
    enemy = Enemy("Enemy", enemy_hp, enemy_attack, enemy_strength, enemy_defense)
    enemy_cmb = enemy.calculate_combat()
    myPlayer.combat = myPlayer.calculate_combat()

    #Factor for damage counters
    factor = 1.50
    #Message variables to print after clearing console in fight loop
    message = None
    message2= None

    #Counters for exp calculations
    turn_counter = 0
    hp_counter = 0
    attack_counter = 0
    strength_counter = 0
    defense_counter = 0

    while fighting and (current_hp > 0 and enemy_hp > 0):
        os.system('cls' if os.name == 'nt' else 'clear')
        if message is not None:
            print(f"===============================\n{message}")
        if message2 is not None:
            print(f"===============================\n{message2}")
        #Initialize player damage counter
        base_dmg_min = 0
        base_dmg_max = round((myPlayer.stats["Attack"].level + round(myPlayer.stats["Strength"].level / 2)) * factor)
        base_dmg = random.randint(base_dmg_min, base_dmg_max)
        p_def_dmg = random.randint(base_dmg_min, round(base_dmg_max - enemy.stats["Defense"].level * 0.5))

        #Add weapon damage
        if myPlayer.weapon.wep is not None:
            base_dmg += myPlayer.weapon.wep.damage
            p_def_dmg += myPlayer.weapon.wep.damage
            has_weapon = True

        #Initialize enemy damage counter
        enemy_dmg_min = 0
        enemy_dmg_max = round((enemy.stats["Attack"].level + round(enemy.stats["Strength"].level / 2)) * factor)
        enemy_base = random.randint(enemy_dmg_min, enemy_dmg_max)
        e_def_dmg = random.randint(enemy_dmg_min, round(enemy_dmg_max - myPlayer.stats["Defense"].level * 0.5))

        #Fight menu
        print("===============================\n"
              f"{myPlayer.name}:Lvl({myPlayer.combat}) vs {enemy.name}:Lvl({enemy_cmb})\n"
              "===============================\n"
              f"{myPlayer.name}'s HP: {current_hp}\n"
              f"{enemy.name}'s HP: {enemy_hp}\n"
              "-------------------\n"
              "1)Attack\n"
              "----------------\n"
              "2)Defend\n"
              "-------------\n"
              "3)Use Item\n"
              "----------\n"
              "4)Run")
        action_option = False
        e_action = random.choice(e_actions)

        #Validate input
        while not action_option:
            p_action = input(f"What should {myPlayer.name} do?\n")
            if p_action not in p_actions:
                print("Enter '1' to 'Attack', '2' to 'Defend', '3' to use an item, '4' to run.")
            elif p_action in p_actions:
                action_option = True
        #If Player attacks
        if p_action == "1":
            #If Enemy also attacks
            if e_action == "Attack":
                if base_dmg > 0:
                    if has_weapon:
                        message = f"{myPlayer.name}'s {myPlayer.weapon.wep.name} dealt\n{base_dmg} damage!"
                    elif not has_weapon:
                        message = f"{myPlayer.name} dealt {base_dmg} damage!"
                    enemy_hp -= base_dmg
                    attack_counter += 2
                    strength_counter += 1
                elif base_dmg == 0:
                    message = f"{myPlayer.name} missed!"
                if enemy_base > 0:
                    message2 = f"The {enemy.name} dealt {enemy_base} damage!"
                    hp_counter += 1
                    current_hp -= enemy_base
                elif enemy_base == 0:
                    message2 = f"The {enemy.name} missed!"
                turn_counter += 1
                continue
            #If Enemy defends
            elif e_action == "Defend":
                if p_def_dmg > 0:
                    if has_weapon:
                        message = f"{myPlayer.name}'s {myPlayer.weapon.wep.name} dealt {p_def_dmg}\ndamage through the {enemy.name}'s defense!"
                    elif not has_weapon:
                        message = f"{myPlayer.name} dealt {p_def_dmg} through the {enemy.name}'s defense!"
                    attack_counter += 1
                    strength_counter += 1
                    enemy_hp -= p_def_dmg
                elif p_def_dmg == 0:
                    message = f"{myPlayer.name}'s attack was blocked by the {enemy.name}!"
                turn_counter += 1
                message2 = None
                continue
        #If Player Defends
        elif p_action == "2":
            #If Enemy attacks
            if e_action == "Attack":
                if e_def_dmg > 0:
                    message2 = f"The {enemy.name} dealt {e_def_dmg} through {myPlayer.name}'s defense!"
                    hp_counter += 2
                    defense_counter += 1
                    current_hp -= e_def_dmg
                elif enemy_base == 0:
                    message2 = f"{myPlayer.name}'s defense held strong!"
                    defense_counter += 2
                turn_counter += 1
                message = None
                continue
            #If Enemy also defends
            elif e_action == "Defend":
                message = f"Both {myPlayer.name} and the {enemy.name} wait for the next move."
                message2 = None
                turn_counter += 1
                continue
        #If Player uses an item
        elif p_action == "3":
            current_hp = use_item(myPlayer, current_hp)
            if e_action == "Attack":
                if enemy_base > 0:
                    message2 = f"The {enemy.name} took the opportunity to deal {enemy_base} damage!"
                    hp_counter += 1
                    current_hp -= enemy_base
                elif enemy_base == 0:
                    message2 = f"The {enemy.name} missed!"
                turn_counter += 1
            elif e_action == "Defend":
                message2 == f"The {enemy.name} observed {myPlayer.name}'s actions."
                turn_counter += 1
        #If Player runs
        elif p_action == "4":
            print("You ran away!")
            press_enter()
            return
    #Win/Lose
    if message is not None:
        print(f"===============================\n{message}")
    if message2 is not None:
        print(f"===============================\n{message2}")
    if current_hp <= 0:
        print(f"-------------------------------\n{myPlayer.name} was defeated.\n-------------------------------\n")
        press_enter()
        fighting = False
    elif enemy_hp <= 0:
        print(f"-------------------------------\n{myPlayer.name} was victorious!\n-------------------------------\n")
        #Bool for dialogue after winning a fight
        did_level = win_exp(myPlayer, turn_counter, hp_counter, attack_counter, strength_counter, defense_counter, enemy)
        if not did_level:
            press_enter()
        myPlayer.combat = myPlayer.calculate_combat()

        drop = random.randint(1, 10)
        if drop == 1:
            create_item(myPlayer)
        fighting = False
    return

#Fight Exp Rewards
def win_exp(myPlayer, turn_counter, hp_counter, attack_counter, strength_counter, defense_counter, enemy):

    #Exp calculations
    hp_exp = round(5 * ((hp_counter / 5) + enemy.combat) - turn_counter)
    attack_exp = round(1.25 * ((attack_counter / 3) + enemy.stats["Attack"].level))
    strength_exp = round(1.25 * ((strength_counter / 2) + enemy.stats["Strength"].level))
    defense_exp = round(1.25 * ((defense_counter / 3) + enemy.stats["Defense"].level))

    print("================\n"
          "   Exp Gained\n"
          "================\n"
          f"HP: {hp_exp}\n"
          "----------------\n"
          f"Attack: {attack_exp}\n"
          "----------------\n"
          f"Strength: {strength_exp}\n"
          "----------------\n"
          f"Defense: {defense_exp}\n"
          "----------------\n")
    #Add exp to stats
    myPlayer.stats["HP"].exp += hp_exp
    myPlayer.stats["Attack"].exp += attack_exp
    myPlayer.stats["Strength"].exp += strength_exp
    myPlayer.stats["Defense"].exp += defense_exp
    did_level = check_and_level(myPlayer)
    return did_level

#Loop through dictionary of stats and check if they can level up after fight
def check_and_level(myPlayer):
    did_level = False
    for stat in myPlayer.stats.values():
        current_level = stat.level
        exp_needed = current_level ** 3 * 2
        if stat.exp >= exp_needed:
            did_level = True
            level_up(stat, myPlayer)
            stat.exp -= exp_needed
    return did_level

#Continue function
def press_enter():
    cont = False
    while not cont:
        press = input("Press 'Enter' to continue")
        if press != '':
            continue
        else:
            break
    return

#Check player stats
def check_stats(myPlayer):
    os.system('cls' if os.name == 'nt' else 'clear')
    myPlayer.combat = myPlayer.calculate_combat()
    print("====================\n"
          f"    {myPlayer.name}'s Stats\n"
          "====================\n"
          f"Combat Level: {myPlayer.combat}\n"
          "--------------------\n"
          f"HP Level: {myPlayer.stats['HP'].level}\n"
          f"HP EXP: {myPlayer.stats['HP'].exp}\n"
          "--------------------\n"
          f"Attack Level: {myPlayer.stats['Attack'].level}\n"
          f"Attack EXP: {myPlayer.stats['Attack'].exp}\n"
          "--------------------\n"
          f"Strength Level: {myPlayer.stats['Strength'].level}\n"
          f"Strength EXP: {myPlayer.stats['Strength'].exp}\n"
          "--------------------\n"
          f"Defense Level: {myPlayer.stats['Defense'].level}\n"
          f"Defense EXP: {myPlayer.stats['Defense'].exp}\n"
          "--------------------\n")
    press_enter()
    return

#Training function for whichever stat is passed to it
def train(myPlayer, stat):

    words = []
    training = True
    #Different word lists depending on which stat is passed
    if stat.name == "Attack":
        words = ["Sword", "Scimitar", "Dagger", "Slash", "Attack", "Stab"]
    elif stat.name == "Strength":
        words = ["Smash", "Crush", "Heavy", "Power", "Destroy", "Strength"]
    elif stat.name == "Defense":
        words = ["Shield", "Defense", "Guard", "Protect", "Stance", "Block"]

    #Train via typing word prompts correclty
    while training:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=========================\n"
              f"     {stat.name} Training\n"
              "=========================")
        word = random.choice(words)
        attempt = input(f"Type: '{word}'\n").title()
        #If attempt was incorrect
        if attempt != word:
            print("Incorrect!\n")
            press_enter()
            continue
        #If attempt was correct
        elif attempt == word:
            #Calculate exp based on length of word prompt
            exp = round(len(word) / 3)
            stat.exp += exp
            print(f"Correct!\n{myPlayer.name} gained {exp} {stat.name} EXP!")
            #Check exp needed to level up
            needed = needed_exp(stat)
            if stat.exp >= needed:
                #Level up
                level_up(stat, myPlayer)
                stat.exp -= needed
            answer = False
            while not answer:
                cont = input("Continue training?\n1)Yes\n2)No\n")
                if cont != "1" and cont != "2":
                    continue
                elif cont == "1":
                    break
                elif cont == "2":
                    training = False
                    break
#Calculate needed exp
def needed_exp(stat):
    current_level = stat.level
    exp_needed = round(current_level ** 2 * 1.75)
    return exp_needed

#Level up stat
def level_up(stat, myPlayer):
    stat.level += 1
    myPlayer.combat = myPlayer.calculate_combat()
    print(f"{myPlayer.name}'s {stat.name} Level is now {stat.level}!")
    press_enter()
    return stat

#View items in inventory
def view_inv(myPlayer):
    os.system('cls' if os.name == 'nt' else 'clear')
    inv = myPlayer.inventory.items
    wep = myPlayer.weapon.wep
    is_weapon = False
    print("====================\n"
        f"{myPlayer.name}'s Inventory\n"
          "====================")
    #Loop throw items in inventory and print item info
    for items in inv:
        if items is not None:
            if items.type == "Potion":
                print(f"{items.name}\n"
                    f"Heals: {items.heal}")
            elif items.type == "Weapon":
                print(f"{items.name}\n"
                      f"Damage: {items.damage}")
                is_weapon = True
        #Shows empty inventory slots
        elif items is None:
            print("Empty Inventory Slot")
        print("--------------------")
    #Print weapon slot
    if wep is not None:
        is_weapon = True
        print("Equipped Weapon\n"
              f"{myPlayer.weapon.wep.name}\n"
              f"Damage: {myPlayer.weapon.wep.damage}")
    else:
        print("Empty Weapon Slot")
    print("--------------------")
    #If a weapon is in inventory
    if is_weapon:
        loop = False
        while not loop:
            equip = input("Enter '1' to equip a weapon.\n"
                          "Enter '2' to unequip a weapon.\n"
                        "Press 'Enter' to return to the main menu.")
            if equip != '1' and equip != '' and equip != '2':
                continue
            elif equip == '1':
                equip_item(myPlayer)
            elif equip == '2':
                unequip_item(myPlayer)
            elif equip == '':
                return
    else:
        press_enter()
#Removes weapon
def unequip_item(myPlayer):
    if myPlayer.weapon.wep is not None:
        myPlayer.weapon.remove_wep(myPlayer.inventory)
    else:
        print("No weapon to unequip.")

#Use potion while in fight
def use_item(myPlayer, current_hp):
    os.system('cls' if os.name == 'nt' else 'clear')
    inv = myPlayer.inventory.items
    print("====================\n"
          f"{myPlayer.name}'s Items\n"
          "====================")

    for i, items in enumerate(inv, start=1):
        if items is not None and items.type == "Potion":
            print(f"{i}){items.name}\n"
                  f"  Heal: {items.heal}\n"
                  "--------------------")
    selected = False
    while not selected:
        select = input("Enter item to use:\n")
        if select == '':
            break
        for i, items in enumerate(inv, start=1):
            if items is not None and items.type == "Potion" and str(i) == select:
                current_hp += items.heal
                myPlayer.inventory.items[i - 1] = None
                selected = True
                break
        if not selected:
            break
    return current_hp

#Equips weapon
def equip_item(myPlayer):
    os.system('cls' if os.name == 'nt' else 'clear')
    inv = myPlayer.inventory.items
    print("====================\n"
          f"   {myPlayer.name}'s Weapons\n"
          "====================")
    #Loop through items and list all weapons, prefixed by i
    for i, items in enumerate(inv, start=1):
        if items is not None and items.type == "Weapon":
            print(f"{i}){items.name}\n"
                  f"  Damage: {items.damage}\n"
                  "--------------------")
    selected = False
    while not selected:
        select = input("Enter item to equip:\n")
        if select == '':
            break
        #Loop through items to get input that is equal to i
        for i, items in enumerate(inv, start=1):
            if items is not None and items.type == "Weapon" and str(i) == select:
                #add weapon to weapon slot
                if myPlayer.weapon.add_wep(items):
                    myPlayer.inventory.items[i - 1] = None
                    selected = True
                    break
        if not selected:
            break
    return
#Item creator
def create_item(myPlayer):
    rand = random.randint(1, 2)
    if rand == 1:
        item = Potion("Health Potion", 5)
        answer = False
        answers = ["1", "2"]
        while not answer:
            take = input(f"{myPlayer.name} found a {item.name}!\n"
                        f"Take the {item.name}?\n"
                        "1)Yes\n"
                        "2)No")
            if take not in answers:
                continue
            elif take == '1':
                myPlayer.inventory.add_item(item)
                break
            else:
                break
    elif rand == 2:
        item = Weapon("Bronze Sword", 2)
        answer = False
        answers = ["1", "2"]
        while not answer:
            take = input(f"{myPlayer.name} found a {item.name}!\n"
                        f"Take the {item.name}?\n"
                        "1)Yes\n"
                        "2)No")
            if take not in answers:
                continue
            elif take == '1':
                myPlayer.inventory.add_item(item)
                break
            else:
                break
    return

if __name__ == "__main__":
    main()
