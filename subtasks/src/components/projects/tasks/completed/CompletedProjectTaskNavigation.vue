<template>
  <section class="flex flex-row pb-3 pt-1 items-center gap-5 mr-0.5">
    <fwb-input v-model="search" class="min-w-[45rem] rounded-xl" placeholder="Search for Tasks" size="md" />
    <button @click="incompleteCheckedTasks" class="cursor-pointer">
      <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
        width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 8v4l3 3M3.22302 14C4.13247 18.008 7.71683 21 12 21c4.9706 0 9-4.0294 9-9 0-4.97056-4.0294-9-9-9-3.72916 0-6.92858 2.26806-8.29409 5.5M7 9H3V5" />
      </svg>
    </button>
    <div class="flex flex-row items-center ml-auto">
      <div class="flex flex-row items-center">
        <button>
          <svg class="w-9 h-9 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
            width="24" height="24" fill="none" viewBox="0 0 24 24">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m14 8-4 4 4 4" />
          </svg>
        </button>
        <button class="cursor-pointer">
          <svg class="w-9 h-9 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
            width="24" height="24" fill="none" viewBox="0 0 24 24">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m10 16 4-4-4-4" />
          </svg>
        </button>
        <p class="text-md font-semibold">
          Show 1-20
        </p>
      </div>
    </div>

  </section>
</template>

<script setup lang="ts">
import { inject, ref } from 'vue'
import { FwbInput } from 'flowbite-vue'
import { useQueryClient } from '@tanstack/vue-query'

async function incompleteTask(id: number) {
  return fetch(`http://localhost:8000/task/${id}/incomplete`, {
    method: "PATCH"
  })
}

const props = defineProps<{
  projectId: number
}>()

const queryClient = useQueryClient()
const checked = inject("checked", [])

function clearCheckedTasks() {
  checked.splice(0)

}
async function incompleteCheckedTasks() {
  await Promise.all(checked.map(id => incompleteTask(id)))
  queryClient.invalidateQueries({ queryKey: ['tasks', props.projectId] })
  clearCheckedTasks()
}

const search = ref('')
</script>
