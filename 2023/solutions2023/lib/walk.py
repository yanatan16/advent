from typing import *

T = TypeVar('T')

def walk(start: T, connected: Callable[T, List[T]]) -> Set[T]:
    seen = set()
    untraveled = {start}

    while len(untraveled) > 0:
        next = untraveled.pop()
        seen.add(next)

        for conn in connected(next):
            if conn not in seen:
                untraveled.add(conn)

    return seen
