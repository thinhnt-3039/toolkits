from calendar import c


def get_line_expand_score(line):
    score = 0
    for i in range(0, len(line) - 2):
        value_check = line[i] + line[i + 1] + line[i + 2]
        # Nếu như có hơn 2 số trong chuỗi 3 thì mới tính
        if value_check < 14:
            continue
        else:
            if line[i] == line[i + 1] and line[i] == line[i + 2]:
                continue
            else:
                if line[i] == line[i + 1] and line[i + 2] == 0:
                    score += 1
                elif line[i] == line[i + 2] and line[i + 1] == 0:
                    score += 1
                elif line[i + 1] == line[i + 2] and line[i] == 0:
                    score += 1
                else:
                    continue
    return score


def get_line_result_score(line):
    score = 0
    for i in range(0, len(line) - 2):
        value_check = line[i] + line[i + 1] + line[i + 2]
        # Nếu như có hơn 2 số trong chuỗi 3 thì mới tính
        if value_check < 14:
            continue
        else:
            if line[i] == line[i + 1] and line[i] == line[i + 2]:
                score += 1
    return score


def get_line_loss_score(line):
    score = 0
    for i in range(0, len(line) - 2):
        value_check = line[i] + line[i + 1] + line[i + 2]

        if value_check < 14:
            continue
        else:
            if line[i] == line[i + 1] and line[i] == line[i + 2]:
                continue
            else:
                if line[i] == line[i + 1] and line[i + 2] == 0:
                    continue
                elif line[i] == line[i + 2] and line[i + 1] == 0:
                    continue
                elif line[i + 1] == line[i + 2] and line[i] == 0:
                    continue
                else:
                    score += 1
    return score


def get_board_expand_score(my_board):
    my_board = [0 if i == -1 else i for i in my_board]
    np_board = [my_board[i * 9 : i * 9 + 9] for i in range(9)]
    board_score = 0
    # row score
    for i in range(9):
        row = [np_board[i][j] for j in range(9)]
        board_score += get_line_expand_score(row)
    # column score
    for i in range(9):
        col = [np_board[j][i] for j in range(9)]
        board_score += get_line_expand_score(col)
    # diagonal score
    n = len(np_board)  # n=9
    for p in range(2 * n - 1):
        line = [np_board[p - q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]
        if len(line) >= 3:
            board_score += get_line_expand_score(line)
        if len(line) >= 3:
            line = [
                np_board[n - p + q - 1][q]
                for q in range(max(0, p - n + 1), min(p, n - 1) + 1)
            ]
        board_score += get_line_expand_score(line)
    return board_score


def get_board_loss_score(my_board):
    my_board = [0 if i == -1 else i for i in my_board]
    np_board = [my_board[i * 9 : i * 9 + 9] for i in range(9)]
    board_score = 0
    # row score
    for i in range(9):
        row = [np_board[i][j] for j in range(9)]
        board_score += get_line_loss_score(row)
    # column score
    for i in range(9):
        col = [np_board[j][i] for j in range(9)]
        board_score += get_line_loss_score(col)
    # diagonal score
    n = len(np_board)  # n=9
    for p in range(2 * n - 1):
        line = [np_board[p - q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]
        if len(line) >= 3:
            board_score += get_line_loss_score(line)
        if len(line) >= 3:
            line = [
                np_board[n - p + q - 1][q]
                for q in range(max(0, p - n + 1), min(p, n - 1) + 1)
            ]
        board_score += get_line_loss_score(line)
    return board_score


def get_board_result_score(my_board):
    my_board = [0 if i == -1 else i for i in my_board]
    np_board = [my_board[i * 9 : i * 9 + 9] for i in range(9)]
    board_score = 0
    # row score
    for i in range(9):
        row = [np_board[i][j] for j in range(9)]
        board_score += get_line_result_score(row)
    # column score
    for i in range(9):
        col = [np_board[j][i] for j in range(9)]
        board_score += get_line_result_score(col)
    # diagonal score
    n = len(np_board)  # n=9
    for p in range(2 * n - 1):
        line = [np_board[p - q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]
        if len(line) >= 3:
            board_score += get_line_result_score(line)
        if len(line) >= 3:
            line = [
                np_board[n - p + q - 1][q]
                for q in range(max(0, p - n + 1), min(p, n - 1) + 1)
            ]
        board_score += get_line_result_score(line)
    return board_score
