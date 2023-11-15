import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useWakeLockStore = defineStore('wakeLock', () => {
    const wakeLock = ref(null);

    function setWakeLock(value) {
        wakeLock.value = value;
    }

    return { wakeLock, setWakeLock };
});
