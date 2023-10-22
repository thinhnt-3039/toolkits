import copy
import random
from utils import *
from score import *
import numpy as np


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


def get_index_base_expand_score(
    random_input, placeables, board, old_loss_score, old_result_score, idx
):
    placeables = find_placeable_slots(board)
    all_expand_score = []
    all_loss_score = []
    all_result_score = []
    for index in range(len(placeables)):
        my_board = copy.deepcopy(board)
        my_board = update_board(random_input, placeables[index], my_board)

        expand_score = get_board_expand_score(my_board)
        loss_score = get_board_loss_score(my_board)
        new_result_score = get_board_result_score(my_board)
        result_score = new_result_score - old_result_score
        new_loss_score = loss_score - old_loss_score

        all_expand_score.append(expand_score)
        all_loss_score.append(new_loss_score)
        all_result_score.append(result_score)
    if idx < 5:
        list_result_check = []
        for expand_score, loss_score, result_score in zip(
            all_expand_score, all_loss_score, all_result_score
        ):
            result_check = 3 * result_score - loss_score + expand_score
            list_result_check.append(result_check)
        max_result_chekc = max(list_result_check)

        best_index_expand_score = []
        for index in range(len(placeables)):
            if list_result_check[index] == max_result_chekc:
                best_index_expand_score.append(index)

    elif idx < 10:
        list_result_check = []
        for expand_score, loss_score, result_score in zip(
            all_expand_score, all_loss_score, all_result_score
        ):
            result_check = 4 * result_score - loss_score + expand_score
            list_result_check.append(result_check)

        max_result_chekc = max(list_result_check)

        best_index_expand_score = []
        for index in range(len(placeables)):
            if list_result_check[index] == max_result_chekc:
                best_index_expand_score.append(index)

    else:
        list_result_check = []
        for expand_score, loss_score, result_score in zip(
            all_expand_score, all_loss_score, all_result_score
        ):
            result_check = expand_score - loss_score + 5 * result_score
            list_result_check.append(result_check)

        max_result_chekc = max(list_result_check)

        best_index_expand_score = []
        for index in range(len(placeables)):
            if list_result_check[index] == max_result_chekc:
                best_index_expand_score.append(index)

    return best_index_expand_score


def get_index_base_result_score(
    random_input, placeables, board, old_loss_score, old_result_score, idx
):
    placeables = find_placeable_slots(board)
    all_loss_score = []
    all_result_score = []
    all_expand_score = []
    for index in range(len(placeables)):
        my_board = copy.deepcopy(board)
        my_board = update_board(random_input, placeables[index], my_board)
        loss_score = get_board_loss_score(my_board)
        new_loss_score = loss_score - old_loss_score
        expand_score = get_board_expand_score(my_board)
        new_result_score = get_board_result_score(my_board)
        result_score = new_result_score - old_result_score
        result_score = get_board_result_score(my_board)

        all_loss_score.append(new_loss_score)
        all_result_score.append(result_score)
        all_expand_score.append(expand_score)

    if idx < 21:
        list_result_check = []
        for expand_score, loss_score, result_score in zip(
            all_expand_score, all_loss_score, all_result_score
        ):
            result_check = 4 * result_score - loss_score + expand_score
            list_result_check.append(result_check)

        max_result_chekc = max(list_result_check)
        best_index_expand_score = []
        for index in range(len(placeables)):
            if list_result_check[index] == max_result_chekc:
                best_index_expand_score.append(index)

    else:
        list_result_check = []
        for expand_score, loss_score, result_score in zip(
            all_expand_score, all_loss_score, all_result_score
        ):
            result_check = 3 * result_score - loss_score + expand_score
            list_result_check.append(result_check)

        max_result_chekc = max(list_result_check)
        best_index_expand_score = []
        for index in range(len(placeables)):
            if list_result_check[index] == max_result_chekc:
                best_index_expand_score.append(index)

    return best_index_expand_score
