import sys
from typing import *
import time
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

    def _run(self, raw: str, verbose: bool = False, timeit: bool = False, part: int | None = None):
        self._verbose = verbose
        parsed = self.parse(raw)
        start = time.time()
        self._print(f"Parsed into {parsed}")

        if part in (None, 1):
            try:
                self._print("\nStarting Part 1")
                print(f'Part 1: {self.solve1(parsed)}')
            except Exception as e:
                print(f'Part 1 Failed! {e}')
                if verbose:
                    raise

            part1 = time.time()
            if timeit:
                print(f'Part 1 Time: {part1-start}s')

        if part in (None, 2):
            try:
                self._print("\nStarting Part 2")
                print(f'Part 2: {self.solve2(parsed)}')
            except Exception as e:
                print(f'Part 2 Failed! {e}')
                if verbose:
                    raise
            part2 = time.time()
            if timeit:
                print(f'Part 2 Time: {part2-part1}s')

    def _print(self, *args, **kwargs):
        if self._verbose:
            print(*args, **kwargs)

    def main(self):
        verbose = '-v' in sys.argv
        very_verbose = '-vv' in sys.argv
        time = '-t' in sys.argv
        part = 2 if '-2' in sys.argv else None

        if verbose:
            print("Running with verbosity")
        if very_verbose:
            print("Running with very verbosity")

        for i, sample in enumerate(self.samples):
            print(f'\nRunning on Sample Input {i+1}')
            self._run(sample, verbose=verbose or very_verbose, timeit=time, part=part)

        print('\nRunning for real')
        self._run(self._input, verbose=very_verbose, timeit=time, part=part)
