<template>
  <div
    style="
      box-shadow: 0 0 5px grey;
      background-color: rgb(244, 246, 247);
      z-index: 999999;
      width: 300px;
      height: 40px;
      padding: 3px;
      font-size: 12px;
    "
  >
    <q-toolbar style="position: absolute; left: 0px; top: -13px;">
      <q-item-label
        style="margin-left: 5px; font-weight: bold; color: #775351;"
        :data-source="node" class="fas fa-email"
        >
        <q-select style="width:275px" v-model="model" :options="options" :dense="true" :options-dense="true">
<template v-slot:prepend>
          <q-icon name="far fa-envelope" />
        </template>
        </q-select>
        <!--{{ name }}
        <q-popup-edit v-model="name" title="Queue Name" buttons>
          <q-input type="string" v-model="name" dense autofocus />
        </q-popup-edit>-->
      </q-item-label>
      <q-space />
      <q-btn flat dense size="xs" icon="close" color="primary" style="cursor:pointer;font-size:.7em;position:absolute;right:5px"></q-btn>

      <!--
      <q-btn-dropdown
        flat
        content-class="text-dark bg-white"
        dense
        color="secondary"
        dropdown-icon="menu"
        style="margin-right: 5px;"
        padding="0px"
        size=".6em"
        no-icon-animation
      >
        <q-list dense>
          <q-item clickable v-close-popup>
            <q-item-section side>
              <q-icon name="fas fa-minus-circle"></q-icon>
            </q-item-section>
            <q-item-section side class="text-blue-grey-8">
              Clear
            </q-item-section>
          </q-item>
          <q-item clickable v-close-popup @click="queueconfig = !queueconfig">
            <q-item-section side>
              <q-icon name="fas fa-cog"></q-icon>
            </q-item-section>
            <q-item-section side class="text-blue-grey-8">
              Configure
            </q-item-section>
          </q-item>
          <q-separator/>
          <q-item clickable v-close-popup>
            <q-item-section side>
              <q-icon name="delete"></q-icon>
            </q-item-section>
            <q-item-section side class="text-blue-grey-8">
              Delete
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>-->
    </q-toolbar>

    <div
      style="
        color: black;
        font-weight: normal;
        font-family: 'Roboto', '-apple-system', 'Helvetica Neue', Helvetica,
          Arial, sans-serif;
        background-color: white;
        border-top: 1px solid #abbcc3;
        width: 100%;
        height: 20px;
        position: absolute;
        top: 20px;
        left: 0px;
        padding: 1px;
        padding-left: 3px;
        font-size: 12px;
        padding-top: 3px;
      "
    >
      Queued
      <span style="font-weight: bold; color: #775351;">{{messages}} ({{bytes}} bytes)</span>
      <q-btn flat dense icon="menu" size="xs" @click="showQueue" color="primary" style="cursor:pointer;font-size:.7em;position:absolute;right:5px"/>
      
    </div>
    <q-card
      style="
        width: 350px;
        height: 400px
        z-index: 999;
        display: block;
        position: absolute;
        left: 0px;
        top: 45px;
      "
      v-if="queueconfig"
    >
      <q-card-actions align="left">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; left: 0px;"
          label="Close"
          class="bg-primary text-white"
          color="primary"
          dense
          size="sm"
          @click="queueconfig = false"
        />
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          dense
          size="sm"
          @click="queueconfig = false"
        />
      </q-card-actions>
    </q-card>

  </div>
</template>
<script>
import { io, Socket } from 'socket.io-client';

let socket = io('http://localhost');

export default {
  name: 'Button',
  props: ['node', 'name'],
  created() {
    var me = this;
    socket.on('global', (data) => {
      //console.log('QUEUE SERVER GLOBAL MESSAGE', data);
      if(data['type'] && data['type'] == 'queues') {
        me.messageReceived(data);
      }
    });
    this.$on('message.received', (msg) => {
      //console.log('QUEUE MESSAGE RECEIVED', msg);
    });
  },
  methods: {
    showQueue() {
      window.root.$emit('view.queue',this.name);
    },
    sizeOf(bytes) {
      if (bytes == 0) { return "0.00 B"; }
      var e = Math.floor(Math.log(bytes) / Math.log(1024));
      return (bytes/Math.pow(1024, e)).toFixed(2)+' '+' KMGTP'.charAt(e)+'B';
    },
    messageReceived(msg) {
      //console.log("QUEUES RECEIVED",msg);
      msg['queues'].forEach( (queue) => {
        //console.log("QUEUE NAME",queue['name'],this.name)
        if(queue['name'] == this.name) {
          //console.log("FOUND MY QUEUE",queue['messages'])
          this.messages = queue['messages']
          this.bytes = this.sizeOf(queue['message_bytes'])
        }
      })
      this.$emit('message.received', msg);
    },
    clickMe() {
      console.log('clicked');
    },
  },
  data() {
    return {
      model: 'sockq2.proc2.do_this',
      options: [
        'sockq2.proc2.do_this', 'sockq1.proc1.do_something', 'queue1', 'pyfi.processors.sample.do_this', 'pyfi.processors.sample.do_something	'
      ],
      messages: 0,
      bytes: 0,
      queueconfig: false,
    };
  },
};
</script>
