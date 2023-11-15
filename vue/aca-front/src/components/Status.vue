<template>
  <div>
    <h1>
      Status: <span :class="{ 'online': serverStatus === 'ONLINE', 'offline': serverStatus === 'OFFLINE' }"> {{ serverStatus }} </span>
    </h1>
    <v-divider class="with-margin"></v-divider>
    <h1>Doors: <span :class="{ 'open': doorStatus === 'OPEN', 'closed': doorStatus === 'CLOSED' }"> {{ doorStatus }} </span></h1>
    <v-divider class="with-margin"></v-divider>
    <h1>Current open door policies: </h1>
    <v-table class="with-margin">
        <thead>
            <tr>
                <th class="text-left">Day</th>
                <th class="text-left">Start</th>
                <th class="text-left">End</th>
                <th class="text-left">Status</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in policies" :key="item.id">
                <td>{{ item.day }}</td>
                <td>{{ item.start }}</td>
                <td>{{ item.end }}</td>
                <td>{{ item.active }}</td>
            </tr>
        </tbody>
    </v-table>
  </div>
</template>

<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { redirectToCallingOnOngoingCall, getServerStatus, getDoorStatus, fetchPoliciesData } from '../api/api.js'
    import { releaseScreen } from '../api/wakeup.js';

    const serverStatus = ref("Loading...");
    const doorStatus = ref("Loading...");

    const pollInterval = 500;
    const router = useRouter();
    let pollTimer;
    let refreshStatusTimer;

    const policies = ref([]);

    onMounted(async () => {
      releaseScreen();
      pollTimer = setInterval(async () => redirectToCallingOnOngoingCall(router), pollInterval);
      refreshStatusTimer = setInterval(
          async () => {
                 policies.value = await fetchPoliciesData();
                 serverStatus.value = await getServerStatus();
                 doorStatus.value = await getDoorStatus();
              },
              pollInterval
          );
    });

    onBeforeUnmount(() => {
      clearInterval(pollTimer);
      clearInterval(refreshStatusTimer);
    });
</script>

<style scoped>
    .online {
      color: green;
    }

    .offline {
      color: red;
    }

    .open {
      color: green;
    }

    .closed {
      color: red;
    }

    .with-margin {
      margin-right: 20px;
    }
</style>
