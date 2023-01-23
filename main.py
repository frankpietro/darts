import server as s
import constants as c
import user_interface as ui
import modules as m

from classes import *


if __name__ == '__main__':
    ui.welcome_print()

    conn = s.create_server_connection()
    cursor = conn.cursor()

    s.create_darts_db(cursor)
    s.create_tables(cursor)
    s.add_foreign_keys(cursor)

    loop = True

    while loop:
        ui.initial_print()
        option = ui.initial_input()
        print()

        # ----------------- NEW PLAYER -----------------

        if option == c.REG_NEW_PLAYER:
            reg_new_player = True

            while reg_new_player:
                print("Register a new player")

                name = ui.ask_for_name()

                id = s.search_player(name, conn)
                if id:
                    print(f"Player {name} already exists with id {id}")
                else:
                    player = Player(name=name)
                    player.insert_to_db(conn)
                    print(f"Player {player.name} successfully registered with id {player.id}")
                
                reg_new_player = ui.ask_for_confirmation("Do you want to register another player? (Y/n): ")

        # ----------------- TRAINING SESSION -----------------

        elif option == c.START_TR_SESS:
            start_tr_sess = True

            while start_tr_sess:
                print("Start a training session")

                player = m.get_player(conn)

                training_session = TrainingSession(player=player)
                training_session.insert_to_db(conn)

                keep_aiming = True
                while keep_aiming:
                    aim = ui.ask_for_aim()
                    
                    keep_throwing = True
                    while keep_throwing:
                        turn = TrainingTurn(aim=aim, training_session_id=training_session.id)
                        
                        turn.fill()

                        turn.insert_to_db(conn)
                        training_session.add_turn(turn)

                        keep_throwing = ui.ask_for_confirmation("Do you want to throw again with same aim? (Y/n): ")

                    keep_aiming = ui.ask_for_confirmation("Do you want to change aim? (Y/n): ")
                
                start_tr_sess = ui.ask_for_confirmation("Do you want to start another training session? (Y/n): ")

        # ----------------- MATCH -----------------

        elif option == c.START_MATCH:
            keep_playing = True
            while keep_playing:
                print("Start a match")

                match = Match(sets=[])

                # ask number of players per team
                n_players_per_team = ui.ask_for_players_per_team()
                print()

                if n_players_per_team == 1:
                    print("Player 1")
                    player1 = m.get_player(conn)
                    match.add_player(player1, 1)
                    print()

                    print("Player 2")
                    player2 = m.get_player(conn, unavailable_player=player1)
                    match.add_player(player2, 2)
                    print()

                elif n_players_per_team == 2:
                    print("Team 1")
                    team1 = m.get_team(conn)
                    match.add_team(team1, 1)
                    print()

                    print("Team 2")
                    team2 = m.get_team(conn, unavailable_team=team1)
                    match.add_team(team2, 2)
                    print()

                # add match to database
                match.insert_to_db(conn)

                # add one set after another
                keep_adding_sets = True
                set_order = 0
                while keep_adding_sets:
                    set_order += 1
                    set = Set(match_id=match.id, set_order=set_order, legs=[])

                    set.insert_to_db(conn)
                    match.add_set(set)

                    keep_adding_legs = True
                    leg_order = 0
                    while keep_adding_legs:
                        leg_order += 1
                        print(f"Leg {leg_order}")
                        # ask for goal of leg
                        goal = ui.ask_for_leg_goal()
                        print()

                        leg = Leg(set_id=set.id, leg_order=leg_order, goal=goal, turns=[])
                        
                        leg.insert_to_db(conn)
                        set.add_leg(leg)

                        turn_order = 0
                        while leg.is_open():
                            turn_order += 1
                            current_thrower = match.next_thrower()
                            turn = MatchTurn(leg_id=leg.id, turn_order=turn_order, player=current_thrower)
                            
                            cap = leg.current_cap()

                            print(f"Turn {turn_order} by {current_thrower.name} - cap: {cap}")

                            turn.fill(cap=cap)

                            turn.insert_to_db(conn)                            
                            leg.add_turn(turn)
                        
                        print(f"Leg {leg_order} closed by {match.current_thrower.name}")

                        if n_players_per_team == 2:
                            print(f"{match.current_team} wins leg {leg_order}")

                        print(set)
                        keep_adding_legs = ui.ask_for_confirmation("Do you want to play another leg? (Y/n): ")

                    keep_adding_sets = ui.ask_for_confirmation("Do you want to play another set? (Y/n): ")

                keep_playing = ui.ask_for_confirmation("Do you want to start another match? (Y/n): ")


        elif option == c.SHOW_STATS:
            pass

        elif option == c.EXIT:
            loop = False

        print()

    conn.commit()
    conn.close()
    ui.final_print()