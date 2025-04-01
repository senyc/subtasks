<template>
  <fwb-table hoverable>
    <thead class="bg-gray-100">
      <tr class="flex flex-row text-xs text-gray-700 uppercase dark:bg-gray-700 dark:text-gray-400 bg-gray-100">
        <fwb-table-head-cell class="w-7">
          <fwb-checkbox @click="toggleAllChecked" :model-value="checked.length === projects?.length && checked.length > 0
            " />
        </fwb-table-head-cell>
        <fwb-table-head-cell class="grow xl:min-w-52 min-w-36"> Project Name</fwb-table-head-cell>
        <fwb-table-head-cell v-if="completed" class="xl:min-w-52 min-w-36">Date Completed</fwb-table-head-cell>
        <fwb-table-head-cell class="xl:min-w-52 min-w-36">Date Due</fwb-table-head-cell>
        <fwb-table-head-cell class="xl:min-w-52 min-w-36">Tasks Remaining</fwb-table-head-cell>
        <fwb-table-head-cell class="xl:min-w-52 min-w-36">Tasks Total</fwb-table-head-cell>
        <fwb-table-head-cell class="xl:min-w-52 min-w-36">Tasks Complete</fwb-table-head-cell>
        <fwb-table-head-cell class="min-w-36">
          <span class="sr-only">Edit</span>
        </fwb-table-head-cell>
      </tr>
    </thead>
    <fwb-table-body>
      <VueDraggable @end="onEnd" v-if="projects" ref="el" v-model="projects">
        <ProjectRow v-if="projects.length > 0" :completed="completed" @toggle-checked="toggleChecked"
          v-for="project in projects" :key="project.id" :checked="checked.includes(project.id)" :project="project" />
        <EmptyRow v-else-if="isFetched" />
      </VueDraggable>
    </fwb-table-body>
  </fwb-table>
</template>

<script setup lang="ts">
import { VueDraggable, type SortableEvent } from "vue-draggable-plus";
import {
  FwbTable,
  FwbCheckbox,
  FwbTableBody,
  FwbTableHeadCell,
} from "flowbite-vue";
import ProjectRow from "./ProjectRow.vue";
import { inject, ref, watchEffect } from "vue";

// Inject api used here because we would like the parent component to know about what is checked to perform
// mutations/deletions on the checked items (via the bar items)
let checked = inject<number[]>("checked", []);
import { useProjects } from "../../composables/useProjects";
import EmptyRow from "@components/shared/EmptyRow.vue";
import type { ProjectResponse } from "@annotations/project";

import { useQueryClient } from "@tanstack/vue-query";
import { getInbetweenOrder } from "../../utils/sorting";

const queryClient = useQueryClient();
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

const { data, isFetched } = useProjects({
  completed: () => completed,
  search: () => search,
  page: () => page,
  pageSize: () => pageSize,
});

// Store re-orderable items
const projects = ref<ProjectResponse[]>([]);

// Sync query data to local state once fetched
watchEffect(() => {
  if (data.value?.projects) {
    projects.value = [...data.value.projects];
  }
});

async function onEnd(event: SortableEvent) {
  const newIndex = event.newIndex;
  const newOrder = getInbetweenOrder(newIndex, projects.value);
  if (newOrder == undefined || newIndex == undefined) {
    return;
  }

  const project = projects.value[newIndex];

  // Update the in-place value
  projects.value[newIndex].order = newOrder;

  const res = await fetch(`http://localhost:8000/project/${project.id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ order: newOrder }),
  });
  if (res.ok) queryClient.invalidateQueries({ queryKey: ["projects"] });
}

function toggleAllChecked() {
  if (!projects) {
    return;
  }

  if (checked.length === projects.value.length) {
    checked.splice(0);
  } else {
    checked.splice(0); // Clear the array reactively
    projects.value.forEach((project) => checked.push(project.id)); // Add all project ids
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
