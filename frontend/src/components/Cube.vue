<template>
  <div ref="cubeContainer" class="cube-container"></div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import * as THREE from 'three'
import { charToColorIndex, colorMap } from '../logic/cube'

const cubeContainer = ref(null)
const props = defineProps({ cubeSpeffz: Map })

let scene, camera, renderer, cubeGroup = new THREE.Group()

const faceData = {
  L: { coord: -1, axis: 'x', index: 1 }, 
  R: { coord: 1, axis: 'x', index: 0 },  
  U: { coord: 1, axis: 'y', index: 2 },
  D: { coord: -1, axis: 'y', index: 3 },
  F: { coord: 1, axis: 'z', index: 4 },
  B: { coord: -1, axis: 'z', index: 5 },
}

function getFaceletIndex(face, x, y, z) {
  const map = {
    U: [
      [-1, 1, -1], [0, 1, -1], [1, 1, -1],
      [-1, 1,  0], [0, 1,  0], [1, 1,  0],
      [-1, 1,  1], [0, 1,  1], [1, 1,  1],
    ],
    D: [
      [-1, -1,  1], [0, -1,  1], [1, -1,  1],
      [-1, -1,  0], [0, -1,  0], [1, -1,  0],
      [-1, -1, -1], [0, -1, -1], [1, -1, -1],
    ],
    F: [
      [-1,  1, 1], [0,  1, 1], [1,  1, 1],
      [-1,  0, 1], [0,  0, 1], [1,  0, 1],
      [-1, -1, 1], [0, -1, 1], [1, -1, 1],
    ],
    B: [
      [1,  1, -1], [0,  1, -1], [-1,  1, -1],
      [1,  0, -1], [0,  0, -1], [-1,  0, -1],
      [1, -1, -1], [0, -1, -1], [-1, -1, -1],
    ],
    L: [
      [-1,  1, -1], [-1,  1, 0], [-1,  1, 1],
      [-1,  0, -1], [-1,  0, 0], [-1,  0, 1],
      [-1, -1, -1], [-1, -1, 0], [-1, -1, 1],
    ],
    R: [
      [1,  1, 1], [1,  1, 0], [1,  1, -1],
      [1,  0, 1], [1,  0, 0], [1,  0, -1],
      [1, -1, 1], [1, -1, 0], [1, -1, -1],
    ],
  }

  const positions = map[face]
  for (let i = 0; i < positions.length; i++) {
    const [px, py, pz] = positions[i]
    if (px === x && py === y && pz === z) {
      return i
    }
  }
  return -1
}

function buildCube(faceMap) {
  cubeGroup.clear()

  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        const materials = Array(6).fill(null).map(() =>
          new THREE.MeshStandardMaterial({ color: '#000000', side: THREE.FrontSide })
        )

        for (const [face, { coord, axis, index }] of Object.entries(faceData)) {
          if ((axis === 'x' && x !== coord) ||
              (axis === 'y' && y !== coord) ||
              (axis === 'z' && z !== coord)) continue

          const faceColors = faceMap.get(face) || []
          const faceletIndex = getFaceletIndex(face, x, y, z)
          if (faceletIndex === -1) continue
          const colorChar = faceColors[faceletIndex] || 'w'
          const hex = colorMap[charToColorIndex[colorChar]]
          materials[index] = new THREE.MeshStandardMaterial({ color: hex, side: THREE.FrontSide })
        }

        const cubelet = new THREE.Mesh(
          new THREE.BoxGeometry(0.95, 0.95, 0.95),
          materials
        )
        cubelet.position.set(x, y, z)
        cubeGroup.add(cubelet)
      }
    }
  }

  scene.add(cubeGroup)
}

onMounted(() => {
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xF5F5DC) 
  camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000)
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(600, 600)
  cubeContainer.value.appendChild(renderer.domElement)

  camera.position.z = 5

  scene.add(new THREE.AmbientLight(0xffffff, 0.3))
  const light = new THREE.DirectionalLight(0xffffff, 0.8)
  light.position.set(5, 5, 5)
  scene.add(light)

  buildCube(props.cubeSpeffz)

  const animate = () => {
    requestAnimationFrame(animate)
    cubeGroup.rotation.y += 0.01
    cubeGroup.rotation.x += 0.003
    renderer.render(scene, camera)
  }

  animate()
})

watch(() => props.cubeSpeffz, (newMap) => {
  buildCube(newMap)
})
</script>

<style scoped>
.cube-container {
  width: 100%;
  height: 100%;
}
</style>
