<template>
  <div>
    <img @click="requestFullscreen" ref="standby" class="standby-image" src="../assets/standby.png">
  </div>
</template>

<script setup>
    const requestFullscreen = () => {
        var elem = document.querySelector("body").requestFullscreen();
    };
</script>

<style scoped>
    .standby-image {
      width: 640px;
      height: 480px;
    }
</style>
