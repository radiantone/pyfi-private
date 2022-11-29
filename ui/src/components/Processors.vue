<template>
  <div style="height: fit;">
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
      <q-breadcrumbs>
        <div style="margin-left:20px;">
          <q-toolbar style="padding:0px">
            <q-breadcrumbs-el
              v-for="path in paths"
              @click="breadcrumbClick(path)"
              v-if="path.icon && showpath"
              :icon="path.icon"
              :key="path.id"
              :label="path.text"
              class="breadcrumb"
            />
            <q-breadcrumbs-el
              v-for="path in paths"
              @click="breadcrumbClick(path)"
              v-if="!path.icon && showpath"
              :key="path.id"
              :label="'/'+path.text"
              class="breadcrumb"
              style="margin-left:10px"
            />
          </q-toolbar>
        </div>
        <div
          v-if="showaddfolder"
          style="
            margin-left: 0px;
            margin-top: -16px;
            margin-bottom: 0px;
          "
        >
          <q-toolbar style="margin-top: 20px; margin-bottom: 0px;">
            <q-input
              dense
              flat
              v-model="newfolder"
              class="bg-white text-primary"
            />
            <q-btn
              dense
              flat
              label="Add"
              @click="addFolder"
              :disabled="newfolder.length === 0"
            />
            <q-space />
            <q-btn
              dense
              flat
              size="xs"
              icon="cancel"
              @click="
                showaddfolder = false;
                showpath = true;
              "
            />
          </q-toolbar>
        </div>
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
      </q-breadcrumbs>
    </div>
    <q-scroll-area style="height: calc(100vh - 300px); width: 100%;">
      <q-list separator>
        <q-item
          v-for="item in items"
          :key="item.id"
          :id="'row' + item.id"
          class="dragrow"
        >
          <q-item-section avatar>
            <q-icon
              name="fas fa-microchip"
              class="text-secondary"
            />
          </q-item-section>
          <q-item-section>
            <a
              class="text-secondary"
              style="
                z-index: 99999;
                cursor: pointer;
                width: 100%;
                min-width: 250px;
                font-size: 1.3em;
              "
            >{{ item.name }}</a>
          </q-item-section>
          <q-space />
        </q-item>
      </q-list>
    </q-scroll-area>

    <q-inner-loading :showing="loading">
      <q-spinner-gears
        size="50px"
        color="primary"
      />
    </q-inner-loading>
  </div>
</template>
<style>
.breadcrumb:hover {
  cursor: pointer;
  text-decoration: underline;
}

a.text-secondary:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>
<script>
import DataService from 'components/util/DataService'

const dd = require('drip-drop')

export default {
  components: {},
  watch: {
    '$store.state.designer.token': function (val) {
      if (val) {
        this.$root.$on('update.' + this.collection, this.synchronize)
        this.synchronize()
      } else {
        this.$root.off('update.' + this.collection, this.synchronize)
      }
    }
  },
  computed: {
  },
  props: ['objecttype', 'collection', 'icon', 'toolbar'],
  mounted () {
    if (this.$auth.isAuthenticated) {
      this.$root.$on('update.' + this.collection, this.synchronize)
      this.synchronize()
    }
  },
  methods: {

    breadcrumbClick (crumb) {
      console.log('CRUMB:', crumb.path)
      let path = crumb.path
      if (crumb.path[0] === '/') {
        path = path.substr(1)
      }

      const p = path.split('/')
      const paths = (this.paths = [])
      let _path = ''
      p.forEach((path) => {
        _path += '/' + path
        paths.push({
          text: path,
          path: _path,
          id: paths.length
        })
      })
      paths[0].icon = 'home'
      this.navigate(path)
    },
    selectFileOrFolder (item) {
      const me = this

      console.log('selectFileOrFolder ', item.id, item, this.objecttype)
      item._id = item.id

      this.flowuuid = item.id
      if (item.type === this.objecttype) {
        DataService.getFile(item.id, this.$store.state.designer.token).then((code) => {
          item.code = code.data
          me.flowcode = item.code
          console.log('FLOW CODE', item)
          me.$root.$emit('load.flow', item)
        })
      } else if (item.type === 'folder') {
        this.foldername = item.path + '/' + item.name
        const p = this.foldername.split('/')
        const paths = (this.paths = [])
        let _path = ''
        p.forEach((path) => {
          _path += '/' + path
          paths.push({
            text: path,
            path: _path,
            id: paths.length
          })
        })
        paths[0].icon = 'home'
        this.paths = paths
        console.log('PATHS:', this.paths)
        this.synchronize()
      }
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
    synchronize () {
      this.loading = true
      const me = this
      try {
        const files = DataService.getProcessors(this.$store.state.designer.token)
        files
          .then(function (result) {
            setTimeout(function () {
              me.loading = false
            }, 100)
            result = result.data
            me.items = result

            setTimeout(() => {
              for (let i = 0; i < result.length; i++) {
                console.log('result', result[i])
                if (result[i].type === 'folder') continue
                // var el = document.querySelector("[id='" + result[i]._id + "']");
                const el = document.querySelector(
                  "[id='row" + result[i].id + "']"
                )
                if (el) {
                  el.data = result[i]
                  el.data.type = 'processor'
                  el.data.icon = 'fas fa-microchip'

                  const draghandle = dd.drag(el, {
                    image: true // default drag image
                  })
                  if (!result[i].columns) result[i].columns = []
                  draghandle.on('start', function (setData, e) {
                    console.log('drag:start:', el, e)
                    setData('object', JSON.stringify({ node: result[i] }))
                  })
                }
              }
            }, 1000)
          })
          .catch(function (error) {
            console.log(error)
            me.loading = false
            me.notifyMessage(
              'dark',
              'error',
              'There was an error synchronizing this view.'
            )
          })
      } catch (error) {
        me.loading = false
        me.notifyMessage(
          'dark',
          'error',
          'There was an error synchronizing this view.'
        )
      }
    }
  },
  data () {
    return {
      showpath: true,
      showaddfolder: false,
      columns: [
        { name: 'type', align: 'left', label: 'Type', field: 'type' },
        {
          name: 'name',
          required: true,
          label: 'Name',
          align: 'left',
          field: 'name',
          sortable: true
        },
        {
          name: 'action',
          align: 'center',
          label: 'Action',
          icon: 'trashcan',
          sortable: true
        }
      ],
      folderprompt: false,
      foldername: 'Home',
      newfolder: '',
      loading: false,
      deleteobject: false,
      flowname: null,
      overwriteflow: false,
      deleteobjectname: null,
      deleteobjectid: null,
      deleteobjecttype: null,
      items: [],
      paths: [
        {
          text: 'Home',
          icon: 'home',
          id: 0
        }
      ]
    }
  }
}
</script>
