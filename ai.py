from pieces import Piece
from bag import Bag
from board import Board
import copy

class AI(object):
    def __init__(self, board, bag, next_piece, depth=16):
        self.board = copy.deepcopy(board)
        self.bag = copy.deepcopy(bag)
        self.piece = copy.deepcopy(next_piece)

    def checkIfWinAt(self, X, Y):
        if X < 0 or X > 3 or Y < 0 or Y > 3:
            raise IndexError

        # Trying to put the piece where there already is one; in that case,
        # just check to see if the board is already a winner.
        #
        # TODO: Is this the best way to handle this?
        if self.board.data[X][Y] is not None:
            return self.board.hasWon()

        self.board.placePiece(self.piece, X, Y)
        out = self.board.hasWon()
        self.board.removePiece(X, Y)
        return out

    def nextMove(self):
        # This checks if it can win on the next move with the current piece.
        for x, y in self.board.emptyTiles():
            if self.checkIfWinAt(x,y):
                return (x, y)
            else:
                P, bag = self.nextPiece(B, self.bag)

        return None

    @staticmethod
    def nextPiece(self, board, bag):
        return None, None

if __name__ == "__main__":
    ai = AI(Board(), Bag(), Piece(1,1,1,1))

    ai.board.placePiece(Piece(1,1,1,1), 0, 0)
    print(ai.nextMove())
    ai.board.placePiece(Piece(1,1,1,1), 0, 1)
    print(ai.nextMove())
    ai.board.placePiece(Piece(1,1,1,1), 0, 2)
    print(ai.nextMove())
