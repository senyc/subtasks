<template>
  <fwb-button class="w-34 cursor-pointer" size="sm" @click="isShowModal = true">
    New Project
    <template #prefix>
      <svg
        class="w-5 h-5 text-white"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 12h14m-7 7V5"
        />
      </svg>
    </template>
  </fwb-button>
  <fwb-modal v-if="isShowModal" @close="isShowModal = false">
    <template #header>
      <div class="flex items-center">New Project</div>
    </template>
    <template #body>
      <ProjectForm :project="project" @on-submit="onSubmit" />
    </template>
    <template #footer>
      <div class="flex justify-between">
        <fwb-button @click="isShowModal = false" color="alternative">
          Cancel
        </fwb-button>
        <fwb-button @click="onSubmit" color="green"> Save </fwb-button>
      </div>
    </template>
  </fwb-modal>
</template>

<script setup lang="ts">
import { useQueryClient } from "@tanstack/vue-query";
import { reactive, ref } from "vue";
import { FwbButton, FwbModal } from "flowbite-vue";
import type { Project } from "@annotations/project";
import ProjectForm from "./ProjectForm.vue";
const queryClient = useQueryClient();

const project = reactive<
  Omit<Project, "id" | "totalTasks" | "completedTasks" | "order">
>({
  title: "",
  body: "",
  due_date: "",
});

const isShowModal = ref(false);
async function onSubmit() {
  isShowModal.value = false;
  const res = await fetch("http://localhost:8000/project", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(project),
  });
  if (res.ok) {
    queryClient.invalidateQueries({ queryKey: ["projects"] });
    project.title = "";
    project.body = "";
    project.due_date = "";
  }
}
</script>
