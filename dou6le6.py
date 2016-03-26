from flask import Flask
from flask import render_template
from FirebaseWrapper import *
import DominoesUtils as Utils
import time

## Firebase Settings
firebase_url = 'https://ENTER-ACCOUNT-NAME-HERE.firebaseio.com/'
firebase_db = '/ENTER-DB-NAME-HERE'

## Set up Firebase Wrapper
fb = FirebaseWrapper(firebase_url, firebase_db)

app = Flask(__name__)

@app.route('/')
def app_status():
    html_str = "<html><head><title>DB Info</title></head><body>"
    fb_users_key = "USERS"
    fb_get_response = fb.get_data(fb_users_key)
    html_str += "<h1>Users</h1>"
    html_str += str(fb_get_response)
    html_str += "<br> <br>"
    html_str += "<h1>Games</h1>"
    fb_get_response = fb.get_data("PUBLIC_GAMES")    
    html_str += str(fb_get_response)
    html_str += "</body></html>"
    return html_str

@app.route('/game/<int:game_id>')
def show_game_info(game_id):
    fb_game_key = 'game_' + str(game_id)
    fb_get_response = fb.get_data(fb_game_key)
    python_game = Utils.extract_game(fb_get_response)
    
    return render_template('game.html', game = python_game, game_id = game_id)

@app.route('/game/reset/<int:game_id>')
def reset_game(game_id):
    fb_game_key = 'game_' + str(game_id)
    fb_get_response = fb.get_data(fb_game_key)
    python_game = Utils.extract_game(fb_get_response)
    
    game = Utils.reset_game(python_game)
    
    fb_post_game = Utils.encode_game(game)
    fb_post_response = fb.write_data(fb_game_key, fb_post_game)
    return fb_post_response

@app.route('/game/join/<int:game_id>/<int:user_id>')
def join(game_id, user_id):
    fb_game_key = 'game_' + str(game_id)
    fb_get_response = fb.get_data(fb_game_key)
    python_game = Utils.extract_game(fb_get_response)

    game = Utils.join_game(python_game, user_id)    
    
    if len(game['players_list']) == 4 and game['has_started'] == False:
        if game['is_private'] == False:
            public_games = fb.get_data("PUBLIC_GAMES")
            delete_ind = None
            for ind, game_list in enumerate(public_games):
                if game_list[0] == game_id:
                    delete_ind = ind
                    break
            if delete_ind != None:
                del public_games[delete_ind]
            fb.write_data("PUBLIC_GAMES", public_games)
        
        game = Utils.initialize_game(game)
    
    fb_post_game = Utils.encode_game(game)
    fb_post_response = fb.write_data(fb_game_key, fb_post_game)
    return fb_post_response

@app.route('/game/leave/<int:game_id>/<int:user_id>')
def leave(game_id, user_id):
    fb_game_key = 'game_' + str(game_id)
    fb_get_response = fb.get_data(fb_game_key)
    python_game = Utils.extract_game(fb_get_response)

    ## Checks user_id in game
    if Utils.is_user_in_game(python_game, user_id):
        game = Utils.leave_game(python_game, user_id)
        if len(game["players_list"]) == 0 and game["is_game_over"] == False:
            return Utils.delete_game(fb, game_id)
        else:
            fb_post_game = Utils.encode_game(game)
            fb_post_response = fb.write_data(fb_game_key, fb_post_game)
            return fb_post_response
    else:
        return "Player with id " + str(user_id) + " is not in game " + str(game_id) + "."
        
    

@app.route('/game/timeup/<int:game_id>')
def timeup(game_id):
    fb_game_key = 'game_' + str(game_id)
    fb_get_response = fb.get_data(fb_game_key)
    python_game = Utils.extract_game(fb_get_response)

    game = Utils.timeup(python_game)    
        
    fb_post_game = Utils.encode_game(game)
    fb_post_response = fb.write_data(fb_game_key, fb_post_game)
    return fb_post_response

@app.route('/game/<int:game_id>/<int:user_id>/play/<direction>/<domino>')
def play_domino(game_id, user_id, direction, domino):
    fb_game_key = 'game_' + str(game_id)
    fb_get_response = fb.get_data(fb_game_key)
    python_game = Utils.extract_game(fb_get_response)
    
    game = Utils.play_domino(python_game, user_id, str(direction), str(domino))

    fb_post_game = Utils.encode_game(game)
    fb_post_response = fb.write_data(fb_game_key, fb_post_game)
    
    if game["is_round_over"] and not game["is_game_over"]:
        time.sleep(10)
        game = Utils.initialize_round(game)
        
        fb_post_game = Utils.encode_game(game)
        fb_post_response = fb.write_data(fb_game_key, fb_post_game)
    return fb_post_response

if __name__ == '__main__':
    app.run(debug=True)
