import random
import string
from dataclasses import dataclass

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


# ---------- 1. Сортировка включением ----------from dataclasses import dataclass
from random import randint
from typing import Callable, Generic, TypeVar

T = TypeVar("T", int, str)

@dataclass
class Statistics:
    comparisons: int = 0
    swaps: int = 0


class Sorter(Generic[T]):
    def __init__(self, data: list[T]) -> None:
        self.data = data
        self.statistics = Statistics()

    def _less(self, first: T, second: T) -> bool:
        self.statistics.comparisons += 1
        return first < second

    def _greater(self, first: T, second: T) -> bool:
        self.statistics.comparisons += 1
        return first > second

    def _swap(self, first: int, second: int) -> None:
        if first != second:
            self.data[first], self.data[second] = (
                self.data[second],
                self.data[first],
            )
            self.statistics.swaps += 1

    def insertion_sort(self) -> None:
        """Сортировка включением (вставками).

        Слева постепенно формируется отсортированная часть массива. Каждый
        следующий элемент сравнивается с предыдущими и соседними обменами
        передвигается влево, пока не займёт подходящее место.
        """
        self._insertion_sort_range(0, len(self.data))

    def _insertion_sort_range(self, begin: int, end: int) -> None:
        """Сортирует полуинтервал [begin, end) соседними обменами."""
        for index in range(begin + 1, end):
            current = index
            while current > begin and self._less(
                self.data[current], self.data[current - 1]
            ):
                self._swap(current, current - 1)
                current -= 1

    def selection_sort(self) -> None:
        """Сортировка выбором.

        На каждом шаге в ещё не отсортированной части находится минимальный
        элемент. Он меняется местами с первым элементом этой части, после чего
        граница отсортированной части сдвигается вправо.
        """
        for index in range(len(self.data)):
            minimum = index
            for current in range(index + 1, len(self.data)):
                if self._less(self.data[current], self.data[minimum]):
                    minimum = current
            self._swap(index, minimum)

    def cocktail_sort(self) -> None:
        """Шейкерная сортировка (двунаправленный пузырёк).

        Проход слева направо перемещает максимальный элемент к правой границе,
        а обратный проход — минимальный элемент к левой. После каждой пары
        проходов рабочая область сужается. Если обменов не было, массив уже
        отсортирован и алгоритм завершается досрочно.
        """
        if len(self.data) < 2:
            return

        left = 0
        right = len(self.data) - 1
        changed = True

        while changed and left < right:
            changed = False
            for index in range(left, right):
                if self._greater(self.data[index], self.data[index + 1]):
                    self._swap(index, index + 1)
                    changed = True

            if not changed:
                break

            changed = False
            right -= 1
            for index in range(right, left, -1):
                if self._greater(self.data[index - 1], self.data[index]):
                    self._swap(index - 1, index)
                    changed = True
            left += 1

    def dual_pivot_quick_sort(self) -> None:
        """Быстрая сортировка с двумя сепараторами.

        Два сепаратора выбираются из внутренних позиций около 1/3 и 2/3
        подмассива. Данные разделяются на три блока: меньше первого
        сепаратора, между сепараторами и больше второго сепаратора. Затем все
        три блока рекурсивно сортируются тем же способом.
        """
        if self.data:
            self._dual_pivot_quick_sort_range(0, len(self.data) - 1)

    def _dual_pivot_quick_sort_range(self, left: int, right: int) -> None:
        if left >= right:
            return

        length = right - left + 1
        if length < 4:
            # Два различных внутренних сепаратора здесь выбрать невозможно.
            self._insertion_sort_range(left, right + 1)
            return

        # Позиции около 1/3 и 2/3 всегда внутренние при length >= 4.
        first_pivot_index = left + length // 3
        second_pivot_index = right - length // 3

        if self._greater(
            self.data[first_pivot_index], self.data[second_pivot_index]
        ):
            self._swap(first_pivot_index, second_pivot_index)

        # Для разделения сепараторы временно переносим к границам.
        self._swap(left, first_pivot_index)
        self._swap(right, second_pivot_index)
        first_pivot = self.data[left]
        second_pivot = self.data[right]

        less_boundary = left + 1
        greater_boundary = right - 1
        current = less_boundary

        while current <= greater_boundary:
            if self._less(self.data[current], first_pivot):
                self._swap(current, less_boundary)
                less_boundary += 1
            elif self._greater(self.data[current], second_pivot):
                while current < greater_boundary and self._greater(
                    self.data[greater_boundary], second_pivot
                ):
                    greater_boundary -= 1

                self._swap(current, greater_boundary)
                greater_boundary -= 1

                if self._less(self.data[current], first_pivot):
                    self._swap(current, less_boundary)
                    less_boundary += 1
            current += 1

        less_boundary -= 1
        greater_boundary += 1
        self._swap(left, less_boundary)
        self._swap(right, greater_boundary)

        self._dual_pivot_quick_sort_range(left, less_boundary - 1)
        if (
            less_boundary + 1 < greater_boundary
            and self._less(first_pivot, second_pivot)
        ):
            self._dual_pivot_quick_sort_range(
                less_boundary + 1, greater_boundary - 1
            )
        self._dual_pivot_quick_sort_range(greater_boundary + 1, right)

    def heap_sort(self) -> None:
        """Bottom-up sift-down (оптимизация Вегенера).

        Фаза 1: спуск от root к листу, всегда по большему ребёнку.
                1 сравнение на уровень (двое детей между собой).
        Фаза 2: подъём от листа до первого места, где элемент встаёт по правилу.
                Затем «сдвиг» элементов пути вверх и размещение x.

        Средне: ~log2(n) + небольшое число сравнений вместо 2*log2(n).
        """
        size = len(self.data)
        if size < 2:
            return

        # Строим max-кучу.
        for root in range(size // 2 - 1, -1, -1):
            self._sift_down(root, size)

        # Переносим максимум в конец и восстанавливаем оставшуюся кучу.
        for heap_size in range(size, 1, -1):
            self._swap(0, heap_size - 1)
            self._sift_down(0, heap_size - 1)

    def _sift_down(self, root: int, heap_size: int) -> None:
        x = self.data[root]

        j = root
        while j < heap_size // 2:
            child = 2 * j + 1
            if child + 1 < heap_size and self._greater(
                self.data[child + 1], self.data[child]
            ):
                child += 1
            j = child

        while j > root and self._greater(x, self.data[j]):
            j = (j - 1) // 2

        carry = x
        while j != root:
            parent = (j - 1) // 2
            self.data[j], carry = carry, self.data[j]
            j = parent
        self.data[root] = carry

SortMethod = Callable[[Sorter[T]], None]


def run_sort(name: str, source: list[T], method: SortMethod[T]) -> None:
    data = source.copy()
    sorter = Sorter(data)
    method(sorter)

    print(f"\n{name}")
    print(f"  Результат: {data}")
    print(f"  Сравнений: {sorter.statistics.comparisons}")
    print(f"  Перестановок: {sorter.statistics.swaps}")


def run_all_sorts(source: list[T]) -> None:
    print(f"\nИсходный массив: {source}")
    algorithms: list[tuple[str, SortMethod[T]]] = [
        ("Сортировка включением", lambda sorter: sorter.insertion_sort()),
        ("Сортировка выбором", lambda sorter: sorter.selection_sort()),
        ("Шейкерная сортировка", lambda sorter: sorter.cocktail_sort()),
        (
            "Быстрая сортировка с двумя сепараторами",
            lambda sorter: sorter.dual_pivot_quick_sort(),
        ),
        ("Пирамидальная сортировка", lambda sorter: sorter.heap_sort()),
    ]

    for name, method in algorithms:
        run_sort(name, source, method)


def generate_numbers(size: int) -> list[int]:
    return [randint(-99, 99) for _ in range(size)]


def generate_characters(size: int) -> list[str]:
    return [chr(randint(ord("A"), ord("Z"))) for _ in range(size)]


def main() -> None:
    try:
        size = int(input("Количество элементов: "))
        if size < 0:
            raise ValueError
    except ValueError:
        print("Ошибка: количество должно быть целым неотрицательным числом.")
        return

    data_type = input("Тип данных (1 — числовой, 2 — символьный): ").strip()
    if data_type == "1":
        run_all_sorts(generate_numbers(size))
    elif data_type == "2":
        run_all_sorts(generate_characters(size))
    else:
        print("Ошибка: выберите тип 1 или 2.")


if __name__ == "__main__":
    main()

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
