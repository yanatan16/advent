from typing import *
from solutions2023.lib import *

Springs = str
Groups = List[int]
Record = Tuple[Springs, Groups]
Input = List[Record]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  n = UtilityParsers.integer
  groups = p.repsep(n, ',')
  springs = p.reg(r'[.#?]+')
  record = springs & groups
  line = record
  input = p.repsep(line, '\n')

@functools.cache
def possible_arrangements(springs: str, grps: Tuple[int]) -> int:
  if len(grps) == 0:
    if all(c != '#' for c in springs):
      # debug(f'arrange "{springs}" {grps} no grps with no # 1')
      return 1
    else:
      # debug(f'arrange "{springs}" {grps} no grps but have # 0')
      return 0
  if len(springs) < sum(grps) + len(grps) - 1:
    # debug(f'arrange "{springs}" {grps} not enough left 0')
    return 0

  grp = grps[0]


  if '?' in springs and ('#' not in springs or springs.index('?') < springs.index('#')):
    i = springs.index('?')
    if all(c in '#?' for c in springs[i:(i+grp)]) and\
       (i+grp) <= len(springs) and\
       (i+grp >= len(springs) or springs[i+grp] != '#'):
      if_used = possible_arrangements(springs[(i+grp+1):], grps[1:])
      if_not = possible_arrangements(springs[(i+1):], grps)
      # debug(f'arrange "{springs}" {grps} both {if_used} + {if_not} = {if_used + if_not}')
      return if_used + if_not
    else:
      ret = possible_arrangements(springs[(i+1):], grps)
      # debug(f'arrange "{springs}" {grps} dot {ret}')
      return ret
  elif '#' in springs:
    i = springs.index('#')
    if all(c in '#?' for c in springs[i:(i+grp)]) and\
       (i+grp >= len(springs) or springs[i+grp] != '#'):
      ret = possible_arrangements(springs[(i+grp+1):], grps[1:])
      # debug(f'arrange "{springs}" {grps} pound {ret}')
      return ret
    else:
      # debug(f'arrange "{springs}" {grps} illegal 0')
      return 0
  else:
    # debug(f'arrange "{springs}" {grps} no grps left 0')
    return 0

def is_arrangement_valid(springs: str, grps: List[int]) -> bool:
  return [len(g) for g in re.findall(r'#+', springs)] == grps

def all_possible_arrangements(springs: str) -> Generator[str, None, None]:
  qindices = [i for i, c in enumerate(springs) if c == '?']
  if len(qindices) == 0:
    yield springs

  for perm in itertools.product('.#', repeat=len(qindices)):
    permlist = list(perm)
    yield ''.join(c if c != '?' else permlist.pop() for c in springs)

def naive_count_valid_arrangements(springs: str, grps: List[int]) -> int:
  return sum(
    1 if is_arrangement_valid(arrangement, grps) else 0
    for arrangement in all_possible_arrangements(springs)
  )

class Day12(Advent[Input]):
    year = 2023
    day = 12

    samples = [
# problems
      '??##.?#?.?#?# 4, 3, 3',
      '.???..??##.. 2,4',

'''#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1''',

      '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1''',

    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      # This was used to find bugs
      # for record in input:
      #   arr = possible_arrangements(*record)
      #   correct_arr = naive_count_valid_arrangements(*record)

      #   if arr != correct_arr:
      #     print(f'{record}: {arr} != {correct_arr}')

      return sum(possible_arrangements(springs, tuple(grps)) for springs, grps in input)

    def solve2(self, input: Input) -> Any:
      def unfold(springs: str, grps: List[int]) -> Tuple[str, List[int]]:
        return '?'.join(itertools.repeat(springs, 5)), grps*5

      tot = 0
      for record in tqdm(input):
        springs, grps = unfold(*record)
        print(f'{springs} {grps}')
        tot += possible_arrangements(springs, tuple(grps))
      return tot


if __name__ == '__main__':
    Day12().main()
