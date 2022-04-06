import random
import copy


class Playground:
    size = 0
    field = []
    diagonals = {}
    diagonals_symbol = {}

    def __init__(self, size):

        self.size = size
        self.field = ["." for i in range(size * size)]
        self._make_list_of_diagonals()

    def _make_list_of_diagonals(self):
        # защищенный метод
        n = self.size

        for i in range(n - 1):
            for j in range(i, n * (n - i), n + 1):
                if i not in self.diagonals:
                    self.diagonals[i] = []
                self.diagonals[i].append(j)
        for i in range(n, n * (n - 1), n):
            for j in range(i, n * n, n + 1):
                if i not in self.diagonals:
                    self.diagonals[i] = []
                self.diagonals[i].append(j)
        for i in range(1, n):
            for j in range(i, (i + 1) * n - 1, n - 1):
                if -i not in self.diagonals:
                    self.diagonals[-i] = []
                self.diagonals[-i].append(j)
        for i in range(2 * n - 1, n * (n - 1), n + 1):
            for j in range(i, n * n, n - 1):
                if -i not in self.diagonals:
                    self.diagonals[-i] = []
                self.diagonals[-i].append(j)

    def print_field(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.field[self.size * j + i], end='')
            print()
        print("______")

    def change_playground_symbol(self, symbol, x, y):
        curr_symbol_index = (y - 1) * self.size + x - 1
        self.field[curr_symbol_index] = symbol

    def cell_is_free(self, x, y):
        if self.field[(y - 1) * self.size + x - 1] == '.':
            return True
        return False


class Game:
    mode = None
    size_of_field = 0
    condition_of_win = 0
    number_of_players = 0
    players = [0]
    move_counter = 0
    playground = None

    def __init__(self, mode):

        self.mode = mode
        self._set_params()

    def _set_params(self):
        if mode == 1:
            self.size_of_field = int(input('Введите размер поля:'))
            self.condition_of_win = int(input(
                "Введите условие победы (кол-во одинаковых символов в строке, столбце или диагонали подряд, необходимое для победы):"))
            self.number_of_players = int(input("Введите количество игроков:"))
            self.playground = Playground(self.size_of_field)
            self.players = [0 for i in range(self.number_of_players)]

        elif mode == 2:
            self.size_of_field = 3
            self.condition_of_win = 3
            self.number_of_players = 2
            self.playground = Playground(self.size_of_field)
            self.players = [0 for i in range(self.number_of_players)]

        self._set_list_of_players()

    def _set_list_of_players(self):
        if self.mode == 1:
            for player in range(1, self.number_of_players + 1):
                symbol = input("Введите символ игрока" + str(player) + " :")
                self.set_player(symbol)
        elif self.mode == 2:
            gamer_symbol = input("Каким символом вы хотите играть (x или o?)")
            self.set_player(gamer_symbol)
            if gamer_symbol == 'x':
                self.players = [ConsolePlayer("x", self), AIPlayer("o", self)]
            elif gamer_symbol == 'o':
                self.players = [AIPlayer("x", self), ConsolePlayer("o", self)]

    def set_player(self, symbol):

        if symbol == "x":
            index = 0
        else:
            index = 1
            while self.players[index] != 0:
                index = random.randint(1, self.number_of_players - 1)
        self.players[index] = ConsolePlayer(symbol, self)

    def pass_turn_to_player(self):

        self.move_counter += 1
        player = self.players[(self.move_counter - 1) % (self.number_of_players)]
        return player

    def change_playground_symbol(self, symbol, coordinates: tuple):
        return self.playground.change_playground_symbol(symbol, coordinates[0], coordinates[1])

    def play_game(self):

        player = self.pass_turn_to_player()
        while True:
            print("Ход игрока " + player.symbol)
            coordinates = player.make_move()
            self.change_playground_symbol(player.symbol, coordinates)
            self.playground.print_field()
            if self.check_win(player.symbol, coordinates[0], coordinates[1]):
                print("Игрок "+player.symbol+" выйграл")
                break
            elif self.if_dead_head(self.playground):
                print("Ничья")
                break
            player = self.pass_turn_to_player()

    def check_win(self, symbol, x, y):

        playground = self.playground

        for key, item in playground.diagonals.items():
            playground.diagonals_symbol[key] = [playground.field[j] for j in playground.diagonals[key]]
            if symbol * self.condition_of_win in "".join(playground.diagonals_symbol[key]):
                return True

        row = x
        check_row = []
        for i in range(1, playground.size + 1):
            check_row.append(playground.field[(i - 1) * playground.size + row - 1])
        if symbol * self.condition_of_win in "".join(check_row):
            return True

        column = y
        check_column = []
        for i in range(1, playground.size + 1):
            check_column.append(playground.field[(column - 1) * playground.size + i - 1])
        if (symbol * self.condition_of_win) in "".join(check_column):
            return True

    def if_dead_head(self, playground):

        if "." not in playground.field:
            return True

    def cell_is_free(self, x, y):
        return self.playground.cell_is_free(x, y)


class Player:
    symbol = ""
    game = None

    def __init__(self, symbol, game):
        self.symbol = symbol
        self.game = game


class ConsolePlayer(Player):

    def make_move(self):
        while True:
            x = int(input("Введите координату x:"))
            y = int(input("Введите координату y:"))
            try:
                if self.game.cell_is_free(x, y):
                    return x, y
                else:
                    print("Клетка уже занята")
            except:
                print("Клетка по заданным вами координатам лежит вне игрового поля")


class AIPlayer(Player):

    def opponent_symbol(self):
        if self.symbol == "x":
            return "o"
        else:
            return "x"

    def necessary_cell(self):
        cell_need_to_take = None
        opponent_symbol = self.opponent_symbol()
        game_state = copy.deepcopy(self.game)
        for i in range(1, 4):
            for j in range(1, 4):
                if game.cell_is_free(i, j):
                    game_state.change_playground_symbol(self.symbol, (i, j))
                    if game_state.check_win(self.symbol, i, j):
                        return i, j
                    else:
                        game_state.change_playground_symbol('.', (i, j))

                    potentional_opponent_coord = (i, j)
                    game_state.change_playground_symbol(opponent_symbol, potentional_opponent_coord)
                    if game_state.check_win(opponent_symbol, i, j):
                        cell_need_to_take = (i, j)
                    game_state.change_playground_symbol('.', potentional_opponent_coord)

        if cell_need_to_take != None:
            return cell_need_to_take
        else:
            return False

    def make_move(self):

        if game.move_counter == 1:
            x, y = 2, 2
            return x, y
        else:
            necessary_cell = self.necessary_cell()
            if not necessary_cell:
                while True:
                    x = random.randint(1, 3)
                    y = random.randint(1, 3)
                    if self.game.cell_is_free(x, y):
                        return x, y
            else:
                return necessary_cell


mode = int(input('Выберите режим игры: 1 - игра с людьми, 2 - игра с компьютером (поле 3х3):'))
game = Game(mode)
game.play_game()
