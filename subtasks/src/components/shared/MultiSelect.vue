<template>
  <Multiselect
    v-model="modelValue"
    :options="props.options"
    placeholder="Pick one or type to add"
    selectLabel=""
    :internal-search="false"
    deselectLabel=""
    selectedLabel=""
    label="name"
    track-by="name"
    multiple
    :close-on-select="false"
    :clear-on-select="false"
  />
</template>

<script setup lang="ts">
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

interface Option {
  name: string;
}
const modelValue = defineModel<Option[]>();

const props = defineProps<{
  options: Option[];
}>();
</script>

<style>
.multiselect__option--selected.multiselect__option--highlight::after {
  background: lightgrey;
}

.multiselect__option--selected.multiselect__option--highlight {
  background: #41b883;
}
</style>
