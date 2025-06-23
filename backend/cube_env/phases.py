from enum import Enum
from cube.enums import Letter, PieceType, Color
from cube.cube import cube

class Phases(Enum):
    Unknown = 0
    EdgesFirstLayer = 1
    CornersFirstLayer = 2
    EdgesSecondLayer = 3
    Solved = 4

def count_solved_edges_first_layer(d_cube: cube) -> int:
    is_edge_1_solved =\
        d_cube.get((Letter.U, PieceType.Edge)) == Color.Yellow\
        and d_cube.get((Letter.K, PieceType.Edge)) == Color.Green
    
    is_edge_2_solved =\
        d_cube.get((Letter.V, PieceType.Edge)) == Color.Yellow\
        and d_cube.get((Letter.O, PieceType.Edge)) == Color.Red
    
    is_edge_3_solved =\
        d_cube.get((Letter.W, PieceType.Edge)) == Color.Yellow\
        and d_cube.get((Letter.S, PieceType.Edge)) == Color.Blue
    
    is_edge_4_solved =\
        d_cube.get((Letter.X, PieceType.Edge)) == Color.Yellow\
        and d_cube.get((Letter.G, PieceType.Edge)) == Color.Orange
    
    return int(is_edge_1_solved) + int(is_edge_2_solved) + int(is_edge_3_solved) + int(is_edge_4_solved)

def are_edges_firs_layer_solved(d_cube: cube) -> bool:
    return count_solved_edges_first_layer(d_cube) == 4

def count_solved_corners_first_layer(d_cube: cube) -> int:
    is_corner_1_solved =\
        d_cube.get((Letter.U, PieceType.Corner)) == Color.Yellow\
        and d_cube.get((Letter.G, PieceType.Corner)) == Color.Orange\
        and d_cube.get((Letter.L, PieceType.Corner)) == Color.Green

    is_corner_2_solved =\
        d_cube.get((Letter.V, PieceType.Corner)) == Color.Yellow\
        and d_cube.get((Letter.K, PieceType.Corner)) == Color.Green\
        and d_cube.get((Letter.P, PieceType.Corner)) == Color.Red

    is_corner_3_solved =\
        d_cube.get((Letter.W, PieceType.Corner)) == Color.Yellow\
        and d_cube.get((Letter.O, PieceType.Corner)) == Color.Red\
        and d_cube.get((Letter.T, PieceType.Corner)) == Color.Blue

    is_corner_4_solved =\
        d_cube.get((Letter.X, PieceType.Corner)) == Color.Yellow\
        and d_cube.get((Letter.S, PieceType.Corner)) == Color.Blue\
        and d_cube.get((Letter.H, PieceType.Corner)) == Color.Orange

    return int(is_corner_1_solved) + int(is_corner_2_solved) + int(is_corner_3_solved) + int(is_corner_4_solved)