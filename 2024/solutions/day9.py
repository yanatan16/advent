from typing import *
from advent.lib import *

Input = List[int] # List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  digit = p.reg(r'[0-9]') > int
  line = p.rep(digit)
  input = line

class Day9(Advent[Input]):
    year = 2024
    day = 9

    samples = [
      '12345',
'''
2333133121414131402
'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      # mem = []
      # nfiles = (len(mem) + 1) // 2

      # for i, d in enumerate(input):
      #   if i % 2 == 0:
      #     id = i // 2
      #     mem += [id] * d
      #   else:
      #     mem += [None] * d

      # self._print(f'start:  {"".join(str(v if v is not None else ".") for v in mem)}')

      # while not all(v is not None for v in mem):
      #   self._print(f'step:   {"".join(str(v if v is not None else ".") for v in mem)}')
      #   if mem[-1] is None:
      #     mem = mem[:-1]
      #   else:
      #     v, mem = mem[-1], mem[:-1]
      #     for i in range(len(mem)):
      #       if mem[i] is None:
      #         mem[i] = v
      #         break


      # self._print(f'finish: {"".join(str(v) for v in mem)}')

      blocks = [(i // 2, d) for i,d in enumerate(input) if i % 2 == 0]
      memlen = sum(d for id, d in blocks)

      fronti = 0
      backi = memlen - 1

      def frontblock(n: int):
        for i, block in enumerate(input):
          if n >= block:
            n -= block
          elif i % 2 == 0:
            return i // 2
          else:
            return None
      
      def reverseblock(n: int):
        for id, block in reversed(blocks):
          if n >= block:
            n -= block
          else:
            return id

      checksum = 0
      backcounter = 0

      for i in tqdm(range(memlen)):
        id = frontblock(i)
        if id is None:
          id = reverseblock(backcounter)
          backcounter += 1
        checksum += i * id

      return checksum


    def solve2(self, input: Input) -> Any:
      class File(NamedTuple):
        id: int
        size: int

      class Empty(NamedTuple):
        size: int

      nfiles = (len(input) + 1) // 2
      mem = [
        File(id=i // 2, size=d)
        if i % 2 == 0
        else Empty(size=d)
        for i, d in enumerate(input)
      ]

      def compact(memory: List[Empty | File]) -> List[Empty | File]:
        newmem = []
        for block in memory:
          if isinstance(block, Empty) and isinstance(newmem[-1], Empty):
            newmem[-1] = Empty(newmem[-1].size + block.size)
          else:
            newmem += [block]

        return newmem

      def move(memory: List[Empty | File], fileid: int) -> List[Empty | File]:
        ifile, f = [(i, f) for i, f in enumerate(mem) if isinstance(f, File) and f.id == id][0]
        newmem = []
        moved = False

        for i, block in enumerate(memory):
          if block == f and moved:
            newmem += [Empty(size=f.size)]
          elif not moved and isinstance(block, Empty) and block.size >= f.size and i < ifile:
            moved = True
            if block.size == f.size:
              newmem += [f]
            else:
              newmem += [f, Empty(size=block.size - f.size)]
          else:
            newmem += [block]

        return newmem

      for id in tqdm(range(nfiles - 1, 0, -1)):
        mem = compact(move(mem, id))

      self._print(f'finish: {mem}')

      checksum = 0
      n = 0
      for block in mem:
        if isinstance(block, File):
          checksum += sum(x*block.id for x in range(n, n + block.size))
        n += block.size

      return checksum

if __name__ == '__main__':
    Day9().main()
