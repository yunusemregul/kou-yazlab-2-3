import math
import random

class Cell:
    def __init__(self, reward=0, actions=[]):
        self.reward = reward
        self.actions = actions

    def getMaxAction(self):
        maxActions = []

        maxActionReward = -math.inf

        for action in self.actions:
            if action.reward > maxActionReward:
                maxActionReward = action.reward

        for action in self.actions:
            if maxActionReward == action.reward:
                maxActions.append(action)

        return random.choice(maxActions)