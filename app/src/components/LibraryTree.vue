<template>
  <div class=" fit" style="padding:0;height:100vh" >
    <q-scroll-area style="height: calc(100vh - 260px); ">
      <q-tree
      :nodes="nodes"
      dense
      ref="tree"
      node-key="id"
      class="text-secondary"
      >          <template v-slot:default-header="prop">
            <div class="row items-center rapidquestnode" :id="prop.node.id" >
              <q-icon :name="prop.node.icon || 'share'" size="18px" class="q-mr-sm text-dark" />
              <div class="text-secondary" :id="prop.node.id" style="font-size:1.2em">{{ prop.node.label }}</div>
            </div>
          </template></q-tree>
      </q-scroll-area>
    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary"/>
    </q-inner-loading>
    <q-toolbar v-if="toolbar" class="fixed-bottom bg-black text-white">
      <q-btn flat round icon="fas fa-sync-alt" class="q-mr-xs" @click="synchronize">
        <q-tooltip  content-style="font-size: 16px" :offset="[10, 10]">Synchronize</q-tooltip>
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
        style="width: 300px;margin-left:30px"
      >
        <template v-slot:no-option>
          <q-item>
            <q-item-section class="text-grey">
              No results
            </q-item-section>
          </q-item>
        </template>
      </q-select>
      <q-space/>
      <q-btn flat round icon="fas fa-plus" @click="">
        <q-tooltip  content-style="font-size: 16px" :offset="[10, 10]">Add Library</q-tooltip>
      </q-btn>
      <q-btn flat round :disable="!selected" icon="fas fa-folder-plus" @click="folderprompt=true">
        <q-tooltip  content-style="font-size: 16px" :offset="[10, 10]">Add Folder</q-tooltip>
      </q-btn>
      <q-btn flat :disable="!selected" round icon="far fa-trash-alt">
        <q-tooltip  content-style="font-size: 16px" :offset="[10, 10]">Delete</q-tooltip>
      </q-btn>
    </q-toolbar>
  </div>
</template>
<style>
  .highlight {

  }
</style>
<script>
var dd = require('drip-drop')
import DataService from 'components/util/DataService'
import { mdiPowerSocketUs } from '@mdi/js';

function addClass (el, classNameToAdd) {
  if (el.className.indexOf(classNameToAdd) === -1) {
    el.className += ' ' + classNameToAdd
  }
}

function removeClass (el, classNameToRemove) {
  if (el.className.indexOf(classNameToRemove) !== -1) {
    var reg = new RegExp(classNameToRemove, 'g')
    el.className = el.className.replace(reg, '')
  }
}

function getNodeFromKey (key, nodes) {
  for (var i = 0; i < nodes.length; i++) {
    const node = nodes[i]
    if (node && node.id && node.id === key) return node
    if (node && node.children && node.children.length > 0) {
      var n = getNodeFromKey(key, node.children)
      if (n != null) return n
    }
  }
  return null
}
export default {
  name: 'LibraryTree',
  props: ['toolbar', 'highlight', 'channel', 'view'],
  components: {},
  methods: {
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
      var me = this
      this.initializeDrag()
      console.log('afterShow ', me.highlight)
      if (me.highlight) {
        for (var i = 0; i < me.nodes.length; i++) {
          var node = me.nodes[i]
          if (node.id.indexOf(me.highlight) === 0) {
            node.disabled = false
            console.log(node, false)
          } else {
            node.disabled = true
            console.log(node, true)
          }
        }
      } else {
        for (var i = 0; i < me.nodes.length; i++) {
          me.nodes[i].disabled = false
        }
      }
      console.log(this.nodes)
    },
    onLazyLoad ({ node, key, done, fail }) {
      // call fail() if any error occurs
      var me = this
      console.log('Lazy load ', node, key, this.highlight)

      var files = ObjectService.listLibrary(node, this.security.auth.user)
      files.then(function (result) {
        setTimeout(function () {
          if (me.highlight) {
            for (var i = 0; i < result.length; i++) {
              var node = result[i]
              if (node.id.indexOf(me.highlight) === 0) {
                node.disabled = false
              } else {
                node.disabled = true
              }
            }
          }
          done(result)
          me.initializeDrag()
        }, 100)
      }).catch(function (error) {
        console.log(error)
        me.$q.notify({
          color: 'negative',
          timeout: 2000,
          position: 'top',
          message: 'There was an error synchronizing this view',
          icon: 'error'
        })

        fail([])
      })
    },
    updateSelected (key) {
      console.log('selected: ', this.selected)
      console.log('key: ', key)
      var node = getNodeFromKey(key, this.nodes)
      console.log('node: ', node)
      window.global.root.$emit(this.channel, node)
    },
    initializeDrag () {
      console.log('initialize drag')
      var els = document.getElementsByClassName('q-tree__node-header')
      for (var i = 0; i < els.length; i++) {
        var el = els[i]
        var draghandle = dd.drag(el, {
          image: true // default drag image
        })
        draghandle.on('start', function (setData, e) {
          var rnode = e.srcElement.querySelector('.rapidquestnode')
          console.log('RNODE:', JSON.stringify({ collection: rnode.getAttribute('collection'), objectid: rnode.getAttribute('id') }))

          var objdata = { collection: rnode.getAttribute('collection'), objectid: rnode.getAttribute('id') }
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
      var me = this

      DataService.getNetworks().then((nodes) => {
        console.log("NETWORKS",nodes)
        me.nodes = nodes.data.networks;
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
    this.synchronize();
    this.initializeDrag()
    console.log('CHANNEL:', this.channel)
  },
  data () {
    return {
      libraries: ['Library 1','Library 2'],
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
      nodes: [
        {
          label: 'Satisfied customers',
          children: [
            {
              label: 'Good food',
              children: [
                { label: 'Quality ingredients' },
                { label: 'Good recipe' }
              ]
            },
            {
              label: 'Good service (disabled node)',
              disabled: true,
              children: [
                { label: 'Prompt attention' },
                { label: 'Professional waiter' }
              ]
            },
            {
              label: 'Pleasant surroundings',
              children: [
                { label: 'Happy atmosphere (*)' },
                { label: 'Good table presentation' },
                { label: 'Pleasing decor (*)' }
              ]
            }
          ]
        }
      ]
    }
  }
}
</script>
