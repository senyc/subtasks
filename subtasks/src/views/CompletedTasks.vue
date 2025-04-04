<template>
  <Header active="tasks" />
  <div class="px-8">
    <TasksBreadCrumbs completed />
    <ProjectTaskNavigation
      :search="$route.query?.search as string"
      :page="parseInt(($route.query?.page as string) ?? '1')"
      completed
    />
    <ProjectTaskList
      :search="$route.query?.search as string"
      :page="parseInt(($route.query?.page as string) ?? '1')"
      completed
    />
  </div>
</template>

<script setup lang="ts">
import { provide, reactive } from "vue";
import TasksBreadCrumbs from "@components/tasks/TasksBreadCrumbs.vue";
import ProjectTaskNavigation from "@components/tasks/ProjectTaskNavigation.vue";
import Header from "@components/Header.vue";
import ProjectTaskList from "@components/tasks/ProjectTaskList.vue";

const checked = reactive<number[]>([]);

provide<number[]>("checked", checked);
</script>
