import mysql.connector

import constants as c
from secret_pw import DB_PW


def create_server_connection(host_name='localhost', user_name='root', user_password=DB_PW):
    # connect to server
    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password
    )

    return connection

# ------------------------------ DATABASE CREATION ------------------------------

def create_darts_db(cursor):
    # create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS " + c.TEST_DATABASE)
    cursor.execute("USE " + c.TEST_DATABASE)


def create_tables(cursor):
    # create match table
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + c.MATCH_TABLE + "` (`id` INT NOT NULL AUTO_INCREMENT, `team1_id` INT NULL, `team2_id` INT NULL, `player1_id` INT NULL, `player2_id` INT NULL, `datetime` DATETIME NULL, PRIMARY KEY (`id`))")
    # create set table
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + c.SET_TABLE + "` (`id` INT NOT NULL AUTO_INCREMENT, `match_id` INT NULL, PRIMARY KEY (`id`))")
    # create leg table
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + c.LEG_TABLE + "` (`id` INT NOT NULL AUTO_INCREMENT, `set_id` INT NULL, `leg_order` INT NULL, `goal` INT NULL, PRIMARY KEY (`id`))")
    # create throw table
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + c.MATCH_TURN_TABLE + "` (`id` INT NOT NULL AUTO_INCREMENT, `leg_id` INT NULL, `turn_order` INT NULL, `player_id` INT NULL, `dart1` VARCHAR(3) NULL, `dart2` VARCHAR(3) NULL, `dart3` VARCHAR(3) NULL, PRIMARY KEY (`id`))")
    # create player table
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + c.PLAYER_TABLE + "` (`id` INT NOT NULL AUTO_INCREMENT, `name` VARCHAR(255) NULL, PRIMARY KEY (`id`))")
    # create team table
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + c.TEAM_TABLE + "` (`id` INT NOT NULL AUTO_INCREMENT, `player1_id` INT NULL, `player2_id` INT NULL, `name` VARCHAR(255) NULL, PRIMARY KEY (`id`))")
    # create training session table
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + c.TRAINING_SESSION_TABLE + "` (`id` INT NOT NULL AUTO_INCREMENT, `datetime` DATETIME NULL, `player_id` INT NULL, PRIMARY KEY (`id`))")
    # create training turn table
    cursor.execute("CREATE TABLE IF NOT EXISTS `" + c.TRAINING_TURN_TABLE + "` (`id` INT NOT NULL AUTO_INCREMENT, `training_session_id` INT NULL, `aim` VARCHAR(4) NULL, `dart1` VARCHAR(3) NULL, `dart2` VARCHAR(3) NULL, `dart3` VARCHAR(3) NULL, PRIMARY KEY (`id`))")


def add_foreign_keys(cursor):
    # match table
    cursor.execute("ALTER TABLE `" + c.MATCH_TABLE + "` ADD FOREIGN KEY (`team1_id`) REFERENCES `" + c.TEAM_TABLE + "`(`id`)")
    cursor.execute("ALTER TABLE `" + c.MATCH_TABLE + "` ADD FOREIGN KEY (`team2_id`) REFERENCES `" + c.TEAM_TABLE + "`(`id`)")
    cursor.execute("ALTER TABLE `" + c.MATCH_TABLE + "` ADD FOREIGN KEY (`player1_id`) REFERENCES `" + c.PLAYER_TABLE + "`(`id`)")
    cursor.execute("ALTER TABLE `" + c.MATCH_TABLE + "` ADD FOREIGN KEY (`player2_id`) REFERENCES `" + c.PLAYER_TABLE + "`(`id`)")
    # set table
    cursor.execute("ALTER TABLE `" + c.SET_TABLE + "` ADD FOREIGN KEY (`match_id`) REFERENCES `" + c.MATCH_TABLE + "`(`id`)")
    # leg table
    cursor.execute("ALTER TABLE `" + c.LEG_TABLE + "` ADD FOREIGN KEY (`set_id`) REFERENCES `" + c.SET_TABLE + "`(`id`)")
    # turn table
    cursor.execute("ALTER TABLE `" + c.MATCH_TURN_TABLE + "` ADD FOREIGN KEY (`leg_id`) REFERENCES `" + c.LEG_TABLE + "`(`id`)")
    cursor.execute("ALTER TABLE `" + c.MATCH_TURN_TABLE + "` ADD FOREIGN KEY (`player_id`) REFERENCES `" + c.PLAYER_TABLE + "`(`id`)")
    # team table
    cursor.execute("ALTER TABLE `" + c.TEAM_TABLE + "` ADD FOREIGN KEY (`player1_id`) REFERENCES `" + c.PLAYER_TABLE + "`(`id`)")
    cursor.execute("ALTER TABLE `" + c.TEAM_TABLE + "` ADD FOREIGN KEY (`player2_id`) REFERENCES `" + c.PLAYER_TABLE + "`(`id`)")
    # training session table
    cursor.execute("ALTER TABLE `" + c.TRAINING_SESSION_TABLE + "` ADD FOREIGN KEY (`player_id`) REFERENCES `" + c.PLAYER_TABLE + "`(`id`)")
    # training turn table
    cursor.execute("ALTER TABLE `" + c.TRAINING_TURN_TABLE + "` ADD FOREIGN KEY (`training_session_id`) REFERENCES `" + c.TRAINING_SESSION_TABLE + "`(`id`)")

# ------------------------------ END DATABASE CREATION ------------------------------


# ------------------------------ SELECT ------------------------------

def search_player(name, conn):
    cursor = conn.cursor()
    search_player_str = "SELECT * FROM `" + c.PLAYER_TABLE + "` WHERE `name` = '" + name + "'"
    cursor.execute(search_player_str)
    result = cursor.fetchall()

    if len(result) == 1:
        return result[0][0]

    return None


def search_team(player1_id, player2_id, conn):
    cursor = conn.cursor()
    search_team_str = "SELECT * FROM `" + c.TEAM_TABLE + "` WHERE `player1_id` = " + str(player1_id) + " AND `player2_id` = " + str(player2_id) + " OR `player1_id` = " + str(player2_id) + " AND `player2_id` = " + str(player1_id)
    cursor.execute(search_team_str)
    result = cursor.fetchall()

    if len(result) == 1:
        return result[0][0], result[0][3]

    return None, None

# ------------------------------ END SELECT ------------------------------


# ------------------------------ INSERT ------------------------------

def insert_player(name, conn):
    cursor = conn.cursor()
    insert_player_str = "INSERT INTO `" + c.PLAYER_TABLE + "` (`name`) VALUES ('" + name + "')"
    cursor.execute(insert_player_str)
    conn.commit()
    return cursor.lastrowid


def insert_training_session(training_session, conn):
    cursor = conn.cursor()
    insert_training_session_str = "INSERT INTO `" + c.TRAINING_SESSION_TABLE + "` (`datetime`, `player_id`) VALUES ('" + str(training_session.datetime.strftime(c.SQL_DATETIME_FORMAT)) + "', " + str(training_session.player.id) + ")"
    cursor.execute(insert_training_session_str)
    conn.commit()
    return cursor.lastrowid


def insert_training_turn(training_turn, training_session_id, conn):
    cursor = conn.cursor()
    insert_training_turn_str = f"INSERT INTO `{c.TRAINING_TURN_TABLE}` (`training_session_id`, `aim`, `dart1`, `dart2`, `dart3`) VALUES ({training_session_id}, '{training_turn.aim}', '{training_turn.dart1.code}', '{training_turn.dart2.code}', '{training_turn.dart3.code}')"
    cursor.execute(insert_training_turn_str)
    conn.commit()
    return cursor.lastrowid


def insert_team(player1_id, player2_id, name, conn):
    cursor = conn.cursor()
    insert_team_str = "INSERT INTO `" + c.TEAM_TABLE + "` (`player1_id`, `player2_id`, `name`) VALUES (" + str(player1_id) + ", " + str(player2_id) + ", '" + name + "')"
    cursor.execute(insert_team_str)
    conn.commit()
    return cursor.lastrowid

# ------------------------------ END INSERT ------------------------------


# ------------------------------ PLAYER REGISTRATION ------------------------------

def register_player(name, conn):
    id = search_player(name, conn)

    if id:
        return False, id
    else:
        return True, insert_player(name, conn)

# ------------------------------ END PLAYER REGISTRATION ------------------------------


# ------------------------------ TRAINING ------------------------------

def save_training_session(training_session, conn):
    ts_id = insert_training_session(training_session, conn)
    
    for t in training_session.turns:
        insert_training_turn(t, ts_id, conn)

# ------------------------------ END TRAINING ------------------------------


# ------------------------------ MATCH ------------------------------



# ------------------------------ END MATCH ------------------------------