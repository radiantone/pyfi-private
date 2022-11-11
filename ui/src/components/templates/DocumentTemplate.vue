<template>
  <div
    class="node jtk-node las la-file fa-5x text-primary"
    @mouseleave="showTooltip(false)"
    @mouseover="showTooltip(true)"
    style="
      color: primary;
      text-size: 0.8em;
      max-width: 100px;
      height: 100px;
      border: black 1px;
    "
  >
    <div
      v-if="true"
      class="text-center"
      style="
        color: black;
        position: relative;
        top: -90px;
        left: -80px;
        min-height: 100px;
        padding-left: 20px;
        font-size: 0.3em;
        font-family: 'Indie Flower', cursive;
        margin-top: 5px;
        width: 200px;
      "
    >
      <q-scroll-area
        class="text-center"
        style="height: 50px; width: 100%;"
        :content-style="contentStyle"
        :thumb-style="thumbStyle"
        :content-active-style="contentActiveStyle"
        ><span style="height: 200px;">
          <q-popup-edit v-model="obj.name" title="Start Label" buttons>
            <q-input
              type="string"
              v-model="obj.name"
              dense
              autofocus
            /> </q-popup-edit
          >{{ this.obj.name }}</span
        ></q-scroll-area
      >
    </div>
    <div
      class="jtk-droppable"
      data-port-name="Document"
      data-port-event="env"
      data-port-id="Document"
      style="
        cursor: pointer;
        position: absolute;
        top: 25px;
        left: 25px;
        min-width: 20px;
        min-height: 20px;
      "
    >
      <jtk-source
        name="source"
        port-id="Document"
        port-type="Output"
        scope="Column"
        filter=".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon"
        filter-exclude="true"
      />
    </div>
  </div>
</template>

<style>
.q-item {
  margin-right: 0px;
}
.ace-editor {
  width: 100%;
  height: 100%;
}
tbody tr:nth-child(odd) {
  background-color: rgb(244, 246, 247) !important;
}

.q-menu {
  border-radius: 0px;
}
.ace_gutter > .ace_layer {
  background-color: #e3e8ec;
}
.resizable-content {
}
</style>
<script>
import { BaseNodeComponent } from 'jsplumbtoolkit-vue2';
import { v4 as uuidv4 } from 'uuid';

export default {
  name: 'PortInTemplate',
  mixins: [BaseNodeComponent],
  components: {
    editor: require('vue2-ace-editor')
  },
  created() {
    var me = this;
    console.log('me.tooltips ', me.tooltips);
    console.log('start listening for show.tooltips');
    window.root.$on('show.tooltips', (value) => {
      console.log('start tooltips:', value);
      me.tooltips = value;
      console.log('ME:', me);
      console.log('TOOLTIPS', me.tooltips);
    });
  },
  data() {
    return {
      collapsed: false,
      obj: {
        icon: 'fab fa-python',
        style: '',
        x: 0,
        y: 0,
        type: 'script',
        name: 'Document',
        label: 'Script',
        description: 'A script processor description',
        package: 'my.python.package',
        disabled: false,
        columns: [],
        properties: [],
      },
      text: '',
      configview: false,
      deleteSpeechID: null,
      sidecode: true,
      bandwidth: true,
      columns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left',
        },
        {
          name: 'bytes',
          align: 'center',
          label: 'Bytes',
          field: 'bytes',
        },
        {
          name: 'time',
          align: 'right',
          classes: 'text-secondary',
          label: 'Time',
          field: 'time',
        },
      ],
      data: [
        {
          name: 'In',
          bytes: '0 (0 bytes)',
          time: '5 min',
        },
        {
          name: 'Read/Write',
          bytes: '0 (0 bytes)',
          time: '5 min',
        },
        {
          name: 'Out',
          bytes: '0 (0 bytes)',
          time: '5 min',
        },
        {
          name: 'Tasks/Time',
          bytes: '0 (0 bytes)',
          time: '5 min',
        },
      ],
      codeview: false,
      entityName: '',
      columnName: '',
      thecode: '',
      tooltips: false,
      tooltip: false,
      code: false,
      ports: {
        next: false,
        error: false,
        join: false,
        split: false,
        complete: false,
      },
      confirm: false,
      deleteItem: false,
      deleteConfirm: false,
      prompt: false,
      contentStyle: {
        backgroundColor: 'rgba(0,0,0,0.02)',
        color: '#555',
      },

      contentActiveStyle: {
        backgroundColor: '#eee',
        color: 'black',
      },

      thumbStyle: {
        right: '2px',
        borderRadius: '5px',
        backgroundColor: '#027be3',
        width: '5px',
        opacity: 0.75,
      },
    };
  },
  methods: {
    showPanel(view, show) {
      this.configview = false;
      this.codeview = false;
      this[view] = show;
    },
    updateDescription(value, initialValue) {
      console.log('updateDesc', value, initialValue);
      this.renameConfirm = true;
      this.renameValue = value;
      this.initialValue = initialValue;
    },
    updateName(value, initialValue) {
      console.log('updateName', value, initialValue);
      this.renameConfirm = true;
      this.renameValue = value;
      this.initialValue = initialValue;
    },
    editorInit: function () {
      var me = this;

      require('brace/ext/language_tools'); // language extension prerequsite...
      require('brace/mode/html');
      require('brace/mode/python'); // language
      require('brace/mode/less');
      require('brace/theme/chrome');
      require('brace/snippets/javascript'); // snippet
      console.log('editorInit');
      const editor = this.$refs.myEditor.editor;

      editor.setAutoScrollEditorIntoView(true);

      setTimeout(function () {
        // me.thecode = me.obj.code;
      }, 500);
    },
    showCode() {
      // this.code = true;
    },
    showTooltip(show) {
      this.tooltip = show;
    },
    confirmDeleteSpeech(id) {
      this.deleteSpeechID = id;
      this.deleteItem = true;
    },
    resetToolkit() {
      console.log('emitting toolkit.dirty');
      this.$root.$emit('toolkit.dirty', false);
    },
    valueChanged() {
      console.log('emitting toolkit.dirty');
      this.$root.$emit('toolkit.dirty', true);
    },
    deleteNode() {
      window.toolkit.removeNode(this.obj);
    },
    removeColumn(column) {
      console.log('Removing column: ', column);

      for (var i = 0; i < this.obj.columns.length; i++) {
        var col = this.obj.columns[i];
        console.log(col);
        if (col.id === column) {
          console.log('Deleted column');
          this.obj.columns.splice(i, 1);
          break;
        }
      }

      var edges = window.toolkit.getAllEdges();

      for (var i = 0; i < edges.length; i++) {
        console.log(edge);
        const edge = edges[i];
        console.log(
          edge.source.getNode().id,
          this.obj.id,
          edge.data.label,
          column
        );
        if (
          edge.source.getNode().id === this.obj.id &&
          edge.data.label === column
        ) {
          window.toolkit.removeEdge(edge);
        }
      }
      // Delete all the edges for this column id
      console.log(this.obj);
      window.toolkit.removePort(this.obj.id, column);
      // window.renderer.repaint(this.obj);
    },
    addPort(port) {
      port.background = 'white';
      port.datatype = 'Column';
      port.id = 'speech' + uuidv4();

      console.log('Port:', port);
      window.toolkit.addNewPort(this.obj.id, 'column', port);
      window.renderer.repaint(this.obj);
      console.log('Firing node updated...');

      console.log(this.obj.columns);
    },
    addNewPort(name, icon) {
      this.addPort({
        name: name,
        icon: icon,
        type: name,
      });
      this.ports[name] = true;
    },
    addErrorPort() {
      if (this.error) {
        this.$q.notify({
          color: 'negative',
          timeout: 2000,
          position: 'bottom',
          message: 'Error is already created',
          icon: 'fas fa-exclamation',
        });
        return;
      }
      this.addPort({
        name: 'Error',
        icon: 'fas fa-exclamation',
        type: 'Error',
      });
      this.error = true;
    },
    showNewSpeechDialog() {
      var me = this;
      this.$refs.speechDialog.showDialog(
        {
          name: 'Test',
          icon: 'fas fa-cube',
          display: 'Always',
          description: 'A description',
          package: 'A package',
          grouped: false,
          type: 'Argument',
          properties: [],
          conditionals: [],
          rules: [],
          notes: [],
        },
        'New',
        function (obj) {
          me.addPort(obj);
        }
      );
    },
    showEditSpeechDialog(data) {
      var me = this;
      this.$refs.speechDialog.showDialog(data, 'Edit', function (obj) {
        me.addPort(obj);
      });
    },
    showEditEntityDialog() {
      window.root.$emit('new.speaker.dialog', {
        mode: 'edit',
        obj: this.obj,
      });
    },
    selectNode: function () {
      console.log('selected: ', this.obj.id);
      window.root.$emit('node.selected', this.obj);
    },
    deleteEntity: function (name) {
      this.entityName = name;
      this.confirm = true;
    },
    clicked: function () {
      console.log('clicked');
    },
  },
};
</script>
