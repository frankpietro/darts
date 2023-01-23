import datetime as dt
import numpy as np

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
        conn.commit()
        self.id = cursor.lastrowid



class Match(DatabaseEntity):
    def __init__(self, id=None, team1=None, team2=None, player1=None, player2=None, datetime=dt.datetime.now(), sets=[], first_thrower=None):
        super().__init__(id)
        self.team1 = team1
        self.team2 = team2
        self.player1 = player1
        self.player2 = player2
        self.datetime = datetime
        self.sets = sets
        self.current_thrower = first_thrower
        

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

    # --------------------- DB queries ---------------------

    def insert_string(self):
        if self.team1 and self.team2:
            insert_str = "INSERT INTO `" + c.MATCH_TABLE + "` (`team1_id`, `team2_id`, `datetime`) VALUES (" + str(self.team1.id) + ", " + str(self.team2.id) + ", '" + str(self.datetime.strftime(c.SQL_DATETIME_FORMAT)) + "')"
        else:
            insert_str = "INSERT INTO `" + c.MATCH_TABLE + "` (`player1_id`, `player2_id`, `datetime`) VALUES (" + str(self.player1.id) + ", " + str(self.player2.id) + ", '" + str(self.datetime.strftime(c.SQL_DATETIME_FORMAT)) + "')"
        
        return insert_str

    # --------------------- end DB queries ---------------------


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
        
        if self.team1 and self.team2:
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

        return self.current_thrower
    

    
class Set(DatabaseEntity):
    def __init__(self, id=None, match_id=None, set_order=None, legs=[]):
        super().__init__(id)
        self.set_order = set_order
        self.match_id = match_id
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

    # --------------------- DB queries ---------------------

    def insert_string(self):
        insert_str = "INSERT INTO `" + c.SET_TABLE + "` (`match_id`, `set_order`) VALUES (" + str(self.match_id) + ", " + str(self.set_order) + ")"
        return insert_str

    # --------------------- end DB queries ---------------------


    def set_id(self, id):
        self.id = id

    
    def add_leg(self, leg):
        self.legs.append(leg)



class Leg(DatabaseEntity):
    def __init__(self, id=None, set_id=None, leg_order=None, goal=None, turns=[]):
        super().__init__(id)
        self.set_id = set_id
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

    # --------------------- DB queries ---------------------

    def insert_string(self):
        insert_str = "INSERT INTO `" + c.LEG_TABLE + "` (`set_id`, `leg_order`, `goal`) VALUES (" + str(self.set_id) + ", " + str(self.leg_order) + ", " + str(self.goal) + ")"
        return insert_str

    # --------------------- end DB queries ---------------------
        


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
    


class TrainingSession(DatabaseEntity):
    def __init__(self, id=None, datetime=dt.datetime.now(), player=None, turns=[]):
        super().__init__(id)
        self.datetime = datetime
        self.player = player
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

    # --------------------- DB queries ---------------------

    def insert_string(self):
        insert_str = "INSERT INTO `" + c.TRAINING_SESSION_TABLE + "` (`datetime`, `player_id`) VALUES ('" + str(self.datetime.strftime(c.SQL_DATETIME_FORMAT)) + "', " + str(self.player.id) + ")"
        return insert_str

    # --------------------- end DB queries ---------------------


    def add_turn(self, turn):
        self.turns.append(turn)

    
    def print_statistics(self):
        total_shots = {}
        total_scores = {}
        hits = {}
        zeros = {}
        close_shots = {}
        score_distr = {}
        

        for t in self.turns:
            print(t)
            aim = t.get_aim()
            # create an entry in each dict with aim as key if it does not exist
            if aim not in total_shots:
                total_shots[aim] = 0
                total_scores[aim] = 0
                hits[aim] = 0
                zeros[aim] = 0
                close_shots[aim] = 0
                score_distr[aim] = np.zeros(c.SCORE_GROUPS)

            total_shots[aim] += t.get_shots()
            total_scores[aim] += t.get_score()
            hits[aim] += t.get_hits()
            zeros[aim] += t.get_zeros()
            close_shots[aim] += t.get_close_shots(aim)
            score_distr[aim][t.get_score()//c.SCORE_GROUP_SIZE] += 1
        
        # for each aim, print statistics
        for aim in total_shots:
            print(f"While aiming at {aim}:")
            print(f"- total shots: {total_shots[aim]}")
            print(f"- total hits: {hits[aim]}")
            
            print(f"- total zeros: {zeros[aim]}")
            print(f"- average score: {round(total_scores[aim] / len(self.turns), 2)}")
            print(f"- hit percentage: {u.perc(hits[aim] / total_shots[aim])}")
            print(f"- zero percentage: {u.perc(zeros[aim] / total_shots[aim])}")
            print(f"- close shot percentage: {u.perc(close_shots[aim] / total_shots[aim])}")
            print("")
            print("Score distribution:")
            for i, score in enumerate(score_distr[aim]):
                print(f"{i*c.SCORE_GROUP_SIZE}-{(i+1)*c.SCORE_GROUP_SIZE - 1}: {score}")



class Turn(DatabaseEntity):
    def __init__(self, id=None, dart1=None, dart2=None, dart3=None):
        super().__init__(id)
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


    # --------------------- DB queries ---------------------

    def insert_string(self):
        raise NotImplementedError("Turns are not stored in the database by themselves")

    # --------------------- end DB queries ---------------------

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


    def get_zeros(self):
        zeros = 0
        for d in [self.dart1, self.dart2, self.dart3]:
            if d is not None and d.get_score() == 0:
                zeros += 1
        return zeros


    def get_shots(self):
        shots = 0
        for d in [self.dart1, self.dart2, self.dart3]:
            if d.get_code() is not None:
                shots += 1
        return shots


    def get_close_shots(self, aim):
        close_shots = 0
        for d in [self.dart1, self.dart2, self.dart3]:
            if d is not None and d.is_close(aim):
                close_shots += 1
        return close_shots


class MatchTurn(Turn):
    def __init__(self, id=None, leg_id=None, turn_order=None, player=None, dart1=None, dart2=None, dart3=None):
        super().__init__(id, dart1, dart2, dart3)
        self.leg_id = leg_id
        self.turn_order = turn_order
        self.player = player


    def __str__(self):
        match_turn_str = ""

        if self.id:
            match_turn_str += f"Turn {self.turn_order} with id {self.id} - {self.player.name} - "
        else:
            match_turn_str += f"Turn {self.turn_order} - {self.player.name} - "

        match_turn_str += super().__str__()

        return match_turn_str

    # --------------------- DB queries ---------------------

    def insert_string(self):
        insert_str = "INSERT INTO `" + c.MATCH_TURN_TABLE + "` (`leg_id`, `player_id`, `turn_order`, `dart1`, `dart2`, `dart3`) VALUES (" + str(self.leg_id) + ", " + str(self.player.id) + ", " + str(self.turn_order) + ", '" + str(self.dart1) + "', '" + str(self.dart2) + "', '" + str(self.dart3) + "')"
        return insert_str

    # --------------------- end DB queries ---------------------

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
                    # add empty darts to fill the turn
                    for j in range(i+1, c.N_DARTS):
                        self.add_dart(Dart())
                    break
                cap -= dart_score


    def fill(self, cap=None):
        correct_turn = False
        while not correct_turn:
            self.remove_all_darts()
            self.add_throws(cap)
            print(self)
            correct_turn = ui.ask_for_confirmation("Is this turn correct? (Y/n): ")

        print(f"Turn score: {self.get_score()}")
        print(f"Remaining cap: {cap - self.get_score()}")



class TrainingTurn(Turn):
    def __init__(self, id=None, dart1=None, dart2=None, dart3=None, aim=None, training_session_id=None):
        super().__init__(id, dart1, dart2, dart3)
        self.aim = aim
        self.training_session_id = training_session_id


    def __str__(self):
        return f"{self.dart1} {self.dart2} {self.dart3} aiming at {self.aim}"

    # --------------------- DB queries ---------------------

    def insert_string(self):
        insert_str = f"INSERT INTO `{c.TRAINING_TURN_TABLE}` (`training_session_id`, `aim`, `dart1`, `dart2`, `dart3`) VALUES ({self.training_session_id}, '{self.aim}', '{self.dart1}', '{self.dart2}', '{self.dart3}')"
        return insert_str

    # --------------------- end DB queries ---------------------

    def get_aim(self):
        return self.aim

    
    def get_hits(self):
        hits = 0
        for dart in [self.dart1, self.dart2, self.dart3]:
            # if aim is bull, hits are all darts that are in BULL_VALUES
            if self.aim == c.BULL:
                # no other ways of scoring 25 or 50
                if dart.get_score() in c.BULL_VALUES:
                    hits += 1
            # if aim is double or triple, only those are hits
            elif self.aim[-1] in c.SECTORS:
                if dart.get_code() == self.aim:
                    hits += 1
            
            # if aim is a number, hits are all darts that are in the same segment
            else:
                code = dart.get_code()
                if code[-1] in c.SECTORS:
                    code = code[:-1]
                if code == self.aim:
                    hits += 1

        return hits


    

class Team(DatabaseEntity):    
    def __init__(self, id=None, player1=None, player2=None, name=None, first_player=None):
        super().__init__(id)
        self.player1 = player1
        self.player2 = player2
        self.name = name
        self.current_player = first_player


    def __str__(self):
        return f"Team {self.id} - {self.name}"

    # --------------------- DB queries ---------------------

    def insert_string(self):
        insert_str = f"INSERT INTO `{c.TEAM_TABLE}` (`player1_id`, `player2_id`, `name`) VALUES ({self.player1.id}, {self.player2.id}, '{self.name}')"
        return insert_str
    
    # --------------------- end DB queries ---------------------

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
        if not self.current_player or self.current_player == self.player2:
            self.current_player = self.player1
        else:
            self.current_player = self.player2
        
        return self.current_player



class Player(DatabaseEntity):
    def __init__(self, id=None, name=None):
        super().__init__(id)
        self.name = name
    

    def __str__(self):
        return f"Player {self.id} - {self.name}"


    def __eq__(self, other):
        if self.id and other.id:
            return self.id == other.id
        else:
            return self.name == other.name

    # --------------------- DB queries ---------------------

    def insert_string(self):
        insert_str = f"INSERT INTO `{c.PLAYER_TABLE}` (`name`) VALUES ('{self.name}')"
        return insert_str

    # --------------------- end DB queries ---------------------

    def change_name(self, new_name):
        self.name = new_name



class Dart:
    def __init__(self, code=None):
        self.code = code


    def __str__(self):
        if self.code:
            return self.code
        else:
            return "-"


    def print_value(self):
        if not self.code[-1].isalpha():
            return self.code
        
        mult = u.sect_to_mult(self.code[-1])
        return f"{mult}{self.code[:-1]}"


    def set_code(self, code):
        self.code = code

    
    def get_code(self):
        return self.code
    

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


    def get_sector(self):
        if not self.code:
            return None

        if self.code[-1].isalpha():
            return self.code[-1]
        else:
            return None


    def get_segment(self):
        if not self.code:
            return None

        if self.code[-1].isalpha():
            return self.code[:-1]
        else:
            return self.code


    def is_close(self, aim):
        # if aim is bull, any shot with sector d is close
        if aim == c.BULL:
            if self.get_sector() == "d":
                return True
            else:
                return False

        # if aim is double, only doubles of close segments and sector b of same segment are close
        elif aim[-1] == "a":
            if self.get_sector() == "a" and u.is_neighbor(self.get_segment(), aim[:-1]):
                return True
            elif self.get_sector() == "b" and self.get_segment() == aim[:-1]:
                return True
            else:
                return False

        # if aim is triple, only triples of close segments and sector b and d of same segment are close
        elif aim[-1] == "c":
            if self.get_sector() == "c" and u.is_neighbor(self.get_segment(), aim[:-1]):
                return True
            elif self.get_sector() in ["b", "d"] and self.get_segment() == aim[:-1]:
                return True
            else:
                return False

        # if aim is a number, any shot in a close segment is close
        else:
            if u.is_neighbor(self.get_segment(), aim):
                return True
            else:
                return False

        
