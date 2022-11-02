<template>
  <q-toolbar class="sidebar node-palette">
    <img
      src="~assets/images/elasticcode.svg"
      style="padding-left: 15px; height: 55px; padding-right: 10px;"
    />

    <q-btn
      flat
      align="left"
      icon="format_list_bulleted"
      aria-label="Processor"
      size="large"
      id="class"
      style="min-height: 56px; cursor: grabbing;"
      class="text-dark text-bold"
    >
      <q-tooltip
        content-style="font-size: 16px"
        content-class="bg-black text-white"
      >
        Class
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

export default {
  name: 'ModelToolPalette',
  created() {},
  mounted() {
    console.log('TOOLPALETTE STORE', this.$store);
  },
  methods: {
    newFlow() {
      this.$root.$emit('new.flow');
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
