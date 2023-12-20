<template>
  <div class="container">
    <img ref="video" class="video" src="../assets/standby.png">
  </div>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { redirectToStandbyOnEndedCall } from '../api/api.js';

    const video = ref(null);

    const router = useRouter();

    let pollTimer;
    const pollInterval = 500;

    onMounted(() => {
      pollTimer = setInterval(async () => redirectToStandbyOnEndedCall(router, video), pollInterval);
      video.value.setAttribute("src", "https://bramka:8080/stream/video.mjpeg")
    });

    onBeforeUnmount(() => {
      clearInterval(pollTimer);
      video.value.setAttribute("src", "../assets/standby.png")
    });


</script>

<style scoped>
    .container {
      width: 640px;
      height: 480px;
    }

    .video {
      width: 640px;
      height: 480px;
    }

    .hidden {
      display: none;
    }
</style>
