<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script lang="ts">
import { LoadingBar } from "quasar";
import { defineComponent } from "@vue/composition-api";
import { JsPlumbToolkitVue2Plugin } from "jsplumbtoolkit-vue2";

import Vue from "vue";

Vue.use(JsPlumbToolkitVue2Plugin);

LoadingBar.setDefaults({
  color: "dark",
  size: "3px",
  position: "top"
});

export default defineComponent({
  name: "App"
});
</script>
