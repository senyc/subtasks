<template>
  <div class="px-8">
    <ProjectBreadCrumbs />
    <ProjectNavigation :page="parseInt($route.query?.page as string ?? '1')" />
    <ProjectList :page="parseInt($route.query?.page as string ?? '1')" />
  </div>
</template>

<script setup lang="ts">
import { provide, reactive, ref, watch } from 'vue';
import ProjectBreadCrumbs from '@components/projects/ProjectBreadCrumbs.vue';
import ProjectList from '@components/projects/ProjectList.vue';
import ProjectNavigation from '@components/projects/ProjectNavigation.vue';
import { useRoute, } from 'vue-router';

const checked = reactive<number[]>([])
const page = ref(1)

provide<number[]>('checked', checked)

const route = useRoute()

watch(
  () => route.query.page,
  (newPage, oldPage) => {
    page.value = parseInt(newPage as string ?? '1')
  },
  { immediate: true }
)

</script>
