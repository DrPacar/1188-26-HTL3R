from collections import deque

knight_moves = [
    (-2, -1),
    (-2, 1),
    (-1, 2),
    (1, 2),
    (2, 1),
    (2, -1),
    (1, -2),
    (-1, -2)
]

def traverse_board(start_pos: tuple[int, int], destination: tuple[int, int], board_size: int = 8):
    queue = deque()
    queue.append((start_pos, []))

    visited_squares = set()
    #visited_squares.add(start_pos)

    while len(queue) > 0:
        curr_square, curr_path = queue.popleft()

        if is_out_of_bounce(curr_square, board_size) or curr_square in visited_squares:
            continue
        visited_squares.add(curr_square)

        curr_path.append(curr_square)
        if curr_square == destination:
            return curr_path

        for neighbor in get_neighbors(curr_square):
            queue.append((neighbor, curr_path.copy()))

def get_neighbors(curr_pos: tuple[int, int]):
    neighbors = []
    for move in knight_moves:
        new_pos = (curr_pos[0] + move[0], curr_pos[1] + move[1])
        neighbors.append(new_pos)

    return neighbors

def is_out_of_bounce(pos: tuple[int, int], board_size: int):
    return pos[0] < 0 or pos[0] >= board_size or pos[1] < 0 or pos[1] >= board_size

def mark_points_on_board(board_size:int, points: list[tuple[int, int]]):
    grid = []
    for _ in range(board_size):
        line = []
        for _ in range(board_size):
            line.append(".")
        grid.append(line)

    for point in points:
        grid[point[0]][point[1]] = 'X'

    for line in grid:
        for char in line:
            print(char, end="")
        print()

def coordinate_to_pos(coordinate: str, board_size: int = 8):
    return board_size - int(coordinate[1]), (ord(coordinate[0]) - ord('a'))

if __name__ == "__main__":
    start = "a1"
    destination = "h8"

    board_size = 8
    start_square = coordinate_to_pos(start, board_size)
    destination_square = coordinate_to_pos(destination, board_size)

    out = traverse_board(start_square, destination_square, board_size)
    #print(out)

    mark_points_on_board(board_size, out)