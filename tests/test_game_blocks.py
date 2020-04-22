from src.game import Player
from src.game.blocks import Block, Path, Wall, Portal


def test_block_render():
    assert Block(0, 0).render() == None
    assert Path(0, 0).render() == 'O'
    assert Wall(0, 0).render() == 'X'
    assert Portal(0, 0).render() == 'B'


def test_player_block_render():
    player = Player()
    path = Path(0, 0)

    path.step(player)

    assert path.render() == 'A'


def test_player_block_step():
    player = Player()
    path1 = Path(0, 0)
    path2 = Path(0, 1)

    assert player.block == None

    path1.step(player)

    assert player.block == path1

    path2.step(player)

    assert player.block == path2


def test_player_portal_block_step():
    player = Player()
    path = Path(0, 0)
    portal = Portal(0, 1)

    path.step(player)

    assert player.is_finished == False

    portal.step(player)

    assert player.is_finished == True


def test_block_is_wall():
    assert Block(0, 0).is_wall() == None
    assert Wall(0, 0).is_wall() == True