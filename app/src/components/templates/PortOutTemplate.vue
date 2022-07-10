<template>
  <div
    class="table node shadow-1 jtk-node"
    style="overflow: unset !important; border-radius: 15px;"
    id="jtknode"
    :style="
      'top:' + obj.y + ';left:' + obj.x + ';min-width:' + obj.width + '; '
    "
    @touchstart.stop
    @contextmenu.stop
  >
    <q-menu context-menu style="border: 1px solid black;">
      <q-list dense>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-cog"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            Configure
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="far fa-times-circle"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">Disable</q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-database"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View Provenance Data
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fa fa-area-chart"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View Status History
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-list"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View State
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-book"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View Usage
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-plug"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View Connections
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="far fa-object-group"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            Center in View
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-palette"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            Change Color
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="far fa-object-group"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">Group</q-item-section>
        </q-item>
        <q-separator />

        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-project-diagram"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            Create Template
          </q-item-section>
        </q-item>
        <q-separator />

        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-copy"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">Copy</q-item-section>
        </q-item>
        <q-separator />

        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-trash"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">Delete</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
    <div
      class="name"
      style="background: white; height: 90px; border-top-left-radius: 15px;"
    >
      <div
        title="Port Out"
        style="
          margin-top: -15px;
          padding: 10px;
          font-weight: normal;
          padding-left: 2px;
          font-size: 40px;
          margin-right: 5px;
        "
      >
        <i
          :class="obj.icon + ' text-secondary'"
          style="transform: rotate(90deg);"
        />
      </div>
      <span
        style="position: absolute; left: 50px; font-size: 20px; top: 5px;"
        class="text-black"
      >
        <span>{{ obj.name }}</span>
      </span>
      <span
        class="text-secondary"
        style="position: absolute; left: 50px; top: 31px; font-size: 14px;"
      >
        {{ obj.description }}
      </span>
      <span
        class="text-blue-grey-8"
        style="position: absolute; left: 50px; top: 51px; font-size: 11px;"
      >
        {{ obj.package }}
      </span>
      <span
        class="text-red"
        style="position: absolute; left: 50px; top: 70px; font-size: 11px;"
      >
        Error messages
      </span>
      <span
        class="text-blue-grey-8 pull-right"
        style="position: absolute; right: 10px; top: 50px; font-size: 11px;"
      >
        v1.2.2
      </span>
      <div class="buttons" style="position: absolute; right: 00px; top: 68px;">
        <div
          class="text-secondary"
          @click="bandwidth = !bandwidth"
          style="margin-right: 10px;"
        >
          <i class="fas fa-tachometer-alt" style="cursor: pointer;" />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Bandwidth Toggle
          </q-tooltip>
        </div>
        <div
          class="text-secondary"
          @click="addNewPort('Input', 'outlet-icon')"
          style="margin-right: 10px;"
        >
          <i class="outlet-icon" style="cursor: pointer;" />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Socket
          </q-tooltip>
        </div>

        <div style="position: absolute; right: 8px; top: 0px;">
          <q-btn
            dense
            flat
            size="xs"
            icon="fa fa-cog"
            @click="showPanel('configview', !configview)"
            class="edit-name text-secondary"
            style="
              position: absolute;
              right: 45px;
              top: -68px;
              width: 30px;
              height: 30px;
            "
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Configure
            </q-tooltip>
          </q-btn>
          <q-btn
            icon="fas fa-times"
            size="xs"
            @click="deleteConfirm = true"
            flat
            dense
            class="new-column add text-secondary"
            style="
              position: absolute;
              right: 20px;
              top: -68px;
              width: 30px;
              height: 30px;
            "
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Delete
            </q-tooltip>
          </q-btn>
        </div>
        <q-btn-dropdown
          flat
          content-class="text-dark bg-white"
          dense
          color="secondary"
          padding="0px"
          style="
            position: absolute;
            right: 0px;
            width: 30px;
            height: 30px;
            top: -68px;
          "
        >
          <q-list dense>
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fas fa-save"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Save
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fas fa-refresh"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Refresh
              </q-item-section>
            </q-item>
            <q-separator />

            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="far fa-comments"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Comments
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fab fa-github"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Git
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fas fa-history"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                History
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fas fa-glasses"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Logs
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fas fa-lock"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Security
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="far fa-list-alt"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Environment
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fas fa-server"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Scaling
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
    </div>
    <ul class="table-columns" v-for="column in obj.columns" :key="column.id">
      <li
        :class="
          'table-column jtk-droppable table-column-type-' + column.datatype
        "
        :style="
          'background:' +
          column.background +
          ';border-top: 1px dashed lightgrey'
        "
        :primary-key="column.primaryKey"
        :data-port-id="column.id"
      >
        <div class="table-column-edit text-primary">
          <i
            class="fa fa-times table-column-delete-icon"
            title="Delete Port"
            @click="confirmDeleteSpeech(column.id)"
          />
        </div>
        <div class="table-column-edit text-primary">
          <i
            class="fas fa-edit"
            title="Edit Argument"
            style="margin-right: 5px;"
            @click=""
          />
        </div>
        <div>
          <div class="float-left text-secondary">
            <i
              :class="column.icon"
              :title="column.name"
              style="margin-right: 5px;"
            />
          </div>
          <span>{{ column.name }} : {{ column.description }}</span>
          <q-popup-edit
            style="
              width: 50%;
              font-weight: bold;
              font-size: 25px;
              font-family: 'Indie Flower', cursive;
              margin-top: 5px;
            "
            v-model="column.name"
            @save="updateName"
          >
            <q-input
              style="
                font-weight: bold;
                font-size: 25px;
                font-family: 'Indie Flower', cursive;
                margin-top: 5px;
              "
              v-model="column.name"
              dense
              autofocus
            />
          </q-popup-edit>
        </div>

        <jtk-source
          name="source"
          :port-id="column.id"
          :scope="column.datatype"
          filter=".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon"
          filter-exclude="true"
        />

        <jtk-target
          name="target"
          :port-id="column.id"
          :scope="column.datatype"
        />
      </li>
    </ul>

    <q-separator />
    <div class="row" id="bandwidth" style="" v-if="bandwidth">
      <q-table
        dense
        hide-header
        hide-bottom
        :data="data"
        :columns="columns"
        row-key="name"
        style="
          border-bottom-left-radius: 15px;
          border-bottom-right-radius: 15px;
          width: 100%;
          border-top-radius: 0px;
          border-bottom-radius: 0px;
        "
      />
    </div>
    <q-dialog v-model="deleteItem" persistent>
      <q-card style="padding: 10px; padding-top: 30px;">
        <q-card-section
          class="bg-secondary"
          style="
            position: absolute;
            left: 0px;
            top: 0px;
            width: 100%;
            height: 40px;
          "
        >
          <div
            style="
              font-weight: bold;
              font-size: 18px;
              color: white;
              margin-left: 10px;
              margin-top: -5px;
              margin-right: 5px;
              color: #fff;
            "
          >
            <q-toolbar>
              <q-item-label>Delete Item</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-trash" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Are you sure you want to delete this item?
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
            flat
            label="Cancel"
            class="bg-accent text-dark"
            color="primary"
            v-close-popup
          />
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Delete"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="removeColumn(deleteSpeechID)"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="code" persistent>
      <q-card style="max-width: 100vw; width: 1500px;">
        <q-card-section class="row items-center bg-primary text-white">
          <q-toolbar>
            <h5 style="margin: 0px;">
              {{ this.obj.name }} - {{ this.obj.description }}
            </h5>
            <q-space />
            <q-btn
              flat
              round
              dense
              icon="close"
              class="text-white"
              v-close-popup
            ></q-btn>
          </q-toolbar>
        </q-card-section>
        <q-card-section class="row items-center">
          <editor
            v-model="obj.code"
            @init="editorInit"
            style="font-size: 25px; min-height: 60vh;"
            lang="python"
            theme="chrome"
            ref="myEditor"
            width="100%"
            height="fit"
          ></editor>
          <q-btn>Save</q-btn>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            label="Close"
            class="bg-primary text-white"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="deleteConfirm" persistent>
      <q-card style="padding: 10px; padding-top: 30px;">
        <q-card-section
          class="bg-secondary"
          style="
            position: absolute;
            left: 0px;
            top: 0px;
            width: 100%;
            height: 40px;
          "
        >
          <div
            style="
              font-weight: bold;
              font-size: 18px;
              color: white;
              margin-left: 10px;
              margin-top: -5px;
              margin-right: 5px;
              color: #fff;
            "
          >
            <q-toolbar>
              <q-item-label>Delete Item</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-trash" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Are you sure you want to delete this item?
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
            flat
            label="Cancel"
            class="bg-accent text-dark"
            color="primary"
            v-close-popup
          />
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Delete"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="deleteNode"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="codeview"
    >
      <q-card-section
        style="padding: 5px; z-index: 999999; padding-bottom: 10px;"
      >
        <editor
          v-model="obj.code"
          @init="editorInit"
          style="font-size: 16px; min-height: 60vh;"
          lang="python"
          theme="chrome"
          ref="myEditor"
          width="100%"
          height="fit"
        ></editor>
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish To Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="codeview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>
    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="configview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 400px;
        "
      >
        Config view
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish to Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="configview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>
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
import { BaseNodeComponent } from "jsplumbtoolkit-vue2";
import { v4 as uuidv4 } from "uuid";
import VueResizable from "vue-resizable";

export default {
  name: "PortOutTemplate",
  mixins: [BaseNodeComponent],
  components: {
    editor: require("vue2-ace-editor"),
    VueResizable,
  },
  created() {
    var me = this;
    console.log("me.tooltips ", me.tooltips);
    console.log("start listening for show.tooltips");
    window.root.$on("show.tooltips", (value) => {
      console.log("start tooltips:", value);
      me.tooltips = value;
      console.log("ME:", me);
      console.log("TOOLTIPS", me.tooltips);
    });
  },
  data() {
    return {
      obj: {},
      text: "",
      configview: false,
      deleteSpeechID: null,
      sidecode: true,
      bandwidth: true,
      columns: [
        {
          name: "name",
          label: "Name",
          field: "name",
          align: "left",
        },
        {
          name: "bytes",
          align: "center",
          label: "Bytes",
          field: "bytes",
        },
        {
          name: "time",
          align: "right",
          classes: "text-secondary",
          label: "Time",
          field: "time",
        },
      ],
      data: [
        {
          name: "In",
          bytes: "0 (0 bytes)",
          time: "5 min",
        },
        {
          name: "Read/Write",
          bytes: "0 (0 bytes)",
          time: "5 min",
        },
        {
          name: "Out",
          bytes: "0 (0 bytes)",
          time: "5 min",
        },
        {
          name: "Tasks/Time",
          bytes: "0 (0 bytes)",
          time: "5 min",
        },
      ],
      codeview: false,
      entityName: "",
      columnName: "",
      thecode: "",
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
        backgroundColor: "rgba(0,0,0,0.02)",
        color: "#555",
      },

      contentActiveStyle: {
        backgroundColor: "#eee",
        color: "black",
      },

      thumbStyle: {
        right: "2px",
        borderRadius: "5px",
        backgroundColor: "#027be3",
        width: "5px",
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
      console.log("updateDesc", value, initialValue);
      this.renameConfirm = true;
      this.renameValue = value;
      this.initialValue = initialValue;
    },
    updateName(value, initialValue) {
      console.log("updateName", value, initialValue);
      this.renameConfirm = true;
      this.renameValue = value;
      this.initialValue = initialValue;
    },
    editorInit: function () {
      var me = this;

      require("brace/ext/language_tools"); // language extension prerequsite...
      require("brace/mode/html");
      require("brace/mode/python"); // language
      require("brace/mode/less");
      require("brace/theme/chrome");
      require("brace/snippets/javascript"); // snippet
      console.log("editorInit");
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
    showSpeakerDialog(tab) {
      // this.$root.$emit("show.speaker.tab",tab);
      window.root.$emit("new.speaker.dialog", {
        mode: "edit",
        tab: tab,
        obj: this.obj,
      });
      console.log("show speaker dialog");
    },
    confirmDeleteSpeech(id) {
      this.deleteSpeechID = id;
      this.deleteItem = true;
    },
    resetToolkit() {
      console.log("emitting toolkit.dirty");
      this.$root.$emit("toolkit.dirty", false);
    },
    valueChanged() {
      console.log("emitting toolkit.dirty");
      this.$root.$emit("toolkit.dirty", true);
    },
    deleteNode() {
      window.toolkit.removeNode(this.obj);
    },
    removeColumn(column) {
      console.log("Removing column: ", column);

      for (var i = 0; i < this.obj.columns.length; i++) {
        var col = this.obj.columns[i];
        console.log(col);
        if (col.id == column) {
          console.log("Deleted column");
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
          edge.data.label == column
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
      port.background = "white";
      port.datatype = "Column";
      port.id = "speech" + uuidv4();

      console.log("Port:", port);
      window.toolkit.addNewPort(this.obj.id, "column", port);
      window.renderer.repaint(this.obj);
      console.log("Firing node updated...");

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
          color: "negative",
          timeout: 2000,
          position: "bottom",
          message: "Error is already created",
          icon: "fas fa-exclamation",
        });
        return;
      }
      this.addPort({
        name: "Error",
        icon: "fas fa-exclamation",
        type: "Error",
      });
      this.error = true;
    },
    showNewSpeechDialog() {
      var me = this;
      this.$refs.speechDialog.showDialog(
        {
          name: "Test",
          icon: "fas fa-cube",
          display: "Always",
          description: "A description",
          package: "A package",
          grouped: false,
          type: "Argument",
          properties: [],
          conditionals: [],
          rules: [],
          notes: [],
        },
        "New",
        function (obj) {
          me.addPort(obj);
        }
      );
    },
    showEditSpeechDialog(data) {
      console.log("New speech dialog");
      var me = this;
      this.$refs.speechDialog.showDialog(data, "Edit", function (obj) {
        me.addPort(obj);
      });
    },
    showEditEntityDialog() {
      console.log("show Edit entity");
      window.root.$emit("new.speaker.dialog", {
        mode: "edit",
        obj: this.obj,
      });
    },
    selectNode: function () {
      console.log("selected: ", this.obj.id);
      window.root.$emit("node.selected", this.obj);
    },
    deleteEntity: function (name) {
      this.entityName = name;
      this.confirm = true;
    },
    clicked: function () {
      console.log("clicked");
    },
  },
};
</script>
