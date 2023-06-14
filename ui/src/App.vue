<template>
  <div id="q-app">
    <keep-alive>
      <router-view />
    </keep-alive>
  </div>
</template>
<script lang="ts">
import { LoadingBar } from 'quasar'
import Vue from 'vue'
import VueRouter from 'vue-router'
import { SecurityPlugin } from './security'
import { rest, setupWorker } from 'msw'

export const handlers = [
  // TODO: Implement flow block dispatcher here
  // It will be up to the app to load the flows first
  // e.g. let flow = ElasticCode.loadFlow("/Home/Database Example")
  // let result = flow.block("Service").run({"some":"data"})
  rest.get('/api1/', (req, res, ctx) => {

    return res(
      ctx.status(200),
      ctx.json({
        username: 'admin'
      })
    )
  })
]
const worker = setupWorker(...handlers)
worker.start({ onUnhandledRequest: 'bypass'})

Vue.use(VueRouter)
import { JsPlumbToolkitVue2Plugin } from 'jsplumbtoolkit-vue2'
import StreamPlugin from './plugins/stream-plugin'
import { domain, clientId } from '../auth_config.json'
import { Auth0Plugin } from './auth'
import router from './router'
import '@quasar/quasar-ui-qmarkdown/dist/index.css'

Vue.use(SecurityPlugin)
// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment,@typescript-eslint/no-var-requires
const VueTypedJs = require('vue-typed-js')
Vue.use(Auth0Plugin, {
  domain,
  clientId,
  onRedirectCallback: (appState: any) => {
    router.push(
      appState && appState.targetUrl
        ? appState.targetUrl
        : window.location.pathname
    )
  }
})
Vue.use(VueTypedJs)
Vue.use(StreamPlugin)
Vue.use(JsPlumbToolkitVue2Plugin)
Vue.config.silent = true

LoadingBar.setDefaults({
  color: 'dark',
  size: '3px',
  position: 'top'
})

export default Vue.extend({
  components: {
  },
  created () {
    console.log('Q', this.$q)
    console.log('VERSION', this.$store.state.designer.version)
    console.log('DEV', process.env.DEV)
    console.log('CLIENT', process.env.CLIENT)
    console.log('SERVER', process.env.SERVER)
    console.log('NODE_ENV', process.env.NODE_ENV)

  },
  mounted () {

  },
  data () {
    return {
      incrementStr: 3
    }
  },
  computed: {
    wrapper (this: { incrementStr: string }) {
      return { increment: +this.incrementStr }
    }
  }
})
</script>
