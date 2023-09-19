<template>
  <audio id="audio" src="https://bramka/api/stream/audio_feed" type="audio/x-wav;codec=pcm" class="hidden" preload="none"></audio>
</template>

<script>
  import { ref, onMounted, onUnmounted } from 'vue';

  const audio = document.getElementById("audio");

  function play() {
    audio.play();
  }

  onMounted(() => {
    audio.play();
  });

  onUnmounted(() => {
    audio.pause(); // To pause the audio when the component is unmounted
  });
</script>
