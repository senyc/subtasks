<template>
  <Dialog
    :close-on-escape="true"
    :draggable="false"
    v-model:visible="visible"
    modal
    header="New Task"
    class="sm:w-200 w-9/10"
  >
    <div class="flex flex-col gap-2">
      <TaskForm :model-value="task" />
      <div class="flex flex-row justify-between gap-2">
        <SecondaryButton
          type="button"
          label="Cancel"
          @click="visible = false"
        />
        <Button type="button" label="Add Task" @click="console.log('test')" />
      </div>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import Button from "@volt/Button.vue";
import Dialog from "@volt/Dialog.vue";
import SecondaryButton from "@volt/SecondaryButton.vue";
import TaskForm from "./TaskForm.vue";
import { ref } from "vue";
import type { Task } from "@annotations/models/task";
const visible = defineModel<boolean>({ required: true });
const task = ref<Task>({ title: "" });
</script>
