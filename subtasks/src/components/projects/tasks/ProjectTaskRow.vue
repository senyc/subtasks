<template>
  <fwb-table-row class="border-b-gray-200 flex flex-row">
    <fwb-table-cell class="!mt-2 w-7">
      <fwb-checkbox
        @click="$emit('toggleChecked', task.id)"
        :model-value="checked"
      />
    </fwb-table-cell>
    <fwb-table-cell class="grow xl:min-w-52 min-w-36">
      <h3 class="text-lg font-bold line-clamp-2 overflow-ellipsis">
        {{ task.title }}
      </h3>
      <p class="overflow-ellipsis line-clamp-1">
        {{ task.body }}
      </p>
    </fwb-table-cell>
    <fwb-table-cell class="xl:min-w-52 min-w-36" v-if="completed">{{
      reprDate(task.completed_date)
    }}</fwb-table-cell>
    <fwb-table-cell
      class="xl:min-w-52 min-w-36"
      :class="{
        'text-red-500': dateHasElapsed(new Date(task.due_date as string)),
      }"
      >{{ reprDate(task.due_date) }}</fwb-table-cell
    >
    <fwb-table-cell class="xl:min-w-52 min-w-36">{{
      reprDate(task.created_at)
    }}</fwb-table-cell>
    <fwb-table-cell class="min-w-36">
      <EditTask :project-id="projectId" :task="task" />
    </fwb-table-cell>
  </fwb-table-row>
</template>

<script setup lang="ts">
import { FwbTableCell, FwbTableRow, FwbCheckbox } from "flowbite-vue";
import type Task from "@annotations/task";
import EditTask from "../../EditTask.vue";
import { reprDate, dateHasElapsed } from "../../../utils/date";

withDefaults(
  defineProps<{
    task: Task;
    checked: boolean;
    projectId: number;
    completed?: boolean;
  }>(),
  {
    completed: false,
  },
);
</script>
