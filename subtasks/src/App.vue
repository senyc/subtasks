<template>
  <main>
    <Header />
    <RouterView />
  </main>
</template>

<script setup lang="ts">
import "./index.css";
import Header from "./components/Header.vue";
</script>
