<template>
  <form @submit.prevent="$emit('submit')">
    <div class="flex flex-col gap-1 mb-4">
      <label for="title" class="font-semibold w-24">Title</label>
      <InputText
        v-model="event.title"
        name="title"
        id="title"
        autocomplete="true"
        :autofocus="true"
      />
    </div>
    <div class="flex flex-col gap-1 mb-8">
      <label for="notes" class="font-semibold w-24">Notes</label>
      <Textarea v-model="event.notes" id="notes" autocomplete="off" />
    </div>
  </form>
</template>

<script setup lang="ts">
import type { Event } from "@annotations/event";
import InputText from "@volt/InputText.vue";
import Textarea from "@volt/Textarea.vue";

defineProps<{
  event: Event;
}>();

defineEmits<{
  submit: [void];
}>();
</script>
