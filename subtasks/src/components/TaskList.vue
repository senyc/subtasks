<template>
  <fwb-table>
    <fwb-table-head class="bg-gray-100">
      <fwb-table-head-cell class="w-5">
        <fwb-checkbox @click="toggleAllChecked" :model-value="checkedTasks.length === tasks?.length" />
      </fwb-table-head-cell>
      <fwb-table-head-cell class="w-4/6">Task Name</fwb-table-head-cell>
      <fwb-table-head-cell class="w-1/6">Date Due</fwb-table-head-cell>
      <fwb-table-head-cell class="w-1/6">Date Added</fwb-table-head-cell>
      <fwb-table-head-cell>
        <span class="sr-only">Edit</span>
      </fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body>
      <TaskRow :project-id="projectId" @toggle-checked="toggleChecked" :checkedTasks="checkedTasks"
        v-for="task in tasks" :key="task.id" :checked="checkedTasks.includes(task.id)" :task="task" />
    </fwb-table-body>
  </fwb-table>
</template>

<script setup lang="ts">
import {
  FwbTable,
  FwbCheckbox,
  FwbTableBody,
  FwbTableHead,
  FwbTableHeadCell,
} from 'flowbite-vue'
import { inject } from 'vue'
import useTasks from '../actions/tasks'
import TaskRow from './TaskRow.vue';

let checkedTasks = inject<number[]>('checked', [])

const props = defineProps<{
  projectId: number
}>()
const { data: tasks } = useTasks(props.projectId)

function toggleAllChecked() {
  if (!tasks.value) {
    return
  }

  if (checkedTasks.length === tasks.value.length) {
    checkedTasks.splice(0);
  } else {
    checkedTasks.splice(0);
    tasks.value.forEach(task => checkedTasks.push(task.id));
  }
}

function toggleChecked(id: number) {
  if (checkedTasks.includes(id)) {
    checkedTasks.splice(checkedTasks.indexOf(id), 1)
  } else {
    checkedTasks.push(id)
  }
}
</script>
