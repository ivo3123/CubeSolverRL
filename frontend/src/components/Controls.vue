<template>
  <div class="controls">
    <button @click="$emit('scramble')">Разбъркай</button>
    <button @click="$emit('step')"> Нова стъпка (RL)</button>
  </div>
</template>

<style scoped>
.controls {
  padding: 1rem;
  display: flex;
  gap: 1rem;
}
</style>