<template>
  <form @submit.prevent="$emit('submit')" class="flex flex-col gap-3 mb-4">
    <div class="flex flex-col gap-1">
      <label
        for="title"
        class="font-semibold after:content-['*'] after:text-red-600 after:align-super after:text-xs"
        >Title</label
      >
      <InputText
        aria-required
        v-model="task.title"
        required
        name="title"
        id="title"
        autocomplete="true"
        :autofocus="true"
      />
    </div>
    <div class="flex flex-col gap-1">
      <label for="body" class="font-semibold">Body</label>
      <Textarea
        id="body"
        name="body"
        class="resize-none"
        v-model="task.body"
        autoResize
        rows="3"
        cols="30"
      />
    </div>
    <div class="flex flex-col gap-1">
      <label for="time_estimate" class="font-semibold">Time Estimate</label>
      <AutoComplete
        fluid
        focus-on-hover
        complete-on-focus
        id="time_estimate"
        name="time_estimate"
        v-model="task.time_estimate"
        @complete="search"
        :suggestions="filteredItems"
      />
    </div>
    <div class="flex flex-col gap-1">
      <label for="do_date" class="font-semibold">Do Date</label>
      <DatePicker v-model="task.do_date" show-icon show-on-focus />
    </div>
  </form>
</template>

<script setup lang="ts">
import type { Task } from "@annotations/models/task";
import InputText from "@volt/InputText.vue";
import Textarea from "@volt/Textarea.vue";
import AutoComplete from "@volt/AutoComplete.vue";
import DatePicker from "@volt/DatePicker.vue";

import { ref } from "vue";
import type { AutoCompleteCompleteEvent } from "primevue";

const items = ref([
  { value: 15, name: "15m" },
  { value: 30, name: "30m" },
  { value: 45, name: "45m" },
  { value: 60, name: "1h" },
  { value: 90, name: "1.5h" },
  { value: 120, name: "2h" },
  { value: 180, name: "3h" },
  { value: 240, name: "4h" },
  { value: 300, name: "5h" },
]);

const filteredItems = ref();
const search = (event: AutoCompleteCompleteEvent) => {
  if (!event.query.trim().length) {
    filteredItems.value = [...items.value.map((item) => item.name)];
  } else {
    filteredItems.value = items.value
      .filter((item) => {
        return item.name.toLowerCase().startsWith(event.query.toLowerCase());
      })
      .map((item) => item.name);
  }
};

const task = defineModel<Task>({ required: true });
defineEmits<{
  submit: [void];
}>();
</script>
