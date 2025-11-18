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
        print()

if __name__ == "__main__":
    with open("l1.txt", "r") as f:
        lines = f.readlines()
    map = to_map(lines)
    print_map(map)