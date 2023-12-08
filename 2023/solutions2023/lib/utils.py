from typing import *
import itertools

T = TypeVar('T')
K = TypeVar('K')

def freqlist(it: Iterable[T], key: Callable[[T], K] | None = None) -> Dict[K, List[T]]:
    return {k: list(grp) for k, grp in itertools.groupby(it, key=key)}

def freqs(it: Iterable[T], key: Callable[[T], K] | None = None) -> Dict[K, int]:
    return {k: sum(1 for _ in grp) for k, grp in itertools.groupby(it, key=key)}
