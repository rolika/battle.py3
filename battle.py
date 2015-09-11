#BattleShip game on console

import random

class Ocean(list):
    """ Create the ocean """
    def __init__(self, rows = 20, columns = 40):
        super().__init__(self)
        self.rows, self.columns = rows, columns
        self._create()

    def _create(self):
        """ Create data field, a list of lists """
        for row in range(self.rows):
            self.append([])
            for column in range(self.columns):
                self[row].append([])
                self[row][column] = random.choice("~˛") #AltGr+1, AltGr+6

    def get(self, row):
        """ Return row of ocean as string """
        return ''.join(self[row])

class Board:
    """ Create game board based on ocean """
    def __init__(self, ocean): #takes ocean as object
        self._ocean = ocean
        self._full_row = " {:>2} {} {}" #left row-num, ocean-row, right row-num
        self._horizontal_nums = \
            ''.join([str(num % 10) for num in range(ocean.columns)])
        self._horizontal_tens = \
            (' ' * 9).join([str(num) for num in range(ocean.columns // 10)])
        self.draw()

    def draw(self):
        """ Draw board with coordinates around """
        print(self._full_row.format("", self._horizontal_tens, ""))
        print(self._full_row.format("", self._horizontal_nums, ""))
        for row in range(self._ocean.rows):
            print(self._full_row.format(row, self._ocean.get(row), row))
        print(self._full_row.format("", self._horizontal_nums, ""))
        print(self._full_row.format("", self._horizontal_tens, ""))

class Ship:
    """ Create a ship """
    def __init__(self, shape): #shape is a multiline string
        self.shape = shape.strip('\n').split('\n')
        self.rows, self.longest = len(self.shape), len(max(self.shape))
        self._extendShort()

    def _extendShort(self):
        """ Extend shorter rows with spaces to equal longest """
        for i in range(self.rows):
            self.shape[i] += " " * (self.longest - len(self.shape[i]))
            
    def getCoords(self):
        """ Return relative coordinates of shape """
        coords = []
        for y, row in enumerate(self.shape):
            for x, c in enumerate(row):
                if c == "#":
                    coords.append((x, y))
        return coords

ocean = Ocean()
board = Board(ocean)
s = """
  ###
######
 ###
"""
ship = Ship(s)
print(ship.getCoords())
