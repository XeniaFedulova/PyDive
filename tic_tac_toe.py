import random


class Playground:
    size = 0
    field = []
    curr_symbol_index = 0
    diagonals = {}
    diagonals_symbol = {}
    condition_of_win = 0

    def __init__(self, size, condition_of_win):

        self.size = size
        self.condition_of_win = condition_of_win
        self.field = ["." for i in range(size * size)]
        self.make_list_of_diagonals(self.size)

    def make_list_of_diagonals(self, size):

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
        self.field[(y - 1) * self.size + x - 1] = symbol

    def check_win(self, symbol, x, y):

        for key, item in self.diagonals.items():
            self.diagonals_symbol[key] = [self.field[j] for j in self.diagonals[key]]
            if symbol * self.condition_of_win in "".join(self.diagonals_symbol[key]):
                print('You win')
                return True

        row = x
        check_row = []
        for i in range(1, self.size + 1):
            check_row.append(self.field[(i - 1) * self.size + row - 1])
        if (symbol * self.condition_of_win) in "".join(check_row):
            print("You win")
            return True

        column = y
        check_column = []
        for i in range(1, self.size + 1):
            check_column.append(self.field[(column - 1) * self.size + i - 1])
        if (symbol * self.condition_of_win) in "".join(check_column):
            print("You win")
            return True

        if "." not in self.field:
            print("Ничья")
            return True


class Game:
    size_of_field = 0
    condition_of_win = 0
    number_of_players = 0
    players = [0]
    number_of_players = 0
    move_counter = 0

    def __init__(self, size_of_field, condition_of_win, number_of_players):

        self.size_of_field = size_of_field
        self.condition_of_win = condition_of_win
        self.number_of_players = number_of_players
        self.playground = Playground(self.size_of_field, self.condition_of_win)
        self.players = [0 for i in range(number_of_players)]


    def set_player(self, symbol):

        if symbol == "x":
            index = 0
        else:
            index = 1
            while self.players[index] != 0:
                index = random.randint(1, number_of_players-1)
        self.players[index] = Player(symbol)

    def pass_turn_to_player(self):

        self.move_counter += 1
        player = self.players[(self.move_counter - 1) % (self.number_of_players)]
        return player

class Player:
    symbol = ""
    turn = None

    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, x, y, playground):
        playground.change_playground_symbol(self.symbol, x, y)
        playground.print_field()


size_of_field = int(input('Введите размер поля:'))
condition_of_win = int(input("Введите количество победных символов:"))
number_of_players = int(input("Введите количество игроков:"))
symbol = ""
game = Game(size_of_field, condition_of_win, number_of_players)

for player in range(1, number_of_players + 1):
    symbol = input("Введите символ игрока " + str(player) + " :")
    game.set_player(symbol)

player = game.pass_turn_to_player()
print("Ход игрока "+player.symbol)
x = int(input("Введите координату x:"))
y = int(input("Введите координату y:"))
player.make_move(x, y, game.playground)
while game.playground.check_win(player.symbol, x, y) != True:
    player = game.pass_turn_to_player()
    print("Ход игрока " + player.symbol)
    x = int(input("Введите координату x:"))
    y = int(input("Введите координату y:"))
    player.make_move(x, y, game.playground)




