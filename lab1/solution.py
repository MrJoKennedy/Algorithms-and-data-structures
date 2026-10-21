# лаба 1 Якимович Никита и Прилищ Андрей

from __future__ import annotations

import sys
from functools import lru_cache


Segment = tuple[int, int]  # ширина участка, заполненная высота
Placement = tuple[int, int, int, int, int]  # i, x1, y1, x2, y2


def merge_equal_neighbours(profile: list[Segment]) -> tuple[Segment, ...]:
    # объединяет сосдние участки профиля одинаковой высоты
    result: list[Segment] = []
    for width, height in profile:
        if width == 0:
            continue
        if result and result[-1][1] == height:
            old_width, _ = result[-1]
            result[-1] = (old_width + width, height)
        else:
            result.append((width, height))
    return tuple(result)


def tile_rectangle(
    target_width: int,
    target_height: int,
    rectangles: list[tuple[int, int]],
) -> list[Placement] | None:

    # возвращает одну подходящую укладку или None, если её нет
    n = len(rectangles)
    target_area = target_width * target_height
    areas = [width * height for width, height in rectangles]

    # remaining_area[mask] — площадь ещё не использованных прямоугольников
    remaining_area = [0] * (1 << n)
    total_area = sum(areas)
    for mask in range(1 << n):
        used_area = sum(areas[i] for i in range(n) if mask & (1 << i))
        remaining_area[mask] = total_area - used_area

    @lru_cache(maxsize=None)
    def search(
        used_mask: int,
        profile: tuple[Segment, ...],
    ) -> tuple[Placement, ...] | None:
        min_height = min(height for _, height in profile)
        if min_height == target_height:
            return ()

        filled_area = sum(width * height for width, height in profile)
        empty_area = target_area - filled_area
        if remaining_area[used_mask] < empty_area:
            return None

        # самый левый участок среди участков минимальной высоты
        x = 0
        segment_index = 0
        for segment_index, (free_width, height) in enumerate(profile):
            if height == min_height:
                break
            x += free_width

        plateau_width = profile[segment_index][0]
        candidates: list[tuple[bool, int, int, int, int]] = []

        for i, (side_a, side_b) in enumerate(rectangles):
            if used_mask & (1 << i):
                continue

            # set убирает повтор одного варианта для квадрата
            for width, height in {(side_a, side_b), (side_b, side_a)}:
                if (
                    width <= plateau_width
                    and min_height + height <= target_height
                    and areas[i] <= empty_area
                ):
                    candidates.append(
                        (width == plateau_width, areas[i], i, width, height)
                    )

        # сначала порбуем варианты, закрывающие весь текущий участок затем более крупные прямоугольники
        candidates.sort(reverse=True)

        for _, _, i, width, height in candidates:
            new_profile = list(profile)
            del new_profile[segment_index]
            replacement: list[Segment] = [(width, min_height + height)]
            if width < plateau_width:
                replacement.append((plateau_width - width, min_height))
            new_profile[segment_index:segment_index] = replacement

            normalized_profile = merge_equal_neighbours(new_profile)
            tail = search(used_mask | (1 << i), normalized_profile)
            if tail is not None:
                placement: Placement = (
                    i + 1,
                    x,
                    min_height,
                    x + width,
                    min_height + height,
                )
                return (placement,) + tail

        return None

    return_value = search(0, ((target_width, 0),))
    return list(return_value) if return_value is not None else None


def main() -> None:
    try:
        n = int(input())
        target_width, target_height = map(int, input().split())
        rectangles = [
            tuple(map(int, input().split()))
            for _ in range(n)
        ]
    except (EOFError, ValueError):
        print("нет")
        return

    if n < 0 or n >= 8:
        print("нет")
        return

    if (
        target_width <= 0
        or target_height <= 0
        or any(width <= 0 or height <= 0 for width, height in rectangles)
    ):
        print("нет")
        return

    answer = tile_rectangle(target_width, target_height, rectangles)
    if answer is None:
        print("нет")
        return

    print("да")
    for placement in answer:
        print(*placement)


if __name__ == "__main__":
    main()
