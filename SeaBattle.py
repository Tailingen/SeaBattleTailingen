from random import randint

L1 = ["1", "2", "3", "4", "5", "6"]
L2 = [1, "O", "O", "O", "O", "O", "O"]
L3 = [2, "O", "O", "O", "O", "O", "O"]
L4 = [3, "O", "O", "O", "O", "O", "O"]
L5 = [4, "O", "O", "O", "O", "O", "O"]
L6 = [5, "O", "O", "O", "O", "O", "O"]
L7 = [6, "O", "O", "O", "O", "O", "O"]
Doska = [L1, L2, L3, L4, L5, L6, L7]
AIL1 = ["1", "2", "3", "4", "5", "6"]
AIL2 = [1, "O", "O", "O", "O", "O", "O"]
AIL3 = [2, "O", "O", "O", "O", "O", "O"]
AIL4 = [3, "O", "O", "O", "O", "O", "O"]
AIL5 = [4, "O", "O", "O", "O", "O", "O"]
AIL6 = [5, "O", "O", "O", "O", "O", "O"]
AIL7 = [6, "O", "O", "O", "O", "O", "O"]
AIDoska = [AIL1, AIL2, AIL3, AIL4, AIL5, AIL6, AIL7]

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Проверьте правильность ввода координат"

class BoardWrongShipException(BoardException):
    pass

class Ship:
    def __init__(self, nose, orient, long):
        self.nose = nose
        self.orient = orient
        self.long = long

    @property
    def points(self):
        ship_dots = []
        for i in range(self.long):
            cur_x = self.nose.x
            cur_y = self.nose.y

            if self.orient == 0:
                cur_x += i

            elif self.orient == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

class Player:
    def __init__(self, healt):
        self.healt = healt

Hero = Player(0)
AI = Player(0)

class Board:
    def __init__(self, dots):
        self.dots = dots

        self.check = []
        self.check2 = []

    def add_ship(self, ship):

        for d in ship.points:
            if self.out(d) or d in self.check:
                raise BoardWrongShipException()
        for d in ship.points:
            self.dots[d.x][d.y] = "■"
            self.check.append(d)

        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.points:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.check:
                    if verb:
                        self.dots[cur.x][cur.y] = "T"
                    self.check.append(cur)

    def out(self, d):
        return not((0 <= d.x <= 6) and (0 <= d.y <= 6))

    def FireAI(self):
        f = str(randint(1, 6)) + "-" + str(randint(1, 6))
        print(f)
        if f in self.check2:
            raise BoardOutException()
        if self.dots[int(f[0])][int(f[2])] == "O":
            self.dots[int(f[0])][int(f[2])] = "T"
            self.check2.append(f)
        else:
            self.dots[int(f[0])][int(f[2])] = "X"
            self.check2.append(f)
            Hero.healt -= 1
            if Hero.healt != 0:
                Show()
                BoardHero.FireAI()

    def FireHero(self):
        f = input("Координаты выстрела")
        if len(f) != 3 or f[1] != ".":
            raise BoardOutException()
        if f[0] not in ["1", "2", "3", "4", "5", "6"]:
            raise BoardOutException()
        if f[2] not in ["1", "2", "3", "4", "5", "6"]:
            raise BoardOutException()
        if f in self.check2:
            raise BoardOutException()
        if self.dots[int(f[0])][int(f[2])] == "O":
            self.dots[int(f[0])][int(f[2])] = "T"
            self.check2.append(f)
        else:
            self.dots[int(f[0])][int(f[2])] = "X"
            self.check2.append(f)
            AI.healt -= 1
            if AI.healt != 0:
                ShowCensored()
                BoardAI.FireHero()

BoardHero = Board(Doska)
BoardAI = Board(AIDoska)

def Show():
    print(" ", " ", L1, "\n", L2, "\n", L3, "\n", L4, "\n", L5, "\n", L6, "\n", L7)

def ShowCensored():
    print(" ", " ", AIL1, "\n", str(AIL2).replace("■", "O"), "\n", str(AIL3).replace("■", "O"), "\n", str(AIL4).replace("■", "O"), "\n", str(AIL5).replace("■", "O"), "\n", str(AIL6).replace("■", "O"), "\n", str(AIL7).replace("■", "O"))

def ConstAI():
    print("Компьютер расставляет корабли")
    while True:
        try:
            s11 = str(randint(1, 6)) + "-" + str(randint(1, 6))
            s12 = randint(0, 1)
            BoardAI.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), s12, 3))
            AI.healt += 3
            break
        except BoardWrongShipException:
            pass
    while True:
        try:
            s11 = str(randint(1, 6)) + "-" + str(randint(1, 6))
            s12 = randint(0, 1)
            BoardAI.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), s12, 2))
            AI.healt += 2
            break
        except BoardWrongShipException:
            pass
    while True:
        try:
            s11 = str(randint(1, 6)) + "-" + str(randint(1, 6))
            s12 = randint(0, 1)
            BoardAI.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), s12, 2))
            AI.healt += 2
            break
        except BoardWrongShipException:
            pass
    while True:
        try:
            s11 = str(randint(1, 6)) + "-" + str(randint(1, 6))
            BoardAI.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), 1, 1))
            AI.healt += 1
            break
        except BoardWrongShipException:
            pass
    while True:
        try:
            s11 = str(randint(1, 6)) + "-" + str(randint(1, 6))
            BoardAI.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), 1, 1))
            AI.healt += 1
            break
        except BoardWrongShipException:
            pass
    for i in range(1, 1000):
        try:
            s11 = str(randint(1, 6)) + "-" + str(randint(1, 6))
            BoardAI.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), 1, 1))
            AI.healt += 1
            break
        except BoardWrongShipException:
            pass
    for i in range(1, 1000):
        try:
            s11 = str(randint(1, 6)) + "-" + str(randint(1, 6))
            BoardAI.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), 1, 1))
            AI.healt += 1
            break
        except BoardWrongShipException:
            pass
    return ShowCensored()

def Const():
    print(" ", " ", L1, "\n", L2, "\n", L3, "\n", L4, "\n", L5, "\n", L6, "\n", L7)
    while True:
        print("Ставим Трёхпалубный корабль")
        try:
            while True:
                s11 = input("Введите координаты носа корабля в формате 'x.y'")
                if int(s11[0]) < 1 or int(s11[0]) > 6:
                    print("Неверный ввод")
                elif len(s11) != 3:
                    print("Неверный ввод")
                elif int(s11[2]) < 1 or int(s11[2]) > 6:
                    print("Неверный ввод")
                else:
                    break
            while True:
                s12 = input("0 - вертикальный корабль, 1 - горизонтальный корабль")
                if int(s12) == 0 or int(s12) == 1:
                    break
                else:
                    print("неверный ввод")
            BoardHero.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), int(s12), 3))
            Hero.healt += 3
            break
        except BoardWrongShipException:
            pass
    print(" ", " ", L1, "\n", L2, "\n", L3, "\n", L4, "\n", L5, "\n", L6, "\n", L7)
    while True:
        print("Ставим Двухпалубный корабль")
        try:
            while True:
                s11 = input("Введите координаты носа корабля в формате 'x.y'")
                if int(s11[0]) < 1 or int(s11[0]) > 6:
                    print("Неверный ввод")
                elif len(s11) != 3:
                    print("Неверный ввод")
                elif int(s11[2]) < 1 or int(s11[2]) > 6:
                    print("Неверный ввод")
                else:
                    break
            while True:
                s12 = input("0 - вертикальный корабль, 1 - горизонтальный корабль")
                if int(s12) == 0 or int(s12) == 1:
                    break
                else:
                    print("неверный ввод")
            BoardHero.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), int(s12), 2))
            Hero.healt += 2
            break
        except BoardWrongShipException:
            pass
    print(" ", " ", L1, "\n", L2, "\n", L3, "\n", L4, "\n", L5, "\n", L6, "\n", L7)
    while True:
        print("Ставим Двухпалубный корабль")
        try:
            while True:
                s11 = input("Введите координаты носа корабля в формате 'x.y'")
                if int(s11[0]) < 1 or int(s11[0]) > 6:
                    print("Неверный ввод")
                elif len(s11) != 3:
                    print("Неверный ввод")
                elif int(s11[2]) < 1 or int(s11[2]) > 6:
                    print("Неверный ввод")
                else:
                    break
            while True:
                s12 = input("0 - вертикальный корабль, 1 - горизонтальный корабль")
                if int(s12) == 0 or int(s12) == 1:
                    break
                else:
                    print("неверный ввод")
            BoardHero.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), int(s12), 2))
            Hero.healt += 2
            break
        except BoardWrongShipException:
            pass
    print(" ", " ", L1, "\n", L2, "\n", L3, "\n", L4, "\n", L5, "\n", L6, "\n", L7)
    while True:
        print("Ставим Однопалубный корабль")
        try:
            while True:
                s11 = input("Введите координаты корабля в формате 'x.y'")
                if int(s11[0]) < 1 or int(s11[0]) > 6:
                    print("Неверный ввод")
                elif len(s11) != 3:
                    print("Неверный ввод")
                elif int(s11[2]) < 1 or int(s11[2]) > 6:
                    print("Неверный ввод")
                else:
                    break
            BoardHero.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), 1, 1))
            Hero.healt += 1
            break
        except BoardWrongShipException:
            pass
    print(" ", " ", L1, "\n", L2, "\n", L3, "\n", L4, "\n", L5, "\n", L6, "\n", L7)
    while True:
        print("Ставим Однопалубный корабль")
        try:
            while True:
                s11 = input("Введите координаты корабля в формате 'x.y'")
                if int(s11[0]) < 1 or int(s11[0]) > 6:
                    print("Неверный ввод")
                elif len(s11) != 3:
                    print("Неверный ввод")
                elif int(s11[2]) < 1 or int(s11[2]) > 6:
                    print("Неверный ввод")
                else:
                    break
            BoardHero.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), 1, 1))
            Hero.healt += 1
            break
        except BoardWrongShipException:
            pass
    print(" ", " ", L1, "\n", L2, "\n", L3, "\n", L4, "\n", L5, "\n", L6, "\n", L7)
    for i in range(1, 6):
        print(f"Ставим Однопалубный корабль, попытка {i}/5")
        try:
            while True:
                s11 = input("Введите координаты корабля в формате 'x.y'")
                if int(s11[0]) < 1 or int(s11[0]) > 6:
                    print("Неверный ввод")
                elif len(s11) != 3:
                    print("Неверный ввод")
                elif int(s11[2]) < 1 or int(s11[2]) > 6:
                    print("Неверный ввод")
                else:
                    break
            BoardHero.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), 1, 1))
            Hero.healt += 1
            break
        except BoardWrongShipException:
            pass
    print(" ", " ", L1, "\n", L2, "\n", L3, "\n", L4, "\n", L5, "\n", L6, "\n", L7)
    for i in range(1, 6):
        print(f"Ставим Однопалубный корабль, попытка {i}/5")
        try:
            while True:
                s11 = input("Введите координаты корабля в формате 'x.y'")
                if int(s11[0]) < 1 or int(s11[0]) > 6:
                    print("Неверный ввод")
                elif len(s11) != 3:
                    print("Неверный ввод")
                elif int(s11[2]) < 1 or int(s11[2]) > 6:
                    print("Неверный ввод")
                else:
                    break
            BoardHero.add_ship(Ship(Dot(int(s11[0]), int(s11[2])), 1, 1))
            Hero.healt += 1
            break
        except BoardWrongShipException:
            pass
    return Show()

def Play():
    print("Начало игры")
    print("Расстановка кораблей")
    c = Const()
    print(c)
    ca = ConstAI()
    print(ca)
    while True:
        while True:
            try:
                print("Ход игрока")
                ShowCensored()
                BoardAI.FireHero()
                ShowCensored()
                break
            except BoardOutException:
                print("Проверьте правильность написания координат")
                pass
        if AI.healt == 0:
            print("Игрок победил")
            break
        print("Ход компьютера")
        Show()
        while True:
            try:
                BoardHero.FireAI()
                break
            except BoardOutException:
                print("Компьютер делает ход")
                pass
        Show()
        if Hero.healt == 0:
            print("Компьютер победил")
            break

p = Play()
print(p)
