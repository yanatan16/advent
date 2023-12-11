from typing import *
from solutions2023.lib import *


class Pipe(Enum):
  empty = '.'
  vertical = '|'
  horizontal = '-'
  ne90 = 'L'
  se90 = 'F'
  nw90 = 'J'
  sw90 = '7'
  start = 'S'

  @property
  def connects_south(self) -> bool:
    return self in (Pipe.vertical, Pipe.se90, Pipe.sw90, Pipe.start)

  @property
  def connects_north(self) -> bool:
    return self in (Pipe.vertical, Pipe.ne90, Pipe.nw90, Pipe.start)

  @property
  def connects_west(self) -> bool:
    return self in (Pipe.horizontal, Pipe.sw90, Pipe.nw90, Pipe.start)

  @property
  def connects_east(self) -> bool:
    return self in (Pipe.horizontal, Pipe.se90, Pipe.ne90, Pipe.start)

Line = List[Pipe | None]
Input = List[Line]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  pipe = p.reg('[|\-LFJ7S.]') > (lambda c: Pipe(c))
  line = p.rep(pipe)
  input = p.repsep(line, '\n')

def next_poss(c: twod.Coord, input: Input) -> List[twod.Coord]:
  poss = [
    c.up() if c.get(input).connects_north and c.up().get(input) and c.up().get(input).connects_south else None,
    
    c.down() if c.get(input).connects_south and c.down().get(input) and c.down().get(input).connects_north else None,
    c.right() if c.get(input).connects_east and c.right().get(input) and c.right().get(input).connects_west else None,
    c.left() if c.get(input).connects_west and c.left().get(input) and c.left().get(input).connects_east else None
  ]

  return [c for c in poss if c is not None]

# Now implement search
def search_for_loop(target: twod.Coord, input: Input) -> List[twod.Coord]:
  paths: List[List[twod.Coord]] = [[target]]

  while len(paths) > 0:
    path = paths.pop()
    for poss in next_poss(path[-1], input):
      if poss == target and len(path) > 2:
        return path
      elif poss not in path:
        paths += [path + [poss]]

  assert False, 'Failed to find a loop'

def find_start(input: Input) -> twod.Coord:
  return [
    c for c in twod.Coord.all_coords(len(input), len(input[0]))
    if c.get(input) == Pipe.start
  ][0]

class Day10(Advent[Input]):
    year = 2023
    day = 10

    samples = [
'''.....
.S-7.
.|.|.
.L-J.
.....''',

      '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ''',

      '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      loop = search_for_loop(find_start(input), input)
      return int(len(loop) / 2)

    def solve2(self, input: Input) -> Any:
      loop = search_for_loop(find_start(input), input)

      debug(
        '\n'.join(
          ''.join(
            '#' if twod.Coord(i,j) in loop else '.'
            for j in range(len(input[0]))
          )
          for i in range(len(input))
        )
      )

      if len(loop) > 100:
        loop = loop[::-1]

      colored = [[0 for _ in range(len(input[0]))]
                 for _ in range(len(input))]

      def spread(c: twod.Coord, value: int = 1):
        visited = set()
        to_visit = [c]
        while len(to_visit):
          c = to_visit.pop()
          visited.add(c)
          if c not in loop and c.inbounds(colored):
            c.set(colored, c.get(colored) + value)
            for d in c.neighbors():
              if d not in visited:
                to_visit += [d]

      for c1, c2 in zip(loop, loop[1:] + [loop[0]]):
        p1 = c1.get(input)

        if (p1, c2) == (Pipe.horizontal, c1.right()):
          spread(c1.down())
        elif (p1, c2) == (Pipe.horizontal, c1.left()):
          spread(c1.up())
        elif (p1, c2) == (Pipe.vertical, c1.up()):
          spread(c1.right())
        elif (p1, c2) == (Pipe.vertical, c1.down()):
          spread(c1.left())
        elif (p1, c2) == (Pipe.ne90, c1.up()):
          spread(c1.up().right())
        elif (p1, c2) == (Pipe.ne90, c1.right()):
          spread(c1.down())
          spread(c1.down().left())
          spread(c1.left())
        elif (p1, c2) == (Pipe.se90, c1.right()):
          spread(c1.down().right())
        elif (p1, c2) == (Pipe.se90, c1.down()):
          spread(c1.up())
          spread(c1.up().left())
          spread(c1.left())
        elif (p1, c2) == (Pipe.sw90, c1.down()):
          spread(c1.down().left())
        elif (p1, c2) == (Pipe.sw90, c1.left()):
          spread(c1.up())
          spread(c1.up().right())
          spread(c1.right())
        elif (p1, c2) == (Pipe.nw90, c1.left()):
          spread(c1.up().left())
        elif (p1, c2) == (Pipe.nw90, c1.up()):
          spread(c1.down())
          spread(c1.down().right())
          spread(c1.right())

      debug(
        '\n'.join(
          ''.join(
            '#' if twod.Coord(i,j) in loop else str(twod.Coord(i,j).get(colored))
            for j in range(len(input[0]))
          )
          for i in range(len(input))
        )
      )

      return sum(1 if c else 0 for row in colored for c in row)

if __name__ == '__main__':
    Day10().main()
