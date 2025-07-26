import { createApp } from "vue";
import App from "./App.vue";
import { VueQueryPlugin } from "@tanstack/vue-query";
import Projects from "./views/Projects.vue";
import { createRouter, createWebHashHistory } from "vue-router";
import ProjectTasks from "./views/ProjectTasks.vue";
import CompletedProjectTasks from "./views/CompletedProjectTasks.vue";
import CompletedProjects from "./views/CompletedProjects.vue";
import Tasks from "./views/Tasks.vue";
import CompletedTasks from "./views/CompletedTasks.vue";
import Tags from "./views/Tags.vue";
import Calendar from "./views/Calendar.vue";

const routes = [
  { path: "", component: Projects, name: "root" },
  { path: "/projects", component: Projects, name: "projects" },
  { path: "/completed", component: CompletedProjects, name: "completed" },
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
  { path: "/tasks", component: Tasks, name: "tasks" },
  { path: "/tasks/tags/edit", component: Tags, name: "tags" },
  {
    path: "/tasks/completed",
    component: CompletedTasks,
    name: "completedTasks",
  },
  { path: "/calendar/", component: Calendar, name: "calendar" },
  { path: "/calendar/:span/", component: Calendar, name: "calendarspan" },
  {
    path: "/calendar/:span/:year/:month/:day",
    component: Calendar,
    name: "calendarspanfulldate",
  },
  {
    path: "/calendar/:span/:year/:month",
    component: Calendar,
    name: "calendarspanmonth",
  },
  {
    path: "/calendar/:span/:year",
    component: Calendar,
    name: "calendarspanyear",
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

createApp(App).use(VueQueryPlugin).use(router).mount("#app");
