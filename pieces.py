from tools import EMPTY_POSITION


class Piece:
    """Definition of a game piece by 4 characteristics:
    - RoundShape [True/False]
    - BigSize [True/False]
    - LightColor [True/False]
    - TopHole [True/False]"""

    def __init__(self, id=1, round_shape=False, big_size=False, light_color=False, top_hole=False):
        self.round_shape = round_shape
        self.big_size = big_size
        self.light_color = light_color
        self.top_hole = top_hole
        self.highlight = False
        self.id = id

    def __str__(self):
        out = ""
        out += "Round, " if self.round_shape else "Square, "
        out += "Tall, " if self.big_size else "Short, "
        out += "Light Brown, "if self.light_color else "Dark Brown, "
        out += "and Concave" if self.top_hole else "and Flat"
        return out

    def __link(self,*args):
        result = ""
        for i in args:
            result += str(int(i))
        return int(result,2)

    def parse(self):
        out = ""
        out += "round " if self.round_shape else ""
        out += "tall " if self.big_size else ""
        out += "" if self.light_color else "dark "
        out += "hole" if self.top_hole else ""
        return out

    def type(self):
        return self.__link(self.round_shape, self.big_size, self.light_color, self.top_hole)
    def validate(self):
        return (int(self.round_shape), int(self.big_size), int(self.light_color), int(self.top_hole))

def makeAPiecefromString(id,string):
    if len(string) != 4:
        raise Exception("The length of the string must be 4")
    round_shape = bool(int(string[0]))
    big_size = bool(int(string[1]))
    light_color = bool(int(string[2]))
    top_hole = bool(int(string[3]))
    return Piece(id, round_shape=round_shape, big_size=big_size, light_color=light_color, top_hole=top_hole)

pieces_list_definition = [
        Piece(1, round_shape= False, big_size= False, light_color= False, top_hole= False),
        Piece(2, round_shape= True, big_size= False, light_color= False, top_hole= False),
        Piece(3, round_shape= False, big_size= True, light_color= False, top_hole= False),
        Piece(4, round_shape= True, big_size= True, light_color= False, top_hole= False),
        Piece(5, round_shape= False, big_size= False, light_color= False, top_hole= True),
        Piece(6, round_shape= True, big_size= False, light_color= False, top_hole= True),
        Piece(7, round_shape= False, big_size= True, light_color= False, top_hole= True),
        Piece(8, round_shape= True, big_size= True, light_color= False, top_hole= True),
        Piece(9, round_shape=False, big_size=False, light_color=True, top_hole=False),
        Piece(10, round_shape=True, big_size=False, light_color=True, top_hole=False),
        Piece(11, round_shape=False, big_size=True, light_color=True, top_hole=False),
        Piece(12, round_shape=True, big_size=True, light_color=True, top_hole=False),
        Piece(13, round_shape= False, big_size= False, light_color= True, top_hole= True),
        Piece(14, round_shape= True, big_size= False, light_color= True, top_hole= True),
        Piece(15, round_shape= False, big_size= True, light_color= True, top_hole= True),
        Piece(16, round_shape= True, big_size= True, light_color= True, top_hole= True)
    ]

if __name__ == "__main__":
    for piece in pieces_list_definition:
        print(piece.type())
        print(piece.validate())