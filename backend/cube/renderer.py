import rich
from cube.enums import Color, PieceType, Letter, Face
from cube.cube import cube

def render_tile(letter: Letter, color: Color, type: PieceType) -> str:
    white = "#F8F8F8"
    yellow = "#FFFF00"
    red = "#FF0000"
    blue = "#009DFF"
    green = "#00FF00"
    orange = "#FFA500"

    d_color_to_hexdec = {
        Color.White: white,
        Color.Yellow: yellow,
        Color.Red: red,
        Color.Blue: blue,
        Color.Green: green,
        Color.Orange: orange
    }

    hexdec = d_color_to_hexdec[color]

    if type == PieceType.Center:
        return f"[black on {hexdec}]   [/black on {hexdec}]"
    
    d_letter_letter = {
        Letter.A: "A",
        Letter.B: "B",
        Letter.C: "C",
        Letter.D: "D",
        Letter.E: "E",
        Letter.F: "F",
        Letter.G: "G",
        Letter.H: "H",
        Letter.I: "I",
        Letter.J: "J",
        Letter.K: "K",
        Letter.L: "L",
        Letter.M: "M",
        Letter.N: "N",
        Letter.O: "O",
        Letter.P: "P",
        Letter.Q: "Q",
        Letter.R: "R",
        Letter.S: "S",
        Letter.T: "T",
        Letter.U: "U",
        Letter.V: "V",
        Letter.W: "W",
        Letter.X: "X",
    }

    letter = d_letter_letter[letter]

    if type == PieceType.Edge:
        return f"[black on {hexdec}] {letter} [/black on {hexdec}]"
    elif type == PieceType.Corner:
        return f"[black on {hexdec}] [italic][underline][bold]{letter}[/bold][/underline][/italic] [/black on {hexdec}]"
    
def print_cube(d_cube: cube) -> None:
    def _render_tile(letter: Letter, type: PieceType) -> str:
        color = d_cube[letter, type]
        return render_tile(letter, color, type)
    
    rich.print(f"""
              {_render_tile(Letter.A, PieceType.Corner)} {_render_tile(Letter.A, PieceType.Edge)} {_render_tile(Letter.B, PieceType.Corner)}

              {_render_tile(Letter.D, PieceType.Edge)} {_render_tile(Face.U, PieceType.Center)} {_render_tile(Letter.B, PieceType.Edge)}

              {_render_tile(Letter.D, PieceType.Corner)} {_render_tile(Letter.C, PieceType.Edge)} {_render_tile(Letter.C, PieceType.Corner)}


{_render_tile(Letter.E, PieceType.Corner)} {_render_tile(Letter.E, PieceType.Edge)} {_render_tile(Letter.F, PieceType.Corner)}   {_render_tile(Letter.I, PieceType.Corner)} {_render_tile(Letter.I, PieceType.Edge)} {_render_tile(Letter.J, PieceType.Corner)}   {_render_tile(Letter.M, PieceType.Corner)} {_render_tile(Letter.M, PieceType.Edge)} {_render_tile(Letter.N, PieceType.Corner)}   {_render_tile(Letter.Q, PieceType.Corner)} {_render_tile(Letter.Q, PieceType.Edge)} {_render_tile(Letter.R, PieceType.Corner)}

{_render_tile(Letter.H, PieceType.Edge)} {_render_tile(Face.L, PieceType.Center)} {_render_tile(Letter.F, PieceType.Edge)}   {_render_tile(Letter.L, PieceType.Edge)} {_render_tile(Face.F, PieceType.Center)} {_render_tile(Letter.J, PieceType.Edge)}   {_render_tile(Letter.P, PieceType.Edge)} {_render_tile(Face.R, PieceType.Center)} {_render_tile(Letter.N, PieceType.Edge)}   {_render_tile(Letter.T, PieceType.Edge)} {_render_tile(Face.B, PieceType.Center)} {_render_tile(Letter.R, PieceType.Edge)}

{_render_tile(Letter.H, PieceType.Corner)} {_render_tile(Letter.G, PieceType.Edge)} {_render_tile(Letter.G, PieceType.Corner)}   {_render_tile(Letter.L, PieceType.Corner)} {_render_tile(Letter.K, PieceType.Edge)} {_render_tile(Letter.K, PieceType.Corner)}   {_render_tile(Letter.P, PieceType.Corner)} {_render_tile(Letter.O, PieceType.Edge)} {_render_tile(Letter.O, PieceType.Corner)}   {_render_tile(Letter.T, PieceType.Corner)} {_render_tile(Letter.S, PieceType.Edge)} {_render_tile(Letter.S, PieceType.Corner)}


              {_render_tile(Letter.U, PieceType.Corner)} {_render_tile(Letter.U, PieceType.Edge)} {_render_tile(Letter.V, PieceType.Corner)}

              {_render_tile(Letter.X, PieceType.Edge)} {_render_tile(Face.D, PieceType.Center)} {_render_tile(Letter.V, PieceType.Edge)}

              {_render_tile(Letter.X, PieceType.Corner)} {_render_tile(Letter.W, PieceType.Edge)} {_render_tile(Letter.W, PieceType.Corner)}
    """)