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
  >
    <template #tag="{ option }">
      <span
        class="font-bold !px-2 !py-1 multiselect__tag"
        :style="{
          backgroundColor: option.color,
          color: textColor(option.color),
        }"
      >
        {{ option.name }}
        <button
          type="button"
          @click.stop="removeTag(option.id)"
          :style="{ cursor: 'pointer' }"
        >
          &times;
        </button>
      </span>
    </template>
  </Multiselect>
</template>

<script setup lang="ts">
import { computed } from "vue";
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

interface Option {
  id: number;
  name: string;
  color: string;
}
const modelValue = defineModel<Option[]>();

const removeTag = (id: number) => {
  modelValue.value = modelValue.value?.filter((value) => value.id != id);
};

const textColor = computed(() => {
  return (color: string) => {
    const hex = color.replace("#", "");
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    // Calculate a darker color (reduce brightness)
    const darken = (value: number) => Math.max(0, value - 95);
    return `rgb(${darken(r)}, ${darken(g)}, ${darken(b)})`;
  };
});
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
