
from fanorona.fanorona_player import FanoronaPlayer
from fanorona.fanorona_rules import FanoronaRules
from fanorona.fanorona_action import FanoronaAction
from fanorona.fanorona_action import FanoronaActionType
import random


class AI(FanoronaPlayer):

    name = "War of Hearts"

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value

    def play(self, state, remain_time):
        #Retrieve a random action
        action = FanoronaRules.random_play(state, self.position)
        #Extract departure and arrival of the piece
        actionDict = action.get_action_as_dict()
        at = actionDict['action']['at']
        to = actionDict['action']['to']
        #check if it is a win move both for approach and remote
        if (FanoronaRules.is_win_approach_move(at, to, state, self.position) is not None) and (FanoronaRules.is_win_remote_move(at, to, state, self.position) is not None) and len(FanoronaRules.is_win_approach_move(at, to, state, self.position)) != 0 and len(FanoronaRules.is_win_remote_move(at, to, state, self.position)) != 0:
            # between win approach and win remoate, check which can let me gain the more adverse pieces
            if len(FanoronaRules.is_win_approach_move(at, to, state, self.position)) < len(FanoronaRules.is_win_remote_move(at, to, state, self.position)):
                action = FanoronaAction(action_type=FanoronaActionType.MOVE, win_by='REMOTE', at=at, to=to)
            else: 
                action = FanoronaAction(action_type=FanoronaActionType.MOVE, win_by='APPROACH', at=at, to=to)
        return action 