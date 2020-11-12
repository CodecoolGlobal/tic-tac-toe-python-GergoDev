import sys
import os
import time
from numpy import random
from Graffic import graphics
from pygame import mixer


mixer.init()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def play_music(file_path):
    mixer.music.load(file_path)
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)


def play_sound_effect(file_path):
    play_effect = mixer.Sound(file_path)
    play_effect.play()


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
            mixer.music.stop()
            os.system("clear")
            print(graphics[3])
            play_sound_effect("sounds/quit.ogg")
            time.sleep(2)
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
        elif opponent_result_count == 2 and player_result_count == 0:
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


def pick_a_situation(win_coordinates):
    size = len(win_coordinates)
    index = random.randint(size)
    return win_coordinates[index]


def get_ai_move(board, player, difficulty):
    time.sleep(1)
    win_coordinates = possible_win(board, player)
    one_step_win_coordinates, two_step_win_coordinates, three_step_win_coordinates, go_for_tie = win_coordinates
    selected_situation = None
    # print("One step win: ", one_step_win_coordinates)
    # print("\n")
    # print("Two step win: ", two_step_win_coordinates)
    # print("\n")
    # print("Three step win: ", three_step_win_coordinates)
    # print("\n")
    # print("Go for tie: ", go_for_tie)
    if difficulty == 1:
        if len(three_step_win_coordinates) != 0:
            selected_situation = pick_a_situation(three_step_win_coordinates)
        elif len(two_step_win_coordinates) != 0:
            selected_situation = pick_a_situation(two_step_win_coordinates)
        elif len(one_step_win_coordinates) != 0:
            selected_situation = pick_a_situation(one_step_win_coordinates)
        else:
            selected_situation = pick_a_situation(go_for_tie)
    elif difficulty == 2:
        if len(one_step_win_coordinates) != 0:
            selected_situation = pick_a_situation(one_step_win_coordinates)
        elif len(two_step_win_coordinates) != 0:
            selected_situation = pick_a_situation(two_step_win_coordinates)
        elif len(three_step_win_coordinates) != 0:
            selected_situation = pick_a_situation(three_step_win_coordinates)
        else:
            selected_situation = pick_a_situation(go_for_tie)
    # If we are one move away from win and Difficulty is 2
    # Win the game
    # If opponent is one move away from win
    # Go for defending
    opponent = switch_player(player, False)
    opponent_one_step_win_coordinates = possible_win(board, opponent)[0]
    # print("Opponent: ", opponent, "Opp one step win: ", opponent_one_step_win_coordinates)
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






                               {bcolors.BOLD}1   2   3{bcolors.ENDC}
                            {bcolors.BOLD}A{bcolors.ENDC}  {board[0][0]} {bcolors.WARNING}|{bcolors.ENDC} {board[0][1]} {bcolors.WARNING}|{bcolors.ENDC} {board[0][2]}
                              {bcolors.WARNING}---+---+---{bcolors.ENDC}
                            {bcolors.BOLD}B{bcolors.ENDC}  {board[1][0]} {bcolors.WARNING}|{bcolors.ENDC} {board[1][1]} {bcolors.WARNING}|{bcolors.ENDC} {board[1][2]}
                              {bcolors.WARNING}---+---+---{bcolors.ENDC}
                            {bcolors.BOLD}C{bcolors.ENDC}  {board[2][0]} {bcolors.WARNING}|{bcolors.ENDC} {board[2][1]} {bcolors.WARNING}|{bcolors.ENDC} {board[2][2]}
    
    



    
    """)


def print_result(winner):
    if winner == "X":
        return graphics[1]
    elif winner == "O":
        return graphics[2]
    else:
        return graphics[4]


def tictactoe_game(mode='HUMAN-HUMAN', level=1):
    if mode == "HUMAN-HUMAN":
        board = init_board()
        print_board(board)
        player = switch_player("X", True)
        while True:
            player = switch_player(player, False)
            row, col = get_move(board, player)
            play_sound_effect("sounds/move.ogg")
            board = mark(board, player, row, col)
            print_board(board)
            if has_won(board, player):
                print(print_result(player))
                mixer.music.stop()
                play_sound_effect("sounds/win.ogg")
                time.sleep(6.5)
                break
            elif is_full(board):
                print(print_result(0))
                mixer.music.stop()
                play_sound_effect("sounds/tie.ogg")
                time.sleep(8.5)
                break
    elif mode == "HUMAN-AI":
        board = init_board()
        print_board(board)
        player = switch_player("X", True)
        while True:
            row, col = get_move(board, player) if player == "X" else get_ai_move(board, player, level)
            play_sound_effect("sounds/move.ogg")
            board = mark(board, player, row, col)
            print_board(board)
            if has_won(board, player):
                print(print_result(player))
                mixer.music.stop()
                play_sound_effect("sounds/win.ogg")
                time.sleep(6.5)
                break
            elif is_full(board):
                print(print_result(0))
                mixer.music.stop()
                play_sound_effect("sounds/tie.ogg")
                time.sleep(8.5)
                break
            player = switch_player(player, False)
    elif mode == "AI-HUMAN":
        board = init_board()
        print_board(board)
        player = switch_player("O", True)
        while True:
            row, col = get_move(board, player) if player == "X" else get_ai_move(board, player, level)
            play_sound_effect("sounds/move.ogg")
            board = mark(board, player, row, col)
            print_board(board)
            if has_won(board, player):
                print(print_result(player))
                mixer.music.stop()
                play_sound_effect("sounds/win.ogg")
                time.sleep(6.5)
                break
            elif is_full(board):
                print(print_result(0))
                mixer.music.stop()
                play_sound_effect("sounds/tie.ogg")
                time.sleep(8.5)
                break
            player = switch_player(player, False)

    elif mode == "AI-AI":
        board = init_board()
        print_board(board)
        player = switch_player("O", True)
        while True:
            row, col = get_ai_move(board, player, level) if player == "X" else get_ai_move(board, player, level)
            play_sound_effect("sounds/move.ogg")
            board = mark(board, player, row, col)
            print_board(board)
            if has_won(board, player):
                print(print_result(player))
                mixer.music.stop()
                play_sound_effect("sounds/win.ogg")
                time.sleep(6.5)
                break
            elif is_full(board):
                print(print_result(0))
                mixer.music.stop()
                play_sound_effect("sounds/tie.ogg")
                time.sleep(8.5)
                break
            player = switch_player(player, False)
            time.sleep(1)


def menu_game_mode_validator():
    list_of_valid_inputs = ["1", "2", "3", "4"]

    while True:
        users_decision = input()
        if users_decision in list_of_valid_inputs:
            return int(users_decision)
        else:
            print("You can only pick option 1-4")


def ai_level():
    list_of_valid_inputs = ["1", "2"]
    while True:
        users_decision = input()
        if users_decision in list_of_valid_inputs:
            return int(users_decision)
        else:
            print("You can only pick option 1-2")


def playing_asker():
    List_of_valid_asker = ["Y", "N", "Quit"]
    asker_to_play = input("Do you want to play again?[Y/N]")
    asker_to_play = asker_to_play.upper()
    if asker_to_play in List_of_valid_asker:
        if asker_to_play == "Y":
            print("Oky Doky")
            time.sleep(1.6)
            return True
        elif asker_to_play == "N":
            os.system("clear")
            print(graphics[3])
            play_sound_effect("sounds/quit.ogg")
            time.sleep(2)
            os.system("clear")
            time.sleep(1.6)
            return False


def main_menu():
    agree_to_play = True

    while agree_to_play:
        play_music("sounds/theme_song.ogg")
        os.system("clear")
        print(graphics[0])
        print(graphics[5])
        game_mode = menu_game_mode_validator()
        play_sound_effect("sounds/select.ogg")
        if game_mode == 1:
            tictactoe_game("HUMAN-HUMAN")
        elif game_mode == 2:
            os.system("clear")
            print(graphics[0])
            print(graphics[6])
            level = ai_level()
            play_sound_effect("sounds/select.ogg")
            tictactoe_game("HUMAN-AI", level)
        elif game_mode == 3:
            os.system("clear")
            print(graphics[0])
            print(graphics[6])
            level = ai_level()
            play_sound_effect("sounds/select.ogg")
            tictactoe_game("AI-HUMAN", level)
        elif game_mode == 4:
            os.system("clear")
            print(graphics[0])
            print(graphics[6])
            level = ai_level()
            play_sound_effect("sounds/select.ogg")
            tictactoe_game("AI-AI", level)
        agree_to_play = playing_asker()


if __name__ == '__main__':
    main_menu()
