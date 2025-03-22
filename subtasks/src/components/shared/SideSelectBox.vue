<template>
  <div class="relative" ref="dropdownRef">
    <label class="block mb-2 text-sm font-medium">{{ labelText }}</label>
    <button
      @click="toggleDropdown"
      class="cursor-pointer flex flex-row justify-between items-center p-2.5 text-sm rounded-lg w-full text-gray-900 bg-gray-50 focus:ring-primary-500 dark:bg-gray-700 border border-gray-300 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
    >
      {{
        options?.find((option) => option.value == selectedOption)?.label ??
        "Select an option"
      }}
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
      <li class="px-4 py-1 select-none text-black/30">Please select one</li>
      <li
        v-for="option in options"
        role="button"
        @mouseenter="isMousedOver = option.value"
        :key="option.value"
        :class="{
          'bg-blue-500 text-white': isMousedOver == option.value,
        }"
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

interface Option {
  label: string;
  value: number;
}

const props = defineProps<{
  options?: Option[];
  labelText: string;
  defaultValue: number;
}>();

defineEmits<{
  (e: "selectedOption", { value, label }: Option): void;
}>();

const selectedOption = ref<number>(props.defaultValue);
// Used to remember the most recent hovered over item, matching flowbite select behavior
const isMousedOver = ref(props.defaultValue);

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
  isMousedOver.value = props.defaultValue;
};

const selectOption = (option: Option) => {
  selectedOption.value = option.value;
  isOpen.value = false;
};
</script>
