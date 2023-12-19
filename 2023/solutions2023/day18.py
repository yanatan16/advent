from typing import *
from solutions2023.lib import *

Direction = Literal['R','L','U','D']
Color = str
class Instruction(NamedTuple):
  dir: Direction
  dist: int
  color: str

  @property
  def direction(self) -> twod.Direction:
    return {'R':'right','D':'down','L':'left','U':'up'}[self.dir]

Input = List[Instruction]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'): #type: ignore
  direction = p.reg('[RLUD]')
  color = p.lit('(#') >> p.reg(r'[a-f0-9]{6}') << p.lit(')')
  line = (direction & UtilityParsers.integer & color) > (lambda t: Instruction(*t))
  input = p.repsep(line, '\n')


class Day18(Advent[Input]):
    year = 2023
    day = 18

    samples = [
'''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      edges = []
      cur = twod.Coord(0,0)

      for instr in input:
        next = cur.move(instr.direction, n=instr.dist)
        edges += [twod.Edge(cur, next)]
        cur = next

      return twod.Edge.area(edges)

    def solve2(self, input: Input) -> Any:
      p2_input = [
        Instruction(
          dir={'0':'R','1':'D','2':'L','3':'U'}[instr.color[-1]],
          dist=int(instr.color[:-1], 16),
          color=instr.color
        )
        for instr in input
      ]

      return self.solve1(p2_input)

if __name__ == '__main__':
    Day18().main()
