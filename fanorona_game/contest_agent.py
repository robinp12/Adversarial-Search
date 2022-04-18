

from os import stat

from sqlalchemy import false
from core.player import Color
from fanorona.fanorona_player import FanoronaPlayer
from fanorona.fanorona_rules import FanoronaRules
from copy import deepcopy


class AI(FanoronaPlayer):

    name = "Group 14"

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value

    def play(self, state, remain_time):
        print("")
        print(f"Player {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        return iterative_deepening (state, self)

def iterative_deepening(state, player):

    def is_cutoff(state, depth):
        if(FanoronaRules.is_end_game(state)):
            return True
        else: 
            return False

    def search_at_depth(depth):
        return 0

    #beginning of the iterative deepening fct    
    for depth in range(8):
        move = search_at_depth(depth, state)
        if move != is_cutoff(state, depth):
            return move