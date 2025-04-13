<template>
  <div>
    <QuillEditor
      ref="editorRef"
      v-model:content="modelValue"
      theme="snow"
      toolbar="#my-toolbar"
      :modules="modules"
    >
      <template #toolbar>
        <div id="my-toolbar">
          <select class="ql-header">
            <option :value="1"></option>
            <option :value="2"></option>
            <option :value="3"></option>
            <option :value="4"></option>
            <option :value="5"></option>
            <option :value="6"></option>
            <option selected :value="false"></option>
          </select>
          <button :tabindex="5" class="ql-bold"></button>
          <button :tabindex="6" class="ql-italic"></button>
          <button :tabindex="7" class="ql-link"></button>
          <select class="ql-align !ml-4" />
          <button :tabindex="9" value="bullet" class="ql-list"></button>
          <button :tabindex="10" value="ordered" class="ql-list"></button>
        </div>
      </template>
    </QuillEditor>
  </div>
</template>

<script setup lang="ts">
import { Delta, QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import { onMounted, nextTick, ref } from "vue";

const modelValue = defineModel<Delta>();
const editorRef = ref();
import BlotFormatter from "quill-blot-formatter";

const modules = {
  name: "blotFormatter",
  module: BlotFormatter,
  options: {
    /* options */
  },
};
const emit = defineEmits<{
  (e: "submit"): void;
}>();

onMounted(() => {
  nextTick(() => {
    const sizeSelect = document.querySelectorAll(".ql-picker-label");
    if (sizeSelect) {
      sizeSelect.forEach((element, idx) =>
        element.setAttribute("tabindex", `${idx + 8}`),
      );
    }

    const quill = editorRef.value?.getEditor();
    if (quill) {
      quill.addEventListener("keydown", (e: KeyboardEvent) => {
        if (e.ctrlKey && e.key === "Enter") {
          e.preventDefault();
          emit("submit");
        }
      });
    }
  });
});
</script>

<style scoped>
:deep(.ql-editor) {
  min-height: 300px;
}
</style>
