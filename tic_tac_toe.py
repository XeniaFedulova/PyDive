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
        self._make_list_of_diagonals(self.size)

    def _make_list_of_diagonals(self, size):
        #защищенный метод
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
        self.curr_symbol_index = (y - 1) * self.size + x - 1
        self.field[self.curr_symbol_index] = symbol

    def cell_is_free(self, x, y):
        if self.field[(y - 1) * self.size + x - 1] == '.':
            return True
        else:
            return False

class Game:
    mode = None
    size_of_field = 0
    condition_of_win = 0
    number_of_players = 0
    players = [0]
    move_counter = 0
    playground = None

    def __init__(self, mode, size_of_field, condition_of_win, number_of_players):

        self.mode = mode
        self.size_of_field = size_of_field
        self.condition_of_win = condition_of_win
        self.number_of_players = number_of_players
        self.playground = Playground(self.size_of_field)
        self.players = [0 for i in range(number_of_players)]

    def set_params(self):
        if mode == 1:
            self.size_of_field = int(input('Введите размер поля:'))
            self.condition_of_win = int(input(
                "Введите условие победы (кол-во одинаковых символов в строке, столбце или диагонали подряд, необходимое для победы):"))
            self.number_of_players = int(input("Введите количество игроков:"))


    def set_player(self, symbol):

        if symbol == "x":
            index = 0
        else:
            index = 1
            while self.players[index] != 0:
                index = random.randint(1, number_of_players - 1)
        self.players[index] = Player(symbol, self)

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
            if self.check_win(player.symbol, coordinates[0], coordinates[1], self.playground):
                print("Вы выйграли!")
                break
            elif self.if_dead_head(self.playground):
                print("Ничья")
                break
            player = self.pass_turn_to_player()

    def check_win(self, symbol, x, y, playground):

        for key, item in playground.diagonals.items():
            playground.diagonals_symbol[key] = [playground.field[j] for j in playground.diagonals[key]]
            if symbol * self.condition_of_win in "".join(playground.diagonals_symbol[key]):
                return True

        row = x
        check_row = []
        for i in range(1, playground.size + 1):
            check_row.append(playground.field[(i - 1) * playground.size + row - 1])
        if (symbol * self.condition_of_win) in "".join(check_row):
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

    def field_state(self):
        field_copy = self.playground.field.copy()
        return field_copy

class Player:

    symbol = ""
    game = None

    def __init__(self, symbol, game):
        self.symbol = symbol
        self.game = game

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


# class ConsolePlayer(Player):
#
#     def make_move(self):


class AIPlayer(Player):

    def opponent(self):
        if self.symbol == "x":
            opponent = AIPlayer("o", self.game)
            return opponent
        else:
            opponent = AIPlayer("x", self.game)
            return opponent


    def make_move(self):

        indexes = {(1,1): 0, (1,2): 0, (1,3): 0, (2,1): 0, (2,2): 0, (2,3): 0, (3,1): 0, (3,2): 0, (3,3): 0}
        for cell, score in indexes.items():
            field_state = self.game.field_state()
            x = cell[0]
            y = cell[1]
            if self.game.cell_is_free(self, x, y):
                field_state[(y - 1) * 3 + x - 1] = self.symbol
                if self.game.check_win(self.symbol, x, y, field_state):
                    score += 10
                    return score
                elif self.game.check_win(self.opponent.symbol(), x, y, field_state):
                    score -= 10
                    return score
                elif self.game.if_dead_head(field_state):
                    score = 0
                    return score

                self.opponent.make_move(field_state)
                self.make_move(field_state)

        maximum = max(indexes, key=indexes.get())
        return maximum












#список игроков и борд создается снаружи

mode = int(input('Выберите режим игры: 1 - игра с людьми, 2 - игра с компьютером (поле 3х3):'))
if mode == 1:
    size_of_field = int(input('Введите размер поля:'))
    condition_of_win = int(input(
        "Введите условие победы (кол-во одинаковых символов в строке, столбце или диагонали подряд, необходимое для победы):"))
    number_of_players = int(input("Введите количество игроков:"))
    symbol = ""
    game = Game(size_of_field, condition_of_win, number_of_players)
if mode == 2:
    game = Game(3, 3, 2)

for player in range(1, number_of_players + 1):
    symbol = input("Введите символ игрока" + str(player) + " :")
    game.set_player(symbol)

game.play_game()







#создать игру
#метод Play у игры с циклами
#игроки наследуются от класса Плеер
#введение координат для ходов игроков - метод игрока


# win = False
# while True:
#     if win:
#         break
#     player = game.pass_turn_to_player()
#     print("Ход игрока " + player.symbol)
#     while True:
#         x = int(input("Введите координату x:"))
#         y = int(input("Введите координату y:"))
#         try:
#             if game.playground.cell_is_free(x, y):
#                 player.make_move(x, y, game.playground)
#                 win = game.playground.check_win(player.symbol, x, y)
#                 break
#             else:
#                 print("Клетка уже занята")
#         except:
#             print("Клетка по заданным вами координатам лежит вне игрового поля")

#написать доку для make move - возвращает валидные координаты, куда можно поставить символ
#перенести чек вин в Game - часть метода play
#логика проверки - в класс Game
#обращение к полям класса - это плохо
