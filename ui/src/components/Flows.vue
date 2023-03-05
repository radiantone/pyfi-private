<template>
  <div style="height: fit">
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
        <div style="margin-left: 20px;">
          <q-toolbar style="padding: 0px;">
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
              :label="'/' + path.text"
              class="breadcrumb"
              style="margin-left: 10px;"
            />
          </q-toolbar>
        </div>
        <div
          v-if="showaddfolder"
          style="margin-left: 0px; margin-top: -16px; margin-bottom: 0px;"
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
        <q-btn
          flat
          round
          icon="fas fa-plus"
          size="xs"
          color="primary"
          class="q-mr-xs"
          style="padding: 0;"
          @click="
            showpath = false;
            showaddfolder = true;
          "
        >
          <q-tooltip
            content-class=""
            content-style="font-size: 16px"
            :offset="[10, 10]"
          >
            Add Folder
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
          class="dragrow text-primary"
        >
          <q-item-section avatar>
            <q-icon
              :name="item.icon"
              color="secondary"
              v-if="item.type === 'folder'"
            />
            <q-icon
              :name="item.icon"
              v-if="item.type !== 'folder'"
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
              @click="selectFileOrFolder(item)"
            >{{ ( item.filename ? item.filename : item.name ) }}</a>
          </q-item-section>
          <q-space />
          <q-toolbar>
            <q-space />
            <q-btn
              flat
              dense
              rounded
              size="sm"
              icon="fas fa-play"
            >
              <q-tooltip
                v-if="item.type === objecttype"
                content-style="font-size: 16px"
                :offset="[10, 10]"
              >
                Run
              </q-tooltip>
            </q-btn>
            <q-btn
              flat
              dense
              rounded
              icon="edit"
              :class="darkStyle"
            >
              <q-tooltip
                v-if="item.type === objecttype"
                content-style="font-size: 16px"
                :offset="[10, 10]"
              >
                Rename
              </q-tooltip>
            </q-btn>
            <q-btn
              flat
              dense
              rounded
              icon="delete"
              :class="darkStyle"
              @click="showDeleteObject(item)"
            >
              <q-tooltip
                v-if="item.type === objecttype"
                content-style="font-size: 16px"
                :offset="[10, 10]"
              >
                Delete
              </q-tooltip>
            </q-btn>
          </q-toolbar>
        </q-item>
      </q-list>
    </q-scroll-area>

    <q-dialog
      v-model="saveflow"
      persistent
    >
      <q-card
        style="padding: 10px; padding-top: 30px; width: 500px; height: 200px;"
      >
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
              <q-item-label>Save Flow</q-item-label>
              <q-space />
              <q-icon
                class="text-primary"
                name="fas fa-save"
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
          <span class="q-ml-sm"> Save flow to folder {{ foldername }}? </span>
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
            label="Save"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="saveFlow"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="deleteobject"
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
              <q-item-label>Delete {{ deleteobjectname }}</q-item-label>
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
            Are you sure you want to delete {{ deleteobjectname }}?
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
            @click="deleteObject"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog
      v-model="overwriteflow"
      persistent
    >
      <q-card
        style="padding: 10px; padding-top: 30px; width: 500px; height: 200px;"
      >
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
              <q-item-label>Filename Exists</q-item-label>
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
            Overwrite existing flow {{ this.flowname }}?
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
            @click="doOverwriteFlow"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

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
/* eslint-disable @typescript-eslint/no-unsafe-call,@typescript-eslint/restrict-plus-operands,@typescript-eslint/no-this-alias,@typescript-eslint/no-unsafe-member-access,@typescript-eslint/no-unsafe-assignment,@typescript-eslint/no-floating-promises */
import DataService from 'components/util/DataService'

var dd = require('drip-drop')

export default {
  components: {},
  props: ['objecttype', 'collection', 'icon', 'toolbar', 'flowid'],
  mounted () {
    if (this.$auth.isAuthenticated) {
      this.$root.$on('update.' + this.collection, this.synchronize)
      this.$root.$on('save.flow.' + this.flowid, this.saveFlowEvent)
      this.$root.$on('save.flow.to.folder.' + this.flowid, this.saveToFolderEvent)
      this.synchronize()
    }
  },
  watch: {
    '$store.state.designer.token': function (val) {
      if (val) {
        this.$root.$on('update.' + this.collection, this.synchronize)
        this.$root.$on('save.flow.' + this.flowid, this.saveFlowEvent)
        this.$root.$on('save.flow.to.folder.' + this.flowid, this.saveToFolderEvent)
        this.synchronize()
      } else {
        this.$root.$off('update.' + this.collection, this.synchronize)
        this.$root.$off('save.flow.' + this.flowid, this.saveFlowEvent)
        this.$root.$off('save.flow.to.folder.' + this.flowid, this.saveToFolderEvent)
      }
    }
  },
  beforeDestroy () {
    this.$root.$off('update.' + this.collection, this.synchronize)
    this.$root.$off('save.flow' + this.flowid)
    this.$root.$off('save.flow.to.folder.' + this.flowid)
  },
  methods: {
    async doOverwriteFlow () {
      console.log('doOverwriteFlow')
      await this.saveFlow()
    },
    async saveFlow () {
      const me = this
      this.loading = true
      console.log(
        'flow',
        this.flowuuid,
        this.foldername,
        this.flowname,
        this.flowcode
      )
      await DataService.newFile(
        'flows',
        this.foldername,
        this.flowuuid,
        this.flowname,
        this.saveas,
        'flow',
        'fas fa-file',
        this.flowcode,
        this.$store.state.designer.token
      )
        .then((response) => {
          me.saveas = false
          me.synchronize()
          console.log(response.data.id)
          me.$q.notify({
            color: 'secondary',
            timeout: 2000,
            position: 'top',
            message: 'Save flow ' + this.flowname + ' succeeded!',
            icon: 'save'
          })
          this.$root.$emit('save.flow.succeeded', this.flowuuid)
          me.flowuuid = response.data.id
          console.log('this.flowuuid is', this.flowuuid)
          this.$root.$emit('flow.uuid', this.flowid, this.flowuuid)
        })
        .catch(({ response }) => {
          console.log(response)
          this.$root.$emit('save.flow.error', this.flowuuid)
          me.loading = false
          me.saveas = false
          if (response.status === 409) {
            console.log('File name exists ', response.data.id)
            me.overwriteflow = true
            me.flowuuid = response.data.id
            me.notifyMessage('dark', 'error', 'The file name already exists.')
          }
        })
      // DataService call to create or save flow in foldername
      // with flowcode as the code
    },
    async deleteObject () {
      console.log('DELETE: ', this.deleteobjectid)
      var me = this
      var res = await DataService.deleteFile(this.deleteobjectid, this.$store.state.designer.token)
        .then((result) => {
          me.$q.notify({
            color: 'secondary',
            timeout: 2000,
            position: 'top',
            message: 'Delete flow ' + this.deleteobjectname + ' succeeded!',
            icon: 'folder'
          })
          me.synchronize()
        })
        .catch((error) => {
          console.log(error.response)
          me.loading = false
          me.notifyMessage('negative', 'error', error.response.data.message)
        })
    },

    saveToFolderEvent (name, uuid, id, flow) {
      this.flowcode = flow
      this.flowname = name
      this.flowid = id
      this.flowuuid = uuid
      this.saveflow = true
      this.saveas = true
    },
    saveFlowEvent (name, uuid, id, flow) {
      this.flowcode = flow
      this.flowname = name
      this.flowid = id
      this.flowuuid = uuid
      if (uuid === undefined) {
        this.saveflow = true
      } else {
        this.saveFlow()
      }
    },
    addFolder () {
      var me = this
      this.showaddfolder = false
      this.showpath = true
      this.loading = true
      DataService.newFolder('flows', this.foldername + '/' + this.newfolder, this.$store.state.designer.token)
        .then(() => {
          me.synchronize()
        })
        .catch(function (error) {
          console.log(error)
          me.loading = false
          me.notifyMessage(
            'dark',
            'error',
            'There was an error creating the folder.'
          )
        })
    },
    breadcrumbClick (crumb) {
      console.log('CRUMB:', crumb.path)
      var path = crumb.path
      if (crumb.path[0] === '/') {
        path = path.substr(1)
      }

      var p = path.split('/')
      var paths = (this.paths = [])
      var _path = ''
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
      var me = this

      console.log('selectFileOrFolder ', item.id, item, this.objecttype)
      item._id = item.id

      this.flowuuid = item.id
      if (item.type === this.objecttype) {
        me.$root.$emit('loading.flow')
        DataService.getFile(item.id, this.$store.state.designer.token).then((code) => {
          item.code = code.data
          me.flowcode = item.code
          console.log('FLOW CODE', item)
          me.$root.$emit('load.flow', item)
        })
      } else if (item.type === 'folder') {
        this.foldername = item.path + '/' + item.filename
        var p = this.foldername.split('/')
        var paths = (this.paths = [])
        var _path = ''
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
      var me = this
      try {
        var files = DataService.getFiles(this.collection, this.foldername, this.$store.state.designer.token)
        files
          .then(function (result) {
            setTimeout(function () {
              me.loading = false
            }, 100)
            result = result.data
            me.items = result

            setTimeout(() => {
              for (let i = 0; i < result.length; i++) {
                if (result[i].type === 'folder') continue
                // var el = document.querySelector("[id='" + result[i]._id + "']");
                var el = document.querySelector(
                  "[id='row" + result[i].id + "']"
                )
                if (el) {
                  // console.log(result[i]._id, el);

                  var draghandle = dd.drag(el, {
                    image: true // default drag image
                  })
                  if (!result[i].columns) result[i].columns = []
                  draghandle.on('start', function (setData, e) {
                    console.log('drag:start:', el, e)
                    setData('object', JSON.stringify({ node: result[i] }))
                  })
                }
              }
            }, 800)
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
    },
    navigate (folder) {
      this.foldername = folder
      this.synchronize()
    },
    showDeleteObject (item) {
      this.deleteobjectname = item.name
      this.deleteobjectid = item.id
      this.deleteobjecttype = item.type
      this.deleteobject = true
    }
  },
  data () {
    return {
      token: null,
      saveas: false,
      saveflow: false,
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
