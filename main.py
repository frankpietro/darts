import server as s
import constants as c
import user_interface as ui

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

                player = Player(player_id, player_name)

                training_session = TrainingSession(player=player)

                keep_aiming = True
                while keep_aiming:
                    aim = ui.ask_for_aim()
                    
                    keep_throwing = True
                    while keep_throwing:
                        print(f"Aim: {aim}")
                        correct_turn = False
                        while not correct_turn:
                            turn = TrainingTurn(aim=aim)
                            print("Insert throws (<number><code>, code: a,b,c,d from outer to inner circle)")
                            for i in range(c.N_DARTS):
                                dart_code = ui.ask_for_dart_code()
                                dart = Dart(dart_code)
                                turn.add_dart(dart)
                            
                            print(turn)
                            correct_turn = ui.ask_for_confirmation("Is this turn correct? (Y/n): ")

                        training_session.add_turn(turn)

                        keep_throwing = ui.ask_for_confirmation("Do you want to throw again with same aim? (Y/n): ")

                    keep_aiming = ui.ask_for_confirmation("Do you want to change aim? (Y/n): ")
                
                s.save_training_session(training_session, conn)
                print("Training session saved to the database")
                
                start_tr_sess = ui.ask_for_confirmation("Do you want to start another training session? (Y/n): ")

        elif option == c.START_MATCH:
            keep_playing = True
            while keep_playing:
                


        elif option == c.SHOW_STATS:
            pass

        elif option == c.EXIT:
            loop = False

        print()

    conn.commit()
    conn.close()
    ui.final_print()