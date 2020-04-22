import os
import sys
import time
import csv
from src.menu import Menu, Option
from src.game import Player, Field, Direction
from src.game.blocks import Path, Wall, Portal


class App():
    def __init__(self):
        self.field = None

        self.ended = False
        self.is_in_maze = False

    def end(self):
        self.ended = True

    def start(self):
        menu = Menu([
            Option("1", "Read and load maze from file", self.load_maze),
            Option("2", "View maze", self.view_maze),
            Option("3", "Play maze game", self.play_maze),
            Option("4", "Configure current maze", self.edit_maze),
            Option("0", "Exit maze", self.end),
        ])

        while not self.ended:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Main menu")
            print("=========")
            print(menu.render())
            if not menu.select(input("Enter your option: ")):
                print("Invalid menu option, try again!")
                input("Press Enter to continue...")
            print()

    def end_play_maze(self):
        self.is_in_maze = False

    def play_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        if self.field == None:
            print("There is no maze currently loaded.")
            input("Press Enter to continue...")
            return

        self.player = Player()
        self.field.enter(self.player)
        self.is_in_maze = True

        while self.is_in_maze:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.field.render())
            print()

            start = self.field.start_block
            blocks = [block for row in self.field.blocks for block in row]
            ends = [block for block in blocks if isinstance(block, Portal)]
            print("Location of start (A) = {0}".format(
                f"(row {start.y + 1}, col {start.x + 1})"))
            print("Location of End (B) = {0}".format(
                ', '.join([f"(row {block.y + 1}, col {block.x + 1})" for block in ends])))

            def move(player, direction):
                if not self.field.move(player, direction):
                    print("Invalid movement entered in game. Please try again")
                    time.sleep(1)

            menu = Menu([
                Option("w", "Move up", lambda: move(
                    self.player, Direction.up)),
                Option("a", "Move left", lambda: move(
                    self.player, Direction.left)),
                Option("s", "Move down", lambda: move(
                    self.player, Direction.down)),
                Option("d", "Move right", lambda: move(
                    self.player, Direction.right)),
                Option("m", "Return to menu", lambda: self.end_play_maze()),
            ])
            selection = input(
                "Use the WASD to move or M key to return to menu: ")
            menu.select(selection)

            if self.player.is_finished:
                print()
                print("You have completed the maze, congratulations!")
                input("Press Enter to continue...")
                self.end_play_maze()

    def view_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        if self.field == None:
            print("There is no maze currently loaded.")
            input("Press Enter to continue...")
            return

        self.player = Player()
        self.field.enter(self.player)
        print(self.field.render())
        input("Press Enter to continue...")

    def load_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        file_name = input("Enter file name (without extension): ")

        try:
            csv_file = open(f'{file_name}.csv')
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_data = list(csv_reader)
            blocks = [[] for _ in range(sum(1 for row in csv_data))]
            start_block = None
            is_invalid = False
            csv_file.close()

            for i, row in enumerate(csv_data):
                for ii, col in enumerate(row):
                    block = (
                        Wall(ii, i) if col == 'X' else
                        Portal(ii, i) if col == 'B' else
                        Path(ii, i) if col == 'A' or col == 'O' else
                        True
                    )
                    blocks[i].append(block)
                    if col == 'A':
                        start_block = block

                    if block == True:
                        is_invalid = True
                        break

            if is_invalid:
                print(
                    "Invalid file type/content, please ensure that the file is proper.")
                input("Press Enter to continue...")
                return

            if start_block is None:
                print("Maze does not contain a start point, please verify the maze file!")
                input("Press Enter to continue...")
                return

            print(f'Processed {len(blocks)} lines.')

            self.field = Field(blocks, start_block)
            self.player = Player()
            self.field.enter(self.player)
            print("\n" + self.field.render() + '\n')

            print("Successfully loaded maze!")
            input("Press Enter to continue...")
        except IOError:
            print("File does not exist.")
            input("Press Enter to continue...")

    def edit_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        if self.field == None:
            print("There is no maze currently loaded.")
            input("Press Enter to continue...")
            return
        Editor(self.field).start()


class Editor():
    def __init__(self, field):
        self.field = field
        self.ended = False

    def end(self):
        self.ended = True

    def start(self):
        while not self.ended:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.field.enter(Player())
            print(self.field.render())
            print()
            print("Configuration Menu")
            print("==================")

            menu = Menu([
                Option("1", "Create wall", self.create_wall),
                Option("2", "Create passageway", self.create_passageway),
                Option("3", "Create start point", self.create_start_point),
                Option("4", "Create end point", self.create_end_point),
                Option("0", "Exit to Main Menu", lambda: self.end()),
            ])
            print(menu.render())
            selection = input("Enter your option: ")
            menu.select(selection)

    def create_start_point(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        player = Player()
        self.field.enter(player)
        print(self.field.render())
        print()

        selection = input(
            "Enter the coordinate of the item (e.g row, col)\n'B' to return to configure menu.\n'M' to return to main menu. ").lower()

        if not (selection == 'm' or selection == 'b'):
            try:
                split = selection.split(',')
                row = int(split[0])
                col = int(split[1])

                block = self.field.blocks[row - 1][col - 1]

                if not isinstance(block, Path):
                    print(f"Cannot place a start point on non-passageways!")
                    input("Press Enter to continue...")
                    return

                self.field.start_block = block
                self.field.enter(player)

                os.system('cls' if os.name == 'nt' else 'clear')
                self.field.enter(Player())
                print(self.field.render())
                print()
                print(f"A Start Point block placed at {row}, {col}")
                input("Press Enter to continue...")
            except:
                print("Invalid block coordinates!")
                input("Press Enter to continue...")
        elif selection == 'm':
            self.end()

    def create_end_point(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        player = Player()
        self.field.enter(player)
        print(self.field.render())
        print()

        selection = input(
            "Enter the coordinate of the item (e.g row, col)\n'B' to return to configure menu.\n'M' to return to main menu. ").lower()

        if not (selection == 'm' or selection == 'b'):
            try:
                split = selection.split(',')
                row = int(split[0])
                col = int(split[1])

                block = self.field.blocks[row - 1][col - 1]

                if not isinstance(block, Path):
                    print(f"Cannot place an end point on non-passageways!")
                    input("Press Enter to continue...")
                    return

                if block == self.field.start_block:
                    print(f"Cannot place an end point on the start block!")
                    input("Press Enter to continue...")
                    return

                blocks = [block for row in self.field.blocks for block in row]
                portals = [
                    block for block in blocks if isinstance(block, Portal)]

                for portal in portals:
                    self.field.blocks[portal.y][portal.x] = Path(
                        portal.x, portal.y)

                self.field.blocks[row - 1][col - 1] = Portal(col - 1, row - 1)
                self.field.enter(player)

                os.system('cls' if os.name == 'nt' else 'clear')
                self.field.enter(Player())
                print(self.field.render())
                print()
                print(f"End Point block placed at {row}, {col}")
                input("Press Enter to continue...")
            except:
                print("Invalid block coordinates!")
                input("Press Enter to continue...")
        elif selection == 'm':
            self.end()

    def create_passageway(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        player = Player()
        self.field.enter(player)
        print(self.field.render())
        print()

        selection = input(
            "Enter the coordinate of the item (e.g row, col)\n'B' to return to configure menu.\n'M' to return to main menu. ").lower()

        if not (selection == 'm' or selection == 'b'):
            try:
                split = selection.split(',')
                row = int(split[0])
                col = int(split[1])

                block = self.field.blocks[row - 1][col - 1]

                if not isinstance(block, Wall):
                    print(f"Path can only be placed over walls")
                    input("Press Enter to continue...")
                    return

                self.field.blocks[row - 1][col - 1] = Path(col - 1, row - 1)
                self.field.enter(player)

                os.system('cls' if os.name == 'nt' else 'clear')
                self.field.enter(Player())
                print(self.field.render())
                print()
                print(f"Path block placed at {row}, {col}")
                input("Press Enter to continue...")
            except:
                print("Invalid block coordinates!")
                input("Press Enter to continue...")
        elif selection == 'm':
            self.end()

    def create_wall(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        player = Player()
        self.field.enter(player)
        print(self.field.render())
        print()

        selection = input(
            "Enter the coordinate of the item (e.g row, col)\n'B' to return to configure menu.\n'M' to return to main menu. ").lower()

        if not (selection == 'm' or selection == 'b'):
            try:
                split = selection.split(',')
                row = int(split[0])
                col = int(split[1])

                block = self.field.blocks[row - 1][col - 1]

                if not isinstance(block, Path):
                    print(f"Walls can only be placed over paths")
                    input("Press Enter to continue...")
                    return

                self.field.blocks[row - 1][col - 1] = Wall(col - 1, row - 1)
                self.field.enter(player)

                os.system('cls' if os.name == 'nt' else 'clear')
                self.field.enter(Player())
                print(self.field.render())
                print()
                print(f"Wall block placed at {row}, {col}")
                input("Press Enter to continue...")
            except:
                print("Invalid block coordinates!")
                input("Press Enter to continue...")
        elif selection == 'm':
            self.end()
