<template>
  <main>
    <Header />
    <RouterView />
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import tasks from './components/store'
const loading = ref(false);
import './index.css'
import Header from "./components/Header.vue";

async function fetchData() {
  loading.value = true

  try {
    const req = await fetch("http://localhost:8000/tasks")
    tasks.push(...await req.json())
  } finally {
    loading.value = false
  }
}

async function deleteTask(id: number) {
  const req = await fetch(`http://localhost:8000/task/${id}`, {
    method: "DELETE"
  })

  const res = await req.json() as number

  // Remove the item that was removed from local state
  tasks.splice(tasks.findIndex(task => task.id === res), 1)
}

onMounted(() => {
  fetchData()
})

</script>
