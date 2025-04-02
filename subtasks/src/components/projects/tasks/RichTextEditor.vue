<template>
  <div>
    <QuillEditor
      v-model:content="modelValue"
      theme="snow"
      toolbar="#my-toolbar"
    >
      <template #toolbar>
        <div id="my-toolbar">
          <select class="ql-size">
            <option value="small"></option>
            <option value="normal" selected></option>
            <option value="large"></option>
            <option value="huge"></option>
          </select>
          <button :tabindex="4" class="ql-bold"></button>
          <button :tabindex="5" class="ql-italic"></button>
        </div>
      </template>
    </QuillEditor>
  </div>
</template>
<script setup lang="ts">
import { Delta, QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

const modelValue = defineModel<Delta>();
import { onMounted, nextTick } from "vue";

onMounted(() => {
  // Updates the toolbar to be after the body in terms of tab order
  nextTick(() => {
    const sizeSelect = document.querySelector(".ql-picker-label");
    if (sizeSelect) {
      sizeSelect.setAttribute("tabindex", "3");
    }
  });
});
</script>
<style scoped>
:deep(.ql-editor) {
  min-height: 300px;
}
</style>
