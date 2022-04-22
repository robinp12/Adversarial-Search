

import imp
from os import stat
from pickle import TRUE

from numpy import piecewise
from core.player import Color
from fanorona.fanorona_player import FanoronaPlayer
from fanorona.fanorona_rules import FanoronaRules
from copy import deepcopy
import random


class AI(FanoronaPlayer):

    name = "OptiV3"

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
                better_action = tuple((action, copy_of_state))
                all_bad_moves.append(better_action)
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
        depth_max_beginner= 4
        depth_max_second = 4
        #advantage if player makes the first move
        if(self.position ==-1):
            if(depth ==depth_max_beginner or FanoronaRules.is_end_game(state)):
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
        
        player = self.color.value
        adv = self.color.value * (-1)
        center_cells = [(2,2),(2,3),(2,4),(2,5)]
        left_and_right_border_cells = [(1,0),(2,0),(3,0),(1,8),(2,8),(3,8)] 
        score = 0

        if(self.position == -1):
            score = state.score[-1] - state.score[1]
        else:
            score = state.score[1] - state.score[-1]
        

        board = state.get_board()
        list_of_our_pieces =  board.get_player_pieces_on_board(Color(player))
        list_of_adv_pieces =  board.get_player_pieces_on_board(Color(adv))
        
        for piece in list_of_our_pieces :
            
            if(piece in center_cells):
                score = score + len(FanoronaRules.get_effective_cell_moves(state, piece))*2
            elif(piece in left_and_right_border_cells or piece[0] == 0 or piece[0] == 4):
                score = score + len(FanoronaRules.get_effective_cell_moves(state, piece))
            else:
                score = score + len(FanoronaRules.get_effective_cell_moves(state, piece))*1.5


        for piece in list_of_adv_pieces :
            if(piece in center_cells):
                score = score - len(FanoronaRules.get_effective_cell_moves(state, piece))*2
            elif(piece in left_and_right_border_cells or piece[0] == 0 or piece[0] == 4):
                score = score - len(FanoronaRules.get_effective_cell_moves(state, piece))
            else:
                score = score - len(FanoronaRules.get_effective_cell_moves(state, piece))*1.5
            
        return score




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