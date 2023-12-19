from typing import *
from solutions2023.lib import *

Category = Literal['x','m','a','s']
Operator = Literal['<','>']

Action = Literal['R','A'] | str

Part = Dict[Category, int]

class CatRange(NamedTuple):
  x: Tuple[int, int]
  m: Tuple[int, int]
  a: Tuple[int, int]
  s: Tuple[int, int]

  def __len__(self) -> int:
    acc = 1
    for low, high in self:
      assert low <= high
      acc *= high - low
    return acc

class Condition(NamedTuple):
  category: Category
  operator: Operator
  value: int

  def passes(self, part: Part) -> bool:
    return (self.operator == '>' and part[self.category] > self.value) or\
      (self.operator == '<' and part[self.category] < self.value)

  def __str__(self) -> str:
    return f'{self.category}{self.operator}{self.value}'

class Rule(NamedTuple):
  category: Category
  operator: Operator
  value: int
  action: Action

  def must_pass(self) -> Condition:
    return Condition(self.category, self.operator, self.value)

  def must_fail(self) -> Condition:
    if self.operator == '<':
      return Condition(self.category, '>', self.value - 1)
    else:
      return Condition(self.category, '<', self.value + 1)

class Workflow(NamedTuple):
  name: str
  rules: List[Rule | Action]

Input = Tuple[List[Workflow],List[Part]]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  name = p.reg('[a-z]+')
  category = p.reg(r'[xmas]')
  operator = p.reg(r'[<>]')
  action = p.reg(r'[RA]') | name
  value = UtilityParsers.integer
  rule = (category & operator & value & (p.lit(':') >> action)) > (lambda p: Rule(*p))
  rules = p.repsep(rule | action, ',')
  workflow = (name & (p.lit('{') >> rules << p.lit('}'))) > (lambda p: Workflow(*p))
  workflows = p.repsep(workflow, '\n')

  partcat = category & (p.lit('=') >> value)
  part = (p.lit('{') >> p.repsep(partcat, ',') << p.lit('}')) > (lambda p: {c:v for c,v in p})
  parts = p.repsep(part, '\n')

  input = workflows & (p.lit('\n\n') >> parts)

class System:
  workflows: Dict[str, Workflow]
  action_lookup: Dict[str, List[Tuple[str, int]]]

  def __init__(self, workflows: List[Workflow]):
    self.workflows = {w.name: w for w in workflows}

    actions = [
      (rule if isinstance(rule, str) else rule.action, workflow.name, rulei)
      for workflow in self.workflows.values()
      for rulei, rule in enumerate(workflow.rules)
    ]
    self.action_lookup = {
      action: [(name, rulei) for _, name, rulei in grp]
      for action, grp in itertools.groupby(sorted(actions), key=lambda trip: trip[0])
    }

  def process_workflow(self, workflow: Workflow, part: Part) -> Action:
    for rule in workflow.rules:
      if isinstance(rule, str):
        return rule

      if rule.operator == '>' and part[rule.category] > rule.value:
        return rule.action
      elif rule.operator == '<' and part[rule.category] < rule.value:
        return rule.action

    assert False, 'reached end of process_workflow. should never happen'


  def process(self, part: Part) -> bool:
    workflowset = set()

    curflow = self.workflows['in']
    while True:
      workflowset.add(curflow.name)

      match self.process_workflow(curflow, part):
        case 'R':
          return False
        case 'A':
          return True
        case flow:
          assert flow not in workflowset, 'Workflow cycle detected'
          curflow = self.workflows[flow]

  def walk_backwards(self, name: str, rulei: int) -> List[List[Condition]]:
    workflow = self.workflows[name]
    rule = workflow.rules[rulei]

    if isinstance(rule, str):
      conditions = []
    else:
      conditions = [rule.must_pass()]

    for rule in workflow.rules[:rulei]:
      assert isinstance(rule, Rule)
      conditions += [rule.must_fail()]

    if workflow.name == 'in':
      return [conditions]

    for subname, subrulei in self.action_lookup[workflow.name]:
      return [conditions + subconditions for subconditions in self.walk_backwards(subname, subrulei)]


  def accept_criteria(self) -> List[List[Condition]]:
    debug(self.action_lookup['A'])

    return [
      conditions
      for name, rulei in self.action_lookup['A']
      for conditions in self.walk_backwards(name, rulei)
    ]


def conditions_to_catrange(criteria: List[Condition]) -> CatRange | None:
  rng = dict(x=[1,4001], m=[1,4001], a=[1,4001], s=[1,4001])

  for cond in criteria:
    if cond.operator == '<':
      rng[cond.category][1] = min(rng[cond.category][1], cond.value)
    else:
      rng[cond.category][0] = max(rng[cond.category][0], cond.value + 1)

  if any(min >= max for min, max in rng.values()):
    return None

  return CatRange(x=tuple(rng['x']),
                  m=tuple(rng['m']),
                  a=tuple(rng['a']),
                  s=tuple(rng['s']))

def catrange_union(crs: List[CatRange]) -> List[CatRange]:
  crset = set(crs)

  for i in range(4):
    distinct_values = sorted({x for cr in crset for x in cr[i]})
    crset = {
      CatRange(x=(x1, x2) if i == 0 else cr.x,
               m=(x1, x2) if i == 1 else cr.m,
               a=(x1, x2) if i == 2 else cr.a,
               s=(x1, x2) if i == 3 else cr.s)
      for cr in crs
      for xs_in_range in [sorted(x for x in distinct_values if cr[i][0] <= x <= cr[i][1])]
      for x1, x2 in zip(xs_in_range, xs_in_range[1:])
    }

  return list(crset)

class Day19(Advent[Input]):
    year = 2023
    day = 19

    samples = [
'''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      workflows, parts = input
      system = System(workflows)

      return sum(
        sum(part.values())
        for part in parts
        if system.process(part)
      )

    def solve2(self, input: Input) -> Any:
      workflows, parts = input
      system = System(workflows)

      criteria = system.accept_criteria()
      ranges = [cr for cr in (conditions_to_catrange(conditions) for conditions in criteria) if cr]

      debug('Criteria\n-------')
      debug('\n'.join(', '.join(str(c) for c in crt) for crt in criteria))
      debug('Ranges\n=======')
      debug('\n'.join(str(cr) for cr in ranges))

      union_ranges = catrange_union(ranges)


      debug('Union Ranges\n=======')
      debug('\n'.join(f'{cr} ({len(cr)})' for cr in union_ranges))

      return sum(len(rng) for rng in union_ranges)

if __name__ == '__main__':
    Day19().main()
