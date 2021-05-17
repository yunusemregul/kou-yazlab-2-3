class Action:
    def __init__(self, direction, reward=0):
        self.reward = reward
        self.direction = direction

    def __repr__(self):
        return "Action{dir='%s', rwrd=%d}" % (self.direction, self.reward)
