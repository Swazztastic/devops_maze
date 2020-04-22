from src.menu import Menu, Option


def test_option_render():
    option = Option("1", "Testing option", lambda: None)
    assert(option.render() == "[1] Testing option")


def test_menu_render():
    option1 = Option("1", "Option 1", lambda: None)
    option2 = Option("2", "Option 2", lambda: None)
    menu = Menu([option1, option2])
    assert menu.render() == "[1] Option 1\n[2] Option 2"


def _option_select():
    assert True


def test_menu_select():
    option = Option("1", "Select!", _option_select)
    menu = Menu([option])

    assert menu.select("1")
    assert menu.select("0") == False
