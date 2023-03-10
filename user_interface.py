import constants as c
import utilities as u


def welcome_print():
    print("Welcome to the darts application!")
    print("")


def initial_print():
    print("Please select an option:")
    print("1. Register a new player")
    print("2. Start a training session")
    print("3. Start a match")
    print("4. Show statistics")
    print("5. Exit")
    print("")


def final_print():
    print("Changes saved to the database.")
    print("Thank you for using the darts application!")
    print("")


def initial_input():
    while True:
        try:
            option = int(input("Option: "))
            if option < 1 or option > 5:
                raise ValueError
            print(f"Option {option} selected.")
            if ask_for_confirmation():
                return option
        except ValueError:
            print("Invalid option. Please try again.")


def ask_for_confirmation(input_message=c.ARE_YOU_SURE):
    while True:
        confirmation = input(input_message)
        if confirmation == "y" or confirmation == "Y" or confirmation == "":
            return True
        elif confirmation == "n" or confirmation == "N":
            return False
        else:
            print("Invalid option. Please try again.")


def ask_for_name():
    while True:
        name = input("Insert player name: ")
        if name:
            print(f"Player name: {name}")
            if ask_for_confirmation():
                return name
        else:
            print("Invalid name. Please try again.")


def ask_for_mult():
    while True:
        mult = input("Insert d for double, t for triple or press enter for standard aim: ")
        if u.valid_mult(mult):
            if mult == "d":
                return "a"
            elif mult == "t":
                return "c"
            else:
                return ""
        else:
            print("Invalid multiplier. Please try again.")


def ask_for_aim():
    while True:
        aim = input("Where are you aiming at? ('b' for bull) ")
        if u.valid_aim(aim):
            if aim != "b":
                mult = ask_for_mult()
                aim = f"{aim}{mult}"
            else:
                aim = c.BULL

            print(f"Aim: {aim}")
            if ask_for_confirmation():
                return aim
        else:
            print("Invalid aim. Please try again.")


def ask_for_dart_code():
    while True:
        dart_code = input("Insert dart: ")
        if u.valid_dart_code(dart_code):
            return dart_code
        else:
            print("Invalid dart. Please try again.")


def ask_for_players_per_team():
    while True:
        try:
            players_per_team = int(input("Insert number of players per team: "))
            if players_per_team < 1 or players_per_team > 2:
                raise ValueError
            print(f"Number of players per team: {players_per_team}")
            if ask_for_confirmation():
                return players_per_team
        except ValueError:
            print("Invalid number. Please try again.")


def ask_for_team_name():
    while True:
        team_name = input("Insert team name: ")
        if team_name:
            print(f"Team name: {team_name}")
            if ask_for_confirmation():
                return team_name
        else:
            print("Invalid name. Please try again.")


def ask_for_leg_goal():
    while True:
        try:
            leg_goal = int(input("Insert leg goal: "))
            if not u.valid_goal(leg_goal):
                raise ValueError
            print(f"Leg goal: {leg_goal}")
            if ask_for_confirmation():
                return leg_goal
        except ValueError:
            print("Invalid leg goal. Please try again.")