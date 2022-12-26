# Advent of Code 2022 Day 19
import sys
from typing import *
from dataclasses import dataclass
import enum
import tqdm
import math
from functools import reduce

class Robot(enum.Enum):
    ore = 'ore'
    clay = 'clay'
    obsidian = 'obsidian'
    geode = 'geode'


Costs = Dict[Robot, int]

def parse_costs(line: str) -> Costs:
    costs = line.split(' and ')
    c: Costs = {}
    for cost in costs:
        n, type = cost.split(' ')
        c[Robot(type)] = int(n)
    return c

@dataclass
class Blueprint:
    id: int
    robots: Dict[Robot, Costs]

    @staticmethod
    def parse(line: str) -> 'Blueprint':
        idstr, rest = line.split(': ')
        id = int(idstr.split(' ')[1])
        ore, clay, obsidian, geode, _ = rest.split('.')
        return Blueprint(
            id = id,
            robots={
                Robot.ore: parse_costs(ore.split('costs ')[1].strip()),
                Robot.clay: parse_costs(clay.split('costs ')[1].strip()),
                Robot.obsidian: parse_costs(obsidian.split('costs ')[1].strip()),
                Robot.geode: parse_costs(geode.split('costs ')[1].strip()),
            }
        )

@dataclass
class Input:
    blueprints: List[Blueprint]

Output = int

class PlannedBuild(NamedTuple):
    time: int
    robot: Robot

    def __str__(self) -> str:
        return f'<build: {robot.value} at {self.time}>'

Plan = List[PlannedBuild]

def is_plan_feasible(blueprint: Blueprint, plan: Plan) -> bool:
    resources:Dict[Robot, int] = {r: 0 for r in Robot}
    robots:Dict[Robot, int] = {r: 0 for r in Robot}
    robots[Robot.ore] = 1
    rest_of_plan = plan

    for time in range(1, 25):
        # print('time', time)
        # print('robots', robots)
        # print('resources', resources)

        while rest_of_plan and rest_of_plan[0].time == time:
            robot_to_build = rest_of_plan[0].robot
            # print('Build', robot_to_build)
            # print('Cost', blueprint.robots[robot_to_build])

            costs = blueprint.robots[robot_to_build]
            for type, cost in costs.items():
                if resources[type] < cost:
                    return False
                else:
                    resources[type] -= cost

            robots[robot_to_build] += 1
            rest_of_plan = rest_of_plan[1:]

        for type, count in robots.items():
            resources[type] += count

    return True

def plan_score(plan: Plan, maxtime=24) -> int:
    geode_build_times = [time for time, robot in plan if robot == Robot.geode]
    return sum(maxtime - time for time in geode_build_times)

def generate_plans(blueprint: Blueprint, plan: Plan = []) -> List[Plan]:
    #assert is_plan_feasible(blueprint, plan), f'plan is infeasible {plan}'

    end_time = max(time for time, _ in plan) if plan else 0
    #print('generate_plans at', len(plan), end_time)
    robots = {
        r: sum(1 if robot == r else 0 for _, robot in plan) +\
           (1 if r == Robot.ore else 0)
        for r in Robot
    }
    resources_now = {
        r: sum(end_time - time - 1 for time, robot in plan if robot == r) -\
           sum(blueprint.robots[robot].get(r, 0) for _, robot in plan) +\
           (end_time - 1 if r == Robot.ore else 0)
        for r in Robot
    }
    resources_end = {
        r: sum(22 - time for time, robot in plan if robot == r) -\
           sum(blueprint.robots[robot].get(r, 0) for _, robot in plan) +\
           (22 if r == Robot.ore else 0)
        for r in Robot
    }

    if (len(plan) == 0 or plan[-1].robot == Robot.ore) and sum(1 if r == Robot.ore else 0 for _, r in plan) < 3:
        limit_builds = [Robot.ore, Robot.clay]
    elif plan[-1].robot == Robot.geode:
        limit_builds = [Robot.geode]
    else:
        limit_builds = [Robot.clay, Robot.obsidian, Robot.geode]

    can_build = [
        r for r in limit_builds
        if all(resources_end[cost_type] >= cost for cost_type, cost in blueprint.robots[r].items())
    ]

    def when_can_build(robot_to_build: Robot) -> int:
        time_to_build = end_time
        resources_at_time = {r:c for r,c in resources_now.items()}
        costs = blueprint.robots[robot_to_build]

        while not all(resources_at_time[t] >= cost for t, cost in costs.items()):
            for robot, count in robots.items():
                resources_at_time[robot] += count
            time_to_build += 1

        assert time_to_build <= 23
        return time_to_build

    can_build_2 = [
        (r, when_can_build(r)) for r in can_build
    ]

    can_build_3 = [
        (r, time) for r, time in can_build_2
        if time < 23 or r == Robot.geode
    ]

    if len(can_build_3) == 0:
        yield plan

    for robot_to_build, time_to_build in can_build_3[::-1]:
        new_plan = plan + [PlannedBuild(time_to_build, robot_to_build)]
        for subplan in generate_plans(blueprint, new_plan):
            yield subplan

def optimize_blueprint_old(blueprint: Blueprint) -> int:
    #print(f'optimizing blueprint {blueprint.id}')
    best = (0, [], 0)
    count = 0
    for plan in generate_plans(blueprint):
        count += 1
        if count - best[2] > 100000:
            return best[0]
        if plan_score(plan) > best[0]:
            best = plan_score(plan), plan, count
            #print(f'new best: {best[0]} {best[1]}')

    return best[0]

def parse_input(raw: str) -> Input:
    return Input(
        blueprints=[
            Blueprint.parse(line) for line in raw.splitlines()
        ]
    )

class State:
    bluprint: Blueprint
    plan: Plan
    max_time: int

    current_time: int
    robots: Dict[Robot, int]
    resources: Dict[Robot, int]
    max_robots: Dict[Robot, int]

    def __init__(self, blueprint: Blueprint, plan: Plan = [], maxtime=24):
        self.blueprint = blueprint
        self.plan = plan
        self.max_time = maxtime

        self.current_time = max(time for time, _  in plan) if plan else 0

        self.robots = {
            r: sum(1 if robot == r else 0 for _, robot in plan) +\
               (1 if r == Robot.ore else 0)
            for r in Robot
        }

        self.resources = {
            r: sum(self.current_time - time - 1 for time, robot in plan if robot == r) -\
               sum(self.blueprint.robots[robot].get(r, 0) for _, robot in plan) +\
               (self.current_time - 1 if r == Robot.ore else 0)
            for r in Robot
        }

        self.max_robots = {
            r: max(cost.get(r,0) for cost in self.blueprint.robots.values())
            if r != Robot.geode else 100
            for r in Robot
        }

    def time_to_build(self, robot_type: Robot) -> int:
        costs = self.blueprint.robots[robot_type]
        max_ttb = 1
        for cost_type, cost_amt in costs.items():
            if self.robots.get(cost_type, 0) == 0:
                return -1
            else:
                needed_resources = cost_amt - self.resources.get(cost_type, 0)
                if needed_resources > 0:
                    ttb = int(math.ceil(needed_resources / self.robots[cost_type]))
                    if ttb > max_ttb:
                        max_ttb = ttb
        return max_ttb

    @property
    def robot_ttb(self) -> Dict[Robot, int]:
        interim = {r: self.time_to_build(r) for r in Robot}
        return {
            r: ttb
            for r, ttb in interim.items()
            if ttb >= 0
            and ttb + self.current_time <= self.max_time - 1
            and self.robots.get(r,0) + 1 <= self.max_robots[r]
        }

    @property
    def possible_future_plans(self) -> List[Plan]:
        return [
            self.plan + [(self.current_time + ttb, r)]
            for r, ttb in self.robot_ttb.items()
        ]

    @property
    def possible_future_states(self) -> List['State']:
        return [
            State(self.blueprint, plan, maxtime=self.max_time)
            for plan in self.possible_future_plans
        ]

    @property
    def score(self) -> int:
        return plan_score(self.plan, maxtime=self.max_time)


## Try #2
def optimize_blueprint(blueprint: Blueprint, plan: Plan = [], maxtime=24) -> int:
    # Current State
    state = State(blueprint, plan, maxtime=maxtime)

    optimized_outcomes = [
        optimize_blueprint(blueprint, future_plan, maxtime=maxtime)
        for future_plan in state.possible_future_plans
    ]

    if len(optimized_outcomes) == 0:
        return state.score
    else:
        return max(optimized_outcomes)


def part1(input: Input) -> Output:
    return sum(blueprint.id * optimize_blueprint(blueprint) for blueprint in tqdm.tqdm(input.blueprints))

def product(l: List[int]) -> int:
    return reduce(lambda a,b: a*b, l, 1)

def part2(input: Input) -> Output:
    optimal = [optimize_blueprint(blueprint, maxtime=32)
               for blueprint in tqdm.tqdm(input.blueprints[:3])]
    print(optimal)
    return product(optimal)

def main(input_file, skip=None):
    with open(input_file) as f:
        input = parse_input(f.read().strip())

    if skip != 'skip':
        print('Part 1:', part1(input))
    else:
        print('Skipping Part 1')
    print('Part 2:', part2(input))

if __name__ == '__main__':
    main(*sys.argv[1:])
 
