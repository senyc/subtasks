<template>
  <div class="px-8">
    <ProjectBreadCrumbs />
    <ProjectNavigation
      :page="parseInt(($route.query?.page as string) ?? '1')"
    />
    <ProjectList :page="parseInt(($route.query?.page as string) ?? '1')" />
  </div>
</template>

<script setup lang="ts">
import { provide, reactive } from "vue";
import ProjectBreadCrumbs from "@components/projects/ProjectBreadCrumbs.vue";
import ProjectList from "@components/projects/ProjectList.vue";
import ProjectNavigation from "@components/projects/ProjectNavigation.vue";

const checked = reactive<number[]>([]);

provide<number[]>("checked", checked);
</script>
