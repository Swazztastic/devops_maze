from src.game import Player, Field, Direction
from src.game.blocks import Path, Wall, Portal


def test_field_enter():
    start_block = Path(0, 0)
    blocks = [[start_block, Path(1, 0)]]
    field = Field(blocks, start_block)
    player = Player()

    assert player.field == None
    assert player.block == None

    field.enter(player)

    assert player.field == field
    assert player.block == start_block


def test_field_render():
    start_block = Path(0, 0)
    blocks = [[start_block, Path(1, 0)]]
    field = Field(blocks, start_block)

    assert field.render() == 'O, O'

    player = Player()
    field.enter(player)

    assert field.render() == 'A, O'

    start_block = Path(0, 0)
    blocks = [[start_block, Path(1, 0)], [Path(0, 1), Path(1, 1)]]
    field = Field(blocks, start_block)

    assert field.render() == 'O, O\nO, O'


def test_field_move():
    left_top = Path(0, 0)
    right_top = Path(1, 0)
    left_bottom = Path(0, 1)
    right_bottom = Path(1, 1)
    blocks = [[left_top, right_top], [left_bottom, right_bottom]]
    field = Field(blocks, left_top)
    player = Player()

    field.enter(player)
    assert player.block == left_top

    field.move(player, Direction.up)
    assert player.block == left_top

    field.move(player, Direction.down)
    assert player.block == left_bottom

    field.move(player, Direction.right)
    assert player.block == right_bottom

    field.move(player, Direction.left | Direction.up)
    assert player.block == left_top


def test_field_move_wall():
    left_top = Path(0, 0)
    right_top = Wall(1, 0)
    left_bottom = Path(0, 1)
    right_bottom = Path(1, 1)
    blocks = [[left_top, right_top], [left_bottom, right_bottom]]
    field = Field(blocks, left_top)
    player = Player()

    field.enter(player)
    field.move(player, Direction.right)
    assert player.block == left_top


def test_field_move_portal():
    left_top = Path(0, 0)
    right_top = Portal(1, 0)
    left_bottom = Path(0, 1)
    right_bottom = Path(1, 1)
    blocks = [[left_top, right_top], [left_bottom, right_bottom]]
    field = Field(blocks, left_top)
    player = Player()

    field.enter(player)
    field.move(player, Direction.right)
    assert player.block == right_top
    assert player.is_finished
