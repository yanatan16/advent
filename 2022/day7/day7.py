# Advent of Code 2022 Day 7
import sys
from typing import *
from dataclasses import dataclass
from itertools import takewhile

@dataclass
class Input:
    lines: List[str]

@dataclass
class Directory:
    name: str
    parent: Optional['Directory'] = None
    files: Optional[List[Tuple[int, str]]] = None
    folders: Optional[List['Directory']] = None

    def get(self, name: str) -> 'Directory':
        return [f for f in self.folders if f.name == name][0]

    def size(self):
        return sum(size for size,_ in self.files) + sum(f.size() for f in self.folders)

    def all_folders_size(self, prefix: str) -> List[Tuple[int, str]]:
        our_prefix = f'{prefix}/{self.name}' if prefix != '/' else f'/{self.name}'
        sub_folders = [
            entry
            for folder in self.folders
            for entry in folder.all_folders_size(our_prefix)
        ]

        our_size = self.size()
        return [(our_size, our_prefix)] + sub_folders

    def __str__(self) -> str:
        return '\n'.join(
            [self.name] +
            [f' {size} {name}' for size, name in self.files] +
            [' ' + line for f in self.folders for line in str(f).splitlines()]
        )

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        lines=[
            line for line in raw.splitlines()
        ]
    )

def execute(input: Input) -> Directory:
    if input.lines[0] != '$ cd /' and input.lines[1] != '$ ls':
        raise Exception('expected cd / and ls first')

    top: Directory = Directory(name='')
    cur: Directory
    rest = input.lines

    while len(rest) > 0:
        assert rest[0][0] == '$'
        cmd = rest[0].split('$ ')[1]
        rest = rest[1:]

        if cmd.startswith('cd'):
            dir = cmd.split(' ')[1]

            if dir == '/':
                cur = top

            elif dir == '..':
                assert cur.parent is not None
                cur = cur.parent

            else:
                matching_folder = [f for f in cur.folders if f.name == dir]
                assert len(matching_folder) == 1
                cur = matching_folder[0]

        elif cmd == 'ls':
            output = list(takewhile(lambda line: line[0] != '$', rest))
            rest = rest[len(output):]

            cur.folders = []
            cur.files = []
            for line in output:
                dir_or_size, name = line.split(' ')
                if dir_or_size == 'dir':
                    cur.folders += [Directory(name, parent=cur)]
                else:
                    cur.files += [(int(dir_or_size), name)]

    return top

def part1(input: Input) -> Output:

    tree = execute(input)
    print(tree)
    all = tree.all_folders_size('')

    print()
    print(all)

    sum = 0
    for size, name in all:
        if size <= 100000:
            print('counting', name, size)
            sum += size

    return sum

def part2(input: Input) -> Output:
    tree = execute(input)

    total_disk = 70000000
    need_disk = 30000000
    taken_disk = tree.size()
    avail_disk = total_disk - taken_disk
    need_to_delete = need_disk - avail_disk

    print('need to delete', need_to_delete)

    folder_sizes = tree.all_folders_size('')
    folder_sizes.sort()

    for size, name in folder_sizes:
        if size >= need_to_delete:
            print('found', size, name)
            return size

    return -1

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
