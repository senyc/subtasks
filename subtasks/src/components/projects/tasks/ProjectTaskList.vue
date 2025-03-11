<template>
  <fwb-table>
    <thead class="font-bold bg-gray-100">
      <tr
        class="flex flex-row text-xs text-gray-700 uppercase dark:bg-gray-700 dark:text-gray-400 bg-gray-100"
      >
        <fwb-table-head-cell class="w-7">
          <fwb-checkbox
            @click="toggleAllChecked"
            :model-value="
              checked.length === data?.tasks.length && checked.length > 0
            "
          />
        </fwb-table-head-cell>
        <fwb-table-head-cell class="grow">Task Name</fwb-table-head-cell>
        <fwb-table-head-cell v-if="completed" class="xl:min-w-52 min-w-36"
          >Date Completed</fwb-table-head-cell
        >
        <fwb-table-head-cell class="xl:min-w-52 min-w-36"
          >Date Due</fwb-table-head-cell
        >
        <fwb-table-head-cell class="xl:min-w-52 min-w-36"
          >Date Added</fwb-table-head-cell
        >
        <fwb-table-head-cell class="min-w-36">
          <span class="sr-only">Edit</span>
        </fwb-table-head-cell>
      </tr>
    </thead>
    <fwb-table-body>
      <ProjectTaskRow
        v-if="data && data.tasks.length > 0"
        :completed="completed"
        :project-id="projectId"
        @toggle-checked="toggleChecked"
        :checkedTasks="checked"
        v-for="task in data.tasks"
        :key="task.id"
        :checked="checked.includes(task.id)"
        :task="task"
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
import { computed, inject } from "vue";
import { getTasks } from "@actions/tasks";
import ProjectTaskRow from "./ProjectTaskRow.vue";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import EmptyRow from "@components/shared/EmptyRow.vue";

const checked = inject<number[]>("checked", []);

const {
  projectId,
  completed = false,
  page,
  pageSize = 20,
  search = "",
} = defineProps<{
  projectId: number;
  completed?: boolean;
  page: number;
  pageSize?: number;
  search: string;
}>();

const { data, isFetched } = useQuery({
  placeholderData: keepPreviousData,
  queryKey: [
    "tasks",
    () => projectId,
    computed(() => (completed ? "completed" : "incompleted")),
    { search: () => search, page: () => page, size: () => pageSize },
  ],
  queryFn: () =>
    getTasks({
      projectId,
      completed,
      page,
      pageSize,
      search,
    }),
});

function toggleAllChecked() {
  if (!data.value) {
    return;
  }

  if (checked.length === data.value.tasks.length) {
    checked.splice(0);
  } else {
    checked.splice(0);
    data.value.tasks.forEach((task) => checked.push(task.id));
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
