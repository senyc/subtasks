<template>
  <fwb-modal size="4xl" @close="$emit('close')">
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
import ProjectTaskForm from "./ProjectTaskForm.vue";
const queryClient = useQueryClient();
import type { Task, TaskDisplay } from "@annotations/task";
import { Delta } from "@vueup/vue-quill";
const props = defineProps<{
  task: Task;
  projectId?: number;
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
    body: JSON.stringify({
      ...task,
      due_date: task.due_date ? task.due_date : undefined,
      body: JSON.stringify(task.body),
    }),
  });
  if (res.ok) {
    emit("close");
    queryClient.invalidateQueries({ queryKey: ["tasks"] });
  }
}

const task = reactive<TaskDisplay>({
  title: props.task.title,
  body: (() => {
    try {
      return new Delta(JSON.parse(props.task.body));
    } catch {
      return new Delta();
    }
  })(),
  due_date: props.task.due_date
    ? new Date(props.task.due_date).toISOString().split("T")[0]
    : "",
  project_id: props.task.project_id,
  time_estimate: props.task.time_estimate,
  tags: props.task.tags,
});
</script>
