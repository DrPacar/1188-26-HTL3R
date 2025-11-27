# Luka Pacar 5CN
__author__ = "Luka Pacar"

from abc import ABC, abstractmethod


class Piece(ABC):

    @staticmethod
    @abstractmethod
    def non_attacking_configuration(piece_to_check, other_pieces, board_size):
        """
        Checks if the piece_to_check is attacked by pieces included in other_pieces.
        All pieces have to be of the same type.
        :param board_size: The size of the board
        :param piece_to_check: The piece to be checked for the attack status
        :param other_pieces: The other pieces that could attack the piece_to_check
        :return: True if the piece_to_check is not attacked
        """
        pass


class Queen(Piece):
    @staticmethod
    def non_attacking_configuration(piece_to_check, other_pieces, board_size):
        for enemy_queen in other_pieces:
            attack_each_other = (abs(enemy_queen[0] - piece_to_check[0]) == abs(enemy_queen[1] - piece_to_check[1])
                                 or enemy_queen[0] == piece_to_check[0]
                                 or enemy_queen[1] == piece_to_check[1])
            if attack_each_other:
                return False

        return True

class Knight(Piece):
    moves = [
        (-2, -1),
        (-2, 1),
        (-1, 2),
        (1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2)
    ]
    pos_to_targets = None

    @staticmethod
    def is_out_of_bounce(board_size: int, position: tuple[int, int]):
        return position[0] < 0 or position[0] >= board_size or position[1] < 0 or position[1] >= board_size

    @staticmethod
    def calculate_target_pos(board_size: int):
        pos_to_targets = {}
        for i in range(board_size):
            for j in range(board_size):
                position = (i, j)
                valid_targets = set()
                for move in Knight.moves:
                    target = (position[0] + move[0], position[1] + move[1])
                    if not Knight.is_out_of_bounce(board_size, target):
                        valid_targets.add(target)
                pos_to_targets[position] = valid_targets

        Knight.pos_to_targets = pos_to_targets



    @staticmethod
    def non_attacking_configuration(piece_to_check, other_pieces, board_size):
        if Knight.pos_to_targets is None:
            Knight.calculate_target_pos(board_size)

        target_set = Knight.pos_to_targets[piece_to_check]
        return not any(position in target_set for position in other_pieces)

def calculate_non_attacking_pos(piece_type: type[Piece], start_pos: tuple[int, int] = (0,0), board_size: int = 8, piece_positions: list[tuple[int, int]] = None):
    """
    Calculates the amount of pieces that can be placed on the board without attacking themselves.
    :param piece_type: The type of piece to place. (f.e. "Queen", "Knight", ...)
    :param start_pos: The current pos to traverse at
    :param board_size: The size of the board
    :param piece_positions: The current piece positions
    :return: The first piece configuration that meet the criteria
    """
    if piece_positions is None:
        piece_positions = set()

    best_positions = [frozenset(piece_positions)]
    curr_pos = start_pos
    while curr_pos[0] != board_size:
        if piece_type.non_attacking_configuration(curr_pos, piece_positions, board_size):
            piece_positions.add(curr_pos)

            result = calculate_non_attacking_pos(piece_type, to_next_field(curr_pos, board_size), board_size, piece_positions)
            result_length = len(result[0])
            best_positions_length = len(best_positions[0])
            if result_length > best_positions_length:
                best_positions = result.copy()
            elif result_length == best_positions_length:
                best_positions.extend(result.copy())

            piece_positions.remove(curr_pos)

        curr_pos = to_next_field(curr_pos, board_size)

    return best_positions

def to_next_field(field: tuple[int, int], board_size: int):
    """
    Calculates the next field of the board.
    :param field: current field
    :param board_size: The size of the board
    :return: next field
    """
    row = field[0]
    col = field[1]
    if col + 1 >= board_size:
        return row + 1, 0
    else:
        return row, col + 1

def calculate_queens(curr_row: int = 0, number_of_queens_to_place: int = 8, board_size: int = 8, queen_positions: list[tuple[int, int]] = None):
    """
    Calculates the amount of queens that can be placed on the board without attacking themselves.
    :param curr_row: The current row to target (default: 0) - This parameter should always be 0
    :param number_of_queens_to_place: The number of queens to be placed (default: 8)
    :param board_size: The size of the board
    :param queen_positions: The current queen positions
    :return: The first queen positions that meet the criteria
    """
    if queen_positions is None:
        queen_positions = set()

    if number_of_queens_to_place == 0:
        return queen_positions

    if curr_row >= board_size:
        return None

    for col in range(board_size):
        curr_pos = (curr_row, col)
        if valid_queen_pos(queen_positions, curr_pos):
            queen_positions.add(curr_pos)

            result = calculate_queens(curr_row + 1, number_of_queens_to_place-1, board_size, queen_positions)
            if result:
                return result
            queen_positions.remove(curr_pos)



def valid_queen_pos(placed_queens: list[tuple[int, int]], queen: tuple[int, int]):
    """
    Checks if a queen is not attacked by other queens.
    :param placed_queens: The other queens.
    :param queen: The queen to check.
    :return: True, if the queen is not attacked by the others, otherwise false.
    """
    for enemy_queen in placed_queens:
        attack_each_other = (abs(enemy_queen[0] - queen[0]) == abs(enemy_queen[1] - queen[1])
                             or enemy_queen[0] == queen[0]
                             or enemy_queen[1] == queen[1])
        if attack_each_other:
            return False

    return True


def print_board(board_size: int, positions: list[tuple[int, int]]):
    """
    prints the given queen positions on the given board_size
    :param board_size: the size of the board
    :param positions: the positions of the pieces
    """
    grid = []
    for i in range(board_size):
        line = []
        for j in range(board_size):
            line.append(".")
        grid.append(line)

    for position in positions:
        grid[len(grid) - 1 - position[0]][position[1]] = 'O'

    for line in grid:
        for char in line:
            print(char, end = "")
        print()

if __name__ == "__main__":
    #queens = calculate_queens(Queen, board_size=8)
    board_size = 8
    positions = calculate_non_attacking_pos(Queen, board_size=board_size)

    print("Number of possible configurations:", len(positions))
    print("Possible Positions")
    for pos in positions:
        print_board(board_size, pos)
        print()