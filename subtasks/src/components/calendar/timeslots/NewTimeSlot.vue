<template>
  <Dialog
    close-on-escape
    draggable
    v-model:visible="visible"
    header="New Task"
    class="sm:w-200 w-9/10"
  >
    <div class="flex flex-col gap-2">
      <TimeSlotForm :model-value="timeSlot" />
      <div class="flex flex-row justify-between gap-2">
        <SecondaryButton type="button" label="Cancel" @click="cancelTimeSlot" />
        <Button type="button" label="Add Time slot" @click="createTimeSlot" />
      </div>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
//TODO: fix this so that if the modal is open it will take in the values of the event if it is resized while modal is open
// probably just have to make something else a model or something (add emits,etc)
import Button from "@volt/Button.vue";
import Dialog from "@volt/Dialog.vue";
import SecondaryButton from "@volt/SecondaryButton.vue";
import TimeSlotForm from "./TimeSlotForm.vue";
import type { TimeSlotForm as TimeSlotFormType } from "@annotations/models/timeSlot";

const emit = defineEmits<{
  (e: "cancelTimeSlot"): void;
  (e: "createTimeSlot", event: TimeSlotFormType): void;
}>();

const visible = defineModel<boolean>("visible", { required: true });
const timeSlot = defineModel<TimeSlotFormType>("timeSlot", { required: true });

function createTimeSlot() {
  visible.value = false;
  emit("createTimeSlot", timeSlot.value);
}

function cancelTimeSlot() {
  visible.value = false;
  emit("cancelTimeSlot");
}
</script>
