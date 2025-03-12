<template>
  <fwb-table hoverable>
    <thead class="bg-gray-100">
      <tr
        class="flex flex-row text-xs text-gray-700 uppercase dark:bg-gray-700 dark:text-gray-400 bg-gray-100"
      >
        <fwb-table-head-cell class="w-7">
          <fwb-checkbox
            @click="toggleAllChecked"
            :model-value="
              checked.length === projects?.length && checked.length > 0
            "
          />
        </fwb-table-head-cell>
        <fwb-table-head-cell class="grow xl:min-w-52 min-w-36">
          Project Name</fwb-table-head-cell
        >
        <fwb-table-head-cell v-if="completed" class="xl:min-w-52 min-w-36"
          >Date Completed</fwb-table-head-cell
        >
        <fwb-table-head-cell class="xl:min-w-52 min-w-36"
          >Date Due</fwb-table-head-cell
        >
        <fwb-table-head-cell class="xl:min-w-52 min-w-36"
          >Tasks Remaining</fwb-table-head-cell
        >
        <fwb-table-head-cell class="xl:min-w-52 min-w-36"
          >Tasks Total</fwb-table-head-cell
        >
        <fwb-table-head-cell class="xl:min-w-52 min-w-36"
          >Tasks Complete</fwb-table-head-cell
        >
        <fwb-table-head-cell class="min-w-36">
          <span class="sr-only">Edit</span>
        </fwb-table-head-cell>
      </tr>
    </thead>
    <fwb-table-body>
      <ProjectRow
        v-if="data && data.projects.length > 0"
        :completed="completed"
        @toggle-checked="toggleChecked"
        v-for="project in data?.projects"
        :key="project.id"
        :checked="checked.includes(project.id)"
        :project="project"
      />
      <EmptyRow v-else-if="isFetched" />
    </fwb-table-body>
  </fwb-table>
</template>

<script setup lang="ts">
import {
  FwbTable,
  FwbCheckbox,
  FwbTableBody,
  FwbTableHeadCell,
} from "flowbite-vue";
import ProjectRow from "./ProjectRow.vue";
import { computed, inject } from "vue";

// Inject api used here because we would like the parent component to know about what is checked to perform
// mutations/deletions on the checked items (via the bar items)
let checked = inject<number[]>("checked", []);
import { getProjects } from "@actions/projects";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import EmptyRow from "@components/shared/EmptyRow.vue";

const {
  completed = false,
  page,
  pageSize = 20,
  search = "",
} = defineProps<{
  completed?: boolean;
  page: number;
  pageSize?: number;
  search?: string;
}>();

const { data, isFetched } = useQuery({
  placeholderData: keepPreviousData,
  queryKey: [
    "projects",
    computed(() => (completed ? "completed" : "incomplete")),
    { search: () => search, page: () => page, size: () => pageSize },
  ],
  queryFn: () =>
    getProjects({
      pageSize,
      page,
      completed,
      search,
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
