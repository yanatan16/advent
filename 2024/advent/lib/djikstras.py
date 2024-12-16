from typing import *

from tqdm import tqdm

from .priorityqueue import PriorityQueue

T = TypeVar('T')
NeighborF = Callable[[T], Iterable[Tuple[T, float]]]

def djikstras(nodes: Iterable[T], start: T, neighbor: NeighborF) -> Tuple[Dict[T, float], Dict[T, List[T]]]:
    dist = {
        node: 0 if node == start else float('inf')
        for node in nodes
    }
    prev = {
        node: [] for node in nodes
    }

    queue = PriorityQueue(lambda node: dist[node])
    for node in nodes:
        queue.push(node)

    pbar = tqdm(total=len(queue))
    while len(queue):
        node = queue.pop()

        dists_changed = False
        for nn, cost in neighbor(node):
            alt = dist[node] + cost
            if alt == dist[nn]:
                prev[nn] += [node]
            elif alt < dist[nn]:
                prev[nn] = [node]
                dist[nn] = alt
                dists_changed = True

        if dists_changed:
            queue.resort()

        pbar.update(1)

    return dist, prev



