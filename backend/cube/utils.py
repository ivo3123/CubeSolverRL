import numpy as np
from cube.enums import Face, Rotation, Letter, Color, PieceType
from cube.cube import get_solved_cube, move

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

def get_neighbor_edge(letter: Letter) -> Letter:
    edge_pairs = {
        Letter.A: Letter.Q, Letter.Q: Letter.A,
        Letter.B: Letter.M, Letter.M: Letter.B,
        Letter.C: Letter.I, Letter.I: Letter.C,
        Letter.D: Letter.E, Letter.E: Letter.D,
        Letter.F: Letter.L, Letter.L: Letter.F,
        Letter.G: Letter.X, Letter.X: Letter.G,
        Letter.H: Letter.R, Letter.R: Letter.H,
        Letter.J: Letter.P, Letter.P: Letter.J,
        Letter.K: Letter.U, Letter.U: Letter.K,
        Letter.N: Letter.T, Letter.T: Letter.N,
        Letter.O: Letter.V, Letter.V: Letter.O,
        Letter.S: Letter.W, Letter.W: Letter.S,
    }

    return edge_pairs.get(letter)

def get_neighbor_corner(letter: Letter) -> tuple[Letter, Letter] | None:
    corner_triplets = [
        (Letter.U, Letter.G, Letter.L),
        (Letter.V, Letter.K, Letter.P),
        (Letter.W, Letter.O, Letter.T),
        (Letter.X, Letter.S, Letter.H),

        (Letter.D, Letter.F, Letter.I),
        (Letter.C, Letter.J, Letter.M),
        (Letter.B, Letter.N, Letter.Q),
        (Letter.A, Letter.E, Letter.R),
    ]
    
    for a, b, c in corner_triplets:
        if letter == a:
            return (b, c)
        elif letter == b:
            return (a, c)
        elif letter == c:
            return (a, b)

def transform_into_numpy_array(
    cube: dict,
    should_consider_edges_first_layer = True,
    should_consider_corners_first_layer = False,
    should_consider_edges_second_layer = False,
    should_consider_edges_third_layer = False,
    should_consider_corners_third_layer = False,
) -> np.ndarray:
    """Convert the cube state to a numpy array observation."""

    cube_copy = cube.copy()

    if not should_consider_corners_first_layer and not should_consider_corners_third_layer:
        for letter in list(Letter):
            cube_copy[(letter, PieceType.Corner)] = Color.Unknown
    elif should_consider_corners_first_layer and not should_consider_corners_third_layer:
        for letter in [Letter.A, Letter.B, Letter.C, Letter.D, Letter.U, Letter.V, Letter.W, Letter.X]:
            neighbor1, neighbor2 = get_neighbor_corner(letter=letter)
            if cube_copy.get((letter, PieceType.Corner)) == Color.White\
                or cube_copy.get((neighbor1, PieceType.Corner)) == Color.White\
                or cube_copy.get((neighbor2, PieceType.Corner)) == Color.White:
                cube_copy[(letter, PieceType.Corner)] = Color.Unknown
                cube_copy[(neighbor1, PieceType.Corner)] = Color.Unknown
                cube_copy[(neighbor2, PieceType.Corner)] = Color.Unknown

    if not should_consider_edges_third_layer:
        for letter in [Letter.A, Letter.B, Letter.C, Letter.D, Letter.J, Letter.R, Letter.L, Letter.N, Letter.U, Letter.V, Letter.W, Letter.X]:
            neighbor = get_neighbor_edge(letter=letter)
            if cube_copy.get((letter, PieceType.Edge)) == Color.White or cube_copy.get((neighbor, PieceType.Edge)) == Color.White:
                cube_copy[(letter, PieceType.Edge)] = Color.Unknown
                cube_copy[(neighbor, PieceType.Edge)] = Color.Unknown

    if not should_consider_edges_second_layer:
        for letter in [Letter.A, Letter.B, Letter.C, Letter.D, Letter.J, Letter.R, Letter.L, Letter.N, Letter.U, Letter.V, Letter.W, Letter.X]:
            neighbor = get_neighbor_edge(letter=letter)
            if cube_copy.get((letter, PieceType.Edge)) not in [Color.White, Color.Yellow] and cube_copy.get((neighbor, PieceType.Edge)) not in [Color.White, Color.Yellow]:
                cube_copy[(letter, PieceType.Edge)] = Color.Unknown
                cube_copy[(neighbor, PieceType.Edge)] = Color.Unknown

    def get_face(letter1, letter2, letter3, letter4, face):
        np_face_top_row = np.array([
            cube_copy.get((letter1, PieceType.Corner)).value,
            cube_copy.get((letter1, PieceType.Edge)).value,
            cube_copy.get((letter2, PieceType.Corner)).value,
        ])

        np_face_middle_row = np.array([
            cube_copy.get((letter4, PieceType.Edge)).value,
            cube_copy.get((face, PieceType.Center)).value,
            cube_copy.get((letter2, PieceType.Edge)).value,
        ])

        np_face_bottom_row = np.array([
            cube_copy.get((letter4, PieceType.Corner)).value,
            cube_copy.get((letter3, PieceType.Edge)).value,
            cube_copy.get((letter3, PieceType.Corner)).value,
        ])

        np_face = np.array([
            np_face_top_row,
            np_face_middle_row,
            np_face_bottom_row,
        ])

        return np_face

    np_u_face = get_face(Letter.A, Letter.B, Letter.C, Letter.D, Face.U)
    np_l_face = get_face(Letter.E, Letter.F, Letter.G, Letter.H, Face.L)
    np_f_face = get_face(Letter.I, Letter.J, Letter.K, Letter.L, Face.F)
    np_r_face = get_face(Letter.M, Letter.N, Letter.O, Letter.P, Face.R)
    np_b_face = get_face(Letter.Q, Letter.R, Letter.S, Letter.T, Face.B)
    np_d_face = get_face(Letter.U, Letter.V, Letter.W, Letter.X, Face.D)

    np_cube = np.array([
        np_u_face,
        np_l_face,
        np_f_face,
        np_r_face,
        np_b_face,
        np_d_face,
    ])

    return np_cube

def flat_state_to_cube_dict(flat_state: list[int]) -> dict:
    """Преобразува 54-елементен масив към вътрешното представяне на куба (dict)."""
    # Подредбата трябва да съответства на transform_into_numpy_array
    # Връща dict[(Letter, PieceType)] = Color
    from cube.enums import Face, Letter, PieceType, Color
    
    # Лицата и позициите по реда на transform_into_numpy_array
    face_letters = [
        # U
        [Letter.A, Letter.B, Letter.C, Letter.D],
        # L
        [Letter.E, Letter.F, Letter.G, Letter.H],
        # F
        [Letter.I, Letter.J, Letter.K, Letter.L],
        # R
        [Letter.M, Letter.N, Letter.O, Letter.P],
        # B
        [Letter.Q, Letter.R, Letter.S, Letter.T],
        # D
        [Letter.U, Letter.V, Letter.W, Letter.X],
    ]
    face_names = [Face.U, Face.L, Face.F, Face.R, Face.B, Face.D]
    
    cube = {}
    idx = 0
    for face_idx, (face, letters) in enumerate(zip(face_names, face_letters)):
        # Top row: corner, edge, corner
        cube[(letters[0], PieceType.Corner)] = Color(flat_state[idx]); idx += 1
        cube[(letters[0], PieceType.Edge)]   = Color(flat_state[idx]); idx += 1
        cube[(letters[1], PieceType.Corner)] = Color(flat_state[idx]); idx += 1
        # Middle row: edge, center, edge
        cube[(letters[3], PieceType.Edge)]   = Color(flat_state[idx]); idx += 1
        cube[(face, PieceType.Center)]       = Color(flat_state[idx]); idx += 1
        cube[(letters[1], PieceType.Edge)]   = Color(flat_state[idx]); idx += 1
        # Bottom row: corner, edge, corner
        cube[(letters[3], PieceType.Corner)] = Color(flat_state[idx]); idx += 1
        cube[(letters[2], PieceType.Edge)]   = Color(flat_state[idx]); idx += 1
        cube[(letters[2], PieceType.Corner)] = Color(flat_state[idx]); idx += 1
    return cube

cube = get_solved_cube()
cube = move(cube, [(Face.U, Rotation.Clockwise)])  # Примерно разбъркване
obs = transform_into_numpy_array(cube, should_consider_edges_first_layer=True)
print(obs.flatten().tolist())

obs = transform_into_numpy_array(get_solved_cube(), should_consider_edges_first_layer=True)
print(obs.flatten().tolist())