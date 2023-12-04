from typing import *
from solutions2023.lib import *

class Card(NamedTuple):
  id:int
  winning: List[int]
  yours: List[int]

Input = List[Card]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  numbers = p.rep(UtilityParsers.integer)
  card = ((p.lit('Card') >> UtilityParsers.integer << p.lit(':')) & numbers & (p.lit('|') >> numbers)) > (lambda trip: Card(*trip))
  input = p.repsep(card, '\n')

def matches(card: Card) -> int:
  winning = set(card.winning)
  return sum(1 if c in winning else 0 for c in card.yours)
def score(card: Card) -> int:
  cnt = matches(card)
  if cnt == 0:
    return 0
  else:
    return 2**int(cnt - 1)

class Day4(Advent[Input]):
    year = 2023
    day = 4

    samples = [
'''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      return sum(
        score(card)
        for card in input
      )

    def solve2(self, input: Input) -> Any:
      copies = {card.id: 1 for card in input}
      
      for card in input:
        sc = matches(card)
        if sc > 0:
          # print(f'card {card.id} with copies {copies[card.id]} scored {sc}')
          for i in range(sc):
            if (card.id + i + 1) in copies:
              # print(f'add {copies[card.id]} to card {card.id + i + 1}')
              copies[card.id + i + 1] += copies[card.id]

      # print([copies[card.id] for card in input])
      return sum(
        copies[card.id]
        for card in input
      )


if __name__ == '__main__':
    Day4().main()
