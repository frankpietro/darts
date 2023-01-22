import itertools
import datetime as dt

import utilities as u


class Match:
    def __init__(self, id=None, team1=None, team2=None, datetime=dt.datetime.now(), sets=[]):
        self.id = id
        self.team1 = team1
        self.team2 = team2
        self.datetime = datetime
        self.sets = sets


    def __str__(self):
        # timestamp_str: dd-mm-yyyy hh:mm
        timestamp_str = self.datetime.strftime("%d-%m-%Y %H:%M")

        match_str = f"Match {self.id} - {timestamp_str}\n"
        match_str += f"Team 1: {self.team1}\n"
        match_str += f"Team 2: {self.team2}\n"

        return match_str


    def __eq__(self, other):
        return self.id == other.id


    def add_team(self, team):
        self.teams.append(team)

    

class Set:
    id_iter = itertools.count()

    def __init__(self, id, order):
        self.id = id
        self.order = order
        self.legs = []


    def __str__(self):
        if self.id:
            return f"Set {self.order} with id {self.id}"
        else:
            return f"Set {self.order}"


    def __eq__(self, other):
        if self.id and other.id:
            return self.id == other.id
        elif not (self.id or other.id):
            return self.legs == other.legs
        else:
            return False



class Leg:
    def __init__(self, id=None, order=None, turns=[]):
        self.id = id
        self.order = order
        self.turns = turns

    
    def __str__(self):
        if self.id:
            return f"Leg {self.order} with id {self.id}"
        else:
            return f"Leg {self.order}"
    


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
    def __init__(self, dart1=None, dart2=None, dart3=None):
        self.dart1 = dart1
        self.dart2 = dart2
        self.dart3 = dart3


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


    def get_score(self):
        score = 0
        if self.dart1 is not None:
            score += self.dart1.score
        if self.dart2 is not None:
            score += self.dart2.score
        if self.dart3 is not None:
            score += self.dart3.score
        return score



class MatchTurn(Turn):
    def __init__(self, id=None, order=None, player=None, dart1=None, dart2=None, dart3=None):
        self.order = order
        self.player = player
        self.id = id
        super().__init__(dart1, dart2, dart3)


    def __str__(self):
        return f"Turn {self.id} - {self.player_id} - {self.dart1.print_value()} {self.dart2.print_value()} {self.dart3.print_value()}"


class TrainingTurn(Turn):
    def __init__(self, id=None, aim=None, dart1=None, dart2=None, dart3=None):
        super().__init__(dart1, dart2, dart3)
        self.aim = aim
        self.id = id


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
    

    def get_score(self, code):
        if not code:
            return 0

        # if last character is not a letter, return the number
        if not code[-1].isalpha():
            return int(code)
        
        score = int(code[:-1])
        # if last character is a letter, return the number multiplied by the letter
        if code[-1] == "a":
            return score * 2
        elif code[-1] == "c":
            return score * 3
        else:
            return score



class Team:
    id_iter = itertools.count()
    
    def __init__(self, name):
        self.id = next(self.id_iter)
        self.players = []


    def __str__(self):
        return f"Team {self.id} - {self.team_name()}"


    def add_player(self, player):
        self.players.append(player)


    def team_name(self):
        if len(self.players) == 0:
            return "-"

        # name: first letter of all player names, capitalized
        name = ""
        for player in self.players:
            name += player.name[0].upper()

        return name



class Player:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    

    def __str__(self):
        return f"Player {self.id} - {self.name}"