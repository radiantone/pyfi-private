<template>
  <div
    :style="'box-shadow: 0 0 5px grey;background-color: rgb(244, 246, 247);z-index: 999999; \
      width: 300px; \
      height: 40px; \
      padding: 3px; \
      visibility: '+visibility+'; \
      font-size: 14px;'
    "
  >
    <q-toolbar style="position: absolute; left: 0px; top: -13px;">
      <q-item-label
        style="margin-left: 5px; font-weight: bold; color: #775351;"
        :data-source="node"
        class="fas fa-email"
      >
        <q-select
          style="width: 275px;"
          v-model="queueName"
          :options="queues"
          :dense="true"
          :options-dense="true"
          :menu-offset="[5, -9]"
          @input="queueSelect"
        >
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
      <q-btn
        flat
        dense
        size="xs"
        icon="close"
        color="primary"
        @click="deleteEdgeConfirm = true"
        style="cursor: pointer; font-size: 0.7em; position: absolute; right: 5px;"
      >
        <q-tooltip
          anchor="top middle"
          :offset="[-30, 40]"
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Remove Edge
        </q-tooltip>
      </q-btn>

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
        font-family: 'Roboto', '-apple-system', 'Helvetica Neue', Helvetica, Arial, sans-serif;
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
      <span style="font-weight: bold; color: #775351;">{{ messages }} ({{ bytes }} bytes)</span>
      <q-btn
        flat
        dense
        icon="fas fa-chart-bar"
        size="xs"
        color="primary"
        style="cursor: pointer; font-size: 0.7em; position: absolute; right: 25px;"
        @click="bandwidthView = !bandwidthView"
      >
        <q-tooltip
          anchor="top middle"
          :offset="[-30, 40]"
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Bandwidth Chart
        </q-tooltip>
      </q-btn>
      <q-btn
        flat
        dense
        icon="menu"
        size="xs"
        @click="showQueue"
        color="primary"
        style="cursor: pointer; font-size: 0.7em; position: absolute; right: 5px;"
      >
        <q-tooltip
          anchor="top middle"
          :offset="[-30, 40]"
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Queued Messages
        </q-tooltip>
      </q-btn>

      <div v-if="bandwidthView">
        <apexchart
          type="area"
          height="190"
          width="300px"
          style="position: absolute; left: -20px;"
          :options="chartOptions2"
          :series="series2"
        />
      </div>
    </div>
    <q-card
      style="
        width: 350px;
        height: 400px;
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

    <q-dialog
      v-model="deleteEdgeConfirm"
      persistent
    >
      <q-card style="padding: 10px; padding-top: 30px;">
        <q-card-section
          class="bg-secondary"
          style="position: absolute; left: 0px; top: 0px; width: 100%; height: 40px;"
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
              <q-item-label>Delete Edge</q-item-label>
              <q-space />
              <q-icon
                class="text-primary"
                name="fas fa-trash"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section
          class="row items-center"
          style="height: 120px;"
        >
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Are you sure you want to delete this edge?
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
            @click="deleteEdge"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>
<script>
import { io, Socket } from 'socket.io-client'

const socket = io('https://app.elasticcode.ai')

export default {
  name: 'Button',
  props: ['node', 'name', 'component', 'hide'],
  mounted () {
    console.log('QUEUE NODE', this.component)
    window.root.$on('update.queues', (queues) => {
      this.queues = queues.map((queue) => queue.name)
    })
  },
  created () {
    var me = this
    if(this.hide) {
      this.visibility = 'hidden'
    }
    socket.on('global', (data) => {
      // console.log('QUEUE SERVER GLOBAL MESSAGE', data);
      if (data.type && data.type === 'queues') {
        me.messageReceived(data)
      }
    })
    this.$on('message.received', (msg) => {
      // console.log('QUEUE MESSAGE RECEIVED', msg);
    })
    if (this.component.edge) {
      this.queueName = this.component.edge.data.queue
    } else {
      this.queueName = 'None'
    }
  },
  computed: {},
  methods: {
    queueSelect (val) {
      console.log('QUEUE SELECTED ', val)
      this.component.edge.data.queue = val
    },
    deleteEdge () {
      console.log('Deleting edge ', this.component)
      window.toolkit.removeEdge(this.component.edge)
    },
    showQueue () {
      window.root.$emit('view.queue', this.queueName)
    },
    sizeOf (bytes) {
      if (bytes === 0) {
        return '0.00 B'
      }
      var e = Math.floor(Math.log(bytes) / Math.log(1024))
      return (bytes / Math.pow(1024, e)).toFixed(2) + ' ' + ' KMGTP'.charAt(e) + 'B'
    },
    messageReceived (msg) {
      // console.log("QUEUES RECEIVED",msg);
      msg.queues.forEach((queue) => {
        // console.log("QUEUE NAME",queue['name'],this.name)
        if (queue.name === this.queueName) {
          // console.log("FOUND MY QUEUE",queue['messages'])
          this.messages = queue.messages
          this.bytes = this.sizeOf(queue.message_bytes)
        }
      })
      this.$emit('message.received', msg)
    },
    clickMe () {
      console.log('clicked')
    }
  },
  data () {
    return {
      visibility: 'visible',
      chartOptions2: {
        dataLabels: {
          enabled: false
        },
        fill: {
          type: 'gradient',
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.9,
            stops: [0, 100]
          }
        },
        stroke: {
          show: true,
          colors: ['#abbcc3', '#6b8791', '#e3e8ec', '#054848'],
          width: 1,
          dashArray: 0
        },
        colors: ['#abbcc3', '#6b8791', '#e3e8ec', '#054848'],
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          }
        },
        plotOptions: {
          candlestick: {
            colors: {
              upward: '#abbcc3',
              downward: '#6b8791'
            },
            wick: {
              useFillColor: true
            }
          }
        },
        candlestick: {
          colors: {
            upward: '#abbcc3',
            downward: '#6b8791'
          },
          wick: {
            useFillColor: true
          }
        },
        chart: {
          toolbar: {
            show: false
          },
          type: 'line',
          height: 350
        },
        xaxis: {
          type: 'datetime'
        },
        yaxis: {
          tooltip: {
            enabled: true
          },
          labels: {
            show: false
          }
        }
      },
      series2: [
        {
          data: [
            {
              x: new Date(1538778600000),
              y: [6629.81, 6650.5, 6623.04, 6633.33]
            },
            {
              x: new Date(1538780400000),
              y: [6632.01, 6643.59, 6620, 6630.11]
            },
            {
              x: new Date(1538782200000),
              y: [6630.71, 6648.95, 6623.34, 6635.65]
            },
            {
              x: new Date(1538784000000),
              y: [6635.65, 6651, 6629.67, 6638.24]
            },
            {
              x: new Date(1538785800000),
              y: [6638.24, 6640, 6620, 6624.47]
            },
            {
              x: new Date(1538787600000),
              y: [6624.53, 6636.03, 6621.68, 6624.31]
            },
            {
              x: new Date(1538789400000),
              y: [6624.61, 6632.2, 6617, 6626.02]
            },
            {
              x: new Date(1538791200000),
              y: [6627, 6627.62, 6584.22, 6603.02]
            },
            {
              x: new Date(1538793000000),
              y: [6605, 6608.03, 6598.95, 6604.01]
            },
            {
              x: new Date(1538794800000),
              y: [6604.5, 6614.4, 6602.26, 6608.02]
            },
            {
              x: new Date(1538796600000),
              y: [6608.02, 6610.68, 6601.99, 6608.91]
            },
            {
              x: new Date(1538798400000),
              y: [6608.91, 6618.99, 6608.01, 6612]
            },
            {
              x: new Date(1538800200000),
              y: [6612, 6615.13, 6605.09, 6612]
            },
            {
              x: new Date(1538802000000),
              y: [6612, 6624.12, 6608.43, 6622.95]
            },
            {
              x: new Date(1538803800000),
              y: [6623.91, 6623.91, 6615, 6615.67]
            },
            {
              x: new Date(1538805600000),
              y: [6618.69, 6618.74, 6610, 6610.4]
            },
            {
              x: new Date(1538807400000),
              y: [6611, 6622.78, 6610.4, 6614.9]
            },
            {
              x: new Date(1538809200000),
              y: [6614.9, 6626.2, 6613.33, 6623.45]
            },
            {
              x: new Date(1538811000000),
              y: [6623.48, 6627, 6618.38, 6620.35]
            },
            {
              x: new Date(1538812800000),
              y: [6619.43, 6620.35, 6610.05, 6615.53]
            },
            {
              x: new Date(1538814600000),
              y: [6615.53, 6617.93, 6610, 6615.19]
            },
            {
              x: new Date(1538816400000),
              y: [6615.19, 6621.6, 6608.2, 6620]
            },
            {
              x: new Date(1538818200000),
              y: [6619.54, 6625.17, 6614.15, 6620]
            },
            {
              x: new Date(1538820000000),
              y: [6620.33, 6634.15, 6617.24, 6624.61]
            },
            {
              x: new Date(1538821800000),
              y: [6625.95, 6626, 6611.66, 6617.58]
            },
            {
              x: new Date(1538823600000),
              y: [6619, 6625.97, 6595.27, 6598.86]
            },
            {
              x: new Date(1538825400000),
              y: [6598.86, 6598.88, 6570, 6587.16]
            },
            {
              x: new Date(1538827200000),
              y: [6588.86, 6600, 6580, 6593.4]
            },
            {
              x: new Date(1538829000000),
              y: [6593.99, 6598.89, 6585, 6587.81]
            },
            {
              x: new Date(1538830800000),
              y: [6587.81, 6592.73, 6567.14, 6578]
            },
            {
              x: new Date(1538832600000),
              y: [6578.35, 6581.72, 6567.39, 6579]
            },
            {
              x: new Date(1538834400000),
              y: [6579.38, 6580.92, 6566.77, 6575.96]
            },
            {
              x: new Date(1538836200000),
              y: [6575.96, 6589, 6571.77, 6588.92]
            },
            {
              x: new Date(1538838000000),
              y: [6588.92, 6594, 6577.55, 6589.22]
            },
            {
              x: new Date(1538839800000),
              y: [6589.3, 6598.89, 6589.1, 6596.08]
            },
            {
              x: new Date(1538841600000),
              y: [6597.5, 6600, 6588.39, 6596.25]
            },
            {
              x: new Date(1538843400000),
              y: [6598.03, 6600, 6588.73, 6595.97]
            },
            {
              x: new Date(1538845200000),
              y: [6595.97, 6602.01, 6588.17, 6602]
            },
            {
              x: new Date(1538847000000),
              y: [6602, 6607, 6596.51, 6599.95]
            },
            {
              x: new Date(1538848800000),
              y: [6600.63, 6601.21, 6590.39, 6591.02]
            },
            {
              x: new Date(1538850600000),
              y: [6591.02, 6603.08, 6591, 6591]
            },
            {
              x: new Date(1538852400000),
              y: [6591, 6601.32, 6585, 6592]
            },
            {
              x: new Date(1538854200000),
              y: [6593.13, 6596.01, 6590, 6593.34]
            },
            {
              x: new Date(1538856000000),
              y: [6593.34, 6604.76, 6582.63, 6593.86]
            },
            {
              x: new Date(1538857800000),
              y: [6593.86, 6604.28, 6586.57, 6600.01]
            },
            {
              x: new Date(1538859600000),
              y: [6601.81, 6603.21, 6592.78, 6596.25]
            },
            {
              x: new Date(1538861400000),
              y: [6596.25, 6604.2, 6590, 6602.99]
            },
            {
              x: new Date(1538863200000),
              y: [6602.99, 6606, 6584.99, 6587.81]
            },
            {
              x: new Date(1538865000000),
              y: [6587.81, 6595, 6583.27, 6591.96]
            },
            {
              x: new Date(1538866800000),
              y: [6591.97, 6596.07, 6585, 6588.39]
            },
            {
              x: new Date(1538868600000),
              y: [6587.6, 6598.21, 6587.6, 6594.27]
            },
            {
              x: new Date(1538870400000),
              y: [6596.44, 6601, 6590, 6596.55]
            },
            {
              x: new Date(1538872200000),
              y: [6598.91, 6605, 6596.61, 6600.02]
            },
            {
              x: new Date(1538874000000),
              y: [6600.55, 6605, 6589.14, 6593.01]
            },
            {
              x: new Date(1538875800000),
              y: [6593.15, 6605, 6592, 6603.06]
            },
            {
              x: new Date(1538877600000),
              y: [6603.07, 6604.5, 6599.09, 6603.89]
            },
            {
              x: new Date(1538879400000),
              y: [6604.44, 6604.44, 6600, 6603.5]
            },
            {
              x: new Date(1538881200000),
              y: [6603.5, 6603.99, 6597.5, 6603.86]
            },
            {
              x: new Date(1538883000000),
              y: [6603.85, 6605, 6600, 6604.07]
            },
            {
              x: new Date(1538884800000),
              y: [6604.98, 6606, 6604.07, 6606]
            }
          ]
        }
      ],
      bandwidthView: false,
      choosequeue: false,
      deleteEdgeConfirm: false,
      queueName: 'None',
      queues: [],
      obj: {},
      messages: 0,
      bytes: 0,
      queueconfig: false
    }
  }
}
</script>
