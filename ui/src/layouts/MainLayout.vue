<template>
  <q-layout view="lHh Lpr lFf">
    <q-inner-loading
      :showing="flowloading"
      style="z-index: 9999999;"
    >
      <q-spinner-gears
        size="50px"
        color="primary"
      />
    </q-inner-loading>
    <q-header elevated>
      <ToolPalette
        v-if="tools === 'code'"
        surface-id="flow1"
        selector="[data-node-type]"
        :nodes="this.stats.nodes"
        :agents="this.stats.agents"
        :queues="this.stats.queues"
        :processors="this.stats.processors"
        :tasks="this.stats.tasks"
        :cpus_total="this.stats.cpus_total"
        :deployments="this.stats.deployments"
        :cpus_running="this.stats.cpus_running"
        ref="toolPalette"
      />
      <ModelToolPalette
        v-if="tools === 'model'"
        surface-id="flow1"
        selector="[data-node-type]"
      />
      <q-toolbar
        class="bg-accent"
        style="min-height: 40px; padding: 0px;"
      >
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-list"
          label="0"
          @click="showStats('Statistics Table', 'statstable')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Statistics Table
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-bullseye"
          :label="transmittedSize"
          @click="showStats('Data Transmitted', 'datatransmitted')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Data Transmitted
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fas fa-satellite-dish"
          :label="messageCount"
          @click="showStats('Messages Transmitted', 'messagestransmitted')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Messages Transmitted
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="las la-play"
          :label="stats.processors_starting"
          @click="showStats('Starting Processors', 'startingprocessors')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Starting Processors
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-play"
          :label="stats.processors_running"
          @click="showStats('Running Processors', 'runningprocessors')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Running Processors
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-stop"
          :label="stats.processors_stopped"
          @click="showStats('Stopped Processors', 'stoppedprocessors')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Stopped Processors
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px;"
          icon="fa fa-warning invalid"
          :label="stats.processors_errored"
          @click="showStats('Errored Processors', 'erroredprocessors')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Errored Processors
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px; font-size: 1em;"
          :icon="mdiEmailFast"
          :label="queuedTasks"
          @click="showStats('Queued Tasks', 'queuedtasks')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Queued Tasks
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px; font-size: 1em;"
          :icon="mdiEmailAlert"
          :label="stats.tasks_failure"
          @click="showStats('Errored Tasks', 'erroredtasks')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Errored Tasks
          </q-tooltip>
        </q-btn>
        <q-btn
          color="secondary"
          flat
          size="sm"
          class="text-dark"
          style="padding: 0px; height: 40px; font-size: 1em;"
          :icon="mdiEmailCheck"
          :label="stats.tasks_success"
          @click="showStats('Completed Tasks', 'completedtasks')"
          :disabled="!hasHosted"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Completed Tasks
          </q-tooltip>
        </q-btn>
        <!--
        <q-separator
          vertical
          inset
          color="primary"
        />
        <q-btn-toggle
          v-model="tools"
          class="my-custom-toggle"
          no-caps
          flat
          dense
          size="sm"
          padding="1em"
          unelevated
          :ripple="false"
          toggle-color="dark"
          color="white"
          text-color="secondary"
          :options="[
            { icon: 'fa fa-database', value: 'model' },
            { icon: 'fab fa-python', value: 'code' },
          ]"
          :disabled="getVersion() === 'FREE'"
        >
        <template #one>
          <div style="font-size: 0.5em; margin-left: 20px;">
            <q-tooltip
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Database Tools
            </q-tooltip>
          </div>
        </template>
        <template #two>
          <div style="font-size: 0.5em; margin-left: 20px;" />

          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Python Tools
          </q-tooltip>
        </template>
        </q-btn-toggle>-->
        <q-space />
        <q-btn
          v-if="$auth.isAuthenticated"
          dense
          flat
          color="secondary"
          @click="chooseplan = true"
        >
          Upgrade Plan
        </q-btn>
        <q-btn
          v-if="!$auth.isAuthenticated"
          dense
          flat
          color="secondary"
          @click="chooseplan = true"
        >
          Subscribe
        </q-btn>

        <q-input
          dark
          dense
          standout
          v-model="text"
          placeholder="Search..."
          style="width: 20%; border-left: 1px solid lightgrey;"
          input-class="text-left text-dark"
          class="q-ml-md text-dark bg-white"
          @keyup="searchString"
        >
          <template #append>
            <q-icon
              color="dark"
              size="sm"
              v-if="text === ''"
              name="search"
            />
            <q-icon
              v-else
              name="clear"
              color="dark"
              size="sm"
              class="cursor-pointer text-dark"
              @click="text = ''"
            />
          </template>
        </q-input>
      </q-toolbar>
    </q-header>

    <q-splitter
      v-model="splitterModel"
      vertical
      :limits="[60, 100]"
      unit="%"
      style="overflow: hidden;"
    >
      <template #before>
        <div style="height: 100vh; width: 100%; position: relative; top: 95px; overflow: hidden;">
          <q-tab-panels
            v-model="tab"
            keep-alive
            v-for="flow in flows"
            :key="flow.id"
          >
            <q-tab-panel
              :name="'flow' + flow.id"
              style="height: calc(100vh - 165px); padding: 0px; overflow: hidden;"
              :ref="'flow' + flow.id"
            >
              <Designer
                :ref="'flow' + flow.id + 'designer'"
                :flowcode="flow.code"
                :flowname="flow.filename"
                @update-name="updateFlow"
                :flowuuid="flow._id"
                :flowid="flow.id"
                :surface-id="'flow' + flow.id"
                showtoolbar="true"
                navigate="true"
              />
            </q-tab-panel>
          </q-tab-panels>
          <q-tabs
            v-model="tab"
            dense
            class="bg-primary"
            align="left"
            @input="tabChanged"
            narrow-indicator
            active-color="dark"
            indicator-color="accent"
            active-bg-color="accent"
          >
            <q-tab
              v-for="flow in flows"
              :key="flow.id"
              :name="'flow' + flow.id"
              class="text-dark"
              :label="flow.filename"
            >
              <!--<q-btn
            flat
            dense
            size="xs"
            icon="close"
            style="position: absolute; right:-15px;top:5px"
          />-->
            </q-tab>
          </q-tabs>
          <q-btn
            flat
            dense
            size="md"
            color="primary"
            icon="menu"
            aria-label="Menu"
            style="z-index: 9999; position: absolute; right: 0px;"
            @click="drawer = !drawer"
          />
        </div>
      </template>
      <template #after>
        <div style="height: 100vh; width: 100%; padding-top: 5px; position: relative; top: 95px; overflow: hidden;">
          <q-tabs
            v-model="drawertab"
            dense
            class="bg-primary"
            align="left"
            @input="tabChanged"
            narrow-indicator
            active-color="dark"
            indicator-color="primary"
            active-bg-color="accent"
          >
            <q-tab
              name="messages"
              class="text-dark"
              label="Messages"
            />
            <q-tab
              name="queues"
              class="text-dark"
              label="Queues"
            />
            <q-tab
              name="monitor"
              class="text-dark"
              label="Monitor"
              disable
            />
            <q-tab
              name="error"
              class="text-dark"
              label="Errors"
              disable
            />
          </q-tabs>
          <q-tab-panels
            v-model="drawertab"
            keep-alive
          >
            <q-tab-panel
              name="messages"
              ref="messages"
              style="padding: 0px; width: 100%; padding-top: 0px; height: calc(100vh - 170px);"
            >
              <q-table
                dense
                :columns="messageColumns"
                :data="msglogs"
                row-key="name"
                flat
                virtual-scroll
                :pagination="initialPagination"
                style="height: 100%; width: 100%; border-top-radius: 0px; border-bottom-radius: 0px;"
              />
            </q-tab-panel>
            <q-tab-panel
              name="queues"
              ref="queues"
              style="padding: 0px; width: 100%; padding-top: 0px; height: calc(100vh - 130px);"
            >
              <q-splitter
                v-model="queueTableSplitter"
                separator-style="background-color: #e3e8ec;height:5px"
                horizontal
                style="height: calc(100% - 40px);"
              >
                <template #before>
                  <q-table
                    dense
                    :data="queues"
                    :columns="columns"
                    row-key="name"
                    :rows-per-page-options="[50]"
                    virtual-scroll
                    style="height: calc(100vh - 170px);"
                  >
                    <template #body="props">
                      <q-tr :props="props">
                        <q-td
                          key="name"
                          :props="props"
                          :width="150"
                        >
                          <a
                            class="text-secondary"
                            style="z-index: 99999; cursor: pointer; width: 100%; min-width: 250px; font-size: 1.3em;"
                            @click="showQueueDetail(props.row.name)"
                          >
                            {{ props.row.name }}
                          </a>
                        </q-td>
                        <q-td
                          key="messages"
                          :props="props"
                        >
                          {{ props.row.messages }}
                        </q-td>
                        <q-td
                          key="ready"
                          :props="props"
                        >
                          <a
                            class="text-secondary"
                            style="z-index: 99999; cursor: pointer; width: 100%; min-width: 250px; font-size: 1.3em;"
                            @click="
                              queuename = props.row.name;
                              viewQueueDialog = true;
                            "
                          >
                            {{ props.row.ready }}
                          </a>
                        </q-td>
                        <q-td
                          key="unacked"
                          :props="props"
                        >
                          {{ props.row.unacked }}
                        </q-td>
                        <!--
                        <q-td key="incoming" :props="props">{{ props.row.incoming }}</q-td>
                        <q-td key="delivered" :props="props">{{ props.row.deliver_rate }}</q-td>
                        <q-td key="acked" :props="props">{{ props.row.acked_rate }}</q-td>-->
                        <q-td
                          key="bytes"
                          :width="200"
                          :props="props"
                        >
                          {{ props.row.bytes }}
                        </q-td>
                        <q-td
                          key="actions"
                          :props="props"
                          style="width: 25px;"
                        >
                          <q-btn
                            flat
                            round
                            dense
                            size="sm"
                            class="bg-white text-primary"
                            :id="props.row.name"
                            width="100"
                            icon="remove_circle"
                            @click="showPurgeConfirm(props.row.name)"
                          >
                            <q-tooltip
                              content-class=""
                              content-style="font-size: 16px"
                              :offset="[10, 10]"
                            >
                              Purge Messages
                            </q-tooltip>
                          </q-btn>
                          <q-btn
                            flat
                            round
                            dense
                            size="sm"
                            class="bg-white text-primary"
                            :id="props.row.name"
                            width="100"
                            icon="fas fa-cog"
                          >
                            <q-tooltip
                              content-class=""
                              content-style="font-size: 16px"
                              :offset="[10, 10]"
                            >
                              Configure
                            </q-tooltip>
                          </q-btn>
                          <q-btn
                            flat
                            round
                            dense
                            size="sm"
                            class="bg-white text-primary"
                            :id="props.row.name"
                            width="100"
                            icon="delete"
                          >
                            <q-tooltip
                              content-class=""
                              content-style="font-size: 16px"
                              :offset="[10, 10]"
                            >
                              Delete Queue
                            </q-tooltip>
                          </q-btn>
                        </q-td>
                      </q-tr>
                    </template>
                  </q-table>
                </template>
                <template #after>
                  <q-tabs
                    v-model="queuedetailtab"
                    dense
                    class="bg-primary"
                    align="left"
                    narrow-indicator
                    active-color="dark"
                    indicator-color="primary"
                    active-bg-color="accent"
                  >
                    <q-tab
                      name="stats"
                      class="text-dark"
                      label="Stats"
                    />
                    <q-tab
                      name="json"
                      class="text-dark"
                      label="JSON"
                    />
                    <q-tab
                      name="history"
                      class="text-dark"
                      label="History"
                    />
                  </q-tabs>
                  <q-tab-panels
                    v-model="queuedetailtab"
                    keep-alive
                    style="height: 100%;"
                  >
                    <q-tab-panel
                      name="stats"
                      ref="stats"
                      style="padding: 0px; width: 100%; padding-top: 0px; height: 100%;"
                    >
                      <q-table
                        dense
                        :columns="queueDetailColumns"
                        :data="queueDetailData"
                        row-key="name"
                        flat
                        virtual-scroll
                        :pagination="initialPagination"
                        style="height: 100%; width: 100%; border-top-radius: 0px; border-bottom-radius: 0px;"
                      />
                    </q-tab-panel>
                    <q-tab-panel
                      name="json"
                      ref="json"
                      style="padding: 0px; width: 100%; padding-top: 0px; height: calc(100% - 25px);"
                      keep-alive
                    >
                      <editor
                        @init="queueDetailEditorInit"
                        style="font-size: 1.5em;"
                        lang="javascript"
                        theme="chrome"
                        ref="queueDetailEditor"
                        width="100%"
                        v-model="queueDetailContent"
                        height="100%"
                      />
                    </q-tab-panel>
                  </q-tab-panels>
                </template>
              </q-splitter>
            </q-tab-panel>
            <q-tab-panel
              name="monitor"
              ref="monitor"
              style="padding: 0px; width: 100%; padding-top: 0px;"
            />
            <q-tab-panel
              name="error"
              ref="error"
              style="padding: 0px; width: 100%; padding-top: 0px;"
            />
          </q-tab-panels>
        </div>
      </template>
    </q-splitter>
    <q-footer
      elevated
      style="
        background-color: rgba(249, 250, 251, 0.9);
        height: 32px;
        font-size: 16px;
        padding: 5px;
        font-weight: bold;
      "
    >
      <q-toolbar style="padding: 0px; margin-top: -12px;">
        <q-btn
          flat
          dense
          color="primary"
        >
          <q-item-label
            class="text-dark"
            style=""
          >
            {{ status }}
          </q-item-label>
        </q-btn>
        <q-space />

        <q-btn-toggle
          v-model="modeModel"
          push
          flat
          dense
          toggle-color="secondary"
          class="text-primary"
          style="margin-right: 40px;"
          :options="[
            { label: 'Disconnected', value: 'disconnected', slot: 'one' },
            { label: 'Connected', value: 'connected', slot: 'two' },
            { label: 'Streaming', value: 'streaming', slot: 'three' },
          ]"
        >
          <template #one>
            <q-icon :name="mdiFlashOutline" />
            <q-tooltip
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Disconnected
            </q-tooltip>
          </template>

          <template #two>
            <q-icon :name="mdiFlash" />
            <q-tooltip
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Connected
            </q-tooltip>
          </template>

          <template #three>
            <q-icon :name="mdiWavesArrowRight" />
            <q-tooltip
              content-style="font-size: 16px"
              content-class="bg-black text-white"
            >
              Streaming
            </q-tooltip>
          </template>
        </q-btn-toggle>
        <q-btn
          flat
          dense
          color="primary"
          icon="chat"
          @click="toggleChat"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            AI Chatbot
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          dense
          color="primary"
          icon="menu"
          @click="toggleSplitter"
        >
          <q-tooltip
            content-style="font-size: 16px"
            content-class="bg-black text-white"
          >
            Streaming Data
          </q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-footer>
    <q-drawer
      v-model="searchdrawer"
      side="right"
      bordered
      :width="512"
      style="overflow: hidden;"
    >
      <q-scroll-area style="height: calc(100vh - 300px); width: 100%;">
        <q-list separator>
          <q-item
            v-for="item in items"
            :key="item.id"
            :id="'row' + item.id"
          >
            <q-item-section avatar>
              <q-icon
                name="fas fa-microchip"
                class="text-secondary"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>
                <a
                  class="text-secondary"
                  style="z-index: 99999; cursor: pointer; width: 100%; min-width: 250px; font-size: 1.3em;"
                  @click="centerNode(item.id)"
                >
                  {{ item.name }}
                </a>
              </q-item-label>
              <q-item-label
                caption
                lines="2"
              >
                {{ item.description }}
              </q-item-label>
            </q-item-section>
            <q-space />
          </q-item>
        </q-list>
      </q-scroll-area>
      <q-inner-loading
        :showing="false"
        style="z-index: 9999999;"
      >
        <q-spinner-gears
          size="50px"
          color="primary"
        />
      </q-inner-loading>
    </q-drawer>
    <q-drawer
      v-model="chatdrawer"
      side="right"
      bordered
      :width="750"
      style="overflow: hidden;"
    >
      <q-tabs
        v-model="pythontabs"
        dense
        class="bg-primary"
        align="left"
        narrow-indicator
        active-color="dark"
        indicator-color="primary"
        active-bg-color="accent"
      >
        <q-tab
          name="pythonconsole"
          label="Scratchpad"
        />
        <q-tab
          name="chatconsole"
          label="AI Coder"
        />
      </q-tabs>

      <q-tab-panels
        v-model="pythontabs"
        keep-alive
      >
        <q-tab-panel
          name="pythonconsole"
          style="padding: 0px;"
          ref="pythonconsole"
        >
          <q-inner-loading
            :showing="true"
            v-if="!$auth.isAuthenticated"
            style="z-index:9999"
          >
            <q-item-label>Not Logged In</q-item-label>
          </q-inner-loading><Console />
        </q-tab-panel>
        <q-tab-panel
          name="chatconsole"
          style="padding: 0px;"
          ref="chatconsole"
        >
          <q-inner-loading
            :showing="true"
            v-if="!$auth.isAuthenticated || !isProPlan"
            style="z-index:9999"
          >
            <q-item-label v-if="!$auth.isAuthenticated">
              Not Logged In
            </q-item-label>
            <q-item-label v-if="$auth.isAuthenticated || !isProPlan">
              Upgrade to Pro Plan
            </q-item-label>
          </q-inner-loading>
          <q-toolbar
            class="bg-accent"
            style="padding: 0px; padding-left: 10px;"
          >
            <q-item-label
              style="
              font-size: 1.5em;
              font-family: 'Indie Flower', cursive;
              margin-top: 5px;
              margin-right: 1em;
            "
            >
              AI Coding Buddy
            </q-item-label>
          </q-toolbar>
          <q-input
            v-model="question"
            label="Hi! Ask me anything...I can even write code!"
            style="width:100%;padding:10px;resize: none !important;"
            type="textarea"
          />
          <q-toolbar>
            <q-space />
            <q-btn
              label="Go!"
              color="secondary"
              @click="sendChat"
              style="margin-right:30px;margin-bottom:30px"
            />
          </q-toolbar>
          <q-separator />
          <q-scroll-area style="height:calc(100vh - 420px);">
            <q-markdown :src="answer" />
            <q-inner-loading
              :showing="loadingchat"
              style="z-index: 9999999;"
            >
              <q-spinner-gears
                size="50px"
                color="primary"
              />
            </q-inner-loading>
          </q-scroll-area>
        </q-tab-panel>
      </q-tab-panels>
    </q-drawer>
    <q-drawer
      v-model="blocksdrawer"
      side="right"
      bordered
      :width="750"
      style="overflow: hidden;"
    >
      <q-tabs
        v-model="blockstabs"
        dense
        class="bg-primary"
        align="left"
        narrow-indicator
        active-color="dark"
        indicator-color="primary"
        active-bg-color="accent"
      >
        <q-tab
          name="blocksregistry"
          label="Blocks"
          icon="las la-cube"
        />
      </q-tabs>

      <q-tab-panels
        v-model="blockstabs"
        keep-alive
      >
        <q-tab-panel
          name="blocksregistry"
          style="display: grid;grid-gap: 10px;grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));justify-content: space-around;padding:10px"
          ref="blocksregistry"
        >
          <q-btn
            flat
            v-for="block in blocks"
            color="secondary"
            :key="block.data.id"
            :icon="block.data.node.icon"
            class="brightness text-primary"
            :id="'block'+block.data.id"
            style="cursor:pointer;font-size:2em;border-radius: 10px; border: 1px lightgrey solid; padding:20px"
            :disabled="!block.data.enabled"
          >
            <div style="font-size:18px;font-family: arial">
              {{ block.data.node.name }}
            </div>
          </q-btn>
          <q-inner-loading
            :showing="true"
            v-if="!$auth.isAuthenticated"
            style="z-index:9999"
          >
            <q-item-label>Not Logged In</q-item-label>
          </q-inner-loading>
        </q-tab-panel>
      </q-tab-panels>
    </q-drawer>
    <q-drawer
      v-model="librarydrawer"
      side="right"
      bordered
      :width="512"
      style="overflow: hidden;"
    >
      <Library
        :objecttype="'template'"
        :icon="'fas fa-wrench'"
        :collection="'library'"
        style="width: 100%;"
      />
    </q-drawer>
    <q-dialog
      v-model="infodialog"
      transition-show="none"
      persistent
    >
      <q-card style="width: 50vw; max-width: 30vw; overflow:hidden; height: 70vh; padding: 10px; padding-left: 30px; padding-top: 40px;">
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
              <q-item-label>{{ infotitle }}</q-item-label>
              <q-space />
              <q-btn
                class="text-primary"
                flat
                dense
                round
                size="sm"
                icon="fas fa-close"
                @click="infodialog = false"
                style="z-index: 10;"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-scroll-area style="height: calc(70vh - 50px); width: 100%;padding:20px">
          <div style="min-height:60vh" />
        </q-scroll-area>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="chooseplan"
      transition-show="none"
      persistent
    >
      <q-card style="width: 70vw; max-width: 40vw; overflow:hidden; height: 70vh; padding: 10px; padding-left: 30px; padding-top: 40px;">
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
              <q-item-label>Choose a Plan</q-item-label>
              <q-space />
              <q-btn
                class="text-primary"
                flat
                dense
                round
                size="sm"
                icon="fas fa-close"
                @click="chooseplan = false"
                style="z-index: 10;"
              />
            </q-toolbar>
          </div>
        </q-card-section>

        <q-scroll-area style="height: calc(100% - 20px); width: 100%;">
          <table
            style="width:100%;"
            cellpadding="10px"
          >
            <thead style="font-weight: bold">
              <tr>
                <td />
                <td>Guest</td>
                <td>Free</td>
                <td>Developer</td>
                <td>Pro</td>
                <td>Hosted</td>
                <td>Enterprise</td>
              </tr>
            </thead>
            <tr style="background-color: rgb(244, 246, 247) !important; border-top: 1px solid black">
              <td>
                Execute Data Flows <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Execute Data Flows')"
                />
              </td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td>
                Browser Execution <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Browser Execution')"
                />
              </td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr style="background-color: rgb(244, 246, 247) !important">
              <td>
                Save Data Flows <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Save Data Flows')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td>
                GIT Integration <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('GIT Integration')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr style="background-color: rgb(244, 246, 247) !important">
              <td>
                Generate Code <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Generate Code')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td>
                REST API <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('REST API')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr style="background-color: rgb(244, 246, 247) !important">
              <td>
                AI Assistant <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('AI Assistant')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td>
                Script Library <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Script Library')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr style="background-color: rgb(244, 246, 247) !important">
              <td>
                Patterns <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Patterns')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td>
                Secure Processors <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Secure Processors')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr style="background-color: rgb(244, 246, 247) !important">
              <td>
                Hosted Services <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Hosted Services')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td>
                Transactional <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Transactional')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr style="background-color: rgb(244, 246, 247) !important">
              <td>
                Co-Development <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Co-Development')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td>
                Streaming <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('Streaming')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr style="background-color: rgb(244, 246, 247) !important">
              <td>
                CLI <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('CLI')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td>
                On Prem <i
                  class="fas fa-info-circle text-secondary"
                  style="font-size:1em; cursor: pointer"
                  @click="info('On Prem')"
                />
              </td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-close2" /></td>
              <td><q-icon name="fas fa-check" /></td>
            </tr>
            <tr>
              <td />
              <td />
              <td>
                <q-btn
                  dense
                  padding="10px 15px"
                  size="md"
                  label="Register"
                  v-if="!$auth.isAuthenticated"
                  @click="login"
                />
              </td>
              <td>
                <q-btn
                  dense
                  padding="10px 15px"
                  size="md"
                  label="Upgrade"
                  v-if="$auth.isAuthenticated && this.sublevel[this.$store.state.designer.subscription] < DEVELOPER"
                  @click="upgrade('ec_developer-USD-Monthly')"
                />
                <q-btn
                  dense
                  padding="10px 15px"
                  size="md"
                  color="secondary"
                  label="My Plan"
                  v-if="$auth.isAuthenticated && this.$store.state.designer.subscription === 'ec_developer-USD-Monthly'"
                  @click="manage"
                />
              </td>
              <td>
                <q-btn
                  dense
                  padding="10px 15px"
                  size="md"
                  label="Upgrade"
                  v-if="$auth.isAuthenticated && this.sublevel[this.$store.state.designer.subscription] < PRO"
                  @click="upgrade('ec_pro-USD-Monthly')"
                />
                <q-btn
                  dense
                  padding="10px 15px"
                  size="md"
                  color="secondary"
                  label="My Plan"
                  v-if="$auth.isAuthenticated && this.$store.state.designer.subscription === 'ec_pro-USD-Monthly'"
                  @click="manage"
                />
              </td>
              <td>
                <q-btn
                  dense
                  padding="10px 15px"
                  size="md"
                  label="Contact Us"
                  v-if="$auth.isAuthenticated && this.sublevel[this.$store.state.designer.subscription] < HOSTED"
                  @click="contact"
                />
                <q-btn
                  dense
                  padding="10px 15px"
                  size="md"
                  color="secondary"
                  label="My Plan"
                  v-if="$auth.isAuthenticated && this.$store.state.designer.subscription === 'ec_hosted-USD-Yearly'"
                  @click="manage"
                />
              </td>
              <td>
                <q-btn
                  dense
                  padding="10px 15px"
                  size="md"
                  label="Contact Us"
                  v-if="$auth.isAuthenticated"
                  @click="contact"
                />
              </td>
            </tr>
          </table>
        </q-scroll-area>
        <q-card-actions align="left">
          <q-btn
            flat
            style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
            label="Manage"
            class="bg-secondary text-white"
            color="primary"
            @click="manage"
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
    <q-dialog
      v-model="viewQueueDialog"
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
              <q-item-label>Queue {{ queuename }}</q-item-label>
              <q-space />
              <q-btn
                class="text-primary"
                flat
                dense
                round
                size="sm"
                icon="fas fa-close"
                @click="viewQueueDialog = false"
                style="z-index: 10;"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-splitter
          v-model="queueSplitter"
          separator-style="background-color: #e3e8ec;height:5px"
          horizontal
          style="height: calc(100% - 40px);"
        >
          <template #before>
            <q-table
              dense
              :columns="queuecolumns"
              :data="queuedata"
              row-key="name"
              flat
              :pagination="queuePagination"
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
                      @click="showMessagePayload(props.row.payload)"
                    >
                      {{ props.cols[1].value }}
                    </a>
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
          </template>
        </q-splitter>
        <q-card-actions align="left">
          <q-btn
            style="position: absolute; bottom: 0px; left: 0px; width: 100px;"
            flat
            icon="refresh"
            class="bg-secondary text-dark"
            color="primary"
            @click="refreshQueues"
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
          :showing="queueloading"
          style="z-index: 99999;"
        >
          <q-spinner-gears
            size="50px"
            color="primary"
          />
        </q-inner-loading>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="newQueueDialog"
      persistent
    >
      <q-card style="padding: 10px; padding-top: 30px; width: 50%; height: 50%;">
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
              <q-item-label>New Queue</q-item-label>
              <q-space />
              <q-icon
                class="text-primary"
                name="far fa-envelope"
              />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section
          class="row items-center"
          style="height: 120px;"
        >
          <span class="q-ml-sm">Create queue form here</span>
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
            label="Create"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="newQueue"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog
      v-model="resolutiondialog"
      persistent
    >
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
              <q-item-label>
                <i
                  class="fas fa-exclamation"
                  style="margin-right:20px"
                />Recommended Resolution
              </q-item-label>
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
          <span class="q-ml-sm">
            Your current monitor resolution does not meet the recommended size of 2460x1440 for best user experience.
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 100px;"
            label="Ok"
            class="bg-secondary text-white"
            color="primary"
            @click="resolutiondialog = false"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="betanoticedialog"
      persistent
    >
      <q-card style="padding: 10px; padding-top: 30px;">
        <q-card-section
          class="bg-secondary"
          style="
            padding: 0px !important;
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
              margin-left: 0px;
              margin-top: -5px;
              margin-right: 0px;
              color: #fff;
            "
          >
            <q-toolbar class="bar">
              <q-space />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section
          class="row items-center"
          style="height: 450px;"
        >
          <span
            class="text-black q-ml-sm"
            style="color:black;margin-top: 30px;margin-bottom:30px"
          >
            <p
              style="font-size:20px"
              class="text-black"
            >Welcome to ElasticCode Early Access! We are glad you stopped by. It is important to understand this software is currently an incomplete development pre-release. Not all features are implemented in this version. Any feedback, bugs reports, or feature requests are highly encouraged! Please submit them <a
              style="text-decoration: underline; color:#6b8791"
              target="support"
              href="https://elasticcode.atlassian.net/servicedesk/customer/portals"
            >here</a></p>
            <br>
            <hr>
            <br>
            <p
              style="font-size:16px"
              class="text-black"
            ><b>NOTE</b>: If the app doesn't display fully on your display, trying scaling it down from your browser until it fits completely.</p>
            <br>
            <b>Recommended Settings:</b>
            <ul style="margin-left:40px">
              <li>Monitor Resolution 2560x1440 or higher resolution</li>
              <li>Google Chrome</li>
            </ul>
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            style="position: absolute; bottom: 0px; right: 0px; width: 150px;"
            label="I Understand"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog
      v-model="confirmQueuePurge"
      persistent
    >
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
              <q-item-label>Purge Queue</q-item-label>
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
            Are you sure you want to purge queue {{ purgeQueueName }}?
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
            @click="purgeQueue(purgeQueueName)"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>
<style>
.q-splitter__after, .q-splitter__before {
  overflow: hidden !important
}

textarea {
  resize: none !important;
}
.q-scrollarea__container {
  min-height: 40vh;
}
a.text-secondary:hover {
  cursor: pointer;
  text-decoration: underline;
}

.q-splitter__before {
  overflow: hidden;
}

.q-splitter__panel {
  overflow: hidden;
}

.q-toolbar {
  position: relative;
  padding: 0px;
  min-height: 50px;
  width: 100%;
}

icon-processor:before {
  content: "\e807";
}

[class^="icon-"]:before,
[class*=" icon-"]:before {
  font-family: "flowfont";
  font-style: normal;
  font-weight: normal;
  speak: none;
  display: inline-block;
  text-decoration: inherit;
  width: 1em;
  margin-right: 0.2em;
  text-align: center;
  font-variant: normal;
  text-transform: none;
  line-height: 1em;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
<script>
const { v4: uuidv4 } = require('uuid')
var dd = require('drip-drop')

import { defineComponent, ref } from '@vue/composition-api'
import Designer from 'src/pages/Designer.vue'
import ToolPalette from 'src/components/ToolPalette.vue'
import ModelToolPalette from 'src/components/ModelToolPalette.vue'
import Console from 'src/components/Console'
import { mdiBorderNoneVariant } from '@mdi/js'

import Library from 'src/components/Library.vue'
import Processors from 'components/Processors.vue'
import DataService from 'components/util/DataService'
import { Auth0Lock } from 'auth0-lock'

const chargebee = require('chargebee')

chargebee.configure({
  site: 'elasticcode-test',
  api_key: 'test_cd3cu6vRcuyFScdCW8W8Y3QU1HmrVZ7AaXEm'
})

var filesize = require('filesize')
const size = filesize.partial({ base: 2, standard: 'jedec' })

import { mappedGetters, mappedActions, Actions, Getters, State, mappedState } from 'src/store/Store'

import 'assets/css/font-awesome.min.css'
import 'assets/css/flowfont.css'
import 'assets/fonts/fontawesome-webfont.eot'
import 'assets/fonts/fontawesome-webfont.svg'
import 'assets/fonts/fontawesome-webfont.woff2'
import 'assets/fonts/fontawesome-webfont.woff'
import 'assets/fonts/flowfont2.woff2'

import {
  mdiFlash,
  mdiFlashOutline,
  mdiWavesArrowRight,
  mdiCodeBraces,
  mdiEmailFast,
  mdiEmailAlert,
  mdiEmailCheck
} from '@mdi/js'

import { io, Socket } from 'socket.io-client'

const socket = io('https://app.elasticcode.ai')

export default defineComponent({
  name: 'MainLayout',
  components: {
    editor: require('vue2-ace-editor'),
    Designer,
    ToolPalette,
    Console,
    ModelToolPalette,
    Processors,
    Library
  },
  created () {
    this.mdiEmailAlert = mdiEmailAlert
    this.mdiEmailFast = mdiEmailFast
    this.mdiEmailCheck = mdiEmailCheck
    this.mdiWavesArrowRight = mdiWavesArrowRight
    this.mdiFlashOutline = mdiFlashOutline
    this.mdiFlash = mdiFlash
    this.borderIcon = mdiBorderNoneVariant

    // Reset connection status to disconnected
    this.$store.commit('designer/setConnected', false)
    this.$store.commit('designer/setStreaming', false)

    const n = this.$q.notify

    this.$q.notify = function (opts) {
      n(opts)
      opts.message = new Date().toLocaleDateString('en-us', { hour: '2-digit', minute: '2-digit' }) + ' ' + opts.message
      me.$root.$emit('log.message', opts.message)
    }

    this.schemaIcon = mdiCodeBraces
    var me = this
    this.tab = 'flow' + this.flows[0].id
    window.layout = this

    this.listenGlobal()
  },
  watch: {
    '$auth.isAuthenticated': function (val) {
      var me = this
      if (val) {
        this.security.token().then((token) => {
          console.log('SET TOKEN', token)
          me.$store.commit('designer/setToken', token)
          me.updateSubscription()
        })
      }
    },
    connected: function (newv, oldv) {
      console.log('CONNECTED', oldv, newv)
      if (newv) {
        // This means that changes to the flow are committed back
        // to the database as they happen
      }
    },
    streaming: function (newv, oldv) {
      console.log('STREAMING', oldv, newv)
      if (newv) {
        // This means the flow is receiving streaming messages in real-time
        console.log('Turning on messages')
        this.listenGlobal()
      } else {
        socket.off('global')
        console.log('Turning off messages')
      }
    },
    viewQueueDialog: function (val) {
      if (val) {
        this.queueloading = true
        DataService.getMessages(this.queuename, this.$store.state.designer.token)
          .then((messages) => {
            this.queueloading = false
            this.queuedata = messages.data
            this.updateQueuedTasks()
          })
          .catch((err) => {
            this.queueloading = false
            // show error message
          })
      }
    },
    text: function (val) {
      if (this.text.length > 0) {
        this.searchdrawer = true
      } else {
        this.searchdrawer = false
      }
    }
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
    },
    modeModel: {
      get () {
        return this.mode
      },
      set (val) {
        var me = this
        this.mode = val

        if (val === 'disconnected') {
          me.$store.commit('designer/setConnected', false)
          me.$store.commit('designer/setStreaming', false)
        }
        if (val === 'connected') {
          me.$store.commit('designer/setConnected', true)
          me.$store.commit('designer/setStreaming', false)
        }
        if (val === 'streaming') {
          me.$store.commit('designer/setConnected', true)
          me.$store.commit('designer/setStreaming', true)
        }
        console.log('setMode', this.mode)
      }
    },
    connected () {
      return this.$store.state.designer.connected
    },
    streaming () {
      return this.$store.state.designer.streaming
    },
    status () {
      return this.$store.state.designer.message
    },
    getSurfaceId () {
      return window.toolkit.surfaceId
    }
  },
  methods: {
    checkResolution () {
      const x = window.screen.width * window.devicePixelRatio
      const y = window.screen.height * window.devicePixelRatio
      if (x < 2460 || y < 1440) {
        this.resolutiondialog = true
      }
    },
    hasEnterprise () {
      if (this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] === this.ENTERPRISE
      } else {
        return false
      }
    },
    updateSubscription () {
      var me = this
      DataService.getSubscriptions(this.$auth.user.name, this.$store.state.designer.token).then((subscriptions) => {
        if (subscriptions.error && subscription.subscription === false) {
          me.$store.commit('designer/setSubscription', 'Registered')
        }
        if (subscriptions.data && subscriptions.data.subscription.status !== 'cancelled') {
          subscriptions.data.subscription.subscription_items.forEach((subscription) => {
            console.log('SUBSCRIPTION', subscription)
            me.$store.commit('designer/setSubscription', subscription.item_price_id)
          })
        } else {
          me.$store.commit('designer/setSubscription', 'cancelled')
        }
      }).catch((error) => {
        me.notifyMessage(
          'dark',
          'error',
          'There was an error retrieving your subscription.'
        )
      })
    },
    info (title) {
      this.infotitle = title
      this.infodialog = true
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
    sendChat () {
      var me = this
      this.loadingchat = true
      DataService.askChat(this.question, this.$store.state.designer.token).then((answer) => {
        me.answer = answer.data
        console.log(me.answer)
        me.loadingchat = false
      }).catch((error) => {

      })
    },
    getToken () {
      debugger
      const accessToken = this.security.token()
      accessToken.then(function (result) {
        // here you can use the result of promiseB
        console.log('accessToken: ', result)
      })
    },
    checkout () {
      const cbInstance = Chargebee.getInstance()

      const cart = cbInstance.getCart()
      const planPriceId = 'ec_developer-USD-Monthly' // Plan price point ID is used to identify the product
      const planPriceQuantity = 1
      const product = cbInstance.initializeProduct(planPriceId, planPriceQuantity)
      cart.replaceProduct(product)

      cart.proceedToCheckout()
    },
    upgrade (plan) {
      this.upgradeDialog = false
      var me = this
      const cbInstance = Chargebee.getInstance()
      const cart = cbInstance.getCart()
      cart.setCustomer({ email: this.$auth.user.name })
      cbInstance.setCheckoutCallbacks(function (cart) {
        return {
          loaded: function () {
            console.log('checkout opened')
          },
          close: function () {
            console.log('checkout closed')
          },
          success: function (hostedPageId) {
            console.log('CART', JSON.parse(JSON.stringify(cart)))

            me.updateSubscription()
          },
          step: function (value) {
            // value -> which step in checkout
            console.log(value)
          }
        }
      })
      const product = cbInstance.initializeProduct(plan, 1)
      // product.addAddon({ id: 'worldmap' })
      // product.addAddon({ id: 'storyboard' })
      cart.replaceProduct(product)
      this.cart = cart
      this.cart.proceedToCheckout()
    },
    manage () {
      const cbInstance = Chargebee.getInstance()
      var cbPortal = cbInstance.createChargebeePortal()
      console.log('Subscriptions opened')
      cbInstance.setCheckoutCallbacks(function (cart) {
        return {
          loaded: function () {
            console.log('checkout opened')
          },
          close: function () {
            console.log('checkout closed')
            window.location.reload()
          },
          success: function (hostedPageId) {
            console.log('checkout success')

            me.updateSubscription()
          },
          step: function (value) {
            console.log('checkout step')
            // value -> which step in checkout
            console.log(value)
          }
        }
      })
      cbPortal.open({
        subscriptionCancelled: (data) => {
          console.log('subscription cancelled')

          // TODO: Show warning dialog about reload

          me.updateSubscription()
        },
        subscriptionReactivated: (data) => {
          console.log('subscription reactivated')

          me.updateSubscription()
        },
        subscriptionChanged: (data) => {
          console.log('subscription changed')

          me.updateSubscription()
        },
        close: () => {
          console.log('Portal closed')
        }
      })
    },
    login () {
      const dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : window.screenX
      const dualScreenTop = window.screenTop !== undefined ? window.screenTop : window.screenY

      const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width
      const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height
      const systemZoom = width / window.screen.availWidth
      const left = (width - 500) / 2 / systemZoom + dualScreenLeft
      const top = (height - 715) / 2 / systemZoom + dualScreenTop
      const popup = window.open(
        '',
        'auth0:authorize:popup',
        'left=' + left + ',top=' + top + ',width=500,height=715,scrollbars=no,resizable=no'
      )
      this.$auth.loginWithPopup(this.getToken, { popup })
    },
    showPurgeConfirm (name) {
      this.purgeQueueName = name
      this.confirmQueuePurge = true
    },
    showStats (name, objects) {
      console.log('showStats', objects)
      this.$root.$emit('show.objects', { name: name, objects: objects, columns: this.objectcolumns[objects] })
    },
    purgeQueue (name) {
      DataService.purgeQueue(name, this.$store.state.designer.token)
        .then((res) => {
          this.$q.notify({
            color: 'secondary',
            timeout: 2000,
            position: 'top',
            message: 'Purging Queue ' + name + '...',
            icon: 'fas fa-exclamation'
          })
        })
        .catch((res) => {
          this.$q.notify({
            color: 'secondary',
            timeout: 2000,
            position: 'top',
            message: 'Error Purging Queue ' + name,
            icon: 'fas fa-exclamation'
          })
        })
    },
    queueDetailEditorInit: function () {
      var me = this

      require('brace/ext/language_tools') // language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/python') // language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') // snippet
      const editor = this.$refs.queueDetailEditor.editor
      editor.setAutoScrollEditorIntoView(true)
    },
    showQueueDetail (name) {
      this.queueDetailData = this.queueDetails[name]
      // const editor = this.$refs.queueDetailEditor.editor;
      this.detailedqueues.forEach((queue) => {
        if (queue.name === name) {
          // editor.session.setValue(JSON.stringify(queue, null, "\t"));
          this.queueDetailContent = JSON.stringify(queue, null, '\t')
        }
      })
    },
    listenGlobal () {
      var me = this

      socket.on('global', (msg) => {
        // console.log('MAINLAYOUT', msg)
        if (msg.type && msg.type === 'DeploymentModel') {
          console.log('DEPLOYMENT WAS UPDATED ', msg)
          window.root.$emit('message.received', msg)
        }
        if (msg.type && msg.type === 'ProcessorModel') {
          // console.log('PROCESSOR WAS UPDATED ', msg)
          window.root.$emit('message.received', msg)
        }
        if (msg.channel === 'task') {
          me.msglogs.unshift(msg)
          me.msglogs = me.msglogs.slice(0, 200)

          window.root.$emit('message.count', 1)
          var bytes = JSON.stringify(msg).length
          window.root.$emit('message.size', bytes)
        } else if (msg.type && msg.type === 'stats') {
          me.stats = msg
        } else {
          var qs = []

          if (msg.type && msg.type === 'queues') {
            var queued_tasks = 0
            me.detailedqueues = msg.queues
            msg.queues.forEach((queue) => {
              if (queue.name.indexOf('celery') === -1) {
                var ack_rate = 0
                var deliver_rate = 0

                var properties = []
                if ('message_stats' in queue) {
                  ack_rate = queue.message_stats && queue.message_stats.ack_details ? queue.message_stats.ack_details.rate : 0
                  deliver_rate = queue.message_stats && queue.message_stats.deliver_get_details ? queue.message_stats.deliver_get_details.rate : 0
                }

                qs.push({
                  name: queue.name,
                  messages: queue.messages,
                  ready: queue.messages_ready,
                  acked_rate: ack_rate,
                  deliver_rate: deliver_rate,
                  unacked: queue.messages_unacknowledged,
                  ready_rate: queue.messages_ready_details,
                  unacked_rate: queue.messages_unacknowledged_details,
                  bytes: queue.message_bytes,
                  action: ''
                })

                properties.push({
                  name: 'Messages Ready',
                  value: queue.messages_ready
                })
                properties.push({
                  name: 'Messages Ackd',
                  value: queue.messages_ready
                })
                properties.push({
                  name: 'Avg Ack Ingress Rate',
                  value: parseFloat(queue.backing_queue_status.avg_ack_ingress_rate).toFixed(2)
                })
                properties.push({
                  name: 'Avg Ingress Rate',
                  value: parseFloat(queue.backing_queue_status.avg_ingress_rate).toFixed(2)
                })
                properties.push({
                  name: 'Avg Engress Rate',
                  value: parseFloat(queue.backing_queue_status.avg_egress_rate).toFixed(2)
                })
                properties.push({
                  name: 'Memory',
                  value: queue.memory
                })
                properties.push({
                  name: 'Message Bytes',
                  value: queue.message_bytes
                })
                properties.push({
                  name: 'Message Bytes Persistent',
                  value: queue.message_bytes_persistent
                })
                properties.push({
                  name: 'Message Bytes Ram',
                  value: queue.message_bytes_ram
                })
                properties.push({
                  name: 'Message Bytes Ready',
                  value: queue.message_bytes_ready
                })
                properties.push({
                  name: 'Message Bytes UnAckd',
                  value: queue.message_bytes_unacknowledged
                })
                properties.push({
                  name: 'Messages',
                  value: queue.messages
                })
                properties.push({
                  name: 'Messages Persistent',
                  value: queue.messages_persistent
                })
                properties.push({
                  name: 'Messages Ram',
                  value: queue.messages_ram
                })
                properties.push({
                  name: 'Messages Ready',
                  value: queue.messages_ready
                })
                properties.push({
                  name: 'Messages Ready Rate',
                  value: parseFloat(queue.messages_ready_details.rate).toFixed(2)
                })
                properties.push({
                  name: 'Messages UnAckd Rate',
                  value: parseFloat(queue.messages_unacknowledged_details.rate).toFixed(2)
                })
                properties.push({
                  name: 'Messages Ready Ram',
                  value: queue.messages_ready_ram
                })
                properties.push({
                  name: 'Node',
                  value: queue.node
                })

                this.queueDetails[queue.name] = properties
                queued_tasks += parseInt(queue.messages)
                this.queuedTasks = queued_tasks
              }
            })

            me.queues = qs
            window.root.$emit('update.queues', qs)
          }
        }
      })
    },
    showMessagePayload (payload) {
      const editor = this.$refs.resultEditor.editor
      editor.session.setValue(payload)
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
      })
    },
    centerNode (id) {
      window.toolkit.surface.centerOn(id, {
        doNotAnimate: true,
        onComplete: function () {
          window.toolkit.surface.pan(0, -200)
        }
      })
    },
    searchString () {
      console.log('Searching for', this.text)
      this.items = []
      this.graph.nodes.forEach((node) => {
        console.log('Searching node ', node)
        if (node.name && (node.name.indexOf(this.text) > -1 || node.description.indexOf(this.text) > -1)) {
          this.items.push(node)
        }
      })
    },
    transmitted () {
      var me = this
      setTimeout(() => {
        me.transmittedSize = size(this.messageSize)
        me.transmitted()
      }, 3000)
    },
    updateStats () {
      console.log('UPDATE STATS')

      var running = 0
      var stopped = 0

      if (window.toolkit) {
        var objs = window.toolkit.getGraph().serialize()

        console.log('OBJS', objs)
        objs.nodes.forEach((node) => {
          console.log('NODE', node)
          if (node.status === 'running') {
            running += 1
          }
          if (node.status === 'stopped') {
            stopped += 1
          }
        })
      }
      // this.stopped = stopped;
      // this.running = running;
      // this.groups = objs['groups'].length;
    },
    getUuid () {
      return 'key_' + uuidv4()
    },
    updateQueuedTasks () {
      var queued_tasks = 0

      this.queuedata.forEach((queue) => {
        console.log('QUEUE', queue)
        queued_tasks += parseInt(queue.messages)
      })

      console.log('QUEUED TASKS', queued_tasks)
      this.queuedTasks = queued_tasks
    },
    refreshQueues () {
      this.queueloading = true
      console.log('QUEUES REFRESHING')
      DataService.getMessages(this.queuename, this.$store.state.designer.token)
        .then((messages) => {
          this.queueloading = false
          this.queuedata = messages.data
          this.updateQueuedTasks()
        })
        .catch((err) => {
          this.queueloading = false
          // show error message
        })
    },
    toggleSplitter () {
      this.librarydrawer = false
      if (this.splitterModel < 100) {
        this.splitterSave = this.splitterModel
        this.splitterModel = 100
      } else {
        this.splitterModel = this.splitterSave
      }
    },
    toggleChat () {
      this.chatdrawer = !this.chatdrawer
    },
    updateFlow (name) {
      this.flow.filename = name
    },
    tabChanged (tab) {
      var me = this

      console.log('REFS:', this.$refs)
      console.log('TAB:', tab, this.$refs[tab])
      for (var i = 0; i < this.flows.length; i++) {
        var flow = this.flows[i]
        if (tab === 'flow' + flow.id) {
          this.flow = flow
        }
      }

      console.log('GRAPH', this.graph)
      if (this.$refs[tab + 'designer']) {
        window.toolkit = this.$refs[tab + 'designer'][0].toolkit
        window.toolkit.$q = this.$q
        this.graph = window.toolkit.getGraph().serialize()
        window.renderer = window.toolkit.renderer
        console.log('Refreshing designer')
        this.$refs[tab + 'designer'][0].redraw() // TODO: refresh
      }
    }
  },
  mounted () {
    var me = this
    this.checkResolution()

    DataService.getCommit().then( (response) => {
      console.log("COMMIT", response)
      let hash = response.data.split('|')[0]
      let buildDate = response.data.split('|')[1]
      let buildUrl = response.data.split('|')[2]
      let repoUrl = response.data.split('|')[3]
      this.$refs.toolPalette.setCommit(hash, buildDate, buildUrl, repoUrl)
    })
    // console.log('MAINLAYOUT MESSAGE', this.$store.state.designer.message);
    // console.log('MAINLAYOUT STORE', this.$store);
    window.designer.$root.$on('toolkit.dirty', () => {
      this.updateStats()
    })
    console.log('STATUS: CONNECTED', this.connected)

    if (this.$auth.isAuthenticated) {
      this.security.token().then((token) => {
        console.log('SET TOKEN', token)
        me.$store.commit('designer/setToken', token)
        DataService.getQueues(token).then((queues) => {
          me.queues = queues.data
          window.root.$emit('update.queues', queues.data)
        })
        me.updateSubscription()
      })
    }

    this.transmitted()
    window.root.$on('message.count', (count) => {
      me.messageCount += count
    })
    window.root.$on('message.size', (size) => {
      me.messageSize += size
    })
    this.$root.$on('flow.uuid', (flowid, flowuuid) => {
      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i]
        if (flow.id === flowid) {
          flow._id = flowuuid
          console.log('Updated flow', flow, ' with uuid', flowuuid)
        }
      }
    })
    window.root.$on('view.queue', (queue) => {
      this.queuename = queue
      this.viewQueueDialog = true
    })
    this.$root.$on('login', this.login)
    this.$root.$on('manage.subscription', this.manage)
    this.$root.$on('upgrade.subscription', this.upgrade)
    this.$root.$on('checkout', this.checkout)

    this.$root.$on('open.blocks', () => {
      this.blocksdrawer = !this.blocksdrawer
    })
    this.$root.$on('open.chat', () => {
      this.chatdrawer = !this.chatdrawer
    })

    this.$root.$on('open.library', () => {
      console.log('open.library')
      this.librarydrawer = !this.librarydrawer
    })
    this.$root.$on('new.queue', () => {
      console.log('NEW.QUEUE')
      this.newQueueDialog = true
    })

    this.$root.$on('close.flow', (flowid) => {
      console.log('DELETING FLOWID', flowid)
      console.log('BEFORE DELETE', me.flows)
      var index = -1
      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i]
        if (flow.id === flowid) {
          index = i
          break
        }
      }
      me.flows = me.flows.filter(function (value, index, arr) {
        console.log(value.id, flowid)
        return value.id !== flowid
      })
      this.tab = 'flow' + me.flows[index - 1].id
      this.$refs[this.tab + 'designer'][0].refresh()
      console.log('AFTER DELETE', me.flows)
    })
    this.$root.$on('new.flow', () => {
      var id = me.flows.length + 1
      me.flows.push({
        filename: 'New Flow',
        id: id,
        code: null
      })
      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i]
        if (flow.id === id) {
          me.flow = flow
        }
      }
      me.tab = 'flow' + id
      setTimeout(() => {
        me.tabChanged(me.tab)
      })
    })
    this.$root.$on('loading.flow', () => {
      me.flowloading = true
    })
    this.$root.$on('load.flow', (flow) => {
      console.log('load.flow', flow)
      me.flowloading = false
      var id = me.flows.length + 1
      flow._id = flow._id
      flow.id = id
      me.flows.push(flow)
      me.tab = 'flow' + id

      setTimeout(() => {
        me.tabChanged(me.tab)
      })
    })
    console.log('Mounting....')
    console.log('REFS', this.$refs)
    window.toolkit = this.$refs.flow1designer[0].toolkit
    window.toolkit.$q = this.$q
    window.renderer = window.toolkit.renderer
    window.toolkit.load({
      type: 'json',
      url: '/scratch.json',
      onload: function () {
        // called after the data has loaded.
        window.toolkit.surface.setZoom(1.0)
        window.toolkit.surface.zoomToFit({ fill: 0.75 })
        window.toolkit.surface.setPan(0, 0, false)
        window.toolkit.surface.setPan(0, 0, false)
        window.toolkit.surface.setPan(0, 0, false)
        me.graph = window.toolkit.getGraph().serialize()
      }
    })
    setTimeout(() => {
      var script = document.querySelector('#script')

      script.data = {
        id: 1,
        enabled: true,
        node: {
          icon: 'las la-scroll',
          style: '',
          type: 'script',
          name: 'Script',
          label: 'Script',
          description: 'A script description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }
      var api = document.querySelector('#api')

      api.data = {
        id: 2,
        enabled: true,
        node: {
          icon: 'las la-cloud-upload-alt',
          style: '',
          type: 'api',
          name: 'API',
          label: 'API',
          description: 'A web API',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var border = document.querySelector('#border')

      border.data = {
        id: 3,
        enabled: true,
        node: {
          style: '',
          icon: this.borderIcon,
          type: 'border',
          name: 'Border',
          label: 'Border'
        }
      }

      var processor = document.querySelector('#processor')

      processor.data = {
        id: 4,
        enabled: this.hasHosted,
        node: {
          icon: 'icon-processor',
          style: '',
          type: 'processor',
          name: 'Processor',
          label: 'Script',
          description: 'A script processor description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var markdown = document.querySelector('#markdown')

      markdown.data = {
        id: 5,
        enabled: true,
        node: {
          icon: 'lab la-markdown',
          style: '',
          type: 'markdown',
          name: 'Markdown',
          label: 'Markdown',
          description: 'A markdown block',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var portin = document.querySelector('#portin')
      portin.data = {
        id: 6,
        enabled: this.hasHosted,
        node: {
          icon: 'icon-port-in',
          style: 'size:50px',
          type: 'portin',
          name: 'Port In',
          label: 'Port In',
          description: 'A port in description',
          package: 'queue name',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var portout = document.querySelector('#portout')
      portout.data = {
        id: 7,
        enabled: this.hasHosted,
        node: {
          icon: 'fas fa-plug',
          style: 'size:50px',
          type: 'portout',
          name: 'Port Out',
          label: 'Port Out',
          description: 'A port out description',
          package: 'queue name',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var group = document.querySelector('#processorgroup')
      group.data = {
        id: 8,
        enabled: true,
        node: {
          icon: 'far fa-object-group',
          style: 'size:50px',
          type: 'group',
          name: 'Group',
          label: 'Group',
          description: 'A processor group description',
          package: 'my.python.package',
          disabled: false,
          group: true,
          columns: [],
          properties: []
        }
      }
      /*
      var parallel = document.querySelector('#parallel')
      parallel.data = {
        node: {
          icon: 'fas fa-list',
          style: 'size:50px',
          type: 'parallel',
          name: 'Parallel',
          label: 'Parallel',
          description: 'A parallel tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var pipeline = document.querySelector('#pipeline')
      pipeline.data = {
        node: {
          icon: 'fas fa-long-arrow-alt-right',
          style: 'size:50px',
          type: 'pipeline',
          name: 'Pipeline',
          label: 'Pipeline',
          description: 'A pipeline tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var segment = document.querySelector('#segment')
      segment.data = {
        node: {
          icon: 'grid_view',
          style: 'size:50px',
          type: 'segment',
          name: 'Segment',
          label: 'Segment',
          description: 'A segment tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var chord = document.querySelector('#chord')
      chord.data = {
        node: {
          icon: 'low_priority',
          style: 'size:50px',
          type: 'chord',
          name: 'Chord',
          label: 'Chord',
          description: 'A chord tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }
*/
      var label = document.querySelector('#label')
      label.data = {
        id: 9,
        enabled: true,
        node: {
          icon: 'icon-label',
          style: 'size:50px',
          type: 'note',
          name: 'Label',
          label: 'Label',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var data = document.querySelector('#data')
      data.data = {
        id: 10,
        enabled: true,
        node: {
          icon: 'las la-file-alt',
          style: 'size:50px',
          type: 'data',
          name: 'Data',
          label: 'Data',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var schema = document.querySelector('#schema')
      schema.data = {
        id: 11,
        enabled: this.hasHosted,
        node: {
          icon: this.schemaIcon,
          style: 'size:50px',
          type: 'schema',
          name: 'Schema',
          label: 'Schema',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      var router = document.querySelector('#router')
      router.data = {
        id: 12,
        enabled: this.hasHosted,
        node: {
          icon: 'alt_route',
          style: 'size:50px',
          type: 'router',
          name: 'Router',
          label: 'Router',
          disabled: false,
          columns: [],
          properties: []
        }
      }

      //, chord, segment, map, reduce
      var els = [script, api, processor, markdown, portin, router, portout, group, label, data, schema, border]

      this.blocks = els

      els.forEach((el) => {
        var data = el.data
        //data.id = uuidv4()
        var draghandle = dd.drag(el, {
          image: true // default drag image
        })
        draghandle.on('start', function (setData, e) {
          setData('object', JSON.stringify(data))
        })
      })

      setTimeout( () => {
        this.blocks.forEach((el) => {
          const _el = document.querySelector('#block' + el.data.id)
          if (el.data.enabled) {
            var data = el.data
            var draghandle = dd.drag(_el, {
              image: true // default drag image
            })
            draghandle.on('start', function (setData, e) {
              setData('object', JSON.stringify(data))
            })
          }
        })
      })

    })
    var me = this

    this.$root.$on('update.tab', () => {
      me.tabChanged(me.tab)
    })
    window.designer.$root.$on('node.added', (node) => {
      me.tabChanged(me.tab)
    })
  },
  data () {
    return {
      sublevel: {
        guest: 0,
        free: 1,
        'ec_developer-USD-Monthly': 2,
        'ec_pro-USD-Monthly': 3,
        'ec_hosted-USD-Yearly': 4
      },
      blocks: [
      ],
      blockstabs: 'blocksregistry',
      GUEST: 0,
      FREE: 1,
      DEVELOPER: 2,
      PRO: 3,
      HOSTED: 4,
      ENTERPRISE: 5,
      loadingchat: false,
      answer: '',
      infodialog: false,
      infotitle: '',
      separator: ref('vertical'),
      chooseplan: false,
      flowloading: false,
      purgeQueueName: null,
      confirmQueuePurge: false,
      queueDetailContent: '',
      queueDetailColumns: [
        {
          name: 'name',
          label: 'Property',
          field: 'name',
          align: 'left'
        },
        {
          name: 'value',
          label: 'Value',
          field: 'value',
          align: 'left'
        }
      ],
      queueDetailData: [],
      queuedetailtab: 'stats',
      objectcolumns: {
        runningprocessors: [
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
        ]
      },
      queueTableSplitter: 40,
      detailedqueues: [],
      queuedTasks: 0,
      mode: 'disconnected',
      messageContent: '',
      graph: {},
      items: [],
      messageCount: 0,
      messageSize: 0,
      transmittedSize: 0,
      stats: {
        nodes: 0,
        agents: 0,
        queues: 0,
        processors: 0,
        cpus_total: 0,
        deployments: 0,
        cpus_running: 0,
        processors_starting: 0,
        processors_running: 0,
        processors_errored: 0,
        tasks: 0
      },
      running: 0,
      stopped: 0,
      groups: 0,
      librarydrawer: false,
      chatdrawer: false,
      blocksdrawer: false,
      newQueueDialog: false,
      pythontabs: 'pythonconsole',
      messagedrawer: false,
      queueloading: false,
      queueSplitter: 50,
      messageSplitter: 70,
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
      queuedata: [],
      queueDetails: {},
      initialPagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 50
        // rowsNumber: xx if getting data from a server
      },

      queuePagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 20
        // rowsNumber: xx if getting data from a server
      },
      viewQueueDialog: false,
      betanoticedialog: true,
      chatModel: 40,
      splitterModel: 100,
      splitterSave: 73,
      messageColumns: [
        {
          name: 'date',
          label: 'Date',
          field: 'date',
          align: 'left'
        },
        {
          name: 'channel',
          label: 'Channel',
          field: 'channel',
          align: 'left'
        },
        {
          name: 'module',
          label: 'Module',
          field: 'module',
          align: 'left'
        },
        {
          name: 'task',
          label: 'Task',
          field: 'task',
          align: 'left'
        },
        {
          name: 'room',
          label: 'Room',
          field: 'room',
          align: 'left'
        },
        {
          name: 'state',
          label: 'State',
          field: 'state',
          align: 'left'
        },
        {
          name: 'duration',
          label: 'Duration',
          field: 'duration',
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
          name: 'messages',
          align: 'center',
          label: 'Messages',
          field: 'messages'
        },
        {
          name: 'ready',
          align: 'center',
          label: 'Ready',
          field: 'ready'
        },
        {
          name: 'unacked',
          align: 'center',
          label: 'Not Acked',
          field: 'unacked'
        }, /*        {
          name: "incoming",
          align: "center",
          label: "Incoming/sec",
          field: "incoming",
        },
        {
          name: "delivered",
          align: "center",
          label: "Delivered/sec",
          field: "delivered",
        },
        {
          name: "acked",
          align: "center",
          label: "Acked/sec",
          field: "acked",
        }, */
        {
          name: 'bytes',
          align: 'right',
          classes: 'text-secondary',
          label: 'Bytes',
          field: 'bytes'
        },
        {
          name: 'actions',
          align: 'center',
          style: 'min-width:150px',
          classes: 'text-secondary',
          label: 'Actions'
        }
      ],
      queues: [],
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
      jsondata: {},
      msglogs: [],
      searchdrawer: false,
      flows: [
        {
          filename: 'Scratch Flow',
          id: 1
        }
      ],
      drawertab: 'messages',
      drawer: true,
      tab: 'flow1',
      tools: 'code',
      question: '',
      text: ''
    }
  }
})
</script>
