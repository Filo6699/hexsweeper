from enum import Enum


class State(Enum):
    UNCOVERED = 1
    COVERED = 2
    FLAGGED = 3


class UncoverResult(Enum):
    SUCCESS = 1
    NOTVALID = 2
    MISTAKE = 3
