<template>
  <div class="max-w-[65em] w-full relative">
    <input
      class="text-sm w-full p-2.5 bg-gray-50 border border-gray-300 text-gray-900 rounded-lg has-[input:focus]:ring-blue-500 has-[input:focus]:border-blue-500"
      :value="search"
      @input="
        (e) => {
          const inputValue = (e.target as HTMLInputElement).value;
          $router.replace({
            query: {
              ...$route.query,
              search: inputValue != '' ? inputValue : undefined,
            },
          });
        }
      "
      type="text"
      :placeholder="placeholder"
      autofocus
    />
    <button
      v-if="search.length > 0"
      @click="
        $router.replace({
          query: {
            ...$route.query,
            search: undefined,
          },
        })
      "
      class="absolute top-2 right-2 rounded-full flex flex-row items-center justify-center size-6 bg-gray-300 cursor-pointer"
    >
      <svg
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M6 18 17.94 6M18 18 6.06 6"
        />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
const { search = "" } = defineProps<{
  search?: string;
  placeholder: string;
}>();
</script>
