import functools, itertools
from typing import *

class KnotHash:
    def _round(self, ls: List[int], lengths: List[int], cur: int = 0, skip: int = 0) -> Tuple[List[int], int, int]:
        size = len(ls)

        for length in lengths:
            rope = (ls + ls)[cur:(cur+length)][::-1]

            assert len(rope) == length, f'{rope}'

            if cur+length > len(ls):
                edge = len(ls) - cur
                ls[cur:] = rope[:edge]
                ls[:(length-edge)] = rope[edge:]
            else:
                ls[cur:(cur+length)] = rope

            cur = (cur + length + skip) % size
            skip += 1

            assert len(ls) == size, f'{ls}'

        return ls, cur, skip

    def _densify(self, hash: List[int]) -> List[int]:
        return [
            functools.reduce(lambda x, y: x ^ y, block)
            for block in itertools.batched(hash, 16)
        ]

    def _hash(self, lengths: List[int]) -> List[int]:
        ls = list(range(256))
        cur = 0
        skip = 0

        for _ in range(64):
            ls, cur, skip = self._round(ls, lengths, cur, skip)

        return self._densify(ls)

    def _lengths(self, key: str) -> List[int]:
        return [ord(c) for c in key.strip()] + [17, 31, 73, 47, 23]

    def _hexes(self, xs: List[int]) -> str:
        return ''.join(hex(x).replace('0x', '') for x in xs)

    def _binary(self, xs: List[int]) -> List[bool]:
        def tobin(n: int) -> List[bool]:
            bstr = bin(n).replace('0b', '')
            if len(bstr) < 8:
                return [False for _ in range(8 - len(bstr))] + [c=='1' for c in bstr]
            else:
                return [c=='1' for c in bstr]

        return [b
                for x in xs
                for b in tobin(x)]

    def hash(self, key: str, format: Literal['hex', 'binary', 'ints']='hex') -> str | List[bool] | List[int]:
        '''Hash a key (interpreted as ASCII bytes) to a hash (hex, binary, or ints)'''
        hash = self._hash(self._lengths(key))

        match format:
            case 'hex':
                return self._hexes(hash)
            case 'binary':
                return self._binary(hash)
            case 'ints':
                return hash


