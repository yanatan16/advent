from typing import *
from advent.lib import *
from advent.lib.twod import *

Input = List[List[str]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapline = p.reg(r'[.#SE]+') > (lambda s: [c for c in s])
  input = p.repsep(mapline, '\n')

class Day20(Advent[Input]):
    year = 2024
    day = 20

    samples = [
'''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, map: Input) -> Any:
      freqs = Coord.freqlist(map)
      start = freqs['S'][0]
      end = freqs['E'][0]
      walls = freqs['#']
      base_nodes = set(freqs['.']).union({start, end})

      dists, prevs = djikstras(
        nodes=base_nodes,
        start=start,
        neighbor=lambda node: [
          (nn, 1) for nn in node.neighbors()
          if nn in base_nodes
        ],
      )

      base_time = dists[end]
      base_paths = djikstras_paths(prevs, end)
      assert len(base_paths) == 1
      self._racepath = racepath = base_paths[0]
      racedict = {
        node: i
        for i, node in enumerate(racepath)
      }
      cheatmin = 50 if len(map) < 100 else 100
      cheats_over_100 = 0

      for wall in walls:
        adjacent_nodes = [
          (racedict[nn], nn) for nn in wall.neighbors()
          if nn in racedict
        ]

        if len(adjacent_nodes) > 1:
          adjsort = list(sorted(adjacent_nodes))
          lowtime = adjsort[0][0]
          hightime = adjsort[-1][0]
          cheat_time = hightime - lowtime - 2

          if cheat_time > 0:
            self._print(f'Removing wall {wall} cheats by {cheat_time}')

          if cheat_time >= cheatmin:
            cheats_over_100 += 1

      return cheats_over_100

    def solve2(self, input: Input) -> Any:
      racepath = self._racepath
      cheatmin = 50 if len(input) < 100 else 100
      cheats = 0
      cheatdict = {}

      for i, cheatstart in tqdm(enumerate(racepath)):
        for j in range(i+cheatmin+2, len(racepath)):
          cheatend = racepath[j]
          dist = (cheatend - cheatstart).manhatten_distance
          if dist <= 20 and (j - i - dist) >= cheatmin:
            self._print(f'Skipping from ({i},{cheatstart}) to ({j},{cheatend}) costs {dist} but saves {j-i} for a cheat of {j-i-dist}')
            cheats += 1
            cheatdict[j-i-dist] = cheatdict.get(j-i-dist, 0) + 1

      if self._verbose:
        for cheat, n in sorted(cheatdict.items()):
          self._print(f'There are {n} cheats for {cheat} distance')

      return cheats

if __name__ == '__main__':
    Day20().main()
