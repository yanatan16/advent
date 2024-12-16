# -*- coding: utf-8 -*-
from typing import *
import heapq

Item = TypeVar('Item')
class PriorityQueue(Generic[Item]):
    q: List[Item]
    total: int

    def __init__(self, key=lambda x: x):
        self.key = key
        self.q = []
        self.total = 0

    def push(self, item):
        heapq.heappush(self.q, (self.key(item), self.total, item))
        self.total += 1

    def pop(self):
        return heapq.heappop(self.q)[2]

    def resort(self):
        newq = []
        for _, order, item in self.q:
            heapq.heappush(newq, (self.key(item), order, item))
        self.q = newq

    def __len__(self) -> int:
        return len(self.q)
