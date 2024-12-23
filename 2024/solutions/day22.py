from typing import *
from advent.lib import *

Input = List[int]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  n = UtilityParsers.integer
  line = n
  input = p.repsep(line, '\n')

ChangeSeq = Tuple[int, int, int, int]

class Day22(Advent[Input]):
    year = 2024
    day = 22

    samples = [
      '''123''',
      '''1
10
100
2024''',
      '''1
2
3
2024'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def next_secret(self, secret: int) -> int:
      s1 = ((secret * 64) ^ secret) % 16777216
      s2 = ((s1 // 32) ^ s1) % 16777216
      s3 = ((s2 * 2048) ^ s2) % 16777216
      return s3

    def nth_secret(self, secret: int, n: int) -> int:
      for _ in range(n):
        secret = self.next_secret(secret)
      return secret

    def solve1(self, input: Input) -> Any:
      if len(input) == 1:
        secret = input[0]
        for i in range(11):
          self._print(f'step {i}: {secret}')
          secret = self.next_secret(secret)

      return sum(
        self.nth_secret(secret, 2000)
        for secret in input
      )
    # 7min

    def _seqprices(self, init_secret: int) -> Generator[Tuple[ChangeSeq, int], None, None]:
      prices = [init_secret % 10]
      secret = init_secret

      for _ in range(2000):
        secret = self.next_secret(secret)
        price = secret % 10
        if len(prices) == 4:
          seq = [p2 - p1 for p1, p2 in zip(prices, prices[1:] + [price])]
          yield (tuple(seq), price)
          prices = prices[1:]

        prices = prices + [price]

    def solve2(self, input: Input) -> Any:
      all_seqs = [
        tuple([p1, p2, p3, p4])
        for p1 in range(-9, 10)
        for p2 in range(-9, 10)
        for p3 in range(-9, 10)
        for p4 in range(-9, 10)
         if -10 < p1+p2 < 10
         and -10 < p2+p3 < 10
         and -10 < p3+p4 < 10
      ]

      sales = {}
      for secret in tqdm(input):
        monkey = {}
        for seq, price in self._seqprices(secret):
          if seq not in monkey:
            monkey[seq] = price
          if len(monkey) == len(all_seqs):
            break

        sales[secret] = monkey

      return max(
        sum(
          sales[secret].get(seq, 0)
          for secret in input
        )
        for seq in all_seqs
      )

if __name__ == '__main__':
    Day22().main()
