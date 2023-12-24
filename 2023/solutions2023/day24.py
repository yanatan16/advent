from typing import *
from solutions2023.lib import *

Coord = threed.Coord
class Hailstone(NamedTuple):
  position: Coord
  velocity: Coord
Input = List[Hailstone]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#]+')
  n = UtilityParsers.integer
  vector = p.repsep(n, ',', min=3, max=3) > (lambda t: Coord(*t))
  hailstone = p.repsep(vector, '@') > (lambda p: Hailstone(*p))
  line = hailstone
  input = p.repsep(line, '\n')




class Day24(Advent[Input]):
    year = 2023
    day = 24

    samples = [
'''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      test_area = (7, 27) if len(input) < 10 else (200000000000000,400000000000000)
      tlow, thigh = test_area

      def intersection(h1: Hailstone, h2: Hailstone) -> bool:
        x1, y1, _ = h1.position
        x2, y2, _ = h1.position + h1.velocity
        x3, y3, _ = h2.position
        x4, y4, _ = h2.position + h2.velocity

        denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        numer_x = (x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)
        numer_y = (x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)

        if denom == 0:
          # No intersection
          debug(f'no intersection for {h1} {h2}')
          return False

        px = numer_x / denom
        py = numer_y / denom

        if px < tlow or px > thigh or py < tlow or py > thigh:
          debug(f'intersection outside bounds {h1} {h2}')
          return False

        if (px - x1)/h1.velocity.x < 0:
          debug(f'intersection in past for first {h1} {h2}')
          return False

        if (px - x3)/h2.velocity.x < 0:
          debug(f'intersection in past for second {h1} {h2} at ({px},{py})')
          return False

        debug(f'Found intersection {h1} {h2} at {px}, {py}')
        return True


      return sum(1 if intersection(h1, h2) else 0 for h1, h2 in itertools.combinations(input, 2))

    def solve2(self, input: Input) -> Any:
      # We need exactly 3 hailstones to determine the starting position and velocity
      # Because each hailstone adds one unknown (tn)

      # Symbols of unknowns
      px, py, pz, vx, vy, vz, t1, t2, t3 = sympy.symbols('px, py, pz, vx, vy, vz, t1, t2, t3')

      # First 3 hailstones
      p1, v1 = input[0]
      p2, v2 = input[1]
      p3, v3 = input[2]

      # Our system of equations
      f = (
        # p1/v1/t1
        px + vx*t1 - v1.x*t1 - p1.x,
        py + vy*t1 - v1.y*t1 - p1.y,
        pz + vz*t1 - v1.z*t1 - p1.z,
        # p2/v2/t2
        px + vx*t2 - v2.x*t2 - p2.x,
        py + vy*t2 - v2.y*t2 - p2.y,
        pz + vz*t2 - v2.z*t2 - p2.z,
        # p3/v3/t3
        px + vx*t3 - v3.x*t3 - p3.x,
        py + vy*t3 - v3.y*t3 - p3.y,
        pz + vz*t3 - v3.z*t3 - p3.z,
      )

      ret, = sympy.solve(f, (px, py, pz, vx, vy, vz, t1, t2, t3))
      p = Coord(*ret[:3])
      v = Coord(*ret[3:6])
      t1, t2, t3 = ret[6:]
      print(f'Solved! Rock is {p} @ {v} for t1 {t1} t2 {t2} t3 {t3}')
      return sum(p)

if __name__ == '__main__':
    Day24().main()
