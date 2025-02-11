<template>
  <div class="px-8">
    <ProjectBreadCrumbs />
    <ProjectTaskNavigation :project-id="projectId" />
    <TaskList :project-id="projectId" />
  </div>
</template>

<script setup lang="ts">
import { provide, reactive } from 'vue'
import TaskList from '../components/TaskList.vue';

import { useRoute } from 'vue-router'
import ProjectBreadCrumbs from '../components/ProjectBreadCrumbs.vue';
import ProjectTaskNavigation from '../components/ProjectTaskNavigation.vue';

const route = useRoute()
const projectId = parseInt(route.params.id as string)

const checkedTasks = reactive<number[]>([])
provide<number[]>('checked', checkedTasks)

</script>
