'Application settings'
from enum import Enum

MAX_SEQUENCE_LENGTH = 6

# Times below are in seconds

DISCARD_PRESSES_OLDER_THAN = 0.5
MIN_WAIT = 1.5
MAX_WAIT = 5
MAX_REACTION_TIME_PER_SEQUENCE_ELEMENT = 1
WAIT_RANGE = MAX_WAIT - MIN_WAIT


class GameMode(Enum):
    Single = 1
    Sequence = 2


GAME_MODE = GameMode.Sequence
