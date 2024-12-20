from typing import *

BinarySearchBoolF = Callable[[int], bool]

def binary_search_bool(low: int, high: int, f: BinarySearchBoolF) -> int:
    """
    Return the first x between low and high that switches
    f(x) from False to True
    """
    if low == high-1:
        assert f(low) == False
        assert f(high) == True
        return high

    elif low == high:
        if f(low) == False:
            return binary_search_bool(low, low+1, f)
        else:
            return binary_search_bool(low-1, low, f)

    else:
        mid = (high + low) // 2
        if f(mid) == False:
            return binary_search_bool(mid, high, f)
        else:
            return binary_search_bool(low, mid, f)
