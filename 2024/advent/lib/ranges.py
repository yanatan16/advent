from typing import *

class Range(NamedTuple):
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length

    def __str__(self) -> str:
        return f'({self.start}:{self.length})'

    def overlap(self, other: 'Range') -> bool:
        return self.start <= other.start < self.end or other.start <= self.start < other.end

    def contains(self, other: Union[int, 'Range']) -> bool:
        if isinstance(other, int):
            return self.start <= other < self.end
        else:
            return self.start <= other.start < self.end and self.start < other.end <= self.end

    def merge(self, other: 'Range') -> 'Range':
        assert self.overlap(other)
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        return Range(start=start, length=end-start)

    @staticmethod
    def merge_all(rs: List['Range']) -> List['Range']:
        out: List[Range] = []

        for range in sorted(rs):
          if len(out) == 0 or not out[-1].overlap(range):
            out += [range]
          else:
            out[-1] = out[-1].merge(range)

        return out

    def split_around(self, other: 'Range') -> Tuple[Optional['Range'], List['Range']]:
        '''Split this range around another range. Return a tuple of a range that is contained inside the other and a list of ranges that are outside.'''

        if not self.overlap(other):
            return None, [self]
        elif other.contains(self):
            return self, []
        elif self.contains(other):
            return other, [
                Range(self.start, other.start - self.start),
                Range(other.end, self.end - other.end)
            ]
        elif self.start <= other.start < self.end:
            # Other start is in contained but end is not
            return (
                Range(other.start, self.end - other.start),
                [Range(self.start, other.start - self.start)]
            )
        else:
            return (
                Range(self.start, other.end - self.start),
                [Range(other.end, self.end - other.end)]
            )


