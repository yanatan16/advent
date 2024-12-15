from typing import *
from advent.lib import *

Coord = twod.Coord
Map = List[List[str]]
Movement = Literal['<','v','>','^']
Movements = List[Movement]
Input = Tuple[Map, Movements]

class Parsers(p.ParserContext, whitespace=r'[ \t]*'):
  mapposition = p.reg(r'[.#O@]')
  mapline = p.rep(mapposition, min=1)
  map = p.repsep(mapline, '\n')
  movement =  p.reg(r'\n*') >> p.reg(r'[<v>^]')
  movements = p.rep(movement)
  input = map & movements

class Day15(Advent[Input]):
    year = 2024
    day = 15

    samples = [
      '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<''',
'''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''
    ]

    def parse(self, raw: str) -> Input:
        return Parsers.input.parse(raw.strip()).unwrap()

    def solve1(self, input: Input) -> Any:
      map, movements = input
      walls = {c for c in Coord.all_coords(map) if c.get(map) == '#'}
      boxes = {c for c in Coord.all_coords(map) if c.get(map) == 'O'}
      robot = [c for c in Coord.all_coords(map) if c.get(map) == '@'][0]

      direction: Dict[Movement, twod.Direction] = {
        '<': 'left',
        'v': 'down',
        '>': 'right',
        '^': 'up'
      }

      class State(NamedTuple):
        boxes: Set[Coord]
        robot: Coord

        def step(state, m: Movement) -> 'State':
          boxes_to_move = set()
          dir = direction[m]
          key = state.robot.move(dir)

          while key in walls or key in state.boxes:
            if key in walls:
              # No movement this time
              return state
            else:
              boxes_to_move.add(key)
              key = key.move(dir)

          moved_boxes = [
            box.move(dir)
            for box in boxes_to_move
          ]

          self._print(f'moving {state.robot} to {state.robot.move(dir)} and moving boxes {boxes_to_move} to {moved_boxes}')
          return State(
            boxes=(state.boxes - boxes_to_move).union(moved_boxes),
            robot=state.robot.move(dir)
          )

        def disp(state):
          self._print('\n'.join(
            ''.join(
              '#' if Coord(x,y) in walls else (
                'O' if Coord(x,y) in state.boxes else (
                  '@' if Coord(x,y) == state.robot else '.'
                )
              )
              for y in range(len(map[0]))
            )
            for x in range(len(map))
          ))

      state = State(boxes, robot)
      state.disp()
      steps = 0

      for movement in tqdm(movements):
        steps += 1
        state = state.step(movement)

        self._print(f'After {steps} steps ({movement} : {direction[movement]})')
        state.disp()

      self._print(f'After {steps} steps')
      state.disp()

      return sum(
        box.x * 100 + box.y
        for box in state.boxes
      )



    def solve2(self, input: Input) -> Any:
        return 'Not implemented'

if __name__ == '__main__':
    Day15().main()
