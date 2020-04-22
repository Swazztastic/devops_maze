class Menu():
    def __init__(self, options):
        self.options = {option.option.lower(): option for option in options}

    def render(self):
        return '\n'.join(
            [option.render() for option in self.options.values()]
        )

    def select(self, option):
        if option.lower() in self.options:
            self.options[option.lower()].action()
            return True
        return False

class Option():
    def __init__(self, option, text, action):
        self.option = option
        self.text = text
        self.action = action

    def render(self):
        return f"[{self.option}] {self.text}"
