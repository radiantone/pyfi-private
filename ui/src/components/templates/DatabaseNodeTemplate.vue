<template>
  <div
    class="aGroup"
    style="min-height: 75px; z-index: -9999;"
    :id="obj.id"
    @mouseenter="setMouseIn(false)"
  >
    <div
      style="position:absolute;left:0px;top:-15px;width:120px;height:120px"
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
        icon="menu"
        dense
        flat
        v-if="showbuttons"
        color="primary"
        style="position:absolute;right:30px;top:0px"
      />
    </div>
    <q-icon name="las la-database" color="secondary"  style="z-index:-9999;font-size:8em"/>
        <q-item-label style="position:absolute;bottom:-1.2em;min-width:300px;left:-90px;text-align: center;margin:auto;width:50%;font-family: 'Indie Flower', cursive;font-size:2em;font-weight:bold;">
      {{ obj.name }}
      <q-popup-edit
        v-model="obj.name"
        buttons
      >
        <q-input
          type="string"
          v-model="obj.name"
          dense
          autofocus
          color="white"
        />
      </q-popup-edit>
    </q-item-label>
    <div class=" jtk-droppable" data-port-name="queue" data-port-template="Object" data-port-event="queue" data-port-id="DatabaseOutput" style="cursor:pointer;border-radius: 10px;  background-color:#6b8791;position:absolute;top:calc(40% - 1px);right:-12px;min-width:25px;min-height:25px;">
      <jtk-source type="Output" name="source" port-template="Object" port-id="InputQueue" port-type="Output" scope="Column" filter=".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon" filter-exclude="true"/>
     </div>
    <div class=" jtk-droppable" data-port-name="queue" data-port-template="Object" data-port-event="queue" data-port-id="DatabaseInput" style="cursor:pointer;border-radius: 10px;  background-color:#6b8791;position:absolute;top:calc(40% - 1px);left:-12px;min-width:25px;min-height:25px;">
      <jtk-target type="Input" name="target" port-template="Object" port-id="OutputQueue" port-type="Input" scope="Column" filter=".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon" filter-exclude="true"/>
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
/* eslint-disable @typescript-eslint/no-this-alias, @typescript-eslint/restrict-plus-operands, @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-call,@typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access */

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
    const me = this
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
        name: 'Queue',
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
    resize: function () {},
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
