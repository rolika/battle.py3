#BattleShip game on console

import random

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
INTACT, HIT, MISS, SUNKEN = '#', '+', 'o', '×'

class Ocean(list):
    """ Create the ocean """
    def __init__(self, rows = 20, columns = 40):
        super().__init__(self)
        self.rows, self.columns = rows, columns
        self.bounds = list() #list of ships upper left & lower right coordinates
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

    def addShips(self, ships):
        """ Randomly place ships in ocean """
        for ship in ships:
            ship.set(self.getCoord())

    def getCoord(self, wide, long):
        """ Return appropriate coordinates for ship """
        new = False
        while not new:
            new = True
            x = random.randrange(self.columns - long)
            y = random.randrange(self.rows - wide)
            for bound in self.bounds:
                if x in range(x, x + long) and y in range(y, y + wide):
                    new = False            
        return x, y

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
        self.newGame()

    def initGame(self):
        """ Init new game """
        self.ocean = Ocean()
        self.board = Board(self.ocean)
        self.ships = [Ship(ship) for ship in SHIPS]
        self.ocean.addShips(self.ships)

    def newGame(self):
        """ Start new game """
        print("{:_^48}".format("_".join(list("torpedó".upper()))))
        self.board.draw()
        print(self.ships[0].wide, self.ships[0].long)
        
app = BattleShip()
