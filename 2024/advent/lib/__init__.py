import sys

from .input import get_input
from .runner import Advent
from .parsers import UtilityParsers
from .walk import walk_bfs, walk_dfs
from .sparse_grid import SparseGrid
from .ranges import Range
from . import twod, threed, hexd
from .utils import freqlist, freqs, product
from .priorityqueue import PriorityQueue
from .system_of_equations import solve_soe_linear_2var
from .djikstras import djikstras, djikstras_paths

from dataclasses import dataclass
from enum import Enum
import itertools, collections, functools, re, math
import parsita as p
from tqdm import tqdm
import numpy as np
import scipy, sympy, networkx as nx

def debug(*args):
    if '-v' in sys.argv:
        print(*args)

__all__ = [
    'get_input',
    'Advent',
    'UtilityParsers',
    'SparseGrid',
    'walk_bfs',
    'walk_dfs',
    'twod',
    'threed',
    'hexd',
    'dataclass',
    'Enum',
    'itertools',
    'collections',
    'functools',
    'p',
    'tqdm',
    're',
    'Range',
    'debug',
    'math',
    'freqlist',
    'freqs',
    'PriorityQueue',
    'np',
    'scipy',
    'sympy',
    'nx',
    'solve_soe_linear_2var',
    'product',
    'djikstras',
    'djikstras_paths',
]
