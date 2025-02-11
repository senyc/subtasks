<template>
  <div class="px-8">
  <ProjectBreadCrumbs />
  <ProjectNavigation />
  <ProjectList />
  </div>
</template>

<script setup lang="ts">
import { provide, reactive } from 'vue';
import ProjectBreadCrumbs from '../components/ProjectBreadCrumbs.vue';
import ProjectList from '../components/ProjectList.vue';
import ProjectNavigation from '../components/ProjectNavigation.vue';
const checkedProjects = reactive<number[]>([])
provide<number[]>('checked', checkedProjects)
</script>
