<template>
  <fwb-table>
    <thead class="font-bold bg-gray-100">
      <tr
        class="flex flex-row justify-center text-xs text-gray-700 uppercase dark:bg-gray-700 dark:text-gray-400 bg-gray-100"
      >
        <fwb-table-head-cell class="w-1/2 grow">Tag Name</fwb-table-head-cell>
        <fwb-table-head-cell class="w-36">Tag Type</fwb-table-head-cell>
        <fwb-table-head-cell class="w-36">Tag Color</fwb-table-head-cell>
        <fwb-table-head-cell class="w-64"></fwb-table-head-cell>
      </tr>
    </thead>
    <fwb-table-body>
      <TagRow v-for="tag in tags" :tag="tag" />
    </fwb-table-body>
  </fwb-table>
</template>

<script setup lang="ts">
import useTags from "@composables/useTags";
import { FwbTable, FwbTableHeadCell, FwbTableBody } from "flowbite-vue";
import TagRow from "./TagRow.vue";

const { type } = defineProps<{ type: "projects" | "tasks" }>();

const { data: tags } = useTags({
  offset: 0,
  limit: 20,
  type,
  enabled: true
});
</script>
