<template>
  <div style="height: calc(95vh - 225px);">
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
      </q-breadcrumbs>
    </div>
    <q-scroll-area class="fit">
      <q-list
        bordered
        separator
        class="fit"
        style="width: 100%;"
        id="patterns"
      >
        <q-item
          v-for="item in items"
          :key="item.id"
          :id="item._id"
          class="pattern"
          data-node-icon="far fa-object-group"
          data-node-type="pattern"
          :data-node-name="item.name"
          :data-node-label="item.name"
          :data-node-code="item.code"
          :data-node-pattern="item.pattern"
          data-node-description="A processor group description"
          data-node-package="my.python.package"
          data-node-id="pattern"
          jtk-is-group="true"
        >
          <q-item-section avatar>
            <q-icon
              name="fas fa-project-diagram"
              class="text-secondary"
            />
          </q-item-section>
          <q-item-section>
            <table
              border="0"
              width="400px"
            >
              <tr>
                <td width="150px">
                  <a
                    style="
                      color: #6b8791;
                      z-index: 99999;
                      cursor: pointer;
                      width: 100%;
                      min-width: 250px;
                    "
                    @click="selectFileOrFolder(item)"
                  >{{ item.filename }}</a>
                </td>
                <td align="left">
                  <img
                    :src="item.image"
                    height="55px"
                  >
                </td>
              </tr>
            </table>
          </q-item-section>
          <q-space />
          <q-toolbar>
            <q-space />

            <q-btn
              flat
              dense
              rounded
              icon="settings"
              style="color: #abbcc3;"
              @click="editObject(item)"
            >
              <q-tooltip
                content-style="font-size: 16px"
                :offset="[10, 10]"
              >
                Edit
              </q-tooltip>
            </q-btn>
            <q-btn
              flat
              dense
              rounded
              icon="delete"
              style="color: #abbcc3;"
              @click="showDeleteObject(item)"
            >
              <q-tooltip
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

    <q-inner-loading :showing="loading">
      <q-spinner-gears
        size="50px"
        color="primary"
      />
    </q-inner-loading>
  </div>
</template>

<style scoped>
.q-item:hover {
  background-color: #e3e8ec;
}
</style>

<script>
import { v4 as uuidv4 } from 'uuid'
import DataService from './util/DataService'

var dd = require('drip-drop')

export default {
  name: 'Patterns',
  created () {},
  methods: {
    synchronize () {
      var me = this
      this.loading = true
      console.log('synchronizing')
      var files = DataService.getFiles('patterns', 'Home')

      files
        .then((result) => {
          me.loading = false
          me.items = me.patterns
          console.log('PATTERNS', result)
          console.log('ITEMS', me.items)
          result.data.forEach((pattern) => {
            pattern.image = JSON.parse(pattern.code).image
            pattern.code = JSON.parse(pattern.code).code
          })
          me.items = me.items.concat(result.data)
          setTimeout(() => {
            var groups = document.querySelectorAll('.pattern')
            groups.forEach((el) => {
              el.data = {
                node: {
                  pattern: true,
                  patternid: el.getAttribute('data-node-pattern'),
                  icon: 'far fa-object-group',
                  style: 'size:50px',
                  type: 'pattern',
                  name: el.getAttribute('data-node-name'),
                  label: el.getAttribute('data-node-label'),
                  code: el.getAttribute('data-node-code'),
                  description: 'A processor group description',
                  package: 'my.python.package',
                  disabled: false,
                  group: true,
                  columns: [],
                  properties: []
                }
              }

              var data = el.data
              data.id = uuidv4()
              var draghandle = dd.drag(el, {
                image: true // default drag image
              })
              draghandle.on('start', function (setData, e) {
                console.log('drag:start:', el, e)
                console.log('DRAG PATTERN DATA', JSON.stringify(data))
                setData('object', JSON.stringify(data))
              })
            })
          })
        })
        .catch((error) => {
          console.log('ERROR', error)
          me.loading = false
          me.notifyMessage(
            'dark',
            'error',
            'There was an error synchronizing patterns view.'
          )
        })
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
    async savePattern (pattern) {
      var me = this

      // Get JSON of flow
      // Get ID of pattern group object
      // Pull out all the nodes with that group, and their ports and edges
      // Save that
      await DataService.newFile(
        'patterns',
        'Home',
        pattern.id,
        pattern.name,
        false,
        'pattern',
        'fas fa-project-diagram',
        JSON.stringify({ image: pattern.image, code: pattern.code })

      )
        .then((response) => {
          me.synchronize()
          console.log(response.data.id)

          me.items.push(pattern)
          me.$q.notify({
            color: 'secondary',
            timeout: 2000,
            position: 'top',
            message: 'Save pattern ' + pattern.name + ' succeeded!',
            icon: 'save'
          })
        })
        .catch(({ response }) => {
          console.log(response)
          me.loading = false
          if (response.status === 409) {
            me.notifyMessage(
              'dark',
              'error',
              'The pattern name already exists.'
            )
          }
        })
    }
  },
  watch: {
    '$auth.isAuthenticated': function (val) {
      if (val) {
        var me = this
        me.synchronize()
        window.root.$on('save.pattern', (id, name, image, objects) => {
          console.log('PATTERNS SAVING', objects)
          var code = JSON.stringify(objects)
          var pattern = {
            id: id,
            name: name,
            pattern: name,
            icon: 'fa fas-home',
            code: code,
            image: image
          }
          me.savePattern(pattern).then(() => {
            me.synchronize()
          })
        })
      }
    }
  },
  mounted () {

  },
  data () {
    return {
      loading: false,
      showpath: true,
      showaddfolder: false,

      paths: [
        {
          text: 'Home',
          icon: 'home',
          id: 0
        }
      ],
      items: [],
      patterns: [
        {
          id: 1,
          filename: 'Pattern A',
          pattern: 'patternA',
          icon: 'fa fas-home',
          image: 'images/pattern1.png'
        },
        {
          id: 2,
          filename: 'Pattern B',
          pattern: 'patternB',
          icon: 'fa fas-home',
          image: 'images/pattern2.png'
        }
      ]
    }
  }
}
</script>
