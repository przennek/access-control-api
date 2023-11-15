import { useWakeLockStore } from '../stores/wake.js';

export const wakeupScreen = async () => {
    const store = useWakeLockStore();
    try {
        const wakeLock = await navigator.wakeLock.request('screen');
        store.setWakeLock(wakeLock);
    } catch (err) {
    }
};

export const releaseScreen = async () => {
    const store = useWakeLockStore();
    const wakeLock = store.wakeLock.value;

    if (wakeLock) {
        try {
            await wakeLock.release();
            store.setWakeLock(null);
        } catch (err) {
        }
    }
};
