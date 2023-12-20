<template>
  <div class="wrapper">
    <v-container>
      <v-row justify="center">
        <v-col cols="auto">
          <v-btn
            class="answer"
            @click="answerCall"
            size="x-large"
            height="150"
            min-width="250"
            :disabled="answerButtonDisabled"
          >
            Answer
          </v-btn>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="auto">
          <v-btn
            class="open-lock"
            @click="openLockThenEndCall"
            height="150"
            min-width="250"
            size="x-large"
          >
            Open Lock <br> then End Call
          </v-btn>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="auto">
          <v-btn
            class="end-call"
            @click="endCall"
            height="150"
            min-width="250"
            size="x-large"
          >
            End Call
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
  <audio id="remote-audio" autoplay=""></audio>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { endCall, openLock, markCallAsAnswered } from '../api/api.js';
    import { start, stop, getAudioStream } from '../api/webrtc.js';
    const router = useRouter();

    const answerButtonDisabled = ref(false);

    onMounted(() => {
      document.getElementById('remote-audio').muted = true;
      start();
    });

    onBeforeUnmount(() => {
      stop();
    });

    const answerCall = async () => {
      await markCallAsAnswered();
      let remoteAudio = document.getElementById('remote-audio');
      remoteAudio.muted = false

      let audio_stream;
      do {
        audio_stream = getAudioStream();
        await new Promise(r => setTimeout(r, 200));
      } while(audio_stream === null);

      audio_stream.getAudioTracks().forEach(track => {
          track.enabled = true;
      });

      router.push({ name: 'answer' });
      answerButtonDisabled.value = true; // Disable the "Answer" button
    };

    const openLockThenEndCall = () => {
      openLock();
      endCall();
    };

    </script>

    <style scoped>
    .wrapper {
    }

    .end-call {
      background-color: #FF5733;
      cursor: pointer;
    }

    .open-lock {
      background-color: #FFFF00;
      cursor: pointer;
    }

    .answer {
      background-color: #33FF57;
      cursor: pointer;
    }
</style>
