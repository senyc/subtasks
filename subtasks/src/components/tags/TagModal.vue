<template>
  <fwb-modal class="test" @close="$emit('close')">
    <template #header>
      <div
        class="ml-2 border-none text-left line-clamp-1 overflow-ellipsis text-lg"
      >
        New Tag
      </div>
    </template>
    <template #body>
      <TagForm :tag="tag" @on-submit="onSubmit" />
    </template>
    <template #footer>
      <div class="flex justify-between">
        <fwb-button @click="$emit('close')" color="alternative">
          Cancel
        </fwb-button>
        <fwb-button @click="onSubmit" color="green"> Save </fwb-button>
      </div>
    </template>
  </fwb-modal>
</template>
<script setup lang="ts">
import type { Tag } from "@annotations/tag";
import TagForm from "./TagForm.vue";
import { FwbButton, FwbModal } from "flowbite-vue";
import { useQueryClient } from "@tanstack/vue-query";

const queryClient = useQueryClient();

const props = defineProps<{
  tag: Omit<Tag, "id">;
  type: "projects" | "tasks";
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

async function onSubmit() {
  const res = await fetch(`http://localhost:8000/tag`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ ...props.tag, type: props.type }),
  });
  if (res.ok) {
    queryClient.invalidateQueries({ queryKey: ["tags", () => props.type] });
    emit("close");
  }
}
</script>
