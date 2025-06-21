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