from typing import *
from dataclasses import dataclass
import itertools, collections, functools, multiprocessing, queue
import multiprocessing.pool
import parsita as p
from tqdm import tqdm
from solutions2017.lib import *

debug = False

class Sound(NamedTuple):
  freq: int | str

class Set(NamedTuple):
  reg: str
  val: int | str

class Add(NamedTuple):
  reg: str
  val: int | str

class Mul(NamedTuple):
  reg: str
  val: int | str

class Mod(NamedTuple):
  reg: str
  val: int | str

class Recover(NamedTuple):
  ifx: int | str

class Jump(NamedTuple):
  ifx: int | str
  offset: int | str

Instruction = Sound | Set | Add | Mul | Mod | Recover | Jump
Input = List[Instruction]

UP = UtilityParsers
class Parsers(UtilityParsers):
  register = UP.char
  int_or_reg = register | UP.integer
  sound = p.lit('snd') >> int_or_reg > (lambda f: Sound(f))
  pair = register & int_or_reg
  set = p.lit('set') >> pair > (lambda p: Set(*p))
  add = p.lit('add') >> pair > (lambda p: Add(*p))
  mul = p.lit('mul') >> pair > (lambda p: Mul(*p))
  mod = p.lit('mod') >> pair > (lambda p: Mod(*p))
  recover = p.lit('rcv') >> int_or_reg > (lambda x: Recover(x))
  jump = p.lit('jgz') >> (int_or_reg & int_or_reg) > (lambda p: Jump(*p))
  instruction = sound | set | add | mul | mod | recover| jump
  input = p.repsep(instruction, UP.newline)


class Duet:
  class RecoveredSound(NamedTuple):
    freq: int

  class DoJump(NamedTuple):
    offset: int

  regs = collections.defaultdict(lambda: 0)
  last_sound: int | None = None

  def get(self, reg_or_int: str | int) -> int:
    if isinstance(reg_or_int, str):
      return self.regs[reg_or_int]
    else:
      return reg_or_int

  def exec(self, inst: Instruction) -> None | RecoveredSound | DoJump:
    match inst:
      case Sound(freq=freq):
        self.last_sound = self.get(freq)
      case Set(reg=reg,val=val):
        self.regs[reg] = self.get(val)
      case Add(reg=reg,val=val):
        self.regs[reg] += self.get(val)
      case Mul(reg=reg,val=val):
        self.regs[reg] *= self.get(val)
      case Mod(reg=reg,val=val):
        self.regs[reg] = self.regs[reg] % self.get(val)
      case Recover(ifx=ifx):
        if self.get(ifx) != 0:
          return Duet.RecoveredSound(self.last_sound)
      case Jump(ifx=ifx, offset=offset):
        if self.get(ifx) > 0:
          return Duet.DoJump(self.get(offset))



class Duet2:
  class Terminate(NamedTuple):
    count: int

  class DoJump(NamedTuple):
    offset: int

  instructions: List[Instruction]
  ptr: int = 0
  regs = collections.defaultdict(lambda: 0)
  receive_queue: multiprocessing.Queue
  send_queue:  multiprocessing.Queue

  def __init__(self, id: int, instructions: List[Instruction], rqueue: multiprocessing.Queue, squeue: multiprocessing.Queue):
    self.id = id
    self.instructions = instructions
    self.ptr = 0
    self.regs = collections.defaultdict(lambda: 0)
    self.regs['p'] = id
    self.receive_queue = rqueue
    self.send_queue = squeue
    self.send_counter = 0

  def get(self, reg_or_int: str | int) -> int:
    if isinstance(reg_or_int, str):
      return self.regs[reg_or_int]
    else:
      return reg_or_int

  def exec_instruction(self, inst: Instruction) -> None | DoJump | Terminate:
    match inst:
      case Sound(freq=reg): # Actually Send
        self.send_counter += 1
        self.send_queue.put(self.get(reg))
        # if self.id == 1:
        #   print(f'Prog {self.id} counter {self.send_counter}')
      case Set(reg=reg,val=val):
        self.regs[reg] = self.get(val)
      case Add(reg=reg,val=val):
        self.regs[reg] += self.get(val)
      case Mul(reg=reg,val=val):
        self.regs[reg] *= self.get(val)
      case Mod(reg=reg,val=val):
        self.regs[reg] %= self.get(val)
      case Recover(ifx=reg): # Actually Receive
        try:
          self.regs[reg] = self.receive_queue.get(timeout=5)
        except queue.Empty:
          return Duet2.Terminate(self.send_counter)
      case Jump(ifx=ifx, offset=offset):
        if self.get(ifx) > 0:
          return Duet2.DoJump(self.get(offset))

    return None

  def exec(self) -> Terminate:
    while 0 <= self.ptr < len(self.instructions):
      match self.exec_instruction(self.instructions[self.ptr]):
        case None:
          self.ptr += 1
        case Duet2.DoJump(offset=offset):
          self.ptr += offset
        case Duet2.Terminate(count=count):
          break

    return Duet2.Terminate(self.send_counter)

class Day18(Advent[Input]):
    day = 18

    samples = [
'''set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2''',
      '''snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      duet = Duet()
      ptr = 0

      while True:
        match duet.exec(input[ptr]):
          case Duet.RecoveredSound(freq=freq):
            return freq
          case Duet.DoJump(offset=offset):
            ptr += offset
          case None:
            ptr += 1

    def solve2(self, input: Input) -> Any:
      pool = multiprocessing.pool.ThreadPool(processes=2)
      qa = multiprocessing.Queue()
      qb = multiprocessing.Queue()

      dueta = Duet2(id=0, instructions=input, rqueue=qa, squeue=qb)
      duetb = Duet2(id=1, instructions=input, rqueue=qb, squeue=qa)


      res1 = pool.apply_async(dueta.exec, ())
      res2 = pool.apply_async(duetb.exec, ())

      res1.get()
      return res2.get()

if __name__ == '__main__':
    Day18().main()
