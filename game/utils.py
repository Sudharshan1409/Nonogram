from random import randint


def generate_grid(rows, columns):
    grid = []
    coords = []
    for i in range(rows):
        row = []
        for j in range(columns):
            row.append(0)
            coords.append((i, j))
        grid.append(row)
    return grid, coords


def generate_nonogram_grid(rows, columns):
    grid = []
    grid, coords = generate_grid(rows, columns)
    i = 0
    total_ones_min = int((rows * columns) * 45 // 100)
    total_ones_max = int((rows * columns) * 70 // 100)
    total_ones = randint(total_ones_min, total_ones_max)
    print(f"Total ones: {total_ones}")
    for i in range(total_ones):
        index = randint(0, len(coords) - 1)
        x, y = coords[index]
        grid[x][y] = 1
        coords.pop(index)
    return grid


def get_row_clues(grid):
    max_row_clues = 0
    row_clues = []
    for row in grid:
        row_clue = []
        count = 0
        for cell in row:
            if cell == 1:
                count += 1
            elif count > 0:
                row_clue.append(count)
                count = 0
        if count > 0:
            row_clue.append(count)
        if len(row_clue) == 0:
            row_clue.append(0)
        row_clues.append(row_clue)
        if len(row_clue) > max_row_clues:
            max_row_clues = len(row_clue)
    return row_clues, max_row_clues


def get_reverse_column_clues(column_clues):
    reversed_column_clues = []
    for column_clue in column_clues:
        print("column_clue", column_clue)
        reversed_column_clue = column_clue[::-1]
        print("reversed_column_clue", reversed_column_clue)
        reversed_column_clues.append(reversed_column_clue)
    return reversed_column_clues


def get_column_clues(grid):
    max_column_clues = 0
    column_clues = []
    for j in range(len(grid[0])):
        column_clue = []
        count = 0
        for i in range(len(grid)):
            if grid[i][j] == 1:
                count += 1
            elif count > 0:
                column_clue.append(count)
                print("appended", count)
                count = 0
        if count > 0:
            column_clue.append(count)
            print("appended", count)
        if len(column_clue) == 0:
            column_clue.append(0)
            print("appended", 0)
        column_clues.append(column_clue)
        if len(column_clue) > max_column_clues:
            max_column_clues = len(column_clue)
    return column_clues, max_column_clues


def print_grid(grid):
    row = len(grid)
    column = len(grid[0])
    row_clues = get_row_clues(grid)
    column_clues = get_column_clues(grid)
    for i in column_clues:
        print(i)
    print()
    print()
    for i in range(row):
        print(str(row_clues[i]).rjust(20, ' '), end=' ')
        for j in range(column):
            print(grid[i][j], end=' ')
        print()


if __name__ == "__main__":
    rows = int(input("Enter number of rows: "))
    columns = int(input("Enter number of columns: "))
    grid = generate_nonogram_grid(rows, columns)
    print_grid(grid)
