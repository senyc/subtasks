<template>
  <fwb-table-row class="border-b-gray-200 flex flex-row">
    <fwb-table-cell class="w-7">
      <fwb-checkbox class="mt-2"
        @click="$emit('toggleChecked', project.id)"
        :model-value="checked"
      />
    </fwb-table-cell>
    <fwb-table-cell
      class="grow min-w-52"
      @click="$router.push(`/projects/${project.id}/tasks`)"
    >
      <h3 class="text-lg font-bold line-clamp-2 overflow-ellipsis">
        {{ project.title }}
      </h3>
      <p class="overflow-ellipsis line-clamp-1">
        {{ project.body }}
      </p>
    </fwb-table-cell>
    <fwb-table-cell
      v-if="completed"
      class="cursor-pointer xl:min-w-52 min-w-36"
      @click="$router.push(`/projects/${project.id}/tasks`)"
      >{{ reprDate(project.completed_date) }}
    </fwb-table-cell>
    <fwb-table-cell
      class="xl:min-w-52 min-w-36 cursor-pointer"
      :class="{
        'text-red-500':
          !completed && dateHasElapsed(new Date(project.due_date as string)),
      }"
      @click="$router.push(`/projects/${project.id}/tasks`)"
      >{{ reprDate(project.due_date) }}</fwb-table-cell
    >
    <fwb-table-cell
      class="cursor-pointer xl:min-w-52 min-w-36"
      @click="$router.push(`/projects/${project.id}/tasks`)"
      >{{ project.total_tasks - project.completed_tasks || 0 }}
    </fwb-table-cell>
    <fwb-table-cell
      class="cursor-pointer xl:min-w-52 min-w-36"
      @click="$router.push(`/projects/${project.id}/tasks`)"
      >{{ project.total_tasks }}</fwb-table-cell
    >
    <fwb-table-cell
      class="cursor-pointer xl:min-w-52 min-w-36"
      @click="$router.push(`/projects/${project.id}/tasks`)"
      >{{ project.completed_tasks }}</fwb-table-cell
    >
    <fwb-table-cell class="min-w-36">
      <EditProject :project="project" />
    </fwb-table-cell>
  </fwb-table-row>
</template>

<script setup lang="ts">
import { FwbTableCell, FwbTableRow, FwbCheckbox } from "flowbite-vue";
import EditProject from "./EditProject.vue";
import type { ProjectResponse } from "@annotations/project";
import { reprDate, dateHasElapsed } from "../../utils/date";

defineEmits(["toggleChecked"]);

withDefaults(
  defineProps<{
    project: ProjectResponse;
    checked: boolean;
    completed?: boolean;
  }>(),
  {
    completed: false,
  },
);
</script>
