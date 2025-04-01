<template>
  <fwb-modal v-if="showModal" @close="$emit('close')">
    <template #header>
      <div
        class="ml-2 border-none text-left line-clamp-1 overflow-ellipsis text-lg"
      >
        Edit: {{ props.task.title }}
      </div>
    </template>
    <template #body>
      <ProjectTaskForm :task="task" @on-submit="onSubmit" />
    </template>
    <template #footer>
      <div class="flex justify-between">
        <fwb-button @click="$emit('close')" color="alternative">
          Cancel
        </fwb-button>
        <fwb-button @click="onSubmit" color="green"> Save </fwb-button>
      </div>
    </template>
  </fwb-modal>
</template>
<script setup lang="ts">
import { useQueryClient } from "@tanstack/vue-query";
import { reactive } from "vue";
import { FwbButton, FwbModal } from "flowbite-vue";
import ProjectTaskForm from "./projects/tasks/ProjectTaskForm.vue";
const queryClient = useQueryClient();
import type Task from "@annotations/task";
const props = defineProps<{
  task: Task;
  projectId: number;
  showModal: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

async function onSubmit() {
  const res = await fetch(`http://localhost:8000/task/${props.task.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(task),
  });
  if (res.ok) {
    emit("close");
    queryClient.invalidateQueries({ queryKey: ["tasks", props.projectId] });
  }
}
const task = reactive<Omit<Task, "id" | "order">>({
  title: props.task.title,
  body: props.task.body,
  due_date: props.task.due_date
    ? new Date(props.task.due_date).toISOString().split("T")[0]
    : "",
  project_id: props.task.project_id,
  time_estimate: props.task.time_estimate,
});
</script>
