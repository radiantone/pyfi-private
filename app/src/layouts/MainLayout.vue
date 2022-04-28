<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <ToolPalette
        v-bind:data-generator="dataGenerator"
        surfaceId="flow1"
        selector="[data-node-type]"
      />
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
      <q-tab-panels v-model="tab" keep-alive v-for="flow in flows" :key="flow.id">
        <q-tab-panel
          :name="'flow'+flow.id"
          style="height: calc(100vh - 165px); padding: 0px;"
          :ref="'flow'+flow.id"
        >
          <Designer :ref="'flow'+flow.id+'designer'" :flowcode="flow.code" :flowname="flow.filename" @update-name="updateFlow" :flowuuid="flow._id" :flowid="flow.id" :surfaceId="'flow'+flow.id"/>
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
        <q-tab v-for="flow in flows" :key="flow.id" :name="'flow'+flow.id" class="text-dark" :label="flow.filename">
        <!--<q-btn
            flat
            dense
            size="xs"
            icon="close"
            style="position: absolute; right:-15px;top:5px"
          />-->
        </q-tab>
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
    <q-btn flat dense color="primary">
    <q-item-label class="text-dark" style="">{{ status }}</q-item-label>
      </q-btn>
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
import ToolPalette from "src/components/ToolPalette.vue";
import { mappedGetters, mappedActions, Actions, Getters, State, mappedState } from 'src/store/Store';

import "assets/css/font-awesome.min.css";
import "assets/css/flowfont.css";
import "assets/fonts/fontawesome-webfont.eot";
import "assets/fonts/fontawesome-webfont.svg";
import "assets/fonts/fontawesome-webfont.woff2";
import "assets/fonts/fontawesome-webfont.woff";
import "assets/fonts/flowfont2.woff2";

export default defineComponent({
  name: "MainLayout",
  components: { Designer, ToolPalette },
  setup() {
    return {};
  },
  created() {
    this.tab = 'flow'+this.flows[0].id;
  },
  computed: {
    status() {
      return this.$store.state.designer.message;
    },
    getSurfaceId() {
      return window.toolkit.surfaceId;
    },
  },
  methods: {
    updateFlow(name){
        this.flow.filename=name;
    },
    dataGenerator: function (el) {
      // This probably needs to be automated
      return {
        type: el.getAttribute("data-node-type"),
        w: 120,
        h: 80,
        properties: [],
        rules: [],
        events: [],
        callbacks: [],
        facts: [],
        behaviors: [],
        notes: [],
        package: el.getAttribute("data-node-package"),
        description: el.getAttribute("data-node-desc"),
        icon: el.getAttribute("data-node-icon"),
        name: el.getAttribute("data-node-name"),
        id: jsPlumbUtil.uuid(),
      };
    },
    tabChanged(tab) {
      console.log("REFS:", this.$refs);
      console.log("TAB:", tab, this.$refs[tab]);
      for(var i=0;i<this.flows.length;i++) {
        var flow = this.flows[i];
        if(tab == 'flow'+flow.id) {
          this.flow = flow;
        }
      }
      if(this.$refs[tab + "designer"]) {
        window.toolkit = this.$refs[tab + "designer"][0].toolkit;
        window.toolkit.$q = this.$q;
        window.renderer = window.toolkit.renderer;
        console.log("Refreshing designer");
        this.$refs[tab + "designer"][0].refresh();
      }
    },
  },
  mounted() {
    var me = this;
    console.log("MAINLAYOUT MESSAGE",this.$store.state.designer.message)
    console.log("MAINLAYOUT STORE",this.$store);
    this.$root.$on("flow.uuid", (flowid, flowuuid) => {
      for(var i=0;i<me.flows.length;i++) {
        var flow = me.flows[i];
        if(flow.id == flowid) {
          flow._id = flowuuid;
          console.log("Updated flow",flow," with uuid",flowuuid);
        }
      }
    });

    this.$root.$on("close.flow",(flowid) => {
      console.log("DELETING FLOWID",flowid)
      console.log("BEFORE DELETE",me.flows)
      var index = -1;
      for(var i=0;i<me.flows.length;i++) {
        var flow = me.flows[i];
        if(flow.id == flowid) {
          index = i;
          break;
        }
      }
      me.flows = me.flows.filter(function(value, index, arr){ 
        console.log(value.id,flowid)
        return value.id != flowid;
      });
      this.tab = 'flow'+me.flows[index-1].id;
      this.$refs[this.tab+'designer'][0].refresh();
      console.log("AFTER DELETE",me.flows)
    });
    this.$root.$on("new.flow",() => {
      var id = me.flows.length+1;
      me.flows.push({
        'filename':'New Flow',
        'id': id,
        'code': null
      })
      for(var i=0;i<me.flows.length;i++) {
        var flow = me.flows[i];
        if(flow.id == id) {
          me.flow = flow;
        }
      }
      me.tab='flow'+id
    });
    this.$root.$on("load.flow",(flow) => {
      console.log("load.flow",flow);
      var id = me.flows.length+1;
      flow._id = flow._id;
      flow.id = id;
      me.flows.push(flow)
      me.tab='flow'+id
    });
    this.$q.loading.show({
      delay: 40,
      spinnerColor: "dark",
      spinnerSize: 154,
      spinnerThickness: 1,
    });
    console.log("Mounting....");
    console.log("REFS",this.$refs);
    window.toolkit = this.$refs["flow1designer"][0].toolkit;
    window.toolkit.$q = this.$q;
    window.renderer = window.toolkit.renderer;
    setTimeout(() => {
      var processor = document.querySelector("#processor");

      processor.data = {
        node: {
          icon: "fab fa-python",
          style: "",
          type: "processor",
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
          package: "queue name",
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
          package: "queue name",
          disabled: false,
          columns: [],
          properties: [],
        },
      };

      var group = document.querySelector("#processorgroup");
      group.data = {
        node: {
          icon: "far fa-object-group",
          style: "size:50px",
          type: "group",
          name: "Group",
          label: "Group",
          description: "A processor group description",
          package: "my.python.package",
          disabled: false,
          group: true,
          columns: [],
          properties: [],
        },
      };

      var parallel = document.querySelector("#parallel");
      parallel.data = {
        node: {
          icon: "fas fa-list",
          style: "size:50px",
          type: "parallel",
          name: "Parallel",
          label: "Parallel",
          description: "A parallel tool description",
          package: "my.python.package",
          disabled: false,
          columns: [],
          properties: [],
        },
      };

      var pipeline = document.querySelector("#pipeline");
      pipeline.data = {
        node: {
          icon: "fas fa-long-arrow-alt-right",
          style: "size:50px",
          type: "pipeline",
          name: "Pipeline",
          label: "Pipeline",
          description: "A pipeline tool description",
          package: "my.python.package",
          disabled: false,
          columns: [],
          properties: [],
        },
      };

      //, chord, segment, map, reduce
      var els = [processor, portin, portout, group, parallel, pipeline];

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
      flows: [
        {
          filename:'Scratch Flow',
          id: 1
        }
      ],
      tab: null,
      text: "",
    };
  },
});
</script>
