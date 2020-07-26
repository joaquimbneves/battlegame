from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell("fire", 25, 600, 'black')
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")


# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1300, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Superpotion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores a player HP/MP", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores all players HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5 }, { "item": hielixer, "quantity": 5}, {"item": grenade, "quantity": 5}]

# Instantiate people
player1 = Person("Valos: ", 3260, 132, 400, 34, player_spells, player_items)
player2 = Person("Nick:  ", 4160, 188, 360, 34, player_spells, player_items)
player3 = Person("Robot: ", 3089, 174, 435, 34, player_spells, player_items)

players = [player1,player2, player3]

enemy1 = Person("Imp:  ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus:", 11200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp:  ", 1250, 130, 560, 325, enemy_spells, [])

enemies = [enemy1,enemy2,enemy3]
running = True

i = 0

print(bcolors.FAIL + bcolors.BOLD + "An enemy appears \n" + bcolors.ENDC)

while running:
    print('=====================================================================')

    print("Name:       HP:                                    MP:")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.enemy_get_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name + "for ", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = player.magic[magic_choice].generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYou don't have enough MP.\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for:" + str(magic_dmg) + "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player_items[item_choice]["item"]

            if player_items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for" + str(item.prop) + "HP" + bcolors.ENDC)

            elif item.type == "elixer":

                if item.type == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores your HP and MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died")
                    del enemies[enemy]


    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies +=1

    for player in players:
        if player.get_hp() == 0:
            defeated_players +=1

    # Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win" + "\n=====================================================" + bcolors.ENDC)
        running = False

    # Check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "You've been defeated. Enemies have won" + bcolors.ENDC)
        running = False

    # Enemy attack fase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        #Chose attack
        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name, " attacks" + players[target].name + ":", enemy_dmg, "hp lost.")

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals " + enemy.name + " for:" + str(magic_dmg) + "HP" + bcolors.ENDC)
            elif spell.type == "black":

                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name + "'s " + spell.name + " deals", str(magic_dmg), "points of damage to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died")
                    del players[target]
            #print("Enemy chose", spell, "Damage taken is", magic_dmg)


