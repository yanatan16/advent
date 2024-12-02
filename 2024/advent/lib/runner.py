import sys
from typing import *
from .input import get_input

Input = TypeVar('Input')

class Advent(Generic[Input]):
    year: int = 2023
    day: int
    samples: List[str] = []
    _verbose: bool = False

    def __init__(self):
        self._input = get_input(self.year, self.day)

    def parse(self, raw: str) -> Input:
        pass

    def solve1(self, input: Input) -> str:
        pass

    def solve2(self, input: Input) -> str:
        pass

    def _run(self, raw: str, verbose=False):
        self._verbose = verboase
        parsed = self.parse(raw)
        try:
            print(f'Part 1: {self.solve1(parsed)}')
        except Exception as e:
            print(f'Part 1 Failed! {e}')
            if verbose:
                raise e
        try:
            print(f'Part 2: {self.solve2(parsed)}')
        except Exception as e:
            print(f'Part 2 Failed! {e}')
            if verbose:
                raise e

    def _print(self, *args, **kwargs):
        if self._verbose:
            print(*args, **kwargs)

    def main(self):
        for i, sample in enumerate(self.samples):
            print(f'Running on Sample Input {i+1} {sample}')
            self._run(sample, verbose='-v' in sys.argv)

        print('Running for real')
        self._run(self._input)
