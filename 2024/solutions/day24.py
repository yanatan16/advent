from typing import *
from advent.lib import *

class Gate(NamedTuple):
  wire1: str
  op: Literal['AND', 'XOR', 'OR']
  wire2: str
  outwire: str

  def calculate(self, w1: int, w2: int) -> int:
    if self.op == 'AND':
      return w1 & w2
    if self.op == 'OR':
      return w1 | w2
    if self.op == 'XOR':
      return w1 ^ w2

  def rename(self, renames: Dict[str, str]) -> 'Gate':
    return Gate(renames.get(self.wire1, self.wire1),
                    self.op,
                    renames.get(self.wire2, self.wire2),
                    renames.get(self.outwire, self.outwire))
  def switch(self, renames: Dict[str, str]) -> 'Gate':
    return Gate(self.wire1, self.op, self.wire2, renames.get(self.outwire, self.outwire))

  def __str__(self) -> str:
    return f'{self.wire1} {" " if self.op == "OR" else ""}{self.op} {self.wire2} -> {self.outwire}'

InitialWire = Tuple[str, int]
Input = Tuple[List[InitialWire], List[Gate]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  wire = p.reg('[a-z\d]+')
  value = p.reg('0|1') > int
  initwire = wire & (p.lit(':') >> value) > tuple
  op = p.lit('AND') | p.lit('OR') | p.lit('XOR')
  gate = (wire & op & wire) & (p.lit('->') >> wire) > (lambda g: Gate(*g))
  
  input = p.repsep(initwire, '\n') & (p.lit('\n\n') >> p.repsep(gate, '\n'))

class Day24(Advent[Input]):
    year = 2024
    day = 24

    samples = [
'''x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02''',
      '''x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      initwires, gates = input
      values = {
        wire: val
        for wire, val in initwires
      }

      uncalculated = gates

      while len(uncalculated):
        uncalc1 = []
        for gate in uncalculated:
          if gate.wire1 in values and gate.wire2 in values:
            values[gate.outwire] = gate.calculate(values[gate.wire1], values[gate.wire2])
          else:
            uncalc1 += [gate]

        uncalculated = uncalc1

      zbits = [
        (int(wire[1:]), val)
        for wire, val in values.items()
        if wire.startswith('z')
        and re.match(r'\d+',wire[1:])
      ]

      return sum(
        z * 2**i
        for i, z in sorted(zbits)
      )

    def solve2(self, input: Input) -> Any:
      initwires, gates = input

      if len(gates) < 100:
        return -1

      def bits2num(values: Dict[str, int], prefix: str) -> int:
        zbits = [
          (int(wire[len(prefix):]), val)
          for wire, val in values.items()
          if wire.startswith(prefix)
          and re.match(r'\d+',wire[len(prefix):])
        ]

        return sum(
          z * 2**i
          for i, z in sorted(zbits)
        )

      def sim(switches: List[Tuple[str, str]]) -> Tuple[int | None, Dict[str, int]]:
        values = {wire: val for wire, val in initwires}
        switch = {
          k:v
          for w1, w2 in switches
          for k,v in [(w1, w2), (w2, w1)]
        }

        uncalculated = gates

        while len(uncalculated):
          uncalc1 = []
          for gate in uncalculated:
            if gate.wire1 in values and gate.wire2 in values:
              values[switch.get(gate.outwire, gate.outwire)] = gate.calculate(values[gate.wire1], values[gate.wire2])
            else:
              uncalc1 += [gate]

          if len(uncalc1) == len(uncalculated):
            self._print(f'Infinite loop on calc: {uncalc1} {switch} {values}')
            return None, values

          uncalculated = uncalc1

        return bits2num(values, 'z'), bits2num(values, 'x'), bits2num(values, 'y')

      switches = [
        ('vvr', 'z08'),
        ('rnq', 'bkr'),
        ('tfb', 'z28'),
        ('mqh', 'z39')
      ]
      switch = {
          k:v
          for w1, w2 in switches
          for k,v in [(w1, w2), (w2, w1)]
      }
      gates = [g.switch(switch) for g in gates]

      renames = {
        'qvn': 'c00',
      }
      for gate in gates:
        if gate.wire1[0] in 'xy' and gate.wire2[0] in 'xy' and not gate.outwire.startswith('z') and gate.outwire not in renames:
          if gate.op == 'XOR':
            renames[gate.outwire] = 'v' + gate.wire1[1:]
          if gate.op == 'AND':
            renames[gate.outwire] = 'b' + gate.wire1[1:]

      for _ in range(45):
        for gate in gates:
          rg = gate.rename(renames)
          if rg.wire1[0] in 'vc' and rg.wire2[0] in 'cv' and rg.op == 'AND' and not rg.outwire.startswith('z') and rg.outwire not in renames and re.match(r'\d+', rg.wire1[1:]) and re.match(r'\d+', rg.wire2[1:]):
            n = max(int(rg.wire1[1:]), int(rg.wire2[1:]))
            renames[rg.outwire] = f'a{n:02}'

      
        for gate in gates:
          rg = gate.rename(renames)
          if rg.wire1[0] in 'ab' and rg.wire2[0] in 'ab' and rg.op == 'OR' and not rg.outwire.startswith('z') and rg.outwire not in renames:
            renames[rg.outwire] = 'c' + rg.wire2[1:]

      for i in range(45):
        pad = f'{i:02}'
        gs = [g for g in gates if pad in g.wire1 or pad in g.wire2 or pad in g.outwire]
        outwires = {g.outwire for g in gs}
        gs2 = [g for g in gates if g.wire1 in outwires or g.wire2 in outwires]
        for g in sorted(set(gs + gs2)):
          print(f'{g.rename(renames)}  ({g})')

        print('\n')


      if len(switches) == 4:
        z, x, y = sim([]) #switches)

        if x + y == z:
          return ','.join(sorted(w for ws in switches for w in ws))
        else:
          raise RuntimeError(f'{x} + {y} != {z}')






if __name__ == '__main__':
    Day24().main()


# add: x XOR y = v
# carry: x AND y = b
# 3add: c XOR (x XOR y) = c XOR v
# 3carry: ((x XOR y) AND c) OR (x AND y) = (v AND c) OR b = a OR c+1

# ((x XOR y) AND c) = v AND c = a
