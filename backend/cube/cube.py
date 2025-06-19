from cube.enums import Color, Face, Letter, PieceType, Rotation

cube = dict[tuple[Letter, PieceType], Color]

def get_solved_cube() -> cube:
    d_cube = {
        **{
            (letter, piece_type): Color.White
            for letter in [Letter.A, Letter.B, Letter.C, Letter.D]
            for piece_type in [PieceType.Edge, PieceType.Corner]
        },
        **{
            (letter, piece_type): Color.Orange
            for letter in [Letter.E, Letter.F, Letter.G, Letter.H]
            for piece_type in [PieceType.Edge, PieceType.Corner]
        },
        **{
            (letter, piece_type): Color.Green
            for letter in [Letter.I, Letter.J, Letter.K, Letter.L]
            for piece_type in [PieceType.Edge, PieceType.Corner]
        },
        **{
            (letter, piece_type): Color.Red
            for letter in [Letter.M, Letter.N, Letter.O, Letter.P]
            for piece_type in [PieceType.Edge, PieceType.Corner]
        },
        **{
            (letter, piece_type): Color.Blue
            for letter in [Letter.Q, Letter.R, Letter.S, Letter.T]
            for piece_type in [PieceType.Edge, PieceType.Corner]
        },
        **{
            (letter, piece_type): Color.Yellow
            for letter in [Letter.U, Letter.V, Letter.W, Letter.X]
            for piece_type in [PieceType.Edge, PieceType.Corner]
        },
        (Face.U, PieceType.Center): Color.White,
        (Face.B, PieceType.Center): Color.Blue,
        (Face.R, PieceType.Center): Color.Red,
        (Face.D, PieceType.Center): Color.Yellow,
        (Face.F, PieceType.Center): Color.Green,
        (Face.L, PieceType.Center): Color.Orange,
    }

    return d_cube

def _move(
    d_cube: cube,
    turn: tuple[Face, Rotation]
) -> dict[tuple[Letter, PieceType], Color]:
    d_cube_res = d_cube.copy()

    def make_single_turn(
        val1: tuple[Letter, PieceType],
        val2: tuple[Letter, PieceType],
        val3: tuple[Letter, PieceType],
        val4: tuple[Letter, PieceType]
    ) -> None:
        old_val1 = d_cube_res.get(val1)
        old_val2 = d_cube_res.get(val2)
        old_val3 = d_cube_res.get(val3)
        old_val4 = d_cube_res.get(val4)

        d_cube_res[val1] = old_val2
        d_cube_res[val2] = old_val3
        d_cube_res[val3] = old_val4
        d_cube_res[val4] = old_val1

    if turn == (Face.R, Rotation.Clockwise):
        make_single_turn(
            (Letter.B, PieceType.Corner),
            (Letter.J, PieceType.Corner),
            (Letter.V, PieceType.Corner),
            (Letter.T, PieceType.Corner),
        )
        make_single_turn(
            (Letter.C, PieceType.Corner),
            (Letter.K, PieceType.Corner),
            (Letter.W, PieceType.Corner),
            (Letter.Q, PieceType.Corner),
        )
        make_single_turn(
            (Letter.B, PieceType.Edge),
            (Letter.J, PieceType.Edge),
            (Letter.V, PieceType.Edge),
            (Letter.T, PieceType.Edge),
        )
        make_single_turn(
            (Letter.M, PieceType.Edge),
            (Letter.P, PieceType.Edge),
            (Letter.O, PieceType.Edge),
            (Letter.N, PieceType.Edge),
        )
        make_single_turn(
            (Letter.M, PieceType.Corner),
            (Letter.P, PieceType.Corner),
            (Letter.O, PieceType.Corner),
            (Letter.N, PieceType.Corner),
        )
    elif turn == (Face.U, Rotation.Clockwise):
        make_single_turn(
            (Letter.J, PieceType.Corner),
            (Letter.N, PieceType.Corner),
            (Letter.R, PieceType.Corner),
            (Letter.F, PieceType.Corner),
        )
        make_single_turn(
            (Letter.I, PieceType.Corner),
            (Letter.M, PieceType.Corner),
            (Letter.Q, PieceType.Corner),
            (Letter.E, PieceType.Corner),
        )
        make_single_turn(
            (Letter.I, PieceType.Edge),
            (Letter.M, PieceType.Edge),
            (Letter.Q, PieceType.Edge),
            (Letter.E, PieceType.Edge),
        )
        make_single_turn(
            (Letter.D, PieceType.Edge),
            (Letter.C, PieceType.Edge),
            (Letter.B, PieceType.Edge),
            (Letter.A, PieceType.Edge),
        )
        make_single_turn(
            (Letter.D, PieceType.Corner),
            (Letter.C, PieceType.Corner),
            (Letter.B, PieceType.Corner),
            (Letter.A, PieceType.Corner),
        )
    elif turn == (Face.L, Rotation.Clockwise):
        make_single_turn(
            (Letter.A, PieceType.Corner),
            (Letter.S, PieceType.Corner),
            (Letter.U, PieceType.Corner),
            (Letter.I, PieceType.Corner),
        )
        make_single_turn(
            (Letter.D, PieceType.Corner),
            (Letter.R, PieceType.Corner),
            (Letter.X, PieceType.Corner),
            (Letter.L, PieceType.Corner),
        )
        make_single_turn(
            (Letter.D, PieceType.Edge),
            (Letter.R, PieceType.Edge),
            (Letter.X, PieceType.Edge),
            (Letter.L, PieceType.Edge),
        )
        make_single_turn(
            (Letter.F, PieceType.Edge),
            (Letter.E, PieceType.Edge),
            (Letter.H, PieceType.Edge),
            (Letter.G, PieceType.Edge),
        )
        make_single_turn(
            (Letter.E, PieceType.Corner),
            (Letter.H, PieceType.Corner),
            (Letter.G, PieceType.Corner),
            (Letter.F, PieceType.Corner),
        )
    elif turn == (Face.D, Rotation.Clockwise):
        make_single_turn(
            (Letter.K, PieceType.Corner),
            (Letter.G, PieceType.Corner),
            (Letter.S, PieceType.Corner),
            (Letter.O, PieceType.Corner),
        )
        make_single_turn(
            (Letter.L, PieceType.Corner),
            (Letter.H, PieceType.Corner),
            (Letter.T, PieceType.Corner),
            (Letter.P, PieceType.Corner),
        )
        make_single_turn(
            (Letter.K, PieceType.Edge),
            (Letter.G, PieceType.Edge),
            (Letter.S, PieceType.Edge),
            (Letter.O, PieceType.Edge),
        )
        make_single_turn(
            (Letter.V, PieceType.Edge),
            (Letter.U, PieceType.Edge),
            (Letter.X, PieceType.Edge),
            (Letter.W, PieceType.Edge),
        )
        make_single_turn(
            (Letter.U, PieceType.Corner),
            (Letter.X, PieceType.Corner),
            (Letter.W, PieceType.Corner),
            (Letter.V, PieceType.Corner),
        )
    elif turn == (Face.F, Rotation.Clockwise):
        make_single_turn(
            (Letter.M, PieceType.Corner),
            (Letter.D, PieceType.Corner),
            (Letter.G, PieceType.Corner),
            (Letter.V, PieceType.Corner),
        )
        make_single_turn(
            (Letter.P, PieceType.Corner),
            (Letter.C, PieceType.Corner),
            (Letter.F, PieceType.Corner),
            (Letter.U, PieceType.Corner),
        )
        make_single_turn(
            (Letter.P, PieceType.Edge),
            (Letter.C, PieceType.Edge),
            (Letter.F, PieceType.Edge),
            (Letter.U, PieceType.Edge),
        )
        make_single_turn(
            (Letter.J, PieceType.Edge),
            (Letter.I, PieceType.Edge),
            (Letter.L, PieceType.Edge),
            (Letter.K, PieceType.Edge),
        )
        make_single_turn(
            (Letter.J, PieceType.Corner),
            (Letter.I, PieceType.Corner),
            (Letter.L, PieceType.Corner),
            (Letter.K, PieceType.Corner),
        )
    elif turn == (Face.B, Rotation.Clockwise):
        make_single_turn(
            (Letter.A, PieceType.Corner),
            (Letter.N, PieceType.Corner),
            (Letter.W, PieceType.Corner),
            (Letter.H, PieceType.Corner),
        )
        make_single_turn(
            (Letter.B, PieceType.Corner),
            (Letter.O, PieceType.Corner),
            (Letter.X, PieceType.Corner),
            (Letter.E, PieceType.Corner),
        )
        make_single_turn(
            (Letter.A, PieceType.Edge),
            (Letter.N, PieceType.Edge),
            (Letter.W, PieceType.Edge),
            (Letter.H, PieceType.Edge),
        )
        make_single_turn(
            (Letter.Q, PieceType.Edge),
            (Letter.T, PieceType.Edge),
            (Letter.S, PieceType.Edge),
            (Letter.R, PieceType.Edge),
        )
        make_single_turn(
            (Letter.Q, PieceType.Corner),
            (Letter.T, PieceType.Corner),
            (Letter.S, PieceType.Corner),
            (Letter.R, PieceType.Corner),
        )
    elif turn[1] == Rotation.Double:
        d_cube_res = _move(d_cube=d_cube_res, turn=(turn[0], Rotation.Clockwise))
        d_cube_res = _move(d_cube=d_cube_res, turn=(turn[0], Rotation.Clockwise))
    elif turn[1] == Rotation.CounterClockwise:
        d_cube_res = _move(d_cube=d_cube_res, turn=(turn[0], Rotation.Clockwise))
        d_cube_res = _move(d_cube=d_cube_res, turn=(turn[0], Rotation.Clockwise))
        d_cube_res = _move(d_cube=d_cube_res, turn=(turn[0], Rotation.Clockwise))

    return d_cube_res

def move(
    d_cube: cube,
    l_turns: list[tuple[Face, Rotation]] | tuple[Face, Rotation]
):
    """
    Apply a sequence of turns to the cube.

    Args:
        d_cube (dict[tuple[Letter, PieceType], Color]): The cube to apply the turns to.
        l_turns (list[tuple[Face, Rotation]] | tuple[Face, Rotation]): A sequence of turns to apply.

    Returns:
        dict[tuple[Letter, PieceType], Color]: The cube after applying the sequence of turns.
    """

    if type(l_turns) == tuple:
        l_turns = [l_turns]
        
    for turn in l_turns:
        d_cube = _move(d_cube=d_cube, turn=turn)

    return d_cube