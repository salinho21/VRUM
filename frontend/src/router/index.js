import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Search from "../views/Search.vue";
import Auth from "../components/auth.vue";
import Profile from "../views/Profile"
import CriarViagem from "../views/CriarViagem"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: 'Home',
    component: Home
  },
  {
    path: "/search",
    name: 'Search',
    component: Search
  },
  {
    path: "/auth",
    name: "auth",
    component: Auth,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/criarviagem",
    name: "CriarViagem",
    component: CriarViagem,
  },

];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
