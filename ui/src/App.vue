<template>
  <div id="q-app">
    <keep-alive>
      <router-view />
    </keep-alive>
  </div>
</template>
<script lang="ts">
import { LoadingBar } from 'quasar'
import { JsPlumbToolkitVue2Plugin } from 'jsplumbtoolkit-vue2'
import StreamPlugin from './plugins/stream-plugin'

// import FloatingVue from 'floating-vue';
import Vue from 'vue'
import Vuetify from 'vuetify'
//import { createApp } from 'vue'
//import { createPinia } from 'pinia'

// import { VueTypedJs } from 'vue-typed-js';
// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment,@typescript-eslint/no-var-requires
const VueTypedJs = require('vue-typed-js')
//const pinia = createPinia()

//Vue.use(pinia)
Vue.use(VueTypedJs)
// import VueD3 from 'vue2-d3';
// Vue.use(VueD3)
// Vue.use(FloatingVue);
Vue.use(StreamPlugin)
Vue.use(Vuetify)
Vue.use(JsPlumbToolkitVue2Plugin)
Vue.config.silent = true

LoadingBar.setDefaults({
  color: 'dark',
  size: '3px',
  position: 'top'
})

let log = console.log
console.log = function () {
  // Invoke the original method with an additional parameter
  log.apply(console,
    [("[" + new Date().toLocaleString() + "] ")].concat([].slice.call(arguments))
  )
}

export default Vue.extend({
  components: {
  },
  created () {
    console.log('Q', this.$q)
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
