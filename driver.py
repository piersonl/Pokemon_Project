"""
Lon Pierson and Roland Waterson
4/16/2022
'Pokemon Tournament' DS2500 Project 2
Laney Strange
"""

# Imports modules
import pandas as pd
import random
from pokemon import Pokemon
from move import Move
import matplotlib.pyplot as plt
import seaborn as sb
from scipy import stats

# File names and Monte Carlo numbers
MOVE_FILE = "move-data.csv"
POKEMON_FILE = "pokemon-data.csv"
TRIALS = 1000
EXPERIMENTS = 100
GRAPH_THRESHOLD = 3
POKEMON_TEST_INDEX = 345

# Dictionary for type weakness modifiers. To access the damage modifier, 
# do TYPE_DAMAGE[move type][opposing pokemon type]. If the opposing pokemon
# has multiple types, multiply the damage modifiers
TYPE_DAMAGE = {"Normal": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0, "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 1},
               "Fire": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 1, "Ice": 2, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1, "Dragon": 0.5, "Dark": 1, "Steel": 2, "Fairy": 1},
               "Water": {"Normal": 1, "Fire": 2, "Water": 0.5, "Grass": 0.5, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 2, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1, "Dragon": 0.5, "Dark": 1, "Steel": 1, "Fairy": 1},
               "Grass": {"Normal": 1, "Fire": 0.5, "Water": 2, "Grass": 0.5, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1, "Dragon": 0.5, "Dark": 1, "Steel": 0.5, "Fairy": 1},
               "Electric": {"Normal": 1, "Fire": 1, "Water": 2, "Grass": 0.5, "Electric": 0.5, "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 0, "Flying": 2, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 0.5, "Dark": 1, "Steel": 1, "Fairy": 1},
               "Ice": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 2, "Electric": 1, "Ice": 0.5, "Fighting": 1, "Poison": 1, "Ground": 2, "Flying": 2, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 1, "Steel": 0.5, "Fairy": 1},
               "Fighting": {"Normal": 2, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 2, "Fighting": 1, "Poison": 0.5, "Ground": 1, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dragon": 1, "Dark": 2, "Steel": 2, "Fairy": 0.5},
               "Poison": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 2, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 0.5, "Ground": 0.5, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 0.5, "Ghost": 0.5, "Dragon": 1, "Dark": 1, "Steel": 0, "Fairy": 2},
               "Ground": {"Normal": 1, "Fire": 2, "Water": 1, "Grass": 0.5, "Electric": 2, "Ice": 1, "Fighting": 1, "Poison": 2, "Ground": 1, "Flying": 0, "Psychic": 1, "Bug": 0.5, "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 2, "Fairy": 1},
               "Flying": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 2, "Electric": 0.5, "Ice": 1, "Fighting": 2, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 2, "Rock": 0.5, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 1},
               "Psychic": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 2, "Poison": 2, "Ground": 1, "Flying": 1, "Psychic": 0.5, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 0, "Steel": 0.5, "Fairy": 1},
               "Bug": {"Normal": 1, "Fire": 0.5, "Water": 1, "Grass": 2, "Electric": 1, "Ice": 1, "Fighting": 0.5, "Poison": 0.5, "Ground": 1, "Flying": 0.5, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 0.5, "Dragon": 1, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
               "Rock": {"Normal": 1, "Fire": 2, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 2, "Fighting": 0.5, "Poison": 1, "Ground": 0.5, "Flying": 2, "Psychic": 1, "Bug": 2, "Rock": 1, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 1},
               "Ghost": {"Normal": 0, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 0.5, "Steel": 1, "Fairy": 1},
               "Dragon": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 1, "Steel": 0.5, "Fairy": 0},
               "Dark": {"Normal": 1, "Fire": 1, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 0.5, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 2, "Bug": 1, "Rock": 1, "Ghost": 2, "Dragon": 1, "Dark": 0.5, "Steel": 1, "Fairy": 0.5},
               "Steel": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Grass": 1, "Electric": 0.5, "Ice": 2, "Fighting": 1, "Poison": 1, "Ground": 1, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 2, "Ghost": 1, "Dragon": 1, "Dark": 1, "Steel": 0.5, "Fairy": 2},
               "Fairy": {"Normal": 1, "Fire": 0.5, "Water": 1, "Grass": 1, "Electric": 1, "Ice": 1, "Fighting": 2, "Poison": 1, "Ground": 0.5, "Flying": 1, "Psychic": 1, "Bug": 1, "Rock": 1, "Ghost": 1, "Dragon": 2, "Dark": 2, "Steel": 0.5, "Fairy": 1}}


def calc_damage(attack, attacker, defender, type_dict, use_random=True):
    '''
    Parameters
    ----------
    attack : Move
        The move being used by the attacker.
    attacker : Pokemon
        The pokemon attacking.
    defender : Pokemon
        The Pokemon defending against the attack
    type_dict : Dictionary
        The dictionary of type match up values.
    use_random : Boolean, optional
        Tells the calc_damage if it should
        use the random damage aspect of the 
        damage formula. The default is True.

    Returns
    -------
    damage : Int
        The number of Damage done to the the defending Pokemon.

    '''
    # Will make better documentation later
    # This calculates damage given the move, the attacking pokemon, the defending pokemon, and the weakness dictionary
    
    # create if and else statement for if the move being used is 
    # physical or special so we can get the correct value
    # from each Pokemon
    if attack.category == "Physical":
        a = attacker.attack
        d = defender.defense
    else:
        a = attacker.sp_attack
        d = defender.sp_defense
        
    # set random damage to 1 in case we dont wanna use the random
    # damage calculator
    random_damage = 1
    
    # fine the random damage value
    if use_random:
        random_damage = random.randint(85, 100) / 100
        
    # set the STAB (same type attack bonus) to 1 and change to 
    # 1.5 if the type of the attack is one of the users types
    stab = 1
    if attack.move_type in attacker.types:
        stab = 1.5
            
    # set type effectiveness to one then check the type dict to see
    # if there are any weaknesses and adjust the effectivness multipler
    type_effectiveness = 1
    for defender_type in defender.types:
        type_effectiveness *= type_dict[attack.move_type][defender_type]
            
    # compute the amount of damage done using the damage formula
    damage = int(((0.84 * attack.power * a / d) + 2) * type_effectiveness * random_damage * stab) 
    
    return damage


def battle(pokemon1, pokemon2):
    '''
    Parameters
    ----------
    pokemon1 : Pokemon
        One of the pokemon participating in the battle.
    pokemon2 : Pokemon
        The other pokemon participating in the battle.
        
    Returns
    -------
    Winner : Pokemon
        The Pokemon that won the battle.
    '''
    # set the Pokemon's health to a dummy variable so we can
    # simulate battles without actual changing their health stat
    poke1_hp = pokemon1.health
    poke2_hp = pokemon2.health
    
    # create a counter for the number of turns taken
    num_moves = 0
    
    # create while loop to to make sure it only runs if both pokemon
    # are not fainted (have positive health)
    while poke1_hp > 0 and poke2_hp > 0:
        
        # create if statement to account for the different speeds
        # one where pokemon1 is faster and one where pokemon2 is 
        # faster (also if they're the same just have pokemon1 go first)
        if pokemon1.speed >= pokemon2.speed:
            
            # pick a move and calculate the damage it will do the opponent
            damage = calc_damage(pokemon1.pick_smart_move(calc_damage, pokemon2, TYPE_DAMAGE), pokemon1, pokemon2, TYPE_DAMAGE)
            
            # subtract that damage from the health
            poke2_hp = poke2_hp - damage
            
            # if the opposing pokemon is fainted, return pokemon1 as winner
            if poke2_hp <= 0:
                return pokemon1
            
            # if the opposing pokemon is unfainted, have them pick a move
            # and calculatet the damage
            damage = calc_damage(pokemon2.pick_smart_move(calc_damage, pokemon1, TYPE_DAMAGE), pokemon2, pokemon1, TYPE_DAMAGE)
            
            # subtract that damage from the health
            poke1_hp = poke1_hp - damage
            
            # if the opposing pokemon is fainted, return pokemon2
            if poke1_hp <= 0:
                return pokemon2
            
            # add one to the number of turns counter
            num_moves += 1
            
        # the exact same as the previous section (lines 132-147)
        # only difference is pokemn2 moves first this time 
        if pokemon2.speed > pokemon1.speed:
            damage = calc_damage(pokemon2.pick_smart_move(calc_damage, pokemon1, TYPE_DAMAGE), pokemon2, pokemon1, TYPE_DAMAGE)
            poke1_hp = poke1_hp - damage
            if poke1_hp <= 0:
                return pokemon2
            damage = calc_damage(pokemon1.pick_smart_move(calc_damage, pokemon2, TYPE_DAMAGE), pokemon1, pokemon2, TYPE_DAMAGE)
            poke2_hp = poke2_hp - damage
            if poke2_hp <= 0:
                return pokemon1
            num_moves += 1
            
        # a saftey net in case somehow there ends up being a matchup
        # where the 2 pokemon can't hurt eachother, super uncommon but
        # was an issue I was running into so this just automatically
        # declares pokemon1 as the winner in that case
        if num_moves > 25:
            return pokemon1
    
def strat_battle(pokemon1, pokemon2):
    '''
     
    The only difference between this function and the normal
    battle function is that pokemon2 in this case randomly
    chooses a move instead of picking a move based on which
    will do the most damage. We need this function so we can
    compare how much using a basic strategy of considering
    stab moves and type effectivness affects your chances of 
    winning.
    
    (All comments from battle function also apply here)

    Parameters
    ----------
    pokemon1 : Pokemon
        One of the pokemon participating in the battle.
    pokemon2 : Pokemon
        The other pokemon participating in the battle.
        
    Returns
    -------
    Winner : Pokemon
        The Pokemon that won the battle.
    
    '''
    poke1_hp = pokemon1.health
    poke2_hp = pokemon2.health
    num_moves = 0
    while poke1_hp > 0 and poke2_hp > 0:
        if pokemon1.speed >= pokemon2.speed:
            damage = calc_damage(pokemon1.pick_smart_move(calc_damage, pokemon2, TYPE_DAMAGE), pokemon1, pokemon2, TYPE_DAMAGE)
            poke2_hp = poke2_hp - damage
            if poke2_hp <= 0:
                return pokemon1
            damage = calc_damage(pokemon2.pick_random_move(), pokemon2, pokemon1, TYPE_DAMAGE)
            poke1_hp = poke1_hp - damage
            if poke1_hp <= 0:
                return pokemon2
            num_moves += 1
        if pokemon2.speed > pokemon1.speed:
            damage = calc_damage(pokemon2.pick_random_move(), pokemon2, pokemon1, TYPE_DAMAGE)
            poke1_hp = poke1_hp - damage
            if poke1_hp <= 0:
                return pokemon2
            damage = calc_damage(pokemon1.pick_smart_move(calc_damage, pokemon2, TYPE_DAMAGE), pokemon1, pokemon2, TYPE_DAMAGE)
            poke2_hp = poke2_hp - damage
            if poke2_hp <= 0:
                return pokemon1
            num_moves += 1
        if num_moves > 25:
            return pokemon1
        
        
        
def tournament(pokemon_lst):
    '''
        Parameters
    ----------
    pokemon1 : List
        The list of all the pokemon.
        
    Returns
    -------
    Winner : Pokemon
        The Pokemon that won the tournament.
    
    '''
    # shuffle the pokemon list to make sure each tournament has
    # unique match-ups
    random.shuffle(pokemon_lst)
    
    # create an empty list to add all the winners to
    winner_lst = []       
    
    # read through the pokemon list in increments of two
    for i  in pokemon_lst[1::2]:
        
        # create if statment for if there's an odd number
        # of pokemon telling it to add the last pokemon to the
        # winner list and end this round of the tournament
        if pokemon_lst.index(i) == (len(pokemon_lst) - 1):
            winner_lst.append(i)
            break
        
        # battle the 2 pokemon next to eachother in the list
        # and add the winner to the winner list
        winner = battle(i, pokemon_lst[pokemon_lst.index(i) + 1])
        winner_lst.append(winner)
        
    # create while loop for when the winner list is greater than
    # one so that it will run until there's only 1 winner
    while len(winner_lst) > 1:
        
        # create a temporary winner list
        temp_lst = []
        
        # read throught the winner list in increments of 2
        for i in winner_lst[1::2]:
            
            # if theres an odd number of pokemon dont have 
            # a battle and just add the last pokemon to the 
            # winner list and continue
            if winner_lst.index(i) == (len(winner_lst) - 1):
                temp_lst.append(i)
                continue
            
            # find the winner of each battle and add it to the temporary
            # winner list
            winner = battle(i, winner_lst[winner_lst.index(i) + 1])
            temp_lst.append(winner)
            
        # set the winner list equal to the temporary winner
        # list so the while loop will continue
        winner_lst = temp_lst
        
    # once the while loop is finished and the winner list has
    # length one, return that pokemon as the winner of the tournament
    return winner_lst[0]
    


def winning_prob(trials, pokemon, pokemon_lst, strat=True):
    '''
    Parameters
    ----------
    trials : Integer
        Number of battles to simulate.
    pokemon : Pokemon
        The Pokemon being put into the simulations.
    pokemon_lst : List
        The full list of Pokemon.
    strat : Boolean
        Tells it if we want both the pokemon being used as the
        control and the opponents if they should use strategy or
        if just the control pokemon should use strategy.

    Returns
    -------
    wins : Integer
        The number of wins the control pokemon had out of
        the number of simulated battles.

    '''
    # set your number of wins to zero
    wins = 0
    
    # create if statement for if you want both pokemon to be using
    # strategy
    if strat:
        
        # create for loop for the number of trials to simulate
        # that many number of battles 
        for i in range(trials):
            winner = battle(pokemon, pokemon_lst[random.randint(0, len(pokemon_lst) -1)])
            
            # if the winner is the control pokemon then add one to its
            # win count
            if winner == pokemon:
                wins += 1
                
    # create if statement for if you want to see how times your pokemon
    # wins given the other pokemon is not using a strategy
    # (otherwise exactly the same as previous section so previous comments
    # still apply)
    if not strat:
        for i in range(trials):
            winner = strat_battle(pokemon, pokemon_lst[random.randint(0, len(pokemon_lst) -1)])
            if winner == pokemon:
                wins += 1
    return wins


def lin_plot(info):
    """
    Creates a linear regression plot of a Pokemon's stat against Pokemon's wins

    Parameters
    ----------
    info : str
        User input choice.
    """
    stat_dict = {"3": "Health", "4": "Attack", "5": "Defense", \
                 "6": "Special Attack", "7": "Special Defense", "8": "Speed"}
    
    # Runs simulation and notes Pokemons and number of tournaments won
    wins = {}
    for i in range(TRIALS):
        winner = tournament(pokemon_list)
        if winner not in wins:
            wins[winner] = 0
        wins[winner] += 1
    poke_value = []
    num_wins = []
    
    # Records given stat of Pokemon with more wins than GRAPH_THRESHOLD
    for value in wins:
        if wins[value] > GRAPH_THRESHOLD:
            if info == "3":
                poke_value.append(value.health)
            elif info == "4":
                poke_value.append(value.attack)
            elif info == "5":
                poke_value.append(value.defense)
            elif info == "6":
                poke_value.append(value.sp_attack)
            elif info == "7":
                poke_value.append(value.sp_defense)
            elif info == "8":
                poke_value.append(value.speed)
            else:
                return None
            
            num_wins.append(wins[value])
        
    # Plots the linear regression plot and prints equation of line of best fit
    p = sb.regplot(x=poke_value, y=num_wins)
    p.set_xlabel(stat_dict[info])
    p.set_ylabel("Wins")
    plt.title("Correlation between  Pokemon " + stat_dict[info] + " stat and winning")
        
    slope, intercept, r, p, se = stats.linregress(poke_value, num_wins)
    print("Wins = " + str(intercept) + " + " + str(slope) + " * " + stat_dict[info])
    print("Correlation: " + str(r))
    


if __name__ == "__main__":
    # reads files, removes Pokemon with special special stuff at the end. Too lazy to comb through
    # each one, so for now I just removed pokemon with a hyphen.
    mdf = pd.read_csv(MOVE_FILE, delimiter=",")
    
    pdf = pd.read_csv(POKEMON_FILE, delimiter=";")
    pdf = pdf[pdf["Name"].str.contains("-") == False]
    
    # IMPORTANT: this is where the moves and pokemons are stored
    move_dict = {}
    pokemon_list = []
    
    # Creates moves and pokemon objects
    for index, row in mdf.iterrows():
        new_move = Move(row[1], row[2], row[3], row[6])
        move_dict[row[1]] = new_move
    
    for index, row in pdf.iterrows():
        new_pokemon = Pokemon(row[0], row[1], row[4], row[5], row[6], row[7], row[8], row[9], row[11], move_dict)
        pokemon_list.append(new_pokemon)
        new_lst = []
        
    for i in range(50):
        new_lst.append(pokemon_list[i])
        
    # as the user if they wanna see information on how strategy affects battles
    # or if they wanna see on average which types are more succesful than others
    info = input("Input choice.\n1: Strategy histogram.\n2: Pokemon type bar chart." \
                 "\n3. Health lin reg.\n4. Attack lin reg.\n5. Defense lin reg." \
                 "\n6. Special Attack lin reg.\n7. Special Defense lin reg.\n8. Speed lin reg." \
                 "\nChoice: ")
    
    # Demos choosing random moves and random pokemon and generating how much damage one does
    # test1 = pokemon_list[random.randint(0, len(pokemon_list) - 1)]
    # test2 = pokemon_list[random.randint(0, len(pokemon_list) - 1)]
    # test_move = test1.pick_smart_move(calc_damage, test2, TYPE_DAMAGE)
    # print(battle(test1, test2))
    # print(test1, "attacks", test2, "using", test_move)
    # print(calc_damage(test_move, test1, test2, TYPE_DAMAGE), "damage is dealt!")
    
    # create if statement for if they want to see information
    # on how strategy changes battle outcomes
    if info == "1":
        
        # create empty lists for the number of wins given they both
        # use equal strategy (No strategy) and for when only your pokemon
        # uses strategy (Strategy is used)
        prob_wins = []
        strat_wins = []
        
        # create for loop for the number of experiments we want to perform
        for n in range(EXPERIMENTS):
            
            # find the number of wins for if they both use strategy (no strategy)
            num_of_wins = winning_prob(TRIALS, pokemon_list[POKEMON_TEST_INDEX], pokemon_list)
            
            # add it to the wins list for no strategy 
            prob_wins.append(num_of_wins)
            
            # find the number of wins for if only you pokemon uses strategy
            strat_wins_num = winning_prob(TRIALS, pokemon_list[POKEMON_TEST_INDEX], pokemon_list, strat=False)
            
            # add to the strategy wins list
            strat_wins.append(strat_wins_num)
    
        # graph the two lists as histograms
        sb.histplot(strat_wins, color="blue", alpha = .5)
        sb.histplot(prob_wins, color="red", alpha = .5)
        
        # add legend and titles
        plt.legend(["Blue = Strategy", "Red = No Strategy"])
        plt.title("How using basic strategy affects " + str(pokemon_list[POKEMON_TEST_INDEX]) + " average wins")
        plt.xlabel("Average Number of Wins")
        plt.ylabel("Number of Experiments")
        
    # create if statement for if they want to see information
    # on which pokemon types tend to be better at battling 
    if info == "2":
        
        # create an empty dictionary for the different types
        winning_types = {}
        
        # create for loop that simulates "trial" number
        # of tournaments
        for i in range(TRIALS):
            
            # simulate a tournament and find save the winner
            winner = tournament(pokemon_list)
            
            # create a for loop to read through all
            # the types of the pokemon
            for types in winner.types:
                
                # if the type isn't yet in the winning types
                # dictionary, add it with value of 1
                if types not in winning_types:
                    winning_types[types] = 1
                    
                # if the type is in the winning types
                # dictionary, add value 1 to it
                if types in winning_types:
                    winning_types[types] += 1
                    
        # sort the dictionary in ascending order
        sorted_dict = {k: v for k, v in sorted(winning_types.items(), key=lambda item: item[-1])}
        
        # create bar graph with each bar representing a type of Pokemon
        # and its number of tournament wins
        plt.bar(list(sorted_dict.keys()), list(sorted_dict.values()), color = "red")
        plt.xticks(rotation = 85)
        
        # add titles and labels
        plt.title("Average Number of Wins for each Type")
        plt.xlabel("Pokemon Types")
        plt.ylabel("Number of Tournament wins")
    
    else:
        lin_plot(info)