<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script lang="ts">
import { LoadingBar } from "quasar";
import { defineComponent } from "@vue/composition-api";
import { JsPlumbToolkitVue2Plugin } from "jsplumbtoolkit-vue2";
import BetterCounter from "components/BetterCounter.vue";
import StreamPlugin from "./plugins/stream-plugin";

import Vue from "vue";
import Vuetify from "vuetify";
//import VueD3 from 'vue2-d3';

//Vue.use(VueD3)
Vue.use(StreamPlugin);
Vue.use(Vuetify);
Vue.use(JsPlumbToolkitVue2Plugin);

LoadingBar.setDefaults({
  color: "dark",
  size: "3px",
  position: "top"
});

export default Vue.extend({
  components: {
  },
  data() {
    return {
      incrementStr: 3,
    };
  },
  computed: {
    wrapper(this: { incrementStr: string }) {
      return { increment: +this.incrementStr };
    },
  },
});
</script>
