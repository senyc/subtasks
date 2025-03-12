<template>
  <fwb-button size="sm" class="w-34 cursor-pointer" @click="isShowModal = true">
    New Task
    <template #prefix>
      <svg class="size-5 text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24"
        fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M5 12h14m-7 7V5" />
      </svg>
    </template>
  </fwb-button>
  <fwb-modal v-if="isShowModal" @close="isShowModal = false">
    <template #header>
      <div class="flex items-center text-lg">
        New Task
      </div>
    </template>
    <template #body>
      <TaskForm :task="task" @on-submit="onSubmit" />
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
import type Task from '@annotations/task'
import TaskForm from './projects/tasks/ProjectTaskForm.vue';
const queryClient = useQueryClient()

const props = defineProps<{
  projectId: number
}>()

const task = reactive<Omit<Task, "id">>({
  title: "",
  body: "",
  project_id: props.projectId
})


const isShowModal = ref(false)
async function onSubmit() {
  isShowModal.value = false
  const res = await fetch(`http://localhost:8000/project/${props.projectId}/task`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    },
    body: JSON.stringify(task)
  })
  if (res.ok) {
    queryClient.invalidateQueries({ queryKey: ["tasks", props.projectId] })
    task.title = ""
    task.body = ""
    task.due_date = ""
  }
}
</script>
