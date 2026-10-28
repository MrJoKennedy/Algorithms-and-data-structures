# ОПИСАНИЕ АЛГОРИТМА: Итеративное динамическое программирование 
# 1. Создаем матрицу состояний `f`, заполняем её INF. Стартовой клетке присваиваем 0, так как мы уже там находимся.
# 
# 2. В цикле проходим по всем клеткам доски. Для каждой клетки проверяем всех 
#    её соседей. Если f[соседа] + 1 < f[клетки], обновляем значение. Повторяем проходы по доске, пока на  
#    очередной итерации ни одно значение не изменится (это значит, что кратчайшие пути найдены для всех клеток).
# 
# 3. Встаем на конечную клетку. На каждом шаге ищем среди соседей ту клетку, 
#    чье значение в матрице `f` ровно на 1 меньше текущего. Переходим в неё.
#    Повторяем, пока не упремся в стартовую клетку (где f = 0).
#    В конце разворачиваем список, чтобы получить путь от начала к концу.

SIZE = 8
MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def knight_path(board, start, end):
    # --- ЭТАП 1: Инициализация таблицы состояний (ДП) ---
    INF = float("inf")
    f = [[INF] * SIZE for _ in range(SIZE)]
    f[start[0]][start[1]] = 0  # Расстояние до старта равно 0

    # --- ЭТАП 2: Итеративная релаксация (пока значения меняются) ---
    changed = True
    while changed:
        changed = False
        for x in range(SIZE):
            for y in range(SIZE):
                if board[x][y] == -1:
                    continue
                
                # Проверяем всех возможных соседей (ходы коня)
                for dx, dy in MOVES:
                    p, q = x + dx, y + dy
                    # Если сосед в пределах доски, не занят, и путь через него короче
                    if 0 <= p < SIZE and 0 <= q < SIZE and board[p][q] != -1 \
                            and f[p][q] + 1 < f[x][y]:
                        f[x][y] = f[p][q] + 1  # Обновляем минимальное расстояние
                        changed = True         # Фиксируем, что на этой итерации были изменения

    ex, ey = end
    if f[ex][ey] == INF:
        return None, None

    # --- ЭТАП 3: Восстановление оптимального маршрута ---
    path = [end]
    x, y = end
    while (x, y) != start:
        for dx, dy in MOVES:
            p, q = x + dx, y + dy
            # Ищем соседа, который находится ровно на 1 ход ближе к старту
            if 0 <= p < SIZE and 0 <= q < SIZE and board[p][q] != -1 \
                    and f[p][q] == f[x][y] - 1:
                x, y = p, q
                path.append((x, y))
                break
    path.reverse()  # Разворачиваем путь, чтобы он шел от старта к финишу
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


def has_repeats(path):
    """True, если в маршруте какое-то поле встречается больше одного раза."""
    return len(set(path)) != len(path)


def main():
    board = [[0] * SIZE for _ in range(SIZE)]

    k = int(input("Количество занятых белыми фигурами полей: "))
    i = 0
    while i < k:
        x, y = read_cell(f"  Занятое поле №{i + 1} (X Y): ")
        if board[x][y] == -1:  # проверка на повторение занятого поля
            print(f"  Поле ({x + 1},{y + 1}) уже было введено, введите другое.")
            continue
        board[x][y] = -1
        i += 1

    start = read_cell("Поле коня (X1 Y1): ")
    if board[start[0]][start[1]] == -1:
        print("Предупреждение: стартовое поле было отмечено как занятое; "
              "считаем, что на нём стоит сам конь.")
    board[start[0]][start[1]] = 0  # на стартовом поле стоит сам конь

    end = read_cell("Целевое поле (X2 Y2): ")
    if end == start:  # проверка на совпадение полей
        print("\nКонь уже стоит на целевом поле: 0 ходов.")
        return
    if board[end[0]][end[1]] == -1:
        print("Целевое поле занято белой фигурой, добраться невозможно.")
        return

    moves, path = knight_path(board, start, end)

    if moves is None:
        print("Добраться до целевого поля невозможно.")
        return

    # проверка маршрута на повторения полей
    if has_repeats(path):
        print("Ошибка: в маршруте есть повторяющиеся поля.")
        return

    print(f"\nа) Минимальное количество ходов: {moves}")
    print("б) Маршрут:", " -> ".join(f"({x + 1},{y + 1})" for x, y in path))
    print("Проверка: поля маршрута не повторяются.")
    print_board(board, path)


if __name__ == "__main__":
    main()