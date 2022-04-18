

from os import stat
from pickle import TRUE

from urllib3 import Retry
from core.player import Color
from fanorona.fanorona_player import FanoronaPlayer
from fanorona.fanorona_rules import FanoronaRules
from copy import deepcopy
import random


class AI(FanoronaPlayer):

    name = "OptiV2"

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value

    def play(self, state, remain_time):
        print("")
        print(f"Player {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        return minimax_search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """
    def successors(self, state):
        all_good_moves=  list()
        all_bad_moves = list()

        #print("\nCurrent score : "+str(state.score[self.position]))

        possible_actions = FanoronaRules.get_player_actions(state, self.color.value)
        for action in possible_actions:
            copy_of_state = deepcopy(state)
            result = FanoronaRules.act(copy_of_state, action, self.color.value)
            if (copy_of_state.score[self.position]>state.score[self.position] and not isinstance(result, bool) ):
                better_action = tuple((action, copy_of_state))
                all_good_moves.append(better_action)
            else:
                bad_action = tuple((action, copy_of_state))
                all_bad_moves.append(bad_action)

        if all_good_moves :
            #sort by descending score
            all_good_moves.sort(key=lambda x: x[1].score[self.position], reverse=True)
            #check if the first score is equal to the last of the list
            if(all_good_moves[0][1].score[self.position]== all_good_moves[-1][1].score[self.position]):
                #if so, it means the list is fill with moves of same scores
                #randomize to avoid looping
                random.shuffle(all_good_moves)
                #print("list randomized")
            """
            for element in all_good_moves:
                print(element)
                new_state = element[1]
                print("score : "+str(new_state.score[self.position]))
            """
            return all_good_moves
        else:
            """
            for element in all_bad_moves:
                print(element)
                new_state = element[1]
                print("score : "+str(new_state.score[self.position]))"""
            random.shuffle(all_bad_moves)
            return all_bad_moves
               


    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """
    def cutoff(self, state, depth):

        depth_max_first = 6
        depth_max_second = 7
        
        #advantage if player makes the first move
        if(self.position ==-1):
            if(depth ==depth_max_first or FanoronaRules.is_end_game(state)):
                return True
            else:
                return False
        else:
        
            if(depth ==depth_max_second or FanoronaRules.is_end_game(state)):
                return True
            else: 
                return False
    """
    The evaluate function must return an integer value
    representing the utility function of the board.
    """
    def evaluate(self, state):
        adversaire = state.get_next_player()

        all_good_moves=  list()

        #print("\nCurrent score : "+str(state.score[self.position]))

        possible_actions = FanoronaRules.get_player_actions(state, adversaire)
        for action in possible_actions:
            copy_of_state = deepcopy(state)
            result = FanoronaRules.act(copy_of_state, action, adversaire)

            if (copy_of_state.score[adversaire]>state.score[adversaire] and not isinstance(result, bool) ):
                better_action = copy_of_state.score[adversaire]-state.score[adversaire] 
                all_good_moves.append(better_action)
            
            else:
                if(self.position == -1):
                    return (state.score[-1] - state.score[1])
                else:
                    return (state.score[1] - state.score[-1])

        coef =0
        all_occ = [None] * (len(all_good_moves))
        #print("len :",len(all_good_moves))
        for i in range(len(all_good_moves)):
            #print("o")
            all_occ[i] = all_good_moves.count(i)
            coef = coef + ((all_occ[i]/len(all_good_moves))*i)
            """        
            for element in all_occ:
            print(element)"""
        
        #print(coef)
        
        if(self.position == -1):
            
            result = state.score[-1] - state.score[1] -coef
            print(result)
            return (result)
        else:
            result = state.score[1] - state.score[-1] -coef
            print(result)
            return (result)




"""
MiniMax and AlphaBeta algorithms.
Adapted from:
    Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
    Copyright (C) 2014, Universite catholique de Louvain
    GNU General Public License <http://www.gnu.org/licenses/>
"""

inf = float("inf")

def minimax_search(state, player, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    player -- a concrete instance of class AI implementing an Alpha-Beta player
    prune -- whether to use AlphaBeta pruning

    """
    def max_value(state, alpha, beta, depth):
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = -inf
        action = None
        for a, s in player.successors(state):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = max_value(s, alpha, beta, depth + 1)
            else:                                             # next turn is for the other one
                v, _ = min_value(s, alpha, beta, depth + 1)
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        return val, action

    def min_value(state, alpha, beta, depth):
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = inf
        action = None
        for a, s in player.successors(state):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = min_value(s, alpha, beta, depth + 1)
            else:                                             # next turn is for the other one
                v, _ = max_value(s, alpha, beta, depth + 1)
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action

    _, action = max_value(state, -inf, inf, 0)
    return action