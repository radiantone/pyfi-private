<template>
  <!-- transform: skew(-3deg, 0deg); -->
  <div
    class="table node shadow-1 jtk-node"
    style="overflow: unset !important;"
    :style="'top:' + obj.y + ';left:' + obj.x + ';min-width:' + obj.width + '; z-index: 99999999'"
    @touchstart.stop
    @contextmenu.stop
    @mousemove1="mouseMove"
    @mouseover1="mouseEnter"
    @mouseleave1="mouseExit"
  >
    <q-inner-loading
      :showing="refreshing"
      style="z-index: 999999;"
    >
      <q-spinner-gears
        size="50px"
        color="primary"
      />
    </q-inner-loading>

    <q-inner-loading
      :showing="login"
      style="z-index: 9999999;"
    >
      <q-spinner-gears
        size="0px"
        color="primary"
      />
      <div class="text-center">
        <q-toolbar>
          <q-input
            filled
            outlined
            square
            bottom-slots
            v-model="password"
            counter
            maxlength="20"
            dense
          >
            <template #before>
              <i
                class="fas fa-lock text-secondary"
                style="font-size: 0.8em;"
              />
            </template>
            <template #after>
              <q-btn
                dense
                flat
                label="Unlock"
                color="secondary"
                @click="doLogin"
              />
            </template>
          </q-input>
        </q-toolbar>
      </div>
    </q-inner-loading>
    <q-menu
      context-menu
      style="border: 1px solid black;"
    >
      <q-list dense>
        <q-separator />
        <q-item
          clickable
          v-close-popup
          @click="configview = true"
        >
          <q-item-section side>
            <q-icon name="fas fa-cog" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Configure
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item
          clickable
          v-close-popup
          v-if="obj.status === 'running'"
          @click="obj.status = 'stopped'"
        >
          <q-item-section side>
            <q-icon name="fas fa-stop" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Stop
          </q-item-section>
        </q-item>
        <q-item
          clickable
          v-close-popup
          v-if="obj.status === 'stopped'"
          @click="triggerExecute"
        >
          <q-item-section side>
            <q-icon name="fas fa-play" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Run All
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item
          clickable
          v-close-popup
          @click="addToLibrary"
        >
          <q-item-section side>
            <q-icon name="fas fa-book" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Add to Library
          </q-item-section>
        </q-item>
        <q-separator />
        <q-separator />
        <q-item
          clickable
          v-close-popup
          disabled
        >
          <q-item-section side>
            <q-icon :name="this.abacusIcon" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            View State
          </q-item-section>
        </q-item>
        <q-item
          clickable
          v-close-popup
          disabled
        >
          <q-item-section side>
            <q-icon name="fas fa-book" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            View Usage
          </q-item-section>
        </q-item>
        <q-item
          clickable
          v-close-popup
          disabled
        >
          <q-item-section side>
            <q-icon name="las la-list" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            View Connections
          </q-item-section>
        </q-item>
        <q-separator />
        <q-item
          clickable
          v-close-popup
          @click="centerOnNode"
        >
          <q-item-section side>
            <q-icon name="far fa-object-group" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Center in View
          </q-item-section>
        </q-item>
        <q-item
          clickable
          v-close-popup
          @click="cornerInView"
        >
          <q-item-section side>
            <q-icon name="far fa-object-group" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Corner in View
          </q-item-section>
        </q-item>
        <!--
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
        </q-item>-->
        <q-separator />

        <q-item
          clickable
          v-close-popup
          @click="copyNode"
        >
          <q-item-section side>
            <q-icon name="fas fa-copy" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Copy
          </q-item-section>
        </q-item>
        <q-separator />

        <q-item
          clickable
          v-close-popup
          @click="deleteConfirm = true"
        >
          <q-item-section side>
            <q-icon name="fas fa-trash" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Delete
          </q-item-section>
        </q-item>
      </q-list>
    </q-menu>
    <div
      class="name"
      style="background: white; height: 90px;"
    >
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
        <div
          title="Database"
          style="
          margin-top: -15px;
          padding: 10px;
          font-weight: normal;
          font-size: 40px;
          margin-right: 15px;
        "
        >
          <q-icon
            name="fas fa-database"
            size="lg"
            color="secondary"
            style="margin-left:-5px;margin-top:-5px"
          />
        </div>
      </div>
      <span
        v-if="obj.titletab"
        id="toptitle"
        style="
          position: absolute;
          left: 5px;
          font-size: 20px;
          top: -40px;
          z-index: -99999;
          width: 300px;
          padding-left: 20px;
          background-color: white;
          padding: 5px;
        "
        class="text-black shadow-2"
      >
        <span
          class="proc-title text-dark"
          style="font-style: italic; margin-left: 5px;"
        >
          {{ obj.name }}
        </span>
      </span>
      <span
        v-if="!obj.titletab"
        style="position: absolute; left: 65px; font-size: 20px; top: 5px;"
        class="text-black"
      >
        <span class="proc-title">
          {{ obj.name }}
        </span>
      </span>
      <span
        class="text-secondary"
        style="position: absolute; left: 65px; top: 31px; font-size: 14px;"
      >
        {{ obj.description.substring(0, 35) + "..." }}
      </span>
      <span
        class="text-blue-grey-8"
        style="position: absolute; left: 65px; top: 51px; font-size: 11px;"
      >
        {{ obj.package }}
      </span>
      <span
        class="text-red"
        v-if="error"
        style="position: absolute; left: 55px; top: 70px; font-size: 11px;"
      >
        <a
          href="#"
          style="color: red;"
        >Error<q-tooltip
          anchor="top middle"
          :offset="[-30, 40]"
          content-style="font-size: 16px"
          content-class="bg-black text-white"
        >
          {{ errorMsg }}
        </q-tooltip></a>
      </span>

      <span
        class="text-blue-grey-8 pull-right"
        style="position: absolute; left: 10px; top: 70px; font-size: 11px;"
      >
        {{ obj.version }}
      </span>
      <div
        class="buttons"
        style="position: absolute; right: 00px; top: 68px;"
      >
        <div
          class="text-secondary"
          @click="cornerInView"
          style="margin-right: 15px;"
        >
          <i
            class="far fa-object-group"
            style="cursor: pointer;"
          />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Corner
          </q-tooltip>
        </div>
        <div
          class="text-secondary"
          @click="obj.bandwidth = !obj.bandwidth"
          style="margin-right: 10px;"
        >
          <i
            class="fas fa-tachometer-alt"
            style="cursor: pointer;"
          />
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Bandwidth Toggle
          </q-tooltip>
        </div>

        <div
          class="text-secondary"
          style="margin-right: 10px;"
        >
          <!--<i class="outlet-icon" style="cursor: pointer;" />-->

          <q-btn-dropdown
            flat
            content-class="text-dark bg-white "
            dense
            menu-self="top left"
            dropdown-icon="las la-table"
            color="secondary"
            padding="0px"
            size=".8em"
            style="margin-right: 0px;"
          >
            <q-list
              dense
              v-for="table in tables"
              :key="table.name"
            >
              <q-item
                clickable
                v-close-popup
                @click="addNewTablePort({ name: table.name, args: [] }, 'Table', 'las la-table')"
              >
                <q-item-section side>
                  <q-icon name="las la-table" />
                </q-item-section>
                <q-item-section
                  side
                  class="text-blue-grey-8"
                >
                  {{ table.name }}
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Table
          </q-tooltip>
        </div>
        <div
          class="text-secondary"
          style="margin-right: 10px;"
        >
          <!--<i class="outlet-icon" style="cursor: pointer;" />-->

          <q-btn-dropdown
            flat
            content-class="text-dark bg-white "
            dense
            menu-self="top left"
            dropdown-icon="las la-search"
            color="secondary"
            padding="0px"
            size=".8em"
            style="margin-right: 0px;"
          >
            <q-list
              dense
              v-for="func in funcs"
              :key="func.name"
            >
              <q-item
                clickable
                v-close-popup
                @click="addNewPort({ function: func.name, args: func.args }, 'Output', 'las la-search')"
              >
                <q-item-section side>
                  <q-icon name="las la-search" />
                </q-item-section>
                <q-item-section
                  side
                  class="text-blue-grey-8"
                >
                  {{ func.name }}
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Query
          </q-tooltip>
        </div>

        <div
          class="text-secondary"
          style="margin-right: 10px;"
        >
          <!--<i class="outlet-icon" style="cursor: pointer;" />-->

          <q-btn-dropdown
            flat
            content-class="text-dark bg-white "
            dense
            menu-self="top left"
            dropdown-icon="fas fa-bolt"
            color="secondary"
            padding="0px"
            size=".6em"
            style="margin-right: 0px;"
          >
            <q-list
              dense
              v-for="event in events"
              :key="event"
            >
              <q-item
                clickable
                v-close-popup
                @click="addNewPort({ function: event, args: [] }, 'Output', 'fas fa-bolt')"
              >
                <q-item-section side>
                  <q-icon name="fas fa-bolt" />
                </q-item-section>
                <q-item-section
                  side
                  class="text-blue-grey-8"
                >
                  {{ event }}
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Trigger
          </q-tooltip>
        </div>
        <div style="position: absolute; right: 8px; top: 0px;">
          <q-btn
            size="xs"
            icon="las la-exchange-alt"
            dense
            flat
            class="show-code text-secondary"
            style="position: absolute; right: 140px; top: -68px; width: 25px; height: 30px;"
            clickable
            v-close-popup
            @click="showPanel('middlewareview', !middlewareview)"
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Middleware
            </q-tooltip>
          </q-btn>
          <q-btn
            size="xs"
            icon="fas fa-search"
            dense
            flat
            @click="showPanel('codeview', !codeview)"
            class="show-code text-secondary"
            style="position: absolute; right: 115px; top: -68px; width: 25px; height: 30px;"
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Queries
            </q-tooltip>
          </q-btn>
          <q-btn
            size="xs"
            icon="fas fa-table"
            dense
            flat
            @click="showPanel('tableview', !tableview)"
            class="show-code text-secondary"
            style="position: absolute; right: 90px; top: -68px; width: 25px; height: 30px;"
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              View
            </q-tooltip>
          </q-btn>
          <q-btn
            dense
            flat
            size="xs"
            icon="fas fa-terminal"
            @click="showPanel('consoleview', !consoleview)"
            class="edit-name text-secondary"
            style="position: absolute; right: 55px; top: -68px; width: 25px; height: 30px;"
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Console
            </q-tooltip>
          </q-btn>
          <q-btn
            dense
            flat
            size="xs"
            icon="fa fa-cog"
            @click="showPanel('configview', !configview)"
            class="edit-name text-secondary"
            style="position: absolute; right: 30px; top: -68px; width: 25px; height: 30px;"
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
            style="position: absolute; right: 15px; top: -68px; width: 25px; height: 30px;"
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
          style="position: absolute; right: 0px; width: 25px; height: 30px; top: -68px;"
        >
          <q-list dense>
            <q-item
              clickable
              v-close-popup
              @click="showPanel('environmentview', !environmentview)"
            >
              <q-item-section side>
                <q-icon name="far fa-list-alt" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Environment
              </q-item-section>
            </q-item>
            <q-separator />

            <q-item
              clickable
              v-close-popup
              @click="showPanel('notesview', !notesview)"
            >
              <q-item-section side>
                <q-icon name="far fa-sticky-note" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Notes
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="loginProcessor"
            >
              <q-item-section side>
                <q-icon name="fas fa-lock" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Lock
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
              @click="showPanel('middlewareview', !middlewareview)"
            >
              <q-item-section side>
                <q-icon name="las la-exchange-alt" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Middleware
              </q-item-section>
            </q-item>
            <q-separator />
            <q-item
              clickable
              v-close-popup
              @click="showPanel('historyview', !historyview)"
            >
              <q-item-section side>
                <q-icon name="fas fa-history" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                History
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="showPanel('logsview', !logsview)"
            >
              <q-item-section side>
                <q-icon name="fas fa-glasses" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Logs
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
              @click="showPanel('requirementsview', !requirementsview)"
            >
              <q-item-section side>
                <q-icon name="fab fa-python" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Requirements
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
    </div>
    <ul
      class="table-columns"
      v-for="column in obj.columns"
      :key="column.id"
    >
      <li
        :class="'table-column jtk-droppable table-column-type-' + column.datatype"
        :style="'background:' + column.background + ';border-top: 1px dashed lightgrey'"
        :primary-key="column.primaryKey"
        :data-port-id="column.id"
        data-port-template="Object"
      >
        <div class="table-column-edit text-primary">
          <div
            class="table-column-edit text-primary"
            style="max-height: 15px; position: absolute; right: 20px; margin-top: -10px;"
          />
          <q-btn
            icon="fa fa-play"
            size="xs"
            title="Execute Query"
            flat
            dense
            round
            v-if="column.type === 'Output'"
          />
          <i
            class="spinload"
            v-if="column.loading"
            style="font-size:1.3em;margin-right:3px"
          />

          <q-btn
            icon="fa fa-cog"
            size="xs"
            title="Configure Table"
            flat
            dense
            round
            v-if="column.type === 'Table'"
          />
          <q-btn
            icon="fa fa-times"
            size="xs"
            title="Delete Table Port"
            flat
            dense
            round
            @click="confirmDeletePort(column.id)"
            v-if="column.type === 'Table' || column.type === 'Output'"
          />
        </div>
        <div
          v-if="column.type === 'Table' || column.type === 'Output'"
        >
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
            </span>
          </span>
        </div>
        <jtk-source
          v-if="column.type === 'Table' || column.type === 'Output'"
          :port-id="column.id"
          name="source"
          :scope="column.datatype"
          filter=".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon"
          filter-exclude="true"
          type="Output"
        />

        <jtk-target
          v-if="column.type === 'Table'"
          name="target"
          :port-id="column.id"
          type="Table"
          :scope="column.datatype"
        />
      </li>
    </ul>

    <q-separator />
    <div
      class="row"
      id="bandwidth"
      v-if="obj.bandwidth"
    >
      <q-table
        dense
        hide-header
        hide-bottom
        :data="data"
        :columns="columns"
        row-key="name"
        style="width: 100%; border-top-radius: 0px; border-bottom-radius: 0px;"
      >
        <template #body="props">
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
              />
              <v-sparkline
                v-if="props.cols[1].value === 'outBytes'"
                :labels="props.row.spark.labels"
                :value="bytes_out_5min"
                color="white"
                line-width="2"
                padding="0"
              />
              <v-sparkline
                v-if="props.cols[1].value === 'totalBytes'"
                :labels="props.row.spark.labels"
                :value="totalbytes_5min"
                color="white"
                line-width="2"
                padding="0"
              />
              <v-sparkline
                v-if="props.cols[1].value === 'taskTime'"
                :labels="props.row.spark.labels"
                :value="tasktime_out_5min"
                color="white"
                line-width="2"
                padding="0"
              />
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
    <q-dialog
      v-model="deleteItem"
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
            "
          >
            <q-toolbar>
              <q-item-label>Delete Socket</q-item-label>
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
            Are you sure you want to delete this socket?
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
            @click="removeColumn(deletePortID)"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>


    <q-dialog
      v-model="clearDataConfirm"
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
            "
          >
            <q-toolbar>
              <q-item-label>Clear Data</q-item-label>
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
            Are you sure you want to clear the data from this table?
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
            @click="clearData"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>


    <!-- Delete dialog -->
    <q-dialog
      v-model="deleteConfirm"
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
            "
          >
            <q-toolbar>
              <q-item-label>Delete Processor</q-item-label>
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
            Are you sure you want to delete this processor?
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
    <Console
      v-if="pythonview && codeview"
      :codewidth="codewidth"
    />

    <q-card
      :style="
        'width: ' +
          codewidth +
          'px;z-index: 999;display: block;position: absolute;right: -' +
          (codewidth + 5) +
          'px;top: 0px;min-height:600px'
      "
      v-if="tableview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding: 0px !important;padding-bottom: 10px;">
        <q-select
          dense
          :options-dense="true"
          style="font-size: 1em; margin-left:20px; margin-right: 5px;"
          v-model="viewtable"
          :options="tables"
          hint="Database Table"
          option-value="name"
          option-label="name"
          value="string"
          :menu-offset="[5, -9]"
        />
        <div style="padding:20px">
          <q-table
            dense
            flat
            :data="tablerows"
            :columns="viewcols"
            row-key="id"
            :rows-per-page-options="[15]"
            style="height:100%;width: 100%; border-top-radius: 0px; border-bottom-radius: 0px;"
          />
        </div>
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 50px;"
          flat
          icon="far fa-arrow-alt-circle-left"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
          @click="codewidth -= 100"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Shrink
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 50px; width: 50px; margin: 0px;"
          flat
          icon="far fa-arrow-alt-circle-right"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
          @click="codewidth += 100"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Expand
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 100px; width: 50px; margin: 0px;"
          flat
          icon="published_with_changes"
          class="bg-primary text-secondary"
          color="primary"
          v-close-popup
          @click="refreshTables"
          :disable="!viewtable"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Fetch Data
          </q-tooltip>
        </q-btn>

        <q-btn
          style="position: absolute; bottom: 0px; left: 150px; width: 50px; margin: 0px;"
          flat
          icon="fas fa-home"
          class="bg-secondary text-accent"
          color="primary"
          v-close-popup
          @click="setZoomLevel"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Reset Zoom Level
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 200px; width: 50px; margin: 0px;"
          flat
          icon="fas fa-plus"
          class="bg-primary text-accent"
          color="primary"
          v-close-popup
          @click="addRow"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Add Row
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 250px; width: 50px; margin: 0px;"
          flat
          icon="fas fa-trash"
          class="bg-accent text-secondary"
          color="primary"
          v-close-popup
          @click="clearDataConfirm = true"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Clear Data
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
          v-close-popup
          @click="tableview = false"
        />
      </q-card-actions>
      <q-inner-loading
        :showing="saving"
        style="z-index: 999999;"
      >
        <q-spinner-gears
          size="50px"
          color="primary"
        />
      </q-inner-loading>
    </q-card>
    <q-card
      :style="
        'width: ' +
          codewidth +
          'px;z-index: 999;display: block;position: absolute;right: -' +
          (codewidth + 5) +
          'px;top: 0px;'
      "
      v-if="codeview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding: 0px !important;padding-bottom: 10px;">
        <editor
          v-model="obj.code"
          @init="editorInit"
          style="font-size: 16px; min-height: 400px;"
          lang="python"
          theme="chrome"
          ref="myEditor"
          width="100%"
          height="fit"
        />
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 50px;"
          flat
          icon="far fa-arrow-alt-circle-left"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
          @click="codewidth -= 100"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Shrink
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 50px; width: 50px; margin: 0px;"
          flat
          icon="far fa-arrow-alt-circle-right"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
          @click="codewidth += 100"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Expand
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 100px; width: 50px; margin: 0px;"
          flat
          icon="published_with_changes"
          class="bg-primary text-secondary"
          color="primary"
          v-close-popup
          @click="fetchCode"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Fetch Code
          </q-tooltip>
        </q-btn>

        <q-btn
          style="position: absolute; bottom: 0px; left: 150px; width: 50px; margin: 0px;"
          flat
          icon="fas fa-home"
          class="bg-secondary text-accent"
          color="primary"
          v-close-popup
          @click="setZoomLevel"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Reset Zoom Level
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
          v-close-popup
          @click="codeview = false"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="requirementsview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px;">
        <editor
          v-model="obj.requirements"
          @init="reqEditorInit"
          style="font-size: 16px; min-height: 600px;"
          lang="python"
          theme="chrome"
          ref="requirementsEditor"
          width="100%"
          height="fit"
        />
      </q-card-section>

      <q-card-actions
        align="right"
        style="margin-top: 15px;"
      >
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="requirementsview = false"
          v-close-popup
        />
      </q-card-actions>
    </q-card>

    <!-- Git dialog -->
    <q-card
      style="
        width: 950px;
        z-index: 999;
        display: block;
        position: absolute;
        right: -955px;
        top: 0px;
        height: 800px;
        padding-bottom: 35px;
      "
      v-if="gitview"
    >
      <q-card-section style="height: 100%;">
        <q-splitter
          v-model="codeSplitterModel"
          separator-style="background-color: #e3e8ec;height:5px"
          horizontal
          style="height: 100%;"
        >
          <template #before>
            <div class="q-pa-md">
              <q-table
                dense
                :columns="gitcolumns"
                :data="gitdata"
                row-key="name"
                flat
                :rows-per-page-options="[10]"
                style="height: calc(100% - 0px); width: 100%; border-top-radius: 0px; border-bottom-radius: 0px;"
              >
                <template #body="props">
                  <q-tr
                    :props="props"
                    :key="getUuid"
                  >
                    <q-td
                      :key="props.cols[0].name"
                      :props="props"
                    >
                      <a
                        href="#"
                        style="color: #6b8791; text-decoration: underline;"
                        @click="showCommit(props.cols[0].value, props.cols[3].value)"
                      >
                        {{ props.cols[0].value }}
                      </a>
                    </q-td>
                    <q-td
                      :key="props.cols[1].name"
                      :props="props"
                    >
                      {{ props.cols[1].value }}
                    </q-td>
                    <q-td
                      :key="props.cols[2].name"
                      :props="props"
                    >
                      {{ props.cols[2].value }}
                    </q-td>
                    <q-td
                      :key="props.cols[3].name"
                      :props="props"
                    >
                      {{ props.cols[3].value }}
                    </q-td>
                  </q-tr>
                </template>
                <template #loading>
                  <q-inner-loading
                    :showing="true"
                    style="z-index: 9999999;"
                  >
                    <q-spinner-gears
                      size="50px"
                      color="primary"
                    />
                  </q-inner-loading>
                </template>
              </q-table>
            </div>
          </template>

          <template #after>
            <div
              class="q-pa-md"
              style="height: 100%; padding: 0px;"
            >
              <editor
                v-model="commitcode"
                @init="gitEditorInit"
                style="font-size: 1.5em;"
                lang="python"
                theme="chrome"
                ref="gitEditor"
                width="100%"
                height="100%"
              />
            </div>
          </template>
        </q-splitter>
      </q-card-section>
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; padding-top: 10px;" />
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          icon="refresh"
          class="bg-primary text-white"
          color="primary"
          @click="getCommits"
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
      <q-item-label style="position: absolute; left: 120px; bottom: 5px; font-size: 1.5em;">
        {{ gitcommit }}
        <span style="margin-right: 40px;" />
        {{ gitdate }}
      </q-item-label>
      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="gitview = false"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="width: 400px; z-index: 999; display: block; position: absolute; right: -405px; height: 400px; top: 0px;"
      v-if="editPort"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 650px;" />

      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="closePortEdit()"
        />
      </q-card-actions>
    </q-card>

    <!-- Config dialog -->

    <q-card
      style="width: 650px; height:580px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="configview"
    >
      <q-item-label style="position:absolute;z-index:99999;float:left;bottom:10px;left:25px">
        {{ schemaResult }}
      </q-item-label>
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 500px;">
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
          <q-tab
            name="settings"
            label="Settings"
          />
          <q-tab
            name="schemaconfig"
            label="Schema"
          />
          <q-tab
            name="containersettings"
            label="Container"
          />
          <q-tab
            name="schedule"
            label="Schedule"
          />
        </q-tabs>

        <q-tab-panels
          v-model="tab"
          keep-alive
        >
          <q-tab-panel
            ref="schemaconfig"
            name="schemaconfig"
            style="padding: 0px;height:480px"
          >
            <div
              class="q-pa-md"
              style="max-width: 100%; padding-bottom: 0px; min-height: 425px;"
            >
              <editor
                v-model="obj.schema"
                @init="schemaEditorInit"
                style="font-size: 1.5em; min-height: 420px;"
                lang="sql"
                theme="chrome"
                ref="schemaEditor"
                width="100%"
                height="100%"
              />
            </div>
            <q-card-actions align="left">
              <q-btn
                style="position: absolute; bottom: 0px; left: 20px; width: 100px;"
                flat
                label="Create"
                class="bg-primary text-dark"
                color="dark"
                @click="createSchema"
              >
                <q-tooltip
                  anchor="top middle"
                  :offset="[-30, 40]"
                  content-style="font-size: 16px"
                  content-class="bg-black text-white"
                >
                  Create Schema
                </q-tooltip>
              </q-btn>
              <q-btn
                style="position: absolute; bottom: 0px; left: 120px; width: 100px;"
                flat
                label="Pull"
                class="bg-primary text-dark"
                color="dark"
                @click="pullSchema"
              >
                <q-tooltip
                  anchor="top middle"
                  :offset="[-30, 40]"
                  content-style="font-size: 16px"
                  content-class="bg-black text-white"
                >
                  Pull Schema
                </q-tooltip>
              </q-btn>
            </q-card-actions>
          </q-tab-panel>
          <q-tab-panel
            ref="settings"
            name="settings"
            style="padding: 0px;height:500px"
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
                  hint="Database Name"
                  lazy-rules
                  :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                />

                <q-input
                  filled
                  v-model="obj.description"
                  dense
                  hint="Database Description"
                  lazy-rules
                  :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                />
                <q-select
                  dense
                  borderless
                  :options-dense="true"
                  style="font-size: 1em; margin-left:20px; margin-right: 5px;"
                  v-model="obj.database"
                  :options="databases"
                  hint="Database Type"
                  value="string"
                  :menu-offset="[5, -9]"
                />
                <q-input
                  filled
                  v-model="obj.connection"
                  dense
                  hint="Connection String"
                  lazy-rules
                  :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                />
                <q-select
                  filled
                  dense
                  v-model="obj.middlewarefunc"
                  use-input
                  input-debounce="0"
                  :options="getfuncs"
                  hint="Middleware Function"
                  style="width: 250px"
                />
                <q-toolbar style="margin-left: -30px;">
                  <q-space />
                  <q-checkbox
                    v-model="obj.usemiddleware"
                    label="Use Middleware"
                    style="margin-left: 40px;"
                  />
                  <q-checkbox
                    v-model="obj.middlewareonly"
                    label="Middleware Only"
                    style="margin-left: 40px;"
                  />
                  <q-checkbox
                    v-model="obj.titletab"
                    label="Title Tab"
                    style="margin-left: 40px;"
                  />
                  <q-checkbox
                    v-model="obj.enabled"
                    label="Enabled"
                    style="margin-left: 40px;"
                  />
                </q-toolbar>
              </q-form>
            </div>

            <q-card-actions align="left">
              <q-btn
                style="position: absolute; bottom: 0px; left: 20px; width: 100px;"
                flat
                label="Test"
                class="bg-primary text-dark"
                color="dark"
                @click="testConnection"
              >
                <q-tooltip
                  anchor="top middle"
                  :offset="[-30, 40]"
                  content-style="font-size: 16px"
                  content-class="bg-black text-white"
                >
                  Test Connection
                </q-tooltip>
              </q-btn>
            </q-card-actions>
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
                  v-model="obj.imagerepo"
                  dense
                  hint="Image Repository"
                  lazy-rules
                  :disable="!hasHosted"
                />
                <q-input
                  filled
                  v-model="obj.containerimage"
                  dense
                  hint="Container Image"
                  lazy-rules
                  :disable="!hasHosted"
                />
                <q-select
                  filled
                  dense
                  v-model="obj.containerimage"
                  use-input
                  input-debounce="0"
                  hint="Prebuilt Images"
                  :options="containers"
                  style="width: 250px"
                />
              </q-form>
              <q-toolbar>
                <q-checkbox
                  v-model="obj.container"
                  label="Containerized"
                  :disable="!hasHosted"
                />
                <q-space />
                <q-btn
                  flat
                  label="Advanced"
                  class="text-white bg-primary text-primary"
                  :disable="!hasHosted"
                />
              </q-toolbar>
            </div>
          </q-tab-panel>
          <q-tab-panel
            name="schedule"
            style="padding: 20px;"
            ref="schedule"
          >
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
              v-model="crontoggle"
              style="margin-top: 30px;"
              label="Use CRON"
            />
          </q-tab-panel>
          <q-tab-panel
            name="security"
            style="padding: 20px;"
            ref="security"
          />
          <q-tab-panel
            name="scaling"
            style="padding: 20px;"
            ref="scaling"
          />
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
      <q-inner-loading
        :showing="saving"
        style="z-index: 999999;"
      >
        <q-spinner-gears
          size="50px"
          color="primary"
        />
      </q-inner-loading>
    </q-card>

    <q-card
      style="width: 100%; width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="environmentview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 400px;">
        <q-table
          dense
          :columns="variablecolumns"
          :data="variabledata"
          row-key="name"
          flat
          style="width: 100%; margin-top: 20px; border-top-radius: 0px; border-bottom-radius: 0px;"
        >
          <template #body="props">
            <q-tr
              :props="props"
              :key="getUuid"
            >
              <q-td
                :key="props.cols[0].name"
                :props="props"
              >
                <a class="text-secondary">{{ props.row.name }}</a>
                <q-popup-edit
                  v-model="props.row.name"
                  v-slot="scope"
                  buttons
                >
                  <q-input
                    v-model="props.row.name"
                    dense
                    autofocus
                    counter
                  />
                </q-popup-edit>
              </q-td>
              <q-td
                :key="props.cols[1].name"
                :props="props"
              >
                <a class="text-secondary">{{ props.row.value }}</a>
                <q-popup-edit
                  v-model="props.row.value"
                  v-slot="scope"
                  buttons
                >
                  <q-input
                    v-model="props.row.value"
                    dense
                    autofocus
                    counter
                  />
                </q-popup-edit>
              </q-td>
              <q-td
                :key="props.cols[2].name"
                :props="props"
              >
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
          @click="environmentview = false"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="width: 100%; width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="scalingview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 400px;">
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
          @click="removeColumn(deletePortID)"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px; height: 450px;"
      v-if="historyview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 400px;">
        <q-table
          dense
          :columns="historycolumns"
          :data="myhistory"
          row-key="name"
          flat
          style="width: 100%; height: 100%; margin-top: 20px; border-top-radius: 0px; border-bottom-radius: 0px;"
        >
          <template #body="props">
            <q-tr
              :props="props"
              :key="getUuid"
            >
              <q-td
                :key="props.cols[0].name"
                :props="props"
              >
                {{ props.row.constructor.name }}
              </q-td>
              <q-td
                :key="props.cols[1].name"
                :props="props"
              >
                {{ props.row.obj.data.name }}
              </q-td>
              <q-td
                :key="props.cols[2].name"
                :props="props"
              >
                {{ props.row.obj.data.id }}
              </q-td>
              <q-td key="owner">
                {{ owner }}
              </q-td>
            </q-tr>
          </template>
        </q-table>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          flat
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="historyview = false"
          v-close-popup
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="width: 100%; width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="consoleview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 520px;">
        <q-scroll-area
          style="height:475px;width:auto"
          ref="scroll"
        >
          <div v-for="(log, index) in consolelogs">
            <div v-if="consolehistory">
              <pre style="font-weight: bold;">{{ log["date"] }}</pre>
              <pre>{{ log["output"] }}</pre>
            </div>
            <vue-typed-js
              v-if="!consolehistory && index === consolelogs.length - 1"
              :show-cursor="false"
              :type-speed="1"
              :strings="[
                '<b>' +
                  consolelogs[consolelogs.length - 1]['date'] +
                  '</b><br><br>' +
                  consolelogs[consolelogs.length - 1]['output'],
              ]"
              :content-type="'html'"
            >
              <pre class="typing" />
            </vue-typed-js>
          </div>
        </q-scroll-area>
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          label="Clear"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
          @click="consolelogs = []"
        />
        <q-btn
          flat
          style="position: absolute; margin: 0px; bottom: 0px; left: 100px; width: 100px;"
          label="Download"
          class="bg-secondary text-white"
          color="primary"
          v-close-popup
          @click="consolelogs = []"
        />
        <q-checkbox
          v-model="consolehistory"
          label="History"
          style="position: absolute; bottom: 0px; left: 210px;"
        />
      </q-card-actions>
      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="consoleview = false"
        />
      </q-card-actions>
    </q-card>

    <q-card
      v-if="mousecard"
      class="bg-secondary"
      :style="'width:200px;height:300px;z-index:9999;position:absolute;top:' + cardY + 'px;left:' + cardX + 'px'"
    />
    <q-card
      style="width: 650px; height: 465px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="notesview"
    >
      <q-card-section style="height: 430px; padding: 5px; z-index: 999999; padding-bottom: 10px;">
        <div style="height: 100%; width: 100%;">
          <editor
            v-model="obj.notes"
            @init="notesEditorInit"
            style="font-size: 1.5em;"
            lang="text"
            theme="chrome"
            ref="notesEditor"
            width="100%"
            height="100%"
          />
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="notesview = false"
          v-close-popup
        />
      </q-card-actions>
    </q-card>

    <q-card
      :style="'width: '+middlewarewidth+'px; height: 465px; z-index: 999; display: block; position: absolute; right: -' +
        (middlewarewidth + 5) +
        'px; top: 0px;'"
      v-if="middlewareview"
    >
      <q-card-section style="height: 430px; padding: 5px; z-index: 999999; padding-bottom: 10px;">
        <div style="height: 100%; width: 100%;">
          <editor
            v-model="middleware"
            @init="middlewareEditorInit"
            style="font-size: 1.5em;"
            lang="python"
            theme="chrome"
            ref="middlewareEditor"
            width="100%"
            height="100%"
          />
        </div>
      </q-card-section>

      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 50px;"
          flat
          icon="far fa-arrow-alt-circle-left"
          class="bg-primary text-white"
          color="primary"
          v-close-popup
          @click="middlewarewidth -= 100"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Shrink
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 50px; width: 50px; margin: 0px;"
          flat
          icon="far fa-arrow-alt-circle-right"
          class="bg-accent text-dark"
          color="primary"
          v-close-popup
          @click="middlewarewidth += 100"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Expand
          </q-tooltip>
        </q-btn>
        <q-btn
          style="position: absolute; bottom: 0px; left: 150px; width: 50px; margin: 0px;"
          flat
          icon="fas fa-home"
          class="bg-secondary text-accent"
          color="primary"
          v-close-popup
          @click="setZoomLevel"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Reset Zoom Level
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
          @click="middlewareview = false"
          v-close-popup
        />
      </q-card-actions>
    </q-card>
    <q-card
      style="width: 100%; width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="securityview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 400px;">
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
          @click="removeColumn(deletePortID)"
        />
      </q-card-actions>
    </q-card>

    <q-card
      style="width: 100%; width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="logsview"
    >
      <q-tabs
        v-model="logtab"
        class="text-primary"
        align="center"
        dense
      >
        <q-tab
          name="tasklog"
          label="Task"
        />
        <q-tab
          name="resultlog"
          label="Result"
        />
        <q-tab
          name="msglog"
          label="Log"
        />
      </q-tabs>
      <q-tab-panels
        v-model="logtab"
        keep-alive
      >
        <q-tab-panel
          name="tasklog"
          style="padding: 0px;"
          ref="tasklog"
        >
          <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 450px;">
            <q-scroll-area style="height:425px;width:auto">
              <div v-for="log in tasklogs">
                {{ log["date"] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{ log["state"] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{
                  log["module"]
                }}&nbsp;&nbsp; --&nbsp;&nbsp;{{ log["task"] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{ log["duration"] }}
              </div>
            </q-scroll-area>
          </q-card-section>
        </q-tab-panel>
        <q-tab-panel
          name="resultlog"
          style="padding: 0px;"
          ref="tasklog"
        >
          <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 450px;">
            <q-scroll-area style="height:425px;width:auto">
              <div v-for="log in resultlogs">
                {{ log["date"] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{ log["module"] }}&nbsp;&nbsp; --&nbsp;&nbsp;{{
                  log["task"]
                }}
                {{ JSON.parse(log["message"]) }}
              </div>
            </q-scroll-area>
          </q-card-section>
        </q-tab-panel>
        <q-tab-panel
          name="msglog"
          style="padding: 0px;"
          ref="msglog"
        >
          <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 450px;">
            <q-scroll-area style="height:425px;width:auto">
              <div v-for="log in msglogs">
                {{ log["date"] }}&nbsp;&nbsp; --&nbsp;&nbsp;&nbsp;
                {{ log["message"] }}
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
      style="width: 100%; width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="dataview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 400px;">
        <div id="chart">
          <apexchart
            type="line"
            height="390"
            :options="chartOptions"
            :series="series"
            ref="bandwidthChart"
          />
        </div>
      </q-card-section>
      <q-card-actions align="left" />
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
<style scoped>

.spinload {
    width: 12px;
    height: 12px;
    border: 2px solid #abbcc3;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
    }

    @keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
    }

.q-expansion-item__container > .q-item {
  padding-left: 0px !important;
  padding-right: 0px !important;
}

.q-expansion-item__content {
  padding-left: 20px !important;
}

.q-item--dense {
  margin-right: 0px;
  padding-left: 0px;
}
.table-columns .q-item__section {
  padding-right: 5px;
}
.parentBox {
  padding: 0px;
  margin-left: 5px;
  margin-right: 5px;
}

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
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { BaseNodeComponent } from 'jsplumbtoolkit-vue2'
import { v4 as uuidv4 } from 'uuid'
import Vuetify from 'vuetify'
import { mdiLambda, mdiAbacus, mdiPowerSocketUs, mdiCodeBraces } from '@mdi/js'
import { ref } from 'vue'
import { TSDB } from 'uts'
import Console from 'components/Console'
import Processor from '../Processor.vue'
import BetterCounter from '../BetterCounter'
import DataService from 'components/util/DataService'

import http from 'src/http-common'

var Moment = require('moment') // require

const tsdb = new TSDB()

// use mixins to mix in methods, data, store for 'Processor' objects.
// The template thus defers to the mixed in methods for its state
// The Processor object mixin connects to the vuex store and websocket detail, and api as well.
// This template simply acts as an input/output layer to t3he mixed in component
// The mixed in component data fields are fully reactive in this Vue template because it's
// mixed in.

/*
Context menu

Configure
Stop
View Status History - Show list of logs with change in status
View State - Any persistent state/env variables set by the processor
View Usage - Docs
View Connections - Table showing source and target plugs
Center in View
Change Color
Group
Copy
Delete

*/
export default {
  name: 'DatabaseTemplate',
  mixins: [BaseNodeComponent, BetterCounter, Processor], // Mixin the components
  vuetify: new Vuetify(),
  setup () {
    // expose to template and other options API hooks
    return {
    }
  },
  components: {
    editor: require('vue2-ace-editor'),
    BetterCounter,
    Console
  },
  watch: {
    'obj.middlewarefunc': function (val) {
      this.middlewarefunc = val
      console.log('SET MIDDLEWARE FUNC', val)
    },
    'obj.usemiddleware': function (val) {
      this.usemiddleware = val
    },
    'obj.middlewareonly': function (val) {
      this.middlewareonly = val
    },
    'obj.cron': function (val) {
      if (val && obj.crontoggle) {
        this.startSchedule(val)
      }
    },
    'obj.status': function (val) {
      window.designer.$root.$emit('toolkit.dirty')
    },
    inBytes: function (val) {
      // console.log('inBytes', val);
    }
  },
  created () {
    let me = this

    this.plugIcon = mdiPowerSocketUs
    this.braces = mdiCodeBraces
    this.lambdaIcon = mdiLambda
    this.abacusIcon = mdiAbacus
    this.obj.usemiddleware = true
    this.obj.middlewareonly = true
    this.usemiddleware = true

    this.id = uuidv4()
    console.log('THIS.ID', this.id)

    console.log('me.tooltips ', me.tooltips)
    console.log('start listening for show.tooltips')
    this.braces = mdiCodeBraces

    window.root.$on('show.tooltips', (value) => {
      console.log('start tooltips:', value)
      me.tooltips = value
      console.log('ME:', me)
      console.log('TOOLTIPS', me.tooltips)
    })

    const avoid = ['icon', 'id']
    window.designer.$on('trigger.data', () => {
      // In this case, the Run Flow button was pressed and
      // Queries added to this database template should be fired
    })
    this.$on('call.completed', (call) => {
      // TODO: Refresh data tables
      this.refreshTables()
      // TODO: Trigger sequential ports that are satisfied
      for (const fname in this.portobjects) {
        console.log('SEQUENCE FUNC', fname)
      }
    })
    this.$on('middleware.complete', (msg) => {
      console.log('DATABASE TEMPLATE: ', msg)
      const bytes = msg.bytes
      me.calls_in += 1
      me.bytes_in_5min.unshift(bytes) // + (Math.random()*100)
      // console.log('BYTE_IN_5MIN', me.bytes_in_5min);
      me.bytes_in_5min = me.bytes_in_5min.slice(0, 8)
      // console.log('BYTE_IN_5MIN SLICED', me.bytes_in_5min.slice(0, 8));
      me.bytes_in += bytes
      setTimeout(me.refreshTables,1000)
/*
      this.obj.columns.forEach((column) => {
        if (column.id === msg.portname) {
          if (column.loaders) {
            column.loaders.pop()
          }
          if (column.loaders.length === 0) {
            column.loading = false
          }
          // Trigger the port AFTER a result has been emitted
          console.log('TRIGGER PORT LOADING:', column)
          this.triggerObject(msg.portname, column, (_column) => {
            console.log('TRIGGER PORT CALLBACK', _column)
          })
        }
      })
*/
      this.$forceUpdate()
    })

    this.$on('middleware.started', (msg) => {
      // When middleware has been started, show
      // the spinner icon
      this.obj.columns.forEach((column) => {
        if (column.id === msg.portname) {
          column.loading = true

          if (!column.loaders) {
            column.loaders = []
          }
          column.loaders.push({})
        }
      })
      setTimeout(me.$forceUpdate)
    })

    this.$on('message.received', (msg) => {
      if (msg.type && msg.type === 'result') {
        this.obj.columns.forEach((column) => {
          if (column.id === msg.portname) {
            if (column.loaders) {
              column.loaders.pop()
            }
            if (column.loaders.length === 0) {
                column.loading = false
            }
            this.$forceUpdate()
            // Trigger the port AFTER a result has been emitted
            console.log('TRIGGER PORT LOADING:', column)
            this.triggerObject(msg.portname, column, msg.obj,(_column) => {
            })
          }
        })
        if (msg.id === this.obj.id) {
          me.currentresult = msg.output
          me.consolelogs.push({ date: new Date(), output: msg.output })
        }
      }

      if (msg.type && msg.type === 'ProcessorModel') {
        if (msg.name === me.obj.name) {
          if (msg.object.receipt > me.obj.receipt) {
            console.log('SCRIPTPROCESSOR: I was updated in DB!', msg)
            for (var key in me.obj) {
              if (key in msg.object && !avoid.includes(key)) {
                me.obj[key] = msg.object[key]
              }
            }
          } else {
            console.log('Ignoring update since receipt is obsolete', msg.object, me.obj)
          }
          console.log('PROCESSOR ID', me.obj.id)
        }
      }

      if (msg.type && msg.type === 'trigger') {
        me.triggerExecute()
      }

      if (msg.type && msg.type === 'output') {
        if (msg.processor === this.obj.name) {
          me.consolelogs.push({ date: new Date(), output: msg.output })
          me.consolelogs = me.consolelogs.slice(0, 100)
        }
      }

      if (msg.room && msg.room !== me.obj.name) {
        return
      }

      if (msg.channel === 'task' && msg.state) {
        var bytes = JSON.stringify(msg).length
        window.root.$emit('message.count', 1)
        window.root.$emit('message.size', bytes)
        tsdb.series('inBytes').insert(
          {
            bytes: bytes
          },
          Date.now()
        )

        var timedata = tsdb.series('inBytes').query({
          metrics: { data: TSDB.map('bytes'), time: TSDB.map('time') },
          where: {
            time: { is: '<', than: Date.now() - 5 * 60 }
          }
        })

        // me.bytes_in_5min = averaged_data
        me.bytes_in_5min.unshift(bytes) // + (Math.random()*100)
        // console.log('BYTE_IN_5MIN', me.bytes_in_5min);
        me.bytes_in_5min = me.bytes_in_5min.slice(0, 8)
        // console.log('BYTE_IN_5MIN SLICED', me.bytes_in_5min.slice(0, 8));
        me.bytes_in += bytes

        me.calls_in = timedata[0].results.data.length
        me.tasklogs.unshift(msg)
        me.tasklogs = me.tasklogs.slice(0, 100)
      }
      if (msg.channel === 'task' && msg.message) {
        const now = Date.now()
        var timedata = tsdb.series('outBytes').query({
          metrics: { data: TSDB.map('bytes'), time: TSDB.map('time') },
          where: {
            time: { is: '<', than: Date.now() - 5 * 60 }
          }
        })
        console.log('TIMEDATA', timedata)
        tsdb.series('outBytes').insert(
          {
            bytes: bytes
          },
          now
        )
        var json = JSON.parse(msg.message)
        me.bytes_out += msg.message.length
        me.bytes_out_5min.unshift(msg.message.length)
        if (msg.state === 'postrun' && msg.duration) {
          const moment = Moment(msg.duration, 'H:mm:ss.SSS')
          // console.log('MOMENT', moment);
          me.tasktime_out_5min.unshift(moment.seconds() + moment.milliseconds())
          me.tasktime_out_5min = me.tasktime_out_5min.slice(0, 8)

          me.task_time = json.duration

          tsdb.series('durations').insert(
            {
              duration: moment,
              seconds: moment.seconds(),
              milliseconds: moment.milliseconds()
            },
            now
          )
        }
        // console.log('TASKTIME_OUT_5MIN', me.tasktime_out_5min);
        me.bytes_out_5min = me.bytes_out_5min.slice(0, 8)
        me.calls_out = timedata[0].results.data.length
        me.resultlogs.unshift(json)
        me.resultlogs = me.resultlogs.slice(0, 100)
      }
      if (msg.channel === 'log' && msg.message) {
        me.msglogs.unshift(msg)
        me.msglogs = me.msglogs.slice(0, 100)
      }
      me.totalbytes_5min.unshift(me.bytes_in + me.bytes_out)
      me.totalbytes_5min = me.totalbytes_5min.slice(0, 8)
      // console.log('TASKLOGS', me.tasklogs);
      // console.log('MSGLOGS', me.msglogs);
      if (msg.channel === 'task') {
        this.updateBandwidthChart()
      }
    })
    // Print some fields from the mixin component
    console.log('BetterCounter: ', this.delayMs, this.internalPerformAsyncIncrement)
    console.log('getcount', this.countLabel)
    // Changing this.delayMs will cause it to be saved in the vuex store and sync'd with server.
    // Any changes to the server will arrive through the customer Store via websockets, update the
    // vuex model and cause any reactive components in this view to change as well.
    setTimeout(() => {
      me.delayMs = 500 // Update the reactive mixin data field
      me.internalPerformAsyncIncrement()
      me.delayMs += 10
      me.count += 10
      // me.name = 'MyProcessor 2!';
    }, 3000)
  },
  computed: {
    getfuncs () {
      this.updateFunctions(this.obj.middleware)
      console.log('GETFUNCS', this.funcs)
      return this.funcs.map(a => a.name)
    },
    viewtable: {
      get: function () {
        return this.table.name
      },
      set: function (val) {
        console.log('SETTING VIEW TABLE', val)
        this.tablerows = []
        this.viewcols = []
        this.table = val
        val.cols.forEach((col) => {
          this.viewcols.push({
            name: col,
            label: col,
            field: col
          })
        })
        this.refreshTables()
      }
    },
    crontoggle: {
      get: function () {
        return this.obj.useschedule
      },
      set: function (val) {
        this.obj.useschedule = val
        if (val) {
          this.startSchedule(this.obj.cron)
        } else {
          this.stopSchedule()
        }
      }
    },
    myhistory () {
      let me = this

      var myhist = []
      window.toolkit.undoredo.undoStack.forEach((entry) => {
        if (entry.obj.data.id === me.obj.id) {
          myhist.push(entry)
        }
      })

      return myhist
    },
    rateLimit (val) {
    },
    taskTime () {
      return this.task_time
    },
    inBytes () {
      return this.calls_in + ' (' + this.bytes_in_human + ' bytes)'
    },
    outBytes () {
      return this.calls_out + ' (' + this.bytes_out_human + ' bytes)'
    },
    totalBytes () {
      return this.calls_out + this.calls_in + ' (' + this.sizeOf(this.bytes_out + this.bytes_in) + ' bytes)'
    },
    bytes_in_human () {
      return this.sizeOf(this.bytes_in)
    },
    bytes_out_human () {
      return this.sizeOf(this.bytes_out)
    },
    readwrite () {
      return this.obj.readwrite
    }
  },
  mounted () {
    let me = this

    console.log('setId ', this.obj.id)
    this.setId(this.obj.id)

    console.log('SETTING PROCESSOR ID', this.id)
    console.log('MOUNTED STORE', this.$store)
    console.log('BYTES_IN', this.bytes_in)

    me.middleware = me.obj.middleware
    me.middlewarefunc = me.obj.middlewarefunc

    d3.selectAll('p').style('color', 'white')
    console.log('D3 ran')
    // Execute method on mixed in component, which sends to server using socket.io
    this.sayHello({ name: 'darren', age: 51 })

    setTimeout(() => {
      console.log('ME.getNode()', me.getNode())
      me.getNode().component = this
    }, 3000)
    this.$el.component = this
    window.designer.$on('toggle.bandwidth', (bandwidth) => {
      console.log('toggle bandwidth', bandwidth)
      me.obj.bandwidth = bandwidth
    })
    window.designer.$root.$on('node.added', (node) => {
      console.log('NODE ADDED', node)
      this.updateSchemas()
    })
    window.designer.$root.$on(this.obj.id, (action) => {
      if (action === 'configure') {
        this.configview = !this.configview
      }
    })
    window.designer.$root.$on('toolkit.dirty', (val) => {
      this.updateSchemas()
    })
    window.root.$on('update.queues', (queues) => {
      this.queues = queues.map((queue) => queue.name)
    })
    window.designer.$root.$emit('toolkit.dirty')
    this.deployLoading = true
    this.fetchCode()
    this.updateBandwidthChart()
    this.updatePorts()
    if (this.obj.crontoggle) {
      this.startSchedule(this.obj.cron)
    }
    this.pullSchema()
  },
  data () {
    return {
      clearDataConfirm: false,
      fetchDisabled: true,
      schemaResult: 'Ready',
      viewcols: [],
      tables: [],
      table: '',
      tablerows: [],
      connectResult: '',
      events: ['Begin', 'Error', 'Complete'],
      databases: ['SQLite', 'MySQL', 'Postgres', 'Oracle'],
      resulttype: 'finished',
      queues: [],
      argports: {},
      portobjects: {},
      funcs: [],
      afuncs: [],
      codewidth: 650,
      middlewarewidth: 875,
      queuecolumns: [
        {
          name: 'task',
          label: 'Task',
          field: 'task',
          align: 'left'
        },
        {
          name: 'tracking',
          label: 'Tracking',
          field: 'tracking',
          align: 'left'
        },
        {
          name: 'id',
          label: 'ID',
          field: 'id',
          align: 'left'
        },
        {
          name: 'time',
          label: 'Time',
          field: 'time',
          align: 'left'
        },
        {
          name: 'parent',
          label: 'Parent',
          field: 'parent',
          align: 'left'
        },
        {
          name: 'routing_key',
          label: 'Routing Key',
          field: 'routing_key',
          align: 'left'
        }
      ],
      resultdata: [],
      commitcode: '',
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
      owner: 'darren',
      historycolumns: [
        {
          name: 'action',
          label: 'Action',
          field: 'name',
          align: 'left'
        },
        {
          name: 'object',
          label: 'Object',
          field: 'object',
          align: 'left'
        },
        {
          name: 'id',
          label: 'Object ID',
          field: 'id',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          align: 'left'
        }
      ],
      resultdataloading: false,
      resultloading: false,
      resultcolumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'id',
          label: 'Result',
          field: 'id',
          align: 'left'
        },

        {
          name: 'id',
          label: 'Output',
          field: 'id',
          align: 'left'
        },
        {
          name: 'created',
          label: 'Created',
          field: 'created',
          align: 'left'
        },
        {
          name: 'state',
          label: 'State',
          field: 'state',
          align: 'left'
        },
        {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        },
        {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        },
        {
          name: 'tracking',
          label: 'Tracking',
          field: 'tracking',
          align: 'left'
        },
        {
          name: 'task_id',
          label: 'Task ID',
          field: 'task_id',
          align: 'left'
        }
      ],
      resultPagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 20
      },
      queuePagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 20
      },
      viewResultsDialog: false,
      resultSplitter: 50,
      messageSplitter: 70,
      types: [],
      deployLoading: false,
      errorMsg: '',
      password: '',
      tasktime_out_5min: [0, 0, 0, 0, 0, 0, 0, 0],
      totalbytes_5min: [0, 0, 0, 0, 0, 0, 0, 0],
      bytes_in_5min: [0, 0, 0, 0, 0, 0, 0, 0],
      bytes_out_5min: [0, 0, 0, 0, 0, 0, 0, 0],
      bytes_in: 0,
      bytes_out: 0,
      calls_in: 0,
      calls_out: 0,
      task_time: 0,
      login: false,
      logtab: 'tasklog',
      cardX: 0,
      cardY: 0,
      mousecard: false,
      tab: 'settings',
      error: false,
      tasklogs: [],
      resultlogs: [],
      msglogs: [],
      consolelogs: [],
      editPort: false,
      settingstab: 'settings',
      refreshing: false,
      consolehistory: false,
      saving: false,
      splitterModel: 50,
      codeSplitterModel: 50,
      series: [],
      chartOptions: {
        colors: ['#abbcc3', '#6b8791', '#465d6f', '#054848'],
        chart: {
          height: 350,
          type: 'line',
          zoom: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          width: [2, 3, 2],
          curve: 'straight',
          dashArray: [0, 8, 5]
        },
        title: {
          text: 'Processor Bandwidth',
          align: 'left'
        },
        legend: {
          tooltipHoverFormatter: function (val, opts) {
            return val + ' - ' + opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] + ''
          }
        },
        markers: {
          size: 0,
          hover: {
            sizeOffset: 6
          }
        },
        xaxis: {
          type: 'category',
          tickAmount: 6,
          categories: []
        },
        tooltip: {
          y: [
            {
              title: {
                formatter: function (val) {
                  return val
                }
              }
            },
            {
              title: {
                formatter: function (val) {
                  return val
                }
              }
            },
            {
              title: {
                formatter: function (val) {
                  return val
                }
              }
            }
          ]
        },
        grid: {
          borderColor: '#f1f1f1'
        }
      },
      obj: {
        // Will come from mixed in Script object (vuex state, etc)
        icon: 'fas fa-database',
        titletab: false,
        schema: '',
        data: [],
        usemiddleware: false,
        middlewareonly: false,
        middlewarefunc: '',
        database: 'SQLite',
        receipt: new Date(),
        notes: '',
        style: '',
        x: 0,
        y: 0,
        middleware: '# object middleware',
        connection: 'sqlite://elasticdb',
        version: 'v1.2.2',
        perworker: true,
        ratelimit: '60',
        websocket: 'ws://localhost:3003',
        bandwidth: true,
        requirements: '',
        gittag: '',
        container: true,
        imagerepo: 'local',
        containerimage: 'pyfi/processor:latest',
        environment: '',
        usegit: true,
        enabled: true,
        endpoint: false,
        beat: false,
        streaming: true,
        api: '/api/processor',
        type: 'script',
        name: 'Data Processor',
        label: 'Data',
        description: 'A data processor description',
        package: 'my.python.package',
        concurrency: 3,
        cron: '* * * * *',
        interval: -1,
        useschedule: false,
        disabled: false,
        commit: '',
        gitrepo:
          'https://github.com/radiantone/pyfi-processors#egg=ext-processor',
        columns: [],
        modulepath: 'ext/processors/queries.py',
        readwrite: 0,
        status: 'stopped',
        properties: []
      },
      text: '',
      configview: false,
      historyview: false,
      consoleview: false,
      logsview: false,
      requirementsview: false,
      notesview: false,
      middlewareview: false,
      securityview: false,
      environmentview: false,
      scalingview: false,
      dataview: false,
      deletePortID: null,
      sidecode: true,
      bandwidth: true,
      deploydata: [
        {
          name: 'Name1',
          owner: 'postgres',
          hostname: 'agent2',
          processor: 'proc1',
          cpus: 5,
          status: 'running'
        }
      ],
      gitdata: [],
      gitcommit: '',
      gitcolumns: [
        {
          name: 'hash',
          label: 'Hash',
          field: 'hash',
          align: 'left'
        },
        {
          name: 'author',
          label: 'Author',
          field: 'author',
          align: 'left'
        },
        {
          name: 'message',
          label: 'Message',
          field: 'message',
          align: 'left'
        },
        {
          name: 'date',
          label: 'Date',
          field: 'date',
          align: 'left'
        }
      ],
      deploycolumns: [
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
          name: 'hostname',
          label: 'Hostname',
          field: 'hostname',
          align: 'left'
        },
        {
          name: 'worker',
          label: 'Worker',
          field: 'worker',
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
      columns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'bytes',
          align: 'center',
          label: 'Bytes',
          field: 'bytes'
        },
        {
          name: 'time',
          align: 'right',
          classes: 'text-secondary',
          label: 'Time',
          field: 'time'
        },
        {
          name: 'spark',
          align: 'center',
          classes: 'text-secondary',
          label: 'Spark',
          field: 'spark'
        }
      ],
      data: [
        {
          name: 'In',
          bytes: 'inBytes',
          time: '5 min',
          spark: {
            name: 'in',
            labels: ['12am', '3am', '6am', '9am', '12pm', '3pm', '6pm', '9pm'],
            value: [200, 675, 410, 390, 310, 460, 250, 240]
          }
        },
        {
          name: 'Out',
          bytes: 'outBytes',
          time: '5 min',
          spark: {
            name: 'readoutwrite',
            labels: ['3pm', '6pm', '9pm', '12am', '3am', '6am', '9am', '12pm'],
            value: [460, 250, 240, 200, 675, 410, 390, 310]
          }
        },
        {
          name: 'Total',
          bytes: 'totalBytes',
          time: '5 min',
          spark: {
            name: 'readwrite',
            labels: ['12am', '3am', '12pm', '3pm', '6pm', '6am', '9am', '9pm'],
            value: [200, 390, 310, 460, 675, 410, 250, 240]
          }
        }
      ],
      tableview: false,
      codeview: false,
      pythonview: false,
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
        complete: false
      },
      confirm: false,
      deleteItem: false,
      deleteConfirm: false,
      prompt: false,
      contentStyle: {
        backgroundColor: 'rgba(0,0,0,0.02)',
        color: '#555'
      },

      contentActiveStyle: {
        backgroundColor: '#eee',
        color: 'black'
      },

      thumbStyle: {
        right: '2px',
        borderRadius: '5px',
        backgroundColor: '#027be3',
        width: '5px',
        opacity: 0.75
      }
    }
  },
  methods: {
    clearData () {
      let me = this
      this.saving = true
      DataService.clearData(this.viewtable, this.obj.database, this.obj.connection, this.obj.schema, this.$store.state.designer.token).then((result) => {
        me.tablerows = []
        me.saving = false
      }).catch((err) => {
        console.log('ERROR', err)
        me.saving = false
      })
    },
    tableSelected () {
      console.log('TABLE SELECTED')
    },
    refreshTables () {
      let me = this
      this.saving = true
      DataService.getRows(this.viewtable, this.obj.database, this.obj.connection, this.obj.schema, this.$store.state.designer.token).then((result) => {
        console.log('REFRESH DataService.getRows', result)
        me.tablerows = result.data
        me.saving = false
      }).catch((err) => {
        console.log('ERROR', err)
        me.saving = false
      })
    },
    pullSchema () {
      let me = this
      this.saving = true
      DataService.fetchTables(this.obj.database, this.obj.connection, this.obj.schema, this.$store.state.designer.token).then((result) => {
        console.log(result)
        me.obj.schema = ''
        me.tables = result.data.tables
        result.data.tables.forEach((table) => {
          me.obj.schema += table.schema + '\n'
        })

        me.schemaResult = 'Pull Schema succeeded'
        me.saving = false
      }).catch(() => {
        me.schemaResult = 'Pull Schema failure'
        me.saving = false
      })
    },
    testConnection () {
      let me = this
      this.saving = true
      DataService.testConnection(this.obj.database, this.obj.connection, this.$store.state.designer.token).then(() => {
        me.schemaResult = 'Connection Success!'
        me.saving = false
      }).catch(() => {
        me.schemaResult = 'Connection Error!'
        me.saving = false
      })
    },
    createSchema () {
      let me = this
      this.saving = true
      DataService.createSchema(this.obj.database, this.obj.connection, this.obj.schema, this.$store.state.designer.token).then(() => {
        me.schemaResult = 'Create Schema succeeded'
        me.saving = false
      }).catch(() => {
        me.schemaResult = 'Create Schema failure'
        me.saving = false
      })
    },
    setZoomLevel () {
      window.toolkit.surface.setZoom(1.0)
    },
    removePort (objid, col) {
      window.toolkit.removePort(objid, col)
      delete this.portobjects[col]
      // this.portobjects.remove(col)
      this.ports
      this.argobjects
    },
    updatePorts () {
      let me = this
      var node = window.designer.toolkit.getNode(this.obj)
      console.log('UPDATE DATA PORTS', node.getPorts())

      node.getPorts().forEach((port) => {
        me.updateDataPort(port)
      })
    },
    updateDataPort (port) {
      this.portobjects[port.id] = port.data
    },
    triggerQuery (portname) {

    },
    triggerObject (portname, column, result, callback) {
      let me = this

      console.log('TRIGGER ALL BEGIN')
      window.root.$emit('trigger.begin')
      console.log('triggerObject', portname, this.portobjects[portname])
      const objectname = this.portobjects[portname].name
      let resultstr = JSON.stringify(result)

      console.log('triggerObject result', result)
      const _port = window.toolkit.getNode(this.obj.id).getPort(portname)
      _port.getEdges().forEach((edge) => {
        console.log('DATA EDGE->NODE', edge, edge.target.getNode())
        const options = edge.target.data
        const target_id = edge.target.getNode().data.id
        console.log('myid, target node id', me.obj.id, target_id)
        if (me.obj.id === target_id) {
          return
        }
        const node = edge.target.getNode()
        const code = node.data.code

        window.root.$emit(target_id, code, options.function, options.name, result, node.data, portname)

        const reslen = resultstr.length
        tsdb.series('outBytes').insert(
          {
            bytes: reslen
          },
          new Date()
        )

        me.bytes_out_5min.unshift(reslen)
        // console.log('BYTE_IN_5MIN', me.bytes_in_5min);
        me.bytes_out_5min = me.bytes_out_5min.slice(0, 8)
        // console.log('BYTE_IN_5MIN SLICED', me.bytes_in_5min.slice(0, 8));
        me.bytes_out += reslen
        me.calls_out += 1
        // send message to target_id with result, _port
        // receiving node will realize this is an argument port and value
        // and store the value internally until all the arguments for the function
        // are present, then trigger the function with all the parameters
      })
      console.log('TRIGGER ALL COMPLETE')
      window.root.$emit('trigger.complete')
      // Trigger all the ports after me
      //this.triggerExecute(portname, column, result, callback)

      console.log('PORT RESULT ', _port, result)
    },
    triggerExecute (port, column, result, callback) {
      /*
      let exe = false

      for (var portname in this.portobjects) {
        if (port === undefined || exe) {
          this.triggerObject(portname, column, result, callback)
        } else {
          if (portname === port) {
            exe = true
          }
        }
      }*/
    },
    updateBandwidthChart () {
      var outBytes = tsdb.series('outBytes').query({
        metrics: { outBytes: TSDB.map('bytes'), time: TSDB.map('time') },
        where: {
          time: { is: '<', than: Date.now() - 60 * 60 }
        }
      })
      // this.series[1].data = outBytes[0].results.outBytes
      var inBytes = tsdb.series('inBytes').query({
        metrics: { inBytes: TSDB.map('bytes'), time: TSDB.map('time') },
        where: {
          time: { is: '<', than: Date.now() - 60 * 60 }
        }
      })
      // this.series[0].data = inBytes[0].results.inBytes
      var durations = tsdb.series('durations').query({
        metrics: { seconds: TSDB.map('seconds'), milliseconds: TSDB.map('milliseconds') },
        where: {
          time: { is: '<', than: Date.now() - 60 * 60 }
        }
      })
      // this.series[2].data = durations[0].results.data

      const xaxis = inBytes[0].results.time.map((x) => {
        const d = new Date(x)
        return d.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
      })
      console.log('XAXIS', xaxis)
      this.chartOptions.xaxis.categories = xaxis
      // console.log('updateBandwidthChart: inBytes', inBytes)
      // console.log('updateBandwidthChart: outBytes', outBytes)
      // console.log('updateBandwidthChart: durations', durations)
      if (this.$refs.bandwidthChart) {
        this.$refs.bandwidthChart.updateSeries([{
          name: 'Bytes Out',
          data: outBytes[0].results.outBytes.slice(0, 25)
        }, {
          name: 'Bytes In',
          data: inBytes[0].results.inBytes.slice(0, 25)
        }])
      }
    },
    showCommit (hash, date) {
      DataService.getCode(this.obj.gitrepo.split('#')[0], hash, this.$store.state.designer.token).then((code) => {
        this.commitcode = code.data
      })
      this.gitcommit = hash
      this.gitdate = date
    },
    getCommits () {
      DataService.getCommits(this.obj.gitrepo.split('#')[0], this.obj.modulepath, this.$store.state.designer.token).then((result) => {
        this.gitdata = result.data
      })
    },
    doLogin () {
      let me = this

      DataService.loginProcessor(this.obj.id, this.password, this.$store.state.designer.token)
        .then((result) => {
          me.login = false
          console.log(result)
        })
        .catch((error) => {
        })
    },
    addVariable () {
      this.variabledata.push({
        name: 'NAME',
        value: 'VALUE',
        scope: 'FLOW'
      })
    },
    addToLibrary () {
      window.root.$emit('add.library', this.obj)
    },
    cornerInView () {
      var node = this.toolkit.getNode(this.obj)
      window.toolkit.surface.setZoom(1.0)
      window.toolkit.surface.centerOn(node, {
        doNotAnimate: true,
        onComplete: function () {
          window.toolkit.surface.pan(-700, -440)
        }
      })
    },
    centerOnNode () {
      var node = this.toolkit.getNode(this.obj)
      window.toolkit.surface.setZoom(1.09)

      window.toolkit.surface.centerOn(node, {
        doNotAnimate: true,
        onComplete: function () {
          var loc = window.toolkit.surface.mapLocation(300, 50)
          // console.log(loc);
          window.toolkit.surface.pan(0, -200)
        }
      })
    },
    addFunc (func) {
      console.log('FUNCS2', this.funcs)
      addNewPort({ function: func.name, args: func.args }, 'Output', 'las la-search')
    },
    showOutput (resultid) {
      this.resultdataloading = true

      DataService.getOutput(resultid, this.$store.state.designer.token).then((result) => {
        this.resultdataloading = false

        const editor = this.$refs.resultEditor.editor
        editor.session.setValue(result.data)
      })
    },
    showResult (resultid) {
      this.resultdataloading = true

      DataService.getResult(resultid, this.$store.state.designer.token).then((result) => {
        this.resultdataloading = false

        const editor = this.$refs.resultEditor.editor
        editor.session.setValue(JSON.stringify(result.data, null, 2))
      })
    },
    refreshResultsData () {
      this.resultloading = true
      DataService.getCalls(this.obj.name, this.$store.state.designer.token)
        .then((calls) => {
          this.resultdata = calls.data
          this.resultloading = false
        })
        .catch((error) => {
          this.resultloading = false
        })
    },
    updateFunctions (code) {
      /* Parse out named objects from editor */
      const re = /def (\w+)\s*\((.*?)\):/g

      console.log('updateFunctions code', code)
      var matches = code.matchAll(re)

      this.funcs = []

      for (const match of matches) {
        var name = match[0].split('(')[0].split(' ').at(-1)
        this.funcs.push({ name: name, args: [] })
      }
    },
    fetchCode () {
      let me = this
      var url = new URL(this.obj.gitrepo)
      console.log('URL ', url)
      // https://raw.githubusercontent.com/radiantone/pyfi-processors/main/pyfi/processors/sample.py
      var codeUrl = 'https://raw.githubusercontent.com/' + url.pathname + '/main/' + this.obj.modulepath
      console.log('CODE', codeUrl)

      if (this.obj.code === undefined) {
        http.get(codeUrl).then((response) => {
          console.log('CODE RESPONSE', response)

          me.obj.code = response.data
          // const re = /(def)\s(\w+)/g;
          me.updateFunctions(response.data)

          if (this.$refs.myEditor) {
            const editor = this.$refs.myEditor.editor

            if (editor) {
              editor.session.setValue(me.obj.code)
            }
          }
        })
      }
    },
    copyNode () {
      console.log('COPY NODE')

      function findMatch (list, obj) {
        for (var i = 0; i < list.length; i++) {
          var o = list[i]
          if (o.id === obj.id) {
            return true
          }
        }
        return false
      }

      function findEdge (list, edge) {
        for (var i = 0; i < list.length; i++) {
          var e = list[i]
          if (e.source === edge.source || e.target === edge.target) {
            return true
          }
        }
        return false
      }

      function haveAllNodes (nodes, edge) {
        var source = false
        var target = false
        for (var i = 0; i < nodes.length; i++) {
          var node = nodes[i]
          if (edge.source.split('.')[0] === node.id) source = true
          if (edge.target.split('.')[0] === node.id) target = true
        }
        return source && target
      }

      var node = window.toolkit.getNode(this.obj.id)

      if (!node) {
        console.log('NODE NOT FOUND!')
      }

      var nodes = [node]

      console.log('COPY SELECTED NODES:', nodes)
      var exportData = window.toolkit.exportData()
      var data = JSON.parse(JSON.stringify(exportData, undefined, '\t'))
      var jsonData = {}
      jsonData.nodes = []
      jsonData.edges = []
      jsonData.ports = []
      for (var i = 0; i < data.nodes.length; i++) {
        const n = data.nodes[i]
        if (findMatch(nodes, n)) {
          jsonData.nodes.push(n)
        }
      }
      for (var i = 0; i < data.edges.length; i++) {
        const e = data.edges[i]
        if (haveAllNodes(jsonData.nodes, e)) {
          jsonData.edges.push(e)
        }
      }
      for (var i = 0; i < jsonData.nodes.length; i++) {
        const node = jsonData.nodes[i]
        for (var p = 0; p < data.ports.length; p++) {
          var port = data.ports[p]
          if (port.id.indexOf(node.id) > -1) {
            jsonData.ports.push(port)
          }
        }
      }

      window.clipboard = jsonData
      var nodes = []
      for (var i = 0; i < window.clipboard.nodes.length; i++) {
        nodes.push(window.toolkit.getNode(window.clipboard.nodes[i].id))
      }
      window.nodes = nodes
      console.log('jsonData:', jsonData)
      this.$store.commit('designer/setMessage', 'Node copied!')
    },
    closePortEdit () {
      this.editPort = false
    },
    saveProcessor () {
      let me = this

      this.refreshing = true

      this.obj.receipt = new Date()

      // embed variabledata, requirements into this.obj.uistate

      DataService.saveProcessor(this.obj, this.$store.state.designer.token)
        .then(() => {
          this.refreshing = false
          this.error = false
          this.errorMsg = ''
          me.$q.notify({
            color: 'secondary',
            timeout: 2000,
            position: 'top',
            message: 'Processor ' + me.obj.name + ' saved!',
            icon: 'save'
          })
        })
        .catch(() => {
          this.error = true
          this.errorMsg = 'Error saving processor'
          this.refreshing = false
        })
    },
    sizeOf (bytes) {
      if (bytes === 0) {
        return '0.00 B'
      }
      var e = Math.floor(Math.log(bytes) / Math.log(1024))
      return (bytes / Math.pow(1024, e)).toFixed(2) + ' ' + ' KMGTP'.charAt(e) + 'B'
    },
    mouseEnter (event) {
      this.cardX = event.clientX
      this.cardY = event.clientY
      this.mousecard = true
    },
    mouseExit (event) {
      console.log('mouseExit')
      // this.mousecard = false;
    },
    mouseMove (event) {
      this.cardX = event.clientX
      this.cardY = event.clientY
      console.log(this.cardX, this.cardY)
    },
    setBandwidth (value) {
      console.log('SET BANDWIDTH', value)
      this.obj.bandwidth = value
    },
    onSubmit () {
    },
    onReset () {
    },
    loginProcessor () {
      this.login = true
    },
    getUuid () {
      return 'key_' + uuidv4()
    },
    rowStripe (row) {
      if (row % 2 === 0) {
        return 'background-color:white'
      }
    },
    showPanel (view, show) {
      this.configview = false
      this.codeview = false
      this.dataview = false
      this.gitview = false
      this.historyview = false
      this.consoleview = false
      this.environmentview = false
      this.scalingview = false
      this.notesview = false
      this.requirementsview = false
      this.logsview = false
      this.securityview = false
      this.middlewareview = false
      this.tableview = false
      this.connectResult = ''
      this[view] = show
      if (this[view + 'Setup']) {
        this[view + 'Setup']()
      }

      if (show) {
        // window.toolkit.surface.setZoom(1.0);

        var node = this.toolkit.getNode(this.obj)
        if (view === 'historyview') {
          console.log(this.myhistory)
        }
        if (view === 'gitview') {
          this.getCommits()
        }
      }
    },
    updateDescription (value, initialValue) {
      console.log('updateDesc', value, initialValue)
      this.renameConfirm = true
      this.renameValue = value
      this.initialValue = initialValue
    },
    updateName (value, initialValue, column) {
      console.log('column edited ', column)
      console.log('updateName', value, initialValue)
      this.renameConfirm = true
      this.renameValue = value
      this.initialValue = initialValue
      var edges = document.querySelectorAll('[data-source=' + column + ']')

      edges.forEach((edge) => {
        edge.innerText = value
      })
    },
    schemaEditorInit: function () {
      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/sql') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.schemaEditor.editor
      editor.setAutoScrollEditorIntoView(true)
    },
    gitEditorInit: function () {
      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.gitEditor.editor
      editor.setAutoScrollEditorIntoView(true)
    },
    reqEditorInit: function () {
      let me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.requirementsEditor.editor
      editor.setAutoScrollEditorIntoView(true)
      editor.on('change', function () {
        me.obj.requirements = editor.getValue()
      })
    },
    middlewareEditorInit: function () {
      let me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.middlewareEditor.editor
      editor.setAutoScrollEditorIntoView(true)
      editor.on('change', function () {
        me.middleware = editor.getValue()
        me.obj.middleware = me.middleware
      })
    },
    notesEditorInit: function () {
      let me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.notesEditor.editor
      editor.setAutoScrollEditorIntoView(true)
      editor.on('change', function () {
        me.obj.notes = editor.getValue()
      })
    },
    resultEditorInit: function () {
      let me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.resultEditor.editor
      editor.setAutoScrollEditorIntoView(true)
      editor.on('change', function () {
        me.updateFunctions(editor.getValue())
      })
    },
    editorInit: function () {
      let me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.myEditor.editor
      editor.setAutoScrollEditorIntoView(true)
      editor.on('change', function () {
        me.updateFunctions(editor.getValue())
      })
      if (me.obj.code) {
        editor.session.setValue(me.obj.code)
      }
    },
    showCode () {
      // this.code = true;
    },
    showTooltip (show) {
      this.tooltip = show
    },
    confirmDeletePort (id) {
      this.deletePortID = id
      this.deleteItem = true
    },
    resetToolkit () {
      console.log('emitting toolkit.dirty')
      this.$root.$emit('toolkit.dirty', false)
    },
    valueChanged () {
      console.log('emitting toolkit.dirty')
      this.$root.$emit('toolkit.dirty', true)
    },
    deleteNode () {
      window.toolkit.removeNode(this.obj)
    },
    removeColumn (column) {
      // Delete all argument columns too
      console.log('Removing column: ', column)

      for (var i = 0; i < this.obj.columns.length; i++) {
        var col = this.obj.columns[i]
        console.log(col)
        if (col.id === column) {
          console.log('Deleted column')
          this.obj.columns.splice(i, 1)
          break
        }
      }

      var edges = window.toolkit.getAllEdges()

      for (var i = 0; i < edges.length; i++) {
        console.log(edge)
        const edge = edges[i]
        console.log(edge.source.getNode().id, this.obj.id, edge.data.label, column)
        if (edge.source.getNode().id === this.obj.id && edge.data.label === column) {
          window.toolkit.removeEdge(edge)
        }
      }
      // Delete all the edges for this column id
      console.log(this.obj)
      console.log('PORT ARGS', this.argports[column])
      this.removePort(this.obj.id, column)

      if (this.argports[column]) {
        this.argports[column].forEach((portid) => {
          this.removePort(this.obj.id, portid)
        })
      }
      // window.renderer.repaint(this.obj);
    },
    addPort (port) {
      port.background = 'white'
      port.datatype = 'Column'
      if (this.types.length > 0) {
        port.schema = this.types[0]
      } else {
        port.schema = null
      }
      port.template = 'Object'
      port.id = 'port' + uuidv4()
      port.id = port.id.replace(/-/g, '')
      port.description = 'A description'
      port.loading = '#fff'
      port.queue = 'None'

      console.log('Port:', port)
      window.toolkit.addNewPort(this.obj.id, 'data', port)
      window.renderer.repaint(this.obj)
      console.log('Firing node updated...')

      console.log(this.obj.columns)

      return port
    },
    updateSchemas () {
      setTimeout(() => {
        var graph = window.toolkit.getGraph().serialize()

        var schemas = []

        graph.nodes.forEach((node) => {
          if (node.type === 'schema') {
            schemas.push(node.name)
          }
        })
        this.types = schemas
      })
    },
    addNewTablePort (table, type, icon) {
      var port = this.addPort({
        name: table.name,
        icon: icon,
        type: type
      })

      this.ports[table.name] = true
      this.portobjects[port.id] = port

      if (type === 'Error') {

      }
    },
    addNewPort (func, type, icon) {
      var port = this.addPort({
        name: func.function,
        icon: icon,
        type: type
      })

      this.ports[func.function] = true
      this.portobjects[port.id] = port

      this.updateSchemas()

      if (type === 'Error') {

      }
    },
    addErrorPort () {
      if (this.error) {
        this.$q.notify({
          color: 'negative',
          timeout: 2000,
          position: 'bottom',
          message: 'Error is already created',
          icon: 'fas fa-exclamation'
        })
        return
      }
      this.addPort({
        name: 'Error',
        icon: 'fas fa-exclamation',
        type: 'Error'
      })
      this.error = true
    },
    selectNode: function () {
      console.log('selected: ', this.obj.id)
      window.root.$emit('node.selected', this.obj)
    },
    deleteEntity: function (name) {
      this.entityName = name
      this.confirm = true
    },
    clicked: function () {
      console.log('clicked')
    }
  }
}
</script>

