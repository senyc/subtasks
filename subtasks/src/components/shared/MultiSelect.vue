<template>
  <div class="w-full max-w-md mx-auto">
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Choose a fruit
    </label>
    <Multiselect
      v-model="selected"
      :options="props.options"
      placeholder="Pick one or type to add"
      selectLabel=""
      deselectLabel=""
      selectedLabel=""
      label="name"
      track-by="name"
      taggable
      @tag="addTag"
      multiple
      class="custom-multiselect"
      :close-on-select="false"
      :clear-on-select="false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

interface Option {
  name: string;
}

const props = defineProps<{
  options: Option[];
}>();

const selected = ref<Option[]>([]); // for multiple selections

function addTag(newTag: string) {
  const newOption = { name: newTag };
  props.options.push(newOption);
  selected.value.push(newOption);
}
</script>

<style>
.multiselect__option--selected.multiselect__option--highlight::after {
  background: lightgrey;
}

.multiselect__option--selected.multiselect__option--highlight {
  background: #41b883;
}
</style>
