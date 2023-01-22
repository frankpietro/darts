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

        if option == c.REG_NEW_PLAYER:
            reg_new_player = True

            while reg_new_player:
                print("Register a new player")

                name = ui.ask_for_name()

                success, id = s.register_player(name, conn)

                if success:
                    print(f"Player {name} successfully registered with id {id}")
                else:
                    print(f"Player {name} already exists with id {id}")
                
                reg_new_player = ui.ask_for_confirmation("Do you want to register another player? (Y/n): ")

        elif option == c.START_TR_SESS:
            start_tr_sess = True

            while start_tr_sess:
                print("Start a training session")

                player = m.get_player(conn)

                training_session = TrainingSession(player=player)

                keep_aiming = True
                while keep_aiming:
                    aim = ui.ask_for_aim()
                    
                    keep_throwing = True
                    while keep_throwing:
                        print(f"Aim: {aim}")

                        turn = TrainingTurn(aim)
                        
                        turn.fill()

                        training_session.add_turn(turn)

                        keep_throwing = ui.ask_for_confirmation("Do you want to throw again with same aim? (Y/n): ")

                    keep_aiming = ui.ask_for_confirmation("Do you want to change aim? (Y/n): ")
                
                s.save_training_session(training_session, conn)
                print("Training session saved to the database")
                
                start_tr_sess = ui.ask_for_confirmation("Do you want to start another training session? (Y/n): ")

        elif option == c.START_MATCH:
            keep_playing = True
            while keep_playing:
                print("Start a match")

                match = Match()

                # ask number of players per team
                n_players_per_team = ui.ask_for_players_per_team()

                if n_players_per_team == 1:
                    player1 = m.get_player(conn)
                    match.add_player(player1, 1)

                    player2 = m.get_player(conn)
                    match.add_player(player2, 2)

                elif n_players_per_team == 2:
                    team1 = m.get_team(conn)
                    match.add_team(team1, 1)

                    team2 = m.get_team(conn)
                    match.add_team(team2, 2)


                keep_playing = ui.ask_for_confirmation("Do you want to start another match? (Y/n): ")


        elif option == c.SHOW_STATS:
            pass

        elif option == c.EXIT:
            loop = False

        print()

    conn.commit()
    conn.close()
    ui.final_print()