def traverse_depth_first_search(map: list[list[str]], curr_pos: tuple[int, int], directions, curr_path, visited_points):
    if is_out_of_bounce(map, curr_pos):
        return None

    if curr_pos in visited_points or map[curr_pos[0]][curr_pos[1]] == '#':
        return None
    visited_points.add(curr_pos)
    curr_path.append(curr_pos)

    if map[curr_pos[0]][curr_pos[1]] == 'A':
        return curr_pos, curr_path

    for _, vector in directions.items():
        new_pos = (curr_pos[0] + vector[0], curr_pos[1] + vector[1])
        copied_path = curr_path.copy()
        result = traverse_depth_first_search(map, new_pos, directions, copied_path, visited_points)
        if result is not None:
            return result

    return None

def is_out_of_bounce(map: list[list[str]], curr_pos: tuple[int, int]):
    return curr_pos[0] < 0 or curr_pos[0] >= len(map) or curr_pos[1] < 0 or curr_pos[1] >= len(map[0])

directions = {
    "UP": (-1,0),
    "RIGHT": (0, 1),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
}

def to_map(map_lines: list[str]):
    output = []
    for line in map_lines:
        curr_line = []
        for char in line:
            curr_line.append(char)
        output.append(curr_line)
    return output

def print_map(map: list[list[str]]):
    for line in map:
        for char in line:
            print(char, end ="")

def mark_map(map, path):
    for node in path:
        map[node[0]][node[1]] = 'O'

if __name__ == "__main__":
    with open("l1.txt", "r") as f:
        lines = f.readlines()
    grid_depth_first_search = to_map(lines)

    # DFS
    result, path = traverse_depth_first_search(grid_depth_first_search, (1,1), directions, [], set())
    mark_map(grid_depth_first_search, path)
    grid_depth_first_search[1][1] = 'S'

    print_map(grid_depth_first_search)