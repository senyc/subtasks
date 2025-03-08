<template>
  <form
    @submit.prevent="$emit('onSubmit')"
    class="flex flex-col gap-2 text-left"
  >
    <fwb-input
      placeholder="Task Title"
      v-model="task.title"
      label="Task Title"
    />
    <fwb-textarea
      v-model="task.body"
      :rows="4"
      label="Task Body"
      placeholder="Task Body"
    />
    <fwb-input type="date" v-model="task.due_date" label="Due Date" />
    <fwb-select
      v-model="task.project_id"
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
import type { Project } from "@annotations/project";
import type Task from "@annotations/task";
import { useQuery } from "@tanstack/vue-query";
import { FwbInput, FwbTextarea } from "flowbite-vue";
type PartialTask = Omit<Task, "id">;
import { FwbSelect } from "flowbite-vue";

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
defineProps<{
  task: PartialTask;
}>();
</script>
