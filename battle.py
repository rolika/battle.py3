#BattleShip game on console

import random

WAVE, VESSEL, HIT, MISS, SUNKEN = "~˛", '#', '+', 'o', '×'
SHIPS = [ \
"""
###   ###
  #####
  #####
###   ###
""",
"""
   ###
 #######
#########
""",
"""
#######
#######
#######
""",
"""
  ###
######
 ###
""" ,
"""
 ####
#######
########
#######
 ####
""",
"""
#######
#     #
#     #
#######
"""]

class Map(list):
    def __init__(self, rows = 17, columns = 40):
        super().__init__()
        self.rows, self.columns = rows, columns
        self.create_dataset()
        self.create_ocean()

    def create_dataset(self):
        """ Create rows and in each row, all the columns """
        for row in range(self.rows):
            self.append([])
            for column in range(self.columns):
                self[row].append('')

    def create_ocean(self):
        """ Fill ocean with wave symbols """
        for row in self:
            for i, column in enumerate(row):
                row[i] = random.choice(WAVE)

    def get(self, row):
        """ Return a row as string for the game board """
        return ''.join(self[row])

    def add(self, ship):
        """ Place ship on map for debug purposes """
        try:
            for coord in ship:
                self[coord[0]][coord[1]] = VESSEL
        except:
            print(ship.coords)

    def __str__(self):
        """ Map's string representation for debug purposes """
        return '\n'.join(map(lambda row: ''.join([c for c in row]), self))

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
    """ Create a ship with its coordinates """
    def __init__(self, shape): #shape is a multiline string
        super().__init__(self)
        shape = shape.strip('\n').split('\n')
        self.coords = self.get_coords(shape)

    def get_coords(self, shape):
        """ Make a list of coordinate pairs """
        coords = list()
        for x, row in enumerate(shape):
            for y, c in enumerate(row):
                if c == VESSEL:
                    coords.append([x, y])
        self.wide = len(shape) #wide & long for placing on map
        self.long = max(max(zip(*coords))) + 1
        return coords

    def check(self):
        """ Check if ship sunken - all vessel parts hit """
        return False if VESSEL in self.values() else True

class BattleShip:
    """ Main game application """
    def __init__(self):
        self.init_game()
        for ship in self.ships:
            self.ocean.add(ship)
        print(self.ocean)
        self.new_game()

    def init_game(self):
        """ Init new game """
        self.ocean = Map()
        self.board = Board(self.ocean)
        self.ships = [Ship(ship) for ship in SHIPS]
        for ship in self.ships:
            self.add(ship)
        self.torpedos = 3

    def add(self, ship):
        """ Add ship to ocean, i.e. translate its coordinates """
        while True:
            x = random.randrange(self.ocean.rows - ship.wide)
            y = random.randrange(self.ocean.columns - ship.long)
            coords =[[coord[0] + x, coord[1] + y] for coord in ship.coords]
            if not self.overlap(coords):
                for coord in coords:
                    ship[tuple(coord)] = VESSEL
                break

    def overlap(self, coords):
        """ Check coordinates already taken """
        for ship in self.ships:
            for coord in ship:
                if list(coord) in coords:
                    return True
        return False

    def new_game(self):
        """ Start new game """
        while True: #main game loop
            print("{:_^48}".format(' '.join(list("torpedó".upper()))))
            self.board.draw()
            print("{} torpedód van.".format(self.torpedos), end = " ")
            try:
                y, x = input("Add meg a célkoordinátákat 0-{} 0-{}: ". \
                   format(self.master.columns - 1, self.master.rows - 1)). \
                   split()
                x, y = int(x), int(y)
            except:
                continue #not two-part string, not integers
            if x not in range(self.master.rows) or \
               y not in range(self.master.columns):
                continue #values not in range
            print("Korrekt értékek")
            break

def test():
    s = Ship(SHIPS[4])
    print(s.coords)

if __name__ == "__main__":
    app = BattleShip()
    #test()
