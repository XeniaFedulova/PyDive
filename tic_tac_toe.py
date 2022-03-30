class Playground:
    size = 0
    field = []
    # cross_cells_x = set()
    # cross_cells_y = set()
    curr_symb_index = 0
    diags = {}
    diags_symb = {}
    condition_of_win = 0

    def __init__(self, size, condition_of_win):

        self.size = size
        self.condition_of_win = condition_of_win
        self.field = ["0" for i in range(size * size)]

        # строим словарь с диагонялми

        n = self.size

        for i in range(n - 1):
            for j in range(i, n * (n - i), n + 1):
                if i not in self.diags:
                    self.diags[i] = []
                self.diags[i].append(j)
        for i in range(n, n * (n - 1), n):
            for j in range(i, n * n, n + 1):
                if i not in self.diags:
                    self.diags[i] = []
                self.diags[i].append(j)

        for i in range(1, n):
            for j in range(i, (i + 1) * n - 1, n - 1):
                if -i not in self.diags:
                    self.diags[-i] = []
                self.diags[-i].append(j)
        for i in range(2 * n - 1, n * (n - 1), n + 1):
            for j in range(i, n * n, n - 1):
                if -i not in self.diags:
                    self.diags[-i] = []
                self.diags[-i].append(j)

    def print_field(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.field[self.size * j + i], end='')
            print()
        print("______")

    def change_playground_symbol(self, symbol, x, y):
        self.curr_symb_index = (y - 1) * self.size + x - 1
        self.field[(y - 1) * self.size + x - 1] = symbol
        self.print_field()
        # if symbol == "x":
        #     self.cross_cells_x.add(x)
        #     self.cross_cells_y.add(y)

        if self.check_win(symbol, x, y):
            print("You win")

    def check_win(self, symbol, x, y):

        for key, item in self.diags.items():
            self.diags_symb[key] = [self.field[j] for j in self.diags[key]]
            if "".join(self.diags_symb[key]) == symbol * self.condition_of_win:
                return True

        # for key, item in self.diags.items():
        #     for k in self.diags[key]:
        #
        #         if k == self.curr_symb_index:
        #             if [self.field[j] for j in diags[key]] == ["x" for i in range(self.size)]:
        #                 print("x in diag")

        string = x
        check_string = []
        for i in range(1, self.size + 1):
            check_string.append(self.field[(i - 1) * self.size + string - 1])
        if "".join(check_string).find(symbol * self.condition_of_win) != -1:
            return True

        row = y
        check_row = []
        for i in range(1, self.size + 1):
            check_row.append(self.field[(row - 1) * self.size + i - 1])
        if "".join(check_row).find(symbol * self.condition_of_win) != -1:
            return True

        return False

        print(check_string)
        print(check_row)


#     def __init__(self, state):
#         pass
#
# class Player:
#     pass
#
# class

b = Playground(5, 3)
b.change_playground_symbol("x", 1, 1)
b.change_playground_symbol("x", 1, 2)
b.change_playground_symbol("x", 1, 3)
