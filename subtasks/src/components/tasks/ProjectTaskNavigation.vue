<template>
  <section class="flex flex-row pb-3 pt-1 items-center gap-5 mr-0.5">
    <SearchBar :search="search" placeholder="Search for Tasks" />
    <button
      v-if="!completed"
      @click="runForAll(completeTask, ['tasks', projectId ?? ''])"
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
          d="M5 11.917 9.724 16.5 19 7.5"
        />
      </svg>
    </button>
    <button
      v-if="completed"
      @click="runForAll(incompleteTask, ['tasks', projectId ?? ''])"
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

    <button
      class="cursor-pointer"
      @click="runForAll(deleteTask, ['tasks', projectId ?? ''])"
    >
      <svg
        class="w-6 h-6 text-gray-800"
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
    <Dropdown>
      <template #button>
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
            stroke-width="3"
            d="M12 6h.01M12 12h.01M12 18h.01"
          />
        </svg>
      </template>
      <div class="flex flex-col gap-3">
        <div class="w-full">
          <SideSelectBox
            @selected-option="
              (option) =>
                runForAll(
                  (id) => updateTaskProject(option.value, id),
                  ['tasks', projectId ?? ''],
                )
            "
            label-text="Select Project"
            :default-value="projectId"
            :options="projectOptions!"
          />
        </div>
        <MultiSelect
          v-model="selectedTags"
          :options="tags!"
          @search-change="(query: string) => (tagSearch = query)"
        />
        <FwbButton
          @click="runForAll(addTag, ['tasks', projectId ?? ''])"
          v-if="(selectedTags?.length || 0) > 0"
          >Add tags to all</FwbButton
        >

        <div class="w-fit">
          <TagModalToggle />
        </div>
      </div>
    </Dropdown>
    <div class="flex flex-row items-center ml-auto">
      <div class="flex flex-row items-center">
        <RouterLink
          :aria-disabled="page > 1"
          :to="{ query: { page: page > 1 ? page - 1 : '1' } }"
        >
          <svg
            :class="{
              'text-gray-800': page > 1,
              'text-gray-800/30 cursor-not-allowed': page <= 1,
            }"
            class="size-9 dark:text-white"
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
            />
          </svg>
        </RouterLink>

        <RouterLink
          :aria-disabled="tasksRemaining <= pageSize"
          :to="{
            query: { page: tasksRemaining <= pageSize ? page : page + 1 },
          }"
          class="cursor-pointer"
        >
          <svg
            :class="{
              'text-gray-800': tasksRemaining > pageSize,
              'text-gray-800/30 cursor-not-allowed': tasksRemaining <= pageSize,
            }"
            class="size-9 dark:text-white"
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
        <div class="w-24">
          <p v-if="isSuccess" class="text-md font-semibold">
            Show {{ (page - 1) * pageSize + 1 }}-{{
              (page - 1) * pageSize +
              (tasksRemaining >= pageSize ? pageSize : tasksRemaining)
            }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, inject, ref } from "vue";
import { useQueryClient } from "@tanstack/vue-query";
import SideSelectBox from "@components/shared/SideSelectBox.vue";
import SearchBar from "@components/shared/SearchBar.vue";
import Dropdown from "@components/shared/Dropdown.vue";
import { useTasks } from "../../composables/useTasks";
import { useProjects } from "../../composables/useProjects";
import TagModalToggle from "@components/tags/TagModalToggle.vue";
import { useTags } from "@composables/useTags";
import MultiSelect from "@components/shared/MultiSelect.vue";
import type { Tag } from "@annotations/tag";
import { FwbButton } from "flowbite-vue";

const {
  completed = false,
  pageSize = 20,
  search = "",
  projectId,
  page,
} = defineProps<{
  projectId?: number;
  completed?: boolean;
  page: number;
  pageSize?: number;
  search?: string;
}>();

const tagSearch = ref("");

const { data: tags } = useTags({
  type: "tasks",
  search: () => tagSearch.value,
});

const selectedTags = defineModel<Tag[]>();

const { data, isSuccess } = useTasks({
  projectId: projectId ? () => projectId : undefined,
  completed: () => completed,
  search: () => search,
  page: () => page,
  pageSize: () => pageSize,
});

// Get projects to show for the project drop down
// TODO: make this a search box so if users have a lot of projects they don't have to page
const { data: projects } = useProjects({
  completed: false,
  page: 1,
  pageSize: 100,
});

const projectOptions = computed(() =>
  projects.value?.projects.map((project) => {
    return { value: project.id, label: project.title };
  }),
);

const tasksRemaining = computed(() => {
  if (!isSuccess) {
    return 0;
  }

  const count = data?.value?.count;
  if (!count) {
    return 0;
  }

  if (count <= pageSize) {
    return count;
  }

  return count - pageSize * (page - 1);
});

const queryClient = useQueryClient();
const checked = inject("checked", []);

function clearCheckedTasks() {
  checked.splice(0);
}

async function runForAll(func: (id: number) => void, key: (string | number)[]) {
  await Promise.all(checked.map((id) => func(id)));
  queryClient.invalidateQueries({ queryKey: key });
  clearCheckedTasks();
}

async function addTag(id: number) {
  return fetch(`http://localhost:8000/task/${id}/tags`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(selectedTags.value),
  });
}

async function completeTask(id: number) {
  return fetch(`http://localhost:8000/task/${id}/complete`, {
    method: "PATCH",
  });
}

async function updateTaskProject(newProjectId: number, id: number) {
  return fetch(`http://localhost:8000/task/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ project_id: newProjectId }),
  });
}

async function incompleteTask(id: number) {
  return fetch(`http://localhost:8000/task/${id}/incomplete`, {
    method: "PATCH",
  });
}

async function deleteTask(id: number) {
  return fetch(`http://localhost:8000/task/${id}`, {
    method: "DELETE",
  });
}
</script>
