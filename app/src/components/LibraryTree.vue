<template>
  <div class=" fit" style="padding:0;height:100vh" >
    <q-scroll-area style="height: calc(100vh - 260px); ">
        <q-tree ref="tree"
                :nodes="nodes"
                default-expand-all
                :selected.sync="selected"
                node-key="id"
                selected-color="primary"
                @update:selected="updateSelected"
                @after-show="afterShow"
                @lazy-load="onLazyLoad"
        >
          <template v-slot:default-header="prop">
            <div class="row items-center rapidquestnode" :id="prop.node.id" :collection="prop.node.collection">
              <q-icon :name="prop.node.icon || 'share'" size="24px" class="q-mr-sm text-secondary" />
              <div class="text-secondary" :id="prop.node.id" :collection="prop.node.collection">{{ prop.node.label }}</div>
            </div>
          </template>

        </q-tree>
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
    <q-dialog v-model="folderprompt" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">New Folder</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input dense v-model="newfolder" autofocus @keyup.enter="folderprompt = false"/>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup/>
          <q-btn flat label="Create" v-close-popup @click="newFolder"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>
<style>
  .highlight {

  }
</style>
<script>
var dd = require('drip-drop')
import ObjectService from 'components/util/ObjectService'

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
    async newFolder () {
      var me = this

      try {
        const node = this.$refs.tree.getNodeByKey(this.selected)

        console.log('newFolder:', node, this.selected, {
          parent: this.selected._id,
          label: this.newfolder
        })
        var res = await ObjectService.newLibraryNode(node, {
          parent: this.selected._id,
          icon: 'folder',
          root: node.root,
          explandable: true,
          lazy: true,
          label: this.newfolder
        }, this.security.auth.user)
        if (res.status === 'error') {
          me.notifyMessage('negative', 'error', 'There was an error creating the new folder.')
        } else {
          me.$q.notify({
            color: 'primary',
            timeout: 2000,
            position: 'top',
            message: 'Create Folder Succeeded',
            icon: 'folder'
          })

          this.$refs.tree.lazy = {}
          console.log(node)
          this.$refs.tree.setExpanded(node.id, true)
        }
      } catch (error) {
        console.log(error)
        me.$q.notify({
          color: 'negative',
          timeout: 2000,
          position: 'top',
          message: 'There was an error synchronizing this view',
          icon: 'error'
        })
      }
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

      this.$refs.tree.lazy = {}
      this.$refs.tree.collapseAll()
      setTimeout(function () {
        me.loading = false
      }, 500)
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
          label: 'Storyboards',
          icon: 'dashboard',
          id: 'storyboards',
          lazy: true,
          expandable: true,
          children: [
          ]
        },
        {
          label: 'Quests',
          lazy: true,
          id: 'quests',
          expandable: true,
          icon: 'fab fa-fort-awesome'
        },
        {
          label: 'Locations',
          lazy: true,
          id: 'locations',
          root: 'locations',
          expandable: true,
          icon: 'location_on'
        },
        {
          label: 'NPCs',
          lazy: true,
          expandable: true,
          id: 'npcs',
          root: 'npcs',
          icon: 'person'
        },
        {
          label: 'Players',
          lazy: true,
          expandable: true,
          id: 'players',
          icon: 'people'
        },
        {
          label: 'Objects',
          lazy: true,
          expandable: true,
          id: 'objects',
          icon: 'fas fa-cubes'
        },
        {
          label: 'Skills',
          lazy: true,
          expandable: true,
          id: 'skills',
          icon: 'fas fa-running'
        },
        {
          label: 'Abilities',
          lazy: true,
          expandable: true,
          id: 'abilities',
          icon: 'accessibility_new'
        },
        {
          label: 'Feats',
          lazy: true,
          expandable: true,
          id: 'feats',
          icon: 'fas fa-dumbbell'
        }

      ]
    }
  }
}
</script>
