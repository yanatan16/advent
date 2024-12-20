from typing import *
from advent.lib import *

Input = Tuple[List[int], List[int]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  register = p.reg(r'Register [ABC]:') >> UtilityParsers.integer
  registers = p.repsep(register, '\n')
  program = p.lit('Program:') >> p.repsep(UtilityParsers.integer, ',')
  input = registers & (p.lit('\n\n') >> program)

@dataclass
class ThreeBitComputer:
  instructions: List[int]
  registers: List[int]
  output: List[int]
  ipointer: int = 0

  def __str__(self):
    return f'Registers: {self.registers} Output: {self.output} IPointer: {self.ipointer}'

  def combo(self, operand: int) -> int:
    if operand <= 3:
      return operand
    return self.registers[operand - 4]

  def adv(self, operand: int):
    self.registers[0] = self.registers[0] // (2 ** self.combo(operand))

  def bxl(self, operand: int):
    self.registers[1] = self.registers[1] ^ operand

  def bst(self, operand: int):
    self.registers[1] = self.combo(operand) % 8

  def jnz(self, operand: int):
    if self.registers[0] != 0:
      self.ipointer = operand - 2

  def bxz(self, _operand: int):
    self.registers[1] = self.registers[1] ^ self.registers[2]

  def out(self, operand: int):
    self.output += [self.combo(operand) % 8]

  def bdv(self, operand: int):
    self.registers[1] = self.registers[0] // (2 ** self.combo(operand))

  def cdv(self, operand: int):
    self.registers[2] = self.registers[0] // (2 ** self.combo(operand))

  def execute(self, opcode: int, operand: int):
    if opcode == 0:
      self.adv(operand)
    elif opcode == 1:
      self.bxl(operand)
    elif opcode == 2:
      self.bst(operand)
    elif opcode == 3:
      self.jnz(operand)
    elif opcode == 4:
      self.bxz(operand)
    elif opcode == 5:
      self.out(operand)
    elif opcode == 6:
      self.bdv(operand)
    elif opcode == 7:
      self.cdv(operand)

  def step(self) -> bool:
    if 0 <= self.ipointer < len(self.instructions):
      self.execute(self.instructions[self.ipointer], self.instructions[self.ipointer + 1])
      self.ipointer += 2
      return True
    else:
      return False

  def complete(self, keep_going: Callable[[List[int]], bool]) -> List[int]:
    while self.step() and keep_going:
      pass
    return self.output


class Day17(Advent[Input]):
    year = 2024
    day = 17

    samples = [
      '''
      Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
      ''',
      '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      registers, instructions = input
      computer = ThreeBitComputer(instructions=instructions, registers=[r for r in registers], output=[])

      while computer.step():
        self._print(computer)

      return ','.join(map(str, computer.output))

    def solve2_direct_failed(self, input: Input) -> Any:
      registers, instructions = input

      def interpret(a: int) -> Generator[int, None, None]:
        while a > 0:
          yield ((a % 8) ^ 6) ^ (a // (2**((a%8)^3))) % 8
          a = a // 8

      istrlen = len(instructions)
      for a in tqdm(range(8**istrlen, 8**(istrlen + 1))):
        if list(interpret(a)) == instructions:
          return a

    def solve2(self, input: Input) -> Any:
      registers, instructions = input

      if registers[0] in (729,2024):
        return -1

      def run(a: int):
        computer = ThreeBitComputer(instructions=instructions, registers=[a, registers[1], registers[2]], output=[])
        return computer.complete(lambda output: True)

      # each iteration reduces A by 8
      # So we run backwards looking for any A that produces the tail of instructions
      # Then we multiply by 8 and look at the next 8 numbers for producing the next tail
      # At each step, multiple A's can produce the tail so we have to keep track of them all and increase them
      # Although some will not keep going

      def findas(base: int, i: int) -> Generator[int, None, None]:
        for a in range(base * 8, base * 8 + 8):
          if run(a) == instructions[(-i-1):]:
            yield a

      bases = [0]
      for i in range(len(instructions)):
        bases = [
          a for base in bases for a in findas(base, i)
        ]
        self._print(f'At step {i} all {bases} produce the tail {instructions[(-i-1):]}')

      return bases[0]




if __name__ == '__main__':
    Day17().main()
