from typing import *
from solutions2023.lib import *

Input = List[str]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  line = p.reg(r'[.|\\/-]+')
  input = p.repsep(line, '\n')

Beam = Tuple[twod.Coord, twod.Direction]

class Day16(Advent[Input]):
    year = 2023
    day = 16

    samples = [
'''.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input, start=(twod.Coord(0,0), 'right')) -> Any:
      seen: Set[Beam] = set()
      pending: List[Beam] = [start]

      while len(pending) > 0:
        debug(f'Start search {pending[0]} ({pending[1:]})')
        beam = pending.pop()

        while beam not in seen and beam[0].inbounds(input):
          debug(f'Beam {beam}')
          seen.add(beam)
          coord, dir = beam

          match coord.get(input), dir:
            case '/', 'right':
              dir = 'up'
            case '/', 'up':
              dir = 'right'
            case '/', 'left':
              dir = 'down'
            case '/', 'down':
              dir = 'left'
            case '\\', 'right':
              dir = 'down'
            case '\\', 'down':
              dir = 'right'
            case '\\', 'left':
              dir = 'up'
            case '\\', 'up':
              dir = 'left'
            case ('-', 'down') | ('-', 'up'):
              pending += [(coord.right(), 'right'), (coord.left(), 'left')]
              break
            case ('|', 'right') | ('|', 'left'):
              pending += [(coord.up(), 'up'), (coord.down(), 'down')]
              break
            
          beam = (coord.move(dir), dir)

      return len({coord for coord, _dir in seen})

    def solve2(self, input: Input) -> Any:
      top_edge = [(twod.Coord(0, j), 'down') for j in range(len(input[0]))]
      bottom_edge = [(twod.Coord(len(input)-1, j), 'up') for j in range(len(input[0]))]
      left_edge = [(twod.Coord(i, 0), 'right') for i in range(len(input))]
      right_edge = [(twod.Coord(i, len(input[0])-1), 'left') for i in range(len(input))]

      return max(self.solve1(input, start=start)
                 for start in tqdm(top_edge + bottom_edge + left_edge + right_edge))

if __name__ == '__main__':
    Day16().main()
