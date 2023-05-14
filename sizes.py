import math

ICON_HEIGHT = 24
TECH_LEVEL_HEIGHT = 5

ICON_SIZE_BOMBER = (int(math.ceil(ICON_HEIGHT * 0.9 / 2)) * 4 - 4, int(math.ceil(ICON_HEIGHT * 0.9 / 2)) * 2)
ICON_SIZE_BOT = (int(math.ceil(ICON_HEIGHT * 1.25 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 0.8 / 2)) * 2)
ICON_SIZE_EXPERIMENTAL = (ICON_HEIGHT, ICON_HEIGHT)
ICON_SIZE_FACTORY = (int(math.ceil(ICON_HEIGHT * 1.3 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 0.8 / 2)) * 2)
ICON_SIZE_FIGHTER = (int(math.ceil(ICON_HEIGHT * 1.2 / 2)) * 2 - 2, int(math.ceil(ICON_HEIGHT * 1.2 / 2)) * 2)
ICON_SIZE_GUNSHIP = (int(math.ceil(ICON_HEIGHT * 1.3 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 0.8 / 2)) * 2)
ICON_SIZE_LAND = (int(math.ceil(ICON_HEIGHT * 1.1 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 1.1 / 2)) * 2)
ICON_SIZE_STRUCTURE = (ICON_HEIGHT, ICON_HEIGHT)
ICON_SIZE_SHIP = (int(math.ceil(ICON_HEIGHT * 1.1 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 0.75 / 2)) * 2)
ICON_SIZE_SUB = (int(math.ceil(ICON_HEIGHT * 1.1 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 0.75 / 2)) * 2)
ICON_SIZE_WALL = (ICON_HEIGHT // 2, ICON_HEIGHT // 2)

ICON_SIZE_NUKE = (int(math.ceil(ICON_HEIGHT * 1.5 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 1.5 / 2)) * 2)
ICON_SIZE_ANTINUKE = (int(math.ceil(ICON_HEIGHT * 2 / 3 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 2 / 3 / 2)) * 2)
ICON_SIZE_COMMANDER = (int(math.ceil(ICON_HEIGHT * 1.25 / 2)) * 2, int(math.ceil(ICON_HEIGHT * 1.25 / 2)) * 2)

TYPE_SIZE = max(6, int(math.ceil(ICON_HEIGHT * 3 / 4 / 2)) * 2)
