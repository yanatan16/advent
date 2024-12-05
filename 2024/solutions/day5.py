from typing import *
from advent.lib import *

Order = Tuple[int, int]
Update = List[int]
Input = Tuple[List[Order], List[Update]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  page = UtilityParsers.integer
  order = page & (p.lit('|') >> page)
  update = p.repsep(page, ',')
  orders = p.repsep(order, '\n')
  updates = p.repsep(update, '\n')
  input = orders & (p.lit('\n\n') >> updates)

class Day5(Advent[Input]):
    year = 2024
    day = 5

    samples = [
'''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def middle_page(self, update: Update) -> int:
      self._print(f'middle page {update}')
      return update[len(update) // 2]

    def in_correct_order(self, update: Update, orders: List[Order]) -> bool:
      for low, high in orders:
        overlap = [page for page in update if page in (low, high)]
        if len(overlap) == 2 and tuple(overlap) == (high, low):
          return False
      return True

    def solve1(self, input: Input) -> Any:
      orders, updates = input
      return sum(
        self.middle_page(update)
        
        for update in updates
        if self.in_correct_order(update, orders)
      )

    def correct_ordering(self, update: Update, orders: List[Order]) -> List[int]:
      pages = set(update)
      relevant_orders = [order for order in orders if len(pages.intersection(order)) == 2]

      correct = []

      while len(pages) > 0:
        relevant_orders = [order for order in relevant_orders if len(pages.intersection(order)) == 2]
        highends = {high for low, high in relevant_orders}
        lowest = [page for page in pages if page not in highends]

        if len(lowest) == 0:
          raise ValueError(f'alg failed with no lowest pages: {pages} {relevant_orders}')

        correct += [lowest[0]]
        pages.remove(lowest[0])

      return correct


    def solve2(self, input: Input) -> Any:
      orders, updates = input


      return sum(
        self.middle_page(self.correct_ordering(update, orders))
        for update in updates
        if not self.in_correct_order(update, orders)
      )

if __name__ == '__main__':
    Day5().main()
