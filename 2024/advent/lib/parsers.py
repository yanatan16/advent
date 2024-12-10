from parsita import *

class UtilityParsers(ParserContext, whitespace=r'[ \t]*'):
    digit = reg(r'[0-9]') > int
    integer = reg(r'[-+]?[0-9]+') > int
    floating = reg(r'[-+]?[0-9]+\.[0-9]+') > float
    name = reg(r'[a-z]+')
    newline = lit('\n')
    char = reg(r'[a-z]')
