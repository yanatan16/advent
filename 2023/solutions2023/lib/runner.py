from typing import *
from .input import get_input

Input = TypeVar('Input')

class Advent(Generic[Input]):
    year: int = 2017
    day: int
    samples: List[str] = []

    def __init__(self):
        self._input = get_input(self.year, self.day)

    def parse(self, raw: str) -> Input:
        pass

    def solve1(self, input: Input) -> str:
        pass

    def solve2(self, input: Input) -> str:
        pass

    def _run(self, raw: str):
        parsed = self.parse(raw)
        print(f'Part 1: {self.solve1(parsed)}')
        print(f'Part 2: {self.solve2(parsed)}')

    def main(self):
        for i, sample in enumerate(self.samples):
            print(f'Running on Sample Input {i+1} {sample}')
            self._run(sample)

        print('Running for real')
        self._run(self._input)
