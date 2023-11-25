from typing import *
from dataclasses import dataclass
from enum import Enum
import itertools, collections, functools
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *


DEBUG = True

class Set(NamedTuple):
  reg: str
  val: int | str

class Sub(NamedTuple):
  reg: str
  val: int | str

class Mul(NamedTuple):
  reg: str
  val: int | str

class JumpNotZero(NamedTuple):
  ifx: int | str
  offset: int | str

Instruction = Set | Mul | Sub | JumpNotZero
Input = List[Instruction]

UP = UtilityParsers
class Parsers(UtilityParsers):
  register = UP.char
  int_or_reg = register | UP.integer
  pair = register & int_or_reg
  set = p.lit('set') >> pair > (lambda p: Set(*p))
  mul = p.lit('mul') >> pair > (lambda p: Mul(*p))
  sub = p.lit('sub') >> pair > (lambda p: Sub(*p))
  jump_not_zero = p.lit('jnz') >> (int_or_reg & int_or_reg) > (lambda p: JumpNotZero(*p))
  instruction = set | sub | mul | jump_not_zero
  input = p.repsep(instruction, UP.newline)

class Duet23:
  class Terminate(NamedTuple):
    count: int

  instructions: List[Instruction]
  ptr: int = 0
  regs: Dict[str, int]
  mul_counter: int = 0
  inst_counter: int = 0
  debug = False

  def __init__(self, instructions: List[Instruction]):
    self.instructions = instructions
    self.ptr = 0
    self.regs = collections.defaultdict(lambda: 0)

  def get(self, reg_or_int: str | int) -> int:
    if isinstance(reg_or_int, str):
      return self.regs[reg_or_int]
    else:
      return reg_or_int

  def exec_instruction(self, inst: Instruction):
    if self.debug:
      print(f'exec {self.ptr} {inst} ({self.regs["h"]})')

    self.inst_counter += 1
    match inst:
      case Set(reg=reg,val=val):
        self.regs[reg] = self.get(val)
        self.ptr += 1
      case Sub(reg=reg,val=val):
        self.regs[reg] -= self.get(val)
        self.ptr += 1
      case Mul(reg=reg,val=val):
        self.regs[reg] *= self.get(val)
        self.ptr += 1
        self.mul_counter += 1
      case JumpNotZero(ifx=ifx, offset=offset):
        if self.get(ifx) != 0:
          self.ptr += self.get(offset)
        else:
          self.ptr += 1

  def exec(self) -> Terminate:
    while 0 <= self.ptr < len(self.instructions):
      self.exec_instruction(self.instructions[self.ptr])

    return Duet23.Terminate(self.mul_counter)


def program() -> int:
  debug = True
  a = b = c = d = e = f = g = h = 0

  a = 1  # part 2 condition
  c = b = 57 # 1-2
  # 3 always jumps 2 to 5

  b *= 100 # 5
  b += 100000 #6
  c = b + 17000 #7-8

  f = 1 #9
  d = 2 #10

  while True: # Line 11 jumps to here
    if debug:
      print(f'a={a} b={b} c={c} d={d} e={e} f={f} g={g} h={h}')
    e = 2 # 11

    while True: # Line 12 jumps to here
      if d * e == b: # 12-15
        f = 0 #16

      e += 1 #17

      if e != b: #18-20
        continue # line 20 jumps -8 to 12

      # e == b on line 20
      d += 1
      if d != b: # 22-24
        break # line 24 jumps -13 to 11

      # d == b on line 24
      if f == 0: #25
        h += 1 # 26

      if b == c: # 27-29
        return h # Line 30 jumps off the program

      b += 17
      break # Line 32 jumps -23 to 11


def program2():
  h = 0

  for b in range(105700, 122700+17, 17):
    # if b is not prime
    for d in range(2, b):
      if b % d == 0 and 2 <= int(b/d) < b:
        h += 1
        break

  return h

class Day23(Advent[Input]):
    day = 23

    samples = [

    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
        cpu = Duet23(input)
        return cpu.exec().count

    def solve2(self, input: Input) -> Any:
      def isprime(n: int) -> bool:
        return not any(n % x == 0 and 2 <= int(n/x) < n for x in range(2,n))

      return sum(1 if not isprime(n) else 0 for n in range(105700, 122700+17, 17))


if __name__ == '__main__':
    Day23().main()
