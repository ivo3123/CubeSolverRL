<template>
  <Cube3D />
</template>

<script>
import Cube3D from './components/Cube3D.vue';

export default {
  name: 'App',
  components: {
    Cube3D
  }
};
</script>

<style>
body, html, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>