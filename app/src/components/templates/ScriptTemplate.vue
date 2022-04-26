<template>
  <div
    class="table node shadow-1 jtk-node"
    style="overflow: unset !important;"
    :style="
      'top:' + obj.y + ';left:' + obj.x + ';min-width:' + obj.width + '; '
    "
    @touchstart.stop
    @contextmenu.stop
  >
    <q-inner-loading :showing="refreshing" style="z-index: 999999;">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
    <q-menu context-menu style="border: 1px solid black;">
      <q-list dense>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-cog"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            Configure
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="far fa-times-circle"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">Disable</q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-database"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View Provenance Data
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fa fa-area-chart"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View Status History
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-list"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View State
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-book"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View Usage
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-plug"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            View Connections
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="far fa-object-group"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            Center in View
          </q-item-section>
        </q-item>
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-palette"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            Change Color
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="far fa-object-group"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">Group</q-item-section>
        </q-item>
        <q-separator />

        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-project-diagram"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">
            Create Template
          </q-item-section>
        </q-item>
        <q-separator />

        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-copy"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">Copy</q-item-section>
        </q-item>
        <q-separator />

        <q-item clickable v-close-popup>
          <q-item-section side>
            <q-icon name="fas fa-trash"></q-icon>
          </q-item-section>
          <q-item-section side class="text-blue-grey-8">Delete</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
    <div class="name" style="background: white; height: 90px;">
      <div
        title="Script"
        style="
          margin-top: -15px;
          padding: 10px;
          font-weight: normal;
          padding-left: 2px;
          font-size: 40px;
          margin-right: 5px;
        "
      >
        <q-btn-dropdown
          flat
          content-class="text-dark bg-white"
          dense
          color="secondary"
          :dropdown-icon="obj.icon"
          padding="0px"
          size=".6em"
        >
          <q-list dense>
            <q-item
              clickable
              v-close-popup
              @click="obj.icon = 'fas fa-database'"
            >
              <q-item-section side>
                <q-icon name="fas fa-database"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Database
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="obj.icon = 'fab fa-python'">
              <q-item-section side>
                <q-icon name="fab fa-python"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Script
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="obj.icon = 'fas fa-cloud'">
              <q-item-section side>
                <q-icon name="fas fa-cloud"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                API
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="obj.icon = 'fas fa-file'">
              <q-item-section side>
                <q-icon name="fas fa-file"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Document
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="obj.icon = 'fas fa-link'">
              <q-item-section side>
                <q-icon name="fas fa-link"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                URL
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="obj.icon = 'fas fa-table'">
              <q-item-section side>
                <q-icon name="fas fa-table"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Spreadsheet
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="obj.icon = 'alt_route'">
              <q-item-section side>
                <q-icon name="alt_route"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Router
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
      <span
        style="position: absolute; left: 55px; font-size: 20px; top: 5px;"
        class="text-black"
      >
        <span>
          {{ obj.name }}
        </span>
      </span>
      <span
        class="text-secondary"
        style="position: absolute; left: 55px; top: 31px; font-size: 14px;"
      >
        {{ obj.description.substring(0,35)+"..." }}

      </span>
      <span
        class="text-blue-grey-8"
        style="position: absolute; left: 55px; top: 51px; font-size: 11px;"
      >
        {{ obj.package }}
      </span>
      <span
        class="text-red"
        v-if="error"
        style="position: absolute; left: 55px; top: 70px; font-size: 11px;"
      >
        Error messages {{ delayMs }} {{ count }}
      </span>
      <span
        class="text-secondary pull-right table-column-edit"
        style="position: absolute; right: 60px; top: 1em; font-weight: bold; font-size: 2em;"
      >
        {{ obj.concurrency }}
        <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Concurrency
          </q-tooltip>
      </span>
      <span
        class="text-blue-grey-8 pull-right"
        style="position: absolute; right: 10px; top: 50px; font-size: 11px;"
      >
        v1.2.2
      </span>
      <div class="buttons" style="position: absolute; right: 00px; top: 68px;">
        <div
          class="text-secondary"
          @click="showPanel('workerview', !workerview)"
          style="margin-right: 10px;"
        >
          <i class="fas fa-hard-hat" style="cursor: pointer;" />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Workers
          </q-tooltip>
        </div>
        <div
          class="text-secondary"
          @click="bandwidth = !bandwidth"
          style="margin-right: 10px;"
        >
          <i class="fas fa-tachometer-alt" style="cursor: pointer;" />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Bandwidth Toggle
          </q-tooltip>
        </div>
        <!--
        <div
          class="text-secondary"
          style="margin-right: 10px;"
          @click="addNewPort('Complete', 'fas fa-flag-checkered')"
        >
          <i class="fas fa-flag-checkered" style="cursor: pointer;" />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Complete Plug
          </q-tooltip>
        </div>-->
        <div
          class="text-secondary"
          style="margin-right: 10px;"
          @click="addNewPort('Error', 'fas fa-exclamation')"
        >
          <i class="fas fa-exclamation" style="cursor: pointer;" />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Error Plug
          </q-tooltip>
        </div>
        <div
          class="text-secondary"
          @click="addNewPort('Input', 'outlet-icon')"
          style="margin-right: 10px;"
        >
          <i class="outlet-icon" style="cursor: pointer;" />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Socket
          </q-tooltip>
        </div>
        <div
          class="text-secondary"
          style="margin-right: 10px;"
          @click="addNewPort('Output', 'fas fa-plug')"
        >
          <i class="fas fa-plug" style="cursor: pointer;"></i>
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Plug
          </q-tooltip>
        </div>

        <div style="position: absolute; right: 8px; top: 0px;">
          <q-btn
            size="xs"
            icon="fas fa-code"
            dense
            flat
            @click="showPanel('codeview', !codeview)"
            class="show-code text-secondary"
            style="
              margin-right: 10px;
              position: absolute;
              right: 105px;
              top: -68px;
              width: 30px;
              height: 30px;
            "
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Code
            </q-tooltip>
          </q-btn>
          <q-btn
            icon="fa fa-play"
            size="xs"
            dense
            flat
            class="edit-name text-secondary"
            style="
              position: absolute;
              right: 75px;
              top: -68px;
              width: 30px;
              height: 30px;
            "
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Run
            </q-tooltip>
          </q-btn>
          <q-btn
            dense
            flat
            size="xs"
            icon="fa fa-cog"
            @click="showPanel('configview', !configview)"
            class="edit-name text-secondary"
            style="
              position: absolute;
              right: 45px;
              top: -68px;
              width: 30px;
              height: 30px;
            "
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Configure
            </q-tooltip>
          </q-btn>
          <q-btn
            icon="fas fa-times"
            size="xs"
            @click="deleteConfirm = true"
            flat
            dense
            class="new-column add text-secondary"
            style="
              position: absolute;
              right: 20px;
              top: -68px;
              width: 30px;
              height: 30px;
            "
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Delete
            </q-tooltip>
          </q-btn>
        </div>
        <q-btn-dropdown
          flat
          content-class="text-dark bg-white"
          dense
          color="secondary"
          padding="0px"
          style="
            position: absolute;
            right: 0px;
            width: 30px;
            height: 30px;
            top: -68px;
          "
        >
          <q-list dense>
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fas fa-save"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Save
              </q-item-section>
            </q-item>
            <q-item clickable v-close-popup @click="refreshProcessor">
              <q-item-section side>
                <q-icon name="fas fa-refresh"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Refresh
              </q-item-section>
            </q-item>
            <q-separator />

            <q-item
              clickable
              v-close-popup
              @click="showPanel('commentsview', !commentsview)"
            >
              <q-item-section side>
                <q-icon name="far fa-comments"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Comments
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
              @click="showPanel('gitview', !gitview)"
            >
              <q-item-section side>
                <q-icon name="fab fa-github"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Git
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="showPanel('historyview', !historyview)"
            >
              <q-item-section side>
                <q-icon name="fas fa-history"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                History
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="showPanel('logsview', !logsview)"
            >
              <q-item-section side>
                <q-icon name="fas fa-glasses"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Logs
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="showPanel('requirementsview', !requirementsview)"
            >
              <q-item-section side>
                <q-icon name="fab fa-python"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Requirements
              </q-item-section>
            </q-item>
            <q-separator />
            
            <q-item
              clickable
              v-close-popup
              @click="showPanel('environmentview', !environmentview)"
            >
              <q-item-section side>
                <q-icon name="far fa-list-alt"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Environment
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
    </div>
    <ul class="table-columns" v-for="column in obj.columns" :key="column.id">
      <li
        :class="
          'table-column jtk-droppable table-column-type-' + column.datatype
        "
        :style="
          'background:' +
          column.background +
          ';border-top: 1px dashed lightgrey'
        "
        :primary-key="column.primaryKey"
        :data-port-id="column.id"
      >
        <div class="table-column-edit text-primary">
          <i
            class="fa fa-times table-column-delete-icon"
            title="Delete Port"
            @click="confirmDeleteSpeech(column.id)"
          />
        </div>
        <div class="table-column-edit text-primary">
          <i
            class="fas fa-edit"
            title="Edit Name"
            style="margin-right: 5px;"
            @click=""
          />
        </div>
        <div>
          <div class="float-left text-secondary">
            <i
              :class="column.icon"
              :title="column.name"
              style="margin-right: 5px;"
            />
          </div>
          <span>
            <span :id="column.id">
              {{ column.name }}
              <q-popup-edit
                style="
                  width: 50%;
                  font-weight: bold;
                  font-size: 25px;
                  font-family: 'Indie Flower', cursive;
                  margin-top: 5px;
                "
                v-model="column.name"
                @save="
                  (val, initialValue) =>
                    updateName(val, initialValue, column.id)
                "
              >
                <q-input
                  style="
                    font-weight: bold;
                    font-size: 25px;
                    font-family: 'Indie Flower', cursive;
                    margin-top: 5px;
                  "
                  v-model="column.name"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </span>
            : {{ column.description }}
          </span>
        </div>

        <jtk-source
          name="source"
          :port-id="column.id"
          :scope="column.datatype"
          filter=".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon"
          filter-exclude="true"
        />

        <jtk-target
          name="target"
          :port-id="column.id"
          :scope="column.datatype"
        />
      </li>
    </ul>

    <q-separator />
    <div class="row" id="bandwidth" v-if="bandwidth">
      <q-table
        dense
        hide-header
        hide-bottom
        :data="data"
        :columns="columns"
        row-key="name"
        style="width: 100%; border-top-radius: 0px; border-bottom-radius: 0px;"
      >
        <template v-slot:body="props">
          <q-tr
            :props="props"
            :key="getUuid"
            @click="showPanel('dataview', !dataview)"
          >
            <q-td
              :key="props.cols[0].name"
              :props="props"
              :style="rowStripe(props.row.index)"
            >
              {{ props.cols[0].value }}
            </q-td>
            <q-td
              :key="props.cols[1].name"
              :props="props"
              :style="rowStripe(props.row.index)"
            >
              {{ props.cols[1].value }}
            </q-td>
            <q-td
              :key="props.cols[3].name"
              :props="props"
              :style="rowStripe(props.row.index) + ';width:80px'"
            >
              <v-sparkline
                :labels="props.row.spark.labels"
                :value="props.row.spark.value"
                color="white"
                line-width="2"
                padding="0"
              ></v-sparkline>
            </q-td>
            <q-td
              :key="props.cols[2].name"
              :props="props"
              :style="rowStripe(props.row.index)"
            >
              {{ props.cols[2].value }}
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
    <q-dialog v-model="deleteItem" persistent>
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
              <q-item-label>Delete Item</q-item-label>
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
            Are you sure you want to delete this item?
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
            @click="removeColumn(deleteSpeechID)"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Delete dialog -->
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
              <q-item-label>Delete Item</q-item-label>
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
            Are you sure you want to delete this item?
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
            @click="deleteNode"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Code dialog -->
    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="codeview"
    >
      <q-card-section
        style="padding: 5px; z-index: 999999; padding-bottom: 10px;"
      >
        <editor
          v-model="obj.code"
          @init="editorInit"
          style="font-size: 16px; min-height: 600px;"
          lang="python"
          theme="chrome"
          ref="myEditor"
          width="100%"
          height="fit"
        ></editor>
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish To Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="codeview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="requirementsview"
    >
      <q-card-section
        style="padding: 5px; z-index: 999999; padding-bottom: 10px;"
      >
        <editor
          v-model="obj.requirements"
          @init="editorInit"
          style="font-size: 16px; min-height: 600px;"
          lang="python"
          theme="chrome"
          ref="myEditor"
          width="100%"
          height="fit"
        ></editor>
      </q-card-section>
      <q-card-actions align="left">
       
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="requirementsview = false"
          v-close-popup
        >
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>

    <!-- Git dialog -->
    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
        height: 500px;
      "
      v-if="gitview"
    >
      <q-card-section>
        <q-splitter v-model="splitterModel" horizontal style="height: 465px;">
          <template v-slot:before>
            <div class="q-pa-md">
              <div class="text-h4 q-mb-md">Before</div>
              <div v-for="n in 20" :key="n" class="q-my-md">
                {{ n }}. Lorem ipsum dolor sit, amet consectetur adipisicing
                elit. Quis praesentium cumque magnam odio iure quidem, quod
                illum numquam possimus obcaecati commodi minima assumenda
                consectetur culpa fuga nulla ullam. In, libero.
              </div>
            </div>
          </template>

          <template v-slot:after>
            <div class="q-pa-md">
              <div class="text-h4 q-mb-md">After</div>
              <div v-for="n in 20" :key="n" class="q-my-md">
                {{ n }}. Lorem ipsum dolor sit, amet consectetur adipisicing
                elit. Quis praesentium cumque magnam odio iure quidem, quod
                illum numquam possimus obcaecati commodi minima assumenda
                consectetur culpa fuga nulla ullam. In, libero.
              </div>
            </div>
          </template>
        </q-splitter>
      </q-card-section>
      <q-card-section
        style="padding: 5px; z-index: 999999; padding-bottom: 10px;"
      ></q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish To Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="gitview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
        />
      </q-card-actions>
    </q-card>

    <!-- Config dialog -->

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="configview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 700px;
        "
      >
      <q-tabs
        v-model="tab"
          dense
          class="bg-accent"
          align="left"
          narrow-indicator
          active-color="dark"
          indicator-color="accent"
          active-bg-color="white"
      >
        <q-tab name="settings"  label="Settings" />
        <q-tab name="concurrency"  label="Concurrency" />
        <q-tab name="schedule" label="Schedule" />
        <q-tab name="security" label="Security" />
        <q-tab name="scaling" label="Scaling" />
      </q-tabs>
       <q-tab-panels v-model="tab" keep-alive>
        <q-tab-panel
          name="settings"
          style="padding: 0px;"
          ref="settings"
        >

        <div class="q-pa-md" style="max-width: 100%;">
          <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
            <q-input
              filled
              v-model="obj.name"
              hint="Processor Name"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
            />

            <q-input
              filled
              v-model="obj.description"
              hint="Processor Description"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
            />
            <q-input
              filled
              v-model="obj.package"
              hint="Processor Package"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
            />
            <q-input
              filled
              v-model="obj.git"
              hint="GIT Repository"
            />

            <q-input
              filled
              v-model="obj.commit"
              hint="Commit Hash"
            />
            <q-input
              filled
              v-model="obj.api"
              hint="API Endpoint"
              lazy-rules
              :disable="!obj.endpoint"
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
              ]"
            />

            <q-toolbar>
              
              <q-space/>
              <q-checkbox v-model="obj.container" label="Containerized" />
              <q-checkbox v-model="obj.enabled" label="Enabled" style="margin-left: 40px;"/>
              <q-checkbox
                v-model="obj.endpoint"
                label="Expose Endpoint"
                style="margin-left: 40px;margin-right:50px"
              />
            </q-toolbar>
          </q-form>
        </div>
        </q-tab-panel>
        <q-tab-panel
          name="concurrency"
          style="padding: 20px;"
          ref="concurrency"
        >
        <q-input style="width:100px" hint="Number of CPUs" type="number" v-model.number="obj.concurrency"  />
        </q-tab-panel>
        <q-tab-panel
          name="schedule"
          style="padding: 20px;"
          ref="schedule"
        >
        <q-input hint="Enter CRON Expression" placeholder="* * * * *" v-model.number="obj.cron"  />

        <q-checkbox v-model="obj.useschedule" style="margin-top:30px" label="Use Schedule" />
        </q-tab-panel>
        <q-tab-panel
          name="security"
          style="padding: 20px;"
          ref="security"
        >
        </q-tab-panel>
        <q-tab-panel
          name="scaling"
          style="padding: 20px;"
          ref="scaling"
        >
        </q-tab-panel>
        </q-tab-panels>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="configview = false"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
        height: calc(100%+10px);
      "
      v-if="workerview"
    >
      <q-inner-loading :showing="workersLoading" style="z-index: 9999999;">
        <q-spinner-gears size="50px" color="primary" />
      </q-inner-loading>
      <q-card-section
        style="padding: 15px; z-index: 999999; padding-bottom: 10px;"
      >
        <q-table
          dense
          :columns="workercolumns"
          :data="workerdata"
          row-key="name"
          flat
          virtual-scroll
          :rows-per-page-options="[10]"
          style="
            width: 100%;
            border-top-radius: 0px;
            border-bottom-radius: 0px;
          "
        >
        </q-table>
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="refresh"
          class="bg-primary text-white"
          color="primary"
          @click="refreshWorkers"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Refresh
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right" style="padding-top: 20px;">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="workerview = false"
          v-close-popup
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="environmentview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 400px;
        "
      >
        Environment view
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish to Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="environmentview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="scalingview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 400px;
        "
      >
        Scaling view
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish to Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="scalingview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="historyview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 400px;
        "
      >
        History view
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish to Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="historyview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="commentsview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 400px;
        "
      >
        Comments view
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish to Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="commentsview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="securityview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 400px;
        "
      >
        Security view
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish to Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="securityview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="logsview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 400px;
        "
      >
        Logs view
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="history"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Revert to Last
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 90px; width: 100px;"
          flat
          icon="published_with_changes"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Publish to Network
          </q-tooltip>
        </q-btn>
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 100px; width: 100px;"
          flat
          label="Close"
          class="bg-accent text-dark"
          color="primary"
          @click="logsview = false"
          v-close-popup
        />
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Save"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="removeColumn(deleteSpeechID)"
        />
      </q-card-actions>
    </q-card>

    <!-- Chart dialog -->
    <q-card
      style="
        width: 100%;
        width: 650px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -655px;
        top: 0px;
      "
      v-if="dataview"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 400px;
        "
      >
        <div id="chart">
          <apexchart
            type="candlestick"
            height="390"
            :options="chartOptions2"
            :series="series2"
          ></apexchart>
        </div>
      </q-card-section>
      <q-card-actions align="left"></q-card-actions>
      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="dataview = false"
          v-close-popup
        />
      </q-card-actions>
    </q-card>
  </div>
</template>
<style>
.q-item {
  margin-right: 0px;
}
.ace-editor {
  width: 100%;
  height: 100%;
}
tbody tr:nth-child(odd) {
  background-color: rgb(244, 246, 247) !important;
}

.q-menu {
  border-radius: 0px;
}
.ace_gutter > .ace_layer {
  background-color: #e3e8ec;
}
.resizable-content {
}
</style>
<script>
import { BaseNodeComponent } from 'jsplumbtoolkit-vue2';
import { v4 as uuidv4 } from 'uuid';
import VueResizable from 'vue-resizable';
import Vuetify from 'vuetify';

// Import the mixin class
import Processor from '../Processor.vue';
import BetterCounter from '../BetterCounter';
// use mixins to mix in methods, data, store for 'Processor' objects.
// The template thus defers to the mixed in methods for its state
// The Processor object mixin connects to the vuex store and websocket detail, and api as well.
// This template simply acts as an input/output layer to t3he mixed in component
// The mixed in component data fields are fully reactive in this Vue template because it's
// mixed in.

export default {
  name: 'ScriptTemplate',
  mixins: [BaseNodeComponent, BetterCounter, Processor], // Mixin the components
  vuetify: new Vuetify(),
  components: {
    editor: require('vue2-ace-editor'),
    VueResizable,
    BetterCounter,
  },
  watch: {
    // Here we can watch mixed in properties that will update behind the scenes
    name: function (val) {
      console.log('NAME IS', this.name);
    },
    delayMs: function (val) {
      console.log('delayMs CHANGED', val);
    },
  },
  created() {
    var me = this;

    console.log('me.tooltips ', me.tooltips);
    console.log('start listening for show.tooltips');
    window.root.$on('show.tooltips', (value) => {
      console.log('start tooltips:', value);
      me.tooltips = value;
      console.log('ME:', me);
      console.log('TOOLTIPS', me.tooltips);
    });

    // Print some fields from the mixin component
    console.log(
      'BetterCounter: ',
      this.delayMs,
      this.internalPerformAsyncIncrement
    );
    console.log('getcount', this.countLabel);
    // Changing this.delayMs will cause it to be saved in the vuex store and sync'd with server.
    // Any changes to the server will arrive through the customer Store via websockets, update the
    // vuex model and cause any reactive components in this view to change as well.
    setTimeout(() => {
      me.delayMs = 500; // Update the reactive mixin data field
      me.internalPerformAsyncIncrement();
      me.delayMs += 10;
      me.count += 10;
      //me.name = 'MyProcessor 2!';
    }, 3000);
  },
  computed: {
    readwrite() {
      return this.obj.readwrite;
    },
  },
  mounted() {
    var me = this;
    console.log('MOUNTED STORE', this.$store);
    // Execute method on mixed in component, which sends to server using socket.io
    this.sayHello({ name: 'darren', age: 51 });
    function shiftvalues() {
      console.log('Rotating...');
      var front = me.data[0].spark.value.shift();
      me.obj.readwrite += front;
      me.data[0].bytes = front + ' (' + me.obj.readwrite + ' bytes)';
      me.data[0].spark.value.push(front);
      var front = me.data[1].spark.value.shift();
      me.data[1].spark.value.push(front);
      var front = me.data[2].spark.value.shift();
      me.data[2].spark.value.push(front);
      var front = me.data[3].spark.value.shift();
      me.data[3].spark.value.push(front);
      setTimeout(shiftvalues, 1000);
    }
    //setTimeout(shiftvalues, 500);
  },
  data() {
    return {
      tab:'settings',
      error: true,
      refreshing: false,
      workersLoading: true,
      splitterModel: 50,
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
      obj: {
        // Will come from mixed in Script object (vuex state, etc)
        icon: 'fab fa-python',
        style: '',
        x: 0,
        y: 0,
        requirements:'',
        container: false,
        enabled: true,
        endpoint: false,
        api: '/api/processor',
        type: 'script',
        name: 'Script Processor',
        label: 'Script',
        description: 'A script processor description',
        package: 'my.python.package',
        concurrency: 3,
        cron:"* * * * *",
        useschedule: false,
        disabled: false,
        commit: "",
        git:
          'https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor',
        columns: [],
        readwrite: 0,
        properties: [],
      },
      text: '',
      configview: false,
      workerview: false,
      historyview: false,
      logsview: false,
      requirementsview: false,
      commentsview: false,
      securityview: false,
      environmentview: false,
      scalingview: false,
      dataview: false,
      deleteSpeechID: null,
      sidecode: true,
      bandwidth: true,
      workercolumns: [
        {
          name: 'Name',
          label: 'Name',
          field: 'name',
          align: 'left',
        },
        {
          name: 'Host',
          label: 'Host',
          field: 'host',
          align: 'left',
        },
        {
          name: 'CPU',
          label: 'CPU',
          field: 'cpu',
          align: 'left',
        },
        {
          name: 'RAM',
          label: 'RAM',
          field: 'ram',
          align: 'left',
        },
        {
          name: 'Disk',
          label: 'Disk',
          field: 'disk',
          align: 'left',
        },
        {
          name: 'Tasks',
          label: 'Tasks',
          field: 'tasks',
          align: 'left',
        },
      ],
      columns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left',
        },
        {
          name: 'bytes',
          align: 'center',
          label: 'Bytes',
          field: 'bytes',
        },
        {
          name: 'time',
          align: 'right',
          classes: 'text-secondary',
          label: 'Time',
          field: 'time',
        },
        {
          name: 'spark',
          align: 'center',
          classes: 'text-secondary',
          label: 'Spark',
          field: 'spark',
        },
      ],
      workerdata: [
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
        {
          name: 'Name1',
          host: 'Host1',
          cpu: 'CPU1',
          disk: 'Disk1',
          ram: 'RAM1',
          tasks: 'Task1',
        },
      ],
      data: [
        {
          name: 'In',
          bytes: '0 (0 bytes)',
          time: '5 min',
          spark: {
            name: 'in',
            labels: ['12am', '3am', '6am', '9am', '12pm', '3pm', '6pm', '9pm'],
            value: [200, 675, 410, 390, 310, 460, 250, 240],
          },
        },
        {
          name: 'Read/Write',
          bytes: '0 (0 bytes)',
          time: '5 min',
          spark: {
            name: 'readwrite',
            labels: ['12am', '3am', '12pm', '3pm', '6pm', '6am', '9am', '9pm'],
            value: [200, 390, 310, 460, 675, 410, 250, 240],
          },
        },
        {
          name: 'Out',
          bytes: '0 (0 bytes)',
          time: '5 min',
          spark: {
            name: 'readoutwrite',
            labels: ['3pm', '6pm', '9pm', '12am', '3am', '6am', '9am', '12pm'],
            value: [460, 250, 240, 200, 675, 410, 390, 310],
          },
        },
        {
          name: 'Tasks/Time',
          bytes: '0 (0 bytes)',
          time: '5 min',
          spark: {
            name: 'taskstime',
            labels: ['9am', '12pm', '3pm', '6pm', '9pm', '12am', '3am', '6am'],
            value: [390, 310, 460, 250, 240, 200, 675, 410],
          },
        },
      ],
      codeview: false,
      gitview: false,
      entityName: '',
      columnName: '',
      thecode: '',
      tooltips: false,
      tooltip: false,
      code: false,
      ports: {
        next: false,
        error: false,
        join: false,
        split: false,
        complete: false,
      },
      confirm: false,
      deleteItem: false,
      deleteConfirm: false,
      prompt: false,
      contentStyle: {
        backgroundColor: 'rgba(0,0,0,0.02)',
        color: '#555',
      },

      contentActiveStyle: {
        backgroundColor: '#eee',
        color: 'black',
      },

      thumbStyle: {
        right: '2px',
        borderRadius: '5px',
        backgroundColor: '#027be3',
        width: '5px',
        opacity: 0.75,
      },
    };
  },
  methods: {
    onSubmit() {

    },
    onReset() {

    },
    refreshWorkers() {
      var me = this;
      this.workersLoading = true;
      setTimeout(() => {
        me.workersLoading = false;
      }, 2000);
    },
    refreshProcessor() {
      var me = this;
      this.refreshing = true;
      setTimeout(() => {
        me.refreshing = false;
      }, 2000);
    },
    getUuid() {
      return 'key_' + uuidv4();
    },
    rowStripe(row) {
      if (row % 2 == 0) {
        return 'background-color:white';
      }
    },
    workerviewSetup() {
      var me = this;
      setTimeout(() => {
        me.workersLoading = false;
      }, 2000);
    },
    showPanel(view, show) {
      this.configview = false;
      this.codeview = false;
      this.dataview = false;
      this.gitview = false;
      this.workerview = false;
      this.historyview = false;
      this.environmentview = false;
      this.scalingview = false;
      this.commentsview = false;
      this.requirementsview = false;
      this.logsview = false;
      this.securityview = false;
      this[view] = show;
      if (this[view + 'Setup']) {
        this[view + 'Setup']();
      }

      if (show) {
        //window.toolkit.surface.setZoom(1.0);

        var node = this.toolkit.getNode(this.obj);
        /*
        window.toolkit.surface.centerOn(node, {
          doNotAnimate: true,
          onComplete: function () {
            var loc = window.toolkit.surface.mapLocation(300, 50);
            console.log(loc);
            window.toolkit.surface.pan(-350, -300);
          },
        });*/
      }
    },
    updateDescription(value, initialValue) {
      console.log('updateDesc', value, initialValue);
      this.renameConfirm = true;
      this.renameValue = value;
      this.initialValue = initialValue;
    },
    updateName(value, initialValue, column) {
      console.log('column edited ', column);
      console.log('updateName', value, initialValue);
      this.renameConfirm = true;
      this.renameValue = value;
      this.initialValue = initialValue;
      var edges = document.querySelectorAll('[data-source=' + column + ']');

      edges.forEach((edge) => {
        edge.innerText = value;
      });
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

      setTimeout(function () {
        // me.thecode = me.obj.code;
      }, 500);
    },
    showCode() {
      // this.code = true;
    },
    showTooltip(show) {
      this.tooltip = show;
    },
    showSpeakerDialog(tab) {
      // this.$root.$emit("show.speaker.tab",tab);
      window.root.$emit('new.speaker.dialog', {
        mode: 'edit',
        tab: tab,
        obj: this.obj,
      });
      console.log('show speaker dialog');
    },
    confirmDeleteSpeech(id) {
      this.deleteSpeechID = id;
      this.deleteItem = true;
    },
    resetToolkit() {
      console.log('emitting toolkit.dirty');
      this.$root.$emit('toolkit.dirty', false);
    },
    valueChanged() {
      console.log('emitting toolkit.dirty');
      this.$root.$emit('toolkit.dirty', true);
    },
    deleteNode() {
      window.toolkit.removeNode(this.obj);
    },
    removeColumn(column) {
      console.log('Removing column: ', column);

      for (var i = 0; i < this.obj.columns.length; i++) {
        var col = this.obj.columns[i];
        console.log(col);
        if (col.id == column) {
          console.log('Deleted column');
          this.obj.columns.splice(i, 1);
          break;
        }
      }

      var edges = window.toolkit.getAllEdges();

      for (var i = 0; i < edges.length; i++) {
        console.log(edge);
        const edge = edges[i];
        console.log(
          edge.source.getNode().id,
          this.obj.id,
          edge.data.label,
          column
        );
        if (
          edge.source.getNode().id === this.obj.id &&
          edge.data.label == column
        ) {
          window.toolkit.removeEdge(edge);
        }
      }
      // Delete all the edges for this column id
      console.log(this.obj);
      window.toolkit.removePort(this.obj.id, column);
      // window.renderer.repaint(this.obj);
    },
    addPort(port) {
      port.background = 'white';
      port.datatype = 'Column';
      port.id = 'port' + uuidv4();
      port.id = port.id.replace(/-/g, '');
      port.description = 'A description';
      console.log('Port:', port);
      window.toolkit.addNewPort(this.obj.id, 'column', port);
      window.renderer.repaint(this.obj);
      console.log('Firing node updated...');

      console.log(this.obj.columns);
    },
    addNewPort(name, icon) {
      this.addPort({
        name: name,
        icon: icon,
        type: name,
      });
      this.ports[name] = true;
    },
    addErrorPort() {
      if (this.error) {
        this.$q.notify({
          color: 'negative',
          timeout: 2000,
          position: 'bottom',
          message: 'Error is already created',
          icon: 'fas fa-exclamation',
        });
        return;
      }
      this.addPort({
        name: 'Error',
        icon: 'fas fa-exclamation',
        type: 'Error',
      });
      this.error = true;
    },
    selectNode: function () {
      console.log('selected: ', this.obj.id);
      window.root.$emit('node.selected', this.obj);
    },
    deleteEntity: function (name) {
      this.entityName = name;
      this.confirm = true;
    },
    clicked: function () {
      console.log('clicked');
    },
  },
};
</script>
