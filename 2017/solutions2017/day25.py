from typing import *
from dataclasses import dataclass
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

class StateCondition(NamedTuple):
  write: int
  move: Literal['right', 'left']
  state: str

class StateInstruction(NamedTuple):
  in_state: str
  if_zero: StateCondition
  if_one: StateCondition

class TuringMachine(NamedTuple):
  begin_state: str
  diagnostic_checksum: int
  state_instructions: List[StateInstruction]

Input = TuringMachine


class Parsers(p.ParserContext, whitespace=r'[ \t\n]*'):
  state = p.reg('[A-Z]')
  dir = p.reg(r'(left|right)')
  value = p.reg(r'(1|0)') > int

  begin_state = p.lit('Begin in state') >> state << p.lit('.')
  diagnostic_checksum = p.lit('Perform a diagnostic checksum after') >> UtilityParsers.integer << p.lit('steps.')
  cond_write = p.lit('- Write the value') >> value << p.lit('.')
  cond_move = p.lit('- Move one slot to the') >> dir << p.lit('.')
  cond_state = p.lit('- Continue with state') >> state << p.lit('.')
  state_condition = (
    cond_write & cond_move & cond_state
  ) > (
    lambda trip: StateCondition(*trip)
  )
  in_state = p.lit('In state') >> state << p.lit(':')
  if_zero = p.lit('If the current value is 0:') >> state_condition
  if_one = p.lit('If the current value is 1:') >> state_condition
  state_instruction = (in_state & if_zero & if_one) > (
    lambda trip: StateInstruction(*trip)
  )
  state_instructions = p.rep(state_instruction)
  turing_machine = (begin_state & diagnostic_checksum & state_instructions) > (
    lambda trip: TuringMachine(*trip)
  )
  input = turing_machine

class Day25(Advent[Input]):
    day = 25

    samples = [
'''Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      tape: Set[int] = set()
      ptr = 0
      state = input.begin_state
      instructions = {i.in_state:i for i in input.state_instructions}

      for step in tqdm(range(input.diagnostic_checksum)):
        inst = instructions[state]
        cond = inst.if_one if ptr in tape else inst.if_zero

        if cond.write == 1:
          tape = tape | {ptr}
        else:
          tape = tape - {ptr}
        ptr += 1 if cond.move == 'right' else -1
        state = cond.state

      return len(tape)



    def solve2(self, input: Input) -> Any:
        return 'Not implemented'

if __name__ == '__main__':
    Day25().main()
