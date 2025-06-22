from cube.enums import Face, Rotation

d_action_turn = {
    0: (Face.U, Rotation.Clockwise),
    1: (Face.U, Rotation.CounterClockwise),
    2: (Face.U, Rotation.Double),
    3: (Face.L, Rotation.Clockwise),
    4: (Face.L, Rotation.CounterClockwise),
    5: (Face.L, Rotation.Double),
    6: (Face.F, Rotation.Clockwise),
    7: (Face.F, Rotation.CounterClockwise),
    8: (Face.F, Rotation.Double),
    9: (Face.R, Rotation.Clockwise),
    10: (Face.R, Rotation.CounterClockwise),
    11: (Face.R, Rotation.Double),
    12: (Face.B, Rotation.Clockwise),
    13: (Face.B, Rotation.CounterClockwise),
    14: (Face.B, Rotation.Double),
    15: (Face.D, Rotation.Clockwise),
    16: (Face.D, Rotation.CounterClockwise),
    17: (Face.D, Rotation.Double),
}