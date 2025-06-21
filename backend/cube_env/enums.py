from enum import Enum

class Phases(Enum):
    Unknown = 0
    EdgesFirstLayer = 1
    CornersFirstLayer = 2
    EdgesSecondLayer = 3
    Solved = 4
