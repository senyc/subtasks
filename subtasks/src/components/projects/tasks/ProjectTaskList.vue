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
        <fwb-table-head-cell class="grow w-1/2">Task Name</fwb-table-head-cell>
        <fwb-table-head-cell v-if="completed" class="xl:min-w-52 min-w-36"
          >Date Completed</fwb-table-head-cell
        >
        <fwb-table-head-cell class="xl:min-w-52 min-w-36"
          >Time Estimate</fwb-table-head-cell
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
      <VueDraggable
        :disabled="disableDraggable"
        @end="onEnd"
        v-if="tasks"
        ref="el"
        v-model="tasks"
      >
        <ProjectTaskRow
          v-if="tasks && tasks.length > 0"
          :completed="completed"
          :project-id="projectId"
          @toggle-checked="toggleChecked"
          v-for="task in tasks"
          :key="task.id"
          :checked="checked.includes(task.id)"
          :task="task"
          @toggle-modal="disableDraggable = !disableDraggable"
        />
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
import { inject, ref, watchEffect } from "vue";
import { useTasks } from "../../../composables/useTasks";
import ProjectTaskRow from "./ProjectTaskRow.vue";
import EmptyRow from "@components/shared/EmptyRow.vue";
import type { Task } from "@annotations/task";
import { useQueryClient } from "@tanstack/vue-query";
import { getInbetweenOrder } from "../../../utils/sorting";

const disableDraggable = ref(false);
const queryClient = useQueryClient();

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

const { data, isFetched } = useTasks({
  projectId: () => projectId,
  completed: () => completed,
  search: () => search,
  page: () => page,
  pageSize: () => pageSize,
});

// Store re-orderable items
const tasks = ref<Task[]>([]);

// Sync query data to local state once fetched
watchEffect(() => {
  if (data.value?.tasks) {
    tasks.value = [...data.value.tasks];
  }
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

async function onEnd(event: SortableEvent) {
  const newIndex = event.newIndex;
  const newOrder = getInbetweenOrder(newIndex, tasks.value);
  if (newOrder == undefined || newIndex == undefined) {
    return;
  }

  const task = tasks.value[newIndex];

  // Update the in-place value
  tasks.value[newIndex].order = newOrder;

  const res = await fetch(`http://localhost:8000/task/${task.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ order: newOrder }),
  });
  if (res.ok)
    queryClient.invalidateQueries({
      queryKey: [
        "tasks",
        () => projectId,
        () => (completed ? "completed" : "incompleted"),
      ],
    });
}

function toggleChecked(id: number) {
  if (checked.includes(id)) {
    checked.splice(checked.indexOf(id), 1);
  } else {
    checked.push(id);
  }
}
</script>
