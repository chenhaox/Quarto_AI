import board
import string
import random
import copy
import bag
from minimax import AI
# Game states
_OPEN = 0
_PLAYING = 1
_FINISHED = 2

class GameError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message):
        self.message = message

class GameValueError(GameError):
    """Raised when invalid values or parameters are passed to the module."""
    code = 400

class GamePlayError(GameError):
    """Raised when an forbidden or invalid action is attempted."""
    code = 403

class GameNotFound(GameError):
    """Raised when a non-extistent game is requested."""
    code = 404

def random_string(N):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(N))

class GameList():
    def __init__(self):
        self.gamelist ={}
        self.allownumberofonlineplayer = 5

    def new_game(self):
        if len(self.gamelist)>= self.allownumberofonlineplayer-1:
            return None
        game_id = random_string(8)
        while game_id in self.gamelist:
            game_id = random_string(8)
        self.gamelist[game_id] = Game()
        self.gamelist[game_id].start_game()
        return game_id

class Game(object):
    def __init__(self):
        self.state = _OPEN
        self.winner = None
        self.board = board.Board()
        self.remaining = bag.Bag()
        self.next_piece = None
        self.active_player = None
        self.AI = AI()

    def start_game(self):
        self.state = _PLAYING
        self.active_player = 1

    def play_validate(self):
        if self.state < _PLAYING:
            raise GamePlayError('The game has not started.');
        if self.state > _PLAYING:
            raise GamePlayError('The game is finished.');

    def select_next(self, *args):
        if self.next_piece != None:
            raise GamePlayError('The current piece must be placed first.')
        if isinstance(args[0],tuple):
            args = args[0]
        try:
            piece = self.remaining.remove(args)
        except ValueError:
            raise GamePlayError('This piece is not remaining.');
        self.next_piece = piece
        # Other player's turn.
        self.active_player = 0 if self.active_player == 1 else 1

    def place_piece(self, coordinates):
        if self.next_piece == None:
            raise GamePlayError('Next piece is not selected.')
        x = coordinates[0]
        y = coordinates[1]
        try:
            self.board.placePiece(self.next_piece,x,y)
            self.next_piece = None
            if self.board.isWon():
                self.state = _FINISHED
                self.winner = self.active_player
            elif self.board.isFull():
                self.state = _FINISHED
        except Exception as e:
            raise Exception(e)

    def AI_place(self):
        print("Calculating")
        result = self.AI.getNext(board=self.board,bag=self.remaining,next_piece=self.next_piece)
        next_piece = result.next_piece
        coordinate = result.coordinate
        print("The result is",result.next_piece.validate(),result.coordinate)
        self.place_piece(coordinate)
        self.select_next(next_piece.validate())
        print("The next_piece is",self.next_piece)

    def get_state(self):
        return {
            'state': ['open', 'playing', 'finished'][self.state],
            'active_player': self.active_player,
            'winner': self.winner,
            'board': self.board.validateBoard(),
            'remaining': self.remaining.validate_bag(),
            'next_piece': None if self.next_piece is None else self.next_piece,
        }

if __name__ == "__main__":
    game = Game()
    game.start_game()
    print(game.play_validate())
    game.select_next(1,0,0,1)
    print(game.get_state())