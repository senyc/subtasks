<template>
  <div class="px-8">
    <ProjectBreadCrumbs show-project-name />
    <ProjectTaskNavigation :project-id="projectId" />
    <ProjectTaskList :project-id="projectId" />
  </div>
</template>

<script setup lang="ts">
import { provide, reactive } from 'vue'
import { useRoute } from 'vue-router'
import ProjectTaskList from '@components/projects/tasks/ProjectTaskList.vue';

import ProjectBreadCrumbs from '@components/projects/ProjectBreadCrumbs.vue';
import ProjectTaskNavigation from '@components/projects/ProjectTaskNavigation.vue';

const route = useRoute()
const projectId = parseInt(route.params.id as string)

const checkedTasks = reactive<number[]>([])
provide<number[]>('checked', checkedTasks)

</script>
