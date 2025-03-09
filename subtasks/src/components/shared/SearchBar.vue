<template>
  <input
    class="max-w-[65em] text-sm w-full p-2.5 bg-gray-50 border border-gray-300 text-gray-900 rounded-lg has-[input:focus]:ring-blue-500 has-[input:focus]:border-blue-500"
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
</template>

<script setup lang="ts">
const { search = "" } = defineProps<{
  search?: string;
  placeholder: string;
}>();
</script>
