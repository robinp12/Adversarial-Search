

from os import stat

from fanorona.fanorona_player import FanoronaPlayer
from fanorona.fanorona_rules import FanoronaRules
from copy import deepcopy
import random



class AI(FanoronaPlayer):

    name = "Contest"

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value

    def play(self, state, remain_time):
        print("")
        print(f"Player {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        return self.iterative_deepening (state, remain_time)

    def successors(self, state):
        all_good_moves=  list()
        all_bad_moves = list()

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
            return all_good_moves
        else:
            #random.shuffle(all_bad_moves)
            return all_bad_moves[0:3]

    def cutoff(self, state, depth):
        if(depth <= 0  or FanoronaRules.is_end_game(state)):
            return True
        else: 
            return False
    
    def evaluate(self, state):
            if(self.position == -1):
                return (state.score[-1] - state.score[1])
            else:
                return (state.score[1] - state.score[-1])

    def iterative_deepening(self, state, remain_time):   

        inf = float("inf")

        def minimax_search(state, alpha, beta, depth):
            def max_value(state, alpha, beta, depth):
                val = -inf
                for a, s in AI.successors(self, state):
                    val = max(val, minimax_search(s, alpha, beta, depth))
                    if val >= beta:
                        return val
                    alpha = max(alpha, val)
                return val

            def min_value(state, alpha, beta, depth):
                val = inf
                for a, s in AI.successors(self, state):
                    val = min(val, minimax_search(s, alpha, beta, depth - 1))
                    if val <= alpha:
                        return val
                    beta = min(beta, val)
                return val

            if self.cutoff(state, depth) or remain_time < 0.25: 
                return AI.evaluate(self, state)

            if state.get_latest_player() == state.get_next_player():
                return max_value(state, alpha, beta, depth)
            else:
                return min_value(state, alpha, beta, depth)
                

        best_action = None
        for depth in range(1,3):
            if remain_time < 0.25:
                break
            #beginning of the iterative deepening fct    
            val = -inf
            for a, s in AI.successors(self, state):
                score = minimax_search(s,-inf,inf, depth)
                if score > val:
                    val, best_action = score, a
        return best_action   