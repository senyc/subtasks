<template>
  <fwb-table>
    <fwb-table-head class="bg-gray-100">
      <fwb-table-head-cell class="w-5">
        <fwb-checkbox
          @click="toggleAllChecked"
          :model-value="checkedTasks.length === tasks?.length"
        />
      </fwb-table-head-cell>
      <fwb-table-head-cell :class="{ 'w-3/6': completed, 'w-4/6': !completed }"
        >Task Name</fwb-table-head-cell
      >
      <fwb-table-head-cell v-if="completed" class="w-1/6"
        >Date Completed</fwb-table-head-cell
      >
      <fwb-table-head-cell class="w-1/6">Date Due</fwb-table-head-cell>
      <fwb-table-head-cell class="w-1/6">Date Added</fwb-table-head-cell>
      <fwb-table-head-cell>
        <span class="sr-only">Edit</span>
      </fwb-table-head-cell>
    </fwb-table-head>
    <fwb-table-body>
      <ProjectTaskRow
        :completed="completed"
        :project-id="projectId"
        @toggle-checked="toggleChecked"
        :checkedTasks="checkedTasks"
        v-for="task in tasks"
        :key="task.id"
        :checked="checkedTasks.includes(task.id)"
        :task="task"
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
import { computed, inject } from "vue";
import { getTasks } from "@actions/tasks";
import ProjectTaskRow from "./ProjectTaskRow.vue";
import { useQuery } from "@tanstack/vue-query";

let checkedTasks = inject<number[]>("checked", []);

const props = withDefaults(
  defineProps<{
    projectId: number;
    completed?: boolean;
    page: number;
    pageSize?: number;
  }>(),
  { completed: false, pageSize: 20 },
);

const { data: tasks } = useQuery({
  queryKey: computed(() => [
    "tasks",
    props.projectId,
    props.completed ? "completed" : "incompleted",
    { page: props.page, size: props.pageSize },
  ]),
  queryFn: () =>
    getTasks({
      projectId: props.projectId,
      completed: props.completed,
      page: props.page,
      pageSize: props.pageSize,
    }),
});

function toggleAllChecked() {
  if (!tasks.value) {
    return;
  }

  if (checkedTasks.length === tasks.value.length) {
    checkedTasks.splice(0);
  } else {
    checkedTasks.splice(0);
    tasks.value.forEach((task) => checkedTasks.push(task.id));
  }
}

function toggleChecked(id: number) {
  if (checkedTasks.includes(id)) {
    checkedTasks.splice(checkedTasks.indexOf(id), 1);
  } else {
    checkedTasks.push(id);
  }
}
</script>
