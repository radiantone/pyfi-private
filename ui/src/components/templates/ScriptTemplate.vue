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
        <q-icon
          name="las la-scroll"
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
                @click="addNewPort({ function: 'error: ' + func.name, args: [] }, 'Error', 'fas fa-exclamation')"
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
              @click="showPanel('gitview', !gitview)"
            >
              <q-item-section side>
                <q-icon name="fab fa-github" />
              </q-item-section>
              <q-item-section
                side
                class="text-blue-grey-8"
              >
                Git
              </q-item-section>
            </q-item>
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
      v-if="obj.icon === 'fab fa-python' || obj.icon === 'las la-scroll' || obj.icon === 'fas fa-plug'"
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
            style="cursor:pointer"
            @click="showArgumentData(column.data)"
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

    <q-dialog
      v-model="confirmCodeFetch"
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
              <q-item-label>Fetch Code</q-item-label>
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
            Fetch code from GIT and overwrite current code?
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
            label="Yes"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="fetchCode"
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
          ref="codeEditor"
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
          class="bg-secondary text-accent"
          color="primary"
          v-close-popup
          @click="confirmFetch"
          :disable="!this.obj.usegit"
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
          class="bg-primary text-white"
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
      <q-card-actions align="left">
        <q-btn
          style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
          flat
          label="Update"
          class="bg-primary text-white"
          color="primary"
        >
          <q-tooltip
            anchor="top middle"
            :offset="[-30, 40]"
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Update Packages
          </q-tooltip>
        </q-btn>
      </q-card-actions>
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
                label="General"
              />
              <q-tab
                name="containersettings"
                label="Container"
              />
              <q-tab
                name="gitsettings"
                label="Git"
              />
              <q-tab
                name="apisettings"
                label="API"
              />
              <q-tab
                name="versions"
                label="Version"
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
                      :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                    />

                    <q-input
                      filled
                      v-model="obj.description"
                      dense
                      hint="Processor Description"
                      lazy-rules
                      :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                    />
                    <q-input
                      filled
                      v-model="obj.package"
                      dense
                      hint="Processor Package"
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
                      v-model="obj.middleware"
                      dense
                      hint="Middleware"
                      lazy-rules
                      :rules="[(val) => (val && val.length > 0) || 'Please type something']"
                    />
                    <q-toolbar style="margin-left: -30px;">
                      <q-space />
                      <q-checkbox
                        v-model="obj.usegit"
                        label="GIT"
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
                      <q-checkbox
                        v-model="obj.endpoint"
                        label="API"
                        style="margin-left: 40px; margin-right: 50px;"
                        :disable="!hasHosted"
                      />
                      <q-checkbox
                        v-model="obj.streaming"
                        label="Streaming"
                        style=""
                        :disable="!hasHosted"
                      />
                    </q-toolbar>
                  </q-form>
                </div>
              </q-tab-panel>
              <q-tab-panel
                name="gitsettings"
                style="padding-top: 0px; padding-bottom: 0px;"
              >
                <div
                  class="q-pa-md"
                  style="max-width: 100%; padding-bottom: 0px;"
                >
                  <q-form class="q-gutter-md">
                    <q-input
                      filled
                      dense
                      :disable="!obj.usegit"
                      v-model="obj.gitrepo"
                      hint="GIT Repository"
                    />

                    <q-input
                      filled
                      dense
                      :disable="!obj.usegit"
                      v-model="obj.modulepath"
                      hint="Module Path"
                    />

                    <q-input
                      filled
                      dense
                      :disable="!obj.usegit"
                      v-model="obj.commit"
                      hint="Commit Hash"
                    />

                    <q-input
                      filled
                      dense
                      :disable="!obj.usegit"
                      v-model="obj.gittag"
                      hint="GIT Tag"
                    />
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
                      :disable="!obj.endpoint || !hasHosted"
                    />
                    <q-input
                      filled
                      v-model="obj.websocket"
                      dense
                      hint="Websocket URL"
                      lazy-rules
                      :disable="!obj.streaming || !hasHosted"
                    />
                  </q-form>
                </div>
              </q-tab-panel>
              <q-tab-panel
                name="versions"
                style="padding-top: 0px; padding-bottom: 0px;"
              >
                <q-toolbar>
                  <q-input
                    style="width: 200px;"
                    hint="Version"
                    type="string"
                    v-model.number="obj.version"
                  />
                </q-toolbar>
              </q-tab-panel>
            </q-tab-panels>
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
      v-if="argumentview"
    >
      <q-card-section style="padding: 5px; z-index: 999999; padding-bottom: 10px; height: 500px;">
        <q-scroll-area
          style="height:475px;width:auto"
          ref="scroll"
        >
          <editor
            @init="jsonArgumentEditorInit"
            style="font-size: 1.5em;"
            lang="javascript"
            theme="chrome"
            ref="jsonArgumentEditor"
            width="100%"
            height="475px"
          />
        </q-scroll-area>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn
          flat
          style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
          label="Close"
          class="bg-secondary text-white"
          color="primary"
          @click="argumentview = false"
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
                    >{{ props.cols[1].value }}</a>
                  </q-td>
                  <q-td
                    :key="props.cols[2].name"
                    :props="props"
                  >
                    <a
                      class="text-secondary"
                      @click="showOutput(JSON.stringify(props.cols[2].value, null, '\t'))"
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
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { BaseNodeComponent } from 'jsplumbtoolkit-vue2'
import { v4 as uuidv4 } from 'uuid'
import Vuetify from 'vuetify'
import { mdiLambda, mdiAbacus, mdiPowerSocketUs, mdiCodeBraces } from '@mdi/js'

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
  name: 'ScriptTemplate',
  mixins: [BaseNodeComponent, BetterCounter, Processor], // Mixin the components
  vuetify: new Vuetify(),
  components: {
    editor: require('vue2-ace-editor'),
    BetterCounter,
    Console
  },
  watch: {
    dataview: function (val) {
      var me = this
      if (val) {
        setTimeout(() => {
          me.updateBandwidthChart()
        })
      }
    },
    'obj.status': function (val) {
      // window.designer.$root.$emit('toolkit.dirty')
    },
    consolehistory: function (val) {
      if (val) {
        this.jsonmode = false
      }
    },
    jsonmode: function (val) {
      if (val) {
        setTimeout(() => {
          this.$refs.jsonEditor.editor.session.setValue(JSON.stringify(JSON.parse(this.currentresult), null, 2))
        })
      }
    },
    currentresult: function (val) {
      if (this.$refs.jsonEditor) {
        this.$refs.jsonEditor.editor.session.setValue(JSON.stringify(JSON.parse(val), null, 2))
      }
    },
    inBytes: function (val) {
      // console.log('inBytes', val);
    }
  },
  created () {
    var me = this

    this.plugIcon = mdiPowerSocketUs
    this.braces = mdiCodeBraces
    this.lambdaIcon = mdiLambda
    this.abacusIcon = mdiAbacus

    console.log('me.tooltips ', me.tooltips)
    console.log('start listening for show.tooltips')

    window.root.$on('show.tooltips', (value) => {
      console.log('start tooltips:', value)
      me.tooltips = value
      console.log('ME:', me)
      console.log('TOOLTIPS', me.tooltips)
    })

    const avoid = ['icon', 'id']
    this.$on('refresh', () => {
      me.updateColumns()
    })
    this.$on('python.error', (error) => {
      me.getNode().getPorts().forEach((port) => {
        if (port.data.type === 'Error' && 'error: ' + error.function === port.data.name) {
          me.errorMsg = 'Error in ' + error.function
          me.error = true
          me.triggerRoute(port.data.id, error)
        }
      })
    })
    this.$on('arg.in', (arg) => {
      if (arg) {
        console.log('arg.in', arg)
        try {
          if (arg instanceof Object) {
            arg = JSON.stringify(arg)
          } else if (arg instanceof String) {

          } else {
            arg = arg.toString()
          }
          me.bytes_in += arg.length
          me.calls_in += 1
        } catch (e) {

        }
      }
    })

    this.$on('message.received', (msg) => {
      if (msg.type && msg.type === 'DeploymentModel') {
        console.log('DEPLOYMENT UPDATED')
        me.refreshDeployments(false)
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
      if (msg.type && msg.type === 'result') {
        if (msg.id === this.obj.id) {
          me.currentresult = msg.output
          me.consolelogs.push({ date: new Date(), output: msg.output })
          window.root.$emit('console.message', new Date(), me.obj, msg.output)
          me.consolelogs = me.consolelogs.slice(0, 100)
          me.task_time = msg.duration
          const resdate = new Date()
          tsdb.series('outBytes').insert(
            {
              bytes: msg.output.length
            },
            resdate
          )

          const answer = JSON.parse(msg.output)

          // update resultdata
          me.resultdata.push({
            name: msg.function,
            id: me.resultdata.length,
            created: resdate,
            state: 'COMPLETE',
            lastupdated: resdate,
            owner: me.$auth.user !== undefined ? me.$auth.user.name : 'guest',
            size: msg.output.length,
            output: answer,
            task_id: uuidv4()
          })

          // me.bytes_out_5min.unshift(msg.output.length)
          // console.log('BYTE_IN_5MIN', me.bytes_in_5min);
          // me.bytes_out_5min = me.bytes_out_5min.slice(0, 8)
          // console.log('BYTE_IN_5MIN SLICED', me.bytes_in_5min.slice(0, 8));
          // me.bytes_out += msg.output.length

          me.updateBandwidthChart()
          // update resultdata

          me.error = false
        }
        Object.entries(this.argobjects).forEach((tuple) => {
          const argobject = tuple[1]
          me.obj.columns.forEach((column) => {
            if (column.argument) {
              if (column.name === argobject.name && column.function === argobject.function) {
                column.data = null
                argobject.data = null
              }
            }
          })
        })
        me.updateColumns()
        const func = msg.function
        // Find the port for the function
        // Emit result over the port edges
        let _plugs = JSON.parse(msg.plugs)
        for (var key in this.portobjects) {
          let port = this.portobjects[key]
          key = key.replace('func:', '')

          if (key in _plugs) {
            let plug_data = _plugs[key]
            if (port.id) {
              me.triggerRoute(port.id, plug_data, msg.plugs)
            }
          }
          if (key === func) {
            //me.triggerObject('func:' + key, msg.output, msg.plugs)
            if (port.id) {
              me.triggerRoute(port.id, JSON.parse(msg.output), msg.plugs)
            }
          }
        }
      }

      if (msg.type && msg.type === 'output') {
        if (msg.id === this.obj.id) {
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
        me.bytes_in_5min.unshift(bytes)
        // console.log('BYTE_IN_5MIN', me.bytes_in_5min);
        me.bytes_in_5min = me.bytes_in_5min.slice(0, 8)
        // console.log('BYTE_IN_5MIN SLICED', me.bytes_in_5min.slice(0, 8));
        me.bytes_in += bytes

        me.calls_in += 1
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
        me.bytes_out_5min = me.bytes_out_5min.slice(0, 8)
        // me.calls_out += 1
        me.resultlogs.unshift(json)
        me.resultlogs = me.resultlogs.slice(0, 100)
      }
      if (msg.channel === 'log' && msg.message) {
        me.msglogs.unshift(msg)
        me.msglogs = me.msglogs.slice(0, 100)
      }
      me.totalbytes_5min.unshift(me.bytes_in + me.bytes_out)
      me.totalbytes_5min = me.totalbytes_5min.slice(0, 8)
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
    consoleview: {
      get: function () {
        return this.obj.consoleview
      },
      set: function (val) {
        this.obj.consoleview = val
      }
    },
    myhistory () {
      var me = this

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
    var me = this
    /*
    async function load () {
      const pyodide = await loadPyodide()
      me.pyodide = pyodide
    }

    load().then(() => {
      console.log('PROCESSOR PYODIDE RESULT', me.pyodide.runPython('1 + 2'))
    }) */

    this.setId(this.obj.id)
    console.log('MOUNTED STORE', this.$store)
    console.log('BYTES_IN', this.bytes_in)

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
    // window.designer.$root.$emit('toolkit.dirty')
    this.deployLoading = true
    this.fetchCode((code) => {
      me.updatePorts()
      me.updateColumns()
    })
    this.updateBandwidthChart()
    this.updatePorts()
  },
  data () {
    return {
      confirmCodeFetch: false,
      currentresult: '',
      resulttype: 'finished',
      queues: [],
      argports: {},
      funcs: [],
      argumentview: false,
      afuncs: [],
      codewidth: 950,
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
          label: 'ID',
          field: 'id',
          align: 'left'
        },

        {
          name: 'output',
          label: 'Output',
          field: 'output',
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
          name: 'size',
          label: 'Size',
          field: 'size',
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
      errorMsg: 'An error',
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
      jsonmode: false,
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
        icon: 'las la-scroll',
        titletab: false,
        consoleview: false,
        receipt: new Date(),
        notes: '',
        style: '',
        x: 0,
        y: 0,
        version: 'v1.2.2',
        perworker: true,
        ratelimit: '60',
        websocket: 'ws://localhost:3003',
        bandwidth: true,
        requirements: '',
        gittag: '',
        container: false,
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
        name: 'Processor',
        label: 'Script',
        description: 'A script processor description',
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
        modulepath: 'ext/processors/sample.py',
        readwrite: 0,
        status: 'stopped',
        properties: []
      },
      text: '',
      configview: false,
      historyview: false,
      logsview: false,
      requirementsview: false,
      notesview: false,
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
      workercolumns: [
        {
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        },
        {
          name: 'host',
          label: 'Host',
          field: 'host',
          align: 'left'
        },
        {
          name: 'cpus',
          label: 'CPUs',
          field: 'cpus',
          align: 'left'
        },
        {
          name: 'deployment',
          label: 'Deployment',
          field: 'deployment',
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
      workerdata: [],
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
        },
        {
          name: 'Task/Time',
          bytes: 'taskTime',
          time: '5 min',
          spark: {
            name: 'taskstime',
            labels: ['9am', '12pm', '3pm', '6pm', '9pm', '12am', '3am', '6am'],
            value: [390, 310, 460, 250, 240, 200, 675, 410]
          }
        }
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
    setZoomLevel () {
      window.toolkit.surface.setZoom(1.0)
    },
    showArgumentData (data) {
      var me = this
      this.argumentview = !this.argumentview
      console.log("showArgumentData", data)
      if (this.argumentview) {
        setTimeout(() => {
          if (me.$refs.jsonArgumentEditor) {
            const editor = me.$refs.jsonArgumentEditor.editor
            editor.session.setValue(data)
          }
        })
      }
    },
    removePort (objid, col) {
      const _port = window.toolkit.getNode(objid).getPort(col)
      window.toolkit.removePort(objid, col)
      const fname = _port.data.name.replace('function: ', '')

      if (!_port.data.argument) {
        for (const key in this.argobjects) {
          if (key.indexOf(fname + ':') === 0) {
            console.log('this is an arg')
            const arg = this.argobjects[key]
            delete this.ports[arg.name]
            delete this.argobjects[key]
          }
        }
      }
      this.argports[col].forEach((portid) => {
        window.toolkit.removePort(objid, portid)
      })
      delete this.portobjects[col]
      delete this.argports[col]
    },
    updatePorts () {
      var me = this
      var node = window.designer.toolkit.getNode(this.obj)
      console.log('UPDATE PORTS', node.getPorts())

      node.getPorts().forEach((port) => {
        if (port.data.argument) {
          me.updateArgumentPort(port)
        } else {
          me.updateFunctionPort(port)
        }
      })
    },
    updateColumns () {
      var me = this
      Object.entries(this.argobjects).forEach((tuple) => {
        const argobject = tuple[1]
        me.obj.columns.forEach((column) => {
          if (column.argument) {
            if (column.name === argobject.name && column.function === argobject.function) {
              if (argobject.data) {
                column.background = '#eee'
                column.data = argobject.data
              } else {
                column.background = 'white'
              }
            }
          }
        })
      })
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
    showGit () {
      this.getCommits()
      this.gitview = true
    },
    getCommits () {
      DataService.getCommits(this.obj.gitrepo.split('#')[0], this.obj.modulepath, this.$store.state.designer.token).then((result) => {
        this.gitdata = result.data
      })
    },
    doLogin () {
      var me = this

      // TODO: Temp code
      me.login = false

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
      addNewPort({ function: 'function: ' + func.name, args: func.args }, 'Output', 'outlet-icon')
    },
    showOutput (output) {
      console.log('showOutput', output)
      const editor = this.$refs.resultEditor.editor
      editor.session.setValue(output)
    },
    refreshResultsData () {

    },
    showResultsDialog () {
      this.viewResultsDialog = true
      this.refreshResultsData()
    },
    updateFunctions (data) {
      const re = /def (\w+)\s*\((.*?)\):/g

      var matches = data.matchAll(re)

      this.funcs = []
      for (const match of matches) {
        var name = match[0].split('(')[0].split(' ').at(-1)
        var args = match[2].split(',')

        var _args = []
        for (const arg of args) {
          if (arg.indexOf('*') > -1 || arg.indexOf('=') > -1) {
          } else {
            if (arg.indexOf(':') > -1) {
              arg = arg.split(':')[0]
            }
            if (arg.length > 0) {
              _args.push(arg)
            }
          }
        }
        this.funcs.push({ name: name, args: _args })
      }
    },
    fetchCode (callback) {
      var me = this
      var url = new URL(this.obj.gitrepo)
      console.log('FETCHCODE URL ', url)
      if (this.obj.gitrepo === undefined || this.obj.gitrepo.length === 0 || !this.obj.usegit) {
        console.log("Criteria not met", this.obj.gitrepo, this.obj.gitrepo.length, this.usegit)
        return
      }

      // TODO: Choose branch name
      var codeUrl = 'https://raw.githubusercontent.com/' + url.pathname + '/main/' + this.obj.modulepath
      http.get(codeUrl).then((response) => {
        console.log('CODE RESPONSE', response)

        me.obj.code = response.data
        // const re = /(def)\s(\w+)/g;
        me.updateFunctions(response.data)

        if (this.$refs.codeEditor) {
          const editor = this.$refs.codeEditor.editor

          if (editor) {
            editor.session.setValue(me.obj.code)
            callback(me.obj.code)
          }
        }
      })
    },
    confirmFetch () {
      if (this.obj.gitrepo === undefined || this.obj.gitrepo.length == 0) {
        return
      }
      if (this.obj.code && this.obj.code.length > 0) {
        this.confirmCodeFetch = true
      }
    },
    copyNode () {
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
      var me = this

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
    workerviewSetup () {
      var me = this
      setTimeout(() => {
        me.workersLoading = false
      }, 2000)
    },
    showPanel (view, show) {
      this.configview = false
      this.codeview = false
      this.dataview = false
      this.gitview = false
      this.workerview = false
      this.historyview = false
      this.consoleview = false
      this.environmentview = false
      this.scalingview = false
      this.notesview = false
      this.requirementsview = false
      this.logsview = false
      this.securityview = false

      this[view] = show
      if (this[view + 'Setup']) {
        this[view + 'Setup']()
      }
      var elems = document.querySelectorAll('.jtk-node')

      elems.forEach((el) => {
        if (el != this.$el) {
          el.style['z-index'] = 0
        }
      })
      elems.forEach((el) => {
        if (el != this.$el && el.jtk && el.jtk.node.getType() === 'border') {
          console.log('HIDING BORDER')
          el.style['z-index'] = -9999
        }
      })
      this.$el.style['z-index'] = 99999

      if (show) {
        // window.toolkit.surface.setZoom(1.0);

        var node = this.toolkit.getNode(this.obj)
        if (view === 'historyview') {
          console.log(this.myhistory)
        }
        if (view === 'gitview') {
          this.getCommits()
        }

        if (this.refreshDeployments) {
          this.refreshDeployments(true)
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
      var me = this

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
    notesEditorInit: function () {
      var me = this

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
    jsonArgumentEditorInit: function () {
      var me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.jsonArgumentEditor.editor
      editor.setAutoScrollEditorIntoView(true)
      editor.on('change', function () {
        me.updateFunctions(editor.getValue())
      })
    },
    jsonEditorInit: function () {
      var me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.jsonEditor.editor
      editor.setAutoScrollEditorIntoView(true)
      editor.on('change', function () {
        me.updateFunctions(editor.getValue())
      })
    },
    resultEditorInit: function () {
      var me = this

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
      var me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.codeEditor.editor
      editor.setAutoScrollEditorIntoView(true)
      if(this.obj.usegit) {
        editor.setReadOnly(true)
      } else {
        editor.setReadOnly(false)
      }
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

      port.queue = 'None'

      console.log('Port:', port)
      window.toolkit.addNewPort(this.obj.id, 'column', port)
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
    updateFunctionPort (port) {
      const fname = port.data.name.replace('function: ', '')
      this.portobjects['func:' + fname] = port.data

      this.portobjects[fname] = []
    },
    updateArgumentPort (port) {
      const fname = port.data.function
      this.portobjects[fname].push(port.data)
      this.argobjects[fname + ':' + port.data.name] = port.data
      this.ports[port.data.name] = true
      if (this.argports[port.id] === undefined) {
        this.argports[port.id] = []
      }
      this.argports[port.id].push(port.id)
      this.obj.columns.forEach((column) => {
        if (column.argument) {
          if (column.name === port.data.name && column.function === port.data.function) {
            column.data = null
            port.data.data = null
          }
        }
      })
    },
    addNewPort (func, type, icon) {
      var me = this

      var port = this.addPort({
        name: func.function,
        icon: icon,
        type: type
      })

      let prefix = 'func:'
      if (type === 'Error') {
        prefix = 'error:'
      }
      this.ports[func.function] = true
      this.argports[port.id] = []

      this.updateSchemas()

      if (type === 'Error') {
        this.errorobjects[port.id] = port
      }

      const fname = func.function.replace('function: ', '')
      me.portobjects[prefix + fname] = port

      me.portobjects[fname] = []
      func.args.forEach((arg) => {
        arg = arg.trim()
        var argport = this.addPort({
          name: arg,
          icon: 'fab fa-python',
          type: 'Input',
          argument: true,
          function: fname
        })
        // This holds the argument port keyed off function-name:argument-name
        // When incoming data events for arguments occur, it will reference the function:argument
        // so it can be associated with this port
        // Push the argument ports onto the function reference in order they appear
        me.portobjects[fname].push(argport)
        me.argobjects[fname + ':' + arg] = argport
        this.ports[arg] = true
        this.argports[port.id].push(argport.id)
      })
    },
    executeObject (portname, data) {
      var me = this
      const call = this.portobjects[portname].name.replace('function: ', '')
      let code = this.obj.code
      code = code + '\n' + call + '()'

      var start = Moment(new Date())
      const result = this.execute(code)
      result.then((res) => {
        let answer = res

        const end = Moment(new Date())
        const diff = end.diff(start)
        var time = Moment.utc(diff).format('HH:mm:ss.SSS')

        me.task_time = time

        tsdb.series('outBytes').insert(
          {
            bytes: res.length
          },
          Date.now()
        )
        me.updateBandwidthChart()
        // TODO: No longer need this, plugs returned explicitly from functions needing them
        // So check the response for dictionary with "plugs" key
        // const _plugs = window.pyodide.globals.get('plugs').toJs()
        debugger
        let _plugs = {}
        let _result = {}
        if (res === Object(res)) {
          answer = Object.fromEntries(res.toJs())
          _plugs = toObject(answer.plugs)
          _result = toObject(answer.result)
        }

        console.log('_PLUGS', _plugs)
        this.getNode().getPorts().forEach((port) => {
          if (port.data.type === 'Plug') {
            debugger
            if (_plugs.hasOwnProperty(port.data.name)) {
              const plug_result = _plugs.get(port.data.name)
              me.triggerRoute(port.data.id, plug_result, {})
            }
          }
        })
        if (res === Object(res)) {
          console.log('CODE CALL RESULT', _result, _plugs)
          this.$emit('message.received', {
            type: 'result',
            id: this.obj.id,
            function: call,
            output: JSON.stringify(_result)
          })
        }
      }, (error) => {
        debugger
        console.log('PYTHON ERROR', error)
      })
    },
    triggerError (portid, error) {
      const _port = window.toolkit.getNode(this.obj.id).getPort(portid)
      _port.getEdges().forEach((edge) => {
        const options = edge.target.data
        const target_id = edge.target.getNode().data.id
        const node = edge.target.getNode()
        const code = node.data.code
        debugger
        // TODO: Insert block JSON here
        window.root.$emit(target_id, code, options.function, options.name, error, this.obj)
      })
    },
    triggerRoute (portid, result, plugs) {
      debugger
      const _port = window.toolkit.getNode(this.obj.id).getPort(portid)
      _port.getEdges().forEach((edge) => {
        const options = edge.target.data
        const target_id = edge.target.getNode().data.id
        const node = edge.target.getNode()
        const code = node.data.code
        debugger
        // TODO: Insert block JSON here
        window.root.$emit(target_id, code, options.function, options.name, { result: result, plugs: plugs }, node.data)
      })
    },
    triggerObject (portname, result, plugs) {
      var me = this
      const reslen = result.toString().length
      const _result = JSON.parse(result)
      const _plugs = JSON.parse(plugs)

      tsdb.series('outBytes').insert(
        {
          bytes: result.toString().length
        },
        Date.now()
      )
      if (portname in this.portobjects) {
        const objectname = this.portobjects[portname].name.replace('function: ', '')
        const port = this.portobjects['func:' + objectname]
        const _port = window.toolkit.getNode(this.obj.id).getPort(port.id)
        _port.getEdges().forEach((edge) => {
          const options = edge.target.data
          const target_id = edge.target.getNode().data.id
          const node = edge.target.getNode()
          const code = node.data.code
          me.calls_out += 1
          me.bytes_out += reslen
          debugger
          // TODO: Insert block JSON here
          window.root.$emit(target_id, code, options.function, options.name, { result: _result, plugs: _plugs }, node.data)
        })
        me.bytes_out_5min.unshift(reslen)
        me.bytes_out_5min = me.bytes_out_5min.slice(0, 8)

        this.getNode().getPorts().forEach((port) => {
          if (port.data.type === 'Plug') {
            if (_plugs.hasOwnProperty(port.data.name)) {
              const plug_result = _plugs[port.data.name]
              me.triggerRoute(port.data.id, plug_result, {}) // plugs
            }
          }
        })
      } else {
        console.log('ERROR', 'No portname', portname)
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
