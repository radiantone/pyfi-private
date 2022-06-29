<template>
  <q-toolbar class="sidebar node-palette">
    <img
      src="~assets/images/pyfi.svg"
      style="padding-left: 15px; height: 45px; padding-right: 10px;"
    />
    <q-btn
      flat
      align="left"
      icon="las la-file-alt"
      aria-label="Data"
      size="large"
      id="data"
      style="min-height: 56px; cursor: grabbing;font-size:1.5em"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Data
      </q-tooltip>
    </q-btn>
    <q-btn
      flat
      align="left"
      :icon="braces"
      aria-label="Data"
      size="large"
      id="schema"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Schema
      </q-tooltip>
    </q-btn>
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
      data-node-icon="far fa-object-group"
      data-node-type="group"
      data-node-name="Group"
      data-node-label="Group"
      data-node-description="A processor group description"
      data-node-package="my.python.package"
      data-node-id="group"
      jtk-is-group="true"
      id="processorgroup"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold sidebar-item"
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
      icon="segment"
      aria-label="Parallel Node"
      id="parallel"
      size="large"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Parallel
      </q-tooltip>
    </q-btn>
    <q-btn
      flat
      align="left"
      icon="fas fa-long-arrow-alt-right"
      aria-label="Pipeline Node"
      size="large"
      id="pipeline"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Pipeline
      </q-tooltip>
    </q-btn>

    <q-btn
      flat
      align="left"
      icon="low_priority"
      aria-label="Chord Node"
      size="large"
      id="chord"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Chord
      </q-tooltip>
    </q-btn>
    <q-btn
      flat
      align="left"
      icon="grid_view"
      aria-label="Segment Node"
      size="large"
      id="segment"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Segment
      </q-tooltip>
    </q-btn>
    <!--<q-btn
      flat
      align="left"
      icon="icon-map"
      aria-label="Map Node"
      size="large"
      id="map"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Map
      </q-tooltip>
    </q-btn>
    <q-btn
      flat
      align="left"
      icon="icon-funnel"
      aria-label="Reduce Node"
      size="large"
      id="reduce"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Reduce
      </q-tooltip>
    </q-btn>-->
    <q-btn
      flat
      align="left"
      icon="alt_route"
      aria-label="Router"
      size="large"
      id="router"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Router
      </q-tooltip>
    </q-btn>
    <q-btn
      flat
      align="left"
      icon="las la-chart-area"
      aria-label="Chart"
      size="large"
      id="router"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Chart
      </q-tooltip>
    </q-btn>
    <q-btn
      flat
      align="left"
      icon="icon-label"
      aria-label="Label"
      size="large"
      id="label"
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
    <q-btn
      flat
      align="left"
      icon="las la-window-maximize"
      aria-label="App"
      size="xl"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
      @click="$router.push('/app')"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        App
      </q-tooltip>
    </q-btn>
    <q-btn
      flat
      align="left"
      icon="las la-book"
      aria-label="App"
      size="xl"
      id="library"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
      @click="openLibrary"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Library
      </q-tooltip>
    </q-btn>
    <q-space />

    <q-item-label
      class="text-secondary"
      style="margin-top: 40px; margin-right: 20px;"
    >
      Active Hosts:
      <span class="text-dark">17</span>
    </q-item-label>

    <q-item-label
      class="text-secondary"
      style="margin-top: 40px; margin-right: 20px;"
    >
      Active Queues:
      <span class="text-dark">20</span>
    </q-item-label>
    <q-item-label
      class="text-secondary"
      style="margin-top: 40px; margin-right: 20px;"
    >
      Active Processors:
      <span class="text-dark">125</span>
    </q-item-label>
    <q-item-label class="text-secondary" style="margin-top: 40px;">
      System Usage:
    </q-item-label>
    <apexchart
      type="bar"
      height="50"
      width="100"
      :options="chartOptions"
      :series="series"
      style="margin-right: 200px;"
    ></apexchart>
    <q-item-label class="text-dark">Welcome, Darren!</q-item-label>
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
          <q-item clickable v-close-popup @click="newFlow">
            <q-item-section side>
              <q-icon name="fas fa-plus"></q-icon>
            </q-item-section>
            <q-item-section side class="text-blue-grey-8">
              New Flow
            </q-item-section>
          </q-item>
          <q-separator />
          <q-item clickable v-close-popup @click="newQueue">
            <q-item-section side>
              <q-icon name="far fa-envelope"></q-icon>
            </q-item-section>
            <q-item-section side class="text-blue-grey-8">
              New Queue
            </q-item-section>
          </q-item>
          <q-separator />
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
          <q-separator />
          <q-item clickable v-close-popup>
            <q-item-section side>
              <q-icon name="fas fa-user"></q-icon>
            </q-item-section>
            <q-item-section side class="text-blue-grey-8">
              Profile
            </q-item-section>
          </q-item>
          <q-separator />
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
</template>
<style scoped>
.my-custom-toggle {
  border: 1px solid #6b8791;
}
.apexcharts-tooltip {
  background: black;
  color: white;
}
</style>
<script>
import { SurfaceDrop } from 'jsplumbtoolkit-vue2-drop';
import { mdiCodeBraces } from '@mdi/js';

export default {
  name: 'ToolPalette',
  created () {
    
    this.braces = mdiCodeBraces;
  },
  mounted() {
    console.log('TOOLPALETTE STORE', this.$store);
  },
  methods: {
    openLibrary () {
      this.$root.$emit('open.library');
    },
    newFlow() {
      this.$root.$emit('new.flow');
    },
    newQueue() {
      this.$root.$emit('new.queue');
    },
  },
  data() {
    return {
      mode: 'code',
      series: [
        {
          data: [12, 14, 2, 47, 42, 15, 47, 75, 65, 19, 14],
        },
      ],
      chartOptions: {
        colors: ['#e3e8ec', '#054848'],
        chart: {
          type: 'bar',
          width: 100,
          height: 35,
          sparkline: {
            enabled: true,
          },
        },
        plotOptions: {
          bar: {
            columnWidth: '50%',
          },
        },
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: {
          crosshairs: {
            width: 1,
          },
        },
        tooltip: {
          fixed: {
            enabled: false,
          },
          x: {
            show: false,
          },
          y: {
            title: {
              formatter: function (seriesName) {
                return 'Value';
              },
            },
          },
          marker: {
            show: false,
          },
        },
      },
    };
  },
};
</script>
