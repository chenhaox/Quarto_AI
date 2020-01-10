import copy
import random
from pieces import pieces_list_definition

class Bag(object):
    def __init__(self):
        self.bag = copy.deepcopy(pieces_list_definition)
        # random.shuffle(self.bag)

    def __str__(self):
        out = "Remaining Pieces:\n"
        for piece in self.bag:
            out += str(piece) + "\n"
        return out

    def __len__(self):
        return len(self.bag)

    def isIn(self, piece):
        return piece in self.bag

    def validate_bag(self):
        bag = []
        for piece in self.bag:
            bag.append(piece.validate())
        return bag
    def remove(self, *args):
        args = args[0]
        if len(args) != 4:
            raise Exception("Argument Error")
        for idx in range(len(self.bag)):
            if self.bag[idx].validate() == args:
                return self.bag.pop(idx)
        else:
            raise Exception("Invalid removing")

if __name__ == "__main__":
    bag = Bag()
    print(bag)