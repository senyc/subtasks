<template>
  <fwb-table hoverable>
    <fwb-table-head class="bg-gray-100">
      <fwb-table-head-cell class="w-5">
        <fwb-checkbox
          @click="toggleAllChecked"
          :model-value="
            checked.length === projects?.length && checked.length > 0
          "
        />
      </fwb-table-head-cell>
      <fwb-table-head-cell class="w-5/10"> Project Name</fwb-table-head-cell>
      <fwb-table-head-cell v-if="!completed" class="w-1/10"
        >Date Due</fwb-table-head-cell
      >
      <fwb-table-head-cell v-else class="w-1/10"
        >Date Completed</fwb-table-head-cell
      >
      <fwb-table-head-cell class="w-1/10">Tasks Remaining</fwb-table-head-cell>
      <fwb-table-head-cell class="w-1/10">Tasks Total</fwb-table-head-cell>
      <fwb-table-head-cell class="w-1/10">Tasks Complete</fwb-table-head-cell>
      <fwb-table-head-cell>
        <span class="sr-only">Edit</span>
      </fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body>
      <ProjectRow
        :completed="completed"
        @toggle-checked="toggleChecked"
        v-for="project in data?.projects"
        :key="project.id"
        :checked="checked.includes(project.id)"
        :project="project"
      />
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
} from "flowbite-vue";
import ProjectRow from "./ProjectRow.vue";
import { computed, inject } from "vue";

// Inject api used here because we would like the parent component to know about what is checked to perform
// mutations/deletions on the checked items (via the bar items)
let checked = inject<number[]>("checked", []);
import { getProjects } from "@actions/projects";
import { useQuery } from "@tanstack/vue-query";

const props = withDefaults(
  defineProps<{
    completed?: boolean;
    page: number;
    pageSize?: number;
  }>(),
  { completed: false, pageSize: 20 },
);

const { data } = useQuery({
  queryKey: [
    "projects",
    computed(() => (props.completed ? "completed" : "incomplete")),
    { page: () => props.page, size: () => props.pageSize },
  ],
  queryFn: () =>
    getProjects({
      pageSize: props.pageSize,
      page: props.page,
      completed: props.completed,
    }),
});

const projects = data.value?.projects;

function toggleAllChecked() {
  if (!projects) {
    return;
  }

  if (checked.length === projects.length) {
    checked.splice(0);
  } else {
    checked.splice(0); // Clear the array reactively
    projects.forEach((project) => checked.push(project.id)); // Add all project ids
  }
}

function toggleChecked(id: number) {
  if (checked.includes(id)) {
    checked.splice(checked.indexOf(id), 1);
  } else {
    checked.push(id);
  }
}
</script>
