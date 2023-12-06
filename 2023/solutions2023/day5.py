from typing import *
from solutions2023.lib import *

class AlmanacMap(NamedTuple):
  categories: Tuple[str, str]
  lines: List[List[int]]

class Almanac(NamedTuple):
  seeds: List[int]
  maps: List[AlmanacMap]

Input = Almanac

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  numbers = p.rep(UtilityParsers.integer, min=1)
  seeds = p.lit('seeds:') >> numbers
  category = p.reg(r'[a-z]+')
  categories = (p.repsep(category, '-to-') << p.lit('map:\n')) > (lambda pair: tuple(pair))
  almanac_map = (categories & p.repsep(numbers, '\n')) > (lambda pair: AlmanacMap(*pair))
  almanac = ((seeds << p.lit('\n\n')) & p.repsep(almanac_map, '\n\n')) > (lambda pair: Almanac(*pair))
  input = almanac

class Day5(Advent[Input]):
    year = 2023
    day = 5

    samples = [
'''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      def map_to(seed: int, lines: List[List[int]]) -> int:
        for dest_start, source_start, range_len in lines:
          if source_start <= seed < source_start + range_len:
            return dest_start + (seed - source_start)
        return seed

      maps_by_source = {
        map.categories[0]: map
        for map in input.maps
      }

      seeds = [n for n in input.seeds]
      category = 'seed'

      while category != 'location':
        map = maps_by_source[category]
        seeds = [map_to(seed, map.lines) for seed in seeds]
        category = map.categories[1]
      
      return min(seeds)

    def solve2(self, input: Input) -> Any:
      # Answer: 2295838615 maps to 100165128
      debug = False

      class RangeMap(NamedTuple):
        dest: int
        src: Range

        def flip(self) -> 'RangeMap':
          return RangeMap(self.src.start, Range(self.dest, self.src.length))

        def map(self, r: Range) -> Range:
          assert self.src.contains(r), f'Source {self.src} doesn\'t contain {r}'
          return Range(
            start=self.dest + r.start - self.src.start,
            length=r.length
          )

      def map_to(range: Range, rangemaps: List[RangeMap]) -> List[Range]:
        if range.length == 0:
          return []

        for rangemap in rangemaps:
          if rangemap.src.overlap(range):
            contained, others = range.split_around(rangemap.src)
            return [rangemap.map(contained)] + [rr for r in others for rr in map_to(r, rangemaps)]

        # No rangemap overlapped for this range
        return [range]

      rangemaps_regular = [
        (
          map.categories,
          [RangeMap(dest_start, Range(src_start, length))
           for dest_start, src_start, length in map.lines]
        )
        for map in input.maps
      ]

      rangemaps_flipped = [
        (
          (cats[1], cats[0]),
          [rmap.flip() for rmap in rmaps]
        )
        for cats, rmaps in rangemaps_regular
      ]

      def fully_map(seed_range: Range, start='seed', end='location', rangemaps=rangemaps_regular) -> List[Range]:
        ranges = [seed_range]
        category = start

        while category != end:
          cats, rmaps = [(cats, rmaps) for cats, rmaps in rangemaps if cats[0] == category][0]
          category = cats[1]
          next_ranges = [dest for src in ranges for dest in map_to(src, rmaps)]
          assert sum(r.length for r in next_ranges) == sum(r.length for r in ranges), f'Map_to changed the total length! {sum(r.length for r in next_ranges)} == {sum(r.length for r in ranges)}'

          ranges = Range.merge_all(next_ranges)

        return ranges

      seeds = [Range(start, length) for start, length in itertools.batched(input.seeds, 2)]

      print('# Forward-processing solution')
      forward_outcome = 100000000000
      for seed in seeds:
        end_ranges = sorted(fully_map(seed))
        forward_outcome = min(forward_outcome, min(r.start for r in end_ranges))
        print(f'Seed {seed} produced {end_ranges} with min {min(r.start for r in end_ranges)}')

      print('# Reverse-processing solution')
      reverse_outcome = 100000000000
      location_rmaps = [rmaps for cats, rmaps in rangemaps_flipped if cats[0] == 'location'][0]

      # Sort by source start (in location because of flip above)
      for rmap in sorted(location_rmaps, key=lambda rmap: rmap.src.start):
        reversed_seed_ranges = fully_map(rmap.src, start='location', end='seed', rangemaps=rangemaps_flipped)
        for rrange in reversed_seed_ranges:
          for seed_range in seeds:
            if seed_range.overlap(rrange):
              contained, _ = rrange.split_around(seed_range)
              assert contained is not None
              print(f'Location range {rmap.src} mapped to {contained} inside the seed')

              seed1 = Range(contained.start, 1)
              seed1_in_location = fully_map(seed1)
              print(f'So we remap {seed1} to {seed1_in_location}')

              reverse_outcome = min(reverse_outcome, min(r.start for r in seed1_in_location))

      return (forward_outcome, reverse_outcome)

if __name__ == '__main__':
    Day5().main()
