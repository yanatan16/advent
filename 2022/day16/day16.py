# Advent of Code 2022 Day 16
import sys
from typing import *
from dataclasses import dataclass
import enum
import tqdm
from itertools import groupby, permutations, chain

@dataclass
class Valve:
    name: str
    rate: int
    tunnels: List[str]

    @staticmethod
    def parse(line: str) -> 'Valve':
        _, name, _, _, ratestr, _, _, _, _, *tunnelstr = line.split(' ')
        return Valve(
            name=name,
            rate=int(ratestr[5:-1]),
            tunnels=[t.split(',')[0] for t in tunnelstr]
        )

@dataclass
class Input:
    valves: List[Valve]

Output = int

def parse_input(raw: str) -> Input:
    return Input(
        valves=[
            Valve.parse(line) for line in raw.splitlines()
        ]
    )

class ValveState:
    valves: Dict[str, Valve]
    open: Set[str] = set()
    total_flow: int = 0
    time_left: int = 30
    location: str = 'AA'

    def iterate(self, open: Optional[str] = None, move: Optional[str] = None) -> 'ValveState':
        new_open = self.open.union({open}) if open else self.open
        new_flow = ((self.time_left - 1) * self.valves[open].rate) if open else 0
        return ValveState(
            valves=self.valves,
            open=new_open,
            total_flow=self.total_flow + new_flow,
            time_left=self.time_left - 1,
            location=move or self.location
        )

    def __init__(self, valves, open, total_flow, time_left, location):
        self.valves = valves
        self.open = open
        self.total_flow = total_flow
        self.time_left = time_left
        self.location = location

    @staticmethod
    def from_input(input: Input):
        return ValveState(
            valves={v.name: v for v in input.valves},
            open=set(),
            total_flow=0,
            time_left=30,
            location='AA'
        )

    @property
    def current_valve(self) -> Valve:
        return self.valves[self.location]

    def is_open(self, valve: str) -> bool:
        return valve in self.open

    def escape1(self: 'ValveState') -> List['ValveState']:
        options: List[ValveState] = []

        if not self.is_open(self.location) and self.current_valve.rate > 0:
            # evaluate opening current valve
            options += [self.iterate(open=self.location)]


        for tunnel in self.current_valve.tunnels:
            # evaluate going to that tunnel
            options += [self.iterate(move=tunnel)]

        return options

    def key(self) -> str:
        return f'{self.location}:' + ''.join('o' if self.is_open(v) else '.' for v in self.valves)

    @staticmethod
    def merge(states: List['ValveState']) -> List['ValveState']:
        best = {}
        for state in states:
            key = state.key()
            if key not in best or state.total_flow > best[key].total_flow:
                best[key] = state

        return list(best.values())


def part1(input: Input) -> Output:
    return -1
    states = [ValveState.from_input(input)]
    for i in tqdm.tqdm(range(30)):
        print(f'Running iteration {i+1} with {len(states)} states')
        #print(list(sorted([state.key() for state in states])))
        states = ValveState.merge([s for state in states for s in state.escape1()])

    return max(state.total_flow for state in states)

@dataclass
class Action:
    open: Optional[str] = None
    move: Optional[str] = None

class ValveState2(ValveState):
    location: Tuple[str, str] = ('AA', 'AA')

    def iterate(self, me: Action, elephant: Action) -> 'ValveState2':
        opening = [v for v in [me.open, elephant.open] if v]
        new_open = self.open.union(opening)
        new_flow = sum(((self.time_left - 1) * self.valves[o].rate) for o in opening)
        return ValveState2(
            valves=self.valves,
            open=new_open,
            total_flow=self.total_flow + new_flow,
            time_left=self.time_left - 1,
            location=(me.move if me.move else self.location[0],
                      elephant.move if elephant.move else self.location[1])
        )

    @staticmethod
    def from_input(input: Input):
        return ValveState2(
            valves={v.name: v for v in input.valves},
            open=set(),
            total_flow=0,
            time_left=26,
            location=('AA', 'AA')
        )

    @property
    def my_current_valve(self):
        return self.valves[self.my_location]

    @property
    def elephant_current_valve(self):
        return self.valves[self.elephant_location]

    @property
    def my_location(self):
        return self.location[0]
    @property
    def elephant_location(self):
        return self.location[1]

    def escape2(self: 'ValveState') -> List['ValveState']:
        my_actions: List[Action] = []
        elephant_actions: List[Action] = []

        if not self.is_open(self.my_location) and self.my_current_valve.rate > 0:
            my_actions += [Action(open=self.my_location)]
        for tunnel in self.my_current_valve.tunnels:
            my_actions += [Action(move=tunnel)]

        if not self.is_open(self.elephant_location) and self.elephant_current_valve.rate > 0:
            elephant_actions += [Action(open=self.elephant_location)]
        for tunnel in self.elephant_current_valve.tunnels:
            elephant_actions += [Action(move=tunnel)]

        options = [
            self.iterate(me=me, elephant=elephant)
            for me in my_actions
            for elephant in elephant_actions
            if not (me.open and me.open == elephant.open)
        ]

        return options

    def key(self) -> str:
        sorted_location = list(sorted(self.location))
        return f'{sorted_location}:' + ''.join('o' if self.is_open(v) else '.' for v in self.valves)


# optimal planning
# me: [JJ, BB, CC]
# el: [DD, HH, EE]

def shortest_paths_from(start: Valve, valves: List[Valve]) -> Dict[Tuple[str, str], int]:
    paths = {(start.name, to.name): 1000 for to in valves}
    vd = {v.name: v for v in valves}

    dist = 0
    nodes = [start]
    while any(d == 1000 for d in paths.values()) and len(nodes):
        # print('nodes', nodes)
        # print('dist', dist)
        # print('paths', paths)
        new_nodes = []
        for node in nodes:
            if paths[(start.name, node.name)] > dist:
                paths[(start.name, node.name)] = dist
                new_nodes += [vd[t] for t in node.tunnels]

        nodes = new_nodes
        dist += 1
    return paths

def shortest_paths(valves: List[Valve]) -> Dict[Tuple[str, str], int]:
    out = {}
    for fro in valves:
        out.update(shortest_paths_from(fro, valves))
    return out

def part2(input: Input) -> Output:
    distances = shortest_paths(input.valves)
    lookup = {v.name: v for v in input.valves}
    total_time = 26

    def plan_time(plan: List[str]) -> int:
        return sum(distances[pair] + 1 for pair in zip(plan, plan[1:]))

    def is_plan_feasible(plan: List[str]) -> bool:
        return plan_time(plan) < total_time

    def plan_score(plan: List[str]) -> int:
        sum = 0
        time = 26
        last_valve = plan[0]
        for valve in plan[1:]:
            time -= distances[(last_valve, valve)] + 1
            #print(f'Travel from {last_valve} to {valve} in {distances[(last_valve, valve)]} and open with rate {lookup[valve].rate} and at time {26-time} for score {time * lookup[valve].rate}')
            sum += time * lookup[valve].rate
            last_valve = valve
        return sum

    pressurized_valves = [v.name for v in input.valves if v.rate > 0]

    def single_plans(pvalves: List[Valve]):
        for length in range(1, len(pvalves) + 1):
            for plan in permutations(pvalves, length):
                p = ['AA'] + list(plan)
                if is_plan_feasible(p):
                    yield p

    def second_plan(plan: List[str]):
        pset = set(plan)
        return single_plans([v for v in pressurized_valves if v not in pset])

    def all_plans():
        for plan1 in single_plans(pressurized_valves):
            for plan2 in second_plan(plan1):
                yield (plan1, plan2)

    pressurized_distances = {
        k:v for k,v in distances.items()
        if (k[0] == 'AA' or k[0] in pressurized_valves)
        and (k[1] == 'AA' or k[1] in pressurized_valves)
        and k[0] != k[1]
    }

    Plan = List[str]
    Plans = Tuple[Plan, Plan]
    starting_plan = (['AA'], ['AA'])

    def plans_score(plans: Plans):
        return plan_score(plans[0]) + plan_score(plans[1])

    def pick_greedy_solution_plan(plan: Plan, valves: Set[str]) -> Plan:
        time_left = total_time - plan_time(plan)
        valve_scores = [
            (lookup[valve].rate * (time_left - 1 - pressurized_distances[(plan[-1], valve)]),
             valve)
            for valve in valves
            if (time_left - 1 - pressurized_distances[(plan[-1], valve)]) > 0
        ]

        if valve_scores:
            pick_valve = max(valve_scores)[1]
            return plan + [pick_valve]
        else:
            return None


    def pick_greedy_solution(plans: Plans) -> (Plans, bool):
        me_time, el_time = [plan_time(plan) for plan in plans]
        available_valves = set(pressurized_valves).difference(plans[0] + plans[1])

        if me_time <= el_time:
            # pick for me
            new_me_plan = pick_greedy_solution_plan(plans[0], available_valves)
            if new_me_plan:
                return (new_me_plan, plans[1]), True
            else:
                new_el_plan = pick_greedy_solution_plan(plans[1], available_valves)
                if new_el_plan:
                    return (plans[0], new_el_plan), True
                else:
                    return plans, False
        else:
            new_el_plan = pick_greedy_solution_plan(plans[1], available_valves)
            if new_el_plan:
                return (plans[0], new_el_plan), True
            else:
                new_me_plan = pick_greedy_solution_plan(plans[0], available_valves)
                if new_me_plan:
                    return (new_me_plan, plans[1]), True
                else:
                    return plans, False

    def is_plan_complete(plan: Plan, available_valves: Set[str]) -> bool:
        time_left = total_time - plan_time(plan)
        return all((time_left - 1 - pressurized_distances[(plan[-1], valve)]) <= 0
                   for valve in available_valves)

    def is_plans_complete(plans: Plans) -> bool:
        available_valves = set(pressurized_valves).difference(plans[0] + plans[1])
    
        return len(available_valves) == 0 or all(is_plan_complete(plan, available_valves) for plan in plans)

    def all_next_plan(plan: Plan, available_valves: List[str]) -> List[Plan]:
        time_left = total_time - plan_time(plan)
        valves_left = [
            valve
            for valve in available_valves
            if (time_left - 1 - pressurized_distances[(plan[-1], valve)]) > 0
        ]
        valves_left.sort(key=lambda valve: -(lookup[valve].rate * (time_left - 1 - pressurized_distances[(plan[-1], valve)])))
        return (plan + [valve] for valve in valves_left)

    def all_next_plans(plans: Plans = (['AA'], ['AA'])):
        if plans[0] == plans[1]:
            # first round, just pick for me
            return ((p1, plans[1]) for p1 in all_next_plan(plans[0], pressurized_valves))
        else:
            available_valves = set(pressurized_valves).difference(plans[0] + plans[1])
            times = [plan_time(plan) for plan in plans]

            if times[0] < times[1] and not is_plan_complete(plans[0], available_valves):
                return ((p1, plans[1]) for p1 in all_next_plan(plans[0], available_valves))
            else:
                return ((plans[0], p2) for p2 in all_next_plan(plans[1], available_valves))

    def plans_generator(plans: Plans = (['AA'], ['AA'])):
        # import ipdb; ipdb.set_trace()
        if is_plans_complete(plans):
            yield plans
        else:
            for subplans in all_next_plans(plans):
                for subsubplans in plans_generator(subplans):
                    yield subsubplans

    # GREED
    # plans = starting_plan
    # while True:
    #     plans, keep_going = pick_greedy_solution(plans)
    #     if not keep_going:
    #         print('Final', plans)
    #         return sum(plan_score(plan) for plan in plans)

    best_plans = None
    best_score = 0

    for plans in tqdm.tqdm(plans_generator()):
        if plans_score(plans) > best_score:
            best_plans = plans
            best_score = plans_score(plans)
            print('new best', best_plans, best_score)
    return best_score

def main(input_file):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    print('Part 1:', part1(input))
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(sys.argv[1])
