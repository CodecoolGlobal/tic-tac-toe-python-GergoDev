import sys


def init_board():
    board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    return board


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
                sys.exit(0)
        if move_pos != "" and len(move_pos) == 2:
            row = list(move_pos)[0]
            col = list(move_pos)[1]
            if row in alphabet_valid and col in numbers_valid and board[alphabet_to_index[row]][numbers_to_index[col]] == ".":
                return (row, col)


def get_ai_move(board, player):
    """Returns the coordinates of a valid move for player on board."""
    row, col = 0, 0
    return row, col


def mark(board, player, row, col):
    alphabet_to_index = {'A': 0, 'B': 1, 'C': 2}
    numbers_to_index = {'1': 0, '2': 1, '3': 2}
    row_index = alphabet_to_index[row]
    col_index = numbers_to_index[col]
    board[row_index][col_index] = player
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
    print(f"""
       1   2   3
    A  {board[0][0]} | {board[0][1]} | {board[0][2]}
      ---+---+---
    B  {board[1][0]} | {board[1][1]} | {board[1][2]}
      ---+---+---
    C  {board[2][0]} | {board[2][1]} | {board[2][2]}""")


def print_result(winner):
    return f"{winner} has won!" if winner != 0 else "It's a tie!"


def switch_player(player):
    return "X" if player == "O" else "O"


def tictactoe_game(mode='HUMAN-HUMAN'):
    if mode == "HUMAN-HUMAN":
        board = init_board()
        player = "X"
        while True:
            player = switch_player(player)
            print_board(board)
            row, col = get_move(board, player)
            board = mark(board, player, row, col)
            print_board(board)
            if has_won(board, player):
                print(print_result(player))
                break
            elif is_full(board):
                print(print_result(0))
                break


# winner = 0
# print_result(winner)


def main_menu():
    tictactoe_game('HUMAN-HUMAN')


if __name__ == '__main__':
    main_menu()
