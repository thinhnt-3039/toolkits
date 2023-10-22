import sys
import random

def parse_input(input_str):
        lines = input_str.split("\n")
        current_piece = list(map(int, lines[1].split(" ")))
        my_board = list(map(int, lines[2].split(" ")))
        return (current_piece, my_board)

def coordinates_to_index(col, row):
    return col * 9 + row

def coordinates_to_slot(col, row):
    return (col // 3) * 9 + row

def convert1to0(board):
    for i in range(0, 81):
        if board[i] == -1:
            board[i] = 0
    return(board)

def find_placeable_slots(board):
    slots = []
    for i in range(3):
        for j in range(9):
            c1 = board[coordinates_to_index(i * 3, j)]
            c2 = board[coordinates_to_index(i * 3 + 1, j)]
            c3 = board[coordinates_to_index(i * 3 + 2, j)]

            if c1 < 1 and c2 < 1 and c3 < 1:
                slots.append(coordinates_to_slot(i * 3, j))

    return slots

def score_board(board):
    list_row = []
    score_row = 0
    for i in range(0, 81):
        if (i+1)%9==0 or (i+2)%9==0:
            continue
        else:
            if board[i] == board[i+1] and board[i] == board[i+2]:
                list_row.append(i)
                list_row.append(i+1)
                list_row.append(i+2)
    for i in list(set(list_row)):
        score_row += board[i]

    list_col = []
    score_col = 0
    for i in range(0, 63):
        if board[i] == board[i+9] and board[i] == board[i+18]:
            list_col.append(i)
            list_col.append(i+9)
            list_col.append(i+18)
    for i in list(set(list_col)):
        score_col += board[i]

    list_cross_right = []
    score_cross_right = 0
    for i in range(0, 63):
        if (i+1)%9==0 or (i+2)%9==0:
            continue
        else:
            if board[i] == board[i+10] and board[i] == board[i+20]:
                list_cross_right.append(i)
                list_cross_right.append(i+10)
                list_cross_right.append(i+20)
    for i in list(set(list_cross_right)):
        score_cross_right += board[i]

    list_cross_left = []
    score_cross_left = 0
    for i in range(0, 63):
        if i%9==0 or (i-1)%9==0:
            continue
        else:
            if board[i] == board[i+8] and board[i] == board[i+16]:
                list_cross_left.append(i)
                list_cross_left.append(i+8)
                list_cross_left.append(i+16)
    for i in list(set(list_cross_left)):
        score_cross_left += board[i]  

    scrore_all = score_col + score_row + score_cross_left + score_cross_right
    return(scrore_all)  

def accumulation(board):
    list_row = []
    score_row = 0
    for i in range(0, 81):
        if (i+1)%9==0 or (i+2)%9==0:
            continue
        else:
            if (board[i] == board[i+1] and board[i+2] == 0) or (board[i] == board[i+2] and board[i+1] == 0) or (board[i+2] == board[i+1] and board[i] == 0):
                score_row += (board[i] + board[i+1] + board[i+2])/2*3

    list_col = []
    score_col = 0
    for i in range(0, 63):
        if (board[i] == board[i+9] and board[i+18] == 0) or (board[i] == board[i+18] and board[i+9] == 0) or (board[i+9] == board[i+18] and board[i] == 0):
            score_row += (board[i] + board[i+9] + board[i+18])/2*3*1.2

    list_cross_right = []
    score_cross_right = 0
    for i in range(0, 63):
        if (i+1)%9==0 or (i+2)%9==0:
            continue
        else:
            if (board[i] == board[i+10] and board[i+20] == 0) or (board[i] == board[i+20] and board[i+10] == 0) or (board[i+10] == board[i+20] and board[i] == 0):
                score_row += (board[i] + board[i+10] + board[i+20])/2*3*1.5

    list_cross_left = []
    score_cross_left = 0
    for i in range(0, 63):
        if i%9==0 or (i-1)%9==0:
            continue
        else:
            if (board[i] == board[i+8] and board[i+16] == 0) or (board[i] == board[i+16] and board[i+8] == 0) or (board[i+8] == board[i+16] and board[i] == 0):
                score_row += (board[i] + board[i+8] + board[i+16])/2*3*1.5

    scrore_all = score_col + score_row + score_cross_left + score_cross_right
    return(scrore_all)    



def space(list):
    final_list = []
    max_space = 0
    for place in list:
        space = 0
        for free_space in [place +1, place -1, place-9, place+9, place+10, place-10, place+8, place-8]:
            if free_space in placeables:
                space += 1
        if space > max_space:
            final_list = []
            max_space = space
            final_list.append(place)
        elif space == max_space:
            final_list.append(place)
    return(final_list)

def cal_space(place):
    space = 0
    for free_space in [place +1, place -1]:
        if free_space in placeables:
            space += 1
    return(space)
    
def main(placeables, my_board, current_piece, a, b, c):
    old_score = score_board(my_board)
    final_score = 0
    choose_list = []
    for place in placeables:
        new_board = my_board.copy()
        new_board[place + (place//9)*18] = current_piece[0]
        new_board[place + (place//9)*18 + 9] = current_piece[1]
        new_board[place + (place//9)*18 + 18] = current_piece[2]
        new_score = score_board(new_board)
        old_sc = accumulation(my_board)
        new_sc = accumulation(new_board)
        sc = new_sc - old_score
        space = cal_space(place)
        new_score = a*new_score + b*sc + c*space
        if new_score > final_score:
            choose_list = []
            final_score = new_score
            choose_list.append(place)
        elif new_score == final_score:
            choose_list.append(place)
    if choose_list == []:
        choose_list = placeables    
            
    # last_list = space(choose_list)
    output = random.choice(choose_list) 
    return(output)

input_str = ""
for line in sys.stdin:
    input_str += line

current_piece, my_board = parse_input(input_str)
my_board = convert1to0(my_board)
placeables = find_placeable_slots(my_board)
if (current_piece[1] == current_piece[0] or current_piece[1] == current_piece[0]) and (set([0, 1, 2, 3]).issubset(set(placeables))) and current_piece[1] == 7:
    output = random.choice([1, 2, 3])
elif (current_piece[1] == current_piece[0] or current_piece[1] == current_piece[0]) and (set([5, 6, 7, 8]).issubset(set(placeables))) and current_piece[1] == 8:
    output = random.choice([5, 6, 7])
elif (current_piece[1] == current_piece[0] or current_piece[1] == current_piece[0]) and (set([18, 19, 20, 21]).issubset(set(placeables))) and current_piece[1] == 9:
    output = random.choice([19, 20, 21])
elif (current_piece[1] == current_piece[0] or current_piece[1] == current_piece[0]) and (set([23, 24, 25, 26]).issubset(set(placeables))) and current_piece[1] == 10:
    output = random.choice([23, 24, 25])
elif sum(my_board) == 0:
    if current_piece[0] == current_piece[1]:
        output = random.choice([12,13,14])
        # output = random.choice([11,12,13,14,15,20,21,22,23,24]) 
    elif current_piece[2] == current_piece[1]:
        output = random.choice([12,13,14])
        # output = random.choice([11,12,13,14,2,3,4,5,6])
    # elif current_piece[0] == current_piece[1] and current_piece[2] == current_piece[1]:
    #     output = random.choice([11,12,13,14,15])
    elif current_piece[0] == current_piece[2]:
        output = random.choice([12,13,14])
        # output = random.choice([11,12,13,14,15])
    else:
        output = random.choice([11,15])
        # output = random.choice([1,2,3,4,5,6,7,19,20,21,22,23,24,25])
else:
    if len(placeables) > 20:
        output = main(placeables, my_board, current_piece, a = 0.8, b = 0.25, c = 15)
    else:
        output = main(placeables, my_board, current_piece, a = 1, b = 0.20, c = 7)

print(output)