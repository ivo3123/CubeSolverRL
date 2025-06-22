<template>
  <div id="app">
    <Controls @scramble="scrambleCube" @step="stepCube" />
    <Cube :cubeSpeffz="cubeSpeffz" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Controls from './components/Controls.vue'
import Cube from './components/Cube.vue'
import { resetCube, stepCube, getCubeState } from './logic/api'

//cube's state as a Map<face, array of 9 chars>
const cubeSpeffz = ref(new Map())

async function scrambleCube() {
  await resetCube()
  const data = await getCubeState()
  cubeSpeffz.value = new Map(Object.entries(data.facelets))  // facelets: { U: ['w', 'w', ...], ... }
}

async function stepOnce() {
  await stepCube(0)  
  const data = await getCubeState()
  cubeSpeffz.value = new Map(Object.entries(data.facelets))
}

/*onMounted(scrambleCube)*/     /*Temporary replaced before using Fast API*/
/*A hardcoded test*/
onMounted(() => {
cubeSpeffz.value = new Map([
  ['U', Array(9).fill('w')],
  ['L', Array(9).fill('o')],
  ['F', Array(9).fill('g')],
  ['R', Array(9).fill('r')],
  ['B', Array(9).fill('b')],
  ['D', Array(9).fill('y')],
])
})
</script>