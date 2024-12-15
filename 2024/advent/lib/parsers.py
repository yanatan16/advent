from parsita import *

from .twod import Coord

class UtilityParsers(ParserContext, whitespace=r'[ \t]*'):
    digit = reg(r'[0-9]') > int
    integer = reg(r'[-+]?[0-9]+') > int
    floating = reg(r'[-+]?[0-9]+\.[0-9]+') > float
    name = reg(r'[a-z]+')
    newline = lit('\n')
    char = reg(r'[a-z]')

    twod_coord = repsep(integer, ',', min=2, max=2) > (lambda ns: Coord(*ns))
