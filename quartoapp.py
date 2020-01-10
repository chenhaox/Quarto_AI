from flask import Flask,url_for,redirect,render_template,session, request, abort, escape
from datetime import timedelta
import os
from game import GameList, GameError
app = Flask(__name__)
app.secret_key = os.urandom(32)
app.permanent_session_lifetime = timedelta(minutes=15)
gamelist= GameList()
print(gamelist.gamelist)
@app.route("/", methods = ["GET","POST"])
def index():
    print(request.method)
    errorcode = None
    if request.method =="POST":
        print("This is a post request")
        try:
        # if True:
            if "gameid" in session and session["gameid"] in gamelist.gamelist:
                gamelist.gamelist[session["gameid"]].play_validate()
                print(request.form)
                if "remaining" in list(request.form.keys()):
                    next_piece = tuple(eval(escape(request.form['remaining'])))
                    print(next_piece)
                    gamelist.gamelist[session["gameid"]].select_next(next_piece)
                    gamelist.gamelist[session["gameid"]].AI_place()
                elif "board" in list(request.form.keys()):
                    coordinate = tuple(eval(escape(request.form['board'])))
                    print(coordinate)
                    gamelist.gamelist[session["gameid"]].place_piece(coordinate)
            else:
                return "Invalid operation",404
        except Exception as e:
            errorcode = e
    if "gameid" in session and session["gameid"] in gamelist.gamelist:
        return render_template('game-view.html', game = gamelist.gamelist[session["gameid"]], game_status = gamelist.gamelist[session["gameid"]].get_state(), errorcode = errorcode)
    else:
        return "There is too many player in the server. Please wait a second and refresh the page"
@app.route("/start/")
def startgame():
    if "gameid" not in session:
        session["gameid"] = gamelist.new_game()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()