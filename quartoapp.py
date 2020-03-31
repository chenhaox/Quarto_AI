from flask import Flask,url_for,redirect,render_template,session, request, abort, escape, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pieces import makeAPiecefromString

import os
import json
from game import Game, GameError
import time
app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(32)
game = Game()

# limitation for the website
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@app.route("/getnextstep", methods = ["POST"])
@limiter.limit("2/second")
def getnextstep():
    print(request.method)
    errorcode = None
    if request.method =="POST":
        print("This is a post request")
        # 确定访问站点
        # 确定API访问秒数

        data = json.loads(request.data)
        print(data)
        game.board.parseDict({(column,row):makeAPiecefromString(row+column,rowvalue) for column,columnvalue in enumerate(data['board'])  for row,rowvalue in enumerate(columnvalue) if rowvalue})
        game.next_piece = makeAPiecefromString('p',data['next_piece']) if data['next_piece'] else None
        game.remaining.bag = [makeAPiecefromString(index,stringx) for index,stringx in enumerate(data['remaining_pieces'])]

        if game.board.getState():
            datareturn = {
                'state': 1,
                'next_piece': "",
                'remaining': data['remaining_pieces'],
                'board': data['board']

            }
            return jsonify(**datareturn)


        next_piece, coordinate = game.AI_place()
        game.board.placePiece(game.next_piece, *coordinate)
        game.next_piece = None
        game.remaining.remove(next_piece.validate())
        datareturn = {
            'winner':  -game.board.getState() if game.board.getState() is not None else "",
            'next_piece':"{:04b}".format(next_piece.type()) if game.board.getState() is None else "",
            'remaining': game.remaining.binary_output(),
            'board': game.board.parseOutput()
        }
        return jsonify(**datareturn)

@app.route('/')
def index():
    return render_template('game-view.html')

if __name__ == "__main__":
    app.run()