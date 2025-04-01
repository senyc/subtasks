<template>
  <form
    @submit.prevent="$emit('onSubmit')"
    class="flex flex-col gap-2 text-left"
  >
    <fwb-input
      placeholder="Task Title"
      v-model="task.title"
      label="Task Title"
      ref="titleRef"
    />
    <fwb-select
      v-model="task.time_estimate as string"
      :options="timeEstimateOptions"
      label="Time Estimate"
    />
    <fwb-textarea
      @keydown.ctrl.enter="$emit('onSubmit')"
      v-model="task.body"
      :rows="4"
      label="Task Body"
      placeholder="Task Body"
    />
    <fwb-input type="date" v-model="task.due_date" label="Due Date" />
    <fwb-select
      v-model="task.project_id as string"
      :options="
        data?.map((project) => {
          return { name: project.title, value: project.id.toString() };
        })
      "
      label="Select a Project"
    />
  </form>
</template>

<script lang="ts" setup>
// @ts-nocheck
import type { Project } from "@annotations/project";
import type Task from "@annotations/task";
import { useQuery } from "@tanstack/vue-query";
import { FwbInput, FwbTextarea, FwbSelect } from "flowbite-vue";
import {
  nextTick,
  useTemplateRef,
  onMounted,
  onBeforeUnmount,
  onBeforeMount,
} from "vue";

type PartialTask = Omit<Task, "id" | "order">;

const titleRef = useTemplateRef("titleRef");

const timeEstimateOptions = [
  { value: 15, name: "15m" },
  { value: 30, name: "30m" },
  { value: 45, name: "45m" },
  { value: 60, name: "1h" },
  { value: 90, name: "1.5h" },
  { value: 120, name: "2h" },
  { value: 180, name: "3h" },
];
const { data } = useQuery({
  queryKey: ["projects", "all"],
  queryFn: async (): Promise<Project[]> => {
    const res = await fetch("http://localhost:8000/projects/all");
    if (!res.ok) {
      throw "Failure getting tasks";
    }
    return res.json();
  },
});

onBeforeUnmount(() => {
  window.onbeforeunload = null;
});

onBeforeMount(() => {
  window.onbeforeunload = () => true;
});

onMounted(() => {
  nextTick(() => {
    // Gets the underlying input element within the flowbite component
    const inputElement = titleRef.value?.$el.querySelector(
      "input",
    ) as HTMLInputElement;
    if (inputElement) {
      inputElement.focus();
    }
  });
});

defineProps<{
  task: PartialTask;
}>();
</script>
