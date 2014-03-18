import random
import math

class Board():
    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

    def __init__(self, azmode=False):
        self.__size = 4
        self.__goal = 2048
        self.__won = False
        self.__azmode = False
        self.__score = 0
        self.__nummoves = 0
        self.cells = [[0]*self.__size for _ in xrange(self.__size)]
        self.addTile()
        self.addTile()


    def __str__(self):
        """
        return a string representation of the current board.
        """
        rg = xrange(self.size())
        s = '\n'.join([' '.join([self.getCellStr(x, y) for x in rg]) for y in rg])
        return s + '\n'

    def size(self):
        """return the board size"""
        return self.__size

    def score(self):
        """return the current score"""
        return self.__score

    def numMoves(self):
        """return the number of moves made so far"""
        return self.__nummoves

    def goal(self):
        """return the board goal"""
        return self.__goal

    def won(self):
        """
        return True if the board contains at least one tile with the board goal, False otherwise
        """
        return self.__won

    def canMove(self):
        """
        return True if there are any possible moves, or False otherwise
        """
        if not self.filled():
            return True

        for y in xrange(0, self.__size):
            for x in xrange(0, self.__size):
                c = self.getCell(x, y)
                if (x < self.__size-1 and c == self.getCell(x+1, y)) or (y < self.__size-1 and c == self.getCell(x, y+1)):
                    return True

        return False

    def filled(self):
        """
        return True if the board is filled
        """
        return len(self.getEmptyCells()) == 0

    def addTile(self, choices=([2]*9+[4])):
        """
        add a random tile in an empty cell
          choices: a list of possible choices for the value of the tile.
                   default is [2, 2, 2, 2, 2, 2, 2, 2, 2, 4].
        """
        v = random.choice(choices)
        empty = self.getEmptyCells()
        if empty:
            x, y = random.choice(empty)
            self.setCell(x, y, v)

    def getCell(self, x, y):
        """return the cell value at x,y"""
        return self.cells[y][x]

    def getCellStr(self, x, y):
        """
        return a string representation of the cell located at x,y.
        """
        c = self.getCell(x, y)

        az = {}
        for i in range(1, int(math.log(self.goal(), 2))):
            az[2**i] = chr(i+96)

        if c == 0 and self.__azmode:
            return '.'
        elif c == 0:
            return '  .'

        elif self.__azmode:
            if c not in az:
                return '?'
            s = az[c]
        elif c == 1024:
            s = ' 1k'
        elif c == 2048:
            s = ' 2k'
        else:
            s = '%3d' % c

        return s

    def setCell(self, x, y, v):
        """set the cell value at x,y"""
        self.cells[y][x] = v

    def getLine(self, y):
        """return the y-th line, starting at 0"""
        return [self.getCell(i, y) for i in xrange(0, self.__size)]

    def getCol(self, x):
        """return the x-th column, starting at 0"""
        return [self.getCell(x, i) for i in xrange(0, self.__size)]

    def setLine(self, y, l):
        """set the y-th line, starting at 0"""
        for i in xrange(0, self.__size):
            self.setCell(i, y, l[i])

    def setCol(self, x, l):
        """set the x-th column, starting at 0"""
        for i in xrange(0, self.__size):
            self.setCell(x, i, l[i])

    def getEmptyCells(self):
        """return a (x, y) pair for each cell"""
        return [(x, y) for x in xrange(self.__size) for y in xrange(self.__size) if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line, d):
        """
        Merge tiles in a line or column according to a direction and return a
        tuple with the new line and the score for the move on this line
        """
        if (d == Board.LEFT or d == Board.UP):
            inc = 1
            rg = xrange(0, self.__size-1, inc)
        else:
            inc = -1
            rg = xrange(self.__size-1, 0, inc)

        pts = 0
        for i in rg:
            if line[i] == 0:
                continue
            if line[i] == line[i+inc]:
                v = line[i]*2
                if v == self.__goal:
                    self.__won = True

                line[i] = v
                line[i+inc] = 0
                pts += v

        return (line, pts)

    def __moveLineOrCol(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == Board.UP or d == Board.LEFT:
            return nl + [0] * (self.__size - len(nl))
        return [0] * (self.__size - len(nl)) + nl

    def move(self, d, add_tile=True):
        """
        move and return the move score
        """
        if d == Board.LEFT or d == Board.RIGHT:
            chg, get = self.setLine, self.getLine
        elif d == Board.UP or d == Board.DOWN:
            chg, get = self.setCol, self.getCol
        else:
            return 0

        moved = False
        score = 0

        for i in xrange(0, self.__size):
            origin = get(i)
            line = self.__moveLineOrCol(origin, d)
            collapsed, pts = self.__collapseLineOrCol(line, d)
            new = self.__moveLineOrCol(collapsed, d)
            chg(i, new)
            if origin != new:
                moved = True
            score += pts

        if moved and add_tile:
            self.addTile()

        self.__score += score
        self.__nummoves += 1

def AIRandomMove():
    return random.choice([1, 2, 3, 4])

def AITest(rounds=1000):
    scores = []
    moves = []

    wins = 0
    for _ in range(10):
        for _ in range(rounds):
            a = Board()
            while a.canMove():
                movetomake = AIRandomMove()
                a.move(movetomake)
            if a.won():
                wins += 1
            scores.append(a.score())
            moves.append(a.numMoves())

        print 'score: ' + str(sum(scores)/float(len(scores)))
        print 'moves: ' + str(sum(moves)/float(len(moves)))
        print 'wins: ' + str(wins)
        print 'win percentage: ' + str(float(wins)/float(rounds)*100) + '%'
        print '\n'

AITest(1000)