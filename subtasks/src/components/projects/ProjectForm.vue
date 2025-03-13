<template>
  <form
    @submit.prevent="$emit('onSubmit')"
    class="flex flex-col gap-2 text-left"
  >
    <fwb-input
      ref="titleRef"
      placeholder="Project Title"
      v-model="project.title"
      label="Project Title"
    />
    <fwb-textarea
      @keydown.ctrl.enter="$emit('onSubmit')"
      v-model="project.body"
      :rows="4"
      label="Project Body"
      placeholder="Project Body"
    />
    <fwb-input type="date" v-model="project.due_date" label="Due Date" />
  </form>
</template>

<script lang="ts" setup>
import type { Project } from "@annotations/project";
import { FwbInput, FwbTextarea } from "flowbite-vue";
import {
  nextTick,
  onBeforeMount,
  onBeforeUnmount,
  onMounted,
  useTemplateRef,
} from "vue";
type PartialProject = Omit<Project, "id" | "totalTasks" | "completedTasks">;

defineProps<{
  project: PartialProject;
}>();

const titleRef = useTemplateRef("titleRef");

onBeforeUnmount(() => {
  window.onbeforeunload = null;
});

onBeforeMount(() => {
  window.onbeforeunload = () => true;
});
onMounted(() => {
  // This is needed because the modal has it's own call to onMounted, setting focus on the modal
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
</script>
