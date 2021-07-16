import { RouteConfig } from 'vue-router'

import MainLayout from 'layouts/MainLayout.vue'
import Designer from 'src/pages/Designer.vue'

const routes: RouteConfig[] = [

  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/Designer.vue') }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
