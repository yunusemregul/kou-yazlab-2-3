import math
import random

from Action import Action
from Constants import REWARDS


class Cell:
    def __init__(self, pos, reward=REWARDS["empty"], actions=[]):
        self.pos = pos
        self.reward = reward
        self.actions = actions

    def getMaxAction(self) -> Action:
        maxActions = []

        maxActionReward = -math.inf

        for action in self.actions:
            if action.reward > maxActionReward:
                maxActionReward = action.reward

        for action in self.actions:
            if maxActionReward == action.reward:
                maxActions.append(action)

        return random.choice(maxActions)

    def __repr__(self):
        return "Cell{%s}" % (self.actions)
