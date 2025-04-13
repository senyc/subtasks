<template>
  <fwb-table-row class="border-b-gray-200 flex justify-center flex-row">
    <fwb-table-cell class="grow w-1/2">
      {{ tag.name }}
    </fwb-table-cell>
    <fwb-table-cell class="w-36">{{ tag.type }}</fwb-table-cell>
    <fwb-table-cell :style="{ color: tag.color }" class="!text-left w-36">{{
      tag.color.toUpperCase()
    }}</fwb-table-cell>
    <fwb-table-cell class="flex flex-row gap-3 w-64"
      ><EditButton @click="modelOpen = !modelOpen" />
      <DeleteButton @click="deleteTag"
    /></fwb-table-cell>
  </fwb-table-row>
  <EditTagModal
    v-if="modelOpen"
    @close="modelOpen = false"
    type="tasks"
    :tag="tag"
  />
</template>

<script setup lang="ts">
import type { Tag } from "@annotations/tag";

import { FwbTableCell, FwbTableRow } from "flowbite-vue";
import { ref } from "vue";
import EditTagModal from "./EditTagModal.vue";
import { useQueryClient } from "@tanstack/vue-query";
import EditButton from "@components/shared/EditButton.vue";
import DeleteButton from "@components/shared/DeleteButton.vue";
const queryClient = useQueryClient();

const props = defineProps<{
  tag: Tag;
}>();

async function deleteTag() {
  const req = await fetch(`http://localhost:8000/tag/${props.tag.id}`, {
    method: "DELETE",
  });

  if (req.ok) {
    queryClient.invalidateQueries({ queryKey: ["tags", () => props.tag.type] });
  }
}

const modelOpen = ref(false);
</script>
