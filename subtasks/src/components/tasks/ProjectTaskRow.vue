<template>
  <fwb-table-row class="border-b-gray-200 flex flex-row">
    <fwb-table-cell @click="$emit('toggleChecked', task.id)" class="!mt-2 w-7">
      <fwb-checkbox :model-value="checked" />
    </fwb-table-cell>
    <fwb-table-cell
      class="grow w-1/2"
      @click="handleClick"
      @dblclick="handleDoubleClick"
    >
      <h3 class="text-lg font-bold line-clamp-2 overflow-ellipsis">
        {{ task.title }}
      </h3>
    </fwb-table-cell>
    <fwb-table-cell class="min-w-36">
      <div class="flex flex-row gap-1">
        <Tag :color="tag.color" v-for="tag in task.tags"
        >{{ tag.name }}
          <template #delete
          ><button @click="() => deleteTag(tag.id!)" class="cursor-pointer">
              &times
            </button></template
          >
        </Tag>
      </div>
    </fwb-table-cell>
    <fwb-table-cell
      v-if="showProjectName"
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="w-64"
      >{{ project?.title }}</fwb-table-cell
    >
    <fwb-table-cell
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="min-w-36"
      v-if="completed"
      >{{ reprDate(task.completed_date) }}</fwb-table-cell
    >
    <fwb-table-cell
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="min-w-36"
      >{{ timeEstimate }}</fwb-table-cell
    >
    <fwb-table-cell
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="min-w-36"
      :class="{
        'text-red-500': !completed && dateHasElapsed(new Date(task.due_date!)),
        'text-yellow-400': !completed && dateIsToday(new Date(task.due_date!)),
      }"
      >{{ reprDate(task.due_date) }}
    </fwb-table-cell>
    <fwb-table-cell
      @click="handleClick"
      @dblclick="handleDoubleClick"
      class="min-w-36"
      >{{ reprDate(task.created_at) }}</fwb-table-cell
    >
    <fwb-table-cell class="min-w-36">
      <EditButton @click="onOpen" />
    </fwb-table-cell>
  </fwb-table-row>
  <EditTaskModal
    v-if="showModal"
    @close="onClose"
    :task="task"
    :project-id="projectId"
  />
</template>

<script setup lang="ts">
import { FwbTableCell, FwbTableRow, FwbCheckbox } from "flowbite-vue";
import type { Task } from "@annotations/task";
import { reprDate, dateHasElapsed, dateIsToday } from "@utils/date";
import { computed, onUnmounted, ref } from "vue";
import EditTaskModal from "./EditTaskModal.vue";
import Tag from "@components/shared/Tag.vue";
import { useQueryClient } from "@tanstack/vue-query";
import useProject from "@composables/useProject";
import EditButton from "@components/shared/EditButton.vue";

const showModal = ref(false);
const queryClient = useQueryClient();

const emit = defineEmits<{
  (e: "toggleChecked", id: number): void;
  (e: "toggleModal"): void;
}>();

function onClose() {
  showModal.value = false;
  emit("toggleModal");
}

function onOpen() {
  showModal.value = true;

  emit("toggleModal");
}

const props = withDefaults(
  defineProps<{
    task: Task;
    checked: boolean;
    projectId: number;
    completed?: boolean;
    showProjectName?: boolean
  }>(),
  {
    completed: false,
    showProjectName: false
  },
);

const { data: project } = useProject({ id: props.projectId, enabled: true });

async function deleteTag(tagId: number) {
  const req = await fetch(`http://localhost:8000/task/${props.task.id}/tags`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(props.task.tags?.filter((tag) => tag.id != tagId)),
  });

  if (req.ok) {
    queryClient.invalidateQueries({
      queryKey: ["tasks"],
    });
  }
}
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
  onOpen();
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
