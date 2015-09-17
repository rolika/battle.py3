#BattleShip game on console

import random

WAVE, VESSEL, HIT, MISS, SUNKEN = "~˛", '#', '+', 'o', '×'
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
""" ,
"""
 ####
##  ###
##   ###
##  ###
 ####
"""]

class Map(list):
    """ Base class to create a list of list holding the maps for:
        - ocean representing game field
        - master map holding the ships position """
    def __init__(self, rows = 17, columns = 40):
        super().__init__()
        self.rows, self.columns = rows, columns
        for row in range(rows):
            self.append([])
            for column in range(columns):
                self[row].append(' ') #needs to be space, not empty string
                
    def __str__(self):
        """ Map's string representation for debug purposes """
        return '\n'.join(map(lambda row: ''.join([c for c in row]), self))

class Ocean(Map):
    """ Create the ocean, ie. the actual game board to display """
    def __init__(self):
        super().__init__()
        for row in self:
            for i, column in enumerate(row):
                row[i] = random.choice(WAVE)

    def get(self, row):
        """ Return row of ocean as string """
        return ''.join(self[row])

class Master(Map):
    """ Master map containing ships """
    def __init__(self):
        super().__init__()

    def add(self, ship, x, y):
        """ Place ship on master map at given coordinates """
        for sx, sy in ship:
            self[sy + y][sx + x] = VESSEL

    def empty(self, ship, x, y):
        """ Check if ship can placed there """
        for sx, sy in ship:
            if self[sy + y][sx + x] == VESSEL:
                return False
        return True

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

class Ship(list):
    """ Create a ship with its relative coordinates """
    def __init__(self, shape): #shape is a multiline string
        super().__init__(self)
        self._shape = shape.strip('\n').split('\n')
        for y, row in enumerate(self._shape): #get coords of ship-tiles
            for x, c in enumerate(row):
                if c == VESSEL:
                    self.append((x, y))
        self.wide = len(self._shape) #wide & long for placing on map
        self.long = max(self)[0]
        self.count = len(self) #hits to sink ship

class BattleShip:
    """ Main game application """
    def __init__(self):
        self.initGame()
        self.newGame()

    def initGame(self):
        """ Init new game """
        self.ocean = Ocean()
        self.master = Master()
        self.board = Board(self.ocean)
        self.ships = [Ship(ship) for ship in SHIPS]        
        for ship in self.ships: #add ships to master map
            while True:
                x = random.randrange(self.master.columns - ship.long)
                y = random.randrange(self.master.rows - ship.wide)
                if self.master.empty(ship, x, y):
                    break
            self.master.add(ship, x, y)
        self.torpedos = sum([ship.count for ship in self.ships]) * 3

    def newGame(self):
        """ Start new game """
        print("{:_^48}".format(' '.join(list("torpedó".upper()))))
        while self.torpedos:
            self.board.draw()
            print("{} torpedód van.".format(self.torpedos), end = " ")
            try:
                x, y = input("Add meg a célkoordinátákat 0-{} 0-{}: ". \
                   format(self.master.columns - 1, self.master.rows - 1)). \
                   split()
                x, y = int(x), int(y)
            except:
                continue #not two-part string, not integers
            if x not in range(self.master.columns) or \
               y not in range(self.master.rows):
                continue #values not in range
            print("Korrekt értékek")
            break

if __name__ == "__main__":
    app = BattleShip()
