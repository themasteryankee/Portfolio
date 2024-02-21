#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>
#include <time.h>
#include "structs.h"

#define ENEMY_MAX 2
#define BASE_DMG 0.75
#define INV_SIZE 5

//Function Prototypes
char main_menu(player *myPlayer);
int increase_melee(player *myPlayer);
int increase_defense(player *myPlayer);
int increase_mining(player *myPlayer);
void check_stats(player *myPlayer);
void fight(player *myPlayer);
int calculate_exp(player *myPlayer, int *defend_counter, int *attack_counter, enemy *new_enemy);
void train_skill(player *myPlayer);
void view_inv(player *myPlayer);
void item_creator(player *myPlayer, bool drop);
void drop_item(player *myPlayer);
void equip_item(player *myPlayer);
void unequip_item(player *myPlayer);

int main(void)
{
    //initialize player struct, allocate memory for player
    player *myPlayer = malloc(sizeof(player));
    if(myPlayer == NULL)
    {
        return -1;
    }
    //initialize player stats
    myPlayer->melee.level = 1;
    myPlayer->melee.exp = 0;
    strcpy(myPlayer->melee.name, "Melee");
    myPlayer->defense.level = 1;
    myPlayer->defense.exp = 0;
    strcpy(myPlayer->defense.name, "Defense");
    myPlayer->hp.level = 10;
    myPlayer->hp.exp = 0;
    strcpy(myPlayer->hp.name, "HP");
    myPlayer->mining.level = 1;
    myPlayer->mining.exp = 0;
    strcpy(myPlayer->mining.name, "Mining");
    myPlayer->combat = 1;
    myPlayer->weapon_item.type = EMPTY;
    myPlayer->kills = 0;
    myPlayer->deaths = 0;
    myPlayer->kd = 0.00;

    //Initialize player inventory
    int num_items = sizeof(myPlayer->inv.items) / sizeof(myPlayer->inv.items[0]);
    for(int i = 0; i < num_items; i++)
    {
        myPlayer->inv.items[i].type = EMPTY;
    }

    //main function variables
    bool name;
    int ch;
    char choice;

    //initializes player's name
    printf("What is your name?\n");
    do
    {
        name = true;
        fgets(myPlayer->name, 10, stdin);

        if(myPlayer->name[strlen(myPlayer->name) - 1] != '\n')
        {
            while ((ch = getchar()) != '\n' && ch != EOF);
        }
        for(int i = 0; i < strlen(myPlayer->name); i++)
        {
            if(myPlayer->name[i] == '\n')
            {
                myPlayer->name[i] = '\0';
            }
        }
        for(int i = 0; i < strlen(myPlayer->name); i++)
        {
            if(!isalpha(myPlayer->name[i]))
            {
                name = false;
                printf("Your name cannot contain digits or punctuation.\nWhat is your name?\n");
                break;
            }
        }
    }while(name != true);

    //gets returned choice value from main_menu function
    printf("Okay, %s.\n", myPlayer->name);
    while(true)
    {
        choice = main_menu(myPlayer);

        if(choice == '1')
        {
            train_skill(myPlayer);
        }
        else if(choice == '2')
        {
            check_stats(myPlayer);
        }
        else if(choice == '3')
        {
            fight(myPlayer);
        }
        else if(choice == '4')
        {
            view_inv(myPlayer);
        }
        else if(choice == '5')
        {
            bool drop = false;
            item_creator(myPlayer, drop);
        }
    }
}

char main_menu(player *myPlayer)
{
    //Displays options of main menu
    printf("=====================\n"
    "      Main Menu\n"
    "=====================\n"
    "(1)|Train a Skill\n"
    "---------------------\n"
    "(2)|Check Stats\n"
    "---------------------\n"
    "(3)|Start Fight\n"
    "---------------------\n"
    "(4)|Check Inventory\n"
    "---------------------\n"
    "(5)|Item Creator\n"
    "---------------------\n");

    //Gets chosen option
    bool fchoice;
    printf("Enter an option:\n");
    char choice;
    int next_char;
    do
    {
        choice = getchar();
        while ((next_char = getchar()) != '\n' && next_char != EOF);
        if(choice != '1' && choice != '2' && choice != '3' && choice != '4' && choice != '5')
        {
            fchoice = false;
            printf("Enter a valid option:\n");
        }
        else if(choice == '1' || choice == '2' || choice == '3' || choice == '4' || choice == '5')
        {
            fchoice = true;
        }
    }while(fchoice == false);

    return choice;
}
//displays player stats
void check_stats(player *myPlayer)
{
    myPlayer->combat = round((myPlayer->melee.level + myPlayer->defense.level) / 2);
    if(myPlayer->deaths == 0)
    {
        myPlayer->kd = myPlayer->kills / 1;
    }
    else if(myPlayer->deaths > 0)
    {
        myPlayer->kd = (float)myPlayer->kills / myPlayer->deaths;
    }
    printf("\n=========================\n"
    " %s's Current Levels\n"
    "=========================\n"
    "   |Combat Level: %i  |\n"
    "   |K/D Ratio: %.2f  |\n"
    "   +-----------------+\n"
    "   |HP Level: %i     |\n"
    "   |HP EXP: %i        |\n"
    "   +-----------------+\n"
    "   |Melee Level: %i   |\n"
    "   |Melee EXP: %i     |\n"
    "   +-----------------+\n"
    "   |Defense Level: %i |\n"
    "   |Defense EXP: %i   |\n"
    "   +-----------------+\n"
    "   |Mining Level: %i  |\n"
    "   |Mining EXP: %i    |\n"
    "   +-----------------+\n",
    myPlayer->name,
    myPlayer->combat,
    myPlayer->kd,
    myPlayer->hp.level,
    myPlayer->hp.exp,
    myPlayer->melee.level,
    myPlayer->melee.exp,
    myPlayer->defense.level,
    myPlayer->defense.exp,
    myPlayer->mining.level,
    myPlayer->mining.exp);

    char cont;
    int ch;
    do
    {
        printf("Enter '1' to continue\n");
        scanf(" %c", &cont);
        while((ch = getchar()) != '\n' && ch != EOF);
    }while(cont != '1');
    if(cont == '1')
    {
        return;
    }
}

void fight(player *myPlayer)
{
    srand(time(NULL));
    bool fighting = true;
    bool win = false;
    bool enemy_ran = false;
    int current_hp = myPlayer->hp.level;

    //Initialize new enemy and range of stats, and range of damage
    enemy *new_enemy = malloc(sizeof(enemy));
    if(new_enemy == NULL)
    {
        exit(1);
    }
    int min_melee = myPlayer->melee.level - 1;
    int max_melee = (myPlayer->melee.level + 1) + ENEMY_MAX;
    int min_defense = myPlayer->defense.level - 1;
    int max_defense = (myPlayer->defense.level + 1) + ENEMY_MAX;
    int min_hp = myPlayer->hp.level - 1;
    int max_hp = (myPlayer->hp.level + 1) + ENEMY_MAX;
    if(myPlayer->melee.level == 1)
    {
        min_melee = 1;
    }
    if(myPlayer->defense.level == 1)
    {
        min_defense = 1;
    }

    //Initialize enemy stat levels
    new_enemy->melee.level = (rand() % (max_melee - min_melee + 1)) + min_melee;
    new_enemy->melee.exp = 0;
    strcpy(new_enemy->melee.name, "Melee");
    new_enemy->defense.level = (rand() % (max_defense - min_defense + 1)) + min_defense;
    new_enemy->defense.exp = 0;
    strcpy(new_enemy->defense.name, "Defense");
    new_enemy->hp.level = (rand() % (max_hp - min_hp + 1)) + min_hp;
    new_enemy->hp.exp = 0;
    strcpy(new_enemy->hp.name, "HP");
    int new_enemy_hp = new_enemy->hp.level;
    new_enemy->combat = round((new_enemy->melee.level + new_enemy->defense.level) / 2);

    //Initialize enemy damage counters
    int enemy_base_dmg_min = round(BASE_DMG * new_enemy->melee.level - 1);
    int enemy_base_dmg_max = round(BASE_DMG * new_enemy->melee.level + 1);
    int enemy_base_dmg;
    int enemy_def_dmg;
    if(enemy_base_dmg_min < 0)
    {
        enemy_base_dmg_min = 0;
    }
    else if(enemy_base_dmg_min > enemy_base_dmg_max)
    {
        int temp = enemy_base_dmg_min;
        enemy_base_dmg_min = enemy_base_dmg_max;
        enemy_base_dmg_max = temp;
    }

    //Initialize player damage counter
    int player_base_dmg_min = round(BASE_DMG * myPlayer->melee.level - 1);
    int player_base_dmg_max = round(BASE_DMG * myPlayer->melee.level + 1);
    int player_base_dmg;
    int player_def_dmg;

    //Initialize turn counter and experience factors
    int turn_counter = 0;
    int defend_counter = 0;
    int attack_counter = 0;

    //Set minimum base damage
    if(player_base_dmg_min < 0)
    {
        player_base_dmg_min = 0;
    }
    else if(player_base_dmg_min > player_base_dmg_max)
    {
        int temp = player_base_dmg_min;
        player_base_dmg_min = player_base_dmg_max;
        player_base_dmg_max = temp;
    }

    bool continueLoop = true;

    printf("\n\nAn Enemy stands before you!\n");
    do
    {
        printf("===============\n"
        "Combat Level: %i\n"
        "---------------\n"
        "Enemy HP: %i\n"
        "---------------\n"
        "%s's HP: %i\n"
        "===============\n", new_enemy->combat, new_enemy_hp, myPlayer->name, current_hp);
        printf("(1)|Attack\n"
        "---------------\n"
        "(2)|Defend\n"
        "---------------\n"
        "(3)|Run\n"
        "---------------\n"
        "(4)|Item\n"
        "===============\n");

        //Initialize base damage counters for current turn in fight
        player_base_dmg = rand() % (player_base_dmg_max + 1 - player_base_dmg_min) + player_base_dmg_min;
        if(myPlayer->weapon_item.type == WEAPON)
        {
            player_base_dmg += myPlayer->weapon_item.Weapon.damage;
        }
        enemy_base_dmg = rand() % (enemy_base_dmg_max + 1 - enemy_base_dmg_min) + enemy_base_dmg_min;

        char option;
        do
        {
            option = getchar();
            getchar();
        }while(option != '1' && option != '2' && option != '3' && option != '4');

        //Determines enemy action for each turn
        int enemy_action = rand() % 2 + 1;

        if(option == '3')
        {
            printf("You ran away!\n");
            continueLoop = false;
            break;
        }

        switch(enemy_action)
        {
            //If enemy attacks
            case 1:
                //If player chooses to attack
                if(option == '1')
                {
                    if(enemy_base_dmg <= 0)
                    {
                        enemy_base_dmg = 0;
                        printf("The Enemy missed!\n");
                    }
                    else if(enemy_base_dmg > 0)
                    {
                        current_hp -= enemy_base_dmg;
                        printf("The Enemy dealt %i damage!\n", enemy_base_dmg);
                    }
                    if(player_base_dmg <= 0)
                    {
                        player_base_dmg = 0;
                        printf("%s missed!\n", myPlayer->name);
                    }
                    else if(player_base_dmg > 0)
                    {
                        new_enemy_hp -= player_base_dmg;
                        //If the player doesn't have a weapon
                        if(myPlayer->weapon_item.type == EMPTY)
                        {
                            printf("%s dealt %i damage!\n", myPlayer->name, player_base_dmg);
                        }
                        //If the player does have a weapon
                        else if(myPlayer->weapon_item.type == WEAPON)
                        {
                            printf("%s dealt %i damage using their %s!\n", myPlayer->name, player_base_dmg, myPlayer->weapon_item.Weapon.name);
                        }
                        attack_counter += 1;
                    }
                    break;
                }
                //If player chooses to defend
                else if(option == '2')
                {
                    enemy_def_dmg = round(enemy_base_dmg / (myPlayer->defense.level * 0.3));
                    if(enemy_def_dmg <= 0)
                    {
                        enemy_def_dmg = 0;
                        defend_counter += 2;
                        printf("%s defended themselves successfully!\n", myPlayer->name);
                    }
                    else
                    {
                        current_hp -= enemy_def_dmg;
                        defend_counter += 1;
                        printf("Despite %s's defenses, the Enemy dealt %i damage!\n", myPlayer->name, enemy_def_dmg);
                    }
                    break;
                }
                //If player uses an item
                else if(option == '4')
                {
                    //prints out inventory items
                    printf("========================\n");
                    for(int i = 0; i < INV_SIZE; i++)
                    {
                        if(myPlayer->inv.items[i].type == POTION)
                        {
                            printf("(%i)|%s\nHeals: %i\n", i + 1, myPlayer->inv.items[i].Potion.name, myPlayer->inv.items[i].Potion.heal);
                        }
                        else if(myPlayer->inv.items[i].type == WEAPON)
                        {
                            printf("(%i)|%s\nDamage: %i\n", i + 1, myPlayer->inv.items[i].Weapon.name, myPlayer->inv.items[i].Weapon.damage);
                        }
                        else if(myPlayer->inv.items[i].type == ORE)
                        {
                            printf("(%i)|%s Ore\n", i + 1, myPlayer->inv.items[i].Ore.type);
                        }
                        else if(myPlayer->inv.items[i].type == EMPTY)
                        {
                            printf("(%i)|Empty Inventory Slot\n", i + 1);
                        }
                        if(i < INV_SIZE)
                        {
                            printf("------------------------\n");
                        }
                        else if(i + 1 == INV_SIZE)
                        {
                            printf("========================\n");
                        }
                    }
                    //select item from inventory
                    char item_option;
                    do
                    {
                        printf("Which item should %s use?\n", myPlayer->name);
                        item_option = getchar();
                        getchar();
                    }while(item_option != '1' && item_option != '2' && item_option != '3' && item_option != '4' && item_option != '5');
                    //Consume item
                    item_option = (item_option - '0') - 1;
                    for(int i = 0; i < INV_SIZE; i++)
                    {
                        if(i == item_option)
                        {
                            if(myPlayer->inv.items[i].type == POTION)
                            {
                                printf("\n\n%s drank the %s!\n", myPlayer->name, myPlayer->inv.items[i].Potion.name);
                                current_hp += myPlayer->inv.items[i].Potion.heal;
                                myPlayer->inv.items[i].type = EMPTY;
                                free(myPlayer->inv.items[i].Potion.name);
                                break;
                            }
                            else if(myPlayer->inv.items[i].type == EMPTY)
                            {
                                printf("There is no item in that inventory slot.\n");
                            }
                            else
                            {
                                printf("You cannot use that item now.\n");
                            }
                        }
                    }
                    if(enemy_base_dmg <= 0)
                    {
                        enemy_base_dmg = 0;
                        printf("The Enemy missed!\n");
                    }
                    else if(enemy_base_dmg > 0)
                    {
                        current_hp -= enemy_base_dmg;
                        printf("The Enemy dealt %i damage!\n", enemy_base_dmg);
                    }
                    break;
                }
            //If enemy defends
            case 2:
                //If player chooses to attack
                if(option == '1')
                {
                    //If the player doesn't have a weapon
                    if(myPlayer->weapon_item.type == EMPTY)
                    {
                        player_def_dmg = round(player_base_dmg / (new_enemy->defense.level * 0.3));

                        if(player_def_dmg <= 0)
                        {
                            player_def_dmg = 0;
                            printf("The Enemy's defense held strong!\n");
                        }
                        else if(player_def_dmg > 0)
                        {
                            attack_counter += 1;
                            printf("Despite the Enemy's defense, %s dealt %i damage!\n", myPlayer->name, player_def_dmg);
                        }
                    }
                    //If the player does have a weapon
                    else if(myPlayer->weapon_item.type == WEAPON)
                    {
                        player_def_dmg = round((player_base_dmg / (new_enemy->defense.level * 0.3)) + myPlayer->weapon_item.Weapon.damage);

                        if(player_def_dmg <= 0)
                        {
                            player_def_dmg = 0;
                            printf("Despite %s's %s, the Enemy's defense held strong!\n", myPlayer->name, myPlayer->weapon_item.Weapon.name);
                        }
                        else if(player_def_dmg > 0)
                        {
                            printf("Depsite the Enemy's defense, %s dealt %i damage with their %s!\n", myPlayer->name, player_def_dmg, myPlayer->weapon_item.Weapon.name);
                        }
                    }
                    new_enemy_hp -= player_def_dmg;
                    break;
                }
                //If player chooses to defend
                else if(option == '2')
                {
                    printf("Both %s and the Enemy wait for the next move.\n", myPlayer->name);
                    break;
                }
                //If player uses an item
                else if(option == '4')
                {
                    //prints out inventory items
                    printf("========================\n");
                    for(int i = 0; i < INV_SIZE; i++)
                    {
                        if(myPlayer->inv.items[i].type == POTION)
                        {
                            printf("(%i)|%s\nHeals: %i\n", i + 1, myPlayer->inv.items[i].Potion.name, myPlayer->inv.items[i].Potion.heal);
                        }
                        else if(myPlayer->inv.items[i].type == WEAPON)
                        {
                            printf("(%i)|%s\nDamage: %i\n", i + 1, myPlayer->inv.items[i].Weapon.name, myPlayer->inv.items[i].Weapon.damage);
                        }
                        else if(myPlayer->inv.items[i].type == ORE)
                        {
                            printf("(%i)|%s Ore\n", i + 1, myPlayer->inv.items[i].Ore.type);
                        }
                        else if(myPlayer->inv.items[i].type == EMPTY)
                        {
                            printf("(%i)|Empty Inventory Slot\n", i + 1);
                        }
                        if(i < INV_SIZE)
                        {
                            printf("------------------------\n");
                        }
                        else if(i + 1 == INV_SIZE)
                        {
                            printf("========================\n");
                        }
                    }
                    //select item from inventory
                    char item_option;
                    do
                    {
                        printf("Which item should %s use?\n", myPlayer->name);
                        item_option = getchar();
                        getchar();
                    }while(item_option != '1' && item_option != '2' && item_option != '3' && item_option != '4' && item_option != '5');
                    //Consume item
                    item_option = (item_option - '0') - 1;
                    for(int i = 0; i < INV_SIZE; i++)
                    {
                        if(i == item_option)
                        {
                            if(myPlayer->inv.items[i].type == POTION)
                            {
                                printf("The Enemy guarded themselves.\n%s drank the %s!\n", myPlayer->name, myPlayer->inv.items[i].Potion.name);
                                current_hp += myPlayer->inv.items[i].Potion.heal;
                                myPlayer->inv.items[i].type = EMPTY;
                                free(myPlayer->inv.items[i].Potion.name);
                                break;
                            }
                            else if(myPlayer->inv.items[i].type == EMPTY)
                            {
                                printf("There is no item in that inventory slot.\n");
                            }
                            else
                            {
                                printf("You cannot use that item now.\n");
                            }
                        }
                    }
                    break;
                }
        }
    }while((current_hp > 0 && new_enemy_hp > 0) && continueLoop);

    if(new_enemy_hp <= 0)
    {
        //If player wins fight, reward exp and possible item drop
        win = true;
        myPlayer->kills += 1;
        calculate_exp(myPlayer, &defend_counter, &attack_counter, new_enemy);
        int drop = rand() % 2;
        bool is_dropped = false;
        if(drop == 0)
        {
            is_dropped = true;
            item_creator(myPlayer, is_dropped);
        }
        return;
    }
    else if(current_hp <= 0)
    {
        win = false;
        myPlayer->deaths += 1;
        printf("%s was defeated.\n", myPlayer->name);
        return;
    }
}
int calculate_exp(player *myPlayer, int *defend_counter, int *attack_counter, enemy *new_enemy)
{
    //Exp calculations from winning a fight
    int hp_exp = (int)round(new_enemy->hp.level * 0.25);
    int melee_exp = (int)round(new_enemy->melee.level * ((double)*attack_counter / 5));
    int defense_exp = (int)round(new_enemy->defense.level * ((double)*defend_counter / 5));
    myPlayer->hp.exp += hp_exp;
    myPlayer->melee.exp += melee_exp;
    myPlayer->defense.exp += defense_exp;
    printf("======================\n"
    " %s is victorious!\n"
    "======================\n"
    "|HP EXP: %i       |\n"
    "+----------------|\n"
    "|Melee EXP: %i    |\n"
    "+----------------|\n"
    "|Defense EXP: %i  |\n"
    "+----------------+\n", myPlayer->name, hp_exp, melee_exp, defense_exp);
    //Level up if exp in stat reaches level threshold
    if(myPlayer->hp.exp >= myPlayer->hp.level * 5)
    {
        int total = myPlayer->hp.level * 5;
        myPlayer->hp.level++;
        myPlayer->hp.exp -= total;
        printf("%s's HP Level is now %i!\n", myPlayer->name, myPlayer->hp.level);
    }
    if(myPlayer->melee.exp >= myPlayer->melee.level * 3)
    {
        int total = myPlayer->melee.level * 3;
        myPlayer->melee.level++;
        myPlayer->melee.exp -= total;
        printf("%s's Melee Level is now %i!\n", myPlayer->name, myPlayer->melee.level);
    }
    if(myPlayer->defense.exp >= myPlayer->defense.level * 3)
    {
        int total = myPlayer->defense.level * 3;
        myPlayer->defense.level++;
        myPlayer->defense.exp -= total;
        printf("%s's Defense Level is now %i!\n", myPlayer->name, myPlayer->defense.level);
    }
    char cont;
    do
    {
        printf("Enter '1' to continue\n");
        cont = getchar();
        getchar();
    }while(cont != '1');
}

void train_skill(player *myPlayer)
{
    //Choose which skill to train
    printf("\n\n====================\n"
    "   Skill Training\n"
    "====================\n"
    "(1)|Melee\n"
    "-------------\n"
    "(2)|Defense\n"
    "-------------\n"
    "(3)|Mining\n"
    "-------------\n"
    "(4)|Exit\n"
    "-------------\n");

    printf("Enter an option:\n");
    char option = getchar();
    getchar();
    int next_char;
    bool foption;

    do
    {
        if(option != '1' && option != '2' && option != '3' && option != '4')
        {
            foption = false;
            printf("Enter a valid option:\n");
            option = getchar();
            while((next_char = getchar()) != '\n' && next_char != EOF);
        }
        if(option == '1')
        {
            increase_melee(myPlayer);
            foption = true;
        }
        else if(option == '2')
        {
            increase_defense(myPlayer);
            foption = true;
        }
        else if(option == '3')
        {
            increase_mining(myPlayer);
            foption = true;
        }
        else if(option == '4')
        {
            foption = true;
            return;
        }
    }while(foption == false);
}

int increase_mining(player *myPlayer)
{
    //array of strings
    char* words[] = {"pickaxe", "ore", "prospect", "copper", "tin"};
    bool mining;
    int ch;

    //starts loop of attempts to type correct string
    do
    {
        //intitializing random seed, bools, and random string from array
        srand(time(NULL));
        mining = true;
        int word = rand() % 5;
        char* type_word = words[word];
        char attempt[10];

        printf("=====================\n"
        "   Mining Training!\n"
        "======================\n"
        "Type: '%s'\n"
        "---------------\n", type_word);

        //user input
        fgets(attempt, 10, stdin);
        if(attempt[strlen(attempt) - 1] != '\n')
        {
            while((ch = getchar()) != '\n' && ch != EOF);
        }
        for(int i = 0; i < strlen(attempt); i++)
        {
            if(attempt[i] == '\n')
            {
                attempt[i] = '\0';
            }
        }
        if(strcasecmp(type_word, attempt) == 0)
        {
            //If typed word is correct, reward exp and possible ore drop
            int exp_gained = 1;
            myPlayer->mining.exp += exp_gained;
            printf("\n\n==========\n Correct!\n==========\n%s gained %i Mining EXP!\n", myPlayer->name, exp_gained);
            if(myPlayer->mining.exp >= myPlayer->mining.level * 3)
            {
                int total = myPlayer->mining.level * 3;
                myPlayer->mining.level++;
                myPlayer->mining.exp -= total;
                printf("%s's Mining Level is now %i!\n", myPlayer->name, myPlayer->mining.level);
            }
            //Create ore if ore is dropped
            int ore_drop = rand() % 10;
            bool is_dropped = false;
            if(ore_drop == 0)
            {
                item_creator(myPlayer, is_dropped);
            }

            printf("Would you like to keep training?\n-------\n(1)|Yes\n-------\n(2)|No\n-------\n");
            char option;
            do
            {
                option = getchar();
                getchar();
                if(option == '1')
                {
                    mining = false;
                }
                else if(option == '2')
                {
                    mining = true;
                }
                else if(option != '1' && option != '2')
                {
                    printf("Would you like to keep training?\n-------\n(1)|Yes\n-------\n(2)|No\n-------\n");
                }
            }while(option != '1' && option != '2');
        }
        else if(strcasecmp(type_word, attempt) != 0)
        {
            printf("\n\n============\n Incorrect.\n============\nTry again.\n\n\n");
            mining = false;
        }
    }while(mining == false);
}

//increase defense
int increase_defense(player *myPlayer)
{
    //array of strings
    char* words[] = {"defend", "practice", "fight", "protect"};
    bool training;
    int ch;
    //Starts loop of attempts to type correct string
    do
    {
        //initialize random seed, bools, and random strings from array
        srand(time(NULL));
        training = true;
        int word = rand() % 4;
        char* type_word = words[word];
        char attempt[10];

        printf("=====================\n"
        "  Defense Training!\n"
        "=====================\n"
        "Type: '%s'\n"
        "---------------\n", type_word);

        //get user input and compare to chosen random string
        fgets(attempt, 10, stdin);
        if(attempt[strlen(attempt) - 1] != '\n')
        {
            while((ch = getchar()) != '\n' && ch != EOF);
        }
        for(int i = 0; i < strlen(attempt); i++)
        {
            if(attempt[i] == '\n')
            {
                attempt[i] = '\0';
            }
        }
        if(strcasecmp(type_word, attempt) == 0)
        {
            int exp_gained = 1;
            myPlayer->defense.exp += exp_gained;
            printf("\n\n==========\n Correct!\n==========\n%s gained %i Defense EXP!\n", myPlayer->name, exp_gained);
            if(myPlayer->defense.exp >= myPlayer->defense.level * 3)
            {
                int total = myPlayer->defense.level * 3;
                myPlayer->defense.level++;
                myPlayer->defense.exp -= total;
                printf("%s's Defense Level is now %i!\n", myPlayer->name, myPlayer->defense.level);
            }
            char option;
            printf("Would you like to keep training?\n-------\n(1)|Yes\n-------\n(2)|No\n-------\n");
            do
            {
                option = getchar();
                getchar();
                if(option == '1')
                {
                    training = false;
                }
                else if(option == '2')
                {
                    training = true;
                }
                else if(option != '1' && option != '2')
                {
                    printf("Would you like to keep training?\n-------\n(1)|Yes\n-------\n(2)|No\n-------\n");
                }
            }while(option != '1' && option != '2');
        }
        else if(strcasecmp(type_word, attempt) != 0)
        {
            printf("\n\n============\n Incorrect.\n============\nTry again.\n\n\n");
            training = false;
        }
    }while(training == false);
}

//increase melee
int increase_melee(player *myPlayer)
{
    //array of strings
    char* words[] = {"attack", "spar", "slash", "weapon"};
    bool training;
    int ch;

    //initializing random seed, bool, and typed words
    do
    {
        srand(time(NULL));
        training = true;
        int word = rand() % 4;
        char* type_word = words[word];
        char attempt[10];

        printf("=====================\n"
        "   Melee Training!\n"
        "=====================\n"
        "Type: '%s'\n"
        "---------------\n", type_word);

        fgets(attempt, 10, stdin);
        if(attempt[strlen(attempt) - 1] != '\n')
        {
            while((ch = getchar()) != '\n' && ch != EOF);
        }
        for(int i = 0; i < strlen(attempt); i++)
        {
            if(attempt[i] == '\n')
            {
                attempt[i] = '\0';
            }
        }
        //if player word attempt is correct
        if(strcasecmp(attempt, type_word) == 0)
        {
            int exp_gained = 1;
            myPlayer->melee.exp += exp_gained;
            printf("\n\n==========\n Correct!\n==========\n%s gained %i Melee EXP!\n", myPlayer->name, exp_gained);
            if(myPlayer->melee.exp >= myPlayer->melee.level * 3)
            {
                int total = myPlayer->melee.level * 3;
                myPlayer->melee.level++;
                myPlayer->melee.exp -= total;
                printf("%s's Melee Level is now %i!\n", myPlayer->name, myPlayer->melee.level);
            }
            char option;
            printf("Would you like to keep training?\n-------\n(1)|Yes\n-------\n(2)|No\n-------\n");
            do
            {
                option = getchar();
                getchar();
                if(option == '1')
                {
                    training = false;
                }
                else if(option == '2')
                {
                    training = true;
                }
                else if(option != '1' && option != '2')
                {
                    printf("Would you like to kep training?\n-------\n(1)|Yes\n-------\n(2)|No\n-------\n");
                }
            }while(option != '1' && option != '2');
        }
        //if player word attempt is incorrect
        else if(strcasecmp(attempt, type_word) != 0)
        {
            printf("\n\n============\n Incorrect.\n============\nTry again.\n\n\n");
            training = false;
        }
    }while(training == false);
}

void view_inv(player *myPlayer)
{
    //View inventory slots
    printf("=====================\n"
    "  %s's Inventory\n"
    "=====================\n", myPlayer->name);
    for(int i = 0; i < INV_SIZE; i++)
    {
        //if item slot is empty or not
        if(myPlayer->inv.items[i].type == EMPTY)
        {
            printf("Empty Inventory Slot\n"
            "------------------------\n");
        }
        //If potion is in item slot
        if(myPlayer->inv.items[i].type == POTION)
        {
            printf("(%i)|%s\nHeals: %i HP\n"
            "------------------------\n", i + 1, myPlayer->inv.items[i].Potion.name, myPlayer->inv.items[i].Potion.heal);
        }
        //if weapon is in item slot
        else if(myPlayer->inv.items[i].type == WEAPON)
        {
            printf("(%i)|%s\nDamage: %i\n"
            "------------------------\n", i + 1, myPlayer->inv.items[i].Weapon.name, myPlayer->inv.items[i].Weapon.damage);
        }
        //if ore is in item slot
        else if(myPlayer->inv.items[i].type == ORE)
        {
            printf("(%i)|%s Ore\n"
            "------------------------\n", i + 1, myPlayer->inv.items[i].Ore.type);
        }
    }
    if(myPlayer->weapon_item.type == EMPTY)
    {
        printf("Weapon Slot\n"
        "=============\n"
        "Empty Weapon Slot\n");
    }
    else if(myPlayer->weapon_item.type == WEAPON)
    {
        printf("Weapon Slot\n"
        "=============\n"
        "%s\nDamage: %i\n"
        "-------------\n", myPlayer->weapon_item.Weapon.name, myPlayer->weapon_item.Weapon.damage);
    }
    printf("Enter '1' to exit\n"
    "Enter '2' to drop an item\n"
    "Enter '3' to equip an item\n");
    bool weapon;
    if(myPlayer->weapon_item.type == WEAPON)
    {
        weapon = true;
        printf("Enter '4' to unequip an item\n");
    }
    char cont;
    do
    {
        cont = getchar();
        getchar();
        if(cont != '1' && cont != '2' && cont != '3' && cont != '4')
        {
            printf("Enter '1' to continue\n"
            "Enter '2' to drop an item\n"
            "Enter '3' to equip an item\n");
        }
        if(myPlayer->weapon_item.type == WEAPON)
        {
            if(cont != '1' && cont != '2' && cont != '3' && cont != '4')
            {
                printf("Enter '4' to unequip an item\n");
            }
        }
    }while(cont != '1' && cont != '2' && cont != '3' && cont != '4');
    if(cont == '1')
    {
        return;
    }
    else if(cont == '2')
    {
        drop_item(myPlayer);
    }
    else if(cont == '3')
    {
        equip_item(myPlayer);
    }
    else if(cont == '4')
    {
        if(myPlayer->weapon_item.type == EMPTY)
        {
            printf("There is no item equipped.\n");
        }
        else if(myPlayer->weapon_item.type == WEAPON)
        {
            unequip_item(myPlayer);
        }
    }
}

void item_creator(player *myPlayer, bool drop)
{
    bool empty = false;
    //If this function is called via getting a dropped item from the fight function
    if(drop == true)
    {
        //Use rand() to determine which kind of item you get
        srand(time(NULL));
        bool is_potion;//rand_item = 0
        bool is_weapon;//rand_item = 1
        int rand_item = rand() % 2;
        if(rand_item == 0)
        {
            //malloc memory for potion struct, and potion name field
            potion *pot = malloc(sizeof(potion));
            if(pot == NULL)
            {
                exit(1);
            }
            pot->name = malloc(strlen("Healing Potion") + 1);
            if(pot->name == NULL)
            {
                exit(1);
            }
            strcpy(pot->name, "Healing Potion");
            pot->heal = 10;
            //Add potion to inventory if empty slot is found
            for(int i = 0; i < INV_SIZE; i++)
            {
                if(myPlayer->inv.items[i].type == EMPTY)
                {
                    //initialize potion struct fields and add to inventory
                    myPlayer->inv.items[i].type = POTION;
                    myPlayer->inv.items[i].Potion = *pot;
                    myPlayer->inv.items[i].Potion.heal = pot->heal;
                    myPlayer->inv.items[i].Potion.name = malloc(strlen(pot->name) + 1);
                    if(myPlayer->inv.items[i].Potion.name == NULL)
                    {
                        exit(1);
                    }
                    strcpy(myPlayer->inv.items[i].Potion.name, pot->name);
                    printf("%s got a %s!\n", myPlayer->name, myPlayer->inv.items[i].Potion.name);
                    empty = true;
                    break;
                }
            }
        }
        else if(rand_item == 1)
        {
            weapon *wep = malloc(sizeof(weapon));
            if(wep == NULL)
            {
                exit(1);
            }
            wep->name = malloc(strlen("Sword") + 1);
            if(wep->name == NULL)
            {
                exit(1);
            }
            strcpy(wep->name, "Sword");
            wep->damage = 2;

            for(int i = 0; i < INV_SIZE; i++)
            {
                if(myPlayer->inv.items[i].type == EMPTY)
                {
                    //Initalize weapon struct fields and add to inventory
                    myPlayer->inv.items[i].type = WEAPON;
                    myPlayer->inv.items[i].Weapon = *wep;
                    myPlayer->inv.items[i].Weapon.damage = wep->damage;
                    myPlayer->inv.items[i].Weapon.name = malloc(strlen(wep->name) + 1);
                    if(myPlayer->inv.items[i].Weapon.name == NULL)
                    {
                        exit(1);
                    }
                    strcpy(myPlayer->inv.items[i].Weapon.name, wep->name);
                    printf("%s got a %s!\n", myPlayer->name, myPlayer->inv.items[i].Weapon.name);
                    empty = true;
                    break;
                }
            }
        }
        if(!empty)
        {
            printf("Your inventory is full!\n");
        }
    }
    //If this function is called via training mining
    else if(drop != true)
    {
        //Creates either Tin or Copper ore
        srand(time(NULL));
        ore *ore = malloc(sizeof(ore));
        if(ore == NULL)
        {
            exit(1);
        }
        int ore_type = rand() % 2;
        if(ore_type == 0)
        {
            ore->type = malloc(strlen("Tin") + 1);
            if(ore->type == NULL)
            {
                exit(1);
            }
            strcpy(ore->type, "Tin");
        }
        else if(ore_type == 1)
        {
            ore->type = malloc(strlen("Copper") + 1);
            if(ore->type == NULL)
            {
                exit(1);
            }
            strcpy(ore->type, "Copper");
        }
        for(int i = 0; i < INV_SIZE; i++)
        {
            //if inventory slot is empty
            if(myPlayer->inv.items[i].type == EMPTY)
            {
                //Initialize ore item fields and add to inventory
                myPlayer->inv.items[i].type = ORE;
                myPlayer->inv.items[i].Ore = *ore;
                myPlayer->inv.items[i].Ore.type = ore->type;
                strcpy(myPlayer->inv.items[i].Ore.type, ore->type);
                printf("%s got some %s Ore!\n", myPlayer->name, myPlayer->inv.items[i].Ore.type);
                empty = true;
                break;
            }
        }
        if(!empty)
        {
            printf("Your inventory is full!\n");
        }
    }
}

void drop_item(player *myPlayer)
{
    //Select which item from the inventory to drop
    printf("Which item would you like to drop?\n");
    char option;
    do
    {
        option = getchar();
        int ch;
        while((ch = getchar()) != '\n' && ch != '\n');
        for(int i = 0; i < INV_SIZE; i++)
        {
            if(i + 1 == option - '0')
            {
                switch(myPlayer->inv.items[i].type)
                {
                    //If the item is a potion
                    case POTION:
                        myPlayer->inv.items[i].type = EMPTY;
                        free(myPlayer->inv.items[i].Potion.name);
                        printf("You dropped the item.\n");
                        break;
                    //If the item is a weapon
                    case WEAPON:
                        myPlayer->inv.items[i].type = EMPTY;
                        free(myPlayer->inv.items[i].Weapon.name);
                        printf("You dropped the item.\n");
                        break;
                    //If the item is an ore
                    case ORE:
                        myPlayer->inv.items[i].type = EMPTY;
                        free(myPlayer->inv.items[i].Ore.type);
                        printf("You dropped the item.\n");
                        break;
                    //If the inventory slot is empty
                    case EMPTY:
                        printf("This inventory slot is already empty.\n");
                }
            }
        }

    }while(option != '1' && option != '2' && option != '3' && option != '4' && option != '5');
}

void equip_item(player *myPlayer)
{
    //Choose which item in inventory to equip
    printf("Which item would you like to equip?\n");
    char option;
    do
    {
        option = getchar();
        int ch;
        while((ch = getchar()) != '\n' && ch != '\n');
        for(int i = 0; i < INV_SIZE; i++)
        {
            if(i + 1 == option - '0')
            {
                //If player's weapon slot is empty
                if(myPlayer->weapon_item.type == EMPTY)
                {
                    switch(myPlayer->inv.items[i].type)
                    {
                        //If selected item is a potion
                        case POTION:
                            printf("That item is not equippable.\n");
                            break;
                        //If selected item is a weapon
                        case WEAPON:
                            //Move the weapon from the inventory into the weapon slot
                            myPlayer->weapon_item.type = WEAPON;
                            myPlayer->weapon_item.Weapon.name = myPlayer->inv.items[i].Weapon.name;
                            myPlayer->weapon_item.Weapon.damage = myPlayer->inv.items[i].Weapon.damage;

                            //Set inventory slot to empty
                            myPlayer->inv.items[i].type = EMPTY;
                            myPlayer->inv.items[i].Weapon.name = NULL;
                            myPlayer->inv.items[i].Weapon.damage = 0;
                            break;
                        //If selected item is an ore
                        case ORE:
                            printf("That item is not equippable.\n");
                            break;
                        //If selected inventory slot is empty
                        case EMPTY:
                            printf("There is no item in that inventory slot.\n");
                            break;
                    }
                }
                //If player's weapon slot is filled
                else
                {
                    printf("You must unequip your current weapon first!\n");
                    break;
                }
            }
        }
    }while(option != '1' && option != '2' && option != '3' && option != '4' && option != '5');
}

void unequip_item(player *myPlayer)
{
    bool empty = false;
    //Check if there is an empty slot
    for(int i = 0; i < INV_SIZE; i++)
    {
        if(myPlayer->inv.items[i].type == EMPTY)
        {
            empty = true;
            myPlayer->inv.items[i].type = WEAPON;
            myPlayer->inv.items[i].Weapon.name = myPlayer->weapon_item.Weapon.name;
            myPlayer->inv.items[i].Weapon.damage = myPlayer->weapon_item.Weapon.damage;
            myPlayer->weapon_item.type = EMPTY;
            myPlayer->weapon_item.Weapon.name = NULL;
            myPlayer->weapon_item.Weapon.damage = 0;
            break;
        }
    }
    if(!empty)
    {
        printf("Your inventory is fulL!\n");
        return;
    }
}

