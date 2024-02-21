#ifndef structs
#define structs

#define NAME_MAX 10

typedef struct
{
    char* name;
    int heal;
} potion;

typedef struct
{
    char* name;
    int damage;
} weapon;

typedef struct
{
    char* type;
} ore;

typedef enum
{
    EMPTY,
    POTION,
    WEAPON,
    ORE
} ItemType;

typedef struct
{
    ItemType type;
    union
    {
        potion Potion;
        weapon Weapon;
        ore Ore;
    };
} item;

typedef struct
{
    item items[5];
}inventory;

typedef struct
{
    char name[NAME_MAX];
    int level;
    int exp;
} stat;

typedef struct
{
    item weapon_item;
    char name[NAME_MAX];
    stat hp;
    stat melee;
    stat defense;
    stat mining;
    int combat;
    int kills;
    int deaths;
    float kd;
    inventory inv;
} player;

typedef struct
{
    char name;
    stat hp;
    stat melee;
    stat defense;
    int combat;
} enemy;

#endif
