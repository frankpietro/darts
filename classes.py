import itertools
import datetime as dt

import utilities as u
import user_interface as ui
import constants as c



class DatabaseEntity:
    def __init__(self, id=None):
        self.id = id

    
    def insert_string(self):
        raise NotImplementedError("Method not implemented")


    def insert_to_db(self, conn):
        cursor = conn.cursor()
        insert_str = self.insert_string()
        cursor.execute(insert_str)
        conn.commit
        self.id = cursor.lastrowid


class Match:
    def __init__(self, id=None, team1=None, team2=None, player1=None, player2=None, datetime=dt.datetime.now(), sets=[], first_thrower=None):
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.player1 = player1
        self.player2 = player2
        self.datetime = datetime
        self.sets = sets

        self.current_thrower = first_thrower
        
        if team1 and team2:
            if not self.current_thrower:
                self.current_team = None
            else:
                if self.current_thrower == self.team1.player1 or self.current_thrower == self.team1.player2:
                    self.current_team = self.team1
                elif self.current_thrower == self.team2.player1 or self.current_thrower == self.team2.player2:
                    self.current_team = self.team2
                else:
                    raise ValueError("Invalid current thrower")
        else:
            self.current_team = None


    def __str__(self):
        # timestamp_str: dd-mm-yyyy hh:mm
        timestamp_str = self.datetime.strftime("%d-%m-%Y %H:%M")

        match_str = ""
        if self.id:
            match_str = f"Match {self.id} - {timestamp_str}\n"
        else:
            match_str = f"Match - {timestamp_str}\n"

        if self.team1:
            match_str += f"Team 1: {self.team1}\n"
        if self.team2:
            match_str += f"Team 2: {self.team2}\n"
        if self.player1:
            match_str += f"Player 1: {self.player1}\n"
        if self.player2:
            match_str += f"Player 2: {self.player2}\n"

        for s in self.sets:
            match_str += f"{s}\n"

        return match_str


    def __eq__(self, other):
        return self.id == other.id


    def set_id(self, id):
        self.id = id


    def add_team(self, team, pos):
        if pos == 1:
            self.team1 = team
        elif pos == 2:
            self.team2 = team
        else:
            raise ValueError("Invalid team position")
    
    
    def add_player(self, player, pos):
        if pos == 1:
            self.player1 = player
        elif pos == 2:
            self.player2 = player
        else:
            raise ValueError("Invalid player position")

    
    def add_set(self, set):
        self.sets.append(set)


    def next_thrower(self):
        if self.team1 and self.team2:
            if not self.current_thrower:
                self.current_thrower = self.team1.next_player()
            elif self.current_thrower == self.team1.player1 or self.current_thrower == self.team1.player2:
                self.current_thrower = self.team2.next_player()
            elif self.current_thrower == self.team2.player1 or self.current_thrower == self.team2.player2:
                self.current_thrower = self.team1.next_player()
            else:
                raise ValueError("Invalid current thrower")

        elif self.player1 and self.player2:
            if not self.current_thrower:
                self.current_thrower = self.player1
            elif self.current_thrower == self.player1:
                self.current_thrower = self.player2
            elif self.current_thrower == self.player2:
                self.current_thrower = self.player1
            else:
                raise ValueError("Invalid current thrower")

        else:
            raise ValueError("Invalid match configuration")
        
        return self.current_thrower
    
    
class Set:
    def __init__(self, id=None, set_order=None, legs=[]):
        self.id = id
        self.set_order = set_order
        self.legs = legs


    def __str__(self):
        set_str = ""

        if self.id:
            set_str += f"Set {self.set_order} with id {self.id}"
        else:
            set_str += f"Set {self.set_order}"

        for l in self.legs:
            set_str += f"\n{l}"

        return set_str
        

    def __eq__(self, other):
        if self.id and other.id:
            return self.id == other.id
        elif not (self.id or other.id):
            return self.legs == other.legs
        else:
            return False


    def set_id(self, id):
        self.id = id

    
    def add_leg(self, leg):
        self.legs.append(leg)



class Leg:
    def __init__(self, id=None, leg_order=None, goal=None, turns=[]):
        self.id = id
        self.leg_order = leg_order
        self.goal = goal
        self.turns = turns

    
    def __str__(self):
        leg_str = ""

        if self.id:
            leg_str += f"Leg {self.leg_order} with id {self.id}"
        else:
            leg_str += f"Leg {self.leg_order}"

        for t in self.turns:
            leg_str += f"\n{t}"

        return leg_str
        


    def is_open(self):
        # sum score of all even turns and of all odd turns
        # if they are both less than goal, leg is open
        even_score = 0
        odd_score = 0
        for i, t in enumerate(self.turns):
            if i % 2 == 0:
                even_score += t.get_score()
            else:
                odd_score += t.get_score()

        return even_score < self.goal and odd_score < self.goal

    
    def current_cap(self):
        # if odd number of turns, sum all odd turns
        # if even number of turns, sum all even turns
        already_scored = 0

        if len(self.turns) % 2 == 0:
            already_scored += sum(t.get_score() for i, t in enumerate(self.turns) if i % 2 == 0)
        else:
            already_scored += sum(t.get_score() for i, t in enumerate(self.turns) if i % 2 != 0)

        return self.goal - already_scored


    def add_turn(self, turn):
        self.turns.append(turn)
    


class TrainingSession:
    def __init__(self, id=None, player=None, datetime=dt.datetime.now(), turns=[]):
        self.id = id
        self.player = player
        self.datetime = datetime
        self.turns = turns

    
    def __str__(self):
        # timestamp_str: dd-mm-yyyy hh:mm
        timestamp_str = self.datetime.strftime("%d-%m-%Y %H:%M")
        if self.id:
            ret_str = f"Training session {self.id}\nTime: {timestamp_str}\n{self.player}"
        else:
            ret_str = f"Training session \nTime: {timestamp_str}\n{self.player}"

        for t in self.turns:
            ret_str += f"\n{t}"

        return ret_str


    def add_turn(self, turn):
        self.turns.append(turn)



class Turn:
    def __init__(self, id=None, dart1=None, dart2=None, dart3=None):
        self.dart1 = dart1
        self.dart2 = dart2
        self.dart3 = dart3
        self.id = id


    def __str__(self):
        ret_str = ""
        if self.dart1 is not None:
            ret_str += str(self.dart1)
        if self.dart2 is not None:
            ret_str += " " + str(self.dart2)
        if self.dart3 is not None:
            ret_str += " " + str(self.dart3)
        return ret_str


    def add_dart(self, dart):
        if self.dart1 is None:
            self.dart1 = dart
        elif self.dart2 is None:
            self.dart2 = dart
        elif self.dart3 is None:
            self.dart3 = dart
        else:
            print("Error: turn already has 3 darts")

    
    def remove_all_darts(self):
        self.dart1 = None
        self.dart2 = None
        self.dart3 = None


    def remove_dart(self):
        if self.dart3 is not None:
            self.dart3 = None
        elif self.dart2 is not None:
            self.dart2 = None
        elif self.dart1 is not None:
            self.dart1 = None
        else:
            print("Error: turn has no darts")


    def get_score(self):
        score = 0
        if self.dart1 is not None:
            score += self.dart1.get_score()
        if self.dart2 is not None:
            score += self.dart2.get_score()
        if self.dart3 is not None:
            score += self.dart3.get_score()
        return score

    
    def add_throws(self):
        print("Insert throws (<number><code>, code: a,b,c,d from outer to inner circle)")
        for i in range(c.N_DARTS):
            dart_code = ui.ask_for_dart_code()
            dart = Dart(dart_code)
            self.add_dart(dart)


    def fill(self):
        correct_turn = False
        while not correct_turn:
            self.remove_all_darts()
            self.add_throws()            
            print(self)
            correct_turn = ui.ask_for_confirmation("Is this turn correct? (Y/n): ")



class MatchTurn(Turn):
    def __init__(self, id=None, turn_order=None, player=None, dart1=None, dart2=None, dart3=None):
        self.turn_order = turn_order
        self.player = player
        super().__init__(id, dart1, dart2, dart3)


    def __str__(self):
        match_turn_str = ""

        if self.id:
            match_turn_str += f"Turn {self.turn_order} with id {self.id} - {self.player.name} - "
        else:
            match_turn_str += f"Turn {self.turn_order} - {self.player.name} - "

        match_turn_str += super().__str__()

        return match_turn_str
         

    def fill(self, cap=None):
        correct_turn = False
        while not correct_turn:
            self.remove_all_darts()
            self.add_throws(cap)
            print(self)
            correct_turn = ui.ask_for_confirmation("Is this turn correct? (Y/n): ")

        print(f"Turn score: {self.get_score()}")
        print(f"Remaining cap: {cap - self.get_score()}")


    def add_throws(self, cap=None):
        print("Insert throws (<number><code>, code: a,b,c,d from outer to inner circle)")
        for i in range(c.N_DARTS):
            dart_code = ui.ask_for_dart_code()
            dart = Dart(dart_code)
            self.add_dart(dart)
            if cap is not None:
                dart_score = dart.get_score()
                if dart_score > cap:
                    print(f"You exceeded the cap! Cap was {cap} and you scored {dart_score}")
                    self.remove_dart()
                    self.add_dart(Dart("0"))
                    continue
                if dart_score == cap:
                    print(f"Game over! You needed exactly {dart_score} to win!")
                    break
                cap -= dart_score



class TrainingTurn(Turn):
    def __init__(self, id=None, aim=None, dart1=None, dart2=None, dart3=None):
        super().__init__(id, dart1, dart2, dart3)
        self.aim = aim


    def __str__(self):
        return f"{self.dart1} {self.dart2} {self.dart3} aiming at {self.aim}"



class Dart:
    def __init__(self, code):
        self.code = code


    def __str__(self):
        return self.code


    def print_value(self):
        if not self.code[-1].isalpha():
            return self.code
        
        mult = u.sect_to_mult(self.code[-1])
        return f"{mult}{self.code[:-1]}"


    def set_code(self, code):
        self.code = code
    

    def get_score(self):
        if not self.code:
            return 0

        # if last character is not a letter, return the number
        if not self.code[-1].isalpha():
            return int(self.code)
        
        score = int(self.code[:-1])
        # if last character is a letter, return the number multiplied by the letter
        if self.code[-1] == "a":
            return score * 2
        elif self.code[-1] == "c":
            return score * 3
        else:
            return score



class Team:    
    def __init__(self, id=None, player1=None, player2=None, name=None, first_player=None):
        self.id = id
        self.player1 = player1
        self.player2 = player2
        self.name = name
        self.current_player = first_player


    def __str__(self):
        return f"Team {self.id} - {self.team_name()}"


    def add_player(self, player):
        if self.player1 is None:
            self.player1 = player
        elif self.player2 is None:
            self.player2 = player
        else:
            print("Error: team already has 2 players")


    def default_name(self):
        # name: first letter of all player names, capitalized
        name = self.player1.name[0].upper() + self.player2.name[0].upper()
        return name


    def next_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        
        return self.current_player



class Player:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    

    def __str__(self):
        return f"Player {self.id} - {self.name}"


    def __eq__(self, other):
        if self.id and other.id:
            return self.id == other.id
        else:
            return self.name == other.name