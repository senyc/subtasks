<script setup lang="ts">
import { onMounted, ref } from "vue";
import tasks from './components/store'
const loading = ref(false);
import TaskForm from "./components/TaskForm.vue";

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

<template>
  <TaskForm />
  <section class="post">
    <div v-if="loading" class="loading">Loading...</div>
    <ul v-for="task in tasks" :key="task.id">
      <li class="task">
        <h4>{{ task.title }}</h4>
        <p>{{ task.body }}</p>
        <button @click="deleteTask(task.id)">Delete</button>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.task {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
