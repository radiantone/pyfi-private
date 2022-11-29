<template>
  <div>
    <q-toolbar class="sidebar node-palette">
      <img
        src="~assets/images/elasticcode.svg"
        style="padding-left: 15px; height: 55px; padding-right: 10px;"
      >
      <q-btn
        flat
        align="left"
        icon="las la-file-alt"
        aria-label="Data"
        size="large"
        id="data"
        style="min-height: 56px; cursor: grabbing; font-size: 1.5em;"
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
        aria-label="Schema"
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
        icon="img:/images/python.svg"
        aria-label="Script"
        size="xl"
        id="script"
        style="min-height: 56px; cursor: grabbing;"
        class="text-dark text-bold"
      >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Script
        </q-tooltip>
      </q-btn>
      <q-btn
        flat
        align="left"
        icon="las la-cloud-upload-alt"
        aria-label="API"
        size="xl"
        id="api"
        style="min-height: 56px; cursor: grabbing;"
        class="text-dark text-bold"
      >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          API
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
        :disabled="!isProPlan"
        title="Upgrade to PRO Plan"
      >
        <!--:disabled="false"-->
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
        :disabled="!isProPlan"
        title="Upgrade to PRO Plan"
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
        :disabled="!isProPlan"
        title="Upgrade to PRO Plan"
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
      <!--
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
      <q-btn
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
        :disabled="!isProPlan"
        title="Upgrade to PRO Plan"
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
        icon="las la-database"
        aria-label="Database"
        size="xl"
        id="database"
        style="min-height: 56px; cursor: grabbing;"
        class="text-dark text-bold"
        :disabled="!isProPlan"
        title="Upgrade to PRO Plan"
      >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Database
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
        <a
          class="link-hover"
          href="#"
          @click="showStats('Nodes', nodeStatsColumns, 'nodes')"
          :disabled="false"
        >Nodes:</a>
        <span class="text-dark">{{ nodes }}</span>
      </q-item-label>
      <q-item-label
        class="text-secondary"
        style="margin-top: 40px; margin-right: 20px;"
        :disabled="false"
      >
        <a
          class="link-hover"
          href="#"
          @click="showStats('Agents', agentStatsColumns,'agents')"
          :disabled="false"
        >Agents:</a>
        <span class="text-dark">{{ agents }}</span>
      </q-item-label>
      <q-item-label
        class="text-secondary"
        style="margin-top: 40px; margin-right: 20px;"
      >
        <a
          class="link-hover"
          href="#"
          @click="showStats('Queues', queueStatsColumns,'queues')"
          :disabled="false"
        >Queues:</a>
        <span class="text-dark">{{ queues }}</span>
      </q-item-label>
      <q-item-label
        class="text-secondary"
        style="margin-top: 40px; margin-right: 20px;"
      >
        <a
          class="link-hover"
          href="#"
          @click="showStats('Processors', procStatsColumns, 'processors')"
          :disabled="false"
        >Processors:</a>
        <span class="text-dark">{{ processors }}</span>
      </q-item-label>
      <q-item-label
        class="text-secondary"
        style="margin-top: 40px; margin-right: 20px;"
      >
        <a
          class="link-hover"
          href="#"
          @click="showStats('Deployments', deployStatsColumns, 'deployments')"
          :disabled="false"
        >Deployments:</a>
        <span class="text-dark">{{ deployments }}</span>
      </q-item-label>
      <q-item-label
        class="text-secondary"
        style="margin-top: 40px; margin-right: 20px;"
      >
        <a
          class="link-hover"
          href="#"
          @click="showStats('CPUs', workerStatsColumns, 'workers')"
          :disabled="false"
        >CPUS:</a>
        <span class="text-dark">{{ cpus_running }}/{{ cpus_total }}</span>
      </q-item-label>
      <q-item-label
        class="text-secondary"
        style="margin-top: 40px; margin-right: 20px;"
      >
        <a
          class="link-hover"
          href="#"
          @click="showStats('Tasks', taskStatsColumns, 'tasks')"
          :disabled="false"
        >Tasks:</a>
        <span class="text-dark">{{ tasks }}</span>
      </q-item-label>
      <q-item-label
        class="text-secondary"
        style="margin-top: 40px;white-space: nowrap;"
        :disabled="false"
      >
        System Usage:
      </q-item-label>
      <apexchart
        type="bar"
        height="50"
        width="100"
        :options="chartOptions"
        :series="series"
        style="margin-right: 80px;"
      />
      <q-item-label
        class="text-accent"
        style="white-space: nowrap;margin-top:40px;margin-right: 20px;"
      >
        {{ this.$store.state.designer.subscription }}
      </q-item-label>
      <q-item-label
        class="text-dark"
        style="white-space: nowrap;"
      >
        <div v-if="!$auth.loading">
          <!-- show login when not authenticated -->
          <button
            v-if="!$auth.isAuthenticated"
            @click="login"
          >
            Log in
          </button>
          <!-- show logout when authenticated -->
          <button
            v-if="$auth.isAuthenticated"
            @click="logout"
          >
            Log out {{ $auth.user.name }}
          </button>
        </div>
      </q-item-label>
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
            <q-item
              clickable
              v-close-popup
              @click="newFlow"
            >
              <q-item-section side>
                <q-icon name="fas fa-plus" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                New Flow
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
              @click="newQueue"
            >
              <q-item-section side>
                <q-icon name="far fa-envelope" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                New Queue
              </q-item-section>
            </q-item>

            <q-item
              clickable
              v-close-popup
              @click="checkout"
            >
              <q-item-section side>
                <q-icon name="far fa-envelope" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Checkout
              </q-item-section>
            </q-item>

            <q-separator />
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-table" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Summary
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-calculator" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Counters
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="loadPython"
            >
              <q-item-section side>
                <q-icon name="fab fa-python" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Load Python
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="far fa-sticky-note" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Bulletin Board
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-database" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Data Provenance
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-wrench" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Controller Settings
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-list-alt" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Parameter Contexts
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fa fa-history" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Flow Configuration History
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fa fa-area-chart" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Node Status History
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-project-diagram" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Templates
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
              @click="$router.push('/profile')"
            >
              <q-item-section side>
                <q-icon name="fas fa-user" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Profile
              </q-item-section>
            </q-item>

            <q-item
              clickable
              v-close-popup
              @click="manage"
            >
              <q-item-section side>
                <q-icon name="far fa-envelope" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Manage Plan
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-question-circle" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Help
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-info-circle" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                About
              </q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
    </q-toolbar>

    <q-dialog
      v-model="viewStatsDialog"
      persistent
    >
      <q-card style="padding: 10px; padding-top: 30px; min-width: 40vw; height: 50%;">
        <q-card-section
          class="bg-secondary"
          style="position: absolute; left: 0px; top: 0px; width: 100%; height: 40px;"
        >
          <div
            style="
              font-weight: bold;
              font-size: 18px;
              margin-left: 10px;
              margin-top: -5px;
              margin-right: 5px;
              color: #fff;
            "
          >
            <q-toolbar>
              <q-item-label>{{ statname }}</q-item-label>
              <q-space />
              <q-icon
                class="text-primary"
                name="fas fa-close"
                @click="viewStatsDialog = false"
                style="z-index: 10; cursor: pointer;"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section
          class="row items-center"
          style="height: 120px; width: 100%;"
        >
          <q-table
            dense
            :columns="viewStatsColumns"
            :data="viewStatsData"
            row-key="name"
            flat
            style="width: 100%; margin-top: 20px; border-top-radius: 0px; border-bottom-radius: 0px;"
          />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Close"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
          />
        </q-card-actions>
        <q-inner-loading
          :showing="viewStatsLoader"
          style="z-index: 9999999;"
        >
          <q-spinner-gears
            size="50px"
            color="primary"
          />
        </q-inner-loading>
      </q-card>
    </q-dialog>
  </div>
</template>
<style scoped>
.my-custom-toggle {
  border: 1px solid #6b8791;
}
.apexcharts-tooltip {
  background: black;
  color: white;
}

.link-hover:hover {
  text-decoration: underline;
}
</style>
<script>
/* eslint-disable @typescript-eslint/no-this-alias */
import { mdiCodeBraces } from '@mdi/js'
import DataService from './util/DataService'

export default {
  name: 'ToolPalette',
  props: ['nodes', 'agents', 'queues', 'processors', 'tasks', 'deployments', 'cpus_total', 'cpus_running'],
  created () {
    this.braces = mdiCodeBraces
  },
  mounted () {
    const me = this

    console.log('TOOLPALETTE STORE', this.$store)
    this.$root.$on('show.objects', (objects) => {
      console.log('show.objects ', objects)
      // eslint-disable-next-line @typescript-eslint/no-unsafe-call
      me.showStats(objects.name, objects.columns, objects.objects)
    })
  },
  computed: {
    isProPlan () {
      return this.$store.state.designer.subscription.toString().indexOf('pro') >= 0
    }
  },
  watch: {
    '$store.state.designer.subscription': function (sub) {

    }
  },
  methods: {
    showProfile () {

    },
    logout () {
      this.$auth.logout({ returnTo: '/logout' })
    },
    login () {
      this.$root.$emit('login')
    },
    getVersion () {
      if (this.$store.state.designer.version.indexOf('Free') >= 0) {
        return 'FREE'
      } else {
        return 'DEV'
      }
    },
    showStats (name, columns, objects) {
      const me = this
      if (this.false) {
        return
      }
      this.statname = name
      this.viewStatsColumns = columns
      this.viewStatsLoader = true
      this.viewStatsDialog = true
      me.viewStatsData = []
      DataService.getObjects(objects, this.$store.state.designer.token).then((response) => {
        me.viewStatsData = response.data
        console.log(name + ' STATS:', response.data)
        me.viewStatsLoader = false
      }).catch((error) => {
        me.notifyMessage('dark', 'error', 'Something went wrong')
        me.viewStatsLoader = false
      })
    },

    notifyMessage (color, icon, message) {
      this.$q.notify({
        color: color,
        timeout: 2000,
        position: 'top',
        message: message,
        icon: icon
      })
    },
    loadPython () {
      const head = document.getElementById('head')
      const script = document.createElement('script')
      script.setAttribute('src', 'https://pyscript.net/alpha/pyscript.js')
      script.setAttribute('type', 'application/javascript')
      head.appendChild(script)
    },
    openLibrary () {
      this.$root.$emit('open.library')
    },
    newFlow () {
      this.$root.$emit('new.flow')
    },
    newQueue () {
      this.$root.$emit('new.queue')
    },
    checkout () {
      this.$root.$emit('checkout')
    },
    manage () {
      this.$root.$emit('manage.subscription')
    },
    upgrade () {
      this.$root.$emit('upgrade.subscription')
    }
  },
  data () {
    return {
      viewStatsLoader: false,
      deployStatsColumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        },
        {
          name: 'created',
          label: 'Created On',
          field: 'created',
          align: 'left'
        },
        {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        },
        {
          name: 'hostname',
          label: 'Host',
          field: 'hostname',
          align: 'left'
        },
        {
          name: 'cpus',
          label: 'CPUS',
          field: 'cpus',
          align: 'left'
        },
        {
          name: 'status',
          label: 'Status',
          field: 'status',
          align: 'left'
        }
      ],
      taskStatsColumns: [
        {
          name: 'name',
          label: 'Function',
          field: 'name',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        },
        {
          name: 'created',
          label: 'Created On',
          field: 'created',
          align: 'left'
        },
        {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        },
        {
          name: 'module',
          label: 'Module',
          field: 'module',
          align: 'left'
        },
        {
          name: 'deployments',
          label: 'Deployments',
          field: 'deployments',
          align: 'left'
        }
      ],
      nodeStatsColumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        },
        {
          name: 'created',
          label: 'Created On',
          field: 'created',
          align: 'left'
        },
        {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        },
        {
          name: 'hostname',
          label: 'Host',
          field: 'hostname',
          align: 'left'
        },
        {
          name: 'cpus',
          label: 'CPUS',
          field: 'cpus',
          align: 'left'
        },
        {
          name: 'status',
          label: 'Status',
          field: 'status',
          align: 'left'
        }
      ],
      agentStatsColumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        },
        {
          name: 'created',
          label: 'Created On',
          field: 'created',
          align: 'left'
        },
        {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        },
        {
          name: 'hostname',
          label: 'Host',
          field: 'hostname',
          align: 'left'
        },
        {
          name: 'cpus',
          label: 'CPUS',
          field: 'cpus',
          align: 'left'
        },
        {
          name: 'status',
          label: 'Status',
          field: 'status',
          align: 'left'
        }
      ],
      queueStatsColumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        },
        {
          name: 'id',
          label: 'ID',
          field: 'id',
          align: 'left'
        },
        {
          name: 'type',
          label: 'Type',
          field: 'type',
          align: 'left'
        },
        {
          name: 'created',
          label: 'Created On',
          field: 'created',
          align: 'left'
        },
        {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        },
        {
          name: 'status',
          label: 'Status',
          field: 'status',
          align: 'left'
        }
      ],
      procStatsColumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        },
        {
          name: 'id',
          label: 'ID',
          field: 'id',
          align: 'left'
        },
        {
          name: 'concurrency',
          label: 'Concurrency',
          field: 'concurrency',
          align: 'left'
        },
        {
          name: 'created',
          label: 'Created On',
          field: 'created',
          align: 'left'
        },
        {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        },
        {
          name: 'status',
          label: 'Status',
          field: 'status',
          align: 'left'
        }
      ],
      workerStatsColumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        },
        {
          name: 'id',
          label: 'ID',
          field: 'id',
          align: 'left'
        },
        {
          name: 'concurrency',
          label: 'Concurrency',
          field: 'concurrency',
          align: 'left'
        },
        {
          name: 'created',
          label: 'Created On',
          field: 'created',
          align: 'left'
        },
        {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        },
        {
          name: 'status',
          label: 'Status',
          field: 'status',
          align: 'left'
        }
      ],
      viewStatsColumns: [],
      viewStatsData: [],
      viewStatsDialog: false,
      statcolumns: [],
      statname: '',
      statdata: [],
      variablecolumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'value',
          label: 'Value',
          field: 'value',
          align: 'left'
        },
        {
          name: 'scope',
          label: 'Scope',
          field: 'scope',
          align: 'left'
        }
      ],
      variabledata: [],
      mode: 'code',
      series: [
        {
          data: [12, 14, 2, 47, 42, 15, 47, 75, 65, 19, 14]
        }
      ],
      chartOptions: {
        colors: ['#e3e8ec', '#054848'],
        chart: {
          type: 'bar',
          width: 100,
          height: 35,
          sparkline: {
            enabled: true
          }
        },
        plotOptions: {
          bar: {
            columnWidth: '50%'
          }
        },
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: {
          crosshairs: {
            width: 1
          }
        },
        tooltip: {
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function (seriesName) {
                return 'Value'
              }
            }
          },
          marker: {
            show: false
          }
        }
      }
    }
  }
}
</script>
