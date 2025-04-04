<template>
  <Header active="projects" />
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
import ProjectTaskNavigation from "@components/tasks/ProjectTaskNavigation.vue";
import ProjectTaskList from "@components/tasks/ProjectTaskList.vue";
import ProjectBreadCrumbs from "@components/projects/ProjectBreadCrumbs.vue";
import { provide, reactive } from "vue";
import { useRoute } from "vue-router";
import Header from "@components/Header.vue";


const route = useRoute();
const projectId = parseInt(route.params.id as string);

const checkedTasks = reactive<number[]>([]);
provide<number[]>("checked", checkedTasks);
</script>
