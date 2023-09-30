<template>
  <div class="container">
    <img ref="video" class="video" src="../assets/standby.png">
  </div>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { redirectToStandbyOnEndedCall } from '../api/api.js';

    const inputValue = ref('');
    const router = useRouter();
    const soundURL = new URL('/static/assets/ring.mp3', import.meta.url);
    let audio;
    const video = ref(null);
    const _3min_timeout = 180000

    const ring = async () => {
        audio.loop = true;
        audio.play();

        setTimeout(async () => {
            const room = parseInt(localStorage.getItem('room'), 10);
            const endpoint = 'https://bramka:443/api/call';
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ room: room, ongoing_call: false }),
            };

            const response = await fetch(endpoint, requestOptions);
                audio.pause();
                router.push({ name: 'standby' });
            },
            _3min_timeout
        );
    };

    let pollTimer;
    const pollInterval = 500;

    onMounted(() => {
        audio = new Audio(soundURL);
        ring();
        video.value.setAttribute("src", "https://bramka/api/stream/video_feed")
        pollTimer = setInterval(() => redirectToStandbyOnEndedCall(router, video), pollInterval);
    });

    onBeforeUnmount(() => {
      clearInterval(pollTimer);
      video.value.setAttribute("src", "../assets/standby.png")
      audio.pause()
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
</style>
