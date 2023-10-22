from curses import getsyx
import re
import sys
import copy
import random
from utils import *


def parse_input(input_str):
    lines = input_str.split("\n")
    current_piece = list(map(int, lines[1].split(" ")))
    my_board = list(map(int, lines[2].split(" ")))
    return (current_piece, my_board)


def coordinates_to_index(col, row):
    return col * 9 + row


def coordinates_to_slot(col, row):
    return (col // 3) * 9 + row


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


def update_board(random_input, index, board):
    for i in range(3):
        for j in range(9):
            if i == 0:
                if (i + j) == index:
                    board[coordinates_to_index(i * 3, j)] = random_input[0]
                    board[coordinates_to_index(i * 3 + 1, j)] = random_input[1]
                    board[coordinates_to_index(i * 3 + 2, j)] = random_input[2]
            else:
                if (i * 9) + j == index:
                    board[coordinates_to_index(i * 3, j)] = random_input[0]
                    board[coordinates_to_index(i * 3 + 1, j)] = random_input[1]
                    board[coordinates_to_index(i * 3 + 2, j)] = random_input[2]

    return board


def get_type_input(random_input):
    if random_input[0] == random_input[1] and random_input[1] == random_input[2]:
        return 0
    elif random_input[0] == random_input[1]:
        return 1
    elif random_input[1] == random_input[2]:
        return 2
    else:
        return 3


def chose_fist_index(random_input, placeables):
    all_edge_index = [0, 8, 9, 17, 18, 26]
    all_middle_index = [10, 11, 12, 13, 14, 15, 16]
    all_top_index = [i for i in range(1, 8)]
    all_bottom_index = [i for i in range(18, 26)]

    edge_index = [i for i in all_edge_index if i in placeables]
    middle_index = [i for i in all_middle_index if i in placeables]
    top_index = [i for i in all_top_index if i in placeables]
    bottom_index = [i for i in all_bottom_index if i in placeables]

    if get_type_input(random_input) == 0:
        index = random.choice(middle_index)

    elif get_type_input(random_input) == 1:
        index = random.choice(bottom_index)

    elif get_type_input(random_input) == 2:
        index = random.choice(top_index)

    else:
        index = random.choice(edge_index)

    return index


def get_index_base_expand_score(random_input, index_input, board):
    placeables = find_placeable_slots(board)

    # điểm mở rộng
    best_score = 0
    best_expand_score = 0
    all_expand_score = []
    all_score = []

    for index in range(len(placeables)):
        my_board = copy.deepcopy(board)
        my_board = update_board(random_input, placeables[index], my_board)

        all_expand_score.append(get_expand_score(my_board, index_input))
        all_score.append(get_board_score(my_board))

        if get_expand_score(my_board, index_input) > best_expand_score:
            best_expand_score = get_expand_score(my_board, index_input)

        if get_board_score(my_board) > best_score:
            best_score = get_board_score(my_board)

    # nếu như chưa có điểm mở rộng thì random ví trị đầu tiên
    if best_expand_score <= 4:
        best_index = chose_fist_index(random_input, placeables)
        return best_index

    # lấy ra những index có dùng điểm expand score
    list_best_index_base_expand_score = []
    for index in range(len(all_expand_score)):
        if all_expand_score[index] == best_expand_score:
            list_best_index_base_expand_score.append(index)

    # Trong những thằng có điểm expand score lấy ra những thằng có tổng điểm cao nhất
    if best_score == 0:
        list_choice_index = [
            placeables[index] for index in list_best_index_base_expand_score
        ]
        best_index = random.choice(list_choice_index)
        return best_index

    else:
        # tìm max_score
        best_score = 0
        for index in list_best_index_base_expand_score:
            if all_score[index] > best_score:
                best_score = all_score[index]

        # lấy ra những thằng cùng max_score
        list_best_index_base_all_score = []
        for index in list_best_index_base_expand_score:
            if all_score[index] == best_score:
                list_best_index_base_all_score.append(index)

        list_choice_index = [
            placeables[index] for index in list_best_index_base_all_score
        ]
        best_index = random.choice(list_choice_index)
        return best_index


def get_index_base_all_score(random_input, board):
    placeables = find_placeable_slots(board)
    best_score = 0
    all_score = []

    # Tìm ra điểm cao nhất
    for index in range(len(placeables)):
        my_board = copy.deepcopy(board)
        my_board = update_board(random_input, placeables[index], my_board)

        all_score.append(get_board_score(my_board))

        if get_board_score(my_board) > best_score:
            best_score = get_board_score(my_board)

    # lấy ra những thằng cùng max_score
    list_best_index_base_all_score = []
    for index in range(len(placeables)):
        if all_score[index] == best_score:
            list_best_index_base_all_score.append(index)

    list_choice_index = [placeables[index] for index in list_best_index_base_all_score]
    best_index = random.choice(list_choice_index)
    return best_index


def get_index_input(placeables):
    return 27 - len(placeables)


def main():
    # init board

    pieces = [[9, 7, 7], [10, 10, 9], [8, 8, 8]]
    my_board = [-1] * 81
    for idx, random_input in enumerate(pieces):
        # print(random_input)
        if idx <= 21:
            if idx == 0:
                placeables = find_placeable_slots(my_board)
                first_index = chose_fist_index(random_input, placeables)
                my_board = update_board(random_input, first_index, my_board)

            best_index = get_index_base_expand_score(random_input, idx, my_board)
            my_board = update_board(random_input, best_index, my_board)
            copy_board = copy.deepcopy(my_board)
            # print(get_board_score(copy_board))
        else:
            placeables = find_placeable_slots(my_board)
            if placeables == []:
                return
            index = get_index_base_all_score(random_input, my_board)
            my_board = update_board(random_input, index, my_board)
            copy_board = copy.deepcopy(my_board)
            print(get_board_score(copy_board))


main()
# input_str = ""
# for line in sys.stdin:
#     input_str += li
# current_piece, my_board = parse_input(input_str)
# placeables = find_placeable_slots(my_board)
# output = random.choice(placeables)

# print(output)
