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
    <RichTextEditor v-model="project.body" />
    <fwb-input type="date" v-model="project.due_date" label="Due Date" />
  </form>
</template>

<script lang="ts" setup>
import type { ProjectDisplay } from "@annotations/project";
import { FwbInput } from "flowbite-vue";
import RichTextEditor from "../projects/tasks/RichTextEditor.vue";
import {
  nextTick,
  onBeforeMount,
  onBeforeUnmount,
  onMounted,
  useTemplateRef,
} from "vue";

defineProps<{
  project: ProjectDisplay;
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
