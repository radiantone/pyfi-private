import { RouteConfig } from 'vue-router'
// import { LoginCallback } from '@okta/okta-vue'

const routes: RouteConfig[] = [

  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/Designer.vue') }]
  },
  {
    path: '/app',
    component: () => import('layouts/AppLayout.vue')
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }, //,
  // { path: '/login/callback', component: LoginCallback }
  {
    path: '/profile',
    name: 'profile',
    component: () => import('components/Profile.vue')
  },
  {
    path: '/logout',
    name: 'logout',
    component: () => import('pages/Logout.vue')
  }
]

export default routes
