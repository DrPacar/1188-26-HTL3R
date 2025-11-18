# Luka Pacar 2025
from collections import deque
import time

__author__ = "Luka Pacar"

def traverse_breadth_first_search(grid: list[list[str]], start_pos: tuple[int, int], directions: dict[str, tuple[int, int]]) -> tuple[tuple[int, int], list[tuple[int, int]]] | None:
    """
    Traverses the graph using Breadth First Search (Breitensuche).
    :param grid: Map to traverse.
    :param start_pos: The starting position in the map.
    :param directions: The possible directions to take
    :return: [0] -> Ending-Point/Destination - [1] -> Path to the destination | Or None if there is no way to the destination
    """
    queue = deque()
    visited_points = set()
    queue.append((start_pos, []))
    while len(queue) > 0:
        curr_pos, curr_path = queue.popleft()
        curr_path = curr_path.copy()
        curr_path.append(curr_pos)

        if curr_pos in visited_points or grid[curr_pos[0]][curr_pos[1]] == '#':
            continue
        visited_points.add(curr_pos)

        if grid[curr_pos[0]][curr_pos[1]] == 'A':
            return curr_pos, curr_path

        for _, vector in directions.items():
            new_pos = (curr_pos[0] + vector[0], curr_pos[1] + vector[1])
            if is_out_of_bounce(grid, new_pos) or new_pos in visited_points or grid[new_pos[0]][new_pos[1]] == 'X':
                continue
            queue.append((new_pos, curr_path))

def traverse_depth_first_search(grid: list[list[str]], curr_pos: tuple[int, int], directions: dict[str, tuple[int, int]], curr_path: list[tuple[int, int]], visited_points: set[tuple[int, int]]) -> tuple[tuple[int, int], list[tuple[int, int]]] | None:
    """
        Traverses the graph using Depth First Search (Tiefensuche).
        :param grid: Map to traverse.
        :param curr_pos: The current position in the map.
        :param directions: The possible directions to take.
        :param curr_path: The current path taken to the curr_pos.
        :param visited_points: The current visited points up until this point.
        :return: [0] -> Ending-Point/Destination - [1] -> Path to the destination | Or None if there is no way to the destination.
        """
    if is_out_of_bounce(grid, curr_pos):
        return None

    if curr_pos in visited_points or grid[curr_pos[0]][curr_pos[1]] == '#':
        return None
    visited_points.add(curr_pos)

    curr_path.append(curr_pos)

    if grid[curr_pos[0]][curr_pos[1]] == 'A':
        return curr_pos, curr_path

    for _, vector in directions.items():
        new_pos = (curr_pos[0] + vector[0], curr_pos[1] + vector[1])
        copied_path = curr_path.copy()
        result = traverse_depth_first_search(grid, new_pos, directions, copied_path, visited_points)
        if result is not None:
            return result

    return None

def is_out_of_bounce(grid: list[list[str]], curr_pos: tuple[int, int]) -> bool:
    """
    Checks if a given point is outside the given map
    :param grid: The given map.
    :param curr_pos: The position to test.
    :return: True if the given value is out of bounce, otherwise False
    """
    return curr_pos[0] < 0 or curr_pos[0] >= len(grid) or curr_pos[1] < 0 or curr_pos[1] >= len(grid[0])

pos_directions = {
    "UP": (-1,0),
    "RIGHT": (0, 1),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
}

def to_map(map_lines: list[str]) -> list[list[str]]:
    """
    Takes string lines and converts them to a traversable map.
    :param map_lines: A list of lines to be converted.
    :return: The Map but with strings converted to character arrays.
    """
    output = []
    for line in map_lines:
        curr_line = []
        for char in line:
            curr_line.append(char)
        output.append(curr_line)
    return output

def print_map(grid: list[list[str]]):
    """ Prints the given map. """
    for line in grid:
        for char in line:
            print(char, end ="")

def mark_map(grid, given_path):
    """Marks the given path in the given map."""
    for node in given_path:
        grid[node[0]][node[1]] = 'O'

if __name__ == "__main__":
    for file in ["l1", "l2", "l3", "l4", "l5"]:
        print(f"{file}:\n")
        with open(f"{file}.txt", "r") as f:
            lines = f.readlines()

        grid_depth_first_search = to_map(lines)
        grid_breadth_first_search = to_map(lines).copy()

        # DFS
        time_start_DFS = time.perf_counter()
        results1, path = traverse_depth_first_search(grid_depth_first_search, (1,1), pos_directions, [], set())
        taken_time_DFS = time.perf_counter() - time_start_DFS

        mark_map(grid_depth_first_search, path)
        grid_depth_first_search[1][1] = 'S'

        print_map(grid_depth_first_search)
        print("Time taken: " + str(taken_time_DFS/1000) + "ms")
        print()
        # BFS
        time_start_BFS = time.perf_counter()
        results2, path = traverse_breadth_first_search(grid_breadth_first_search, (1, 1), pos_directions)
        taken_time_BFS = time.perf_counter() - time_start_BFS

        mark_map(grid_breadth_first_search, path)
        grid_breadth_first_search[1][1] = 'S'

        print_map(grid_breadth_first_search)
        print("Time taken: " + str(taken_time_BFS/1000) + "ms")
        print()