<template>
  <fwb-table-row class="my-3 border-b-gray-200">
    <fwb-table-cell>
      <fwb-checkbox @click="$emit('toggleChecked', project.id)" :model-value="checked" />
    </fwb-table-cell>
    <fwb-table-cell @click="$router.push(`/projects/${project.id}/tasks`)"
      class="cursor-pointer flex overflow-ellipsis line-clamp-1 flex-col">
      <h3 class="text-lg font-bold">
        {{ project.title }}
      </h3>
      <p>
        {{ project.body }}
      </p>
    </fwb-table-cell>
    <fwb-table-cell v-if="!completed" class="cursor-pointer" @click="$router.push(`/projects/${project.id}/tasks`)">{{
      reprDate(project.due_date) }}</fwb-table-cell>
    <fwb-table-cell v-else class="cursor-pointer" @click="$router.push(`/projects/${project.id}/tasks`)">{{
      reprDate(project.completed_date) }}</fwb-table-cell>
    <fwb-table-cell class="cursor-pointer" @click="$router.push(`/projects/${project.id}/tasks`)">{{
      (project.total_tasks - project.completed_tasks) || 0 }} </fwb-table-cell>
    <fwb-table-cell class="cursor-pointer" @click="$router.push(`/projects/${project.id}/tasks`)">{{ project.total_tasks
      }}</fwb-table-cell>
    <fwb-table-cell class="cursor-pointer" @click="$router.push(`/projects/${project.id}/tasks`)">{{
      project.completed_tasks }}</fwb-table-cell>
    <fwb-table-cell>
      <EditProject :project=project />
    </fwb-table-cell>
  </fwb-table-row>
</template>

<script setup lang="ts">
import {
  FwbTableCell,
  FwbTableRow,
  FwbCheckbox,
} from 'flowbite-vue'
import EditProject from './EditProject.vue';
import type { ProjectResponse } from '@annotations/project';
import { reprDate } from '../../utils/date';

withDefaults(defineProps<{
  project: ProjectResponse
  checked: boolean
  completed?: boolean
}>(), {
  completed: false,
})

</script>
