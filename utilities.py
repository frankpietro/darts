import constants as c

def add_value_to_dict(key, dict):
    # if key is not in dict, add it with value 1, else add 1 to its value
    if key not in dict:
        dict[key] = 1
    else:
        dict[key] += 1


# method: 0 for key, 1 for value
def sort_dict(dict, method):
    # sort dict by value
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[method])}


# custom open file function
def open_file(filename):
    # read file training.txt
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    return lines


# validation of aim
def valid_aim(aim):
    # aim must be either between 1 and 20, 25 or 50
    return aim in c.BOARD_INPUTS


# validation of moltiplicator
def valid_moltiplicator(moltiplicator):
    # moltiplicator must be either s, d or t
    if moltiplicator.upper() in c.MOLTIPLICATORS or moltiplicator == "":
        return True


# validation of dart code
def valid_dart_code(code):
    if not code[-1].isalpha():
        if code not in ["0", "25", "50"]:
            return False
    else:
        if code[-1] not in ["a", "b", "c", "d", "A", "B", "C", "D"]:
            return False
        if code[:-1] not in c.BOARD_INPUTS or code[:-1] in ["0", "25", "50"]:
            return False
    
    return True


# convert sector a,b,c,d to eventual T or D multiplier
def sect_to_mult(sector):
    if sector == "a" or sector == "A":
        return "D"
    elif sector == "c" or sector == "C":
        return "T"
    else:
        return ""
