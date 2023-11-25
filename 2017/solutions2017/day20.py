from typing import *
from dataclasses import dataclass
import itertools, collections, functools, math
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

@dataclass
class Particle:
  position: threed.Coord
  velocity: threed.Coord
  acceleration: threed.Coord
  id: int | None = None


Input = List[int]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  threed_coord = '<' >> (p.repsep(UtilityParsers.integer, ',', min=3, max=3) > (lambda trip: threed.Coord(*trip))) << '>'
  position = p.lit('p=') >> threed_coord
  velocity = p.lit('v=') >> threed_coord
  acceleration = p.lit('a=') >> threed_coord
  particle = ((position << p.lit(',')) & (velocity << p.lit(',')) & acceleration) > (lambda trip: Particle(*trip))
  input = p.repsep(particle, UtilityParsers.newline)


class Day20(Advent[Input]):
    day = 20

    samples = [
# '''p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
# p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>''',

      '''p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      return min(
        enumerate(input),
        key=lambda pair: pair[1].acceleration.norm1()
      )[0]

    def solve2(self, input: Input) -> Any:
      ps = input

      for step in tqdm(range(5000)):
        for p in ps:
          p.velocity += p.acceleration
          p.position += p.velocity

        collision_points = {pos for pos, grp in itertools.groupby(sorted(p.position for p in ps)) if sum(1 for _ in grp) > 1}
        colliders = [p for p in ps if p.position in collision_points]

        if colliders:
          print(f'At step {step} {len(colliders)} collided at {len(collision_points)}')

        ps = [p for p in ps if p.position not in collision_points]

      return len(ps)

if __name__ == '__main__':
    Day20().main()
