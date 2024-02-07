#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>

#define MAX_ITEMS 5

//prototypes
int increase_melee(player *myplayer);
int increase_defense(player *myplayer);
char choose(void);
void fight(player *myplayer);
void check_stats(player *myplayer);
void level_up(stat *stat_ptr, player *myplayer);
void add_to_inventory(item *item, player *myplayer);
char* sword_names(sword_type sword);
void drop_item(player* myplayer);
void check_inventory(player *myplayer);

//General yes and no answers to compare user input to
char yes[] = "Yes";
char no[] = "No";

int main(void)
{
    //Creates player and asks for users name
    player *myplayer = malloc(sizeof(player));
    if(myplayer == NULL)
    {
        return 1;
    }

    //Initializes player stats
    myplayer->hp.level = 10;
    myplayer->hp.exp = 0;
    strcpy(myplayer->hp.name, "HP");
    myplayer->melee.level = 1;
    myplayer->melee.exp = 0;
    strcpy(myplayer->melee.name, "Melee");
    myplayer->defense.level = 1;
    myplayer->defense.exp = 0;
    strcpy(myplayer->defense.name, "Defense");
    myplayer->weapon = NULL;
    myplayer->combat = (int) ((myplayer->melee.level + myplayer->hp.level + myplayer->defense.level) / 3);

    //Initialize inventory
    for(int i = 0; i < MAX_ITEMS; i++)
    {
        myplayer->inv.items[i] = NULL;
    }

    printf("Hello, and welcome to TextScape. Tell me, what is your name?\n");
    fgets(myplayer->name, 10, stdin);

    //Removes newline character from players name
    char *newline = strchr(myplayer->name, '\n');
    if(newline)
    {
        *newline = '\0';
    }

    //Question to determine the players preferred stat
    char def_answer[4];
    bool first = true;
    do
    {
        if (first)
        {
            printf("Ah.. %s... I see..\nWould you say you are more defensive than offensive?\nYes/No:\n", myplayer->name);
            first = false;
        }
        else
        {
            printf("Can you repeat that?\nYes/No:\n");
        }

        fgets(def_answer, 4, stdin);
        char *newline = strchr(def_answer, '\n');
        if(newline)
        {
            *newline = '\0';
        }
    }
    while(strcasecmp(def_answer, yes) != 0 && strcasecmp(def_answer, no) != 0);

    //Calls stat functions based on answer
    if(strcasecmp(def_answer, yes) == 0)
    {
        printf("Of course, you seem to be a sturdy adventurer!\n");
        increase_defense(myplayer);
    }
    else if(strcasecmp(def_answer, no) == 0)
    {
        printf("That makes sense, as you seem to be proficient with a weapon!\n");
        increase_melee(myplayer);
    }

    printf("\n<===============================================>\n"
    "   Now, go forth, into the world of TextScape!\n"
    "<===============================================>\n");
    //Call choose function for players choice of activity
    do
    {
        char choice = choose();
        //Calls activity function
        if(choice == '1')
        {
            increase_melee(myplayer);
        }
        else if(choice == '2')
        {
            increase_defense(myplayer);
        }
        else if (choice == '3')
        {
            fight(myplayer);
        }
        else if (choice == '4')
        {
            check_stats(myplayer);
        }
        else if (choice == '5')
        {
            check_inventory(myplayer);
        }
    }
    while(true);
}

//Increases melee
int increase_melee(player *myplayer)
{
    if(myplayer->melee.level == 99)
    {
        printf("Your Melee Level is maxed!\n");
    }
    else
    {
        myplayer->melee.level++;
        printf("Your Melee Level is now %i!\n", myplayer->melee.level);
    }
}

//Increases defense
int increase_defense(player *myplayer)
{
    if(myplayer->defense.level == 99)
    {
        printf("Your Defense Level is maxed!\n");
    }
    else
    {
        myplayer->defense.level++;
        printf("Your Defense Level is now %i!\n", myplayer->defense.level);
    }
}

//Displays list of options for player, and returns the player's choice
char choose(void)
{
    char choice[3];

    printf("\n<=================>\n"
    "     Main Menu\n"
    "<=================>\n"
    "1. Train Melee\n"
    "================\n"
    "2. Train Defense\n"
    "================\n"
    "3. Fight\n"
    "================\n"
    "4. Check Stats\n"
    "================\n"
    "5. Check Inventory\n"
    "================\n");

    do
    {
        printf("Choose an activity:\n");
        fgets(choice, 3, stdin);
        char ch;

        char *newline = strchr(choice, '\n');
        if(newline)
        {
            *newline = '\0';
        }
    }
    while(choice[0] != '1' && choice[0] != '2' && choice[0] != '3' && choice[0] != '4' && choice[0] != '5');

    return choice[0];
}

void check_stats(player *myplayer)
{
    printf("\n<========================>\n  "
    "%s's Current Levels\n"
    "<========================>\n"
    "Combat Level: %i |"
    "\n-----------------\nHP Level: %i     |"
    "\n-----------------\nHP EXP: %i        |"
    "\n-----------------\nMelee Level: %i   |"
    "\n-----------------\nMelee EXP: %i     |"
    "\n-----------------\nDefense Level: %i |"
    "\n-----------------\nDefense EXP: %i   |"
    "\n-----------------\n", myplayer->name, myplayer->combat, myplayer->hp.level, myplayer->hp.exp, myplayer->melee.level, myplayer->melee.exp, myplayer->defense.level, myplayer->defense.exp);

    printf("Enter '1' to exit\n");

    char exit[4];
    do
    {
        fgets(exit, 4, stdin);

        char *newline = strchr(exit, '\n');
        if(newline)
        {
            *newline = '\0';
        }
    }
    while(strcasecmp(exit, "1") != 0);
}

//Initiates fight
void fight(player *myplayer)
{
    srand(time(NULL));

    //Initializes player's current HP
    int currenthp = myplayer->hp.level;

    //Initializes variables to calculate range of enemy stats
    enemy new_enemy;
    int hpmin = myplayer->hp.level - 2;
    int hpmax = myplayer->hp.level + 1;
    int melee_min;
    int melee_max = myplayer->melee.level + 1;
    int defense_min;
    int defense_max = myplayer->defense.level + 1;

    if(myplayer->melee.level == 1)
    {
        melee_min = 1;
    }
    else
    {
        melee_min = myplayer->melee.level - 1;
    }

    if(myplayer->defense.level == 1)
    {
        defense_min = 1;
    }
    else
    {
        defense_min = myplayer->defense.level - 1;
    }

    //Initializes random range of enemy stats
    new_enemy.hp = hpmin + rand() % (hpmax - hpmin + 1);
    int enemy_hp_exp = new_enemy.hp;
    new_enemy.melee = melee_min + rand() % (melee_max - melee_min + 1);
    new_enemy.defense = defense_min + rand() % (defense_max - defense_min + 1);
    new_enemy.combat = (new_enemy.melee + new_enemy.defense + new_enemy.hp) / 3;

    if(new_enemy.combat > myplayer->combat)
    {
        printf("\n\n\n<===================================>\n"
        "  A strong Enemy stands before you.\n"
        "<===================================>\n");
    }
    else if(new_enemy.combat < myplayer->combat)
    {
        printf("\n\n\n<===================================>\n"
        "   A weak Enemy stands before you.\n"
        "<===================================>\n");
    }
    else if(new_enemy.combat == myplayer->combat)
    {
        printf("\n\n\n<===================================>\n"
        "     An Enemy stands before you.\n"
        "<===================================>\n");
    }

    int turn_counter = 0;
    bool run_away = false;

    //Prompts user for action input
    while(currenthp > 0 && new_enemy.hp > 0 && run_away == false)
    {
        printf("\n<==============>\n"
        " Enemy HP: %i\n %s's HP: %i\n"
        "<==============>\n"
        "(1) Attack\n"
        "(2) Protect\n"
        "(3) Run\n", new_enemy.hp, myplayer->name, currenthp);

        char action[5];
        do
        {
            printf("Choose an action:\n");
            fgets(action, 5, stdin);
            char ch;

            char *newline = strchr(action, '\n');
            if(newline)
            {
                *newline = '\0';
            }
        }
        while(action[0] != '1' && action[0] != '2' && action[0] != '3');

        //Initialize player damage counter
        int player_base_dmg = rand() % 3 + 1;
        float player_dmg = myplayer->melee.level * 0.2;
        float total_player_dmg = player_base_dmg + player_dmg;
        total_player_dmg = round(total_player_dmg);

        //Initialize enemy damage counter
        int base_enemy_dmg = rand() % 3 + 1;
        float enemy_dmg = new_enemy.melee * 0.2;
        float total_enemy_dmg = base_enemy_dmg + enemy_dmg;
        total_enemy_dmg = round(total_enemy_dmg);

        int enemy_action = rand() % 2;

        //Change gameplay depending on enemies random actions and player's input
        switch(enemy_action)
        {
            case 0:
                //Enemy attack
                if(action[0] == '1')
                {
                    printf("\n\n\n%s dealt %.0f damage!\n", myplayer->name, total_player_dmg);
                    printf("The Enemy dealt %.0f damage!\n", total_enemy_dmg);
                    new_enemy.hp -= total_player_dmg;
                    currenthp -= total_enemy_dmg;
                }
                else if(action[0] == '2')
                {
                    total_enemy_dmg = (total_enemy_dmg - myplayer->defense.level * 0.25) > 0 ? (total_enemy_dmg - myplayer->defense.level * 0.25) : 1;

                    if(total_enemy_dmg == 0 || total_enemy_dmg < 0)
                    {
                        printf("\n\n\nYou defended yourself!\nThe Enemy's attack had no effect!\n");
                        break;
                    }
                    else
                    {
                        printf("\n\n\nDespite holding your ground, the Enemy dealt %.0f damage!\n", total_enemy_dmg);
                        currenthp -= total_enemy_dmg;
                    }
                }
                else if(action[0] == '3')
                {
                    printf("\n\n\n------------------------------\n"
                    " You ran away from the Enemy!\n"
                    "------------------------------\n");
                    run_away = true;
                }
                break;
            case 1:
                //Enemy protect
                if(action[0] == '1')
                {
                    total_player_dmg = (total_player_dmg - new_enemy.defense * 0.25) > 0 ? (total_player_dmg - new_enemy.defense * 0.25) : 1;

                    if(total_player_dmg < 0)
                    {
                        total_player_dmg = 0;
                        printf("\n\n\nThe Enemy defended themselves!\n%s's attack had no effect!\n", myplayer->name);
                        break;
                    }
                    else if(total_player_dmg == 0)
                    {
                        printf("\n\n\nThe Enemy defended themselves!\n%s's attack had no effect!\n", myplayer->name);
                        break;
                    }
                    else
                    {
                        printf("\n\n\nThe Enemy defended themselves, but their defense wasn't enough!\n%s did %.0f damage!\n", myplayer->name, total_player_dmg);
                    }

                    new_enemy.hp -= total_player_dmg;
                }
                else if(action[0] == '2')
                {
                    printf("\n\n\nYour gaze meets the Enemy's, both of you waiting for the next move.\n");
                }
                else if(action[0] == '3')
                {
                    printf("\n\n\nYou ran away from the Enemy!\n");
                    run_away = true;
                    break;
                }
                break;
        }

        //Reset counters
        total_player_dmg = 0;
        total_enemy_dmg = 0;
        turn_counter++;
    }

    //Initialize experience gain
    int melee_exp_gain;
    int defense_exp_gain;
    int hp_exp_gain;

    if(turn_counter == 0)
    {
        melee_exp_gain = (int)round((new_enemy.melee * 0.40));
        defense_exp_gain = (int)round((new_enemy.defense * 0.40));
        hp_exp_gain = (int)round((new_enemy.hp * 0.30));
    }
    else
    {
        melee_exp_gain = (int)round((new_enemy.melee * 0.30) / turn_counter + 2);
        defense_exp_gain = (int)round((new_enemy.defense * 0.30) / turn_counter + 2);
        hp_exp_gain = (int)round((new_enemy.hp * 0.20) / turn_counter + 1);
    }

    //Print victory and experience gain
    if(new_enemy.hp == 0 || new_enemy.hp < 0)
    {
        printf("\n<=====================>\n  "
        "You are victorious!\n"
        "<=====================>\n"
        "  Experience Gained\n"
        "<=====================>\n"
        "| Health EXP: %i\n----------------------\n| "
        "Melee EXP: %i\n----------------------\n| "
        "Defense EXP: %i\n----------------------\n", hp_exp_gain, melee_exp_gain, defense_exp_gain);

        //Rolls enemy drop chance
        int drop = rand() % 3;
        if(drop == 0)
        {
            //Rolls type of drop
            int random_index = rand() % 3;
            //Allocates memory for item
            item *dropped_sword = malloc(sizeof(item));
            if(dropped_sword == NULL)
            {
                exit(1);
            }
            dropped_sword->class = WEAPON;
            dropped_sword->type = "Sword";

            if(random_index == 1)
            {
                dropped_sword->item_type.s = swords[0];
            }
            else if (random_index == 2)
            {
                dropped_sword->item_type.s = swords[1];
            }
            else
            {
                dropped_sword->item_type.s = swords[2];
            }

            char* name = sword_names(dropped_sword->item_type.s.type);

            printf("The Enemy dropped a %s Sword!\n", name);
            printf("Would you like to take the sword?\nYes/No:\n");
            char sword_answer[4];
            do
            {

                fgets(sword_answer, 4, stdin);
                char *newline = strchr(sword_answer, '\n');
                if(newline)
                {
                *newline = '\0';
                }

                if(strcasecmp(sword_answer, yes) == 0)
                {
                    printf("You got a %s Sword!\n", name);

                    add_to_inventory(dropped_sword, myplayer);
                }
                else if(strcasecmp(sword_answer, no) == 0)
                {
                    printf("You decided to not take the sword.\n");
                }
            }
            while(strcasecmp(sword_answer, yes) != 0 && strcasecmp(sword_answer, no) != 0);
        }

        myplayer->hp.exp += hp_exp_gain;
        myplayer->melee.exp += melee_exp_gain;
        myplayer->defense.exp += defense_exp_gain;

        int hp_exp_needed = 8 * pow(myplayer->hp.level, 1.5);
        int melee_exp_needed = 8 * pow(myplayer->melee.level, 1.5);
        int defense_exp_needed = 8 * pow(myplayer->defense.level, 1.5);

        if(myplayer->hp.exp >= hp_exp_needed)
        {
            level_up(&myplayer->hp, myplayer);
        }
        if(myplayer->melee.exp >= melee_exp_needed)
        {
            level_up(&myplayer->melee, myplayer);
        }
        if(myplayer->defense.exp >= defense_exp_needed)
        {
            level_up(&myplayer->defense, myplayer);
        }
    }
    //Print loss
    else if(currenthp == 0 || currenthp < 0)
    {
        printf("\n<=====================>\n  You were defeated. \n<=====================>\n");
        free(myplayer);
    }
}

//Level up from experience gain
void level_up(stat *stat_ptr, player *myplayer)
{
    stat_ptr->level++;

    printf("(||)====================================(||)\n"
    "       %s's %s Level is now %i!  \n"
    "(||)====================================(||)\n", myplayer->name, stat_ptr->name, stat_ptr->level);
}

//Add an item to the inventory
void add_to_inventory(item *item, player *myplayer)
{
    int add_counter = 0;

    for(int i = 0; i < MAX_ITEMS; i++)
    {
        if(myplayer->inv.items[i] == NULL)
        {
            myplayer->inv.items[i] = item;
            add_counter++;
            break;
        }
    }
    if(add_counter == 0)
    {
        printf("Your inventory is full! You can't carry any more items.");
    }
}

//Display inventory from main menu
void check_inventory(player *myplayer)
{
    printf("   <===========>\n"
    "     Inventory\n"
    "   <===========>\n");
    int counter = 0;
    if(myplayer == NULL)
    {
        printf("Error: playernot initialized\n");
        return;
    }
    else if (myplayer->inv.items == NULL)
    {
        printf("Error: inventory not initialized\n");
    }
    for(int i = 0; i < MAX_ITEMS; i++)
    {
        if(myplayer->inv.items[i] == NULL)
        {
            printf("====================\n");
            printf("Empty Inventory Slot\n");
        }
        else
        {
            if(myplayer->inv.items[i]->class == WEAPON)
            {
                char* name = sword_names(myplayer->inv.items[i]->item_type.s.type);
                printf("====================\n");
                printf("%i.%s Sword\n", counter + 1, name);
                counter++;
            }
            else
            {
                printf("%i.%s\n", counter + 1, myplayer->inv.items[i]->type);
                counter++;
            }
        }
    }
    printf("Would you like to drop an item?\n");

                char drop_answer[4];

                do
                {
                    fgets(drop_answer, 4, stdin);

                    char *newline = strchr(drop_answer, '\n');
                    if(newline)
                    {
                        *newline = '\0';
                    }

                    if(strcasecmp(drop_answer, yes) == 0)
                    {
                        drop_item(myplayer);
                    }
                }
                while(strcasecmp(drop_answer, no) != 0 && strcasecmp(drop_answer, yes) != 0);

    printf("====================\n"
    "Enter '1' to exit\n");

    char exit[4];
    do
    {
        fgets(exit, 4, stdin);

        char *newline = strchr(exit, '\n');
        if(newline)
        {
            *newline = '\0';
        }
    }
    while(strcasecmp(exit, "1") != 0);
}

//Converts enum values for swords into strings
char* sword_names(sword_type sword)
{
    if(sword == BRONZE)
    {
        return "Bronze";
    }
    else if(sword == IRON)
    {
        return "Iron";
    }
    else if(sword == STEEL)
    {
        return "Steel";
    }
    else
    {
        return "None";
    }
}

//Remove items from inventory and free the allocated space
void drop_item(player* myplayer)
{
    printf("Which item would you like to drop?\n");

    char item_del[4];

    do
    {
        fgets(item_del, 4, stdin);

        char *newline = strchr(item_del, '\n');
        if(newline)
        {
            *newline = '\0';
        }

        if(item_del[0] == '1')
        {
            if(myplayer->inv.items[0] != NULL)
            {
                free(myplayer->inv.items[0]);
                myplayer->inv.items[0] = NULL;
            }
        }
        else if(item_del[0] == '2')
        {
            if(myplayer->inv.items[1] != NULL)
            {
                free(myplayer->inv.items[1]);
                myplayer->inv.items[1] = NULL;
            }
        }
        else if(item_del[0] == '3')
        {
            if(myplayer->inv.items[2] != NULL)
            {
                free(myplayer->inv.items[2]);
                myplayer->inv.items[2] = NULL;
            }
        }
        else if(item_del[0] == '4')
        {
            if(myplayer->inv.items[3] != NULL)
            {
                free(myplayer->inv.items[3]);
                myplayer->inv.items[3] = NULL;
            }
        }
        else if(item_del[0] == '5')
        {
            if(myplayer->inv.items[5] != NULL)
            {
                free(myplayer->inv.items[5]);
                myplayer->inv.items[5] = NULL;
            }
        }
    }
    while(item_del[0] == '1' && item_del[0] == '2' && item_del[0] == '3' && item_del[0] == '4' && item_del[0] == '5');
}
