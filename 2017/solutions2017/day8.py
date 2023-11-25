from typing import *
from solutions2017.lib import Advent
from dataclasses import dataclass
import itertools, collections, functools
from parsita import *

class Day8Parsers(ParserContext, whitespace=r'[ \t]*'):
    register = reg(r'[a-z]+')
    comparison = reg(r'(<=|>=|>|<|==|!=)')
    integer = reg(r'[-+]?[0-9]+') > int
    cond = register & comparison & integer
    instruction = reg(r'(inc|dec)')
    inst = register & instruction & integer
    line = inst & (lit('if') >> cond)


@dataclass
class Cond:
    register: str
    comparison: Literal ['>', '<', '>=', '<=', '==', '!=']
    amount: int

@dataclass
class Inst:
    register: str
    instruction: Literal['inc', 'dec']
    amount: int
    condition: Cond

Input = List[Inst]

class Day8(Advent[Input]):
    day = 8

    samples = [
'''b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10'''
    ]

    def parse_line(self, line: str) -> Inst:
        resp = Day8Parsers.line.parse(line)
        insts, conds = resp.unwrap()
        r, c, a = conds
        cond = Cond(register=r, comparison=c, amount=a)
        r, i, a = insts
        return Inst(register=r, instruction=i, amount=a, condition=cond)

    def parse(self, raw: str) -> Input:
        return [self.parse_line(s) for s in raw.strip().splitlines()]

    def solve1(self, input: Input) -> Any:
        registers = collections.defaultdict(lambda: 0)
        maxever = 0

        for inst in input:
            cond = inst.condition
            if eval(f'{registers[cond.register]} {cond.comparison} {cond.amount}'):
                registers[inst.register] += (1 if inst.instruction == 'inc' else -1) * inst.amount
                maxever = max([maxever, max(registers.values())])

        return max(registers.values()), maxever

    def solve2(self, input: Input) -> Any:
        return 'See part 1'

if __name__ == '__main__':
    Day8().main()
