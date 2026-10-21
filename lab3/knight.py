SIZE = 8
MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def knight_path(board, start, end):

    INF = float("inf")
    f = [[INF] * SIZE for _ in range(SIZE)]
    f[start[0]][start[1]] = 0

    changed = True
    while changed:
        changed = False
        for x in range(SIZE):
            for y in range(SIZE):
                if board[x][y] == -1:
                    continue
                for dx, dy in MOVES:
                    p, q = x + dx, y + dy
                    if 0 <= p < SIZE and 0 <= q < SIZE and board[p][q] != -1 \
                            and f[p][q] + 1 < f[x][y]:
                        f[x][y] = f[p][q] + 1
                        changed = True

    ex, ey = end
    if f[ex][ey] == INF:
        return None, None

    # восстановление маршрута
    path = [end]
    x, y = end
    while (x, y) != start:
        for dx, dy in MOVES:
            p, q = x + dx, y + dy
            if 0 <= p < SIZE and 0 <= q < SIZE and board[p][q] != -1 \
                    and f[p][q] == f[x][y] - 1:
                x, y = p, q
                path.append((x, y))
                break
    path.reverse()
    return f[ex][ey], path


def read_cell(prompt):
    while True:
        try:
            x, y = map(int, input(prompt).split())
            if 1 <= x <= SIZE and 1 <= y <= SIZE:
                return x - 1, y - 1
        except ValueError:
            pass
        print("Введите два числа от 1 до 8 через пробел.")


def print_board(board, path):
    on_path = {c: i for i, c in enumerate(path)}
    print("\nДоска (K - старт, F - финиш, цифры - номер хода, # - занято, . - свободно):")
    for y in range(SIZE - 1, -1, -1):
        row = []
        for x in range(SIZE):
            if (x, y) == path[0]:
                row.append("K")
            elif (x, y) == path[-1]:
                row.append("F")
            elif (x, y) in on_path:
                row.append(str(on_path[(x, y)]))
            elif board[x][y] == -1:
                row.append("#")
            else:
                row.append(".")
        print(f"{y + 1} | " + " ".join(f"{c:>2}" for c in row))
    print("    " + " ".join(f"{x + 1:>2}" for x in range(SIZE)))


def main():
    board = [[0] * SIZE for _ in range(SIZE)]

    k = int(input("Количество занятых белыми фигурами полей: "))
    for i in range(k):
        x, y = read_cell(f"  Занятое поле №{i + 1} (X Y): ")
        board[x][y] = -1

    start = read_cell("Поле коня (X1 Y1): ")
    end = read_cell("Целевое поле (X2 Y2): ")
    board[start[0]][start[1]] = 0  # на стартовом поле стоит сам конь

    moves, path = knight_path(board, start, end)

    if moves is None:
        print("Добраться до целевого поля невозможно.")
        return

    print(f"\nа) Минимальное количество ходов: {moves}")
    print("б) Маршрут:", " -> ".join(f"({x + 1},{y + 1})" for x, y in path))
    print_board(board, path)


if __name__ == "__main__":
    main()
