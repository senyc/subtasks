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
  <fwb-modal size="4xl" v-if="isShowModal" @close="isShowModal = false">
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
import type { TaskDisplay } from '@annotations/task'
import TaskForm from './ProjectTaskForm.vue';
import { Delta } from '@vueup/vue-quill';
const queryClient = useQueryClient()

const props = defineProps<{
  projectId?: number
}>()

const task = reactive<TaskDisplay>({
  title: "",
  body: new Delta(),
  project_id: props.projectId,
  time_estimate: 15
})


const isShowModal = ref(false)
async function onSubmit() {
  isShowModal.value = false
  const url = `http://localhost:8000${props.projectId ? `/project/${props.projectId}` : "" }/task`
  const res = await fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'accept': 'application/json'
    },
    body: JSON.stringify({ ...task, body: JSON.stringify(task.body) }),
  })
  if (res.ok) {
    queryClient.invalidateQueries({ queryKey: ["tasks", props.projectId || "" ] })
    // Reset the new task data
    task.title = ""
    task.body = new Delta()
    task.due_date = undefined
  }
}
</script>
