import user_interface as ui
import server as s
import constants as c
import utilities as u

from classes import *


def get_player(conn):
    player_found = False

    while not player_found:
        player_name = ui.ask_for_name()
        player_id = s.search_player(player_name, conn)
        if not player_id:
            print(f"Player {player_name} not found")
            if ui.ask_for_confirmation("Do you want to register him? (Y/n): "):
                player_id = s.add_player(player_name, conn)
                print(f"Player {player_name} successfully registered with id {player_id}")
                player_found = True
            else:
                print("Registration aborted")

        else:
            print(f"Player {player_name} found with id {player_id}")
            player_found = True
    
    return Player(player_id, player_name)


def get_turn(turn):
    correct_turn = False
    while not correct_turn:
        print("Insert throws (<number><code>, code: a,b,c,d from outer to inner circle)")
        for i in range(c.N_DARTS):
            dart_code = ui.ask_for_dart_code()
            dart = Dart(dart_code)
            turn.add_dart(dart)
        
        print(turn)
        correct_turn = ui.ask_for_confirmation("Is this turn correct? (Y/n): ")

    return turn