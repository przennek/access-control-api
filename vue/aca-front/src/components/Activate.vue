<template>
  <div class="container">
    <v-sheet max-width="300" class="mx-auto">
    <v-form validate-on="submit lazy" @submit.prevent="submit">
      <v-text-field
        v-model="inputValue"
        :rules="rules"
        label="Username"
      ></v-text-field>

      <v-btn
        :loading="loading"
        type="submit"
        block
        class="mt-2"
        text="Activate"
        @click="activate"
      ></v-btn>
    </v-form>
  </v-sheet>
  </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router';
    import { handleUserActivation } from '../api/api.js';

    const inputValue = ref('');
    const router = useRouter();

    const activate = async () => {
        await handleUserActivation(router, inputValue.value)
    };

    onMounted(() => {
      if (localStorage.getItem('user')) {
        router.push({ name: 'standby' });
      }
    });
</script>

<style scoped>
    .container {
      width: 640px;
      height: 480px;
    }
</style>
