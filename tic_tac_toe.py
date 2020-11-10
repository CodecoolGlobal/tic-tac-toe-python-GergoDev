import sys
import os
import time
from numpy import random


def init_board():
    board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    return board


def switch_player(player, first_run):
    if first_run:
        return player
    elif player == "O":
        return "X"
    elif player == "X":
        return "O"


def get_move(board, player):
    alphabet_to_index = {'A': 0, 'B': 1, 'C': 2}
    numbers_to_index = {'1': 0, '2': 1, '3': 2}
    alphabet_valid = ["C", "B", "A"]
    numbers_valid = ["1", "2", "3"]
    while True:
        print(f"It's {player}'s turn")
        move_pos = input("Please enter your move: ")
        move_pos = move_pos.upper()
        if move_pos == "QUIT":
            os.system("clear")
            print("Good bye!")
            time.sleep(1.3)
            os.system("clear")
            sys.exit(0)
        if move_pos != "" and len(move_pos) == 2:
            row = list(move_pos)[0]
            col = list(move_pos)[1]
            if row in alphabet_valid and col in numbers_valid and board[alphabet_to_index[row]][numbers_to_index[col]] == ".":
                return (alphabet_to_index[row], numbers_to_index[col])
        else:
            print("Please enter a valid position! A-C, 1-3")


def possible_win(board, player):
    one_step_win_coordinates = []
    two_step_win_coordinates = []
    three_step_win_coordinates = []
    go_for_tie = []
    situations = [
        [[0, 0], [0, 1], [0, 2]],
        [[1, 0], [1, 1], [1, 2]],
        [[2, 0], [2, 1], [2, 2]],
        [[0, 0], [1, 0], [2, 0]],
        [[0, 1], [1, 1], [2, 1]],
        [[0, 2], [1, 2], [2, 2]],
        [[0, 0], [1, 1], [2, 2]],
        [[0, 2], [1, 1], [2, 0]]
    ]
    for situation in situations:
        player_result_count = 0
        opponent_result_count = 0
        for pos in situation:
            pos_content = board[pos[0]][pos[1]]
            if pos_content != ".":
                if pos_content == player:
                    player_result_count += 1
                else:
                    opponent_result_count += 1
        if player_result_count == 2 and opponent_result_count == 0:
            one_step_win_coordinates.append(situation)
        elif player_result_count == 1 and opponent_result_count == 0:
            two_step_win_coordinates.append(situation)
        elif player_result_count == 0 and opponent_result_count == 0:
            three_step_win_coordinates.append(situation)
        elif player_result_count == 1 and opponent_result_count == 1:
            go_for_tie.append(situation)
    return [
        one_step_win_coordinates,
        two_step_win_coordinates,
        three_step_win_coordinates,
        go_for_tie
    ]


def pick_possible_coordinate(board, situation):
    possible_coordinates = []
    for coordinate in situation:
        pos_content = board[coordinate[0]][coordinate[1]]
        if pos_content == ".":
            possible_coordinates.append(coordinate)
    size = len(possible_coordinates)
    index = random.randint(size) if size > 1 else 0
    return possible_coordinates[index]


def get_ai_move(board, player, difficulty):
    win_coordinates = possible_win(board, player)
    one_step_win_coordinates, two_step_win_coordinates, three_step_win_coordinates, go_for_tie = win_coordinates
    selected_situation = None
    print("One step win: ", one_step_win_coordinates)
    print("\n")
    print("Two step win: ", two_step_win_coordinates)
    print("\n")
    print("Three step win: ", three_step_win_coordinates)
    print("\n")
    print("Go for tie: ", go_for_tie)
    if difficulty == 1:
        if len(three_step_win_coordinates) != 0:
            size = len(three_step_win_coordinates)
            index = random.randint(size)
            selected_situation = three_step_win_coordinates[index]
        elif len(two_step_win_coordinates) != 0:
            size = len(two_step_win_coordinates)
            index = random.randint(size)
            selected_situation = two_step_win_coordinates[index]
        elif len(three_step_win_coordinates) != 0:
            size = len(one_step_win_coordinates)
            index = random.randint(size)
            selected_situation = one_step_win_coordinates[index]
        else:
            size = len(go_for_tie)
            index = random.randint(size)
            selected_situation = go_for_tie[index]
    elif difficulty == 2:
        if len(one_step_win_coordinates) != 0:
            size = len(one_step_win_coordinates)
            index = random.randint(size)
            selected_situation = one_step_win_coordinates[index]
        elif len(two_step_win_coordinates) != 0:
            size = len(two_step_win_coordinates)
            index = random.randint(size)
            selected_situation = two_step_win_coordinates[index]
        elif len(three_step_win_coordinates) != 0:
            size = len(three_step_win_coordinates)
            index = random.randint(size)
            selected_situation = three_step_win_coordinates[index]
        else:
            size = len(go_for_tie)
            index = random.randint(size)
            selected_situation = go_for_tie[index]
    # If we are one move away from win and Difficulty is 2
    # Win the game
    # If opponent is one move away from win
    # Go for defending
    opponent = switch_player(player, False)
    opponent_one_step_win_coordinates = possible_win(board, opponent)[0]
    print("Opponent: ", opponent, "Opp one step win: ", opponent_one_step_win_coordinates)
    if len(one_step_win_coordinates) != 0 and difficulty == 2:
        return pick_possible_coordinate(board, selected_situation)
    elif len(opponent_one_step_win_coordinates) != 0 and difficulty == 2:
        size = len(opponent_one_step_win_coordinates)
        index = random.randint(size)-1 if size > 1 else 0
        selected_situation = opponent_one_step_win_coordinates[index]
        return pick_possible_coordinate(board, selected_situation)
    return pick_possible_coordinate(board, selected_situation)


def mark(board, player, row, col):
    board[row][col] = player
    return board


def has_won(board, player):
    if board[0][0] == player and board[0][1] == player and board[0][2] == player:
        return True
    elif board[1][0] == player and board[1][1] == player and board[1][2] == player:
        return True
    elif board[2][0] == player and board[2][1] == player and board[2][2] == player:
        return True
    elif board[0][0] == player and board[1][0] == player and board[2][0] == player:
        return True
    elif board[0][1] == player and board[1][1] == player and board[2][1] == player:
        return True
    elif board[0][2] == player and board[1][2] == player and board[2][2] == player:
        return True
    elif board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    elif board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    else:
        return False


def is_full(board):
    for i in board:
        if "." in i:
            return False
    return True


def print_board(board):
    os.system("clear")
    print(f"""
       1   2   3
    A  {board[0][0]} | {board[0][1]} | {board[0][2]}
      ---+---+---
    B  {board[1][0]} | {board[1][1]} | {board[1][2]}
      ---+---+---
    C  {board[2][0]} | {board[2][1]} | {board[2][2]}""")


def print_result(winner):
    return f"{winner} has won!" if winner != 0 else "It's a tie!"


def tictactoe_game(mode='HUMAN-HUMAN', level=1):
    if mode == "HUMAN-HUMAN":
        board = init_board()
        print_board(board)
        player = switch_player("X", True)
        while True:
            player = switch_player(player, False)
            row, col = get_move(board, player)
            board = mark(board, player, row, col)
            print_board(board)
            if has_won(board, player):
                print(print_result(player))
                break
            elif is_full(board):
                print(print_result(0))
                break
    elif mode == "HUMAN-AI":
        board = init_board()
        print_board(board)
        player = switch_player("X", True)
        while True:
            row, col = get_move(board, player) if player == "X" else get_ai_move(board, player, level)
            board = mark(board, player, row, col)
            print_board(board)
            if has_won(board, player):
                print(print_result(player))
                break
            elif is_full(board):
                print(print_result(0))
                break
            player = switch_player(player, False)


def main_menu():
    tictactoe_game("HUMAN-AI", 2)


if __name__ == '__main__':
    main_menu()
