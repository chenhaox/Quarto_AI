from pieces import pieces_list_definition
import copy
class FullSquareException(Exception):
    def __init__(self,msg):
        self.msg = msg

class SizeException(Exception):
    def __init__(self, size):
        self.size = size


class Board(object):
    def __init__(self):
        self.data = [[None for i in range(4)] for j in range(4)]
        self.datacopy = copy.deepcopy(self.data)


    def placePiece(self, whichPiece, X, Y):
        if X > 3 or X < 0 or Y > 3 or Y < 0:
            raise IndexError
        if self.data[X][Y] is not None:
            raise FullSquareException(str((X,Y))+" has already be occupied")
        self.data[X][Y] = whichPiece

    def removePiece(self, X, Y):
        if X > 3 or X < 0 or Y > 3 or Y < 0:
            raise IndexError

        self.data[X][Y] = None

    def isWon(self):
        rows = [self.__check(self.data[i]) for i in range(4)]
        cols = [self.__check([self.data[j][i] for j in range(4)]) for i in range(4)]
        diag = self.__check([self.data[i][i] for i in range(4)])
        antidiag = self.__check([self.data[i][3 - i] for i in range(4)])

        return any(rows) or any(cols) or diag or antidiag

    def __check(self, group):
        if len(group) != 4:
            raise SizeException(len(group))

        if None in group:
            return False

        result1 = None
        result2 = None
        for piece in group:
            result1 = piece.type() if result1 is None else result1 & piece.type()
            result2 = piece.type() ^ 15 if result2 is None else result2 & (piece.type() ^ 15)
        print(result1)
        print(result2)
        if result1 > 0 or result2>0:
            for piece in group:
                piece.highlight = True
            return True
        else:
            return False

    def parseDict(self,dict = {}):
        """
        parse the dictionary
        :param dict: {(x,y):piece}
        :return: none
        """

        self.data = copy.deepcopy(self.datacopy)
        for key,value in dict.items():
            self.placePiece(value,*key)

    def isFull(self):
        for x in range(4):
            for y in range(4):
                if self.data[x][y] is None:
                    return False
        return True

    def validateBoard(self):
        counter = 0
        data = []
        namelist = ["A","B","C","D","E","F","G","H"]
        for row in self.data:
            rowlist = []
            for col in row:
                value = col if col is not None else None
                rowlist.append(value)
            data.append(rowlist)
            counter += 1
        return data

    def emptyTiles(self):
        out = []
        for i in range(4):
            for j in range(4):
                if self.data[i][j] is None:
                    out.append((i, j))
        return out

    def Pieces(self):
        out = []
        for i in range(4):
            for j in range(4):
                if self.data[i][j] is not None:
                    out.append((self.data[i][j], i, j))
        return out

    def parseOutput(self):
        out = []
        for i in range(4):
            tmp = []
            for j in range(4):
                if self.data[i][j] is None:
                    tmp.append("")
                if self.data[i][j] is not None:
                    print(self.data[i][j])
                    tmp.append("{:04b}".format(self.data[i][j].type()))
            out.append(tmp)
        return out

    def getState(self):
        state = None
        if self.isWon():
            state = 1
        elif self.isFull():
            state = 0
        return state

if __name__ == "__main__":
    test = Board()
    test.placePiece(pieces_list_definition[0],0,0)
    test.placePiece(pieces_list_definition[2], 0, 1)
    test.placePiece(pieces_list_definition[4], 0, 2)
    test.placePiece(pieces_list_definition[8], 2, 3)
    print(test.isWon())