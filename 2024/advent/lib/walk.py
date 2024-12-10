from typing import *

T = TypeVar('T')

def walk_bfs(start: T, connected: Callable[[T], List[T]]) -> Set[T]:
    seen = set()
    untraveled = {start}

    while len(untraveled) > 0:
        next = untraveled.pop()
        seen.add(next)

        for conn in connected(next):
            if conn not in seen:
                untraveled.add(conn)

    return seen

def walk_dfs(
        start: T,
        connected: Callable[[T], List[T]],
        done: Callable[[T], bool]
) -> List[List[T]]:
    def walk(node: T) -> List[List[T]]:
        if done(node):
            return [[node]]

        return [
            [node] + rest
            for n2 in connected(node)
            for rest in walk(n2)
        ]

    return walk(start)
