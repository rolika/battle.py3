#! /usr/bin/env python3
#BattleShip game on console

import random

WIDTH = 80 #terminal window character width
WAVE, VESSEL, HIT, MISS = "~˛", '#', 'X', 'O'
SHIPS = [ \
"""
 #
###
 #
""",
"""
##
##
""",
"""
###
""",
"""
#
#
#
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
        for coord in ship:
                self[coord[0]][coord[1]] = VESSEL

    def __str__(self):
        """ Map's string representation for debug purposes """
        return '\n'.join(map(lambda row: ''.join([c for c in row]), self))

class Board:
    """ Create game board based on ocean """
    def __init__(self, ocean): #takes ocean as object
        self._ocean = ocean
        self._full_row = "{}{:>2} {} {}" #left row-num, ocean-row, right row-num
        self._horizontal_nums = \
            ''.join([str(num % 10) for num in range(self._ocean.columns)])
        self._horizontal_tens = (' ' * 9).join([str(num) \
                                for num in range(self._ocean.columns // 10)])
        self.offset = " " * ((WIDTH - self._ocean.columns - 6) // 2)

    def draw(self):
        """ Draw board with coordinates around """
        print(self._full_row.format(self.offset, "", self._horizontal_tens, ""))
        print(self._full_row.format(self.offset, "", self._horizontal_nums, ""))
        for row in range(self._ocean.rows):
            print(self._full_row.format(self.offset,
                                        row, self._ocean.get(row), row))
        print(self._full_row.format(self.offset, "", self._horizontal_nums, ""))
        print(self._full_row.format(self.offset, "", self._horizontal_tens, ""))

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
        self.long = max(max(zip(*coords))) + 1 #highest number in a list of lists
        return coords

class BattleShip:
    """ Main game application """
    def __init__(self):
        self.init_game()
##        for ship in self.ships: #debug
##            self.ocean.add(ship)
        self.new_game()

    def init_game(self):
        """ Init new game """
        self.ocean = Map(10, 10)
        self.board = Board(self.ocean)
        self.torpedos = 0
        self.ships = [Ship(ship) for ship in SHIPS]
        for ship in self.ships:
            self.add(ship)
            self.torpedos += len(ship)
        self.message = "{} hajó van az óceánon.".format(len(self.ships))
        self.torpedos *= 2 #all ship-parts × 2

    def add(self, ship):
        """ Add ship to ocean randomly, i.e. translate its coordinates """
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

    def ask(self):
        """ Ask for coordinates and validate entry """
        while True:
            coords = input("Add meg a célkoordinátákat 0-{} 0-{}: ".\
                           format(self.ocean.columns - 1,
                                  self.ocean.rows - 1))
            if "vége" in coords:
                quit("Vége a játéknak.")
            coords = coords.split()
            if len(coords) != 2:
                print("Két koordinátát kérek!")
                continue
            try:
                x, y = int(coords[1]), int(coords[0])
            except:
                print("Két pozitív egész számot kérek!")
                continue
            break
        return x, y
        
    def new_game(self):
        """ Start new game """
        while True: #main game loop
            print("{:_^80}".format(' '.join(list("torpedó".upper()))))
            self.board.draw()
            print("{} {} torpedód van.".format(self.message, self.torpedos))
            if not self.torpedos:
                break
            x, y = self.ask()
            if x not in range(self.ocean.rows) or \
               y not in range(self.ocean.columns):
                self.message = "A torpedó az óceánon kívül csapódna be..."
                continue #values not in range
            self.torpedos -= 1
            try:
                ship = next(filter(lambda ship:\
                                   ship.get((x, y), False) == VESSEL,
                                   self.ships))
            except:
                ship = False
            if ship:
                ship[(x, y)] = self.ocean[x][y] = HIT #mark both as hit
                self.message = "Eltaláltál egy hajót!"
                if VESSEL not in ship.values(): #no intact part left
                    self.message = "Elsüllyesztetted az egész hajót!"
                    self.ships.remove(ship)
            elif self.ocean[x][y] in WAVE:
                self.message = "Nem talált!"
                self.ocean[x][y] = MISS
            elif self.ocean[x][y] == HIT:
                self.message = "Itt már meglőttél egy hajót!"
            elif self.ocean[x][y] == MISS:
                self.message = "Itt már az előbb sem volt semmi..."
            continue
            if len(self.ships) == 0:
                self.board.draw()
                print("Gratulálok, az összes hajót elsüllyesztetted!")
            elif self.torpedos < 0:
                print("Nincs több torpedód!")
            break
        print("Vége a játéknak.")

def main():
    game = BattleShip()

if __name__ == "__main__":
    main()
