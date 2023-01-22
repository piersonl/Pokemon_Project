"""
Lon Pierson and Roland Waterson
4/16/2022
'Move Classification' DS2500 Project 2
Laney Strange
"""
import random

class Move():
    
    def __init__(self, name, move_type, category, power):
        '''
        Parameters
        ----------
        name : String
            The name of the move.
        move_type : String
            the type of the move.
        category : String
            whether the move is physical or special.
        power : Integer
            The power value of the move.

        '''
        
        self.name = name
        self.move_type = move_type
        self.category = category
        if power == "None":
            self.power = 0
        else: 
            self.power = int(power)
        
    def __hash__(self):
        return hash(self.name) + hash(self.move_type) + hash(self.category) + hash(self.power)
    
    def __gt__(self, other):
        return int(self.power) > int(other.power)
    
    def __lt__(self, other):
        return int(self.power) < int(other.power)
    
    def __str__(self):
        return (self.name + " (" + self.move_type + " " + self.category + \
                " move with " + str(self.power) + " power)")
            
    def __repr__(self):
        return self.__str__()
    
    
        
    
    
            