from typing import *
from advent.lib import *

Coord = twod.Coord
Map = List[List[str]]
Movement = twod.Arrow
Movements = List[twod.Arrow]
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
      map, movements = input

      newmap = [
        [
          '#' if Coord(i,j).get(map) == '#' else (
            '[]'[w] if Coord(i,j).get(map) == 'O' else (
              '@' if Coord(i,j).get(map) == '@' and w == 0 else '.'
            )
          )
          for j in range(len(map[0]))
          for w in range(2)
        ]
        for i in range(len(map))
      ]

      mapfreqs = Coord.freqlist(newmap)
      robot = mapfreqs['@'][0]
      walls = mapfreqs['#']

      class State(NamedTuple):
        boxes_left: Set[Coord]
        boxes_right: Set[Coord]
        robot: Coord

        def step(state, m: twod.Arrow) -> 'State':
          boxes_to_move = set()
          dir = twod.arrows[m]
          keys = {state.robot.move(dir)}
          can_move = False

          while not can_move:
            newkeys = set()
            for key in keys:
              if key in walls:
                # No movement this time
                return state
              elif key in state.boxes_left:
                boxes_to_move.add(key)
                boxes_to_move.add(key.move('right'))
                if m == '>':
                  newkeys.add(key.move('right').move('right'))
                else:
                  newkeys.add(key.move(dir))
                  newkeys.add(key.move('right').move(dir))
              elif key in state.boxes_right:
                boxes_to_move.add(key)
                boxes_to_move.add(key.move('left'))
                if m == '<':
                  newkeys.add(key.move('left', 2))
                else:
                  newkeys.add(key.move(dir))
                  newkeys.add(key.move('left').move(dir))
              else:
                newkeys.add(key)

            # if no key changes were detected, we move
            if newkeys == keys:
              can_move = True
            else:
              keys = newkeys

          moved_boxes_left = [
            box.move(dir)
            for box in boxes_to_move
            if box in state.boxes_left
          ]
          moved_boxes_right = [
            box.move(dir)
            for box in boxes_to_move
            if box in state.boxes_right
          ]

          self._print(f'moving {state.robot} to {state.robot.move(dir)} and moving boxes {boxes_to_move} to {moved_boxes_left} and {moved_boxes_right}')
          return State(
            boxes_left=(state.boxes_left - boxes_to_move).union(moved_boxes_left),
            boxes_right=(state.boxes_right - boxes_to_move).union(moved_boxes_right),
            robot=state.robot.move(dir)
          )

        def disp(state):
          if self._verbose:
            self._print('\n'.join(
              ''.join(
                '#' if Coord(x,y) in walls else (
                  '[' if Coord(x,y) in state.boxes_left else (
                    ']' if Coord(x,y) in state.boxes_right else (
                      '@' if Coord(x,y) == state.robot else '.'
                    )
                  )
                )
                for y in range(len(newmap[0]))
              )
              for x in range(len(newmap))
            ))

      state = State(set(mapfreqs['[']), set(mapfreqs[']']), robot)
      state.disp()
      steps = 0

      for movement in tqdm(movements):
        steps += 1
        state = state.step(movement)

        self._print(f'After {steps} steps ({movement} : {twod.arrows[movement]})')
        state.disp()

      self._print(f'After {steps} steps')
      state.disp()

      return sum(
        box.x * 100 + box.y
        for box in state.boxes_left
      )

if __name__ == '__main__':
    Day15().main()
