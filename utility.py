#Convert a guess to a dictionary
def guess_to_dict(answers, players):
    lstOfAns = answers.split(",")
    d = {}
    for i in range(len(lstOfAns)):
        d[str(players[i])] = str(lstOfAns[i])
    return d


#Based on answers, return a dictionary with correct answers
def get_correct_answer(s):
    values = s.get_all_values()
    solution = {}
    keys = list()
    vals = list()
    for player in values:
        keys.append(player[0])
        vals.append(player[3])
    for i in range(0, 4):
        solution[keys[i]] = vals[i]
    return solution

#Reset the sheet for a new game
def reset(s):
    cells = all_cells(s)
    for cell in cells:
        cell.value = "0"
    s.update_cells(cells)

#More utility
def col_cells(s, col):
    return s.range(1, col, 4, col)

#Clear the answers
def clear_answers(s):
    cells = col_cells(s, 4)
    for cell in cells:
        cell.value = "0"
    s.update_cells(cells)

#Utility
def all_cells(s):
    return s.range(1, 1, 4, 5)

#Clear the guesses
def clear_guesses(s):
    cells = col_cells(s, 5)
    for cell in cells:
        cell.value = "0"
    s.update_cells(cells)

#Update your score
def update_score(s, inc, row):
    score = int(s.cell(row, 2).value)
    s.update_cell(row, 2, score + inc)

#Send an answer
def send_answer(s, ans, row):
    s.update_cell(row, 4, ans)

#Send a guess
def send_guess(s, guess, row):
    s.update_cell(row, 5, guess)

#Read col
def read_col(s, col):
    return s.col_values(col)

#Check value at a cell
def check_cell(s, row, col, val):
    return s.cell(row, col).value == val

#Check col for zeroes
def check_col(s, col, v):
    vals = s.col_values(col)
    for val in vals:
        if val == v:
            return False
    return True
