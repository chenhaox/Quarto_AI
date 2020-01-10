
class Node():
    def __init__(self, coordinate, next_piece, player):
        self.coordinate = coordinate
        self.next_piece = next_piece
        self.player = player
        self.children = []
        self.isleaf = True
        self.isquarto = False

    def addChild(self,node):
        self.children.append(node)
        self.isleaf = False

    def __str__(self):
        out = "<"+ str(self.coordinate) + "," + str(self.next_piece) + "," + str(self.player)
        if (self.isquarto):
            out += ",Q!"
        out += ">"
        return out