<template>
  <fwb-modal class="test" @close="$emit('close')">
    <template #header>
      <div
        class="ml-2 border-none text-left line-clamp-1 overflow-ellipsis text-lg"
      >
        Edit Tag
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
import { reactive } from "vue";

const queryClient = useQueryClient();

const props = defineProps<{
  tag: Tag;
  type: "projects" | "tasks";
}>();

const tag = reactive<Tag>({
  ...props.tag,
});

const emit = defineEmits<{
  (e: "close"): void;
}>();

async function onSubmit() {
  const res = await fetch(`http://localhost:8000/tag/${props.tag.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ ...tag, id: undefined }),
  });

  if (res.ok) {
    queryClient.invalidateQueries({ queryKey: ["tags", () => props.type] });
    emit("close");
  }
}
</script>
