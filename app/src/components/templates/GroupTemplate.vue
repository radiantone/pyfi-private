<template>
  <div
    class="aGroup"
    style="border: 2px dashed black; min-height: 150px; z-index: -100;"
    id="jtkgroup"
  >
    <q-slider
      v-model="obj.w"
      color="primary"
      v-if="icon === 'fas fa-minus'"
      :step="10"
      :min="400"
      :max="3000"
      style="position: absolute; left: 0px; top: -30px;"
    />
    <q-slider
      v-model="obj.h"
      vertical
      color="primary"
      v-if="icon === 'fas fa-minus'"
      :step="10"
      :min="400"
      :max="3000"
      style="height: 100%; position: absolute; left: -30px; top: 0px;"
    />
    <h4 class="group-title">
      <span style="min-width: 500px;">
        {{ obj.name }}
        <i class="fas fa-edit text-primary" style="cursor: pointer;">
          <q-popup-edit
            style="font-size: 15px; margin-top: 5px;"
            v-model="obj.name"
          >
            <q-input style="" v-model="obj.name" dense autofocus />
          </q-popup-edit>
        </i>
      </span>
      <q-toolbar>
        <q-space />
        <q-btn
          flat
          size="xs"
          class="bg-secondary"
          icon="fas fa-save"
          @click="savePatternDialog = true"
        >
          <q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Save as Pattern
          </q-tooltip>
        </q-btn>
        <q-btn flat size="xs" icon="colorize" class="bg-secondary">
            <q-popup-proxy
              cover
              transition-show="scale"
              transition-hide="scale"
            >
              <q-color no-header no-footer v-model="color" />
            </q-popup-proxy>
            <q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Background Color
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          size="xs"
          class="bg-secondary"
          icon="fas fa-expand-arrows-alt"
        >
        </q-btn>
        <q-btn
          flat
          size="xs"
          class="bg-secondary"
          icon="settings"
          @click="groupSettings"
        ><q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Settings
          </q-tooltip>
        </q-btn>
        <q-btn flat size="xs" :icon="icon" class="bg-secondary" @click="click">
        <q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Collapse/Expand
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          size="xs"
          icon="fas fa-close"
          class="bg-secondary"
          @click="deleteGroup = true"
        ><q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Delete Group
          </q-tooltip>
        </q-btn>
      </q-toolbar>
    </h4>
    <jtk-source filter=".group-connect, .group-connect *" />
    <jtk-target />
    <div
      jtk-group-content="true"
      class="aGroupInner"
      :style="
        'background-color:' +
        color +
        ';width:' +
        obj.w +
        'px;height:' +
        obj.h +
        'px;'
      "
    ></div>
    <q-inner-loading :showing="showing" style="z-index: 999999;">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>

    <q-dialog v-model="savePatternDialog" persistent >
      <q-card style="width:400px; height:200px padding: 10px; padding-left:30px;padding-top: 30px;">
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
              <q-item-label>Save Pattern</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-save" />
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
            
            <q-input dense v-model="patternName" autofocus @keyup.enter="savePatternDialog = false"/>
          </span>
        </q-card-section>

        <q-card-actions align="left">
          <q-btn
            style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
            flat
            label="Cancel"
            class="bg-accent text-dark"
            color="primary"
            v-close-popup
          />
          </q-card-actions>
          <q-card-actions align="right"><q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Save"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="savePattern"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="deleteGroup" persistent>
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
              <q-item-label>Delete Group</q-item-label>
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
            Are you sure you want to delete this group?
          </span>
        </q-card-section>

        <q-card-actions align="left">
          <q-btn
            style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
            flat
            label="Cancel"
            class="bg-accent text-dark"
            color="primary"
            v-close-popup
          />
          </q-card-actions>
          <q-card-actions align="right">
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
            label="Delete"
            class="bg-primary text-white"
            color="primary"
            v-close-popup
            @click="deleteAGroup(false)"
          /><q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Delete All"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="deleteAGroup(true)"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>
<style scoped>
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
<script>
import { BaseNodeComponent } from 'jsplumbtoolkit-vue2';

export default {
  name: 'GroupTemplate',
  mixins: [BaseNodeComponent],
  components: {},
  mounted() {
    var me = this;
    this.toolkit = window.toolkit;
  },
  created() {},
  data() {
    return {
      showing: false,
      title: 'Chapter 1',
      savePatternDialog: false,
      patternName: '',
      color: '',
      dimension: 500,
      deleteGroup: false,
      icon: 'fas fa-minus',
    };
  },
  methods: {
    savePattern() {

    },
    deleteAGroup(all) {
      console.log("Removing group",this.obj);
      window.toolkit.removeGroup(this.obj,all);
    },
    resize: function () {},
    saveTrope() {},
    groupSettings: function () {
      var me = this;
      console.log('new.group.dialog', this.obj);
      this.$root.$emit('new.group.dialog', {
        obj: this.obj,
        callback: (object) => {
          console.log(object);
          me.obj = object;
        },
      });
    },
    remove: function () {
      console.log(this.obj);
      var group = this.toolkit.getObjectInfo(this.obj);

      this.toolkit.removeGroup(group.obj, true);
    },
    click: function () {
      this.toolkit.renderer.toggleGroup(this.obj);
      if (this.icon === 'fas fa-minus') {
        this.icon = 'fas fa-plus';
      } else {
        this.icon = 'fas fa-minus';
      }
    },
  },
};
</script>
saveTrope