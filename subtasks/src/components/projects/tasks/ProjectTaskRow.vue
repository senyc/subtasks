<template>
  <fwb-table-row class="border-b-gray-200 flex flex-row">
    <fwb-table-cell
      @click="$emit('toggleChecked', task.id)"
      class="!mt-2 w-7"
    >
      <fwb-checkbox :model-value="checked" />
    </fwb-table-cell>
    <fwb-table-cell
      class="grow xl:min-w-52 min-w-36"
      @click="handleClick"
      @dblclick="handleDoubleClick"
    >
      <h3 class="text-lg font-bold line-clamp-2 overflow-ellipsis">
        {{ task.title }}
      </h3>
      <p class="overflow-ellipsis line-clamp-1">
        {{ task.body }}
      </p>
    </fwb-table-cell>
    <fwb-table-cell
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="xl:min-w-52 min-w-36"
      v-if="completed"
      >{{ reprDate(task.completed_date) }}</fwb-table-cell
    >
    <fwb-table-cell
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="xl:min-w-52 min-w-36"
      >{{ timeEstimate }}</fwb-table-cell
    >
    <fwb-table-cell
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="xl:min-w-52 min-w-36"
      :class="{
        'text-red-500':
          !completed && dateHasElapsed(new Date(task.due_date as string)),
      }"
      >{{ reprDate(task.due_date) }}
    </fwb-table-cell>
    <fwb-table-cell
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="xl:min-w-52 min-w-36"
      >{{ reprDate(task.created_at) }}</fwb-table-cell
    >
    <fwb-table-cell class="w-42">
      <EditTask @click="showModal = true" />
    </fwb-table-cell>
  </fwb-table-row>
  <EditTaskModal
    @close="showModal = false"
    :task="task"
    :project-id="projectId"
    :show-modal="showModal"
  />
</template>

<script setup lang="ts">
import { FwbTableCell, FwbTableRow, FwbCheckbox } from "flowbite-vue";
import type Task from "@annotations/task";
import EditTask from "../../EditTask.vue";
import { reprDate, dateHasElapsed } from "../../../utils/date";
import { computed, onUnmounted, ref } from "vue";
import EditTaskModal from "../../EditTaskModal.vue";

const showModal = ref(false);

const emit = defineEmits<{
  (e: "toggleChecked", id: number): void;
}>();

const props = withDefaults(
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

const clickTimeout = ref<number | null>(null);

const handleClick = () => {
  if (clickTimeout.value) {
    clearTimeout(clickTimeout.value);
    clickTimeout.value = null;
    return;
  }

  clickTimeout.value = setTimeout(() => {
    emit("toggleChecked", props.task.id);
    clickTimeout.value = null;
  }, 230);
};

const handleDoubleClick = () => {
  clickTimeout.value && clearTimeout(clickTimeout.value);
  clickTimeout.value = null;
  showModal.value = true;
};

// Cleanup timeout when the component is unmounted
onUnmounted(() => {
  if (clickTimeout.value) {
    clearTimeout(clickTimeout.value);
  }
});
const timeEstimate = computed(() => {
  const time = props.task?.time_estimate || 0;
  if (!time) {
    return "";
  }
  return (time < 60 ? time : time / 60) + (time < 60 ? "m" : "h");
});
</script>
