<template>
  <Header active="projects" />
  <div class="px-8">
    <ProjectBreadCrumbs show-project-name />
    <ProjectTaskNavigation
      :search="$route.query?.search as string"
      :page="parseInt(($route.query?.page as string) ?? '1')"
      :project-id="projectId"
    />
    <ProjectTaskList
      :search="$route.query?.search as string"
      :page="parseInt(($route.query?.page as string) ?? '1')"
      :project-id="projectId"
    />
  </div>
</template>

<script setup lang="ts">
import { provide, reactive } from "vue";
import { useRoute } from "vue-router";
import ProjectTaskList from "@components/tasks/ProjectTaskList.vue";
import Header from "@components/Header.vue";

import ProjectBreadCrumbs from "@components/projects/ProjectBreadCrumbs.vue";
import ProjectTaskNavigation from "@components/tasks/ProjectTaskNavigation.vue";

const route = useRoute();
const projectId = parseInt(route.params.id as string);

const checkedTasks = reactive<number[]>([]);
provide<number[]>("checked", checkedTasks);
</script>
