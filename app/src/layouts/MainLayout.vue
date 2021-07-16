<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <img
          src="~assets/images/pyfi.svg"
          style="padding-left: 15px; height: 45px; padding-right: 10px;"
        />
        <q-btn
          flat
          align="left"
          icon="icon-processor"
          aria-label="Processor"
          size="large"
          id="processor"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Processor
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          align="left"
          icon="icon-port-in"
          aria-label="Port In"
          size="large"
          id="portin"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Port In
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          align="left"
          icon="icon-port-out"
          aria-label="Port Out"
          id="portout"
          size="large"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Port Out
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          align="left"
          icon="icon-group"
          aria-label="Group"
          size="large"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Process Group
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          align="left"
          icon="icon-group-remote"
          aria-label="Remote Group"
          size="large"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Remote Process Group
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          align="left"
          icon="icon-funnel"
          aria-label="Funnel"
          size="large"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Funnel
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          align="left"
          icon="icon-template"
          aria-label="Template"
          size="large"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Template
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          align="left"
          icon="icon-label"
          aria-label="Label"
          size="large"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Label
          </q-tooltip>
        </q-btn>
        <q-space />

        <q-btn
          flat
          aria-label="Menu"
          icon="menu"
          size="large"
          style="min-height: 56px; cursor: grabbing;"
          class="text-dark text-bold"
        >
          <q-menu>
            <q-list dense>
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fas fa-table"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Summary
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fas fa-calculator"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Counters
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="far fa-sticky-note"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Bulletin Board
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fas fa-database"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Data Provenance
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fas fa-wrench"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Controller Settings
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fas fa-list-alt"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Parameter Contexts
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fa fa-history"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Flow Configuration History
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fa fa-area-chart"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Node Status History
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fas fa-project-diagram"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Templates
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fas fa-question-circle"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  Help
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup>
                <q-item-section side>
                  <q-icon name="fas fa-info-circle"></q-icon>
                </q-item-section>
                <q-item-section side class="text-blue-grey-8">
                  About
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
      <q-toolbar class="bg-accent" style="min-height: 40px; padding: 0px;">
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-list"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-bullseye"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fas fa-satellite-dish"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-play"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-stop"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-warning invalid"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fas fa-bolt"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-check"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-asterisk"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-arrow-circle-up"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-exclamation-circle"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-question"
          label="0"
        />
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-refresh"
          label="12:36:17 EDT"
        />
        <q-space />
        <q-input
          dark
          dense
          standout
          v-model="text"
          placeholder="Search..."
          style="width: 20%; border-left: 1px solid lightgrey;"
          input-class="text-left text-dark"
          class="q-ml-md text-dark bg-white"
        >
          <template v-slot:append>
            <q-icon color="dark" size="sm" v-if="text === ''" name="search" />
            <q-icon
              v-else
              name="clear"
              color="dark"
              size="sm"
              class="cursor-pointer text-dark"
              @click="text = ''"
            />
          </template>
        </q-input>
      </q-toolbar>
    </q-header>

    <div style="height: 100vh; width: 100%; position: relative; top: 95px;">
      <q-tab-panels v-model="tab" keep-alive>
        <q-tab-panel
          name="flow1"
          style="height: calc(100vh - 165px); padding: 0px;"
          ref="flow1"
        >
          <Designer ref="flow1designer" />
        </q-tab-panel>
        <q-tab-panel
          name="flow2"
          style="height: calc(100vh - 165px); padding: 0px;"
          ref="flow2"
        >
          <Designer ref="flow2designer" />
        </q-tab-panel>
        <q-tab-panel
          name="flow3"
          style="height: calc(100vh - 165px); padding: 0px;"
          ref="flow3"
        >
          <Designer ref="flow3designer" />
        </q-tab-panel>
      </q-tab-panels>
      <q-tabs
        v-model="tab"
        dense
        class="bg-primary"
        align="left"
        @input="tabChanged"
        narrow-indicator
        active-color="dark"
        indicator-color="accent"
        active-bg-color="accent"
      >
        <q-tab name="flow1" class="text-dark" label="Flow #1" />
        <q-tab name="flow2" class="text-dark" label="Flow #2" />
        <q-tab name="flow3" class="text-dark" label="Flow #3" />
      </q-tabs>
    </div>
    <q-footer
      elevated
      style="
        background-color: rgba(249, 250, 251, 0.9);
        height: 32px;
        font-size: 16px;
        padding: 5px;
        font-weight: bold;
      "
    >
      <q-item-label class="text-dark" style="">Ready</q-item-label>
    </q-footer>
  </q-layout>
</template>
<style>
.q-toolbar {
  position: relative;
  padding: 0px;
  min-height: 50px;
  width: 100%;
}
icon-processor:before {
  content: "\e807";
}
[class^="icon-"]:before,
[class*=" icon-"]:before {
  font-family: "flowfont";
  font-style: normal;
  font-weight: normal;
  speak: none;
  display: inline-block;
  text-decoration: inherit;
  width: 1em;
  margin-right: 0.2em;
  text-align: center;
  font-variant: normal;
  text-transform: none;
  line-height: 1em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
<script>

const { v4: uuidv4 } = require("uuid");
var dd = require("drip-drop");

import { QSpinnerOval } from "quasar";
import { defineComponent, ref } from "@vue/composition-api";
import Designer from "src/pages/Designer.vue";

import "assets/css/font-awesome.min.css";
import "assets/css/flowfont.css";
import "assets/fonts/fontawesome-webfont.eot";
import "assets/fonts/fontawesome-webfont.svg";
import "assets/fonts/fontawesome-webfont.woff2";
import "assets/fonts/fontawesome-webfont.woff";
import "assets/fonts/flowfont.woff2";

export default defineComponent({
  name: "MainLayout",
  components: { Designer },
  setup() {
    return {};
  },
  created() {},
  methods: {
    tabChanged(tab) {
      console.log("TAB:", tab, this.$refs[tab]);
      window.toolkit = this.$refs[tab + "designer"].toolkit;
      window.toolkit.$q = this.$q;
      window.renderer = window.toolkit.renderer;
    },
  },
  mounted() {
    this.$q.loading.show({
      delay: 40,
      spinnerColor: "dark",
      spinnerSize: 154,
      spinnerThickness: 1,
    });
    window.toolkit = this.$refs["flow1designer"].toolkit;
    window.toolkit.$q = this.$q;
    window.renderer = window.toolkit.renderer;
    setTimeout(() => {
      var processor = document.querySelector("#processor");

      processor.data = {
        node: {
          icon: "fab fa-python",
          style: "",
          type: "script",
          name: "Script Processor",
          label: "Script",
          description: "A script processor description",
          package: "my.python.package",
          disabled: false,
          columns: [],
          properties: [],
        },
      };

      var portin = document.querySelector("#portin");
      portin.data = {
        node: {
          icon: "outlet-icon2",
          style: "size:50px",
          type: "portin",
          name: "Port In",
          label: "Port In",
          description: "A port in description",
          package: "my.python.package",
          disabled: false,
          columns: [],
          properties: [],
        },
      };
      var portout = document.querySelector("#portout");
      portout.data = {
        node: {
          icon: "fas fa-plug",
          style: "size:50px",
          type: "portout",
          name: "Port Out",
          label: "Port Out",
          description: "A port out description",
          package: "my.python.package",
          disabled: false,
          columns: [],
          properties: [],
        },
      };
      var els = [processor, portin, portout];

      els.forEach((el) => {
        var data = el.data;
        data.id = uuidv4();
        var draghandle = dd.drag(el, {
          image: true, // default drag image
        });
        draghandle.on("start", function (setData, e) {
          console.log("drag:start:", el, e);
          setData("object", JSON.stringify(data));
        });
      });
    });
    var me = this;
    setTimeout(function () {
      me.$q.loading.hide();
    }, 500);
  },
  data() {
    return {
      tab: "flow1",
      text: "",
    };
  },
});
</script>
