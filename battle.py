#BattleShip game on console

import random

WAVE, INTACT, HIT, MISS, SUNKEN = "~˛", '#', '+', 'o', '×'
SHIPS = [ \
"""
###   ###
   ###
   ###
###   ###
""",
"""
   ###
 #######
#########
""",
"""
#####
#####
#####
""",
"""
  ###
######
 ###
""" ]

class Map(list):
    """ Base class to create a list of list holding the maps for:
        - ocean representing game field
        - master map holding the ships position """
    def __init__(self, rows = 20, columns = 40):
        super().__init__()
        self.rows, self.columns = rows, columns
        for row in range(rows):
            self.append([])
            for column in range(columns):
                self[row].append('')

class Ocean(Map):
    """ Create the ocean, ie. the actual game board to display """
    def __init__(self):
        super().__init__()
        for row in self:
            for i, column in enumerate(row):
                row[i] = random.choice(WAVE)

    def __str__(self):
        """ Map's string representation for debug purposes """
        return '\n'.join([self.get(row) for row in range(len(self))])
        #return '\n'.join(map(lambda row: ''.join([c for c in row]), self))

    def get(self, row):
        """ Return row of ocean as string """
        return ''.join(self[row])

class Master(Map):
    """ Master map containing ships """
    def __init__(self):
        super().__init__()

    def __str__(self):
        """ Map's string representation for debug purposes """
        return '\n'.join(map(lambda lst: ''.join([l[0] for l in lst]), self))

    def add(self, ship, x, y):
        """ Place ship on master map at given coordinates """
        for sx, sy in ship:
            self[x + sx][y + sy] = ship[(sx, sy)]

class Board:
    """ Create game board based on ocean """
    def __init__(self, ocean): #takes ocean as object
        self._ocean = ocean
        self._full_row = " {:>2} {} {}" #left row-num, ocean-row, right row-num
        self._horizontal_nums = \
            ''.join([str(num % 10) for num in range(ocean.columns)])
        self._horizontal_tens = \
            (' ' * 9).join([str(num) for num in range(ocean.columns // 10)])

    def draw(self):
        """ Draw board with coordinates around """
        print(self._full_row.format("", self._horizontal_tens, ""))
        print(self._full_row.format("", self._horizontal_nums, ""))
        for row in range(self._ocean.rows):
            print(self._full_row.format(row, self._ocean.get(row), row))
        print(self._full_row.format("", self._horizontal_nums, ""))
        print(self._full_row.format("", self._horizontal_tens, ""))

class Ship(dict):
    """ Create a ship """
    def __init__(self, shape): #shape is a multiline string
        super().__init__(self)
        self._shape = shape.strip('\n').split('\n')
        self._coords = list()
        for y, row in enumerate(self._shape): #get coords of ship-tiles
            for x, c in enumerate(row):
                if c == "#":
                    self._coords.append([x, y])
        self.wide = len(self._shape)
        self.long = max(self._coords)[0]

    def set(self, x, y):
        """ Set intact ship to given coordinates on ocean """
        for sx, sy in self._coords:
            self[(sx + x, sy + y)] = INTACT

    def hit(self, x, y):
        """ Ship-tile hit by torpedo """
        self[(x, y)] = HIT

    def sunken(self):
        """ Check and redraw sunken ship """
        for coord in self:
            if self[coord] == INTACT: #at least one intact tile
                return False
        for coord in self: #else redraw
            self[coord] = SUNKEN
        return True

class BattleShip:
    """ Main game application """
    def __init__(self):
        self.initGame()
        #self.newGame()

    def initGame(self):
        """ Init new game """
        self.ocean = Ocean()
        print(self.ocean)
##        print(self.ocean[0][0][0])
##        self.master = Master()
##        self.board = Board(self.ocean)
##        self.ships = [Ship(ship) for ship in SHIPS]
##        self.master.add(self.ships[0], 0, 0)
##        print(self.master)

    def newGame(self):
        """ Start new game """
        print("{:_^48}".format(' '.join(list(" torpedó ".upper()))))
        self.board.draw()

app = BattleShip()
