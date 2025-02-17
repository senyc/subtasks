<template>
  <form @submit.prevent="$emit('onSubmit')" class="flex flex-col gap-2 text-left">
    <fwb-input placeholder="Task Title" v-model="task.title" label="Task Title" />
    <fwb-textarea v-model="task.body" :rows="4" label="Task Body" placeholder="Task Body" />
    <fwb-input type="date" v-model="task.due_date" label="Due Date" />
  </form>
</template>

<script lang="ts" setup>
import type Task from '@annotations/task';
import { FwbInput, FwbTextarea } from 'flowbite-vue'
type PartialTask = Omit<Task, "id">

defineProps<{
  task: PartialTask
}>()
</script>
