<template>
  <section class="flex flex-row pb-3 pt-1 items-center gap-5 mr-0.5">
    <fwb-input
      :model-value="search"
      @input="
        (e) =>
          $router.replace({
            query: { ...$route.query, search: e.target.value },
          })
      "
      class="min-w-[45rem] rounded-xl"
      placeholder="Search for Projects"
      size="md"
    />
    <button
      v-if="!completed"
      class="cursor-pointer"
      @click="completeCheckedTasks"
    >
      <svg
        class="w-6 h-6 text-gray-800 dark:text-white"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 11.917 9.724 16.5 19 7.5"
        />
      </svg>
    </button>

    <button
      v-if="completed"
      @click="incompleteCheckedTasks"
      class="cursor-pointer"
    >
      <svg
        class="w-6 h-6 text-gray-800 dark:text-white"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M12 8v4l3 3M3.22302 14C4.13247 18.008 7.71683 21 12 21c4.9706 0 9-4.0294 9-9 0-4.97056-4.0294-9-9-9-3.72916 0-6.92858 2.26806-8.29409 5.5M7 9H3V5"
        />
      </svg>
    </button>

    <button class="cursor-pointer" @click="deleteCheckedTasks">
      <svg
        class="w-6 h-6 text-gray-800 dark:text-white"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 7h14m-9 3v8m4-8v8M10 3h4a1 1 0 0 1 1 1v3H9V4a1 1 0 0 1 1-1ZM6 7h12v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7Z"
        />
      </svg>
    </button>

    <div class="flex flex-row items-center ml-auto">
      <div class="flex flex-row items-center">
        <RouterLink :to="{ query: { page: page > 1 ? page - 1 : '1' } }"
          ><svg
            class="w-9 h-9 text-gray-800 dark:text-white"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m14 8-4 4 4 4"
            /></svg
        ></RouterLink>
        <RouterLink :to="{ query: { page: page + 1 } }" class="cursor-pointer">
          <svg
            class="w-9 h-9 text-gray-800 dark:text-white"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m10 16 4-4-4-4"
            />
          </svg>
        </RouterLink>
        <p class="text-md font-semibold">
          Show {{ (page - 1) * pageSize + 1 }}-{{ page * pageSize }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { inject } from "vue";
import { FwbInput } from "flowbite-vue";
import { useQueryClient } from "@tanstack/vue-query";

const {
  completed = false,
  pageSize = 20,
  search = "",
} = defineProps<{
  projectId: number;
  completed?: boolean;
  page: number;
  pageSize?: number;
  search?: string;
}>();

const queryClient = useQueryClient();
const checked = inject("checked", []);

function clearCheckedTasks() {
  checked.splice(0);
}

async function completeTask(id: number) {
  return fetch(`http://localhost:8000/task/${id}/complete`, {
    method: "PATCH",
  });
}

async function incompleteTask(id: number) {
  return fetch(`http://localhost:8000/task/${id}/incomplete`, {
    method: "PATCH",
  });
}

async function incompleteCheckedTasks() {
  await Promise.all(checked.map((id) => incompleteTask(id)));
  queryClient.invalidateQueries({ queryKey: ["tasks", props.projectId] });
  clearCheckedTasks();
}

async function deleteTask(id: number) {
  return fetch(`http://localhost:8000/task/${id}`, {
    method: "DELETE",
  });
}

async function deleteCheckedTasks() {
  await Promise.all(checked.map((id) => deleteTask(id)));
  queryClient.invalidateQueries({ queryKey: ["tasks", props.projectId] });
  clearCheckedTasks();
}

async function completeCheckedTasks() {
  await Promise.all(checked.map((id) => completeTask(id)));
  queryClient.invalidateQueries({ queryKey: ["tasks", props.projectId] });
  clearCheckedTasks();
}
</script>
