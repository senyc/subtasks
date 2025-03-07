<template>
  <fwb-table hoverable>
    <fwb-table-head class="bg-gray-100">
      <fwb-table-head-cell class="w-5">
        <fwb-checkbox @click="toggleAllChecked"
          :model-value="checkedProjects.length === projects?.length && checkedProjects.length > 0" />
      </fwb-table-head-cell>
      <fwb-table-head-cell class="w-5/10">Project
        Name</fwb-table-head-cell>
      <fwb-table-head-cell v-if="!completed" class="w-1/10">Date Due</fwb-table-head-cell>
      <fwb-table-head-cell v-else class="w-1/10">Date Completed</fwb-table-head-cell>
      <fwb-table-head-cell class="w-1/10">Tasks Remaining</fwb-table-head-cell>
      <fwb-table-head-cell class="w-1/10">Tasks Total</fwb-table-head-cell>
      <fwb-table-head-cell class="w-1/10">Tasks Complete</fwb-table-head-cell>
      <fwb-table-head-cell>
        <span class="sr-only">Edit</span>
      </fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body>
      <ProjectRow :completed="completed" :toggle-checked="toggleChecked" :checked-projects="checkedProjects"
        v-for="project in projects" :key="project.id" :checked="checkedProjects.includes(project.id)"
        :project="project" />
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
import ProjectRow from "./ProjectRow.vue";
import { inject } from 'vue';


// Inject api used here because we would like the parent component to know about what is checked to perform 
// mutations/deletions on the checked items (via the bar items)
let checkedProjects = inject<number[]>('checked', [])
import useProjects from '@actions/projects'

const props = withDefaults(defineProps<{
  completed?: boolean
}>(),
  { completed: false })

const { data: projects } = useProjects({ completed: props.completed })

function toggleAllChecked() {
  if (!projects.value) {
    return
  }

  if (checkedProjects.length === projects.value.length) {
    checkedProjects.splice(0);
  } else {
    checkedProjects.splice(0); // Clear the array reactively
    projects.value.forEach(project => checkedProjects.push(project.id)); // Add all project ids
  }
}

function toggleChecked(id: number) {
  if (checkedProjects.includes(id)) {
    checkedProjects.splice(checkedProjects.indexOf(id), 1)
  } else {
    checkedProjects.push(id)
  }
}
</script>
