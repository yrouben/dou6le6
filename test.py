from flask import Flask
from FirebaseWrapper import *
import DominoesUtils as Utils
import random

## Firebase Settings
firebase_url = 'https://ENTER-ACCOUNT-NAME-HERE.firebaseio.com/'
firebase_db = '/ENTER-DB-NAME-HERE'

## Set up Firebase Wrapper
fb = FirebaseWrapper(firebase_url, firebase_db)

def create_test_user(fb_users, test_users):
    rand_uid = random.randint(1, 4294967295)
    while rand_uid in fb_users or rand_uid in test_users:
        rand_uid = random.randint(1, 4294967295)
    test_nickname = "test_" + str(rand_uid)
    test_in_game = False
    test_user = [test_nickname, test_in_game]
    return (test_user, rand_uid)

def create_test_users(num_test_users):
    print("Creating " + str(num_test_users) + " test users.")
    fb_users = fb.get_data("USERS")
    test_users = []
    
    for i in range(num_test_users):
        (test_user, test_user_uid) =  create_test_user(fb_users, test_users)
        test_user_key = "user_" + str(test_user_uid)
        
        fb.write_data(test_user_key, test_user)
        
        fb_users.append(test_user_uid)
        test_users.append(test_user_uid)
        
    fb.write_data("USERS", fb_users)
    print("Users successfully added.")
    return test_users

def remove_test_users(test_users):
    print("Removing test users.")
    fb_users = fb.get_data("USERS")
    
    for test_user in test_users:
        test_user_key = "user_" + str(test_user)
        fb.delete_data(test_user_key)
        
        if test_user in fb_users:
            fb_users.remove(test_user)
    fb.write_data("USERS", fb_users)
    print("Users successfully deleted.")

def create_test_game():
    print("Creating test game.")
    fb_games = fb.get_data("PUBLIC_GAMES")
    rand_game_uid = random.randint(1, 4294967295)
    while rand_game_uid in fb_games:
         rand_game_uid = random.randint(1, 4294967295)
    test_game_info = [rand_game_uid, "test_game"]
    fb_games.append(test_game_info)
    
    fb.write_data("PUBLIC_GAMES", fb_games)
        
    game = ["test_game", False, False, [], [[],[],[],[]], 1, "GAME-END-REASON", False, [], [], "CENTER-DOMINO-NOT-PLAYED",[0,0,0,0,0,0,0]]
    
    game_key = "game_" + str(rand_game_uid)
    fb.write_data(game_key, game)
    print("Test game created successfully.")
    return test_game_info

def remove_test_game(test_game):
    print("Removing test game.")
    test_game_uid = test_game[0]
    test_game_key = "game_" + str(test_game_uid)
    fb_games = fb.get_data("PUBLIC_GAMES")
    fb_games.remove(test_game)
    fb.write_data("PUBLIC_GAMES", fb_games)
    
    fb.delete_data(test_game_key)
    print("Game successfully removed.")

def test_join(test_game, test_users):
    pass

def test_leave(test_game, test_users):
    pass

def test_play_moves():
    pass

def run_tests():
    test_users = create_test_users(4)
    test_game = create_test_game()
    
    test_join()
    test_leave()
    test_play_moves()
    
    remove_test_game(test_game)
    remove_test_users(test_users)
    

if __name__ == '__main__':
    run_tests()