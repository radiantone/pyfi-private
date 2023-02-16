<template>
  <div
    class="aGroup"
    style="-webkit-box-shadow: 10px 9px 5px -6px rgba(0,0,0,0.21);
-moz-box-shadow: 10px 9px 5px -6px rgba(0,0,0,0.21);
box-shadow: 10px 9px 5px -6px rgba(0,0,0,0.21);padding:10px;border: black 1px solid;background-color: white; min-height: 75px; z-index: -9999;"
    :id="obj.id"

    @mouseenter="setMouseIn(false)"
  >
    <div
      style="position:absolute;right:0px;top:-35px;width:100px;height:35px"
      @mouseenter="showbuttons=true"
      @mouseleave="showbuttons=false"
    >
      <q-btn
        icon="close"
        dense
        flat
        v-if="showbuttons"
        color="primary"
        style="position:absolute;right:0px;top:0px"
      />
      <q-btn
        icon="edit"
        dense
        flat
        v-if="showbuttons"
        color="primary"
        @click="showEditor = !showEditor"
        style="position:absolute;right:30px;top:0px"
      />
    </div>

    <div
      @mouseenter="setMouseIn(true)"
      style="position:absolute;bottom:0px;left:0px;width:100%;height:35px"
    >
      <q-slider
        v-model="obj.w"
        color="primary"
        v-if="mousein"
        :step="10"
        :min="400"
        :max="3000"
        style="z-index:99999;position: absolute; padding-right:60px; left: 0px; bottom: -30px;"
      />
    </div>
    <div
      @mouseenter="setMouseIn(true)"
      style="position:absolute;top:0px;right:-35px;width:35px;height:100%;"
    >
      <q-slider
        v-model="obj.h"
        vertical
        color="primary"
        v-if="mousein"
        :step="10"
        :min="400"
        :max="3000"
        style="z-index:99999;height: 100%; position: absolute; right: 0px; top: 0px;"
      />
    </div>
    <div
      :style="
        'background-color:' +
          obj.color +
          ';min-width:' +
          myWidth +
          'px !important;height:' +
          myHeight +
          'px;'
      "
    >
      <editor
        v-model="obj.markdown"
        @init="editorInit"
        style="font-size: 16px; min-height: 100px; height:100%; margin-bottom:-50px"
        lang="python"
        theme="chrome"
        ref="myEditor"
        width="100%"
        height="100%"
        v-if="showEditor"
      />
      <q-markdown
        :src="obj.markdown"
        v-if="!showEditor"
      />
    </div>
  </div>
</template>
<style scoped>
.aGroupInner {
  width: calc(100% - 10px) !important;
}
.jtk-group {
  border: 2px solid #9e9e9e;
  z-index: 10;
  min-width: 500px;
  min-height: 300px;
}

.jtk-group.jtk-drag-hover,
.jtk-node.jtk-drag-hover {
  outline: 2px solid red;
}

.group-title {
  margin: 0;
  width: 100%;
  display: flex;
  align-items: center;
  background-color: #6b8791;
  color: white;
  font-weight: bold;
  font-family: 'Roboto', '-apple-system', 'Helvetica Neue', Helvetica, Arial,
    sans-serif;
  font-size: 20px;
  letter-spacing: 4px;
  text-transform: uppercase;
  text-indent: 7px;
  max-height: 25px;
  box-sizing: border-box;
}

.group-title button:hover {
  background-color: #f7f7f7;
}

.group-title .expand {
  margin-left: auto;
}

.group-title .group-delete {
  right: 45px;
}

.group-title .group-delete:after {
  content: 'x';
}

.group-connect {
  position: absolute;
  bottom: 10px;
  left: 10px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.jtk-group {
  background-color: #f3f3f3;
}

.jtk-group.jtk-group-collapsed {
  height: 40px;
  min-height: 0;
}

.jtk-group [jtk-group-content] {
  min-height: 210px;
  margin: 5px;
  width: auto;
}

.jtk-group.jtk-group-collapsed [jtk-group-content] {
  display: none;
  min-height: 0;
}

.jtk-connector {
  z-index: 12;
}

.jtk-node .add,
.jtk-node .delete {
  position: absolute;
  top: 3px;
}
</style>
<style src="@quasar/quasar-ui-qmarkdown/dist/index.css"></style>

<script>
import { v4 as uuidv4 } from 'uuid'

import { QMarkdown } from '@quasar/quasar-ui-qmarkdown'

export default {
  name: 'BorderTemplate',
  components: {
    QMarkdown,
    editor: require('vue2-ace-editor')
  },
  computed: {
    myWidth () {
      var mywidth = this.obj.w > 0 ? this.obj.w : 'auto'
      return mywidth
    },
    myHeight () {
      return this.obj.h ? this.obj.h : 'auto'
    }
  },
  mounted () {
    var me = this
    this.toolkit = window.toolkit
  },
  created () {
  },
  watch: {
  },
  data () {
    return {
      showEditor: false,
      mousein: false,
      showbuttons: false,
      key: 1,
      obj: {
        w: 500,
        h: 200,
        name: 'Border Title',
        color: '',
        markdown: `:::
This is a **test** of markdown
:::`
      },
      showing: false,
      title: 'Chapter 1',
      savePatternDialog: false,
      patternName: '',
      disabled: false,
      dimension: 500,
      deleteGroup: false,
      icon: 'fas fa-minus'
    }
  },
  methods: {
    setMouseIn (val) {
      this.mousein = val
    },
    editorInit: function () {
      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/markdown') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      console.log('editorInit')
      const editor = this.$refs.myEditor.editor

      editor.setAutoScrollEditorIntoView(true)
      editor.focus()
    },
    setLayer () {
      console.log('setLayer')
      this.mousein = !this.mousein
      this.$el.style.zIndex = -999999
      this.showEditor = false
    },
    savePattern () {
      var me = this
      this.savePatternDialog = false
      var el = document.getElementById(this.obj.id + 'inner')
      this.showing = true

      var code = JSON.parse(
        JSON.stringify(window.toolkit.getGraph().serialize(), null, '\t')
      )

      // Got to find the id of this group
      var gid = this.getGroup().id

      var edges = []
      var ports = []
      var nodes = []

      code.nodes.forEach((node) => {
        if (node.group && node.group === gid) {
          nodes.push(node)

          code.edges.forEach((edge) => {
            if (edge.source.indexOf(node.id) === 0) {
              edges.push(edge)
            }
          })
          code.ports.forEach((port) => {
            if (port.id.indexOf(node.id) === 0) {
              ports.push(port)
            }
          })
        }
      })
      var pattern = {
        groups: [this.getGroup().data],
        edges: edges,
        ports: ports,
        nodes: nodes
      }

      console.log('SAVE PATTERN CODE', code)
      console.log('SAVE PATTERN', pattern)

      htmlToImage
        .toPng(el)
        .then(function (dataUrl) {
          var img = new Image()
          img.src = dataUrl
          window.root.$emit(
            'save.pattern',
            uuidv4(),
            me.patternName,
            img.src,
            pattern
          )
          console.log('IMAGE2', me.patternName, img)
          me.showing = false
        })
        .catch(function (error) {
          me.showing = false
          console.error('oops, something went wrong!', error)
        })
    },
    deleteAGroup (all) {
      debugger
      console.log('Removing group', this.obj)
      window.toolkit.removeGroup(this.obj, all)
    },
    resize: function () {},
    saveTrope () {},
    groupSettings: function () {
      var me = this
      console.log('new.group.dialog', this.obj)
      this.$root.$emit('new.group.dialog', {
        obj: this.obj,
        callback: (object) => {
          console.log(object)
          me.obj = object
        }
      })
    },
    remove: function () {
      console.log(this.obj)
      var group = this.toolkit.getObjectInfo(this.obj)

      this.toolkit.removeGroup(group.obj, true)
    },
    click: function () {
      this.toolkit.renderer.toggleGroup(this.obj)
      if (this.icon === 'fas fa-minus') {
        this.icon = 'fas fa-plus'
      } else {
        this.icon = 'fas fa-minus'
      }
    }
  }
}
</script>
saveTrope
