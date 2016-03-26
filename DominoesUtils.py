import random
import time
from FirebaseWrapper import *

dominoes = []
for i in range(7):
    for j in range(i+1):
        dominoes.append([j, i])

def extract_game(game_data):
    game_dict = {
        'name'                : game_data[0],
        'is_private'          : game_data[1],
        'has_started'         : game_data[2],
        'players_list'        : game_data[3],
        'players_dominoes'    : game_data[4],
        'current_player'      : game_data[5],
        'left_dominoes'       : game_data[6],
        'right_dominoes'      : game_data[7],
        'starting_domino'     : game_data[8],
        'num_of_each_domino'  : game_data[9],
        'reason_round_over'   : game_data[10],
        'is_round_over'       : game_data[11],
        'points'              : game_data[12],
        'round_count'         : game_data[13],
        'reason_game_over'    : game_data[14],
        'is_game_over'        : game_data[15]
    }
    return game_dict

def encode_game(game_dict):
    game_data = [game_dict['name'],
                 game_dict['is_private'],
                 game_dict['has_started'],
                 game_dict['players_list'],
                 game_dict['players_dominoes'],
                 game_dict['current_player'],
                 game_dict['left_dominoes'],
                 game_dict['right_dominoes'],
                 game_dict['starting_domino'],
                 game_dict['num_of_each_domino'],
                 game_dict['reason_round_over'],
                 game_dict['is_round_over'],
                 game_dict['points'],
                 game_dict['round_count'],
                 game_dict['reason_game_over'],
                 game_dict['is_game_over']
                ]
    return game_data

def is_user_in_game(game, user_id):
    return user_id in game['players_list']

def delete_game(fb, game_id):
    public_games = fb.get_data("PUBLIC_GAMES")
    delete_ind = None
    for ind, game_list in enumerate(public_games):
        if game_list[0] == game_id:
            delete_ind = ind
            break
    if delete_ind != None:
        del public_games[delete_ind]
    fb.write_data("PUBLIC_GAMES", public_games)
    
    fb_game_key = "game_" + str(game_id)
    return fb.delete_data(fb_game_key)

def reset_game(game_dict):
    ## Reset Game
    game_dict['has_started'] = False
    game_dict['players_list'] = []
    game_dict['players_dominoes'] = [[],[],[],[]]
    game_dict['left_dominoes'] = []
    game_dict['right_dominoes'] = []
    game_dict['starting_domino'] = "CENTER-DOMINO-NOT-PLAYED"
    game_dict['num_of_each_domino'] = [0 for i in range(7)]
    game_dict['reason_round_over'] = "ROUND-END-REASON"
    game_dict['is_round_over'] = False
    game_dict['points'] = [0, 0]
    game_dict['round_count'] = 0
    game_dict['reason_game_over'] = "GAME-END-REASON"
    game_dict['is_game_over'] = False
    return game_dict
    
def remove_from_public_games(fb, game_id):
    public_games = fb.get_data("PUBLIC_GAMES")
    delete_ind = None
    for ind, game_list in enumerate(public_games):
        if game_list[0] == game_id:
            delete_ind = ind
            break
    if delete_ind != None:
        del public_games[delete_ind]
    fb.write_data("PUBLIC_GAMES", public_games)

def not_passable(rand_dominoes):
    if rand_dominoes == dominoes:
        return True
    
    for i in range(4):
        player_hand = rand_dominoes[7*i:7*(i+1)]
        count_doubles = 0
        for domino in player_hand:
            count_doubles += (domino[0] == domino[1]) # 1 if double, 0 if not
        if count_doubles >= 5:
            return True
    return False

def randomize_dominoes():
    rand_dominoes = dominoes[:]
    count = 0
    while not_passable(rand_dominoes) or count < 10:
        random.shuffle(rand_dominoes)
        count += 1
    return rand_dominoes

def join_game(game_dict, user_id):
    players = game_dict['players_list'] 
    if user_id not in players:
        players.append(user_id)
    game_dict['players_list'] = players
    return game_dict

def initialize_round(game_dict):
    rand_dominoes = randomize_dominoes()
    players_hands = []
    for i in range(4):
        hand = rand_dominoes[7*i:7*i+7]
        players_hands.append(rand_dominoes[7*i:7*i+7])
    ## Initialize Game
    game_dict['players_dominoes'] = players_hands
    game_dict['has_started'] = True
    game_dict['left_dominoes'] = []
    game_dict['right_dominoes'] = []
    game_dict['starting_domino'] = "CENTER-DOMINO-NOT-PLAYED"
    game_dict['num_of_each_domino'] = [0 for i in range(7)]
    game_dict['reason_round_over'] = "ROUND-END-REASON"
    game_dict['is_round_over'] = False
    game_dict['round_count'] += 1
    game_dict['reason_game_over'] = "GAME-END-REASON"
    game_dict['is_game_over'] = False
    return game_dict

def initialize_game(game_dict):
    rand_dominoes = randomize_dominoes()
    players_hands = []
    for i in range(4):
        hand = rand_dominoes[7*i:7*i+7]
        if [6,6] in hand:
            game_dict["current_player"] = i+1
        players_hands.append(rand_dominoes[7*i:7*i+7])
    ## Initialize Game
    game_dict['players_dominoes'] = players_hands
    game_dict['has_started'] = True
    game_dict['left_dominoes'] = []
    game_dict['right_dominoes'] = []
    game_dict['starting_domino'] = "CENTER-DOMINO-NOT-PLAYED"
    game_dict['num_of_each_domino'] = [0 for i in range(7)]
    game_dict['reason_round_over'] = "ROUND-END-REASON"
    game_dict['is_round_over'] = False
    game_dict['points'] = [0, 0]
    game_dict['round_count'] = 1
    game_dict['reason_game_over'] = "GAME-END-REASON"
    game_dict['is_game_over'] = False
    return game_dict

def leave_game(game_dict, user_id):
    players = game_dict['players_list']
    player_leaving = players.index(user_id) + 1
    
    has_started = game_dict['has_started']
    
    if has_started:
        game_dict['reason_game_over'] = "Player " + str(player_leaving) + " has forfeited the game."
        game_dict['is_game_over'] = True
    
    if user_id in players:
        players.remove(user_id)
        game_dict['players_list'] = players
    
    return game_dict

def timeup(game_dict):
    game_dict['reason_game_over'] = " Player " + str(game_dict['current_player']) + "'s time to play has expired. "
    game_dict['is_game_over'] = True
    return game_dict


def play_domino(game, user_id, direction, domino):
    
    # initialize temp var for current_player index
    current_player_index = game["players_list"].index(user_id)
    
    # if domino == pass, then simply update the current_player in firebaseDB
    if domino == "PASS":
        
        game["current_player"] = (current_player_index + 1) % 4 + 1
        return game
    
    # Possible orientations of the domino being played
    domino_0 = [int(domino[0]), int(domino[1])]
    domino_1 = [int(domino[1]), int(domino[0])]
    
    # If no starting domino has been played yet, then play the current domino
    # as the starting one.
    if game["starting_domino"] == "CENTER-DOMINO-NOT-PLAYED":
        game["starting_domino"] = domino_0
    # A starting domino exists, so verify which orientation the domino must be
    # to be played on the user specified side.
    else:
        if direction == "L":
            if len(game["left_dominoes"]) >0:
                l_domino_num = str(game["left_dominoes"][-1][-1])
            else:
                l_domino_num = str(game["starting_domino"][0])

            if domino[0] == l_domino_num:
                game["left_dominoes"].append(domino_0)
            elif domino[1] == l_domino_num:
                game["left_dominoes"].append(domino_1)
            else:
                return game

        elif direction == "R":
            if len(game["right_dominoes"]) >0:
                r_domino_num = str(game["right_dominoes"][-1][-1])
            else:
                r_domino_num = str(game["starting_domino"][-1])

            if domino[0] == r_domino_num:
                game["right_dominoes"].append(domino_0)
            elif domino[1] == r_domino_num:
                game["right_dominoes"].append(domino_1)
            else:
                return game

    # Update the count for the number of each domino number played.
    # keep track of the edge case for when a domino is a double
    game["num_of_each_domino"][int(domino[0])] +=1
    if int(domino[0]) != int(domino[1]):
        game["num_of_each_domino"][int(domino[1])] +=1

    # Verify which domino orientation was in the players hand and remove the
    # domino from the players hand.
    if domino_0 in game["players_dominoes"][current_player_index]:
        game["players_dominoes"][current_player_index].remove(domino_0)
    elif domino_1 in game["players_dominoes"][current_player_index]:
        game["players_dominoes"][current_player_index].remove(domino_1)
    
    # Verify if after making the play, the round has ended with a winning move.
    game, winning_player = is_round_over(game, game["current_player"])
    
    # Verify if the points limit has been reached to end the game.
    game = is_game_over(game)

    # Update the current_player number in FirebaseDB
    if game["is_round_over"]:
        game["current_player"] = winning_player
    else:
        game["current_player"] = (game["current_player"]) % 4 + 1

    return game


def is_game_over(game):
    
    points = game['points']
    reason = "GAME-END-REASON"
    game_over = False
    game_limit = 100
    
    if points[0] >= game_limit:
        reason = "Team 1 won this game with " + str(points[0]) + " points."
        game_over = True
    elif points[1] >= game_limit:
        reason = "Team 2 won this game with " + str(points[1]) + " points."
        game_over = True
    
    game['reason_game_over'] = reason
    game['is_game_over'] = game_over
    
    return game


def is_round_over(game, current_player):
    
    reason = "ROUND-END-REASON"
    round_over = False
    winning_player = 0
    round_points = 0
 
    
    if len(game["left_dominoes"]) > 0:
        left_end_num = game["left_dominoes"][-1][-1]
    else:
        left_end_num = game["starting_domino"][0]
        
    if len(game["right_dominoes"]) > 0:
        right_end_num = game["right_dominoes"][-1][-1]
    else:
        right_end_num = game["starting_domino"][-1]

    if (game["num_of_each_domino"][left_end_num] == 7) and (game["num_of_each_domino"][right_end_num] == 7):
        round_over = True
        winning_player, winning_team, round_points = determine_blocked_game_winner(game["players_dominoes"], current_player)
        reason = "Player " + str(current_player) + " blocked the game. Team " + str(winning_team) + " wins this round, gaining " + str(round_points) + " points. Player " + str(winning_player) + " starts the next round."
        
    elif len(game["players_dominoes"][current_player-1]) == 0:
        round_over = True
        winning_player, winning_team, round_points = current_player_wins(game["players_dominoes"], current_player)
        reason = "Player " + str(current_player) + " finished all their dominoes first. Team " + str(winning_team) + " wins this round, gaining " + str(round_points) + " points. Player " + str(winning_player) + " starts the next round."

    if round_over:
        game["points"][winning_team-1] += round_points
        game['reason_round_over'] = reason
        game['is_round_over'] = round_over
    
    
    return game, winning_player


# If the player won by finishing their dominoes, then they are the winner
# and their team is the winning team
def current_player_wins(player_dominoes, current_player):
    
    # Calculate points to be won
    points = calculate_points(player_dominoes)
    
    # Determine which team the current player is on
    current_player_team = determine_current_player_team(current_player)

    winning_player = current_player
    winning_team = current_player_team

    return winning_player, winning_team, points
        

# If the game was blocked, determine who has less points in their team's
# hand. If the current player does, then their team wins, else, the other team
# wins and the player after the current player starts the next round
def determine_blocked_game_winner(player_dominoes, current_player):
    
    # Calculate points to be won
    points = calculate_points(player_dominoes)
    current_player_team = determine_current_player_team(current_player)
    
    team_1_points = calculate_points([player_dominoes[0],player_dominoes[2]])
    team_2_points = calculate_points([player_dominoes[1],player_dominoes[3]])
        
    if team_2_points  > team_1_points:
        winning_team = 1
    elif team_1_points > team_2_points:
        winning_team = 2
    elif team_1_points == team_2_points:
        winning_team = current_player_team
        
    if winning_team == current_player_team:
        winning_player = current_player
    elif winning_team != current_player_team:
        winning_player = (current_player % 4) + 1
    
    return winning_player, winning_team, points
        
        
def determine_current_player_team(current_player):
    
    # Verify which team the current player is on
    if current_player % 2 == 1:
        current_player_team = 1
    else:
        current_player_team = 2
        
    return current_player_team
    
    
    
def calculate_points(player_dominoes):
    
    points = 0
    for i in player_dominoes:
        for j in i:
            points += sum(j)
        
    return points
        