<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <ToolPalette
        v-if="tools == 'code'"
        v-bind:data-generator="dataGenerator"
        surfaceId="flow1"
        selector="[data-node-type]"
      />
      <ModelToolPalette
        v-if="tools == 'model'"
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

        <q-btn-toggle
          v-model="tools"
          class="my-custom-toggle"
          no-caps
          flat
          dense
          size="sm"
          padding="1em"
          unelevated
          :ripple="false"
          toggle-color="dark"
          color="white"
          text-color="secondary"
          :options="[
            { icon: 'fa fa-database', value: 'model' },
            { icon: 'fab fa-python', value: 'code' },
          ]"
        >
          <template v-slot:one>
            <div style="font-size: 0.5em; margin-left: 20px;">
              <q-tooltip
                content-style="font-size: 16px"
                content-class="bg-black text-white"
              >
                Database Tools
              </q-tooltip>
            </div>
          </template>
          <template v-slot:two>
            <div style="font-size: 0.5em; margin-left: 20px;"></div>

            <q-tooltip
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Python Tools
            </q-tooltip>
          </template>
        </q-btn-toggle>
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

    <q-splitter
      v-model="splitterModel"
      vertical
      :limits="[60, 100]"
      unit="%"
      style="overflow: hidden;"
    >
      <template v-slot:before>
        <div
          style="
            height: 100vh;
            width: 100%;
            position: relative;
            top: 95px;
            overflow: hidden;
          "
        >
          <q-tab-panels
            v-model="tab"
            keep-alive
            v-for="flow in flows"
            :key="flow.id"
          >
            <q-tab-panel
              :name="'flow' + flow.id"
              style="
                height: calc(100vh - 165px);
                padding: 0px;
                overflow: hidden;
              "
              :ref="'flow' + flow.id"
            >
              <Designer
                :ref="'flow' + flow.id + 'designer'"
                :flowcode="flow.code"
                :flowname="flow.filename"
                @update-name="updateFlow"
                :flowuuid="flow._id"
                :flowid="flow.id"
                :surfaceId="'flow' + flow.id"
              />
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
            <q-tab
              v-for="flow in flows"
              :key="flow.id"
              :name="'flow' + flow.id"
              class="text-dark"
              :label="flow.filename"
            >
              <!--<q-btn
            flat
            dense
            size="xs"
            icon="close"
            style="position: absolute; right:-15px;top:5px"
          />-->
            </q-tab>
          </q-tabs>
          <q-btn
            flat
            dense
            size="md"
            color="primary"
            icon="menu"
            aria-label="Menu"
            style="z-index: 9999; position: absolute; right: 0px;"
            @click="drawer = !drawer"
          />
        </div>
      </template>
      <template v-slot:after>
        <div
          style="
            height: 100vh;
            width: 100%;
            padding-top: 5px;
            position: relative;
            top: 95px;
            overflow: hidden;
          "
        >
          <q-tabs
            v-model="drawertab"
            dense
            class="bg-primary"
            align="left"
            narrow-indicator
            active-color="dark"
            indicator-color="primary"
            active-bg-color="accent"
          >
            <q-tab name="messages" class="text-dark" label="Messages" />
            <q-tab name="queues" class="text-dark" label="Queues" />
            <q-tab name="monitor" class="text-dark" label="Monitor" />
            <q-tab name="error" class="text-dark" label="Errors" />
          </q-tabs>
          <q-tab-panels v-model="drawertab" keep-alive>
            <q-tab-panel
              name="messages"
              ref="messages"
              style="padding: 0px; width: 100%; padding-top: 0px;"
            >
              <q-card-section
                style="
                  padding: 5px;
                  z-index: 999999;
                  padding-bottom: 10px;
                  height: calc(100vh - 200px);
                "
              >
            <q-table
              dense
              :columns="messageColumns"
              :data="msglogs"
              row-key="name"
              flat
              virtual-scroll
              :pagination="initialPagination"
              style="
              height:100%;
                width: 100%;
                border-top-radius: 0px;
                border-bottom-radius: 0px;
              "
            >
            </q-table>
              <!--
                <q-scroll-area style="height:calc(100vh - 200px);width::auto">
                  <div v-for="log in msglogs">
                    {{ log['date'] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{
                      log['state']
                    }}&nbsp;&nbsp; --&nbsp;&nbsp;{{ log['module'] }}&nbsp;&nbsp;
                    --&nbsp;&nbsp;{{ log['task'] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{
                      log['duration']
                    }}
                  </div>
                </q-scroll-area>-->

              </q-card-section>
            </q-tab-panel>
            <q-tab-panel
              name="queues"
              ref="queues"
              style="
                padding: 0px;
                width: 100%;
                padding-top: 0px;
                height: calc(100vh - 170px);
              "
            >
              <q-table
                dense
                :data="queues"
                :columns="columns"
                row-key="name"
                :rows-per-page-options="[50]"
                virtual-scroll
                style="height: calc(100vh - 170px);"
              >
                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td key="name" :props="props" :width="150">
                    <a
              class="text-secondary"
              style="
                z-index: 99999;
                cursor: pointer;
                width: 100%;
                min-width: 250px;
                font-size: 1.3em;
              "
              @click="queuename = props.row.name; viewQueueDialog=true"
              >{{ props.row.name }}</a>
                      
                    </q-td>
                    <q-td key="messages" :props="props">
                      {{ props.row.messages }}
                    </q-td>
                    <q-td key="bytes" :width="200" :props="props">
                      {{ props.row.bytes }}
                    </q-td>
                    <q-td key="actions" :props="props" style="width: 25px;">
                    <q-btn
                        flat
                        round
                        dense
                        size="sm"
                        class="bg-white text-primary"
                        :id="props.row.name"
                        width="100"
                        icon="remove_circle"
                      />
                    <q-btn
                        flat
                        round
                        dense
                        size="sm"
                        class="bg-white text-primary"
                        :id="props.row.name"
                        width="100"
                        icon="fas fa-cog"
                      />
                      <q-btn
                        flat
                        round
                        dense
                        size="sm"
                        class="bg-white text-primary"
                        :id="props.row.name"
                        width="100"
                        icon="delete"
                      />
                    </q-td>
                  </q-tr>
                </template>
              </q-table>
            </q-tab-panel>
            <q-tab-panel
              name="monitor"
              ref="monitor"
              style="padding: 0px; width: 100%; padding-top: 0px;"
            ></q-tab-panel>
            <q-tab-panel
              name="error"
              ref="error"
              style="padding: 0px; width: 100%; padding-top: 0px;"
            ></q-tab-panel>
          </q-tab-panels>
        </div>
      </template>
    </q-splitter>
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
      <q-toolbar style="padding: 0px; margin-top: -12px;">
        <q-btn flat dense color="primary">
          <q-item-label class="text-dark" style="">{{ status }}</q-item-label>
        </q-btn>
        <q-space />
        <q-btn
          flat
          dense
          color="primary"
          icon="menu"
          @click="toggleSplitter"
        ></q-btn>
      </q-toolbar>
    </q-footer>
    <q-drawer
      v-model="searchdrawer"
      side="right"
      bordered
      :width="512"
      style="overflow: hidden;"
    >
      <q-inner-loading :showing="true" style="z-index: 9999999;">
        <q-spinner-gears size="50px" color="primary" />
      </q-inner-loading>
    </q-drawer>
        <q-dialog v-model="viewQueueDialog" transition-show="none" persistent>
      <q-card
        style="width:70vw; max-width: 70vw; height:80vh; padding: 10px; padding-left:30px;padding-top: 30px;"
      >
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
              <q-item-label>Queue {{queuename}}</q-item-label>
              <q-space />
              <q-btn class="text-primary" flat dense round size="sm" icon="fas fa-close" @click="viewQueueDialog=false"/>
            </q-toolbar>
          </div>
        </q-card-section>

        <q-card-actions align="left">
          <q-btn
            style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
            flat
            label="Close"
            class="bg-accent text-dark"
            color="primary"
            v-close-popup
          />
        </q-card-actions>
        <q-card-actions align="right"
          ><q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Save"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>
<style>
a.text-secondary:hover {
  cursor: pointer;
  text-decoration: underline;
}
.q-splitter__before {
  overflow: hidden;
}
.q-splitter__panel {
  overflow: hidden;
}
.q-toolbar {
  position: relative;
  padding: 0px;
  min-height: 50px;
  width: 100%;
}
icon-processor:before {
  content: '\e807';
}
[class^='icon-']:before,
[class*=' icon-']:before {
  font-family: 'flowfont';
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
const { v4: uuidv4 } = require('uuid');
var dd = require('drip-drop');

import { QSpinnerOval } from 'quasar';
import { defineComponent, ref } from '@vue/composition-api';
import Designer from 'src/pages/Designer.vue';
import ToolPalette from 'src/components/ToolPalette.vue';
import ModelToolPalette from 'src/components/ModelToolPalette.vue';
import {
  mappedGetters,
  mappedActions,
  Actions,
  Getters,
  State,
  mappedState,
} from 'src/store/Store';

import 'assets/css/font-awesome.min.css';
import 'assets/css/flowfont.css';
import 'assets/fonts/fontawesome-webfont.eot';
import 'assets/fonts/fontawesome-webfont.svg';
import 'assets/fonts/fontawesome-webfont.woff2';
import 'assets/fonts/fontawesome-webfont.woff';
import 'assets/fonts/flowfont2.woff2';

import { io, Socket } from 'socket.io-client';
const socket = io('http://localhost');

export default defineComponent({
  name: 'MainLayout',
  components: { Designer, ToolPalette, ModelToolPalette },
  setup() {
    return {};
  },
  created() {
    var me = this;
    this.tab = 'flow' + this.flows[0].id;
    window.layout = this;
    socket.on('global', (msg) => {
      //console.log('MAINLAYOUT', msg);
      if (msg['channel'] == 'task') {
        me.msglogs.unshift(msg);
        me.msglogs = me.msglogs.slice(0, 200);
      } else {
        var qs = [];
        if (msg['type'] && msg['type'] == 'queues') {
          msg['queues'].forEach((queue) => {
            if(queue['name'].indexOf('celery') == -1) {
              qs.push({
                name: queue['name'],
                messages: queue['messages'],
                bytes: queue['message_bytes'],
                action: ''
            });
            }
          });
          me.queues = qs;
        }
      }
    });
  },
  watch: {
    text: function (val) {
      if (this.text.length > 0) {
        this.searchdrawer = true;
      } else {
        this.searchdrawer = false;
      }
    },
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
    toggleSplitter() {
      if (this.splitterModel < 100) {
        this.splitterSave = this.splitterModel;
        this.splitterModel = 100;
      } else {
        this.splitterModel = this.splitterSave;
      }
    },
    updateFlow(name) {
      this.flow.filename = name;
    },
    dataGenerator: function (el) {
      // This probably needs to be automated
      return {
        type: el.getAttribute('data-node-type'),
        w: 120,
        h: 80,
        properties: [],
        rules: [],
        events: [],
        callbacks: [],
        facts: [],
        behaviors: [],
        notes: [],
        package: el.getAttribute('data-node-package'),
        description: el.getAttribute('data-node-desc'),
        icon: el.getAttribute('data-node-icon'),
        name: el.getAttribute('data-node-name'),
        id: jsPlumbUtil.uuid(),
      };
    },
    tabChanged(tab) {
      console.log('REFS:', this.$refs);
      console.log('TAB:', tab, this.$refs[tab]);
      for (var i = 0; i < this.flows.length; i++) {
        var flow = this.flows[i];
        if (tab == 'flow' + flow.id) {
          this.flow = flow;
        }
      }
      if (this.$refs[tab + 'designer']) {
        window.toolkit = this.$refs[tab + 'designer'][0].toolkit;
        window.toolkit.$q = this.$q;
        window.renderer = window.toolkit.renderer;
        console.log('Refreshing designer');
        this.$refs[tab + 'designer'][0].refresh();
      }
    },
  },
  mounted() {
    var me = this;
    //console.log('MAINLAYOUT MESSAGE', this.$store.state.designer.message);
    //console.log('MAINLAYOUT STORE', this.$store);
    this.$root.$on('flow.uuid', (flowid, flowuuid) => {
      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i];
        if (flow.id == flowid) {
          flow._id = flowuuid;
          console.log('Updated flow', flow, ' with uuid', flowuuid);
        }
      }
    });

    this.$root.$on('close.flow', (flowid) => {
      console.log('DELETING FLOWID', flowid);
      console.log('BEFORE DELETE', me.flows);
      var index = -1;
      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i];
        if (flow.id == flowid) {
          index = i;
          break;
        }
      }
      me.flows = me.flows.filter(function (value, index, arr) {
        console.log(value.id, flowid);
        return value.id != flowid;
      });
      this.tab = 'flow' + me.flows[index - 1].id;
      this.$refs[this.tab + 'designer'][0].refresh();
      console.log('AFTER DELETE', me.flows);
    });
    this.$root.$on('new.flow', () => {
      var id = me.flows.length + 1;
      me.flows.push({
        filename: 'New Flow',
        id: id,
        code: null,
      });
      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i];
        if (flow.id == id) {
          me.flow = flow;
        }
      }
      me.tab = 'flow' + id;
    });
    this.$root.$on('load.flow', (flow) => {
      console.log('load.flow', flow);
      var id = me.flows.length + 1;
      flow._id = flow._id;
      flow.id = id;
      me.flows.push(flow);
      me.tab = 'flow' + id;
    });
    this.$q.loading.show({
      delay: 40,
      spinnerColor: 'dark',
      spinnerSize: 154,
      spinnerThickness: 1,
    });
    console.log('Mounting....');
    console.log('REFS', this.$refs);
    window.toolkit = this.$refs['flow1designer'][0].toolkit;
    window.toolkit.$q = this.$q;
    window.renderer = window.toolkit.renderer;
    setTimeout(() => {
      var processor = document.querySelector('#processor');

      processor.data = {
        node: {
          icon: 'fab fa-python',
          style: '',
          type: 'processor',
          name: 'Script Processor',
          label: 'Script',
          description: 'A script processor description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: [],
        },
      };

      var portin = document.querySelector('#portin');
      portin.data = {
        node: {
          icon: 'outlet-icon2',
          style: 'size:50px',
          type: 'portin',
          name: 'Port In',
          label: 'Port In',
          description: 'A port in description',
          package: 'queue name',
          disabled: false,
          columns: [],
          properties: [],
        },
      };

      var portout = document.querySelector('#portout');
      portout.data = {
        node: {
          icon: 'fas fa-plug',
          style: 'size:50px',
          type: 'portout',
          name: 'Port Out',
          label: 'Port Out',
          description: 'A port out description',
          package: 'queue name',
          disabled: false,
          columns: [],
          properties: [],
        },
      };

      var group = document.querySelector('#processorgroup');
      group.data = {
        node: {
          icon: 'far fa-object-group',
          style: 'size:50px',
          type: 'group',
          name: 'Group',
          label: 'Group',
          description: 'A processor group description',
          package: 'my.python.package',
          disabled: false,
          group: true,
          columns: [],
          properties: [],
        },
      };

      var parallel = document.querySelector('#parallel');
      parallel.data = {
        node: {
          icon: 'fas fa-list',
          style: 'size:50px',
          type: 'parallel',
          name: 'Parallel',
          label: 'Parallel',
          description: 'A parallel tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: [],
        },
      };

      var pipeline = document.querySelector('#pipeline');
      pipeline.data = {
        node: {
          icon: 'fas fa-long-arrow-alt-right',
          style: 'size:50px',
          type: 'pipeline',
          name: 'Pipeline',
          label: 'Pipeline',
          description: 'A pipeline tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: [],
        },
      };
      var label = document.querySelector('#label');
      label.data = {
        node: {
          icon: 'icon-label',
          style: 'size:50px',
          type: 'note',
          name: 'Label',
          label: 'Label',
          disabled: false,
          columns: [],
          properties: [],
        },
      };
      //, chord, segment, map, reduce
      var els = [processor, portin, portout, group, parallel, pipeline, label];

      els.forEach((el) => {
        var data = el.data;
        data.id = uuidv4();
        var draghandle = dd.drag(el, {
          image: true, // default drag image
        });
        draghandle.on('start', function (setData, e) {
          console.log('drag:start:', el, e);
          setData('object', JSON.stringify(data));
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
      initialPagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 50
        // rowsNumber: xx if getting data from a server
      },
      viewQueueDialog: false,
      splitterModel: 100,
      splitterSave: 70,
      messageColumns: [
        {
          name: 'date',
          label: 'Date',
          field: 'date',
          align: 'left',
        },{
          name: 'channel',
          label: 'Channel',
          field: 'channel',
          align: 'left',
        },{
          name: 'module',
          label: 'Module',
          field: 'module',
          align: 'left',
        },{
          name: 'task',
          label: 'Task',
          field: 'task',
          align: 'left',
        },{
          name: 'room',
          label: 'Room',
          field: 'room',
          align: 'left',
        },{
          name: 'state',
          label: 'State',
          field: 'state',
          align: 'left',
        },{
          name: 'duration',
          label: 'Duration',
          field: 'duration',
          align: 'left',
        }
      ],
      columns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left',
        },
        {
          name: 'messages',
          align: 'center',
          label: 'Messages',
          field: 'messages',
        },
        {
          name: 'bytes',
          align: 'right',
          classes: 'text-secondary',
          label: 'Bytes',
          field: 'bytes',
        },
        {
          name: 'actions',
          align: 'center',
          style: 'min-width:150px',
          classes: 'text-secondary',
          label: 'Actions'
        }
      ],
      queues: [],
      jsondata: {},
      msglogs: [],
      searchdrawer: false,
      flows: [
        {
          filename: 'Scratch Flow',
          id: 1,
        },
      ],
      drawertab: 'messages',
      drawer: true,
      tab: null,
      tools: 'code',
      text: '',
    };
  },
});
</script>
