<template>
  <div
    class="table node shadow-1 jtk-node"
    style="overflow: unset !important;"
    :style="
      'top:' + obj.y + ';left:' + obj.x + ';min-width:' + obj.width + '; '
    "
    @touchstart.stop
    @contextmenu.stop
    @mousemove1="mouseMove"
    @mouseover1="mouseEnter"
    @mouseleave1="mouseExit"
  >
    <q-inner-loading :showing="refreshing" style="z-index: 999999;">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>

    <q-inner-loading :showing="login" style="z-index: 9999999;">
      <q-spinner-gears size="0px" color="primary" />
      <div class="text-center">
        <q-toolbar>
          <q-input
            filled
            outlined
            square
            bottom-slots
            v-model="loginname"
            counter
            maxlength="20"
            dense
          >
            <template v-slot:before>
              <i class="fas fa-lock text-secondary" style="font-size: 0.8em;" />
            </template>
            <template v-slot:after>
              <q-btn dense flat label="Unlock" color="secondary" />
            </template>
          </q-input>
        </q-toolbar>
      </div>
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
              @click="
                obj.icon = 'fas fa-database';
                settingstab = 'database';
              "
            >
              <q-item-section side>
                <q-icon name="fas fa-database"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Database
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="
                obj.icon = 'fab fa-python';
                settingstab = 'settings';
              "
            >
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
            <q-item
              clickable
              v-close-popup
              @click="
                obj.icon = lambdaIcon;
                settingstab = 'lambda';
              "
            >
              <q-item-section side>
                <q-icon
                  :name="this.lambdaIcon"
                  style="font-weight: bold; font-size: 1.2em;"
                ></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Lambda
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
        <span class="proc-title">
          {{ obj.name }}
        </span>
      </span>
      <span
        class="text-secondary"
        style="position: absolute; left: 55px; top: 31px; font-size: 14px;"
      >
        {{ obj.description.substring(0, 35) + '...' }}
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
        style="
          position: absolute;
          right: 60px;
          top: 1em;
          font-weight: bold;
          font-size: 2em;
        "
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
          @click="obj.bandwidth = !obj.bandwidth"
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
            <q-item clickable v-close-popup>
              <q-item-section side>
                <q-icon name="fas fa-list"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Results
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
            <q-item clickable v-close-popup @click="loginProcessor">
              <q-item-section side>
                <q-icon name="fas fa-lock"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Lock
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
    <ul
      v-if="obj.icon === 'fas fa-database'"
      class="table-columns"
      v-for="column in obj.columns"
      :key="column.id"
    >
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
              <q-btn-dropdown
                flat
                content-class="text-dark bg-white"
                dense
                color="secondary"
                label="Query"
                padding="0px"
                size=".8em"
              >
                <q-list dense>
                  <q-item clickable v-close-popup>
                    <q-item-section side>
                      <q-icon name="fas fa-question"></q-icon>
                    </q-item-section>
                    <q-item-section side class="text-blue-grey-8">
                      Query 1
                    </q-item-section>
                  </q-item>
                  <q-item clickable v-close-popup>
                    <q-item-section side>
                      <q-icon name="fas fa-question"></q-icon>
                    </q-item-section>
                    <q-item-section side class="text-blue-grey-8">
                      Query 2
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-btn-dropdown>
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

    <ul
      v-if="obj.icon === 'fab fa-python'"
      class="table-columns"
      v-for="column in obj.columns"
      :key="column.id"
    >
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
            @click="editPort = !editPort"
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
    <div class="row" id="bandwidth" v-if="obj.bandwidth">
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
              v-if="props.cols[1].value === 'inBytes'"
            >
              {{ inBytes }}
            </q-td>
            <q-td
              :key="props.cols[1].name"
              :props="props"
              :style="rowStripe(props.row.index)"
              v-if="props.cols[1].value === 'totalBytes'"
            >
              {{ totalBytes }}
            </q-td>
            <q-td
              :key="props.cols[1].name"
              :props="props"
              :style="rowStripe(props.row.index)"
              v-if="props.cols[1].value === 'outBytes'"
            >
              {{ outBytes }}
            </q-td>
            <q-td
              :key="props.cols[1].name"
              :props="props"
              :style="rowStripe(props.row.index)"
              v-if="props.cols[1].value === 'taskTime'"
            >
              {{ taskTime }}
            </q-td>
            <q-td
              :key="props.cols[3].name"
              :props="props"
              :style="rowStripe(props.row.index) + ';width:80px'"
            >
              <v-sparkline
                v-if="props.cols[1].value === 'inBytes'"
                :labels="props.row.spark.labels"
                :value="bytes_in_5min"
                color="white"
                line-width="2"
                padding="0"
              ></v-sparkline>
              <v-sparkline
                v-if="props.cols[1].value === 'outBytes'"
                :labels="props.row.spark.labels"
                :value="bytes_out_5min"
                color="white"
                line-width="2"
                padding="0"
              ></v-sparkline>
              <v-sparkline
                v-if="props.cols[1].value === 'totalBytes'"
                :labels="props.row.spark.labels"
                :value="totalbytes_5min"
                color="white"
                line-width="2"
                padding="0"
              ></v-sparkline>
              <v-sparkline
                v-if="props.cols[1].value === 'taskTime'"
                :labels="props.row.spark.labels"
                :value="tasktime_out_5min"
                color="white"
                line-width="2"
                padding="0"
              ></v-sparkline>
            </q-td>
            <q-td
              :key="props.cols[1].name"
              :props="props"
              :style="rowStripe(props.row.index)"
            >
              5 min
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
    <q-dialog v-model="deleteItem" persistent>
      <q-card style="padding: 10px; padding-top: 30px;">
        <q-card-section
          class="bg-primary"
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

    <q-card
      style="
        width: 400px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -405px;
        height: 400px;
        top: 0px;
      "
      v-if="editPort"
    >
      <q-card-section
        style="
          padding: 5px;
          z-index: 999999;
          padding-bottom: 10px;
          height: 650px;
        "
      >
      </q-card-section>

      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="editPort = false"
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
          height: 570px;
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
          <q-tab name="settings" label="Settings" />
          <q-tab name="concurrency" label="Concurrency" />
          <q-tab name="schedule" label="Schedule" />
          <q-tab name="security" label="Security" />
          <q-tab name="scaling" label="Scaling" />
        </q-tabs>

        <q-tab-panels v-model="tab" keep-alive>
          <q-tab-panel name="settings" style="padding: 0px;" ref="settings">
            <q-tabs
              v-model="settingstab"
              class="text-primary"
              align="center"
              dense
            >
              <q-tab name="settings" label="Processor" />
              <q-tab name="containersettings" label="Container" />
              <q-tab name="apisettings" label="API" />
              <q-tab
                v-if="obj.icon === lambdaIcon"
                name="lambda"
                label="Lambda"
              /><q-tab
                v-if="obj.icon === 'fas fa-database'"
                name="database"
                label="Database"
              />
            </q-tabs>
            <q-tab-panels v-model="settingstab">
              <q-tab-panel
                name="settings"
                style="padding-top: 0px; padding-bottom: 0px;"
              >
                <div
                  class="q-pa-md"
                  style="max-width: 100%; padding-bottom: 0px;"
                >
                  <q-form
                    @submit="onSubmit"
                    @reset="onReset"
                    class="q-gutter-md"
                  >
                    <q-input
                      filled
                      v-model="obj.name"
                      dense
                      hint="Processor Name"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) || 'Please type something',
                      ]"
                    />

                    <q-input
                      filled
                      v-model="obj.description"
                      dense
                      hint="Processor Description"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) || 'Please type something',
                      ]"
                    />
                    <q-input
                      filled
                      v-model="obj.package"
                      dense
                      hint="Processor Package"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) || 'Please type something',
                      ]"
                    />
                    <q-input
                      filled
                      dense
                      :disable="!obj.usegit"
                      v-model="obj.git"
                      hint="GIT Repository"
                    />

                    <q-input
                      filled
                      dense
                      :disable="!obj.usegit"
                      v-model="obj.commit"
                      hint="Commit Hash"
                    />

                    <q-toolbar>
                      <q-space />
                      <q-checkbox v-model="obj.usegit" label="GIT" />
                      <q-checkbox
                        v-model="obj.container"
                        label="Containerized"
                        style="margin-left: 40px;"
                      />
                      <q-checkbox
                        v-model="obj.enabled"
                        label="Enabled"
                        style="margin-left: 40px;"
                      />
                      <q-checkbox
                        v-model="obj.endpoint"
                        label="API"
                        style="margin-left: 40px; margin-right: 50px;"
                      />
                      <q-checkbox
                        v-model="obj.streaming"
                        label="Streaming"
                        style=""
                      />
                    </q-toolbar>
                  </q-form>
                </div>
              </q-tab-panel>
              <q-tab-panel
                name="containersettings"
                style="padding-top: 0px; padding-bottom: 0px;"
              >
                <div
                  class="q-pa-md"
                  style="max-width: 100%; padding-bottom: 0px;"
                >
                  <q-form class="q-gutter-md">
                    <q-input
                      filled
                      v-model="obj.imagerepository"
                      dense
                      hint="Image Repository"
                      lazy-rules
                      :disable="!obj.container"
                    />
                    <q-input
                      filled
                      v-model="obj.containerimage"
                      dense
                      hint="Container Image"
                      lazy-rules
                      :disable="!obj.container"
                    />
                  </q-form>
                </div>
              </q-tab-panel>
              <q-tab-panel
                name="apisettings"
                style="padding-top: 0px; padding-bottom: 0px;"
              >
                <div
                  class="q-pa-md"
                  style="max-width: 100%; padding-bottom: 0px;"
                >
                  <q-form class="q-gutter-md">
                    <q-input
                      filled
                      v-model="obj.api"
                      dense
                      hint="API Endpoint"
                      lazy-rules
                      :disable="!obj.endpoint"
                    />
                    <q-input
                      filled
                      v-model="obj.websocket"
                      dense
                      hint="Websocket URL"
                      lazy-rules
                      :disable="!obj.streaming"
                    />
                  </q-form>
                </div>
              </q-tab-panel>
              <q-tab-panel
                name="lambda"
                v-if="obj.icon === lambdaIcon"
                style="padding-top: 0px;"
              >
                <div class="q-pa-md" style="max-width: 100%;">
                  <q-form
                    @submit="onSubmit"
                    @reset="onReset"
                    class="q-gutter-md"
                  >
                    <q-input
                      filled
                      v-model="obj.lamdaurl"
                      dense
                      hint="Lambda URL"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) || 'Please type something',
                      ]"
                    />
                  </q-form>
                </div>
              </q-tab-panel>
              <q-tab-panel
                name="database"
                v-if="obj.icon === 'fas fa-database'"
                style="padding-top: 0px;"
              >
                <div class="q-pa-md" style="max-width: 100%;">
                  <q-form
                    @submit="onSubmit"
                    @reset="onReset"
                    class="q-gutter-md"
                  >
                    <q-input
                      filled
                      v-model="obj.databasestring"
                      dense
                      hint="Connection String"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) || 'Please type something',
                      ]"
                    />
                  </q-form>
                </div>
              </q-tab-panel>
            </q-tab-panels>
          </q-tab-panel>
          <q-tab-panel
            name="concurrency"
            style="padding: 20px;"
            ref="concurrency"
          >
            <q-table
              dense
              :columns="deploycolumns"
              :data="deploydata"
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
              <template v-slot:loading>
                <q-inner-loading :showing="true" style="z-index: 9999999;">
                  <q-spinner-gears size="50px" color="primary" />
                </q-inner-loading>
              </template>
            </q-table>
            <q-input
              style="width: 100px;"
              hint="Number of CPUs"
              type="number"
              v-model.number="obj.concurrency"
            />
            <q-inner-loading :showing="deployLoading" style="z-index: 9999999;">
              <q-spinner-gears size="50px" color="primary" />
            </q-inner-loading>
                    <q-btn
          style="position: absolute; bottom: 0px; right: 0px; margin-right:20px"
          flat
          icon="refresh"
          class="bg-primary text-white"
          color="primary"
          @click="refreshDeployments"
          v-close-popup
        />
          </q-tab-panel>
          <q-tab-panel name="schedule" style="padding: 20px;" ref="schedule">
            <q-input
              hint="Enter CRON Expression"
              placeholder="* * * * *"
              v-model.number="obj.cron"
            />
            <q-input
              style="width: 100px;"
              hint="Beat Interval"
              type="number"
              v-model.number="obj.interval"
            />
            <q-checkbox
              v-model="obj.beat"
              style="margin-top: 30px;"
              label="Beat"
            />
            <q-checkbox
              v-model="obj.useschedule"
              style="margin-top: 30px;"
              label="Use CRON"
            />
          </q-tab-panel>
          <q-tab-panel name="security" style="padding: 20px;" ref="security">
          </q-tab-panel>
          <q-tab-panel name="scaling" style="padding: 20px;" ref="scaling">
          </q-tab-panel>
        </q-tab-panels>
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          label="Save"
          class="bg-primary text-white"
          color="primary"
          @click="saveProcessor"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Save
          </q-tooltip>
        </q-btn>
      </q-card-actions>
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
          <q-inner-loading :showing="saving" style="z-index: 999999;">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
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
      v-if="mousecard"
      class="bg-secondary"
      :style="
        'width:200px;height:300px;z-index:9999;position:absolute;top:' +
        cardY +
        'px;left:' +
        cardX +
        'px'
      "
    >
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
      <q-tabs v-model="logtab" class="text-primary" align="center" dense>
        <q-tab name="tasklog" label="Task" />
        <q-tab name="resultlog" label="Result" />
        <q-tab name="msglog" label="Log" />
      </q-tabs>
      <q-tab-panels v-model="logtab" keep-alive>
        <q-tab-panel name="tasklog" style="padding: 0px;" ref="tasklog">
          <q-card-section
            style="
              padding: 5px;
              z-index: 999999;
              padding-bottom: 10px;
              height: 450px;
            "
          >
            <q-scroll-area style="height:425px;width:auto">
              <div v-for="log in tasklogs">
                {{ log['date'] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{
                  log['state']
                }}&nbsp;&nbsp; --&nbsp;&nbsp;{{ log['module'] }}&nbsp;&nbsp;
                --&nbsp;&nbsp;{{ log['task'] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{
                  log['duration']
                }}
              </div>
            </q-scroll-area>
          </q-card-section>
        </q-tab-panel>
        <q-tab-panel name="resultlog" style="padding: 0px;" ref="tasklog">
          <q-card-section
            style="
              padding: 5px;
              z-index: 999999;
              padding-bottom: 10px;
              height: 450px;
            "
          >
            <q-scroll-area style="height:425px;width:auto">
              <div v-for="log in resultlogs">
                {{ log['date'] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{
                  log['module']
                }}&nbsp;&nbsp; --&nbsp;&nbsp;{{ log['task'] }}
                {{ JSON.parse(log['message']) }}
              </div>
            </q-scroll-area>
          </q-card-section>
        </q-tab-panel>
        <q-tab-panel name="msglog" style="padding: 0px;" ref="msglog">
          <q-card-section
            style="
              padding: 5px;
              z-index: 999999;
              padding-bottom: 10px;
              height: 450px;
            "
          >
            <q-scroll-area style="height:425px;width:auto">
              <div v-for="log in msglogs">
                {{ log['date'] }}&nbsp;&nbsp; --&nbsp;&nbsp;&nbsp;
                {{ log['message'] }}
              </div>
            </q-scroll-area>
          </q-card-section>
        </q-tab-panel>
      </q-tab-panels>

      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          flat
          label="Close"
          class="bg-secondary text-dark"
          color="accent"
          @click="logsview = false"
          v-close-popup
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

import ScriptTemplate from 'components/templates/ProcessorTemplate';

export default {
  name: 'ParallelTemplate',
  mixins: [ScriptTemplate]
};
</script>
