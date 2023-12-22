from typing import *
from solutions2023.lib import *

Coord = threed.Coord

Brick = Tuple[Coord, Coord]
Input = List[Brick]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  n = UtilityParsers.integer
  coord = p.repsep(n, ',', min=3, max=3) > (lambda p: Coord(*p))
  brick = p.repsep(coord, '~', min=2, max=2)
  input = p.repsep(brick, '\n')

def valid_disintegration(disintegrated: List[int], links: List[Tuple[int, int]]):
  before_disintegration = {supported for _, supported in links}
  after_disintegration = {supported for support, supported in links if support not in disintegrated}

  return before_disintegration == after_disintegration

class Day22(Advent[Input]):
    year = 2023
    day = 22

    samples = [
'''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def settle_bricks(self, input: Input) -> Any:
      bricks = [(i, b[0], b[1]) for i, b in enumerate(input)]
      bricks.sort(key=lambda b: min(b[1].z, b[1].z))

      settled: List[Tuple[int, Coord, Coord]] = []
      supports: Dict[Tuple[int,int], Tuple[int, int | None]] = {}
      links: List[Tuple[int, int]] = []

      for i, a, b in bricks:
        if a.x == b.x and a.y == b.y:
          v = (a.x, a.y)
          sz, si = supports.get(v, (0, -1))

          assert sz <= min(a.z, b.z)

          botz = sz + 1
          topz = botz + (b.z - a.z)

          settled += [(i, Coord(a.x, a.y, botz), Coord(b.x, b.y, topz))]
          supports[v] = (topz, i)
          links += [(si, i)]

        elif a.x == b.x and a.z == b.z:
          lowy = min(a.y, b.y)
          highy = max(a.y, b.y)

          vs = [(a.x, y) for y in range(lowy, highy+1)]
          poss_supports = [supports.get(v, (0, -1)) for v in vs]

          z = max(poss_supports, key=lambda p: p[0])[0]
          assert z < a.z

          settled += [(i, Coord(a.x, a.y, z+1), Coord(b.x, b.y, z+1))]

          for v in vs:
            supports[v] = (z+1, i)

          actual_links = {si for sz, si in poss_supports if sz == z}
          for link in actual_links:
            links += [(link, i)]

        else:
          lowx = min(a.x, b.x)
          highx = max(a.x, b.x)

          vs = [(x, a.y) for x in range(lowx, highx+1)]
          poss_supports = [supports.get(v, (0, -1)) for v in vs]

          z = max(poss_supports, key=lambda p: p[0])[0]
          assert z < a.z

          settled += [(i, Coord(a.x, a.y, z+1), Coord(b.x, b.y, z+1))]

          for v in vs:
            supports[v] = (z+1, i)

          actual_links = {si for sz, si in poss_supports if sz == z}
          for link in actual_links:
            links += [(link, i)]

      return bricks, links

    def solve1(self, input: Input) -> Any:
      bricks, links = self.settle_bricks(input)

      low_lookup = {support: [supported for _, supported in grp] for support, grp in itertools.groupby(sorted(links, key=lambda p: p[0]), key=lambda p: p[0])}
      high_lookup = {supported: [support for support, _ in grp] for supported, grp in itertools.groupby(sorted(links, key=lambda p: p[1]), key=lambda p: p[1])}

      multi_supporters = {
        i for i, *_ in bricks
        if i in low_lookup
        and all(len(high_lookup[supported]) > 1 for supported in low_lookup[i])
      }
      no_low_count = sum(1 if i not in low_lookup else 0 for i,a,b in bricks)

      return no_low_count + len(multi_supporters)



    def solve2(self, input: Input) -> Any:
      bricks, links = self.settle_bricks(input)
      low_lookup = {support: [supported for _, supported in grp] for support, grp in itertools.groupby(sorted(links, key=lambda p: p[0]), key=lambda p: p[0])}
      high_lookup = {supported: [support for support, _ in grp] for supported, grp in itertools.groupby(sorted(links, key=lambda p: p[1]), key=lambda p: p[1])}

      @functools.cache
      def simulate_disintegration(bid: int) -> int:
        removed = set()
        q = [bid]

        while q:
          nxt = q.pop(0)
          removed.add(nxt)

          for supported in low_lookup.get(nxt, []):
            supports = [b for b in high_lookup[supported] if b not in removed]
            if len(supports) == 0:
              q.append(supported)

        return len(removed) - 1

      #debug('\n'.join(f'{bid}: {simulate_disintegration(bid)}' for bid, *_ in bricks))

      return sum(simulate_disintegration(bid) for bid, *_ in bricks)

if __name__ == '__main__':
    Day22().main()
