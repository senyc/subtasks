<template>
  <form @submit.prevent="$emit('submit')">
    <div class="flex flex-col gap-1 mb-4">
      <label for="title" class="font-semibold w-24">Title</label>
      <InputText
        v-model="timeSlot.title"
        name="title"
        id="title"
        autocomplete="true"
        :autofocus="true"
      />
    </div>
    <SelectButton v-model="timeSlot.type" :options="options" />
    <div class="flex flex-col gap-1 mb-8">
      <label for="notes" class="font-semibold w-24">Notes</label>
      <Textarea v-model="timeSlot.notes" id="notes" autocomplete="off" />
    </div>
  </form>
</template>

<script setup lang="ts">
import InputText from "@volt/InputText.vue";
import Textarea from "@volt/Textarea.vue";
import SelectButton from "@volt/SelectButton.vue";
import type { TimeSlotForm } from "@annotations/models/timeSlot";
import { ref } from "vue";

const timeSlot = defineModel<TimeSlotForm>({ required: true });
defineEmits<{
  submit: [void];
}>();

const options = ref(["event", "task"]);
</script>
