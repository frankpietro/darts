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
                player_id = s.insert_player(player_name, conn)
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


def get_team(conn):
    team_found = False

    while not team_found:
        player1 = get_player(conn)
        player2 = get_player(conn)

        team_id, team_name = s.search_team(player1.id, player2.id, conn)

        if not team_id:
            print(f"Team {player1.name} - {player2.name} not found")
            if ui.ask_for_confirmation("Do you want to register it? (Y/n): "):
                team_id = s.insert_team(player1.id, player2.id, conn)
                print(f"Team {player1.name} - {player2.name} successfully registered with id {team_id}")
                team_name = ui.ask_for_team_name()
                team_found = True
            else:
                print("Registration aborted")
        
        else:
            print(f"Team {player1.name} - {player2.name} found with id {team_id} and name {team_name}")
            team_found = True

    return Team(id=team_id, player1=player1, player2=player2, name=team_name)