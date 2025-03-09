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
      class="absolute top-2 right-2 rounded-full size-6 bg-gray-300 cursor-pointer"
    >
      X
    </button>
  </div>
</template>

<script setup lang="ts">
const { search = "" } = defineProps<{
  search?: string;
  placeholder: string;
}>();
</script>
