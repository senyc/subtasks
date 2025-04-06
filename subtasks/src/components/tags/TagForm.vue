<template>
  <form
    @submit.prevent="$emit('onSubmit')"
    class="flex flex-col gap-3 text-left"
  >
    <fwb-input
      placeholder="Tag Name"
      v-model="tag.name"
      label="Tag Name"
      ref="nameRef"
    />
    <fwb-textarea
      placeholder="Tag Description"
      v-model="tag.description"
      label="Tag Description"
    />
    <div class="w-fit">
      <fwb-input
        class="w-fit"
        type="color"
        v-model="tag.color"
        label="Tag Color"
      />
    </div>
  </form>
</template>

<script lang="ts" setup>
import type { Tag } from "@annotations/tag";
import { ref } from "vue";
import { FwbInput, FwbTextarea } from "flowbite-vue";

const nameRef = ref(null);

defineProps<{
  tag: Tag;
}>();
</script>
