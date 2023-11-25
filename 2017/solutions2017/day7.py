from typing import *
from solutions2017.lib import Advent
from dataclasses import dataclass
from functools import cache
import itertools

@dataclass
class Node:
    name: str
    weight: int
    children: List[str]

Input = List[Node]

class Day7(Advent[Input]):
    day = 7

    samples = [
'''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)'''
    ]

    def parse_node(self, line: str) -> Node:
        name, rest = line.split(' (')
        weight, rest = rest.split(')')
        if rest:
            _, children_str = rest.split(' -> ')
            children = children_str.split(', ')
        else:
            children = []
        return Node(name=name, weight=int(weight), children=children)

    def parse(self, raw: str) -> Input:
        return [self.parse_node(line) for line in raw.strip().splitlines()]

    def solve1(self, input: Input) -> Any:
        # bottom node is one that is not mentioned as a child

        node_names = {node.name for node in input}
        children_names = {child for node in input for child in node.children}
        bottoms = node_names.difference(children_names)
        return list(bottoms)[0]

    def solve2(self, input: Input) -> Any:
        nodes = {node.name: node for node in input}

        @cache
        def weight(name: str) -> int:
            return nodes[name].weight + sum(weight(child) for child in nodes[name].children)

        @cache
        def balanced(name: str) -> bool:
            node = nodes[name]
            if len(node.children) < 2:
                return True

            weights = [weight(child) for child in node.children]
            return all(w == weights[0] for w in weights[1:])

        def child_weights(name: str) -> List[Tuple[str, int]]:
            return [(child, weight(child)) for child in nodes[name].children]

        bottom = self.solve1(input)

        bottom_weights = sorted(weight(child) for child in nodes[bottom].children)
        pairs = sorted([(sum(1 for _ in children), weight) for weight, children in itertools.groupby(bottom_weights)])

        assert len(pairs) == 2, f'{pairs}'

        diff = pairs[1][1] - pairs[0][1]

        cur = bottom
        while True:
            cw = {child: weight for child, weight in child_weights(cur)}
            weights = sorted(cw.values())
            offweights = [weight for weight, ls in itertools.groupby(weights) if sum(1 for _ in ls) == 1]

            if len(offweights) == 0:
                print(f'editing {cur} {nodes[cur].weight} to {nodes[cur].weight + diff}')
                return nodes[cur].weight + diff

            offweight = offweights[0]
            cur = [child for child, weight in cw.items() if weight == offweight][0]

        return 'Not implemented'

if __name__ == '__main__':
    Day7().main()
