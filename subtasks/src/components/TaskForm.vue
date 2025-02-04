<script setup lang="ts">
import { reactive } from 'vue';
import tasks from './store'
const newTask = reactive({ title: "", body: "" })

async function onSubmit() {
  const res = await fetch("http://localhost:8000/tasks", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(newTask)
  })

  // Add new task to shared state
  tasks.push(await res.json())
  // Empty fields
  newTask.body = ""
  newTask.title = ""
}
</script>

<template>
  <form @submit.prevent="onSubmit">
    <section class='form'>
      <div class="item">
        <p>title:</p>
        <input autofocus required v-model="newTask.title" type="text" />
      </div>
      <div class="item">
        <p>body:</p>
        <input v-model="newTask.body" type="text" />
      </div>
    </section>
    <input type="submit" />
  </form>
</template>

<style>
.form {
  display: flex;
  gap: 10px;
  padding-bottom: 10px;
}

.item {
  align-items: center;
  height: 36px;
  gap: 10px;
  font-size: 15px;
  display: flex;
}
</style>
