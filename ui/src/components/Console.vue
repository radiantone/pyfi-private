<template>
  <q-card
    :style="'min-height: 647px;width: '+consolewidth+'px; z-index:9999999;position: absolute; left:'+(codewidth+412)+'px;top:0px'"
  >
    <q-scroll-area style="height: 610px; width: 100%;">
      <py-repl
        id="my-repl"
        auto-generate="true"
        style="width:95%"
      />
    </q-scroll-area>
    <q-card-actions align="left">
      <q-btn
        style="position: absolute; bottom: 0px; left: 0px; width: 50px;"
        flat
        icon="far fa-arrow-alt-circle-left"
        class="bg-primary text-white"
        color="primary"
        v-close-popup
        @click="consolewidth -= 100"
      >
        <q-tooltip
          anchor="top middle"
          :offset="[-30, 40]"
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Shrink
        </q-tooltip>
      </q-btn>
      <q-btn
        style="position: absolute; bottom: 0px; left: 50px; width: 50px; margin: 0px;"
        flat
        icon="far fa-arrow-alt-circle-right"
        class="bg-accent text-dark"
        color="primary"
        v-close-popup
        @click="consolewidth += 100"
      >
        <q-tooltip
          anchor="top middle"
          :offset="[-30, 40]"
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Expand
        </q-tooltip>
      </q-btn>
      <q-btn
        style="position: absolute; bottom: 0px; left: 100px; width: 50px; margin: 0px;"
        flat
        icon="published_with_changes"
        class="bg-secondary text-accent"
        color="primary"
        v-close-popup
        @click="fetchCode"
      >
        <q-tooltip
          anchor="top middle"
          :offset="[-30, 40]"
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Fetch Code
        </q-tooltip>
      </q-btn>
      <q-btn
        style="position: absolute; bottom: 0px; left: 150px; width: 50px; margin: 0px;"
        flat
        icon="fab fa-python"
        class="bg-accent text-secondary"
        color="primary"
        v-close-popup
        @click="pythonview = !pythonview"
      >
        <q-tooltip
          anchor="top middle"
          :offset="[-30, 40]"
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Python Console
        </q-tooltip>
      </q-btn>
    </q-card-actions>
  </q-card>
</template>

<style scoped>

@import "../css/pyscript.css";

#btnRun > svg {
  color: #93b9b4 !important;
}

</style>

<script>
export default {
  name: 'Console',
  props: ['codewidth'],
  components: {},
  data () {
    return {
      consolewidth: 600
    }
  }
}
</script>
