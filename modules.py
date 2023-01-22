import user_interface as ui
import server as s
import constants as c
import utilities as u

from classes import *


def get_player(conn, unavailable_player=None):
    player_found = False

    while not player_found:
        available = False
        while not available:
            player_name = ui.ask_for_name()
            if unavailable_player:
                if player_name == unavailable_player.name:
                    print(f"Player {player_name} is already playing")
                    continue

            available = True

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


def get_team(conn, unavailable_team=None):
    team_found = False

    while not team_found:
        p1_available = False
        while not p1_available:
            player1 = get_player(conn)
            if unavailable_team:
                if player1.id == unavailable_team.player1.id or player1.id == unavailable_team.player2.id:
                    print(f"Player {player1.name} is already playing")
                    continue
            p1_available = True

        p2_available = False
        while not p2_available:
            player2 = get_player(conn)
            if unavailable_team:
                if player2.id == unavailable_team.player1.id or player2.id == unavailable_team.player2.id:
                    print(f"Player {player2.name} is already playing")
                    continue
            if player1.id == player2.id:
                print("You cannot play with yourself")
                continue
            
            p2_available = True

        team_id, team_name = s.search_team(player1.id, player2.id, conn)

        if not team_id:
            print(f"Team {player1.name} - {player2.name} not found")
            if ui.ask_for_confirmation("Do you want to register it? (Y/n): "):
                team_name = ui.ask_for_team_name()
                team_id = s.insert_team(player1.id, player2.id, team_name, conn)
                print(f"Team {player1.name} - {player2.name} successfully registered with id {team_id} and name {team_name}")
                team_found = True
            else:
                print("Registration aborted")
        
        else:
            print(f"Team {player1.name} - {player2.name} found with id {team_id} and name {team_name}")
            team_found = True

    return Team(id=team_id, player1=player1, player2=player2, name=team_name)