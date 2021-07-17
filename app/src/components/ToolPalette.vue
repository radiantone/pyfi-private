<template>
      <q-toolbar class="sidebar node-palette" >
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
</template>
<style>
</style>
<script>
import { SurfaceDrop } from 'jsplumbtoolkit-vue2-drop';

export default {
  name: 'ToolPalette',
  //mixins: [SurfaceDrop],
  created () {
  }
}
</script>