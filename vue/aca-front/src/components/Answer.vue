<template>
  <div class="container">
    <img ref="video" class="video" src="../assets/standby.png">
    <audio id="audio" ref="audio" src="" type="audio/x-wav;codec=pcm" class="hidden" preload="none"></audio>
  </div>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { redirectToStandbyOnEndedCall } from '../api/api.js'

    const audio = ref(null);
    const video = ref(null);
    const router = useRouter();
    let pollTimer;
    const pollInterval = 500;

    onMounted(() => {
      pollTimer = setInterval(async () => redirectToStandbyOnEndedCall(router, video), pollInterval);
      video.value.setAttribute("src", "https://bramka/api/stream/video_feed")
      audio.value.setAttribute("src", "https://bramka/api/stream/audio_feed")
      audio.value.play();
    });

    onBeforeUnmount(() => {
      clearInterval(pollTimer);
      video.value.setAttribute("src", "../assets/standby.png")
      audio.value.setAttribute("src", "")
      audio.value.pause();
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
