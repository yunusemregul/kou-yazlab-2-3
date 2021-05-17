directionVectors = {
    'top': (0, -1),
    'bottom': (0, 1),
    'left': (-1, 0),
    'right': (1, 0),
    'topleft': (-1, -1),
    'topright': (1, -1),
    'bottomleft': (-1, 1),
    'bottomright': (1, 1)
}


class Action:
    def __init__(self, direction, reward=0):
        self.reward = reward
        self.direction = direction
        self.directionVector = directionVectors[self.direction]

    def __repr__(self):
        return "Action{dir='%s', rwrd=%d}" % (self.direction, self.reward)
