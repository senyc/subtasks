<template>
  <form @submit.prevent="$emit('onSubmit')" class="flex flex-col gap-2 text-left">
    <fwb-input placeholder="Project Title" v-model="project.title" label="Project Title" />
    <fwb-textarea v-model="project.body" :rows="4" label="Project Body" placeholder="Project Body" />
    <fwb-input type="date" v-model="project.due_date" label="Due Date" />
  </form>
</template>

<script lang="ts" setup>
import type { Project } from '@annotations/project';
import { FwbInput, FwbTextarea } from 'flowbite-vue'
type PartialProject = Omit<Project, "id" | "totalTasks" | "completedTasks">

defineProps<{
  project: PartialProject
}>()
</script>
