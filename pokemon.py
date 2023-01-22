"""
Lon Pierson and Roland Waterson
4/16/2022
'Pokemon Classification' DS2500 Project 2
Laney Strange
"""

import random

class Pokemon():
    
    def __init__(self, name, types, hp, a, d, sa, sd, sp, move_list, move_dict):
        """
        Creates a Pokemon object. Input stats are base stats, actual object stats
        are predicted stats at level 100.

        Parameters
        ----------
        name : str
            Name of Pokemon.
        types : str
            Str representation of Pokemon's types.
        hp : int
            Health.
        a : int
            Attack.
        d : int
            Defense.
        sa : int
            Special Attack.
        sd : int
            Special Defense.
        sp : int
            Speed.
        move_list : str
            Str representation of all possible moves pokemon can do.
        move_dict : dict
            Dictionary mapping the str name of a move to a Move object.

        """
        # Trivial values, basic stats are scaled to approximately level 100
        self.name = name
        self.health = int(2 * hp + (10 * hp) ** 0.5 + 140)
        self.attack = int(2 * a + (10 * a) ** 0.5 + 40 )
        self.defense = int(2 * d + (10 * d) ** 0.5 + 40)
        self.sp_attack = int(2 * sa + (10 * sa) ** 0.5 + 40)
        self.sp_defense = int(2 * sd + (10 * sd) ** 0.5 + 40)
        self.speed = int(2 * sp + (10 * sp) ** 0.5 + 40)
        
        # Had to get a little creative with how I stored the types and move_list
        # Because the file contained both , and ;, I had to use splitting to turn
        # The string back into a list, and the clean up the values.
        self.types = types.split(", ")
        for i in range(len(self.types)):
            self.types[i] = self.types[i].replace("\'", "")
            self.types[i] = self.types[i].replace("[", "")
            self.types[i] = self.types[i].replace("]", "")
        
        self.move_list = move_list.split(", ")
        self.move_list[0] = self.move_list[0][1:]
        self.move_list[-1] = self.move_list[-1][:-1]
        for i in range(len(self.move_list)):
            self.move_list[i] = self.move_list[i][1:-1]
            self.move_list[i] = self.move_list[i].replace("\'", "-")
            self.move_list[i] = self.move_list[i].replace("-s", "\'s")
            
        # Finds the top 4 moves a Pokemon can use
        self.find_best_moves(move_dict)
                
        
        
    def find_best_moves(self, move_dict):
        """
        Chooses the 4 moves the Pokemon can use in the tournament. The function 
        makes sure that the Pokemon (1) Has at least one special and one physical
        move, (2) Has at least one move that is a different type from the others
        and (3) Chooses the most powerful moves under the previous constraints

        Parameters
        ----------
        move_dict : dict
            Dictionary mapping str name of the move to equivalent Move object.

        Note: This doesn't actually remove the status moves, as a Pokemon can
        use these moves if they have less than 4 moves. However, there are very
        few Pokemon that fit this, such as Ditto. 

        """
        
        # Sorts the moves from greatest to least power and deletes duplicate moves
        top_moves = []
        for attack in self.move_list:
            top_moves.append(move_dict[attack])
        top_moves = list(set(top_moves))
        top_moves.sort(reverse=True)
        
        # Returns as many moves possible if less than 4
        if len(top_moves) < 4:
            self.top_moves = top_moves
        
        # Fulfills conditions (1) and (2)
        else:
            varied_top_moves = [0, 0, 0, 0]
            varied_top_moves_types = [0, 0, 0, 0]
            varied_top_moves_norspe = [0, 0, 0, 0]
            
            # Chooses top 4 initial moves
            for i in range(4):
                popped_move = top_moves.pop(0)
                varied_top_moves[i] = popped_move
                varied_top_moves_types[i] = popped_move.move_type
                varied_top_moves_norspe[i] = popped_move.category
            
            # Picks a new move if one of the conditions isn't fulfilled
            while len(list(set(varied_top_moves_types))) == 1 and len(list(set(varied_top_moves_norspe))) == 1:
                popped_move = top_moves.pop(0)
                varied_top_moves[-1] = popped_move
                varied_top_moves_types[-1] = popped_move.move_type
                varied_top_moves_norspe[-1] = popped_move.category
            self.top_moves = varied_top_moves
            

    def __str__(self):
        # 2nd return intended for more verbose descriptions of Pokemon 
        return (self.name)
    
        return (self.name + " is a " + str(self.types) + " Pokemon with stats " + \
                str(self.health) + "/" + str(self.attack) + "/" + str(self.defense) + \
                "/" + str(self.sp_attack) + "/" + str(self.sp_defense) + " with moves " + \
                str(self.top_moves)) 
    
    
    def pick_random_move(self):
        """
        Picks a random move from a Pokemon's top moves.

        Returns
        -------
        Move
            Intended move.

        """
        return self.top_moves[random.randint(0, len(self.top_moves) - 1)]
            
    def pick_smart_move(self, damage_fun, defender, type_dict):
        """
        Chooses the move that will do the most damage to a specific opponenet
        without random damage modifiers

        Parameters
        ----------
        damage_fun : fun
            Name of the function that calculates damage.
        defender : Pokemon
            Opponent Pokemon.
        type_dict : dict
            Dictionary with damage multipliers based on pokemon types.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        
        max_damage = 0
        damage_index = 0
        for i in range(len(self.top_moves)):
            if damage_fun(self.top_moves[i], self, defender, type_dict) > max_damage:
                max_damage = damage_fun(self.top_moves[i], self, defender, type_dict, False)
                damage_index = i
        return self.top_moves[damage_index]
            
    
    def __hash__(self):
        return hash(self.name) + hash(self.attack) + hash(self.defense) + hash(self.sp_attack) + hash(self.sp_defense) + hash(self.speed)
    
    
    
    
    
    
    
    # def pick_type_move(self, opponent, type_dict):
    #     # Picks a move from the top 4 moves
    #     temp_top_moves = self.top_moves
    #     for move in temp_top_moves:
    #         if len(temp_top_moves) == 1:
    #             return move
    #         for types in opponent.types:
    #             if type_dict[move.move_type][types] > 1:
    #                 return move
    #             elif type_dict[move.move_type][types] < 1:
    #                  temp_top_moves.remove(move)
    #                  return temp_top_moves[random.randint(0, len(self.top_moves) - 1)]
    #             else:
    #                 return self.top_moves[random.randint(0, len(self.top_moves) - 1)]
            