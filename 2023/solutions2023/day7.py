from typing import *
from solutions2023.lib import *

Hand = str
Bid = int
Input = List[Tuple[Hand, Bid]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  hand = p.reg(r'[2-9AKQJT]{5}')
  bet = UtilityParsers.integer
  input = p.repsep(hand & bet, '\n')

class HandType(Enum):
  five_of_a_kind = 10
  four_of_a_kind = 9
  full_house = 8
  three_of_a_kind = 7
  two_pair = 6
  one_pair = 5
  high_card = 4

  @staticmethod
  def calc(hand: Hand, part2 = False) -> 'HandType':
    freqs = {c: sum(1 for _ in grp) for c, grp in itertools.groupby(sorted(hand))}
    
    if part2 and 'J' in freqs:
      jokers = freqs['J']
      del freqs['J']
    else:
      jokers = 0

    counts = sorted(freqs.values())

    high_freq = counts[-1] if len(counts) > 0 else 0
    second_high_freq = counts[-2] if len(counts) > 1 else 0

    match high_freq + jokers, second_high_freq:
      case 5, _:
        return HandType.five_of_a_kind
      case 4, _:
        return HandType.four_of_a_kind
      case 3, 2:
        return HandType.full_house
      case 3, _:
        return HandType.three_of_a_kind
      case 2, 2:
        return HandType.two_pair
      case 2, _:
        return HandType.one_pair
      case 1, _:
        return HandType.high_card

    raise RuntimeError(f'Failed to match for high {high_freq} jokers {jokers} second {second_high_freq}')

card_value_d = {
  'T': 10,
  'J': 11,
  'Q': 12,
  'K': 13,
  'A': 14
}

def card_value(card: str, part2 = False) -> int:
  if part2 and card == 'J':
    return 1

  if card in card_value_d:
    return card_value_d[card]

  return int(card)

def hand_sortkey(h: Hand, part2 = False) -> int:
  return (
    card_value(h[4], part2=part2) +
    card_value(h[3], part2=part2) * 15 +
    card_value(h[2], part2=part2) * (15**2) +
    card_value(h[1], part2=part2) * (15**3) +
    card_value(h[0], part2=part2) * (15**4) +
    HandType.calc(h, part2=part2).value * (15**5)
  )

class Day7(Advent[Input]):
    year = 2023
    day = 7

    samples = [
'''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      # Sorts so low is first
      sorted_hands = sorted(input, key=lambda pair: hand_sortkey(pair[0]))
      return sum(
        pair[1] * (i+1)
        for i, pair in enumerate(sorted_hands)
      )

    def solve2(self, input: Input) -> Any:
      # Sorts so low is first
      sorted_hands = sorted(input, key=lambda pair: hand_sortkey(pair[0], part2=True))
      return sum(
        pair[1] * (i+1)
        for i, pair in enumerate(sorted_hands)
      )

if __name__ == '__main__':
    Day7().main()
