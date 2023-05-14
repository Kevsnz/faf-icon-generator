from enum import Enum
from collections import namedtuple

from colors import COLOR_WHITE, COLOR_BLACK, COLOR_FACTION

ModeType = namedtuple('ModeType', ['thick', 'outline', 'type'])


class IconMode(Enum):  # is thick, outline color, type color
    Rest = ModeType(False, COLOR_BLACK, COLOR_BLACK)
    Over = ModeType(False, COLOR_FACTION, COLOR_WHITE)
    Selected = ModeType(True, COLOR_WHITE, COLOR_BLACK)
    SelectedOver = ModeType(True, COLOR_FACTION, COLOR_WHITE)
