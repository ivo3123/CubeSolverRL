//New
import colors from "../colors";

const [white, orange, green, red, blue, yellow] = Object.values(colors);

const initialCubeState = {
    U: { pieceIds: ["A", "B", "C", "D"], color: white },
    L: { pieceIds: ["E", "F", "G", "H"], color: orange },
    F: { pieceIds: ["I", "J", "K", "L"], color: green },
    R: { pieceIds: ["M", "N", "O", "P"], color: red },
    B: { pieceIds: ["Q", "R", "S", "T"], color: blue },
    D: { pieceIds: ["U", "V", "W", "X"], color: yellow },
};

export function createCube() {
    const cube = new Map();

    // Initialize
    for (const face in initialCubeState) {
        const { pieceIds, color } = initialCubeState[face];
        for (const letter of pieceIds) {
            cube.set(`${letter}edge`, color);
            cube.set(`${letter}corner`, color);
        }
        cube.set(`${face}centre`, color);
    }

    const makeSingleTurn = (val1, val2, val3, val4) => {
        const tmp = cube.get(val1);
        cube.set(val1, cube.get(val4));
        cube.set(val4, cube.get(val3));
        cube.set(val3, cube.get(val2));
        cube.set(val2, tmp);
    };

    const makeDoubleTurn = (val1, val2, val3, val4) => {
        makeSingleTurn(val1, val2, val3, val4);
        makeSingleTurn(val1, val2, val3, val4);
    };

    const move = (turn) => {
        const m = makeSingleTurn;
        const d = makeDoubleTurn;

       if (turn === "R") {
        makeSingleTurn("Bcorner", "Jcorner", "Vcorner", "Tcorner");
        makeSingleTurn("Ccorner", "Kcorner", "Wcorner", "Qcorner");
        makeSingleTurn("Bedge", "Jedge", "Vedge", "Tedge");

        makeSingleTurn("Medge", "Pedge", "Oedge", "Nedge");
        makeSingleTurn("Mcorner", "Pcorner", "Ocorner", "Ncorner");
    } else if (turn === "R'") {
        makeSingleTurn("Bcorner", "Tcorner", "Vcorner", "Jcorner");
        makeSingleTurn("Ccorner", "Qcorner", "Wcorner", "Kcorner");
        makeSingleTurn("Bedge", "Tedge", "Vedge", "Jedge");

        makeSingleTurn("Medge", "Nedge", "Oedge", "Pedge");
        makeSingleTurn("Mcorner", "Ncorner", "Ocorner", "Pcorner");
    } else if (turn === "R2") {
        makeDoubleTurn("Bcorner", "Jcorner", "Vcorner", "Tcorner");
        makeDoubleTurn("Ccorner", "Kcorner", "Wcorner", "Qcorner");
        makeDoubleTurn("Bedge", "Jedge", "Vedge", "Tedge");

        makeDoubleTurn("Medge", "Pedge", "Oedge", "Nedge");
        makeDoubleTurn("Mcorner", "Pcorner", "Ocorner", "Ncorner");
    } else if (turn == "U") {
        makeSingleTurn("Jcorner", "Ncorner", "Rcorner", "Fcorner");
        makeSingleTurn("Icorner", "Mcorner", "Qcorner", "Ecorner");
        makeSingleTurn("Iedge", "Medge", "Qedge", "Eedge");

        makeSingleTurn("Dedge", "Cedge", "Bedge", "Aedge");
        makeSingleTurn("Dcorner", "Ccorner", "Bcorner", "Acorner");
    } else if (turn === "U'") {
        makeSingleTurn("Jcorner", "Fcorner", "Rcorner", "Ncorner");
        makeSingleTurn("Icorner", "Ecorner", "Qcorner", "Mcorner");
        makeSingleTurn("Iedge", "Eedge", "Qedge", "Medge");

        makeSingleTurn("Aedge", "Bedge", "Cedge", "Dedge");
        makeSingleTurn("Acorner", "Bcorner", "Ccorner", "Dcorner");
    } else if (turn === "U2") {
        makeDoubleTurn("Jcorner", "Ncorner", "Rcorner", "Fcorner");
        makeDoubleTurn("Icorner", "Mcorner", "Qcorner", "Ecorner");
        makeDoubleTurn("Iedge", "Medge", "Qedge", "Eedge");

        makeDoubleTurn("Dedge", "Cedge", "Bedge", "Aedge");
        makeDoubleTurn("Dcorner", "Ccorner", "Bcorner", "Acorner");
    } else if (turn === "L") {
        makeSingleTurn("Acorner", "Scorner", "Ucorner", "Icorner");
        makeSingleTurn("Dcorner", "Rcorner", "Xcorner", "Lcorner");
        makeSingleTurn("Dedge", "Redge", "Xedge", "Ledge");

        makeSingleTurn("Fcorner", "Ecorner", "Hcorner", "Gcorner");
        makeSingleTurn("Eedge", "Hedge", "Gedge", "Fedge");
    } else if (turn === "L'") {
        makeSingleTurn("Acorner", "Icorner", "Ucorner", "Scorner");
        makeSingleTurn("Dcorner", "Lcorner", "Xcorner", "Rcorner");
        makeSingleTurn("Dedge", "Ledge", "Xedge", "Redge");

        makeSingleTurn("Fcorner", "Gcorner", "Hcorner", "Ecorner");
        makeSingleTurn("Eedge", "Fedge", "Gedge", "Hedge");
    } else if (turn === "L2") {
        makeDoubleTurn("Acorner", "Scorner", "Ucorner", "Icorner");
        makeDoubleTurn("Dcorner", "Rcorner", "Xcorner", "Lcorner");
        makeDoubleTurn("Dedge", "Redge", "Xedge", "Ledge");

        makeDoubleTurn("Fcorner", "Ecorner", "Hcorner", "Gcorner");
        makeDoubleTurn("Eedge", "Hedge", "Gedge", "Fedge");
    } else if (turn === "D") {
        makeSingleTurn("Kcorner", "Gcorner", "Scorner", "Ocorner");
        makeSingleTurn("Lcorner", "Hcorner", "Tcorner", "Pcorner");
        makeSingleTurn("Kedge", "Gedge", "Sedge", "Oedge");

        makeSingleTurn("Vcorner", "Ucorner", "Xcorner", "Wcorner");
        makeSingleTurn("Uedge", "Xedge", "Wedge", "Vedge");
    } else if (turn === "D'") {
        makeSingleTurn("Kcorner", "Ocorner", "Scorner", "Gcorner");
        makeSingleTurn("Lcorner", "Pcorner", "Tcorner", "Hcorner");
        makeSingleTurn("Kedge", "Oedge", "Sedge", "Gedge");

        makeSingleTurn("Vcorner", "Wcorner", "Xcorner", "Ucorner");
        makeSingleTurn("Uedge", "Vedge", "Wedge", "Xedge");
    } else if (turn === "D2") {
        makeDoubleTurn("Kcorner", "Gcorner", "Scorner", "Ocorner");
        makeDoubleTurn("Lcorner", "Hcorner", "Tcorner", "Pcorner");
        makeDoubleTurn("Kedge", "Gedge", "Sedge", "Oedge");

        makeDoubleTurn("Vcorner", "Ucorner", "Xcorner", "Wcorner");
        makeDoubleTurn("Uedge", "Xedge", "Wedge", "Vedge");
    } else if (turn === "F") {
        makeSingleTurn("Mcorner", "Dcorner", "Gcorner", "Vcorner");
        makeSingleTurn("Pcorner", "Ccorner", "Fcorner", "Ucorner");
        makeSingleTurn("Pedge", "Cedge", "Fedge", "Uedge");

        makeSingleTurn("Jcorner", "Icorner", "Lcorner", "Kcorner");
        makeSingleTurn("Jedge", "Iedge", "Ledge", "Kedge");
    } else if (turn === "F'") {
        makeSingleTurn("Mcorner", "Vcorner", "Gcorner", "Dcorner");
        makeSingleTurn("Pcorner", "Ucorner", "Fcorner", "Ccorner");
        makeSingleTurn("Pedge", "Uedge", "Fedge", "Cedge");

        makeSingleTurn("Jcorner", "Kcorner", "Lcorner", "Icorner");
        makeSingleTurn("Jedge", "Kedge", "Ledge", "Iedge");
    } else if (turn === "F2") {
        makeDoubleTurn("Mcorner", "Dcorner", "Gcorner", "Vcorner");
        makeDoubleTurn("Pcorner", "Ccorner", "Fcorner", "Ucorner");
        makeDoubleTurn("Pedge", "Cedge", "Fedge", "Uedge");

        makeDoubleTurn("Jcorner", "Icorner", "Lcorner", "Kcorner");
        makeDoubleTurn("Jedge", "Iedge", "Ledge", "Kedge");
    } else if (turn === "B") {
        makeSingleTurn("Acorner", "Ncorner", "Wcorner", "Hcorner");
        makeSingleTurn("Bcorner", "Ocorner", "Xcorner", "Ecorner");
        makeSingleTurn("Aedge", "Nedge", "Wedge", "Hedge");

        makeSingleTurn("Qcorner", "Tcorner", "Scorner", "Rcorner");
        makeSingleTurn("Qedge", "Tedge", "Sedge", "Redge");
    } else if (turn === "B'") {
        makeSingleTurn("Acorner", "Hcorner", "Wcorner", "Ncorner");
        makeSingleTurn("Bcorner", "Ecorner", "Xcorner", "Ocorner");
        makeSingleTurn("Aedge", "Hedge", "Wedge", "Nedge");

        makeSingleTurn("Qcorner", "Rcorner", "Scorner", "Tcorner");
        makeSingleTurn("Qedge", "Redge", "Sedge", "Tedge");
    } else if (turn === "B2") {
        makeDoubleTurn("Acorner", "Ncorner", "Wcorner", "Hcorner");
        makeDoubleTurn("Bcorner", "Ocorner", "Xcorner", "Ecorner");
        makeDoubleTurn("Aedge", "Nedge", "Wedge", "Hedge");

        makeDoubleTurn("Qcorner", "Tcorner", "Scorner", "Rcorner");
        makeDoubleTurn("Qedge", "Tedge", "Sedge", "Redge");
    }
    };

    return {
        get state() {
            return cube;
        },
        move,
    };
}