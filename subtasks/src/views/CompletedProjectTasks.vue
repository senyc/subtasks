<template>
  <div class="px-8">
    <ProjectBreadCrumbs showProjectName completed />
    <ProjectTaskNavigation
      completed
      :project-id="projectId"
      :search="$route.query?.search as string"
      :page="parseInt(($route.query?.page as string) ?? '1')"
    />
    <ProjectTaskList
      completed
      :project-id="projectId"
      :search="$route.query?.search as string"
      :page="parseInt(($route.query?.page as string) ?? '1')"
    />
  </div>
</template>

<script setup lang="ts">
import ProjectTaskNavigation from "@components/projects/ProjectTaskNavigation.vue";
import ProjectTaskList from "@components/projects/tasks/ProjectTaskList.vue";
import ProjectBreadCrumbs from "@components/projects/ProjectBreadCrumbs.vue";
import { provide, reactive } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const projectId = parseInt(route.params.id as string);

const checkedTasks = reactive<number[]>([]);
provide<number[]>("checked", checkedTasks);
</script>
