<template>
  <div class="container">
    <img ref="video" class="video" src="../assets/standby.png">
  </div>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { redirectToStandbyOnEndedCall } from '../api/api.js';
    import { start, stop } from '../api/webrtc.js';
    import { wakeupScreen } from '../api/wakeup.js';

    const inputValue = ref('');
    const router = useRouter();
    const soundURL = new URL('/static/assets/ring.mp3', import.meta.url);
    let audio;
    const video = ref(null);
    const _3min_timeout = 180000

    const ring = async () => {
        wakeupScreen();
        audio.loop = true;
        audio.play();

        setTimeout(async () => {
            const room = parseInt(localStorage.getItem('room'), 10);
            const endpoint = 'https://bramka:443/api/call';
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ room: room, call_status: "INACTIVE" }),
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
        video.value.setAttribute("src", "https://bramka:8080/stream/video.mjpeg")
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
