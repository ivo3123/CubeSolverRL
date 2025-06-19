from enum import Enum

class PieceType(Enum):
    Center = 0
    Edge = 1
    Corner = 2

class Color(Enum):
    White = 0
    Orange = 1
    Green = 2
    Red = 3
    Blue = 4
    Yellow = 5

class Face(Enum):
    U = 0
    L = 1
    F = 2
    R = 3
    B = 4
    D = 5

class Letter(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9
    K = 10
    L = 11
    M = 12
    N = 13
    O = 14
    P = 15
    Q = 16
    R = 17
    S = 18
    T = 19
    U = 20
    V = 21
    W = 22
    X = 23

class Rotation(Enum):
    Clockwise = 0
    CounterClockwise = 1
    Double = 2
