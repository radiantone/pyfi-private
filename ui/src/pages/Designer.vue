<template>
  <q-layout container view="hHh lpR fFf" style="height: calc(100vh - 130px);">
    <q-header class="bg-white text-black">
      <q-toolbar
        dense
        class="text-dark"
        size="sm"
        style="padding-left: 10px; border-bottom: 2px dashed grey;"
        v-if="showtoolbar"
      >
        <q-btn-toggle
          name="mode"
          size="md"
          dense
          value="pan"
          v-model="mode"
          @input="setMode"
          style="min-height: 45px;"
          toggle-color="primary"
          :options="[
            { icon: 'fas fa-arrows-alt', value: 'pan', slot: 'pan' },
            { icon: 'far fa-object-group', value: 'select', slot: 'select' },
          ]"
        >
          <template v-slot:pan>
            <q-tooltip
              content-class
              content-style="font-size: 16px"
              :offset="[10, 10]"
            >
              Pan Mode
            </q-tooltip>
          </template>
          <template v-slot:select>
            <q-tooltip
              content-class
              content-style="font-size: 16px"
              :offset="[10, 10]"
            >
              Select Mode
            </q-tooltip>
          </template>
        </q-btn-toggle>
        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          icon="fa fa-stop"
          class="q-mr-xs"
          @click="nodeStatus('stopped')"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Stop Nodes
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          icon="fa fa-play"
          class="q-mr-xs"
          @click="nodeStatus('running')"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Start Nodes
          </q-tooltip>
        </q-btn>

        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          icon="fas fa-minus-circle"
          @click="clear = true"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Clear Nodes
          </q-tooltip>
        </q-btn>
        <q-separator vertical inset/>
        <q-btn
          flat
          style="min-height: 45px;"
          size="md"
          icon="far fa-play-circle"
          class="q-mr-xs"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Run Flow
          </q-tooltip>
        </q-btn>

        <q-separator vertical inset/>
        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          icon="far fa-copy"
          @click="copyNodes"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Copy
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          icon="fas fa-paste"
          @click="pasteNodes"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Paste
          </q-tooltip>
        </q-btn>

        <q-btn
          flat
          style="min-height: 45px;"
          @click="undo"
          size="sm"
          icon="fa fa-undo"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Undo
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          style="min-height: 45px;"
          @click="redo"
          size="sm"
          icon="fa fa-redo"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Redo
          </q-tooltip>
        </q-btn>

        <q-separator vertical inset/>
        <q-btn
          flat
          style="min-height: 45px;"
          @click="showCode"
          size="sm"
          icon="fas fa-code"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            View Code
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          icon="fas fa-save"
          @click="saveFlow"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px;"
            :offset="[10, 10]"
          >
            Save Flow
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          style="min-height: 45px; font-size: 0.8em;"
          size="sm"
          :icon="this.saveAsIcon"
          @click="saveToFolder"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px;"
            :offset="[10, 10]"
          >
            Save to Current Folder
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          icon="fas fa-upload"
          :disabled="connected"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px;"
            :offset="[10, 10]"
          >
            Publish
          </q-tooltip>
        </q-btn>
        <q-separator vertical inset/>
        <q-btn
          flat
          style="min-height: 45px;"
          @click="redraw"
          size="sm"
          icon="fas fa-retweet"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Redraw
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          style="min-height: 45px;"
          @click="redraw"
          size="sm"
          icon="fas fa-refresh"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Resync
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          style="min-height: 45px;"
          @click="bandwidthToggle"
          size="sm"
          icon="fas fa-tachometer-alt"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Toggle Bandwidth Display
          </q-tooltip>
        </q-btn>

        <q-separator vertical inset/>
        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          @click="confirmDeleteNodes()"
          icon="fas fa-trash-alt"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Delete Nodes
          </q-tooltip>
        </q-btn>
        <q-separator vertical inset v-if="flowid !== 1"/>
        <q-btn
          flat
          style="min-height: 45px;"
          size="sm"
          icon="fas fa-close"
          @click="showconfirmclose = true"
          v-if="flowid !== 1"
        >
          <q-tooltip
            content-class
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Close Flow
          </q-tooltip>
        </q-btn>

        <q-space />

        <div
          key="div"
          style="
            font-size: 2em;
            font-family: 'Indie Flower', cursive;
            margin-top: 5px;
            margin-right: 1em;
          "
        >
          <q-popup-edit v-model="fname" key="popup">
            <q-input
              key="input"
              type="string"
              v-model="fname"
              dense
              autofocus
              style="
                font-size: 2em;
                font-family: 'Indie Flower', cursive;
                margin-top: 5px;
              "
            />
          </q-popup-edit>
          <transition
            appear
            enter-active-class="animated bounceInDown"
            leave-active-class="animated fadeOut"
            v-if="showName"
          >
            <q-item-label>{{ fname }}</q-item-label>
          </transition>
        </div>
        <q-btn
          flat
          dense
          size="md"
          color="primary"
          icon="menu"
          aria-label="Menu"
          style="z-index: 9999;"
          @click="drawer = !drawer"
        />
        <div class="cursor-pointer">
          <span
            class="text-h5 text-weight-bold"
            style="font-family: 'Indie Flower', cursive; margin-top: 5px;"
          ></span>
        </div>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="drawer"
      side="right"
      bordered
      :width="500"
      style="overflow: hidden;"
    >
      <div>
        <q-tabs
          v-model="tab"
          dense
          class="bg-primary"
          align="left"
          narrow-indicator
          active-color="dark"
          indicator-color="primary"
          active-bg-color="accent"
        >
          <q-tab name="flows" class="text-dark" label="Flows" />
          <q-tab name="patterns" class="text-dark" label="Patterns" />
          <q-tab name="processors" class="text-dark" label="Processors" />
          <q-tab name="network" class="text-dark" label="Network" />
        </q-tabs>

        <q-tab-panels v-model="tab" keep-alive>
          <q-tab-panel
            name="processors"
            ref="processors"
            style="padding: 0px; width: 100%; padding-top: 0px;"
          >
            <Processors
              :objecttype="'processor'"
              :icon="'fas fa-wrench'"
              :collection="'processors'"
              style="width: 100%;"
          /></q-tab-panel>
          <q-tab-panel
            name="patterns"
            ref="patterns"
            style="padding: 0px; width: 100%; padding-top: 0px;"
            ><Patterns
          /></q-tab-panel>
          <q-tab-panel
            name="flows"
            ref="flows"
            style="padding: 0px; width: 100%; padding-top: 0px;"
          >
            <Flows
              :objecttype="'flow'"
              :icon="'fas fa-wrench'"
              :collection="'flows'"
              style="width: 100%;"
              ref="_flows"
              :flowid="flowid"
            />
          </q-tab-panel>
          <q-tab-panel name="network" ref="network" style="padding: 0px;">
            <Networks />
          </q-tab-panel>
        </q-tab-panels>
      </div>

      <q-card
        class=" "
        v-if="showCard"
        style="
          background-color: white;
          width: 450px;
          height: 500px;
          position: absolute;
          left: -465px;
          top: 5px;
        "
      >
        <q-toolbar class="bg-accent" style="padding: 0px; padding-left: 10px;">
          <q-item-label
            style="
              font-size: 1.5em;
              font-family: 'Indie Flower', cursive;
              margin-top: 5px;
              margin-right: 1em;
            "
          >
            {{ card.label }}
          </q-item-label>
          <q-space />
          <q-btn
            flat
            dense
            size="sm"
            icon="close"
            style="padding-right: 10px;"
            color="primary"
            @click="showCard = false"
          ></q-btn>
        </q-toolbar>

        <div
          style="
            padding-left: 10px;
            position: absolute;
            bottom: -20px;
            height: 20px;
            left: 0px;
            width: 100%;
          "
          class="bg-primary text-accent"
        >
          {{ card.id }}
        </div>
      </q-card>
    </q-drawer>
    <q-page-container style="overflow: hidden;">
      <div class="full-height" style="overflow: hidden;">
        <jsplumb-toolkit
          ref="toolkitComponent"
          auto-save="true"
          v-bind:render-params="renderParams"
          v-bind:view="view"
          id="toolkit"
          :surface-id="surfaceId"
          v-bind:toolkit-params="toolkitParams"
          style="height: 100vh; width: 100%;"
        ></jsplumb-toolkit>
        <q-inner-loading :showing="loading" style="z-index: 9999;">
          <q-spinner-gears size="50px" color="primary" />
        </q-inner-loading>
        <q-menu context-menu>
          <q-list dense>
            <q-item clickable v-close-popup @click="redraw">
              <q-item-section side>
                <q-icon name="fas fa-refresh"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Refresh
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="viewConfigureDialog = true">
              <q-item-section side>
                <q-icon name="fas fa-cog"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Configure
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="versionsDialog = true">
              <q-item-section side>
                <q-icon name="far fa-clone"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Versions
              </q-item-section>
            </q-item>

            <q-item clickable v-close-popup @click="showHistory">
              <q-item-section side>
                <q-icon name="fas fa-history"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                History
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="viewVariablesDialog = true">
              <q-item-section side>
                <q-icon name="fas fa-font"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Variables
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup @click="nodeStatus('running')">
              <q-item-section side>
                <q-icon name="fas fa-play"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Start
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="nodeStatus('stopped')">
              <q-item-section side>
                <q-icon name="fas fa-stop"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Stop
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup disabled>
              <q-item-section side>
                <q-icon name="fas fa-bolt"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Enable
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup disabled>
              <q-item-section side>
                <q-icon name="fas fa-times-circle"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Disable
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup @click="pasteNodes">
              <q-item-section side>
                <q-icon name="fas fa-paste"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Paste
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup @click="downloadFlow">
              <q-item-section side>
                <q-icon name="fas fa-download"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Download Flow
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup disabled>
              <q-item-section side>
                <q-icon name="fas fa-upload"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Upload Flow
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup @click="emptyQueuesDialog = true">
              <q-item-section side>
                <q-icon name="fas fa-minus-circle"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Empty All Queues
              </q-item-section>
            </q-item>
          </q-list>
        </q-menu>
        <q-item-label
          v-if="toolbar === false"
          class="text-h5 text-weight-bold text-black"
          style="
            font-family: 'Indie Flower', cursive;
            position: absolute;
            right: 10px;
            top: 10px;
          "
        >
          {{ filename }}
        </q-item-label>
      </div>
    </q-page-container>

    <q-footer></q-footer>
    <q-item-label
      class="text-secondary"
      style="position: absolute; top: 65px; right: 150px;"
    >
      x,y: {{ position[0] }},{{ position[1] }}</q-item-label
    >
    <q-item-label
      class="text-secondary"
      style="position: absolute; top: 60px; right: 40px;"
    >
      Zoom: {{ zoom }}</q-item-label
    >
    <div
      elevated
      class="q-pa-md"
      v-if="navigate"
      style="max-width: 350px; position: absolute; left: 0px; top: 50px;"
    >
      <q-expansion-item
        default-opened
        style="
          box-shadow: 0 0 5px 0px lightgrey;
          border: 1px solid #abbcc3;
          background-color: white;
          font-size: 14px;
          min-width: 300px;
        "
        class="text-dark"
        dense
        expand-icon="far fa-plus-square text-blue-grey-5"
        expanded-icon="far fa-minus-square text-blue-grey-5"
        icon="far fa-compass"
        label="Navigate"
        id="navigator"
      >
        <q-card style="padding: 0px;">
          <q-card-section>
            <q-toolbar>
              <q-btn
                dense
                flat
                size="sm"
                icon="fas fa-crosshairs"
                class="text-dark"
                @click="panToZero"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                ><q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                >
                  Pan to 0,0
                </q-tooltip></q-btn
              >
              <q-btn
                dense
                flat
                size="sm"
                icon="fas fa-home"
                class="text-dark"
                @click="zoomToOne"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                ><q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                >
                  Zoom Level 1.0
                </q-tooltip></q-btn
              >
              <q-btn
                dense
                flat
                size="sm"
                icon="fas fa-search-plus"
                class="text-dark"
                @click="zoomIn"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                ><q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                >
                  Zoom In
                </q-tooltip></q-btn
              >
              <q-btn
                dense
                flat
                size="sm"
                icon="fas fa-search-minus"
                class="text-dark"
                @click="zoomOut"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                ><q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                >
                  Zoom Out
                </q-tooltip></q-btn
              >
              <q-separator style="margin-right: 8px;" />
              <q-btn
                dense
                flat
                size="sm"
                icon="fas fa-expand"
                class="text-dark"
                @click="zoomToSelection"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                ><q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                >
                  Zoom to Selection
                </q-tooltip></q-btn
              >
              <q-btn
                dense
                flat
                size="sm"
                icon="fas fa-expand-arrows-alt"
                class="text-dark"
                @click="zoomToFit"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                ><q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                >
                  Zoom to Fit
                </q-tooltip></q-btn
              >
            </q-toolbar>
            <jsplumb-miniview
              style="width: 100%; height: 200px;"
              :surface-id="surfaceId"
            ></jsplumb-miniview>
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-expansion-item
        default-opened
        style="
          margin-top: 5px;
          box-shadow: 0 0 5px 0px lightgrey;
          border: 1px solid #abbcc3;
          background-color: white;
          font-size: 14px;
          min-width: 300px;
        "
        class="text-dark"
        dense
        expand-icon="far fa-plus-square text-blue-grey-5"
        expanded-icon="far fa-minus-square text-blue-grey-5"
        icon="far fa-hand-pointer"
        label="Selection"
      >
        <q-card style="padding: 0px;">
          <q-card-section>
            <div
              style="
                font-size: 16px;
                padding: 0px;
                position: absolute;
                top: 0px;
                left: 45px;
              "
            >
              <q-popup-edit
                v-model="node.data.name"
                v-if="node !== null"
                title="Name"
                buttons
              >
                <q-input
                  type="string"
                  v-model="node.data.name"
                  dense
                  autofocus
                />
              </q-popup-edit>
              {{ node !== null ? node.data.name : 'No Selection' }}
            </div>
            <div
              class="text-info"
              style="
                font-size: 12px;
                padding: 0px;
                position: absolute;
                top: 20px;
                left: 45px;
              "
            >
              <q-popup-edit
                v-model="node.data.description"
                v-if="node !== null"
                title="Description"
                buttons
              >
                <q-input
                  type="string"
                  v-model="node.data.description"
                  dense
                  autofocus
                />
              </q-popup-edit>
              {{ node !== null ? node.data.description : '' }}
            </div>
            <div
              class="text-primary"
              style="
                font-size: 12px;
                padding: 0px;
                position: absolute;
                top: 40px;
                left: 45px;
              "
            >
              {{ node !== null ? node.id : '' }}
            </div>

            <img src="~assets/images/droplet.svg" style="width: 30px;" />
          </q-card-section>
          <q-card-section>
            <q-toolbar
              style="min-height: 20px; margin-top: 5px; margin-bottom: 0px;"
            >
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="fas fa-cog"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                @click="notifyNode(node.data.id,'configure')"
                ><q-tooltip>Configure</q-tooltip></q-btn
              >
              <q-separator style="margin-right: 8px;" />
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="fas fa-book"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                @click="notifyNode(node.data.id,'savetolibrary')"
                ><q-tooltip>Save to Library</q-tooltip></q-btn
              >
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="far fa-times-circle"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
              ></q-btn>
              <q-separator style="margin-right: 8px;" />
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="fas fa-play"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                @click="notifyNode(node.data.id,'start')"
                ><q-tooltip>Run Processor</q-tooltip></q-btn
              >
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="fas fa-stop"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                @click="notifyNode(node.data.id,'stop')"
                ><q-tooltip>Stop Processor</q-tooltip></q-btn
              >
              <q-separator style="margin-right: 8px;" />
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="fas fa-save"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                @click="notifyNode(node.data.id,'save')"
                ><q-tooltip>Save Processor</q-tooltip></q-btn
              >
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="fas fa-upload"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                ><q-tooltip>Publish Processor</q-tooltip></q-btn
              >
            </q-toolbar>
            <q-toolbar style="margin-top: 0px; min-height: 20px;">
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="fas fa-copy"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                @click="copyNodes"
                ><q-tooltip>Copy Processor</q-tooltip></q-btn
              >
              <q-separator style="margin-right: 8px;" />

              <q-separator />
              <q-separator style="margin-right: 8px;" />
              <q-btn
                dense
                flat
                size="sm"
                :disable="node === null"
                icon="far fa-object-group"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                @click="notifyNode(node.data.id,'corner')"
              ></q-btn>
              <q-btn
                dense
                flat
                :disable="node === null"
                size="sm"
                icon="fas fa-paint-brush"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
              ></q-btn>
              <q-separator style="margin-right: 8px;" />
              <q-btn
                dense
                flat
                :disable="node === null"
                size="sm"
                label="Delete"
                icon="far fa-trash-alt"
                class="text-dark"
                style="margin: 3px; padding: 2px; border: 1px solid #abbcc3;"
                @click="notifyNode(node.data.id,'delete')"
                ><q-tooltip>Delete Processor</q-tooltip></q-btn
              >
            </q-toolbar>
          </q-card-section>
        </q-card>
      </q-expansion-item>
      <q-expansion-item
        default-closed
        style="
          margin-top: 5px;
          box-shadow: 0 0 5px 0px lightgrey;
          border: 1px solid #abbcc3;
          background-color: white;
          font-size: 14px;
          min-width: 300px;
        "
        class="text-dark"
        dense
        expand-icon="far fa-plus-square text-blue-grey-5"
        expanded-icon="far fa-minus-square text-blue-grey-5"
        icon="mail_outline"
        label="Messages"
      >
        <q-card style="padding: 5px; height: 400px;">
          <q-scroll-area style="height: 395px; width: 100%;">
            <span id="logspan" v-for="msg in messages">
              {{msg}}<br>
            </span>
          </q-scroll-area>
        </q-card>
      </q-expansion-item>
    </div>

    <q-dialog v-model="showconfirmclose" persistent>
      <q-card style="padding: 10px; padding-top: 30px;">
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
              <q-item-label>Close Flow</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-close" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Are you sure you want to close this flow?
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
            label="Close"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="closeFlow()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="clear" persistent>
      <q-card style="padding: 10px; padding-top: 30px;">
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
              <q-item-label>Clear Nodes</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-trash" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Are you sure you want to clear all the nodes?
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
            label="Clear"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="clearNodes()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="deleteConfirm" persistent>
      <q-card style="padding: 10px; padding-top: 30px;">
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
              <q-item-label>Delete Nodes</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-trash" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm" v-if="deleteCount > 0">
            Are you sure you want to delete {{ deleteCount }} {{ deleteText }}?
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
            @click="deleteSelectedNodes()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="code"
      transition-show="none"
      persistent
      style="height: 60vh;"
    >
      <q-card style="max-width: 100vw; width: 1500px;">
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
              <q-item-label>Flow Source</q-item-label>
              <q-space />
              <q-icon
                class="text-primary"
                name="fas fa-close"
                @click="code = false"
                style="z-index: 10; cursor: pointer;"
              />
            </q-toolbar>
          </div>
        </q-card-section>

        <q-card-section
          class="row items-center"
          style="
            padding-top: 45px;
            padding-bottom: 20px;
            padding-left: 0px;
            padding-right: 0px;
          "
        >
          <editor
            v-model="thecode"
            id="editor"
            @init="editorInit"
            style="font-size: 25px; height: 60vh;"
            lang="javascript"
            theme="chrome"
            ref="myEditor"
            width="100%"
            height="60vh"
          ></editor>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
            flat
            label="Update"
            class="bg-accent text-dark"
            color="primary"
            v-close-popup
          />
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Close"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="selectAlert" persistent>
      <q-card style="padding: 10px; padding-top: 30px;">
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
              <q-item-label>Delete Nodes</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-trash" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Please select at least one node to delete
          </span>
        </q-card-section>

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
    <q-dialog v-model="versionsDialog" transition-show="none" persistent>
      <q-card
        style="
          width: 70vw;
          max-width: 70vw;
          height: 80vh;
          padding: 10px;
          padding-left: 30px;
          padding-top: 40px;
        "
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
              <q-item-label>Versions</q-item-label>
              <q-space />
              <q-btn
                class="text-primary"
                flat
                dense
                round
                size="sm"
                icon="fas fa-close"
                @click="versionsDialog = false"
                style="z-index: 10;"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-splitter
          v-model="versionSplitter"
          separator-style="background-color: #e3e8ec;height:5px"
          horizontal
          style="height: calc(100% - 40px);"
        >
          <template v-slot:before>
            <q-table
              dense
              :columns="versioncolumns"
              :data="versiondata"
              row-key="name"
              flat
              :pagination="versionPagination"
              style="
                height: calc(100% - 0px);
                width: 100%;
                border-top-radius: 0px;
                border-bottom-radius: 0px;
              "
            >
              <template v-slot:body="props">
                <q-tr :props="props" :key="getUuid">
                  <q-td :key="props.cols[0].name" :props="props">
                    <a
                      class="text-secondary"
                      @click="previewFlow(props.row.version)"
                      >{{ props.cols[0].value }}</a
                    >
                  </q-td>
                  <q-td :key="props.cols[1].name" :props="props">
                    {{ props.cols[1].value }}
                  </q-td>
                  <q-td :key="props.cols[2].name" :props="props">
                    {{ props.cols[2].value }}
                  </q-td>
                  <q-td :key="props.cols[3].name" :props="props">
                    {{ props.cols[3].value }}
                  </q-td>
                  <q-td :key="props.cols[4].name" :props="props">
                    {{ props.cols[4].value }}
                  </q-td>
                  <q-td :key="props.cols[5].name" :props="props">
                    {{ props.cols[5].value }}
                  </q-td>
                </q-tr>
              </template>
            </q-table>
          </template>
          <template v-slot:after
            ><div style="height: 100%; width: 100%;">
              <Designer
                :ref="'previewdesigner'"
                :flowcode="''"
                :flowname="''"
                :flowuuid="''"
                :flowid="''"
                :surfaceId="''"
                navigate="false"
                :showtoolbar="false"
              /></div
          ></template>
        </q-splitter>
        <q-card-actions align="left">
          <!--
          <q-btn
            style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
            flat
            icon="refresh"
            class="bg-secondary text-dark"
            color="primary"
            @click="refreshVersions"
          />-->
        </q-card-actions>
        <q-card-actions align="right"
          ><q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Close"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
          />
        </q-card-actions>

        <q-inner-loading :showing="versionsLoading" style="z-index: 9999;">
          <q-spinner-gears size="50px" color="primary" />
        </q-inner-loading>
      </q-card>
    </q-dialog>

    <q-dialog v-model="viewVariablesDialog" persistent>
      <q-card
        style="padding: 10px; padding-top: 30px; min-width: 40vw; height: 50%;"
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
              <q-item-label>Variables</q-item-label>
              <q-space />
              <q-icon
                class="text-primary"
                name="fas fa-close"
                @click="viewVariablesDialog = false"
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
            :columns="variablecolumns"
            :data="variabledata"
            row-key="name"
            flat
            style="
              width: 100%;
              margin-top: 20px;
              border-top-radius: 0px;
              border-bottom-radius: 0px;
            "
          >
            <template v-slot:body="props">
              <q-tr :props="props" :key="getUuid">
                <q-td :key="props.cols[0].name" :props="props">
                  <a class="text-secondary">{{ props.row.name }}</a>
                  <q-popup-edit v-model="props.row.name" v-slot="scope" buttons>
                    <q-input
                      v-model="props.row.name"
                      dense
                      autofocus
                      counter
                    />
                  </q-popup-edit>
                </q-td>
                <q-td :key="props.cols[1].name" :props="props">
                  <a class="text-secondary">{{ props.row.value }}</a>
                  <q-popup-edit v-model="props.row.value" v-slot="scope" buttons>
                    <q-input
                      v-model="props.row.value"
                      dense
                      autofocus
                      counter
                    />
                  </q-popup-edit>
                </q-td>
                <q-td :key="props.cols[2].name" :props="props">
                  {{ props.cols[2].value }}
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </q-card-section>

        <q-card-actions align="left">
          <q-btn
            flat
            style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
            label="Add"
            class="bg-primary text-secondary"
            color="primary"
            @click="addVariable"
          />
        </q-card-actions>
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
      </q-card>
    </q-dialog>

    <q-dialog v-model="viewConfigureDialog" persistent>
      <q-card
        style="padding: 10px; padding-top: 30px; min-width: 40vw; height: 50%;"
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
              <q-item-label>Configure</q-item-label>
              <q-space />
              <q-icon
                class="text-primary"
                name="fas fa-close"
                @click="viewConfigureDialog = false"
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
            :columns="variablecolumns"
            :data="variabledata"
            row-key="name"
            flat
            style="
              width: 100%;
              margin-top: 20px;
              border-top-radius: 0px;
              border-bottom-radius: 0px;
            "
          >
            <template v-slot:body="props">
              <q-tr :props="props" :key="getUuid">
                <q-td :key="props.cols[0].name" :props="props">
                  <a class="text-secondary">{{ props.row.name }}</a>
                  <q-popup-edit v-model="props.row.name" v-slot="scope" buttons>
                    <q-input
                      v-model="scope.value"
                      dense
                      autofocus
                      counter
                    />
                  </q-popup-edit>
                </q-td>
                <q-td :key="props.cols[1].name" :props="props">
                  <a class="text-secondary">{{ props.row.value }}</a>
                  <q-popup-edit v-model="props.row.value" v-slot="scope" >
                    <q-input
                      v-model="scope.value"
                      dense
                      autofocus
                      counter
                    />
                  </q-popup-edit>
                </q-td>
                <q-td :key="props.cols[2].name" :props="props">
                  {{ props.cols[2].value }}
                </q-td>
              </q-tr>
            </template>
          </q-table>
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
      </q-card>
    </q-dialog>

    <q-dialog v-model="viewHistoryDialog" persistent>
      <q-card
        style="padding: 10px; padding-top: 30px; min-width: 40vw; height: 50%;"
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
              <q-item-label>History</q-item-label>
              <q-space />
              <q-icon
                class="text-primary"
                name="fas fa-close"
                @click="viewHistoryDialog = false"
                style="z-index: 10; cursor: pointer;"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section
          class="row items-center"
          style="height: calc(100% - 40px); width: 100%;"
        >
          <q-table
            dense
            :columns="historycolumns"
            :data="undoredo.undoStack"
            row-key="name"
            flat
            style="
              width: 100%;
              height: 100%;
              margin-top: 20px;
              border-top-radius: 0px;
              border-bottom-radius: 0px;
            "
          >
            <template v-slot:body="props">
              <q-tr :props="props" :key="getUuid">
                <q-td :key="props.cols[0].name" :props="props">
                  {{ props.row.constructor.name }}
                </q-td>
                <q-td :key="props.cols[1].name" :props="props">
                  {{ props.row.obj.data.name }}
                </q-td>
                <q-td :key="props.cols[2].name" :props="props">
                  {{ props.row.obj.data.id }}
                </q-td>
                <q-td key="owner" >
                  {{owner}}
                </q-td>
              </q-tr>
            </template>
          </q-table>
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
      </q-card>
    </q-dialog>


    <q-dialog v-model="emptyQueuesDialog" persistent>
      <q-card style="padding: 10px; padding-top: 30px;">
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
              <q-item-label>Empty All Queues</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-trash" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Are you sure you want to empty all the queues?
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
            flat
            label="No"
            class="bg-accent text-dark"
            color="primary"
            v-close-popup
          />
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Yes, Empty"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="emptyAllQueues"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>


  </q-layout>
</template>
<style>
.q-icon {
  font-size: 16px;
}
.q-item__section--side > .q-icon {
  font-size: 16px;
  /* font-size: 24px; */
}
.q-item__section--avatar {
  color: inherit;
  min-width: 16px;
}

.scroll {
  overflow: hidden;
}
.q-card__section--vert {
  padding: 5px;
  padding-top: 0px;
}
.absolute-full {
  right: 0px !important;
}

.jtk-surface {
  background-image: url('~assets/images/Graph-paper.svg');
  height: 100vh;
  overflow: hidden;
}

.jtk-bootstrap .jtk-page-container {
  /* display: flex; */
  width: 100vw;
  /* justify-content: center; */
  /* flex: 1; */
}

.delete-relationship:hover {
  z-index: 999999;
}
.jtk-demo-main {
  position: relative;
  margin-top: 0px;
  display: flex;
  height: 100%;
  flex-direction: column;
}

.jtk-bootstrap-wide .jtk-container {
  width: 100vw;
  max-width: 100vw;
}

.jtk-surface-no-grid {
  background-image: none !important;
}
.jtk-miniview {
  overflow: hidden !important;
  width: 125px;
  height: 125px;
  position: relative;
  background-color: transparent;
  border: 2px solid #6b8791;
  border-radius: 4px;
  opacity: 0.5;
}
.jtk-demo-canvas {
  height: calc(100vh - 160px);
  max-height: 100vh;
  border: 1px solid #ccc;
  background-color: white;
  display: flex;
  flex-grow: 1;
  position: relative;
}

.q-drawer__content {
  overflow: hidden !important;
}

.jtk-overlay {
  z-index: -10 !important;
}
.common-edge {
  z-index: -10;
}
.jtk-miniview-collapse {
  font-size: 0px;
}

.delete-relationship {
  border-radius: 0px !important;
  padding: 5px;
  z-index: 0;
  cursor: pointer;
  z-index: 9;
  background-color: #1976d2;
  font-size: 14px;
  border: 1px solid black;
  text-align: center;
  width: 100px;
}
.hide {
  display: none;
}
@import url('https://fonts.googleapis.com/css?family=Indie+Flower&display=swap');

.q-btn.disabled {
  color: #a9adb1 !important;
}
</style>
<script>
import {
  jsPlumb,
  Dialogs,
  DrawingTools,
  jsTarget,
  jsPlumbUtil,
} from 'jsplumbtoolkit';
import Vue from 'vue';

import { jsPlumbToolkitVue2 } from 'jsplumbtoolkit-vue2';
import { jsPlumbSyntaxHighlighter } from 'jsplumbtoolkit-syntax-highlighter';
import { jsPlumbToolkitUndoRedo } from 'jsplumbtoolkit-undo-redo';
import { SurfaceDrop } from 'jsplumbtoolkit-vue2-drop';
import NoteTemplate from 'components/templates/NoteTemplate.vue';

import Queue from 'components/Queue.vue';

import PipelineTemplate from 'components/templates/PipelineTemplate.vue';
import SegmentTemplate from 'components/templates/SegmentTemplate.vue';
import ChordTemplate from 'components/templates/ChordTemplate.vue';
import DataTemplate from 'components/templates/DataTemplate.vue';
import ScriptTemplate from 'components/templates/ScriptTemplate.vue';
import GroupTemplate from 'components/templates/GroupTemplate.vue';
import PatternTemplate from 'components/templates/PatternTemplate.vue';

import DocumentTemplate from 'components/templates/DocumentTemplate.vue';
import PortInTemplate from 'components/templates/PortInTemplate.vue';
import PortOutTemplate from 'components/templates/PortOutTemplate.vue';
import RouterTemplate from 'src/components/templates/RouterTemplate.vue';
import ParallelTemplate from 'src/components/templates/ParallelTemplate.vue';
import SchemaTemplate from 'src/components/templates/SchemaTemplate.vue';
import Flows from 'components/Flows.vue';
import Processors from 'components/Processors.vue';
import Networks from 'components/Networks.vue';

var dd = require('drip-drop');

var idFunction = function (n) {
  return n.id;
};

// This function is what the toolkit will use to get the associated type from a node.
var typeFunction = function (n) {
  return n.type;
};

var dd = require('drip-drop');

import { v4 as uuidv4 } from 'uuid';

import 'assets/css/jsplumbtoolkit.css';
import 'assets/css/jsplumbtoolkit-editable-connectors.css';
import 'assets/css/jsplumbtoolkit-syntax-highlighter.css';
import 'assets/css/jsplumbtoolkit-defaults.css';

import Styles from 'components/Styles.vue';
import Patterns from 'components/Patterns.vue';
import { mdiContentSaveMove } from '@mdi/js';
import DataService from 'src/components/util/DataService';
import ParallelTemplateVue from 'src/components/templates/ParallelTemplate.vue';
//import 'floating-vue/dist/style.css'

function downloadFile(file) {
  // Create a link and set the URL using `createObjectURL`
  const link = document.createElement('a');
  link.style.display = 'none';
  link.href = URL.createObjectURL(file);
  link.download = file.name;

  // It needs to be added to the DOM so it can be clicked
  document.body.appendChild(link);
  link.click();

  // To make this work on Firefox we need to wait
  // a little while before removing it.
  setTimeout(() => {
    URL.revokeObjectURL(link.href);
    link.parentNode.removeChild(link);
  }, 0);
}

function htmlToElement(html) {
  var template = document.createElement('template');
  html = html.trim(); // Never return a text node of whitespace as the result
  template.innerHTML = html;
  return template.content.firstChild;
}

export default {
  name: 'Designer',
  props: [
    'surfaceId',
    'flowcode',
    'flowid',
    'flowuuid',
    'flow',
    'showtoolbar',
    'flowname',
    'navigate',
  ],
  components: {
    Styles,
    Processors,
    Flows,
    Patterns,
    Queue,
    Networks,
    editor: require('vue2-ace-editor'),
  },
  watch: {
    'undoredo.undoStack': function () {
    },
    versionsDialog: function (value) {
      if (value) {
        console.log('LOAD VERSIONS');
        DataService.getVersions(this.flowuuid)
          .then((versions) => {
            this.versiondata = versions.data;
            this.versionsLoading = false;
          })
          .catch((error) => {
            this.versionsLoading = false;
          });
      }
    },
  },
  computed: {
    connected() {
      return this.$store.state.designer.connected;
    },
    htmlDataComponent() {
      return {
        template:
          "<div style='box-shadow: 0 0 5px grey;background-color:rgb(244, 246, 247); z-index:999999; width: 200px; height:40px; padding: 3px; font-size: 12px'> Name " +
          "<span style='font-weight: bold; color: #775351' data-source=''>Queue</span><i class='pull-right fas fa-cog text-primary'/>" +
          '<div style=\'color:black;font-weight:normal;font-family: "Roboto", "-apple-system", "Helvetica Neue", Helvetica, Arial, sans-serif;background-color: white; border-top: 1px solid #abbcc3; width:200px;height:20px; position:absolute; top:20px; left:0px; padding: 1px; padding-left: 3px;font-size: 12px;padding-top:3px\'> Queued ' +
          "<span style='font-weight: bold; color: #775351'>0 (0 bytes)</span>" +
          '</div>' +
          '</div>',

        data() {
          return {
            name: 'component',
            value: '',
          };
        },
        created() {
          // value of "this" is formComponent
          console.log(this.name + ' created');
        },
        methods: {
          // proxy components method to parent method,
          // actually you done have to
          onInputProxy: this.onInput,
        },
      };
    },
    fname: {
      get() {
        return this.flowname;
      },
      set(name) {
        this.$emit('update-name', name);
      },
    },
  },
  methods: {
    notifyNode(id) {
      console.log("Notifying",id)
      this.$root.$emit(id,'configure')
    },
    addVariable() {
      this.variabledata.push({
        'name': 'NAME',
        'value': 'VALUE',
        'scope':'FLOW'
      })
    },
    emptyAllQueues() {

    },
    showHistory () {
      this.viewHistoryDialog = true;
    },
    downloadFlow() {
      var thecode = JSON.stringify(
        window.toolkit.getGraph().serialize(),
        null,
        '\t'
      );

      // TODO: Insert variables and config

      // Dynamically create a File
      const myFile = new File([thecode], this.flowname + '.json');

      // Download it using our function
      downloadFile(myFile);
    },
    previewFlow(version) {
      console.log('preview', version, this.versiondata);
      this.versiondata.forEach((row) => {
        console.log('row', row);
        if (row.version === version) {
          console.log('PREVIEW', row.code);
          this.$refs.previewdesigner.toolkit.clear();
          this.$refs.previewdesigner.toolkit.load({
            type: 'json',
            data: JSON.parse(row.code),
          });
        }
      });
    },
    nodeStatus(status) {
      this.showBandwidth = !this.showBandwidth;
      var selection = window.toolkit.getSelection();
      var nodes = selection.getAll();

      if (nodes.length > 0) {
        nodes.forEach((node) => {
          setTimeout(() => {
            if (node.component && node.component.setBandwidth) {
              node.component.obj.status = status;
            }
          });
        });
      } else {
        window.toolkit.getNodes().forEach((node) => {
          setTimeout(() => {
            if (node.component && node.component.setBandwidth) {
              node.component.obj.status = status;
            }
          });
        });
      }
    },
    bandwidthToggle() {
      this.showBandwidth = !this.showBandwidth;
      var selection = window.toolkit.getSelection();
      var nodes = selection.getAll();

      if (nodes.length > 0) {
        nodes.forEach((node) => {
          setTimeout(() => {
            if (node.component && node.component.setBandwidth) {
              node.component.setBandwidth(this.showBandwidth);
            }
          });
        });
      } else {
        window.toolkit.getNodes().forEach((node) => {
          setTimeout(() => {
            if (node.component && node.component.setBandwidth) {
              node.component.setBandwidth(this.showBandwidth);
            }
          });
        });
      }
      this.$emit('toggle.bandwith', this.showBandwidth);
    },
    redraw() {
      window.toolkit.surface.refresh();
      //this.$store.commit('designer/setMessage', 'Canvas refreshed!');
      this.$q.notify({
            color: 'secondary',
            timeout: 2000,
            position: 'top',
            message: 'Canvas refreshed',
            icon: 'fas fa-refresh',
          });
    },
    resetView() {
      window.toolkit.surface.setZoom(1.0);
      window.toolkit.surface.setPan(0, 0, true);
    },
    zoomToOne() {
      window.toolkit.surface.setZoom(1.0);
    },
    panToZero() {
      window.toolkit.surface.setPan(0, 0, true);
    },
    refresh() {
      console.log('Synchronizing flows');
      this.$refs['_flows'].synchronize();
    },
    editorInit: function () {
      var me = this;

      require('brace/ext/language_tools'); // language extension prerequsite...
      require('brace/mode/html');
      require('brace/mode/python'); // language
      require('brace/mode/less');
      require('brace/theme/chrome');
      require('brace/snippets/javascript'); // snippet
      console.log('editorInit');
      const editor = this.$refs.myEditor.editor;
      editor.setAutoScrollEditorIntoView(true);
    },
    saveToFolder() {
      var thecode = JSON.stringify(
        window.toolkit.getGraph().serialize(),
        null,
        '\t'
      );

      // TODO: Insert variables and config

      this.$root.$emit(
        'save.flow.to.folder.' + this.flowid,
        this.flowname,
        this.flowuuid,
        this.flowid,
        thecode
      );
    },
    saveFlow() {
      var thecode = JSON.stringify(
        window.toolkit.getGraph().serialize(),
        null,
        '\t'
      );
      this.$root.$emit(
        'save.flow.' + this.flowid,
        this.flowname,
        this.flowuuid,
        this.flowid,
        thecode
      );
    },
    showCode() {
      this.code = true;
      this.thecode = JSON.stringify(
        window.toolkit.getGraph().serialize(),
        null,
        '\t'
      );
      console.log('NODE', window.toolkit.getNodes());
    },
    copyNodes() {
      function findMatch(list, obj) {
        for (var i = 0; i < list.length; i++) {
          var o = list[i];
          if (o.id === obj.id) {
            return true;
          }
        }
        return false;
      }
      function findEdge(list, edge) {
        for (var i = 0; i < list.length; i++) {
          var e = list[i];
          if (e.source === edge.source || e.target === edge.target) {
            return true;
          }
        }
        return false;
      }
      function haveAllNodes(nodes, edge) {
        var source = false;
        var target = false;
        for (var i = 0; i < nodes.length; i++) {
          var node = nodes[i];
          if (edge.source.split('.')[0] === node.id) source = true;
          if (edge.target.split('.')[0] === node.id) target = true;
        }
        return source && target;
      }

      var selection = window.toolkit.getSelection();
      var nodes = selection.getAll();
      console.log('COPY SELECTED NODES:', nodes);
      var exportData = window.toolkit.exportData();
      var data = JSON.parse(JSON.stringify(exportData, undefined, '\t'));
      var jsonData = {};
      jsonData.nodes = [];
      jsonData.edges = [];
      jsonData.ports = [];
      for (var i = 0; i < data.nodes.length; i++) {
        const n = data.nodes[i];
        if (findMatch(nodes, n)) {
          jsonData.nodes.push(n);
        }
      }
      for (var i = 0; i < data.edges.length; i++) {
        const e = data.edges[i];
        if (haveAllNodes(jsonData.nodes, e)) {
          jsonData.edges.push(e);
        }
      }
      for (var i = 0; i < jsonData.nodes.length; i++) {
        const node = jsonData.nodes[i];
        for (var p = 0; p < data.ports.length; p++) {
          var port = data.ports[p];
          if (port.id.indexOf(node.id) > -1) {
            jsonData.ports.push(port);
          }
        }
      }

      window.clipboard = jsonData;
      var nodes = [];
      for (var i = 0; i < window.clipboard.nodes.length; i++) {
        nodes.push(window.toolkit.getNode(window.clipboard.nodes[i].id));
      }
      window.nodes = nodes;
      console.log('jsonData:', jsonData);
    },
    pasteNodes() {
      console.log('pasteNodes: ', window.clipboard);

      var data = [];

      window.toolkit.load({
        type: 'json',
        data: window.clipboard,
        onload: function () {
          window.toolkit.setSelection(window.nodes);
          window.toolkit.surface.zoomToSelection({ doNotZoomIfVisible: true });
        },
      });

      this.$root.$emit('status.message', {
        color: 'black',
        message: 'Pasted ' + nodes.length + ' nodes!',
      });
      //window.setDirty(true)
    },
    closeFlow() {
      this.$root.$emit('close.flow', this.flowid);
    },
    confirmDeleteNodes() {
      var selection = window.toolkit.getSelection();
      console.log('DELETE NODES', selection.getAll());

      selection.getAll().forEach((node) => {
        console.log('NODE EL', node.nodeEl);
      });
      this.deleteCount = selection.getAll().length;
      if (this.deleteCount > 1) {
        this.deletText = 'nodes';
        this.deleteConfirm = true;
      } else if (this.deleteCount === 1) {
        this.deleteText = 'node';
        this.deleteConfirm = true;
      } else if (this.deleteCount === 0) {
        this.selectAlert = true;
      }
    },
    deleteSelectedNodes() {
      var selection = window.toolkit.getSelection();
      console.log('SELECTION', selection);
      selection.getAll().map(function (node) {
        console.log('Removing:', node);
        window.toolkit.removeNode(node);
      });
    },
    undo() {
      this.undoredo.undo();
    },
    redo() {
      this.undoredo.redo();
    },
    zoomIn() {
      window.toolkit.surface.nudgeZoom(0.25);
    },
    zoomOut() {
      window.toolkit.surface.nudgeZoom(-0.25);
    },
    zoomToFit() {
      window.toolkit.surface.zoomToFit({ fill: 0.75 });
      this.mode = 'pan';
    },
    zoomToSelection() {
      window.toolkit.surface.animateToSelection({ fill: 0.75 });
      this.mode = 'pan';
    },
    clearNodes() {
      window.toolkit.clear();
      window.toolkit.dirty = true;
    },
    setMode(mode) {
      console.log('setMode:', mode);
      window.toolkit.surface.setMode(mode);
    },
  },
  created() {
    this.saveAsIcon = mdiContentSaveMove;
  },
  mounted() {
    var me = this;
    setTimeout(() => {
      //me.$store.state.designer.message="Connected";
      me.$store.commit('designer/setMessage', 'Connected');
    }, 5000);

    setTimeout(() => {
      me.showName = true;
    }, 1000);

    this.$root.$on('log.message', (message) => {
      me.messages.unshift(message);
    })
    this.toolkitComponent = this.$refs.toolkitComponent;
    this.toolkit = this.toolkitComponent.toolkit;
    console.log('NAVIGATE', this.navigate);
    console.log('FLOW UUID', this.flowuuid);
    console.log('MOUNTED DESIGNER: STORE', this.$store);
    window.store = this.$store;
    jsPlumbToolkit.ready(function () {
      jsPlumbToolkitVue2.getSurface(me.surfaceId, (s) => {
        me.surface = s;
        me.surface.bind('lasso:end', function () {
          me.mode = 'pan';
        });

        console.log('SURFACE EL', me.surface.$el);
        me.surface.setPan(0, 0);
        me.surface.setPan(0, 0);
        console.log('PAN', me.surface.getPan());
        me.surface.setZoom(1.0);
        function getpan() {
          me.position = me.surface.getPan();
          setTimeout(getpan, 1000);
        }
        getpan();
        me.surface.bind('zoom', function () {
          me.zoom = me.surface.getZoom().toFixed(2);
        });
        console.log('SURFACE ', me.surfaceId, s);
        s.bind('lasso:end', function () {
          me.isdisabled = false;
          me.selectedNodes = me.toolkit.getSelection().getAll().length;
        });
        s.bind('canvasClick', function () {
          me.isdisabled = true;
        });
        window.root = me.$root;
        window.toolkit = me.toolkit;
        window.toolkit.surface = me.surface;
        window.designer = me;
        me.$root.$on('flow.uuid', (flowid, flowuuid) => {
          if (flowid === me.flowid) {
            me.flowuuid = flowuuid;
          }
        });

        me.$root.$on('object.card', (card) => {
          me.card = card;
        });
        me.$root.$on('toggle.card', () => {
          me.showCard = !me.showCard;
        });
        me.$root.$on('node.selected', (node) => {
          me.node = node;
          console.log('Animate node');
          var adhocSelection = toolkit.filter(function (obj) {
            return obj === node;
          });
          if (node !== null) {
            //me.surface.setZoom(0.001);
          }
        });
        me.toolkit.uuid = uuidv4();
        console.log('toolkit myUUID: ', me.toolkit.uuid);
        me.toolkit.$root = me.$root;
        me.toolkit.renderer = s;

        if (me.flowcode) {
          me.toolkit.load({
            type: 'json',
            data: me.flowcode,
            onload: function () {
              // called after the data has loaded.
              window.toolkit.surface.setZoom(1.0);
              me.toolkit.surface.zoomToFit({ fill: 0.75 });
              window.designer.$root.$on('toolkit.dirty');
            },
          });
        }

        var els = me.$el.getElementsByClassName('jtk-surface');
        console.log('ELS:', els);
        for (var i = 0; i < els.length; i++) {
          var el = els[i];
          console.log('DD:EL:', el);
          dd.drop(el).on('drop', function (data, event) {
            console.log('drop:canvas', data, event);
            var number = me.surface.mapLocation(event.clientX, event.clientY);
            if (data.object) {
              var node = JSON.parse(data.object);
              console.log('NUMBER:', number);
              node.node.left = number.left - 390 / 2;
              node.node.top = number.top - 135 / 2;
              node.node.x = number.left - 390 / 2;
              node.node.y = number.top - 135 / 2;
              console.log('DROP NODE:', node);

              window.toolkit.$root.$emit('node.added', { data: node });
              var data = JSON.parse(JSON.stringify(node.node));
              console.log('DROP DATA:', data);
              console.log('SURFACE', me.surface);
              if (data.type === 'pattern') {
                console.log('DROP PATTERN', data.code);
                if (data.code) {
                  me.showing = false;
                  window.toolkit.load({
                    type: 'json',
                    data: JSON.parse(data.code),
                    onload: function () {
                      console.log(
                        'FINISHED LOADING PATTERN',
                        JSON.parse(data.code)
                      );
                    },
                  });
                } else {
                  DataService.getPattern(data.patternid)
                    .then((pattern) => {
                      me.showing = false;
                      console.log('LOADED PATTERN', pattern);
                      window.toolkit.load({
                        type: 'json',
                        data: pattern.data,
                        onload: function () {
                          console.log('DONE LOADING');
                          setTimeout(() => {
                            //window.toolkit.zoomToOne();
                            //window.toolkit.zoomToFit();
                          }, 500);
                        },
                      });
                    })
                    .catch((error) => {
                      me.$q.notify({
                        color: 'negative',
                        timeout: 2000,
                        position: 'top',
                        message: 'An error occurred loading the pattern!',
                        icon: 'error',
                      });
                    });
                }
                return;
              }
              if (data.group) {
                delete data.group;
                data.id = uuidv4();
                window.toolkit.addFactoryGroup(data.type, data);
              } else {
                window.toolkit.addNode(node.node, data);
              }

              node.toolkit = window.toolkit;
              console.log('NODES', me.surface.getNodes());
            }
          });
          dd.drop(el).on('enter', function (keys, event) {
            console.log('drop enter:canvas', keys, event);
          });
          dd.drop(el).on('leave', function (keys, event) {
            console.log('drop leave:canvas', keys, event);
          });
        }
        new DrawingTools({
          renderer: s,
        });
        me.undoredo = new jsPlumbToolkitUndoRedo({
          surface: s,
          onChange: function (undo, undoSize, redoSize) {
            // controls.setAttribute("can-undo", undoSize > 0);
            // controls.setAttribute("can-redo", redoSize > 0);
          },
          compound: true,
        });
        me.toolkit.undoredo = me.undoredo;
      });
    });
  },
  data: () => {
    return {
      owner:'darren',
      messages:[],
      undoredo: {},
      variabledata: [
      ],
      historycolumns: [
        {
          name: 'action',
          label: 'Action',
          field: 'name',
          align: 'left',
        },
        {
          name: 'object',
          label: 'Object',
          field: 'object',
          align: 'left',
        },
        {
          name: 'id',
          label: 'Object ID',
          field: 'id',
          align: 'left',
        },
        {
          name: 'owner',
          label: 'Owner',
          align: 'left',
        }
      ],
      variablecolumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left',
        },
        {
          name: 'value',
          label: 'Value',
          field: 'value',
          align: 'left',
        },
        {
          name: 'scope',
          label: 'Scope',
          field: 'scope',
          align: 'left',
        },
      ],
      viewVariablesDialog: false,
      viewConfigureDialog: false,
      emptyQueuesDialog: false,
      versiondata: [],
      versionsLoading: true,
      flow: {
        id: '',
        code: '',
        filename: '',
        _id: '',
      },
      navigate: true,
      versioncolumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left',
        },
        {
          name: 'type',
          label: 'Type',
          field: 'type',
          align: 'left',
        },
        {
          name: 'filepath',
          label: 'File Path',
          field: 'filepath',
          align: 'left',
        },
        {
          name: 'collection',
          label: 'Collection',
          field: 'collection',
          align: 'left',
        },
        {
          name: 'version',
          label: 'Version',
          field: 'version',
          align: 'left',
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left',
        },
      ],
      versionSplitter: 50,
      versionPagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 20,
        // rowsNumber: xx if getting data from a server
      },
      versionsDialog: false,
      zoom: 1.0,
      value: true,
      showBandwidth: true,
      showName: false,
      card: {
        name: 'Object Name',
      },
      showCard: false,
      tab: 'flows',
      clear: false,
      position: [-20, -20],
      showconfirmclose: false,
      deleteText: 'nodes',
      deleteCount: 0,
      series2: [
        {
          data: [
            {
              x: new Date(1538778600000),
              y: [6629.81, 6650.5, 6623.04, 6633.33],
            },
            {
              x: new Date(1538780400000),
              y: [6632.01, 6643.59, 6620, 6630.11],
            },
            {
              x: new Date(1538782200000),
              y: [6630.71, 6648.95, 6623.34, 6635.65],
            },
            {
              x: new Date(1538784000000),
              y: [6635.65, 6651, 6629.67, 6638.24],
            },
            {
              x: new Date(1538785800000),
              y: [6638.24, 6640, 6620, 6624.47],
            },
            {
              x: new Date(1538787600000),
              y: [6624.53, 6636.03, 6621.68, 6624.31],
            },
            {
              x: new Date(1538789400000),
              y: [6624.61, 6632.2, 6617, 6626.02],
            },
            {
              x: new Date(1538791200000),
              y: [6627, 6627.62, 6584.22, 6603.02],
            },
            {
              x: new Date(1538793000000),
              y: [6605, 6608.03, 6598.95, 6604.01],
            },
            {
              x: new Date(1538794800000),
              y: [6604.5, 6614.4, 6602.26, 6608.02],
            },
            {
              x: new Date(1538796600000),
              y: [6608.02, 6610.68, 6601.99, 6608.91],
            },
            {
              x: new Date(1538798400000),
              y: [6608.91, 6618.99, 6608.01, 6612],
            },
            {
              x: new Date(1538800200000),
              y: [6612, 6615.13, 6605.09, 6612],
            },
            {
              x: new Date(1538802000000),
              y: [6612, 6624.12, 6608.43, 6622.95],
            },
            {
              x: new Date(1538803800000),
              y: [6623.91, 6623.91, 6615, 6615.67],
            },
            {
              x: new Date(1538805600000),
              y: [6618.69, 6618.74, 6610, 6610.4],
            },
            {
              x: new Date(1538807400000),
              y: [6611, 6622.78, 6610.4, 6614.9],
            },
            {
              x: new Date(1538809200000),
              y: [6614.9, 6626.2, 6613.33, 6623.45],
            },
            {
              x: new Date(1538811000000),
              y: [6623.48, 6627, 6618.38, 6620.35],
            },
            {
              x: new Date(1538812800000),
              y: [6619.43, 6620.35, 6610.05, 6615.53],
            },
            {
              x: new Date(1538814600000),
              y: [6615.53, 6617.93, 6610, 6615.19],
            },
            {
              x: new Date(1538816400000),
              y: [6615.19, 6621.6, 6608.2, 6620],
            },
            {
              x: new Date(1538818200000),
              y: [6619.54, 6625.17, 6614.15, 6620],
            },
            {
              x: new Date(1538820000000),
              y: [6620.33, 6634.15, 6617.24, 6624.61],
            },
            {
              x: new Date(1538821800000),
              y: [6625.95, 6626, 6611.66, 6617.58],
            },
            {
              x: new Date(1538823600000),
              y: [6619, 6625.97, 6595.27, 6598.86],
            },
            {
              x: new Date(1538825400000),
              y: [6598.86, 6598.88, 6570, 6587.16],
            },
            {
              x: new Date(1538827200000),
              y: [6588.86, 6600, 6580, 6593.4],
            },
            {
              x: new Date(1538829000000),
              y: [6593.99, 6598.89, 6585, 6587.81],
            },
            {
              x: new Date(1538830800000),
              y: [6587.81, 6592.73, 6567.14, 6578],
            },
            {
              x: new Date(1538832600000),
              y: [6578.35, 6581.72, 6567.39, 6579],
            },
            {
              x: new Date(1538834400000),
              y: [6579.38, 6580.92, 6566.77, 6575.96],
            },
            {
              x: new Date(1538836200000),
              y: [6575.96, 6589, 6571.77, 6588.92],
            },
            {
              x: new Date(1538838000000),
              y: [6588.92, 6594, 6577.55, 6589.22],
            },
            {
              x: new Date(1538839800000),
              y: [6589.3, 6598.89, 6589.1, 6596.08],
            },
            {
              x: new Date(1538841600000),
              y: [6597.5, 6600, 6588.39, 6596.25],
            },
            {
              x: new Date(1538843400000),
              y: [6598.03, 6600, 6588.73, 6595.97],
            },
            {
              x: new Date(1538845200000),
              y: [6595.97, 6602.01, 6588.17, 6602],
            },
            {
              x: new Date(1538847000000),
              y: [6602, 6607, 6596.51, 6599.95],
            },
            {
              x: new Date(1538848800000),
              y: [6600.63, 6601.21, 6590.39, 6591.02],
            },
            {
              x: new Date(1538850600000),
              y: [6591.02, 6603.08, 6591, 6591],
            },
            {
              x: new Date(1538852400000),
              y: [6591, 6601.32, 6585, 6592],
            },
            {
              x: new Date(1538854200000),
              y: [6593.13, 6596.01, 6590, 6593.34],
            },
            {
              x: new Date(1538856000000),
              y: [6593.34, 6604.76, 6582.63, 6593.86],
            },
            {
              x: new Date(1538857800000),
              y: [6593.86, 6604.28, 6586.57, 6600.01],
            },
            {
              x: new Date(1538859600000),
              y: [6601.81, 6603.21, 6592.78, 6596.25],
            },
            {
              x: new Date(1538861400000),
              y: [6596.25, 6604.2, 6590, 6602.99],
            },
            {
              x: new Date(1538863200000),
              y: [6602.99, 6606, 6584.99, 6587.81],
            },
            {
              x: new Date(1538865000000),
              y: [6587.81, 6595, 6583.27, 6591.96],
            },
            {
              x: new Date(1538866800000),
              y: [6591.97, 6596.07, 6585, 6588.39],
            },
            {
              x: new Date(1538868600000),
              y: [6587.6, 6598.21, 6587.6, 6594.27],
            },
            {
              x: new Date(1538870400000),
              y: [6596.44, 6601, 6590, 6596.55],
            },
            {
              x: new Date(1538872200000),
              y: [6598.91, 6605, 6596.61, 6600.02],
            },
            {
              x: new Date(1538874000000),
              y: [6600.55, 6605, 6589.14, 6593.01],
            },
            {
              x: new Date(1538875800000),
              y: [6593.15, 6605, 6592, 6603.06],
            },
            {
              x: new Date(1538877600000),
              y: [6603.07, 6604.5, 6599.09, 6603.89],
            },
            {
              x: new Date(1538879400000),
              y: [6604.44, 6604.44, 6600, 6603.5],
            },
            {
              x: new Date(1538881200000),
              y: [6603.5, 6603.99, 6597.5, 6603.86],
            },
            {
              x: new Date(1538883000000),
              y: [6603.85, 6605, 6600, 6604.07],
            },
            {
              x: new Date(1538884800000),
              y: [6604.98, 6606, 6604.07, 6606],
            },
          ],
        },
      ],
      chartOptions2: {
        plotOptions: {
          candlestick: {
            colors: {
              upward: '#abbcc3',
              downward: '#6b8791',
            },
            wick: {
              useFillColor: true,
            },
          },
        },
        candlestick: {
          colors: {
            upward: '#abbcc3',
            downward: '#6b8791',
          },
          wick: {
            useFillColor: true,
          },
        },
        chart: {
          type: 'candlestick',
          height: 350,
        },
        xaxis: {
          type: 'datetime',
        },
        yaxis: {
          tooltip: {
            enabled: true,
          },
        },
      },
      series: [
        {
          name: 'Submitted',
          type: 'column',
          data: [440, 505, 414, 671, 227, 413, 201, 352, 752, 320, 257, 160],
        },
        {
          name: 'Succeeded',
          type: 'line',
          data: [23, 42, 35, 27, 43, 22, 17, 31, 22, 22, 12, 16],
        },
      ],
      chartOptions: {
        colors: ['#abbcc3', '#728e9b'],
        chart: {
          height: 350,
          type: 'line',
        },
        stroke: {
          width: [0, 4],
        },
        title: {},
        dataLabels: {
          enabled: true,
          enabledOnSeries: [1],
        },
        labels: [
          '01 Jan 2001',
          '02 Jan 2001',
          '03 Jan 2001',
          '04 Jan 2001',
          '05 Jan 2001',
          '06 Jan 2001',
          '07 Jan 2001',
          '08 Jan 2001',
          '09 Jan 2001',
          '10 Jan 2001',
          '11 Jan 2001',
          '12 Jan 2001',
        ],
        xaxis: {
          type: 'datetime',
        },
        yaxis: [
          {
            title: {
              text: 'Submitted',
            },
          },
          {
            opposite: true,
            title: {
              text: 'Succeeded',
            },
          },
        ],
      },
      expanded: true,
      drawer: false,
      mode: 'pan',
      console: true,
      toolbar: true,
      node: null,
      filename: '',
      updateGraphConfirm: false,
      deleteCandidate: {},
      isdisabled: true,
      saveUrl: process.env.APISERVER + '/flow',
      debug: false,
      nodebrowser: false,
      status: 'Ready',
      gridLines: true,
      code: false,
      thecode: 'the code',
      plotpoints: [],
      confirm: false,
      tropes: false,
      roadmap: false,
      renameConfirm: false,
      clear: false,
      edgelabels: true,
      mode: 'pan',
      selectedNodes: 0,
      syncModal: false,
      tooltips: false,
      version: false,
      loading: false,
      selectedTrope: null,
      saveTropeDialog: false,
      deleteConfirm: false,
      deleteConfirmNode: false,
      selectAlert: false,
      savecolor: 'black',
      hotbutton: false,
      toolkitParams: {
        idFunction: idFunction,
        typeFunction: typeFunction,
        autoSave: true,
        autoSaveHandler: function (toolkit) {
          // Notify user about needing save
          console.log('auto save handler');
          //console.log(toolkit.view);
          // toolkit.$root.$emit('flow.shown', toolkit.view)
          toolkit.$root.$emit('status.message', {
            color: 'red',
            type: 'unsavedchanges',
            message: 'Your flow has unsaved changes!',
          });
          toolkit.dirty = true;

          //toolkit.$root.$emit('toolkit.dirty', true);
        },
        groupFactory: function (type, data, callback) {
          console.log('Group factory:', type, data);
          callback(data);
        },
        nodeFactory: function (type, data, callback) {
          console.log('Node factory:', type, data);
          data.columns = [];
          data.rules = [];

          window.root.$emit('node.added', { data: data });
          window.root.$emit('drop.' + type + '.dialog', {
            mode: 'edit',
            obj: data,
          });
          callback(data);
        },
        edgeFactory: function (params, data, callback) {
          // you must hit the callback if you provide the edgeFactory.
          console.log('EDGE FACTORY:', params, data, callback);
          if (!data.name) {
            data.name = data.label;
          }
          data.event = data.label.toLowerCase();
          callback(data);
        },
        // the name of the property in each node's data that is the key for the data for the ports for that node.
        // we used to use portExtractor and portUpdater in this demo, prior to the existence of portDataProperty.
        // for more complex setups, those functions may still be needed.
        portDataProperty: 'columns',
        //
        // Prevent connections from a column to itself or to another column on the same table.
        //
        beforeStartConnect: function (source, edgetype) {
          console.log('beforeStartConnect', source, edgetype);
          if (!source.data.name) {
            source.data.name = source.data.id;
          }
          return {
            label: source.data.id,
            name: source.data.name,
          };
        },
        beforeConnect: function (source, target) {
          console.log('beforeConnect:', source, target);
          console.log(
            source !== target && source.getNode() !== target.getNode()
          );
          return source !== target; // && source.getNode() !== target.getNode();
        },
      },
      renderParams: {
        enablePanButtons: false,
        jsPlumb: {
          Connector: 'StateMachine',
          Endpoint: 'Blank',
        },
        // Layout the nodes using a 'Spring' (force directed) layout. This is the best layout in the jsPlumbToolkit
        // for an application such as this.
        layout: {
          type: 'Spring',
          parameters: {
            padding: [150, 150],
          },
        },
        // Register for certain events from the renderer. Here we have subscribed to the 'nodeRendered' event,
        // which is fired each time a new node is rendered.  We attach listeners to the 'new column' button
        // in each table node.  'data' has 'node' and 'el' as properties: node is the underlying node data,
        // and el is the DOM element. We also attach listeners to all of the columns.
        // At this point we can use our underlying library to attach event listeners etc.
        events: {
          modeChanged: function (mode) {},
          edgeAdded: function (params) {
            // Check here that the edge was not added programmatically, ie. on load.
            console.log('edgeAdded:', params);
            if (params.addedByMouse) {
              var source = params.sourceId.split('.');
              var target = params.targetId.split('.');

              var sourceType = params.source.data['type'];
              var targetType = params.target.data['type'];

              console.log(sourceType, targetType);
              if (!(sourceType === 'Output' && targetType === 'Input')) {
                window.toolkit.removeEdge(params.edge);
              }

              console.log(params.target.getEdges());
              console.log(params.source.getEdges());
              console.log(params.target.getNode().data);

              var sourceEdges = params.source.getEdges();
              var targetEdges = params.target.getEdges();

              var edgeCount = 0;
              for (var i = 0; i < sourceEdges.length; i++) {
                var sourceEdge = sourceEdges[i];
                var sourceId = sourceEdge.data.id;
                var sourceNode = sourceEdge.source.getNode();
                if (sourceNode === params.source.getNode()) {
                  if (sourceEdge.target.getNode() === params.target.getNode()) {
                    let argname = targetEdges[0].target.data.name;
                    console.log('Existing edge: ', sourceEdge);
                    edgeCount += 1;
                  }
                }
              }
              if (edgeCount > 1) {
                console.log(
                  'Cannot add duplicate edge between same source and target!!!!!!'
                );
                console.log(window.toolkit.$q);
                window.toolkit.removeEdge(params.edge);
              } else {
                if (
                  source[1] === target[1] &&
                  params.target.getNode().data.type === 'relation'
                ) {
                  window.toolkit.updateEdge(params.edge, {
                    label: source[1],
                    type: '1:1',
                    etype: source[1],
                  });
                } else {
                }
              }

              if (edgeCount > 1) {
                window.toolkit.$q.notify({
                  color: 'secondary',
                  timeout: 2000,
                  position: 'center',
                  classes: 'flat',
                  message:
                    'Cannot add duplicate edge between same source and target!',
                  icon: '',
                });
              }
            }
          },
          canvasClick: function (e) {
            console.log('Canvas clicked');
            window.toolkit.$root.$emit('set.mode', 'pan');
            window.toolkit.clearSelection();
            window.designer.mode = 'pan';
            window.root.$emit('node.selected', null);
            window.root.$emit('nodes.selected', null);
          },
        },
        dragOptions: {
          filter:
            'i, .view .buttons, .table .buttons, .table-column *, .view-edit, .edit-name',
        },
        consumeRightClick: false,
        zoomToFit: true,
      },
      view: {
        nodes: {
          note: {
            component: NoteTemplate,
            events: {
              tap: function (params) {
                // toolkit.toggleSelection(params.node);
              },
            },
          },
          processor: {
            component: ScriptTemplate,
            events: {
              tap: function (params) {
                if (
                  params.e.srcElement.localName === 'span' &&
                  params.e.srcElement.className === 'proc-title'
                ) {
                  var parentId = params.e.srcElement.firstChild.parentNode.id;
                  var childId = params.e.srcElement.firstChild.id;
                  if (
                    ((childId && childId.indexOf('port') === -1) || !childId) &&
                    ((parentId && parentId.indexOf('port') === -1) || !parentId)
                  ) {
                    toolkit.toggleSelection(params.node);
                    var elems = document.querySelectorAll('.jtk-node');

                    elems.forEach((el) => {
                      el.style['z-index'] = 0;
                    });
                    params.el.style['z-index'] = 99999;
                    var nodes = toolkit.getSelection().getAll();
                    if (nodes.length === 0) {
                      window.root.$emit('node.selected', null);
                    } else {
                      window.root.$emit('node.selected', params.node);
                      window.root.$emit('nodes.selected', nodes);
                    }
                  }
                }
              },
            },
          },

          document: {
            component: DocumentTemplate,
            events: {
              tap: function (params) {
                if (
                  params.e.srcElement.localName !== 'i' &&
                  params.e.srcElement.localName !== 'td'
                ) {
                  toolkit.toggleSelection(params.node);
                  var elems = document.querySelectorAll('.jtk-node');

                  elems.forEach((el) => {
                    el.style['z-index'] = 0;
                  });
                  params.el.style['z-index'] = 99999;
                  var nodes = toolkit.getSelection().getAll();
                  if (nodes.length === 0) {
                    window.root.$emit('node.selected', null);
                  } else {
                    window.root.$emit('node.selected', params.node);
                    window.root.$emit('nodes.selected', nodes);
                  }
                }
              },
            },
          },
          portin: {
            component: PortInTemplate,
            events: {
              tap: function (params) {
                if (
                  params.e.srcElement.localName !== 'i' &&
                  params.e.srcElement.localName !== 'td'
                ) {
                  toolkit.toggleSelection(params.node);
                  var elems = document.querySelectorAll('.jtk-node');

                  elems.forEach((el) => {
                    el.style['z-index'] = 0;
                  });
                  params.el.style['z-index'] = 99999;
                  var nodes = toolkit.getSelection().getAll();
                  if (nodes.length === 0) {
                    window.root.$emit('node.selected', null);
                  } else {
                    window.root.$emit('node.selected', params.node);
                    window.root.$emit('nodes.selected', nodes);
                  }
                }
              },
            },
          },
          portout: {
            component: PortOutTemplate,
            events: {
              tap: function (params) {
                if (
                  params.e.srcElement.localName !== 'i' &&
                  params.e.srcElement.localName !== 'td'
                ) {
                  toolkit.toggleSelection(params.node);
                  var elems = document.querySelectorAll('.jtk-node');

                  elems.forEach((el) => {
                    el.style['z-index'] = 0;
                  });
                  params.el.style['z-index'] = 99999;
                  var nodes = toolkit.getSelection().getAll();
                  if (nodes.length === 0) {
                    window.root.$emit('node.selected', null);
                  } else {
                    window.root.$emit('node.selected', params.node);
                    window.root.$emit('nodes.selected', nodes);
                  }
                }
              },
            },
          },
          data: {
            component: DataTemplate,
          },
          schema: {
            component: SchemaTemplate,
          },

          router: {
            component: RouterTemplate,
            events: {
              tap: function (params) {
                // params.e.srcElement.localName !== "i" &&
                // params.e.srcElement.localName !== "td"
                if (
                  params.e.srcElement.localName === 'span' ||
                  params.e.srcElement.className === 'jtk-draw-skeleton'
                ) {
                  var parentId = params.e.srcElement.firstChild.parentNode.id;
                  var childId = params.e.srcElement.firstChild.id;
                  if (
                    ((childId && childId.indexOf('port') === -1) || !childId) &&
                    ((parentId && parentId.indexOf('port') === -1) || !parentId)
                  ) {
                    toolkit.toggleSelection(params.node);
                    var elems = document.querySelectorAll('.jtk-node');

                    elems.forEach((el) => {
                      el.style['z-index'] = 0;
                    });
                    params.el.style['z-index'] = 99999;
                    var nodes = toolkit.getSelection().getAll();
                    if (nodes.length === 0) {
                      window.root.$emit('node.selected', null);
                    } else {
                      window.root.$emit('node.selected', params.node);
                      window.root.$emit('nodes.selected', nodes);
                    }
                  }
                }
              },
            },
          },
          parallel: {
            component: ParallelTemplate,
            events: {
              tap: function (params) {
                // params.e.srcElement.localName !== "i" &&
                // params.e.srcElement.localName != "td"
                if (
                  params.e.srcElement.localName === 'span' ||
                  params.e.srcElement.className === 'jtk-draw-skeleton'
                ) {
                  var parentId = params.e.srcElement.firstChild.parentNode.id;
                  var childId = params.e.srcElement.firstChild.id;
                  if (
                    ((childId && childId.indexOf('port') === -1) || !childId) &&
                    ((parentId && parentId.indexOf('port') === -1) || !parentId)
                  ) {
                    toolkit.toggleSelection(params.node);
                    var elems = document.querySelectorAll('.jtk-node');

                    elems.forEach((el) => {
                      el.style['z-index'] = 0;
                    });
                    params.el.style['z-index'] = 99999;
                    var nodes = toolkit.getSelection().getAll();
                    if (nodes.length === 0) {
                      window.root.$emit('node.selected', null);
                    } else {
                      window.root.$emit('node.selected', params.node);
                      window.root.$emit('nodes.selected', nodes);
                    }
                  }
                }
              },
            },
          },
          pipeline: {
            component: PipelineTemplate,
            events: {
              tap: function (params) {
                // params.e.srcElement.localName != "i" &&
                // params.e.srcElement.localName != "td"
                if (
                  params.e.srcElement.localName === 'span' ||
                  params.e.srcElement.className === 'jtk-draw-skeleton'
                ) {
                  var parentId = params.e.srcElement.firstChild.parentNode.id;
                  var childId = params.e.srcElement.firstChild.id;
                  if (
                    ((childId && childId.indexOf('port') === -1) || !childId) &&
                    ((parentId && parentId.indexOf('port') === -1) || !parentId)
                  ) {
                    toolkit.toggleSelection(params.node);
                    var elems = document.querySelectorAll('.jtk-node');

                    elems.forEach((el) => {
                      el.style['z-index'] = 0;
                    });
                    params.el.style['z-index'] = 99999;
                    var nodes = toolkit.getSelection().getAll();
                    if (nodes.length === 0) {
                      window.root.$emit('node.selected', null);
                    } else {
                      window.root.$emit('node.selected', params.node);
                      window.root.$emit('nodes.selected', nodes);
                    }
                  }
                }
              },
            },
          },
          segment: {
            component: SegmentTemplate,
            events: {
              tap: function (params) {
                // params.e.srcElement.localName != "i" &&
                // params.e.srcElement.localName != "td"
                if (
                  params.e.srcElement.localName === 'span' ||
                  params.e.srcElement.className === 'jtk-draw-skeleton'
                ) {
                  var parentId = params.e.srcElement.firstChild.parentNode.id;
                  var childId = params.e.srcElement.firstChild.id;
                  if (
                    ((childId && childId.indexOf('port') === -1) || !childId) &&
                    ((parentId && parentId.indexOf('port') === -1) || !parentId)
                  ) {
                    toolkit.toggleSelection(params.node);
                    var elems = document.querySelectorAll('.jtk-node');

                    elems.forEach((el) => {
                      el.style['z-index'] = 0;
                    });
                    params.el.style['z-index'] = 99999;
                    var nodes = toolkit.getSelection().getAll();
                    if (nodes.length === 0) {
                      window.root.$emit('node.selected', null);
                    } else {
                      window.root.$emit('node.selected', params.node);
                      window.root.$emit('nodes.selected', nodes);
                    }
                  }
                }
              },
            },
          },
          chord: {
            component: ChordTemplate,
            events: {
              tap: function (params) {
                // params.e.srcElement.localName != "i" &&
                // params.e.srcElement.localName != "td"
                if (
                  params.e.srcElement.localName === 'span' ||
                  params.e.srcElement.className === 'jtk-draw-skeleton'
                ) {
                  var parentId = params.e.srcElement.firstChild.parentNode.id;
                  var childId = params.e.srcElement.firstChild.id;
                  if (
                    ((childId && childId.indexOf('port') === -1) || !childId) &&
                    ((parentId && parentId.indexOf('port') === -1) || !parentId)
                  ) {
                    toolkit.toggleSelection(params.node);
                    var elems = document.querySelectorAll('.jtk-node');

                    elems.forEach((el) => {
                      el.style['z-index'] = 0;
                    });
                    params.el.style['z-index'] = 99999;
                    var nodes = toolkit.getSelection().getAll();
                    if (nodes.length === 0) {
                      window.root.$emit('node.selected', null);
                    } else {
                      window.root.$emit('node.selected', params.node);
                      window.root.$emit('nodes.selected', nodes);
                    }
                  }
                }
              },
            },
          },
        },
        // Three edge types  - '1:1', '1:N' and 'N:M',
        // sharing  a common parent, in which the connector type, anchors
        // and appearance is defined.
        edges: {
          flowchart: {
            endpoint: 'Blank',
            anchor: ['Left', 'Right'], // anchors for the endpoints
            // connector: ["Flowchart", { cornerRadius: 10 }], //  StateMachine connector
            connector: ['Flowchart', { cornerRadius: 10 }], //  StateMachine connector type
            cssClass: 'common-edge',
            events: {
              dbltap: function (params) {
                _editEdge(params.edge);
              },
            },
            overlays: [
              ['Arrow', { location: 1 }],
              [
                'Label',
                {
                  cssClass: 'delete-relationship text-white',
                  label: '${name}',
                  event: '${event}',
                  name: '${name}',
                  events: {
                    tap: function (params) {},
                  },
                },
              ],
            ],
          },
          default: {
            endpoint: 'Blank',
            anchor: ['Left', 'Right'], // anchors for the endpoints
            connector: ['Straight', { stub: 0 }], //  StateMachine connector
            //connector: ["Bezier", {}], //  StateMachine connector type
            cssClass: 'common-edge',
            events: {
              dbltap: function (params) {
                _editEdge(params.edge);
              },
            },
            overlays: [
              ['Arrow', { location: 1 }],
              [
                'Custom',
                {
                  label: '${name}',
                  event: '${event}',
                  name: '${name}',
                  create: function (component) {
                    let QueueClass = Vue.extend(Queue);
                    var nodeValue = null;

                    if (component.source.attributes['data-jtk-port-id']) {
                      nodeValue =
                        component.source.attributes['data-jtk-port-id']
                          .nodeValue;
                    } else if (component.source.attributes['data-port-id']) {
                      nodeValue =
                        component.source.attributes['data-port-id'].nodeValue;
                    }
                    let instance = new QueueClass({
                      propsData: {
                        node: nodeValue,
                        component: component,
                        name: 'sockq2.proc2.do_this', //component.getData()['name'],
                      },
                    });
                    instance.$mount();
                    return instance.$el;
                  },
                  id: 'connector',
                  events: {
                    tap: function (params) {},
                  },
                },
              ],
            ],
          },
        },
        groups: {
          group: {
            component: GroupTemplate,
            constrain: false,
            orphan: true,
            autoSize: true
          },
          pattern: {
            component: PatternTemplate,
            constrain: false,
            orphan: true,
            autoSize: true
          }
        },
        ports: {
          default: {
            template: 'tmplColumn',
            paintStyle: { fill: '#abbcc3' }, // the endpoint's appearance
            hoverPaintStyle: { fill: '#434343' }, // appearance when mouse hovering on endpoint or connection
            edgeType: 'default', // the type of edge for connections from this port type
            maxConnections: -1, // no limit on connections
            dropOptions: {
              hoverClass: 'drop-hover',
            },
            events: {
              dblclick: function () {
                console.log(arguments);
              },
            },
          },
        },
      },
    };
  },
};
</script>
