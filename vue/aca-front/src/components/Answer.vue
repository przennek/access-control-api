<template>
  <audio id="audio" ref="audio" src="" type="audio/x-wav;codec=pcm" class="hidden" preload="none"></audio>
</template>

<script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';

  const audio = ref(null);

  onMounted(() => {
    audio._value.setAttribute("src", "https://bramka/api/stream/audio_feed")
    audio._value.play();
  });

  onBeforeUnmount(() => {
    audio._value.setAttribute("src", "")
    audio._value.pause();
  });
</script>
