import { createApp } from "vue";
import App from "./App.vue";
import { VueQueryPlugin } from "@tanstack/vue-query";
import Projects from "./views/Projects.vue";
import { createRouter, createWebHistory } from "vue-router";
import ProjectTasks from "./views/ProjectTasks.vue";

const routes = [
  { path: "", component: Projects, name: "root" },
  { path: "/projects", component: Projects, name: "projects" },
  { path: "/projects/:id/tasks", component: ProjectTasks, name: "projectTasks" },
  { path: "/projects/:id", component: Projects, name: "project" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(VueQueryPlugin).use(router).mount("#app");
