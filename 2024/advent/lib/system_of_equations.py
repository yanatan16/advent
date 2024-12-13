from typing import *

def solve_soe_linear_2var(x1: float, y1: float, c1: float, x2: float, y2: float, c2: float) -> Tuple[float, float] | Tuple[None, None]:
    '''
    Solve a linear system of equations with two variables in the form:
    x1*X + y1*Y = c1
    x2*X + y2*Y = c2

    Returns tuple (X, Y) of solution
    If the system is unsolvable, return Tuple[None, None].
    If requiring an integer solution, handle that after receiving solution.
    '''

    denom = (x1 * y2) - (y1 * x2)
    if denom == 0:
        return None, None

    x = (c1 * y2 - y1 * c2) / denom
    y = (x1 * c2 - c1 * x2) / denom

    return (x, y)
