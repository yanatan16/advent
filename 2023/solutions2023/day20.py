from typing import *
from solutions2023.lib import *

class Pulse(Enum):
  low = 1
  high = 2

ModuleType = Literal['%', '&', '']
class Module(NamedTuple):
  modtype: ModuleType
  name: str
  outputs: List[str]

Input = List[Module]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  modtype = p.reg(r'[%&]?')
  name = p.reg(r'[a-z]+')
  module = (modtype & name & (p.lit('->') >> p.repsep(name, ','))) > (lambda p: Module(*p))
  input = p.repsep(module, '\n')

class PulseSystem:
  modules: Dict[str, Module]
  conjunctions: Dict[str, Dict[str, Pulse]]
  flipflops: Dict[str, bool]
  counts: Dict[Pulse, int]

  def __init__(self, modules: List[Module]):
    self.modules = {m.name: m for m in modules}
    self.conjunctions = {
      m.name: {
        n.name: Pulse.low
        for n in modules
        if m.name in n.outputs
      }
      for m in modules
      if m.modtype == '&'
    }
    self.counts = {
      Pulse.low: 0,
      Pulse.high: 0
    }
    self.flipflops = {m.name: False for m in modules if m.modtype == '%'}
    self.pushes = 0
    self.important = [mod.name for mod in modules if 'rx' in mod.outputs][0]
    self.important_periods = {
      n: None
      for n in self.conjunctions[self.important].keys()
    }

  def push_button(self):
    self.pushes += 1
    pulses: List[Tuple[str, List[str], Pulse]] = [('button', ['broadcaster'], Pulse.low)]

    while len(pulses) > 0:
      frommod, tomods, pulsetype = pulses.pop(0)
      self.counts[pulsetype] += len(tomods)

      for tomod in tomods:
        if tomod not in self.modules:
          continue

        if tomod == self.important and pulsetype == Pulse.high and self.important_periods[frommod] is None:
          print(f'Found period for important module {frommod} to be {self.pushes}')
          self.important_periods[frommod] = self.pushes

        module = self.modules[tomod]

        match tomod, module.modtype, pulsetype:
          case 'broadcaster', _, _:
            pulses.append((module.name, module.outputs, pulsetype))

          case _, '%', Pulse.low:
            if self.flipflops[module.name]:
              self.flipflops[module.name] = False
              pulses.append((module.name, module.outputs, Pulse.low))
            else:
              self.flipflops[module.name] = True
              pulses.append((module.name, module.outputs, Pulse.high))

          case _, '&', _:
            self.conjunctions[module.name][frommod] = pulsetype
            if {Pulse.high} == set(self.conjunctions[module.name].values()):
              pulses.append((module.name, module.outputs, Pulse.low))
            else:
              pulses.append((module.name, module.outputs, Pulse.high))

          case _, '%', Pulse.high:
            pass
          case _, _, _:
            raise Exception('wtf')



def diffs(vx: List[int]) -> List[int]:
  return [y-x for x,y in zip(vx, vx[1:])]

class Day20(Advent[Input]):
    year = 2023
    day = 20

    samples = [
'''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a''',
      '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      system = PulseSystem(input)
      for _ in range(1000):
        system.push_button()

      return system.counts[Pulse.high] * system.counts[Pulse.low]

    def solve2(self, input: Input) -> Any:
      if not any('rx' in m.outputs for m in input):
        return -1

      system = PulseSystem(input)
      system.push_button()


      while system.pushes < 10000 and not all(period is not None for period in system.important_periods.values()):
        system.push_button()

      if not all(period is not None for period in system.important_periods.values()):
        print('Failed to find periods')
      else:
        return math.lcm(*system.important_periods.values())


if __name__ == '__main__':
  Day20().main()
