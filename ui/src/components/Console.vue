<template>
  <q-card
    :style="'min-height: 647px;width: '+consolewidth+'px; z-index:9999999;position: absolute; left:'+(codewidth+412)+'px;top:0px'"
  >
    <q-scroll-area
      id="replscroll"
      style="height: 610px; width: 100%;"
    >
      <q-input dense style="width:100%" bottom-slots v-model="text" >
        <template v-slot:after>
          <q-btn round dense flat icon="fas fa-play" @click="runPython"/>
        </template>
      </q-input>
      <div id="repl-out" style="height:500px;background-color:#ddd">{{ output }}</div>
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
  methods: {
    runPython () {
        const result = window.pyodide.runPython(this.text)
        console.log(result)
        this.output = result
    }
  },
  data () {
    return {
      text: '',
      output: '',
      consolewidth: 600
    }
  }
}
</script>
