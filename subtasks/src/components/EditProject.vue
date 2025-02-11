<template>
  <fwb-button class="cursor-pointer" @click="isShowModal = true">
    <template #prefix>
      <svg class="size-5 text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
        fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="m14.304 4.844 2.852 2.852M7 7H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-4.5m2.409-9.91a2.017 2.017 0 0 1 0 2.853l-6.844 6.844L8 14l.713-3.565 6.844-6.844a2.015 2.015 0 0 1 2.852 0Z" />
      </svg>
    </template>
    Edit
  </fwb-button>
  <fwb-modal v-if="isShowModal" @close="isShowModal = false">
    <template #header>
      <div class="border-none flex items-center text-lg">
        Edit {{ props.project.title }}
      </div>
    </template>
    <template #body>
      <ProjectForm :project="project" @on-submit="onSubmit" />
    </template>
    <template #footer>
      <div class="flex justify-between">
        <fwb-button @click="isShowModal = false" color="alternative">
          Cancel
        </fwb-button>
        <fwb-button @click="onSubmit" color="green">
          Save
        </fwb-button>
      </div>
    </template>
  </fwb-modal>
</template>

<script setup lang="ts">
import { useQueryClient } from '@tanstack/vue-query'
import { reactive, ref } from 'vue'
import { FwbButton, FwbModal } from 'flowbite-vue'
import type { Project } from '@annotations/project'
import ProjectForm from './ProjectForm.vue';
const queryClient = useQueryClient()

const props = defineProps<{
  project: Project
}>()

const isShowModal = ref(false)

const project = reactive<Omit<Project, "id" | "totalTasks" | "completedTasks">>({
  title: props.project.title,
  body: props.project.body,
})

async function onSubmit() {

  const res = await fetch(`http://localhost:8000/project/${props.project.id}`, {
    method: "PUT",
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    },
    body: JSON.stringify({
      title: project.title,
      body: project.body
    })
  })
  if (res.ok) {
    isShowModal.value = false
    queryClient.invalidateQueries({ queryKey: ["projects"] })
  }
}
</script>
