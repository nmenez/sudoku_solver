import copy


class cell(object):
    def __init__(self, row, column, box, value=None):

        self.row = row
        self.column = column
        self.box = box
        self.cells = []

        if value is not None:
            self.value = value
            self.options = value
        else:
            self.value = None
            self.options = list(range(1, 10))

    def __repr__(self):
        out = 'hello i am row: %s, columns: %s , box:%s ' % (
            self.row, self.column, self.box)
        if self.value is not None:
            out += '\n' + 'my value is %s' % self.value
        else:
            out += '\n' + ' my potential values are %s ' % str(self.options)
        return out

    def getvalue(self):
        return self._value

    def setvalue(self, value):
        if self.cells.__len__() > 0:
            for c in self.cells:
                if ((c.row == self.row) | (c.column == self.column) |
                        (c.box == self.box)) & (c is not self):
                    if c.value == value:

                        raise Exception
                    else:
                        self._value = value
                        self.options = [value]
        else:
            self._value = value
    value = property(getvalue, setvalue)

    def remove_potential(self, value):
        if self.value is not None:
            return True

        elif self.options.__len__() == 0:
            return False

        elif value in self.options:
            self.options.remove(value)
            if self.options.__len__() == 1:

                self.value = self.options[0]
                self.broadcast_value()
            else:
                return True

    def broadcast_value(self, talk=False):
        for c in self.cells:
            if c is self:
                continue
            if (c.row == self.row) | (c.column == self.column) \
                    | (c.box == self.box):
                c.remove_potential(self.value)


class Game(object):
    def __init__(self, values):

        self.cells = []
        for r, row in enumerate(values):
            for c, value in enumerate(row):
                if value == '':
                    value = None
                if value == 0:
                    value = None
                self.cells.append(cell(r, c, (r // 3, c // 3), value))

        for c in self.cells:
            c.cells = self.cells
            c.game = self

    def boxes_solved(self):
        # return filter(lambda c: c.value is not None, self.cells).__len__()
        return len([c for c in self.cells if c.value is not None])

    def __repr__(self):
        current_row = 0
        out = ''
        for cell in self.cells:
            if cell.row != current_row:
                out += '\n'
                current_row = cell.row
            if cell.value is not None:
                out += '|' + str(cell.value)
            else:
                out += '|' + ' '

        return out

    def issolved(self):
        for cell in self.cells:
            if cell.value is None:
                return False

        return True

    def obvious_solves(self):
        for idx, c in enumerate(self.cells):
            if c.value is not None:
                c.broadcast_value()

    def test(self, cell_index, value):
        test_game = copy.deepcopy(self)
        try:
            test_game.cells[cell_index].value = value
            test_game.obvious_solves()
            return True, value, test_game.boxes_solved()
        except:
            return False, 0, 0

    def strike_bads(self):
        for idx, c in enumerate(self.cells):
            if self.issolved() is True:
                break
            if c.value is None:
                # print c
                options = list(c.options)
                successes = [self.test(idx, a) for a in options]
                successes = [x for x in successes if x[0] is True]
                #successes = filter(lambda x: x[0], successes)
                solution = sorted(successes, key=lambda x: x[2], reverse=True)
                if solution.__len__() > 1:
                    new_options = [s[1] for s in solution]
                    c.options = new_options
                else:
                    c.value = solution[0][1]

                    c.options = [c.value]
                    c.broadcast_value()


def get_game_values(game_values_file):
    game_values = []
    with open(game_values_file) as fp:
        for line in fp:
            row = line.split(',')
            row = [int(r) for r in row]
            game_values.append(row)

    return game_values


def play(game_file):

    game_values = get_game_values(game_file)

    game = Game(game_values)
    print(game)
    print('____________________')
    round = 0
    while game.issolved() is False:
        round += 1
        print('=====================')
        print('round : %s' % round)
        game.obvious_solves()
        game.strike_bads()
    print(game)


if __name__  ==  "__main__":
    play('game_values3.txt')
