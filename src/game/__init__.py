from enum import IntFlag


class Player():
    def __init__(self):
        self.field = None
        self.block = None
        self.is_finished = False


class Field():
    def __init__(self, blocks, start_block):
        self.blocks = blocks
        self.start_block = start_block

    def enter(self, player):
        player.field = self
        self.start_block.step(player)

    def move(self, player, direction):
        target_x = player.block.x
        target_y = player.block.y

        if Direction.up in direction:
            target_y -= 1
        if Direction.down in direction:
            target_y += 1
        if Direction.left in direction:
            target_x -= 1
        if Direction.right in direction:
            target_x += 1

        target_y = max(0, target_y)
        target_x = max(0, target_x)
        target_y = min(len(self.blocks) - 1, target_y)
        target_x = min(len(self.blocks[0]) - 1, target_x)

        target_block = self.blocks[target_y][target_x]

        if not target_block.is_wall():
            target_block.step(player)
            return True
        return False

    def render(self):
        render = [', '.join([block.render() for block in row])
                  for row in self.blocks]
        render = '\n'.join(render)
        return render


class Block():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player = None

    def is_wall(self):
        pass

    def step(self, player):
        if player.block != None:
            player.block.player = None
        player.block = self
        self.player = player

    def render(self):
        pass


class Direction(IntFlag):
    up = 0x1
    down = 0x2
    left = 0x4
    right = 0x8
