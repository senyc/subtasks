<template>
  <div class="px-8">
    <ProjectBreadCrumbs completed/>
    <ProjectNavigation completed />
    <ProjectList />
  </div>
</template>

<script setup lang="ts">
import { provide, reactive } from 'vue';
import ProjectBreadCrumbs from '@components/projects/ProjectBreadCrumbs.vue';
import ProjectList from '@components/projects/completed/ProjectList.vue';
import ProjectNavigation from '@components/projects/ProjectNavigation.vue';
const checkedProjects = reactive<number[]>([])
provide<number[]>('checked', checkedProjects)
</script>
