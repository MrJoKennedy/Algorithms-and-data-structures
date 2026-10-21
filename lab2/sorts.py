import random
import string


class Stats:
    """Счётчики сравнений и перестановок."""
    def __init__(self):
        self.cmp = 0
        self.swp = 0


def less(a, b, st):
    st.cmp += 1
    return a < b


def greater(a, b, st):
    st.cmp += 1
    return a > b


def swap(arr, i, j, st):
    if i != j:
        arr[i], arr[j] = arr[j], arr[i]
        st.swp += 1


# ---------- 1. Сортировка включением ----------
def insertion_sort(arr, st):
    for i in range(1, len(arr)):
        j = i
        # двигаем элемент влево, пока он меньше предыдущего
        while j > 0 and less(arr[j], arr[j - 1], st):
            swap(arr, j, j - 1, st)
            j -= 1


# ---------- 2. Сортировка выбором ----------
def selection_sort(arr, st):
    n = len(arr)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if less(arr[j], arr[m], st):
                m = j
        swap(arr, i, m, st)


# ---------- 3. Шейкерная сортировка ----------
def shaker_sort(arr, st):
    left, right = 0, len(arr) - 1
    while left < right:
        last = left
        for i in range(left, right):            # проход вправо
            if greater(arr[i], arr[i + 1], st):
                swap(arr, i, i + 1, st)
                last = i
        right = last
        last = right
        for i in range(right, left, -1):        # проход влево
            if less(arr[i], arr[i - 1], st):
                swap(arr, i, i - 1, st)
                last = i
        left = last


# ---------- 4. Быстрая сортировка с двумя опорными ----------
def _insertion_range(arr, lo, hi, st):
    for i in range(lo + 1, hi + 1):
        j = i
        while j > lo and less(arr[j], arr[j - 1], st):
            swap(arr, j, j - 1, st)
            j -= 1


def _quick(arr, lo, hi, st):
    if hi - lo + 1 < 4:                 # маленький кусок — вставками
        _insertion_range(arr, lo, hi, st)
        return
    # опорные: a[lo+1] и a[hi-1] (не крайние позиции)
    if greater(arr[lo + 1], arr[hi - 1], st):
        swap(arr, lo + 1, hi - 1, st)
    swap(arr, lo, lo + 1, st)           # p1 -> в начало
    swap(arr, hi, hi - 1, st)           # p2 -> в конец
    p1, p2 = arr[lo], arr[hi]

    lt, gt, i = lo + 1, hi - 1, lo + 1
    while i <= gt:
        if less(arr[i], p1, st):                # в левый блок
            swap(arr, i, lt, st)
            lt += 1
        elif greater(arr[i], p2, st):           # в правый блок
            while i < gt and greater(arr[gt], p2, st):
                gt -= 1
            swap(arr, i, gt, st)
            gt -= 1
            if less(arr[i], p1, st):
                swap(arr, i, lt, st)
                lt += 1
        i += 1
    lt -= 1
    gt += 1
    swap(arr, lo, lt, st)               # опорные на свои места
    swap(arr, hi, gt, st)

    _quick(arr, lo, lt - 1, st)         # < p1
    _quick(arr, lt + 1, gt - 1, st)     # p1 <= x <= p2
    _quick(arr, gt + 1, hi, st)         # > p2


def quick_sort(arr, st):
    _quick(arr, 0, len(arr) - 1, st)


# ---------- 5. Пирамидальная сортировка ----------
def _sift_down(arr, root, size, st):
    while True:
        child = 2 * root + 1
        if child >= size:
            return
        if child + 1 < size and less(arr[child], arr[child + 1], st):
            child += 1                  # выбираем большего потомка
        if less(arr[root], arr[child], st):
            swap(arr, root, child, st)
            root = child
        else:
            return


def heap_sort(arr, st):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):  # построение кучи
        _sift_down(arr, i, n, st)
    for end in range(n - 1, 0, -1):      # извлечение максимума
        swap(arr, 0, end, st)
        _sift_down(arr, 0, end, st)


# ---------- Ввод и запуск ----------
def main():
    n = int(input("Количество элементов: "))
    kind = input("Тип данных (1 - числовой, 2 - символьный): ").strip()
    if kind == "2":
        data = [random.choice(string.ascii_lowercase) for _ in range(n)]
    else:
        data = [random.randint(-100, 100) for _ in range(n)]
    print("Исходный массив:", data)

    algos = [
        ("Сортировка включением", insertion_sort),
        ("Сортировка выбором", selection_sort),
        ("Шейкерная сортировка", shaker_sort),
        ("Быстрая сортировка (2 медианы)", quick_sort),
        ("Пирамидальная сортировка", heap_sort),
    ]
    for name, func in algos:
        arr = data[:]                    # у каждой сортировки своя копия
        st = Stats()
        func(arr, st)
        print(f"\n{name}")
        print("Результат:", arr)
        print("Сравнений:", st.cmp)
        print("Перестановок:", st.swp)


if __name__ == "__main__":
    main()
