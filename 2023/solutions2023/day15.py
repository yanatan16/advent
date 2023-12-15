from typing import *
from solutions2023.lib import *

Step = str
Input = List[Step]

class Parsers(p.ParserContext, whitespace=r'[ \t\n]*'):
  step = p.reg(r'[^,]+')
  input = p.repsep(step, ',')

@functools.cache
def hash(init: str) -> int:
  v = 0
  for c in init:
    v = ((v + ord(c)) * 17) % 256
  return v

class Lens(NamedTuple):
  label: str
  focal: int

  def __str__(self) -> str:
    return f'[{self.label} {self.focal}]'


class HASHMAP:
  boxes: List[List[Lens]]

  def __init__(self):
    self.boxes = [[] for _ in range(256)]

  def remove(self, box: int, label: str):
    self.boxes[box] = [lens for lens in self.boxes[box] if lens.label != label]

  def add(self, box: int, lens: Lens):
    for i, l in enumerate(self.boxes[box]):
      if l.label == lens.label:
        self.boxes[box][i] = lens
        return

    self.boxes[box] += [lens]

  def power(self) -> int:
    return sum(
      (box+1) * (i+1) * lens.focal
      for box in range(256)
      for i, lens in enumerate(self.boxes[box])
    )

  def __str__(self) -> str:
    return '\n'.join(
      f'Box {box}: {", ".join(str(lens) for lens in self.boxes[box])}'
      for box in range(256)
      if self.boxes[box]
    )

class Day15(Advent[Input]):
    year = 2023
    day = 15

    samples = [
'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      return sum(
        hash(step) for step in input
      )

    def solve2(self, input: Input) -> Any:
      hashmap = HASHMAP()
      for step in input:
        if step.endswith('-'):
          label = step.split('-')[0]
          box = hash(label)
          hashmap.remove(box, label)
        else:
          label, focal = step.split('=')
          box = hash(label)
          hashmap.add(box, Lens(label, int(focal)))

        debug(f'Step {step}')
        debug(hashmap)

      return hashmap.power()

if __name__ == '__main__':
    Day15().main()
