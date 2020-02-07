from node import Node
import copy
import random
class AI():
    def __init__(self, depth = 2):
        self.depth = depth
        self.player = 1

    def getNext(self,board, bag, next_piece):
        board = copy.deepcopy(board)
        bag = copy.deepcopy(bag)
        next_piece = copy.deepcopy(next_piece)
        remspots = board.emptyTiles()
        nRemSpots = len(remspots)
        if nRemSpots > 12:
            result = self.simple_getMove(board,bag, next_piece)
        elif 9<nRemSpots<=12:
            result = self.maxmin_getMove(board,bag, next_piece, 1)
        elif 7<nRemSpots<=9:
            result = self.maxmin_getMove(board,bag, next_piece, 2)
        elif 5< nRemSpots <= 9:
            result = self.maxmin_getMove(board,bag, next_piece, 3)
        elif 1< nRemSpots <= 5:
            result = self.maxmin_getMove(board,bag, next_piece, 4)
        else:
            result = remspots[0]
        return result


    def maxmin_getMove(self, board, bag, next_piece, depth):
        board = copy.deepcopy(board)
        bag = copy.deepcopy(bag)
        next_piece = copy.deepcopy(next_piece)
        debug = True
        remspots = board.emptyTiles()       #剩下的空余地方
        rempieces = bag.bag                 #剩下的棋子
        scorenodes = []
        rootnodes = []
        passedPiece = next_piece
        m = 0
        maximizer = -999
        minimizer = 999
        breakflag = 0
        for i in range(len(remspots)):
            if breakflag ==1:
                break
            for j in range(len(rempieces)):
                returnresult = self.buildTree(passedPiece=passedPiece, board=board, bag=bag, coordinate=remspots[i],
                               next_piece=rempieces[j], player=1 if self.player == 0 else 0, depth=depth,
                               maximizer=maximizer, minimizer=minimizer)
                if returnresult is None:
                    continue
                if self.player == 1:
                    if returnresult > maximizer:
                        scorenodes.append(returnresult)
                        maximizer = max(maximizer, returnresult)
                        rootnodes.append(
                            Node(next_piece=rempieces[j], coordinate=remspots[i], player=1 if self.player == 0 else 0))
                        if returnresult == 1:
                            breakflag = 1
                            break
                    else:
                        continue
                else:
                    if returnresult < minimizer:
                        scorenodes.append(returnresult)
                        minimizer = min(minimizer, returnresult)
                        rootnodes.append(
                            Node(next_piece=rempieces[j], coordinate=remspots[i], player=1 if self.player == 0 else 0))
                        if returnresult == -1:
                            breakflag = 1
                            break
                    else:
                        continue
            m += 1
        print("The final score is:",max(scorenodes))
        return rootnodes[scorenodes.index(max(scorenodes))]

    def simple_getMove(self, board, bag, next_piece):
        remspots = board.emptyTiles()
        rempieces = copy.deepcopy(bag.bag)
        winner = -1;
        isQ = False

        for i in range(len(remspots)):
            if self.checkIfWinAt(board, next_piece, X= remspots[i][0],Y=remspots[i][1]):
                winner = i
                isQ = True
                break
        if (winner == -1):
            randpos = random.choice(remspots)

        randPiece = random.choice(rempieces)
        result = Node(coordinate=randpos,next_piece=randPiece, player=0)
        if isQ:
            result.isquarto = True
        return result


    def checkIfWinAt(self, board, piece, X, Y):
        if X < 0 or X > 3 or Y < 0 or Y > 3:
            raise IndexError

        if board.data[X][Y] is not None:
            return board.isWon()
        board.placePiece(piece, X, Y)
        out = board.isWon()
        board.removePiece(X, Y)
        return out

    def checkIfWinAt2(self, board, cbag, piece, X, Y):
        if X < 0 or X > 3 or Y < 0 or Y > 3:
            raise IndexError

        if board.data[X][Y] is not None:
            return board.isWon()
        board.placePiece(piece, X, Y)
        out = board.isWon()
        try:
            cbag.remove(piece.validate())
        except:
            pass

        return out

    def buildTree(self,board, bag, passedPiece, coordinate, next_piece, player,depth,maximizer=-999, minimizer=999):
        # print("Building Tree"+str(depth))
        # node = Node(next_piece= next_piece, coordinate=coordinate, player= player)
        cboard = copy.deepcopy(board)
        cbag = copy.deepcopy(bag)
        x = coordinate[0]
        y = coordinate[1]
        if next_piece == 16:
            return 0
        if self.checkIfWinAt2(cboard,cbag, passedPiece, x, y):
            return -1 if player == 1 else 1
        if depth == 0:
            return 0

        remspots = cboard.emptyTiles()
        rempieces = cbag.bag
        scorepoll = []
        breakflag = 0
        for i in range(len(remspots)):
            if breakflag == 1:
                break
            if len(rempieces) > 0:
                for j in range(len(rempieces)):
                    returnresult = self.buildTree(board=cboard, bag=cbag, passedPiece=next_piece, next_piece=rempieces[j],
                                   coordinate=remspots[i], player=1 if player == 0 else 0, depth=depth - 1, maximizer=maximizer, minimizer=minimizer)
                    if returnresult is None:
                        continue
                    if player == 1:
                        if returnresult > maximizer:
                            scorepoll.append(returnresult)
                            maximizer = max(maximizer, returnresult)
                            if returnresult == 1:
                                breakflag = 1
                                break
                        else:
                            continue
                    else:
                        if returnresult < minimizer:
                            scorepoll.append(returnresult)
                            minimizer = min(minimizer, returnresult)
                            if returnresult == -1:
                                breakflag = 1
                                break
                        else:
                            continue
                else:
                    returnresult = self.buildTree(board=cboard, bag=cbag, passedPiece=next_piece, next_piece=16,
                                   coordinate=remspots[i], player=1 if player == 0 else 0, depth=depth - 1, maximizer=maximizer, minimizer=minimizer)
                    if returnresult is None:
                        continue
                    if player == 1:
                        if returnresult > maximizer:
                            scorepoll.append(returnresult)
                            maximizer = max(maximizer, returnresult)
                            if returnresult == 1:
                                break
                        else:
                            continue
                    else:
                        if returnresult < minimizer:
                            scorepoll.append(returnresult)
                            minimizer = min(minimizer, returnresult)
                            if returnresult == -1:
                                break
                        else:
                            continue
        if len(scorepoll) == 0:
            return None
        return max(scorepoll) if player == 1 else min(scorepoll)

    def  __computeMinimax(self, node):
        if node.isleaf:
            if node.isquarto:
                return 1 if node.player == 0 else -1
            else:
                return 0

        ans = 0
        childnodeiter = iter(node.children)
        for childnode in childnodeiter:
            tans = self.__computeMinimax(childnode)
            if node.player == 0:
                ans = min(ans, tans)
            else:
                ans = max(ans, tans)
        return ans

if __name__ == "__main__":
    from board import Board
    from bag import Bag
    board = Board()
    bag = Bag()
    next_piece = bag.remove((0,1,0,1))
    # test.placePiece(pieces_list_definition[0], 0, 0)
    ai = AI(depth=1)
    print(ai.getNext(board=board,bag=bag,next_piece=next_piece))