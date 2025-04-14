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
      @keydown="(e) => handleKeydown(e)"
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
    <ul
      v-if="tags?.length && !search.includes(' ') && search.length > 0"
      class="absolute z-10 bg-white border border-gray-300 rounded-lg mt-1 w-full"
    >
      <li
        v-for="(tag, index) in filteredOutDuplicateTags"
        :key="tag.id"
        @click="selectTag(tag.name)"
        :class="{ 'bg-gray-100': index == selectedTag }"
        class="p-2 hover:bg-gray-100 cursor-pointer"
      >
        tag:{{ tag.name }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import useTags from "@composables/useTags";
import { computed, ref, watch } from "@vue/reactivity";
import { useRoute, useRouter } from "vue-router";

const selectedTag = ref(0);
const { search = "", type = "tasks" } = defineProps<{
  search?: string;
  placeholder: string;
  type: "tasks" | "projects";
}>();

const { data: tags } = useTags({
  type,
  search: () => {
    const split = search.split(",");
    const searchString = split[split.length - 1];
    return searchString.replace("tag:", "");
  },
  enabled: () => !search.includes(" "),
  limit: 5,
  offset: 0,
});

const router = useRouter();
const route = useRoute();

const filteredOutDuplicateTags = computed(() => {
  selectedTag.value = 0; // Reset selectedTag when search changes
  if (!tags.value) {
    return tags.value;
  }
  return tags.value.filter((tag) => !search.includes(tag.name));
});

watch(
  () => search,
  () => {
    selectedTag.value = 0; // Reset selectedTag when search value changes
  },
);

const handleKeydown = (event: KeyboardEvent) => {
  switch (event.key) {
    case "Tab":
      if ((tags.value?.length || 0) > 0) {
        event.preventDefault();
        const firstTag =
          filteredOutDuplicateTags.value?.[selectedTag.value].name || "";
        const prevSearch = search.split(",");
        const previousTagsSplit = prevSearch.slice(0, prevSearch.length - 1);
        let previousTags = previousTagsSplit.join(",");
        if (previousTags) {
          previousTags += ",";
        }
        router.replace({
          query: {
            ...route.query,
            search: previousTags + `tag:${firstTag}`,
          },
        });
      }
      break;
    case "Enter":
      if ((tags.value?.length || 0) > 0) {
        event.preventDefault();
        const firstTag =
          filteredOutDuplicateTags.value?.[selectedTag.value].name || "";
        const prevSearch = search.split(",");
        const previousTagsSplit = prevSearch.slice(0, prevSearch.length - 1);
        let previousTags = previousTagsSplit.join(",");
        if (previousTags) {
          previousTags += ",";
        }
        router.replace({
          query: {
            ...route.query,
            search: previousTags + `tag:${firstTag}`,
          },
        });
      }
      break;
    case "ArrowUp":
      event.preventDefault();
      selectedTag.value =
        (selectedTag.value - 1 + filteredOutDuplicateTags!.value!.length) %
        filteredOutDuplicateTags!.value!.length;
      break;
    case "ArrowDown":
      event.preventDefault();
      selectedTag.value =
        (selectedTag.value + 1) % filteredOutDuplicateTags!.value!.length;
      break;
  }
};

const selectTag = (tag: string) => {
  const prevSearch = search.split(",");
  const previousTagsSplit = prevSearch.slice(0, prevSearch.length - 1);
  let previousTags = previousTagsSplit.join(",");
  if (previousTags) {
    previousTags += ",";
  }
  router.replace({
    query: {
      ...route.query,
      search: previousTags + `tag:${tag}`,
    },
  });
};
</script>
