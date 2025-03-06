<template>
  <fwb-table-row class="my-3 border-b-gray-200">
    <fwb-table-cell>
      <fwb-checkbox @click="$emit('toggleChecked', task.id)" :model-value="checked" />
    </fwb-table-cell>
    <fwb-table-cell class="flex overflow-ellipsis line-clamp-1 flex-col">
      <h3 class="text-lg font-bold">
        {{ task.title }}
      </h3>
      <p>
        {{ task.body }}
      </p>
    </fwb-table-cell>
    <fwb-table-cell v-if="completed">{{ reprDate(task.completed_date) }}</fwb-table-cell>
    <fwb-table-cell>{{ reprDate(task.due_date) }}</fwb-table-cell>
    <fwb-table-cell>{{ reprDate(task.created_at) }}</fwb-table-cell>
    <fwb-table-cell>
      <EditTask :project-id="projectId" :task=task />
    </fwb-table-cell>
  </fwb-table-row>
</template>

<script setup lang="ts">
import {
  FwbTableCell,
  FwbTableRow,
  FwbCheckbox,
} from 'flowbite-vue'
import type Task from '@annotations/task';
import EditTask from '../../EditTask.vue';
import { reprDate } from '../../../utils/date';

withDefaults(defineProps<{
  task: Task
  checked: boolean
  projectId: number
  completed?: boolean
}>(), {
  completed: false
})

</script>
