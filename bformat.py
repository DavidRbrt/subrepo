import sys

# colors
DEFAULT   = '\033[00m'
RED       = '\033[31m'
GREEN     = '\033[32m'
YELLOW    = '\033[33m'
BLUE      = '\033[34m'
PURPLE    = '\033[35m'
CYAN      = '\033[36m'
BOLD      = '\033[1m'
UNDERLINE = '\033[4m'
#
SUCCESS = GREEN + BOLD
ERROR   = RED

# symbols
CHECKMARK = '\u2713'
CROSSMARK = '\u2717'

try:
    # try to print special chars
    print(f'{CHECKMARK + CROSSMARK}',)
    # if the print was ok, go up and clear line
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
except UnicodeEncodeError as e:
    # if chars are not in the charmap, use these
    CHECKMARK = 'OK'
    CROSSMARK = 'X'

NESTEDMARK = '> '

# sequences
SUCCESSMARK = GREEN + CHECKMARK + DEFAULT
ERRORMARK = RED + CROSSMARK + DEFAULT

    