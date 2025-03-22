<template>
  <div class="relative">
    <label class="block mb-2 text-sm font-medium">{{ labelText }}</label>
    <button
      @click="toggleDropdown"
      class="flex flex-row justify-between items-center p-2.5 text-sm rounded-lg w-full text-gray-900 bg-gray-50 focus:ring-primary-500 dark:bg-gray-700 border border-gray-300 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
    >
      {{ selectedOption || "Select an option" }}
      <svg
        class="size-4"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="m15 19-7-7 7-7"
        />
      </svg>
    </button>
    <ul
      v-if="isOpen"
      class="absolute top-7 right-[103%] bg-white border border-gray-300 text-sm shadow-md p-1 rounded-lg w-52"
    >
      <li
        v-for="option in options"
        :key="option.value"
        @click="
          selectOption(option);
          $emit('selectedOption', option);
        "
        class="px-4 py-1.5 cursor-pointer hover:bg-blue-500 hover:text-white text-black rounded-md"
      >
        {{ option.label }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const isOpen = ref(false);
const selectedOption = ref<string>();

interface Option {
  label: string;
  value: number;
}

defineProps<{ options: Option[]; labelText: string }>();

defineEmits<{
  (e: "selectedOption", { value, label }: Option): void;
}>();

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const selectOption = (option: Option) => {
  selectedOption.value = option.label;
  isOpen.value = false;
};
</script>
