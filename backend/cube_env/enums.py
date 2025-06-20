from enum import Enum

class Phases(Enum):
    Initial = 0
    EdgesFirstLayer = 1
    CornersFirstLayer = 2
    EdgesSecondLayer = 3
    Solved = 4
