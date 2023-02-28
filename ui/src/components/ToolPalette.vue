<template>
  <div>
    <q-toolbar
      class="sidebar node-palette"
      style="padding:0px"
    >
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
        :icon="border"
        aria-label="Border"
        size="large"
        id="border"
        style="min-height: 56px; cursor: grabbing;"
        class="text-dark text-bold"
      >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Border
        </q-tooltip>
      </q-btn>
      <q-btn
        flat
        align="left"
        icon="las la-scroll"
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
        :disabled="!hasHosted"
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
      </q-btn>-->
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
      <!--
      <q-btn
        flat
        align="left"
        icon="las la-chart-area"
        aria-label="Chart"
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
          Chart
        </q-tooltip>
      </q-btn>-->
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
        :icon="markdown"
        aria-label="Label"
        size="xl"
        id="markdown"
        style=" min-height: 56px; cursor: grabbing;"
        class="text-dark text-bold"
      >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Markdown
        </q-tooltip>
      </q-btn>
      <q-btn
        flat
        align="left"
        icon="las la-robot"
        aria-label="Label"
        size="xl"
        id="chatgpt"
        style="display:none;min-height: 56px; cursor: grabbing;"
        class="text-dark text-bold"
      >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          ChatGPT
        </q-tooltip>
      </q-btn>
      <!--
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
      </q-btn>-->
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
        :disabled="!isProPlan"
        title="Upgrade to PRO Plan"
      >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Library
        </q-tooltip>
      </q-btn>
      <q-btn
        flat
        align="left"
        aria-label="AI Buddy"
        size="xl"
        id="chat"
        style="min-height: 56px; cursor: grabbing;"
        class="text-dark text-bold"
        @click="openChat"
        title="Python Tools"
      >
        <img
          src="~assets/images/python.svg"
          style="width:40px;min-width:40px"
        >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          Python Tools
        </q-tooltip>
      </q-btn>
      <q-btn
        flat
        align="left"
        icon="las la-ellipsis-h"
        aria-label="Elipsis"
        size="large"
        id="openblocks"
        style="min-height: 56px; cursor: grabbing;"
        class="text-dark text-bold"
        @click="openBlocks"
      >
        <q-tooltip
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          More Blocks
        </q-tooltip>
      </q-btn>
      <q-item-label class="text-secondary">BETA SOFTWARE</q-item-label>
      <q-space />
      <q-toolbar v-if="$auth.isAuthenticated && hasHosted">
        <q-space />
        <q-item-label
          class="text-secondary"
          style="margin-top: 40px; margin-right: 20px;"
        >
          <a
            class="link-hover"
            href="#"
            @click="showStats('Nodes', nodeStatsColumns, 'nodes')"
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
          >Tasks:</a>
          <span class="text-dark">{{ tasks }}</span>
        </q-item-label>
      </q-toolbar>
      <q-item-label
        class="text-secondary"
        style="margin-top: 40px;white-space: nowrap;"
        v-if="$auth.isAuthenticated && hasHosted"
      >
        System Usage:
      </q-item-label>
      <apexchart
        type="bar"
        height="50"
        width="100"
        :options="chartOptions"
        :series="series"
        style="margin-right: 280px;"
        v-if="$auth.isAuthenticated && hasHosted"
      />
      <q-item-label
        class="text-accent"
        style="white-space: nowrap;margin-top:40px;margin-right: -190px;"
      >
        {{ this.subscriptions[this.$store.state.designer.subscription] }}
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
              disabled
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

            <q-separator />
            <q-item
              clickable
              v-close-popup
              disabled
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
              disabled
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

            <q-separator />

            <q-item
              clickable
              v-close-popup
              disabled
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
              disabled
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
              disabled
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
              disabled
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
              disabled
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
              disabled
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
              :disabled="!this.$auth.isAuthenticated"
              @click="showProfile"
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
                @click="showAboutDialog=true"
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

    <q-dialog
      v-model="showAboutDialog"
      persistent
    >
      <q-card style="width:800px;height:500px;padding: 10px; padding-top: 30px;">
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
              margin-left: 10px;
              margin-top: -5px;
              margin-right: 5px;
              color: #fff;
            "
          >
            <q-toolbar>
              <q-item-label>
                <i
                  class="fas fa-info"
                  style="margin-right:20px"
                />About ElasticCode
              </q-item-label>
              <q-space />
              <q-btn
                class="text-primary"
                flat
                dense
                round
                size="sm"
                icon="fas fa-close"
                @click="showAboutDialog = false"
                style="z-index: 10;"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section
          class="row items-center"
          style="margin-top:30px"
        ><b>Build ID</b>: <a :href="buildUrl" target="build">{{ commit.substring(0,7) }}</a></q-card-section>

        <q-card-section
          class="row items-center"
        >
        <b>Build Date</b>: {{ buildDate }}</q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Ok"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog
      v-model="showProfileDialog"
      persistent
    >
      <q-card style="width:800px;height:500px;padding: 10px; padding-top: 30px;">
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
              margin-left: 10px;
              margin-top: -5px;
              margin-right: 5px;
              color: #fff;
            "
          >
            <q-toolbar>
              <q-item-label>
                <i
                  class="fas fa-user"
                  style="margin-right:20px"
                />Your Profile
              </q-item-label>
              <q-space />
              <q-btn
                class="text-primary"
                flat
                dense
                round
                size="sm"
                icon="fas fa-close"
                @click="showProfileDialog = false"
                style="z-index: 10;"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section
          class="row items-center"
          style="height: 120px;margin-top:20px"
        >
          <q-icon
            name="fas fa-user"
            color="primary"
            style="font-size:5em"
          />
        </q-card-section>
        <q-card-section
          class="row items-center"
        >
          <span style="font-size:2em">{{ $auth.user ? $auth.user.nickname : '' }}</span>
        </q-card-section>
        <q-card-section
          class="row items-center"
        >
          <span><b>Name</b>: {{ $auth.user ? $auth.user.name : '' }}</span>
        </q-card-section>
        <q-card-section
          class="row items-center"
        >
          <span><b>Email</b>: {{ $auth.user ? $auth.user.email : '' }}</span>
        </q-card-section>
        <q-card-section
          class="row items-center"
        >
          <span><b>Verified</b>: {{ $auth.user ? $auth.user.email_verified : '' }}</span>
        </q-card-section>
        <q-card-section
          class="row items-center"
        >
          <span><b>Last Updated</b>: {{ $auth.user ? $auth.user.updated_at : '' }}</span>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Ok"
            class="bg-secondary text-white"
            color="primary"
            @click="showProfileDialog = false"
            v-close-popup
          />
        </q-card-actions>
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
  color: black;
}

.link-hover:hover {
  text-decoration: underline;
}
</style>
<script>
/* eslint-disable @typescript-eslint/no-this-alias */
import { mdiCodeBraces } from '@mdi/js'
import { mdiBorderNoneVariant } from '@mdi/js'
import { mdiLanguagePython } from '@mdi/js'
import { mdiLanguageMarkdownOutline } from '@mdi/js';

import DataService from './util/DataService'

export default {
  name: 'ToolPalette',
  props: ['nodes', 'agents', 'queues', 'processors', 'tasks', 'deployments', 'cpus_total', 'cpus_running'],
  created () {
    this.braces = mdiCodeBraces
    this.border = mdiBorderNoneVariant
    this.python = mdiLanguagePython
    this.markdown = mdiLanguageMarkdownOutline
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
    hasHosted () {
      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] >= this.HOSTED
      } else {
        return false
      }
    },
    isProPlan () {
      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] >= this.PRO
      } else {
        return false
      }
    }
  },
  watch: {
    '$store.state.designer.subscription': function (sub) {

    }
  },
  methods: {
    setCommit (commit, buildDate, buildUrl, repoUrl) {
      this.commit = commit
      this.buildDate = buildDate
      this.buildUrl = buildUrl
      this.repoUrl = repoUrl
    },
    hasEnterprise () {
      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] === this.ENTERPRISE
      } else {
        return false
      }
    },
    showProfile () {
      console.log(this.$auth.user)
      this.showProfileDialog = this.$auth.isAuthenticated
    },
    logout () {
      this.$auth.logout({ returnTo: '/logout' })
    },
    login () {
      this.$root.$emit('login')
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
      const style = document.createElement('link')
      style.setAttribute('href', 'https://pyscript.net/latest/pyscript.css')
      style.setAttribute('rel', 'stylesheet')
      script.setAttribute('src', 'https://pyscript.net/latest/pyscript.js')
      script.setAttribute('type', 'application/javascript')
      head.appendChild(style)
      head.appendChild(script)
    },
    openBlocks () {
      this.$root.$emit('open.blocks')
    },
    openChat () {
      this.$root.$emit('open.chat')
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
      GUEST: 0,
      FREE: 1,
      DEVELOPER: 2,
      PRO: 3,
      HOSTED: 4,
      ENTERPRISE: 5,
      subscriptions: {
        'ec_developer-USD-Monthly': 'Developer',
        'ec_hosted-USD-Yearly': 'Hosted'
      },
      buildDate: 'N/A',
      sublevel: {
        guest: 0,
        free: 1,
        'ec_developer-USD-Monthly': 2,
        'ec_pro-USD-Monthly': 3,
        'ec_hosted-USD-Yearly': 4
      },
      showProfileDialog: false,
      showAboutDialog: false,
      viewStatsLoader: false,
      commit: '',
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
          theme: 'dark',
          y: {
            title: {
              formatter: function (seriesName) {
                return 'Tasks'
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
