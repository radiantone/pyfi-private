<template>
  <div
    class="table node shadow-1 jtk-node"
    style="overflow: unset !important;"
    :style="'top:' + obj.y + ';left:' + obj.x + ';min-width:' + obj.width + '; z-index: 999'"
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
          @click="obj.status = 'running'"
        >
          <q-item-section side>
            <q-icon name="fas fa-play" />
          </q-item-section>
          <q-item-section
            side
            class="text-blue-grey-8"
          >
            Run
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
            <q-icon name="fas fa-plug" />
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
        title="API Endpoint"
        style="
          margin-top: -15px;
          padding: 10px;
          font-weight: normal;
          padding-left: 2px;
          font-size: 40px;
          margin-right: 5px;
        "
      >
        <q-icon
          name="las la-cloud-upload-alt"
          size="xl"
          color="secondary"
          style="margin-left:-5px;margin-top:-5px"
        />
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
          padding-left: 10px;
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
          <q-popup-edit
            v-model="obj.name"
            buttons
          >
            <q-input
              type="string"
              v-model="obj.name"
              dense
              autofocus
            />
          </q-popup-edit>
        </span>
      </span>
      <span
        v-if="!obj.titletab"
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
        {{ obj.description.substring(0, 35) + "..." }}
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
          <q-btn-dropdown
            flat
            content-class="text-dark bg-white "
            dense
            menu-self="top left"
            dropdown-icon="fas fa-exclamation"
            color="secondary"
            padding="0px"
            size=".6em"
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
                @click="addNewPort({ function: 'function: ' + func.name, args: [] }, 'Error', 'fas fa-exclamation')"
              >
                <q-item-section side>
                  <q-icon name="fab fa-python" />
                </q-item-section>
                <q-item-section
                  side
                  class="text-blue-grey-8"
                >
                  function: {{ func.name }}
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
            Add Error Plug
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
            :dropdown-icon="plugIcon"
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
                @click="addNewPort({ function: 'function: ' + func.name, args: func.args }, 'Output', 'outlet-icon')"
              >
                <q-item-section side>
                  <q-icon name="fab fa-python" />
                </q-item-section>
                <q-item-section
                  side
                  class="text-blue-grey-8"
                >
                  function: {{ func.name }}
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
            Add Socket
          </q-tooltip>
        </div>

        <div
          class="text-secondary"
          style="margin-right: 10px;"
          @click="addNewPort({ function: 'route A', args: [] }, 'Plug', 'fas fa-plug')"
        >
          <i
            class="fas fa-plug"
            style="cursor: pointer;"
          />
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
            style="margin-right: 10px; position: absolute; right: 135px; top: -68px; width: 25px; height: 30px;"
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
            v-if="obj.status === 'stopped'"
            flat
            class="edit-name text-secondary"
            @click="obj.status = 'running'"
            style="position: absolute; right: 110px; top: -68px; width: 25px; height: 30px;"
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Run All
            </q-tooltip>
          </q-btn>
          <q-btn
            icon="fa fa-stop"
            size="xs"
            dense
            flat
            v-if="obj.status === 'running'"
            @click="obj.status = 'stopped'"
            class="edit-name text-secondary text-green"
            style="position: absolute; right: 110px; top: -68px; width: 25px; height: 30px;"
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Stop
            </q-tooltip>
          </q-btn>
          <q-btn
            dense
            flat
            size="xs"
            icon="fas fa-terminal"
            @click="showPanel('consoleview', !consoleview)"
            class="edit-name text-secondary"
            style="position: absolute; right: 85px; top: -68px; width: 25px; height: 30px;"
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
            icon="fas fa-list"
            @click="showResultsDialog"
            class="edit-name text-secondary"
            style="position: absolute; right: 55px; top: -68px; width: 25px; height: 30px;"
          >
            <q-tooltip
              anchor="top middle"
              :offset="[-30, 40]"
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              View Results
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
        :style="'background:'+column.background+';border-top: 1px dashed lightgrey'"
        :primary-key="column.primaryKey"
        :data-port-id="column.id"
      >
        <div class="table-column-edit text-primary">
          <div
            class="table-column-edit text-primary"
            style="max-height: 15px; position: absolute; right: 20px; margin-top: -10px;"
          />
          <i
            v-if="column.type !== 'Input' && column.type !== 'Plug' && column.type !== 'Error'"
            class="fa fa-play table-column-delete-icon"
            title="Trigger Port"
            style="margin-right: 5px;"
            @click="executeObject('func:'+column.name.replace('function: ',''))"
          />
          <i
            v-if="column.type !== 'Input'"
            class="fa fa-times table-column-delete-icon"
            title="Delete Port"
            @click="confirmDeletePort(column.id)"
          />

          <i
            v-if="column.data"
            class="fas fa-envelope text-secondary"
            title="View Argument Data"
          />
        </div>
        <div
          class="table-column-edit text-primary"
          style="max-height: 15px; position: absolute; right: 20px; margin-top: -10px;"
        >
          <q-select
            dense
            borderless
            v-if="column.type === 'Input'"
            :options-dense="true"
            style="font-size: 1em; margin-right: 5px;"
            label-color="orange"
            v-model="column.schema"
            :options="types"
            value="string"
            :menu-offset="[5, -9]"
          />
        </div>
        <div v-if="column.type !== 'Input'">
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
                v-model="column.name"
                buttons
                v-if="column.icon === 'fas fa-plug'"
              >
                <q-input
                  type="string"
                  v-model="column.name"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </span>
          </span>
        </div>
        <div
          v-if="column.type === 'Input'"
          style="margin-left: 30px;"
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
          v-if="column.type !== 'Input'"
          name="source"
          :port-id="column.id"
          :scope="column.datatype"
          filter=".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon"
          filter-exclude="true"
          type="Output"
        />

        <jtk-target
          v-if="column.type === 'Input'"
          name="target"
          :port-id="column.id"
          type="Input"
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
              color: #fff;
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
              color: #fff;
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
          'px;top: 0px;'
      "
      v-if="codeview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px;">
        <editor
          v-model="obj.code"
          @init="editorInit"
          style="font-size: 16px; min-height: 600px;"
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
          icon="fab fa-python"
          class="bg-accent text-secondary"
          color="primary"
          v-close-popup
          @click="pythonview = !pythonview"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Python Console
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
          @click=""
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
      style="width: 100%; width: 650px; z-index: 999; display: block; position: absolute; right: -655px; top: 0px;"
      v-if="configview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 550px;">
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
            name="schedule"
            label="Schedule"
          />
        </q-tabs>

        <q-tab-panels
          v-model="tab"
          keep-alive
        >
          <q-tab-panel
            name="settings"
            style="padding: 0px;"
            ref="settings"
          >
            <q-tabs
              v-model="settingstab"
              class="text-primary"
              align="center"
              dense
            >
              <q-tab
                name="settings"
                label="Processor"
              />
              <q-tab
                v-if="obj.icon === lambdaIcon"
                name="lambda"
                label="Lambda"
              />
              <q-tab
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
                      v-model="obj.swagger"
                      dense
                      hint="Swagger URL"
                      lazy-rules
                      :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                    />

                    <q-input
                      filled
                      v-model="obj.icon"
                      dense
                      hint="Icon Class"
                      lazy-rules
                      :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                    />
                    <q-input
                      filled
                      v-model="obj.mode"
                      dense
                      hint="Mode"
                      lazy-rules
                      :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                    />
                    <q-input
                      filled
                      v-model="obj.credentials"
                      dense
                      hint="Credentials"
                      lazy-rules
                      :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                    />
                    <q-toolbar style="margin-left: -30px;">
                      <q-space />
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
                      <q-checkbox
                        v-model="obj.endpoint"
                        label="API"
                        style="margin-left: 40px; margin-right: 50px;"
                      />
                    </q-toolbar>
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
              style="width: 100%; border-top-radius: 0px; border-bottom-radius: 0px;"
            >
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
            <q-toolbar>
              <q-input
                style="width: 100px;"
                hint="Number of CPUs"
                type="number"
                v-model.number="obj.concurrency"
              />
            </q-toolbar>
            <q-inner-loading
              :showing="deployLoading"
              style="z-index: 9999999;"
            >
              <q-spinner-gears
                size="50px"
                color="primary"
              />
            </q-inner-loading>
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
              v-model="obj.useschedule"
              style="margin-top: 30px;"
              label="Use CRON"
            />
          </q-tab-panel>
        </q-tab-panels>
      </q-card-section>
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          label="Generate"
          class="bg-primary text-secondary"
          color="primary"
          @click="generateClient"
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
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 500px;">
        <q-scroll-area
          style="height:475px;width:auto"
          ref="scroll"
        >
          <div v-if="jsonmode">
            <editor
              @init="jsonEditorInit"
              style="font-size: 1.5em;"
              lang="javascript"
              theme="chrome"
              ref="jsonEditor"
              width="100%"
              height="475px"
            />
          </div>
          <div
            v-for="(log, index) in consolelogs"
            v-if="!jsonmode"
          >
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
        <q-checkbox
          v-model="jsonmode"
          label="JSON View"
          style="position: absolute; bottom: 0px; left: 300px;"
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

    <q-dialog
      v-model="viewResultsDialog"
      transition-show="none"
      persistent
    >
      <q-card style="width: 70vw; max-width: 70vw; height: 80vh; padding: 10px; padding-left: 30px; padding-top: 40px;">
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
              <q-item-label>Results for {{ obj.name }}</q-item-label>
              <q-space />
              <q-select
                dense
                borderless
                :options-dense="true"
                style="font-size: 1em; margin-right: 20px; color: white;"
                v-model="resulttype"
                :options="['finished', 'error']"
              />
              <q-btn
                class="text-primary"
                flat
                dense
                round
                size="sm"
                icon="fas fa-close"
                @click="viewResultsDialog = false"
                style="z-index: 10;"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-splitter
          v-model="resultSplitter"
          separator-style="background-color: #e3e8ec;height:5px"
          horizontal
          style="height: calc(100% - 40px);"
        >
          <template #before>
            <q-table
              dense
              :columns="resultcolumns"
              :data="resultdata"
              row-key="name"
              flat
              :pagination="resultPagination"
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
                    {{ props.cols[0].value }}
                  </q-td>
                  <q-td
                    :key="props.cols[1].name"
                    :props="props"
                  >
                    <a
                      class="text-secondary"
                      @click="showResult(props.row.resultid)"
                    >{{ props.cols[1].value }}</a>
                  </q-td>
                  <q-td
                    :key="props.cols[2].name"
                    :props="props"
                  >
                    <a
                      class="text-secondary"
                      @click="showOutput(props.cols[1].value)"
                    >Output</a>
                  </q-td>
                  <q-td
                    :key="props.cols[3].name"
                    :props="props"
                  >
                    {{ props.cols[3].value }}
                  </q-td>
                  <q-td
                    :key="props.cols[4].name"
                    :props="props"
                  >
                    {{ props.cols[4].value }}
                  </q-td>
                  <q-td
                    :key="props.cols[5].name"
                    :props="props"
                  >
                    {{ props.cols[5].value }}
                  </q-td>

                  <q-td
                    :key="props.cols[6].name"
                    :props="props"
                  >
                    {{ props.cols[6].value }}
                  </q-td>

                  <q-td
                    :key="props.cols[7].name"
                    :props="props"
                  >
                    {{ props.cols[7].value }}
                  </q-td>
                  <q-td
                    :key="props.cols[8].name"
                    :props="props"
                  >
                    {{ props.cols[8].value }}
                  </q-td>
                </q-tr>
              </template>
            </q-table>
          </template>
          <template #after>
            <div style="height: 100%; width: 100%;">
              <editor
                @init="resultEditorInit"
                style="font-size: 1.5em;"
                lang="javascript"
                theme="chrome"
                ref="resultEditor"
                width="100%"
                height="100%"
              />
            </div>
            <q-inner-loading
              :showing="resultdataloading"
              style="z-index: 0;"
            >
              <q-spinner-gears
                size="50px"
                color="primary"
              />
            </q-inner-loading>
          </template>
        </q-splitter>
        <q-card-actions align="left">
          <q-btn
            style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
            flat
            icon="refresh"
            class="bg-secondary text-dark"
            color="primary"
            @click="refreshResultsData"
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
        <q-inner-loading
          :showing="resultloading"
          style="z-index: 99999;"
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
<style>
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

import { TSDB } from 'uts'
import SwaggerParser from '@apidevtools/swagger-parser'
import ScriptTemplate from './ScriptTemplate'

var Moment = require('moment') // require

const tsdb = new TSDB()

export default {
  name: 'ApiTemplate',
  extends: ScriptTemplate,
  created () {
      this.obj.gitrepo = ''
  },
  async mounted () {
    try {
      const api = await SwaggerParser.validate('https://apitools.dev/swagger-parser/online/sample/swagger.yaml')
      console.log('API name: %s, Version: %s', api.info.title, api.info.version)
      this.obj.swagger = 'https://petstore.swagger.io/v2/swagger.json'
      this.obj.mode = "CORS"
      this.obj.credentials = "same-origin"
    } catch (err) {
      console.error(err)
    }
  },
  methods: {

    async generateClient () {
      var me = this

      var code = ''
      const get = async () => {
        try {
          const api = await SwaggerParser.validate(me.obj.swagger)
          console.log('API name: %s, Version: %s', api.info.title, api.info.version)
          return api
        } catch (err) {
          console.error(err)
        }
      }

      await get().then((api) => {
        console.log(api)
        me.obj.name = api.info.title
        me.obj.description = api.info.description
        me.obj.version = api.info.version
        // Generate python client wrappers
        console.log("url = 'https://" + api.host + api.basePath + "'")
        for (var path in api.paths) {
          const pathobj = api.paths[path]
          let _path = path.replace(/}/gm, '')
          _path = _path.replace(/\/{/gm, '_')
          _path = _path.replace(/\//gm, '_')
          for (var method in pathobj) {
            let func = 'def ' + method + _path
            const params = pathobj[method].parameters
            func += '('
            for (const index in params) {
              const param = params[index]
              func = func + param.name
              if (parseInt(index) < params.length - 1) {
                func = func + ','
              }
            }
            func = func + '):\n'
            func = func + '    from pyodide.http import pyfetch\n'
            func = func + '    import json\n'
            func = func + "    data = json.dumps({'this':'that'})\n"
            func = func + '    response = pyfetch(url+f"' + path + "\", mode=\"" + me.obj.mode + "\", cache=\"no-cache\", credentials=\"" + me.obj.credentials + "\", headers={'Content-Type': 'application/json'}, body=data, method=\"" + method.toUpperCase() + '")\n\n'
            code = code + func + '\n'
            console.log(func)
          }
        }
        me.obj.code = code

        me.updateFunctions(code)
      })
    }
  },
  data () {
    return {
      myobj: {
        // Will come from mixed in Script object (vuex state, etc)
        icon: 'las la-cloud-upload-alt',
        titletab: false,
        receipt: new Date(),
        notes: '',
        style: '',
        x: 0,
        y: 0,
        swagger: 'https://petstore.swagger.io/v2/swagger.json',
        version: 'v1.2.2',
        perworker: true,
        ratelimit: '60',
        websocket: 'ws://localhost:3003',
        bandwidth: true,
        requirements: '',
        gittag: '',
        container: true,
        imagerepo: 'local',
        containerimage: 'pyfi/processors:latest',
        environment: '',
        usegit: true,
        enabled: true,
        endpoint: false,
        beat: false,
        streaming: true,
        api: '/api/processor',
        type: 'script',
        name: 'API',
        label: 'API',
        description: 'An API block',
        concurrency: 3,
        cron: '* * * * *',
        interval: 5,
        useschedule: false,
        disabled: false,
        commit: '',
        columns: [],
        readwrite: 0,
        status: 'stopped',
        properties: []
      }
    }
  }
}
</script>
