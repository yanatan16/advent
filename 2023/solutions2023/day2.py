from typing import *
from solutions2023.lib import *

class Pull(NamedTuple):
  n: int
  color: Literal['red','blue','green']

class Game(NamedTuple):
  id: int
  sets: List[List[Pull]]

Input = List[Game]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  color = p.lit('red') | p.lit('green') | p.lit('blue')
  n = UtilityParsers.integer
  pull = (n & color) > (lambda pair: Pull(*pair))
  setofpulls = p.repsep(pull, ',')
  sets = p.repsep(setofpulls, ';')
  game = ((p.lit('Game') >> n << p.lit(':')) & sets) > (lambda pair: Game(*pair))
  input = p.repsep(game, '\n')

class Day2(Advent[Input]):
    year = 2023
    day = 2

    samples = [
'''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      def can_be_solved(game: Game, avail=dict(red=12, green=13, blue=14)):
        return all(avail[pull.color] >= pull.n for pulls in game.sets for pull in pulls)
      return sum(
        game.id if can_be_solved(game) else 0
        for game in input
      )

    def solve2(self, input: Input) -> Any:
      def lowest_amts_power(game: Game) -> int:
        return max(pull.n for pulls in game.sets for pull in pulls if pull.color == 'green') *\
          max(pull.n for pulls in game.sets for pull in pulls if pull.color == 'red') *\
          max(pull.n for pulls in game.sets for pull in pulls if pull.color == 'blue')

      return sum(lowest_amts_power(game) for game in input)

if __name__ == '__main__':
    Day2().main()
