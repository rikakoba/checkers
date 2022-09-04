def check_kill(field, i, g, kill, enemy, p, dict_kill: dict, prev: list):
    direction = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    try:
        direction.remove(p)
    except:
        pass
    for d in direction:
        if 0 <= i + d[1] < 8 and 0 <= g + d[0] < 8:
            if field[i + d[1]][g + d[0]] == enemy or field[i + d[1]][g + d[0]] == enemy + "k":
                if 0 <= i + d[1] * 2 < 8 and 0 <= g + d[0] * 2 < 8:
                    if field[i + d[1] * 2][g + d[0] * 2] == "-":
                        data = (i + d[1], g + d[0])
                        prev.append(data)
                        kill.append((i + d[1] * 2, g + d[0] * 2))
                        dict_kill.setdefault((i + d[1] * 2, g + d[0] * 2), prev.copy())
                        check_kill(field, i + d[1] * 2, g + d[0] * 2, kill, enemy, (d[0] * -1, d[1] * -1), dict_kill, prev)
                        prev.remove(data)


class Checker:
    def __init__(self, i, g, enemy):
        self.dict_kill = {}
        self.i = i
        self.g = g
        self.enemy = enemy
        self.pos = []
        self.kill = []

    def move(self, field, i, g):
        field[i][g] = field[self.i][self.g]
        field[self.i][self.g] = "-"
        self.i = i
        self.g = g

    def check(self, field):
        self.pos.clear()
        self.kill.clear()
        self.dict_kill.clear()
        if self.enemy == "r":
            direction = [(-1, 1), (1, 1)]
        else:
            direction = [(-1, -1), (1, -1)]
        for d in direction:
            if 0 <= self.i + d[1] < 8 and 0 <= self.g + d[0] < 8:
                if field[self.i + d[1]][self.g + d[0]] == "-":
                    self.pos.append((self.i + d[1], self.g + d[0]))
                elif field[self.i + d[1]][self.g + d[0]] == self.enemy or field[self.i + d[1]][self.g + d[0]] == self.enemy + "k":
                    check_kill(field, self.i, self.g, self.kill, self.enemy, (None, None), self.dict_kill, [])


class Checker_king(Checker):
    def check_kill(self, field, point, prev_list: list, prev):
        direction = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        try:
            direction.remove(prev)
        except:
            pass
        for d in direction:
            for i in range(1, 8):
                if 0 <= point[0] + d[0] * i < 8 and 0 <= point[1] + d[1] * i < 8:
                    if field[point[0] + d[0] * i][point[1] + d[1] * i] == self.enemy or field[point[0] + d[0] * i][point[1] + d[1] * i] == self.enemy + "k":
                        for k in range(i + 1, 8):
                            if 0 <= point[0] + d[0] * k < 8 and 0 <= point[1] + d[1] * k < 8:
                                if field[point[0] + d[0] * k][point[1] + d[1] * k] != "-":
                                    break
                                prev_list.append((point[0] + d[0] * i, point[1] + d[1] * i))
                                self.dict_kill.setdefault((point[0] + d[0] * k, point[1] + d[1] * k), prev_list.copy())
                                self.check_kill(field, (point[0] + d[0] * k, point[1] + d[1] * k), prev_list, (-d[0], -d[1]))
                                prev_list.remove((point[0] + d[0] * i, point[1] + d[1] * i))

    def check(self, field):
        self.pos.clear()
        self.dict_kill.clear()
        direction = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for d in direction:
            i = 1
            while i <= 8:
                if 0 <= self.i + d[1] * i < 8 and 0 <= self.g + d[0] * i < 8:
                    if field[self.i + d[1] * i][self.g + d[0] * i] == self.enemy:
                        break
                    if field[self.i + d[1] * i][self.g + d[0] * i] == "-":
                        self.pos.append((self.i + d[1] * i, self.g + d[0] * i))
                i += 1
        self.check_kill(field, (self.i, self.g), [], [])