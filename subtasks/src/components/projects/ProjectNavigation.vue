<template>
  <section class="flex flex-row pb-3 pt-1 items-center gap-5 mr-0.5">
    <fwb-input v-model="search" class="min-w-[45rem] rounded-xl" placeholder="Search for Projects" size="md" />
    <button v-if="!completed" @click="completeCheckedProjects" class="cursor-pointer">
      <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
        width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M5 11.917 9.724 16.5 19 7.5" />
      </svg>
    </button>
    <button class="cursor-pointer" @click="deleteCheckedProjects"><svg class="w-6 h-6 text-gray-800 dark:text-white"
        aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M5 7h14m-9 3v8m4-8v8M10 3h4a1 1 0 0 1 1 1v3H9V4a1 1 0 0 1 1-1ZM6 7h12v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7Z" />
      </svg></button>
    <div class="flex flex-row items-center ml-auto">
      <div class="flex flex-row items-center">
        <svg class="w-9 h-9 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
          width="24" height="24" fill="none" viewBox="0 0 24 24">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="m14 8-4 4 4 4" />
        </svg>


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

const queryClient = useQueryClient()
const checked = inject("checked", [])

withDefaults(defineProps<{
  completed?: boolean
}>(), { completed: false })

function clearCheckedProjects() {
  checked.splice(0)
}

async function deleteProject(id: number) {
  return fetch(`http://localhost:8000/project/${id}`, {
    method: "DELETE"
  })
}

async function deleteCheckedProjects() {
  await Promise.all(checked.map(id => deleteProject(id)))
  queryClient.invalidateQueries({ queryKey: ['projects'] })
  clearCheckedProjects()
}

async function completeProject(id: number) {
  return fetch(`http://localhost:8000/project/${id}/complete`, {
    method: "PATCH"
  })
}

async function completeCheckedProjects() {
  await Promise.all(checked.map(id => completeProject(id)))
  queryClient.invalidateQueries({ queryKey: ['projects'] })
  clearCheckedProjects()
}

const search = ref('')
</script>
