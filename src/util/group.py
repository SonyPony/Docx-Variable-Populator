from typing import List


def group_by_n(data: List, n: int) -> List[List]:
    for i in range(0, len(data), n):
        yield data[i:i+n]