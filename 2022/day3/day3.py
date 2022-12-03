# Advent of Code 2022 Day 3
import sys
from typing import List, Tuple, Set

Rucksack = Tuple[str, str]
Item = str # lower case character
Input = List[Rucksack]

Group = List[Rucksack]

def parse_input(raw: str) -> Input:
    split_in_half = lambda s: (s[:int(len(s) / 2)], s[int(len(s) / 2):])
    return [
        split_in_half(line) for line in raw.splitlines() if line
    ]

def find_shared_item(rucksack: Rucksack) -> Item:
    return list(set(rucksack[0]).intersection(set(rucksack[1])))[0]

def find_item(rucksack: Rucksack, item_search: Item) -> List[Item]:
    [
        item
        for item in (rucksack[0]+rucksack[1])
        if item.lower() == item_search.lower()
    ]

def priority(item: Item) -> int:
    if item == item.lower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27

def combine_rucksack(rucksack: Rucksack) -> Set[str]:
    return set(rucksack[0] + rucksack[1])

def part1(input: Input) -> int:
    return sum(priority(find_shared_item(rucksack)) for rucksack in input)

def part2(input: Input) -> int:
    sum = 0
    for i in range(int(len(input) / 3)):
        group = input[(i*3):(i*3+3)]

        try:
            badge = list(
                combine_rucksack(group[0])
                .intersection(combine_rucksack(group[1]))
                .intersection(combine_rucksack(group[2]))
            )[0]
            sum += priority(badge)
        except:
            print('group', group)
    
    return sum

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])

