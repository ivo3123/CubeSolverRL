<template>
  <div>
    <canvas ref="canvas" style="width: 100%; height: 100vh;"></canvas>
    <div id="cube-buttons" style="position: absolute; top: 10px; left: 10px; background: white; padding: 10px;">
      <button @click="applyMove('R')">R</button>
      <button @click="applyMove(`R'`)">R'</button>
      <button @click="applyMove('R2')">R2</button>

      <button @click="applyMove('U')">U</button>      
      <button @click="applyMove(`U'`)">U'</button>      
      <button @click="applyMove('U2')">U2</button>

      <button @click="applyMove('L')">L</button>
      <button @click="applyMove(`L'`)">L'</button>
      <button @click="applyMove('L2')">L2</button>

      <button @click="applyMove('D')">D</button>
      <button @click="applyMove(`D'`)">D'</button>
      <button @click="applyMove('D2')">D2</button>

      <button @click="applyMove('F')">F</button>
      <button @click="applyMove(`F'`)">F'</button>
      <button @click="applyMove('F2')">F2</button>

      <button @click="applyMove('B')">B</button>
      <button @click="applyMove(`B'`)">B'</button>
      <button @click="applyMove('B2')">B2</button>
      <button @click="fetchAndApplyMoves">Solve Cube</button>
      <button @click="applyScramble">Scramble Cube</button>
      
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import * as THREE from 'three'
import { createCube } from '../logic/cube3x3.js'

const canvas = ref(null)
let cubeInstance
let cubieMap = {}

const FACE_INDEX = {
  right: 0,
  left: 1,
  top: 2,
  bottom: 3,
  front: 4,
  back: 5,
}

const speffzMap = {
  Acorner: { pos: [-1, 1, -1], face: 'top' },
  Bcorner: { pos: [1, 1, -1], face: 'top' },
  Ccorner: { pos: [1, 1, 1], face: 'top' },
  Dcorner: { pos: [-1, 1, 1], face: 'top' },
  
  Aedge: { pos: [0, 1, -1], face: 'top' },   
  Bedge: { pos: [1, 1, 0], face: 'top' },    
  Cedge: { pos: [0, 1, 1], face: 'top' },    
  Dedge: { pos: [-1, 1, 0], face: 'top' },   

  Ecorner: { pos: [-1, 1, -1], face: 'left' },
  Eedge:   { pos: [-1, 0, -1], face: 'left' },
  Fcorner: { pos: [-1, 1, 0], face: 'left' },
  Fedge: { pos: [-1, 0, 0], face: 'left' },
  Gcorner: { pos: [-1, -1, 0], face: 'left' },
  Gedge:   { pos: [-1, -1, 0], face: 'left' },
  Hcorner: { pos: [-1, -1, -1], face: 'left' },
  Hedge:   { pos: [-1, 0, -1], face: 'left' },

  Icorner: { pos: [-1, 1, 1], face: 'front' },
  Iedge:   { pos: [0, 1, 1], face: 'front' },
  Jcorner: { pos: [1, 1, 1], face: 'front' },
  Jedge: { pos: [1, 0, 1], face: 'front' },
  Kcorner: { pos: [1, -1, 1], face: 'front' },
  Kedge:   { pos: [0, -1, 1], face: 'front' },
  Lcorner: { pos: [-1, -1, 1], face: 'front' },
  Ledge:   { pos: [-1, 0, 1], face: 'front' },

  Mcorner: { pos: [1, 1, 1], face: 'right' },
  Medge:   { pos: [1, 1, 0], face: 'right' },
  Ncorner: { pos: [1, 1, -1], face: 'right' },  
  Nedge: { pos: [1, 0, -1], face: 'right' },  
  Ocorner: { pos: [1, -1, -1], face: 'right' },
  Oedge:   { pos: [1, -1, 0], face: 'right' },
  Pcorner: { pos: [1, -1, 1], face: 'right' },
  Pedge:   { pos: [1, 0, 1], face: 'right' },

  Qcorner: { pos: [1, 1, -1], face: 'back' },
  Qedge:   { pos: [0, 1, -1], face: 'back' },
  Rcorner: { pos: [-1, 1, -1], face: 'back' },  
  Redge: { pos: [-1, 0, -1], face: 'back' }, 
  Scorner: { pos: [-1, -1, -1], face: 'back' },
  Sedge:   { pos: [0, -1, -1], face: 'back' },
  Tcorner: { pos: [1, -1, -1], face: 'back' },
  Tedge:   { pos: [1, 0, -1], face: 'back' },

  Ucorner: { pos: [-1, -1, 1], face: 'bottom' },
  Uedge:   { pos: [0, -1, 1], face: 'bottom' },
  Vcorner: { pos: [1, -1, 1], face: 'bottom' },
  Vedge: { pos: [1, -1, 0], face: 'bottom' }, 
  Wcorner: { pos: [1, -1, -1], face: 'bottom' },
  Wedge: { pos: [0, -1, -1], face: 'bottom' },
  Xcorner: { pos: [-1, -1, -1], face: 'bottom' },
  Xedge: { pos: [-1, -1, 0], face: 'bottom' },

  Ucentre: { pos: [0, 1, 0], face: 'top' },
  Dcentre: { pos: [0, -1, 0], face: 'bottom' },
  Fcentre: { pos: [0, 0, 1], face: 'front' },
  Bcentre: { pos: [0, 0, -1], face: 'back' },
  Lcentre: { pos: [-1, 0, 0], face: 'left' },
  Rcentre: { pos: [1, 0, 0], face: 'right' },
}

const getLetter = (id) => id.replace(/(edge|corner)/, '')

const updateColorsFromCube = () => {
  const cubeState = cubeInstance.state

  for (const key of cubeInstance.state.keys()) {
  const color = cubeInstance.state.get(key)
  //const entry = speffzMap[key]
  const entry = speffzMap[key] || speffzMap[letter]
  if (!entry) continue

  const { pos, face } = entry
  const mesh = cubieMap[pos.toString()]
  const faceIdx = FACE_INDEX[face]

  if (mesh && mesh.material[faceIdx].color.getHexString() === '000000') {
    mesh.material[faceIdx].color.set(color)
  }
}
}

const applyMove = (notation) => {
  cubeInstance.move(notation)
  for (const mesh of Object.values(cubieMap)) {
    mesh.material.forEach(m => m.color.set('black'))
  }
  updateColorsFromCube()
}

onMounted(() => {
  cubeInstance = createCube()

  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 1000)
  camera.position.set(5, 5, 5)
  camera.lookAt(0, 0, 0)

  const renderer = new THREE.WebGLRenderer({ canvas: canvas.value, antialias: true })
  renderer.setSize(window.innerWidth, window.innerHeight)

  const light = new THREE.AmbientLight(0xffffff)
  scene.add(light)

  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        const materials = new Array(6).fill().map(() => new THREE.MeshBasicMaterial({ color: 'black' }))
        const cube = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.95, 0.95), materials)
        cube.position.set(x, y, z)
        scene.add(cube)
        cubieMap[`${x},${y},${z}`] = cube
      }
    }
  }

  updateColorsFromCube()

  const animate = () => {
    requestAnimationFrame(animate)
    renderer.render(scene, camera)
  }

  animate()
})

function applyMoves(moves) {
  if (!Array.isArray(moves)) {
    console.error("Invalid moves:", moves);
    return;
  }

  let delay = 500; // milliseconds between moves
  let index = 0;

  const performNextMove = () => {
    if (index >= moves.length) return;

    const move = moves[index];
    applyMove(move);
    index++;

    setTimeout(performNextMove, delay);
  };

  performNextMove();
}

function fetchAndApplyMoves() {
 fetch("http://127.0.0.1:8000/solve")
  .then(res => res.json())
  .then(data => {
    const moves = data.moves;
    console.log(data)
    console.log(moves)
    applyMoves(moves);
  });
}

function applyScramble() {
  const scramble = ["R2", "U2", "F'", "L", "D2", "B'", "R", "D", "L'", "F2", "U", "B2"];
  applyMoves(scramble);
}
</script>