import sys

from .input import get_input
from .runner import Advent
from .parsers import UtilityParsers
from .walk import walk
from .sparse_grid import SparseGrid
from .ranges import Range
from . import twod, threed, hexd
from .utils import freqlist, freqs

from dataclasses import dataclass
from enum import Enum
import itertools, collections, functools, re, math
import parsita as p
from tqdm import tqdm

def debug(*args):
    if '-v' in sys.argv:
        print(*args)

__all__ = [
    'get_input',
    'Advent',
    'UtilityParsers',
    'SparseGrid',
    'walk',
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
    'freqs'
]
