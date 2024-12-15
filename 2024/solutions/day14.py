from typing import *
from advent.lib import *

Coord = twod.Coord

class Robot(NamedTuple):
  p: Coord
  v: Coord

Input = List[Robot]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  coord = UtilityParsers.twod_coord
  robot = (p.lit('p=') >> coord) & (p.lit('v=') >> coord) > (lambda pair: Robot(*pair))
  line = robot
  input = p.repsep(line, '\n')

class Day14(Advent[Input]):
    year = 2024
    day = 14

    samples = [
'''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def step(self, r: Robot, xmax: int, ymax: int) -> Robot:
      x = (r.p.x + r.v.x) % xmax
      y = (r.p.y + r.v.y) % ymax
      return Robot(p=Coord(x,y), v=r.v)

    def solve1(self, input: Input) -> Any:
      if len(input) < 20:
        xmax, ymax = 11, 7
      else:
        xmax, ymax = 101, 103

      robots = input
      for _ in range(100):
        robots = [self.step(r, xmax, ymax) for r in robots]

      xhalf = (xmax - 1) / 2
      yhalf = (ymax - 1) / 2
      def quadrant(r: Robot) -> int | None:
        if r.p.x < xhalf and r.p.y < yhalf:
          return 1
        if r.p.x < xhalf and r.p.y > yhalf:
          return 2
        if r.p.x > xhalf and r.p.y < yhalf:
          return 3
        if r.p.x > xhalf and r.p.y > yhalf:
          return 4
        return None

      scores = {}
      for r in robots:
        q = quadrant(r)
        scores[q] = scores.get(q, 0) + 1

      return product(scores.get(q, 0) for q in range(1, 5))


    def solve2(self, input: Input) -> Any:
      if len(input) < 20:
        return -1
      else:
        xmax, ymax = 101, 103

      def disp(robots: List[Robot]):
        print('\n'.join(
          ''.join('X' if Coord(x,y) in posset else '.'
                  for x in range(xmax))
          for y in range(ymax)
        ))

      # This didn't work
      # def trunk_pct(posset: Set[Coord]) -> float:
      #   '''Percentage of the middle vertical line that has robots on it'''
      #   xhalf = (xmax - 1) / 2
      #   trunk_coords = [Coord(xhalf, y) for y in range(ymax)]
      #   return sum(
      #     1 if c in posset else 0
      #     for c in trunk_coords
      #   ) / ymax

      def connected_factor(posset: Set[Coord]) -> float:
        '''Average number of immediate neighbors per node in set'''
        return sum(
          sum(
            1 if neighbor in posset else 0
            for neighbor in node.neighbors()
          )
          for node in posset
        ) / len(posset)

      robots = input
      for step in range(1000000):
        robots = [self.step(r, xmax, ymax) for r in robots]
        posset = {r.p for r in robots}
        #if trunk_pct(posset) > 0.75 or connected_factor(posset) > 1:
        if connected_factor(posset) > 1:
          self._print(f'\n\nStep {step+1}')
          # self._print(f'Trunk Percent: {trunk_pct(posset)}%')
          self._print(f'Connected Factor: {connected_factor(posset)}%')
          disp(robots)
          return step+1

if __name__ == '__main__':
    Day14().main()
