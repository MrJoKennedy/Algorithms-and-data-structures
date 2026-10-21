from collections import deque

N = 8
MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def knight_path(board, start, end):
    """Возвращает маршрут [(x, y), ...] от start до end или None, если пути нет."""
    (x1, y1), (x2, y2) = start, end
    if board[y2 - 1][x2 - 1] == 1 and start != end:
        return None                         # конечное поле занято своей фигурой

    prev = {start: None}                    # откуда пришли в каждое поле
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            break
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= N and 1 <= ny <= N \
                    and board[ny - 1][nx - 1] == 0 and (nx, ny) not in prev:
                prev[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    if end not in prev:
        return None
    path = []
    cell = end
    while cell is not None:                 # восстанавливаем путь с конца
        path.append(cell)
        cell = prev[cell]
    return path[::-1]


def read_board():
    print("Введите доску: 8 строк по 8 цифр (1 - занято, 0 - свободно),")
    print("строка 1 - первая строка доски. Цифры можно писать через пробел или слитно.")
    board = []
    while len(board) < N:
        row = [int(c) for c in input(f"Строка {len(board) + 1}: ") if c in "01"]
        if len(row) != N:
            print("Нужно ровно 8 цифр (0 или 1), повторите ввод.")
            continue
        board.append(row)
    return board


def read_cell(name):
    while True:
        try:
            x, y = map(int, input(f"{name} (X Y, от 1 до 8): ").split())
            if 1 <= x <= N and 1 <= y <= N:
                return x, y
        except ValueError:
            pass
        print("Введите два числа от 1 до 8 через пробел.")


def print_board(board, path):
    on_path = set(path)
    print("\n  X: " + " ".join(str(i) for i in range(1, N + 1)))
    for y in range(N):
        line = []
        for x in range(N):
            if (x + 1, y + 1) == path[0]:
                line.append("S")            # старт
            elif (x + 1, y + 1) == path[-1]:
                line.append("F")            # финиш
            elif (x + 1, y + 1) in on_path:
                line.append("*")            # промежуточное поле маршрута
            else:
                line.append("#" if board[y][x] else ".")
        print(f"Y{y + 1}:  " + " ".join(line))
    print("S - старт, F - финиш, * - маршрут, # - занято, . - свободно")


def main():
    board = read_board()
    start = read_cell("Начальное поле (X1, Y1)")
    end = read_cell("Конечное поле (X2, Y2)")

    path = knight_path(board, start, end)
    if path is None:
        print("\nКонь не может добраться до этого поля.")
        return
    print(f"\nа) Минимальное количество ходов: {len(path) - 1}")
    print("б) Маршрут: " + " -> ".join(f"({x},{y})" for x, y in path))
    print_board(board, path)


if __name__ == "__main__":
    main()
