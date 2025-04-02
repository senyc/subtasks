<template>
  <div>
    <QuillEditor
      v-model:content="modelValue"
      theme="snow"
      toolbar="#my-toolbar"

    >
      <template #toolbar>
        <div id="my-toolbar">
          <select :tabindex="4" class="ql-header">
            <option :value="1"></option>
            <option :value="2" ></option>
            <option :value="3"></option>
            <option :value="4"></option>
            <option :value="5"></option>
            <option :value="6"></option>
            <option selected :value="false"></option>
          </select>
          <button :tabindex="5" class="ql-bold"></button>
          <button :tabindex="6" class="ql-italic"></button>
          <select class="ql-align !ml-4" />
          <button :tabindex="8" value="bullet" class="ql-list"></button>
          <button :tabindex="9" value="ordered" class="ql-list"></button>
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
    const sizeSelect = document.querySelectorAll(".ql-picker-label");
    if (sizeSelect) {
      sizeSelect.forEach((element, idx) =>
        element.setAttribute("tabindex", `${idx + 7}`),
      );
    }
  });
});
</script>
<style scoped>
:deep(.ql-editor) {
  min-height: 300px;
}
</style>
