<template>
  <main>
    <RouterView />
    <Toast position="bottom-center" />
  </main>
</template>

<script setup lang="ts">
import "./index.css";
import "primeicons/primeicons.css";
import Toast from "./volt/Toast.vue";
</script>
