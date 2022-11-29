<template>
  <div
    class="fit"
    style="padding: 0; height: 100vh;"
  >
    <div
      class="bg-accent text-secondary"
      style="border-bottom: 1px solid #abbcc3; overflow: hidden;"
    >
      <q-inner-loading
        :showing="true"
        v-if="!$auth.isAuthenticated"
        style="z-index:9999"
      >
        <q-item-label>Not Logged In</q-item-label>
      </q-inner-loading>
      <q-toolbar style="padding: 0px; padding-left: 20px;">
        <q-btn
          flat
          :icon="expandAll"
          size="sm"
          dense
          color="secondary"
          class="q-mr-xs"
          style="padding: 0;"
          @click="expandAllNodes"
        >
          <q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Expand All
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          dense
          :icon="collapseAll"
          size="sm"
          color="secondary"
          class="q-mr-xs"
          style="padding: 0;"
          @click="collapseAllNodes"
        >
          <q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Collapse All
          </q-tooltip>
        </q-btn>
        <q-btn
          flat
          dense
          :icon="cardOutline"
          size="sm"
          color="secondary"
          class="q-mr-xs"
          style="padding: 0;"
          @click="$root.$emit('toggle.card')"
        >
          <q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Show Card
          </q-tooltip>
        </q-btn>
        <q-space />

        <q-btn
          flat
          round
          icon="fas fa-sync-alt"
          size="xs"
          color="primary"
          class="q-mr-xs"
          style="padding: 0;"
          @click="synchronize"
        >
          <q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Refresh
          </q-tooltip>
        </q-btn>
      </q-toolbar>
    </div>
    <q-scroll-area style="height: calc(100vh - 300px);">
      <q-tree
        :nodes="nodes"
        dense
        ref="tree"
        node-key="id"
        no-nodes-label="No networks available"
        class="text-secondary"
      >
        <template v-slot:default-header="prop">
          <div
            class="row items-center rapidquestnode"
            :id="prop.node.id"
          >
            <q-icon
              :name="prop.node.icon || 'share'"
              size="18px"
              class="q-mr-sm text-dark"
            />
            <div
              class="text-secondary network-node"
              :id="prop.node.id"
              style="font-size: 1.2em;"
              @mouseover="updateCard(prop.node)"
            >
              {{ prop.node.label }}
              <q-tooltip
                content-class=""
                content-style="font-size: 16px"
                anchor="top left"
                self="bottom middle"
                :offset="[10, 10]"
              >
                {{ prop.node.tooltip }}
              </q-tooltip>
            </div>
          </div>
        </template>
      </q-tree>
    </q-scroll-area>
    <q-inner-loading :showing="loading">
      <q-spinner-gears
        size="50px"
        color="primary"
      />
    </q-inner-loading>
    <q-toolbar
      v-if="toolbar"
      class="fixed-bottom bg-black text-white"
    >
      <q-btn
        flat
        round
        icon="fas fa-sync-alt"
        class="q-mr-xs"
        @click="synchronize"
      >
        <q-tooltip
          content-style="font-size: 16px"
          :offset="[10, 10]"
        >
          Synchronize
        </q-tooltip>
      </q-btn>
      <q-select
        filled
        v-model="library"
        use-input
        hide-selected
        dark
        clearable
        fill-input
        input-debounce="0"
        placeholder="Select Library..."
        dense
        @input="selectLibrary"
        :options="libraries"
        style="width: 300px; margin-left: 30px;"
      >
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">
              No results
            </q-item-section>
          </q-item>
        </template>
      </q-select>
      <q-space />
      <q-btn
        flat
        round
        icon="fas fa-plus"
        @click=""
      >
        <q-tooltip
          content-style="font-size: 16px"
          :offset="[10, 10]"
        >
          Add Library
        </q-tooltip>
      </q-btn>
      <q-btn
        flat
        round
        :disable="!selected"
        icon="fas fa-folder-plus"
        @click="folderprompt = true"
      >
        <q-tooltip
          content-style="font-size: 16px"
          :offset="[10, 10]"
        >
          Add Folder
        </q-tooltip>
      </q-btn>
      <q-btn
        flat
        :disable="!selected"
        round
        icon="far fa-trash-alt"
      >
        <q-tooltip
          content-style="font-size: 16px"
          :offset="[10, 10]"
        >
          Delete
        </q-tooltip>
      </q-btn>
    </q-toolbar>
  </div>
</template>
<style>
.highlight {
}

.network-node:hover {
  text-decoration: underline;
}
</style>
<script>
const dd = require('drip-drop')
import DataService from 'components/util/DataService'
import { mdiArrowCollapseAll } from '@mdi/js'
import { mdiArrowExpandAll } from '@mdi/js'
import { mdiCardTextOutline } from '@mdi/js'

function addClass (el, classNameToAdd) {
  if (el.className.indexOf(classNameToAdd) === -1) {
    el.className += ' ' + classNameToAdd
  }
}

function removeClass (el, classNameToRemove) {
  if (el.className.indexOf(classNameToRemove) !== -1) {
    const reg = new RegExp(classNameToRemove, 'g')
    el.className = el.className.replace(reg, '')
  }
}

function getNodeFromKey (key, nodes) {
  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i]
    if (node && node.id && node.id === key) return node
    if (node && node.children && node.children.length > 0) {
      const n = getNodeFromKey(key, node.children)
      if (n !== null) return n
    }
  }
  return null
}

export default {
  name: 'LibraryTree',
  props: ['toolbar', 'highlight', 'channel', 'view'],
  components: {},
  created () {
    this.collapseAll = mdiArrowCollapseAll
    this.expandAll = mdiArrowExpandAll
    this.cardOutline = mdiCardTextOutline
  },
  watch: {
    '$store.state.designer.token': function (val) {
      if (val) {
        this.synchronize()
        this.initializeDrag()
      } else {
      }
    }
  },
  methods: {
    updateCard (node) {
      console.log('object.card', node)
      this.$root.$emit('object.card', node)
    },
    expandAllNodes () {
      this.$refs.tree.expandAll()
    },
    collapseAllNodes () {
      this.$refs.tree.collapseAll()
    },
    showUpgrade () {
      this.$root.$emit('subscriptions')
    },
    addItem (item) {
    },
    mouseover (node) {
      console.log(node)
    },
    updated () {
      console.log('updated')
    },
    afterShow () {
      let i;
      const me = this
      this.initializeDrag()
      console.log('afterShow ', me.highlight)
      if (me.highlight) {
        for (i = 0; i < me.nodes.length; i++) {
          const node = me.nodes[i]
          if (node.id.indexOf(me.highlight) === 0) {
            node.disabled = false
            console.log(node, false)
          } else {
            node.disabled = true
            console.log(node, true)
          }
        }
      } else {
        for (i = 0; i < me.nodes.length; i++) {
          me.nodes[i].disabled = false
        }
      }
      console.log(this.nodes)
    },
    updateSelected (key) {
      console.log('selected: ', this.selected)
      console.log('key: ', key)
      const node = getNodeFromKey(key, this.nodes)
      console.log('node: ', node)
      window.global.root.$emit(this.channel, node)
    },
    initializeDrag () {
      console.log('initialize drag')
      const els = document.getElementsByClassName('q-tree__node-header')
      for (let i = 0; i < els.length; i++) {
        const el = els[i]
        const draghandle = dd.drag(el, {
          image: true // default drag image
        })
        draghandle.on('start', function (setData, e) {
          const rnode = e.srcElement.querySelector('.rapidquestnode')
          console.log(
            'RNODE:',
            JSON.stringify({
              collection: rnode.getAttribute('collection'),
              objectid: rnode.getAttribute('id')
            })
          )

          const objdata = {
            collection: rnode.getAttribute('collection'),
            objectid: rnode.getAttribute('id')
          }
          console.log('objdata:', objdata)
          setData('objectid', JSON.stringify(objdata))
          // Put data in vuex?

          // Pull method calls off element attributes, invoke that method with 'start'
        })

        dd.drop(el).on('enter', function (keys, event) {
          console.log('drop enter', keys, event)
          // Lookup keys in Vuex store
          // Update styles/classes based on data (e.g. allow or disallow)
          addClass(event.target, 'highlight')
        })
        dd.drop(el).on('leave', function (keys, event) {
          console.log('drop leave', keys, event)
          // Lookup keys in Vuex store
          // Update styles/classes based on data
          removeClass(event.target, 'highlight')
        })
      }
    },
    synchronize () {
      this.loading = true
      const me = this

      DataService.getNetworks(this.$store.state.designer.token).then((nodes) => {
        console.log('NETWORKS', nodes)
        me.nodes = nodes.data.networks
        this.$refs.tree.lazy = {}
        this.$refs.tree.collapseAll()
        setTimeout(function () {
          me.loading = false
        }, 500)
      })
    },
    unselectNode () {
      this.selected = null
    },
    showNewEntityDialog () {
      console.log('library show new entity')
      this.$root.$emit('new.entity.dialog')
    }
  },
  mounted () {
    if (this.$auth.isAuthenticated) {
      this.synchronize()
      this.initializeDrag()
    }
  },
  data () {
    return {
      libraries: ['Library 1', 'Library 2'],
      step: 1,
      library: '',
      selectLibrary: '',
      selected: null,
      loading: false,
      folderprompt: false,
      newfolder: '',
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
      },
      tab: 'environment',
      upgrade: true,
      showToolbar: true,
      nodes: []
    }
  }
}
</script>
