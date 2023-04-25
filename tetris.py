from random import choice


class Field:
    # figures = {
    #     'i': [(-1, 0), (0, 0), (1, 0), (2, 0)],
    #     'o': [(0, 0), (1, 0), (0, -1), (1, -1)],
    #     't': [(0, 0), (-1, -1), (0, -1), (1, -1)],
    #     'l': [(-1, -1), (0, -1), (1, -1), (1, 0)],
    #     'j': [(-1, 0), (0, 0), (1, 0), (1, -1)],
    #     'z': [(0, 1), (1, 1), (1, 0), (2, 0)],
    #     's': [(-1, 0), (0, 0), (0, 1), (1, 1)]
    # }
    figures = [
        [(-1, 0), (0, 0), (1, 0), (2, 0)],
        [(0, 0), (1, 0), (0, -1), (1, -1)],
        [(0, 0), (-1, -1), (0, -1), (1, -1)],
        [(-1, -1), (0, -1), (1, -1), (1, 0)],
        [(-1, 0), (0, 0), (1, 0), (1, -1)],
        [(-1, 0), (0, 0), (0, -1), (1, -1)],
        [(-1, -1), (0, -1), (0, 0), (1, 0)]
    ]
    changes = {
        'left': {
            (-1, 0): (0, -2),
            (-1, -1): (1, -2),
            (0, 1): (-1, -1),
            (0, 0): (0, -1),
            (0, -1): (1, -1),
            (0, -2): (2, -1),
            (1, 1): (-1, 0),
            (1, 0): (0, 0),
            (1, -1): (1, 0),
            (1, -2): (2, 0),
            (2, 0): (0, 1),
            (2, -1): (1, 1)
        },
        'right': {
            (0, -2): (-1, 0),
            (1, -2): (-1, -1),
            (-1, -1): (0, 1),
            (0, -1): (0, 0),
            (1, -1): (0, -1),
            (2, -1): (0, -2),
            (-1, 0): (1, 1),
            (0, 0): (1, 0),
            (1, 0): (1, -1),
            (2, 0): (1, -2),
            (0, 1): (2, 0),
            (1, 1): (2, -1)
        }
    }

    x = 10
    y = 20
    field = [['🟥' for _ in range(10)] for _ in range(20)]

    point = [2, 0]
    figure = choice(figures)

    score = 0

    def choose_figure(self):
        self.figure = choice(self.figures)

    def edit(self, color):
        for tale in self.figure:
            self.field[self.point[1] - tale[1]][self.point[0] + tale[0]] = color

    def add(self):
        self.edit(color='🟩')

    def remove(self):
        self.edit(color='🟥')

    def fly(self):
        for tale in self.figure:
            if (self.point[1] - tale[1] == self.y-1
                    or self.field[self.point[1] - tale[1] + 1][self.point[0] + tale[0]] == '🟦'):
                self.edit(color='🟦')
                self.choose_figure()
                self.point = [2, 0]
                self.add()
                return
        self.edit(color='🟥')
        self.point[1] += 1
        self.edit(color='🟩')

    def move(self, direction):
        for tale in self.figure:
            match direction:
                case 'left':
                    if (self.point[0] + tale[0] == 0
                            or self.field[self.point[1] - tale[1]][self.point[0] + tale[0]-1] == '🟦'):
                        return
                case 'right':
                    if (self.point[0] + tale[0] == self.x - 1
                            or self.field[self.point[1] - tale[1]][self.point[0] + tale[0]+1] == '🟦'):
                        return

        self.edit(color='🟥')
        match direction:
            case 'left':
                self.point[0] -= 1
            case 'right':
                self.point[0] += 1
        self.edit(color='🟩')

    def rotate(self, direction):
        for tale_id in range(len(self.figure)):
            new_tale = self.changes[direction][self.figure[tale_id]]
            if (self.point[0] + new_tale[0] < 0 or self.point[0] + new_tale[0] > self.x - 1
                    or self.point[1] - new_tale[1] < 0 or self.point[1] - new_tale[1] > self.y - 1
                    or self.field[self.point[1] - new_tale[1]][self.point[1] - new_tale[1]] == '🟦'):
                return
        self.remove()
        for tale_id in range(len(self.figure)):
            self.figure[tale_id] = self.changes[direction][self.figure[tale_id]]
        self.add()

    def check_line(self, line):
        for column in range(self.x):
            if self.field[line][column] != '🟦':
                return False
        return True

    def remove_line(self, line_num):
        for column in range(self.x):
            self.field[line_num][column] = '🟥'

    def shift_line(self, line_num: int):
        for line in range(line_num - 1, -1, -1):
            for column in range(self.x):
                if self.field[line][column] == '🟦':
                    self.field[line][column] = '🟥'
                    self.field[line+1][column] = '🟦'

    def win(self):
        for line in range(self.y - 1, -1, -1):
            while self.check_line(line):
                self.remove_line(line)
                self.shift_line(line)

    def lose(self):
        for column in range(self.x):
            if self.field[0][column] == '🟦':
                return False
        return True

    def get_field(self) -> str:
        text = ''
        for line in self.field:
            for tile in line:
                text += tile
            text += '\n'
        return text


if __name__ == '__main__':
    f = Field()
    f.add()
    while f.lose():
        for i in f.field:
            for j in i:
                print(j, end='')
            print()
        x = int(input('Введите команду: '))
        match x:
            case 1:
                f.fly()
            case 2:
                f.move('left')
            case 3:
                f.move('right')
            case 4:
                f.rotate('right')
            case 5:
                f.rotate('left')
        f.win()

    print('Вы проиграли')

