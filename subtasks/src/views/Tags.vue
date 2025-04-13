<template>
  <Header active="tasks" />
  <div class="px-8">
    <TagsBreadCrumbs />
    <TagList type="tasks" />
  </div>
</template>

<script setup lang="ts">
import Header from "@components/Header.vue";
import TagList from "@components/tags/TagList.vue";
import TagsBreadCrumbs from "@components/tags/TagsBreadCrumbs.vue";
</script>
