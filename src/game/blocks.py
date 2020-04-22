from src.game import Block


class Path(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)

    def is_wall(self):
        return False

    def render(self):
        return 'O' if self.player == None else 'A'


class Wall(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)

    def is_wall(self):
        return True

    def render(self):
        return 'X'


class Portal(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y)

    def is_wall(self):
        return False

    def render(self):
        return 'B'

    def step(self, player):
        Block.step(self, player)
        player.is_finished = True
