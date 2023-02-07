<template>
  <q-card
    style="min-height: 100%;width: 100%;"
  >
    <q-splitter
      v-model="queueTableSplitter"
      separator-style="background-color: #e3e8ec;height:5px"
      horizontal
      style="height: calc(100vh - 140px);"
    >
      <template #before>
        <editor
          v-model="code"
          @init="editorInit"
          style="font-size: 16px; min-height: 100px;margin-bottom:-50px"
          lang="python"
          theme="chrome"
          ref="myEditor"
          width="100%"
          height="100%"
        />
        <q-toolbar>
          <q-space/>
          <q-btn
          round
          dense
          flat
          color="secondary"
          title="Execute Python Code"
          icon="fas fa-play"
          style="margin-right:10px"
          @click="runPython"
        />
        </q-toolbar>
      </template>
      <template #after>
        <q-scroll-area style="height: 100%; width: 100%;">
        <pre
          id="repl-out"
          style="height:100vh;background-color:#fff;padding:10px"
        />
        </q-scroll-area>
      </template>
    </q-splitter>
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
  components: {
    editor: require('vue2-ace-editor')
  },
  methods: {
    editorInit: function () {
      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      console.log('editorInit')
      const editor = this.$refs.myEditor.editor

      editor.setAutoScrollEditorIntoView(true)

      setTimeout(function () {
        // me.thecode = me.obj.code;
      }, 500)
    },
    runPython () {
      const result = window.pyodide.runPython(this.code)

      debugger
      console.log(result)
      this.output = result
    }
  },
  data () {
    return {
      queueTableSplitter: 40,
      code: '',
      text: '',
      output: '',
      consolewidth: 600
    }
  }
}
</script>
