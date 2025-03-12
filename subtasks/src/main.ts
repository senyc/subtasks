import { createApp } from "vue";
import App from "./App.vue";
import { VueQueryPlugin } from "@tanstack/vue-query";
import Projects from "./views/Projects.vue";
import { createRouter, createWebHashHistory, } from "vue-router";
import ProjectTasks from "./views/ProjectTasks.vue";
import CompletedProjectTasks from "./views/CompletedProjectTasks.vue";
import CompletedProjects from "./views/CompletedProjects.vue";

const routes = [
  { path: "", component: Projects, name: "root" },
  { path: "/completed", component: CompletedProjects, name: "completed" },
  { path: "/projects", component: Projects, name: "projects" },
  {
    path: "/projects/completed",
    component: CompletedProjects,
    name: "completedProjects",
  },
  {
    path: "/projects/:id/tasks",
    component: ProjectTasks,
    name: "projectTasks",
  },
  {
    path: "/projects/:id/tasks/completed",
    component: CompletedProjectTasks,
    name: "completedProjectTasks",
  },
  { path: "/projects/:id", component: Projects, name: "project" },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

createApp(App).use(VueQueryPlugin).use(router).mount("#app");
