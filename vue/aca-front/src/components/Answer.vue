<template>
  <div class="container">
    <img ref="video" class="video" src="../assets/standby.png">
    <audio id="remote-audio" autoplay=""></audio>
  </div>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { redirectToStandbyOnEndedCall } from '../api/api.js';
    import { start, stop } from '../api/webrtc.js';

    const video = ref(null);

    const router = useRouter();

    let pollTimer;
    const pollInterval = 500;

    onMounted(() => {
      pollTimer = setInterval(async () => redirectToStandbyOnEndedCall(router, video), pollInterval);
      start();
      video.value.setAttribute("src", "https://bramka:8080/stream/video.mjpeg")
    });

    onBeforeUnmount(() => {
      clearInterval(pollTimer);
      video.value.setAttribute("src", "../assets/standby.png")
      stop();
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
