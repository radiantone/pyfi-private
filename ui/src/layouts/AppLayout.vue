<template>
  <q-layout
    view="lHh Lpr lFf"
    class="bg-white"
  >
    <q-header elevated>
      <q-toolbar style="background-color:#0ca940">
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen=!leftDrawerOpen"
          aria-label="Menu"
          icon="menu"
        />

        <q-toolbar-title>
          Customer Portal
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-2"
    >
      <q-list>
        <q-item-label header style="font-size: 1.5em">
          Component Palette
        </q-item-label>
        <q-item @drag="drag" @dragend="dragend" draggable="true"
                unselectable="on"
        >
          <q-item-section avatar>
            <q-icon size="lg" color="grey-7" name="image"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Banner</q-item-label>
            <q-item-label caption>
              Application Image Banner
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item @drag="drag" @dragend="dragend" draggable="true"
                unselectable="on"
        >
          <q-item-section avatar>
            <q-icon size="lg" color="grey-7" name="group"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Customers</q-item-label>
            <q-item-label caption>
              Customer Data List
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item @drag="drag" @dragend="dragend" draggable="true"
                unselectable="on"
        >
          <q-item-section avatar>
            <q-icon size="lg" color="grey-7" name="las la-tractor"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Farms</q-item-label>
            <q-item-label caption>
              Customer Farms List
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item @drag="drag" @dragend="dragend" draggable="true"
                unselectable="on"
        >
          <q-item-section avatar>
            <q-icon size="lg" color="grey-7" name="grass"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Fields</q-item-label>
            <q-item-label caption>
              Customer Farm Fields
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item @drag="drag" @dragend="dragend" draggable="true"
                unselectable="on"
        >
          <q-item-section avatar>
            <q-icon size="lg" color="grey-7" name="cloud"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Weather</q-item-label>
            <q-item-label caption>
              Weather Widget
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          clickable
          @click="$router.push('/')"
        >
          <q-item-section avatar>
            <q-icon size="lg" color="grey-7" name="architecture"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Designer</q-item-label>
            <q-item-label caption>
              Back to Designer
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <LayoutTemplate ref="layout"/>
      <div class="q-pa-md" style="max-width: 1200px; max-height:600px">
        <q-input
          v-model="text"
          filled
          type="textarea"
        />
        <q-btn label="Fetch" @click="fetch"></q-btn>
      </div>
    </q-page-container>
  </q-layout>
</template>
<style>
.vue-grid-item.vue-grid-placeholder {
        display: none !important;
    }
</style>
<script>
import DataService from "components/util/DataService"
import LayoutTemplate from "components/templates/LayoutTemplate.vue"

let mouseXY = {"x": null, "y": null};
let DragPos = {"x": null, "y": null, "w": 1, "h": 1, "i": null};

export default {
  name: 'AppLayout',
  components: {
    LayoutTemplate
  },
  data() {
    return {
      leftDrawerOpen: false,
      text: "No Data",
      index: 0
    }
  },
  mounted() {
    DataService.getMock().then((res) => {
      console.log("DATA MOCK FROM APP", res)
    })
    document.addEventListener("dragover", function (e) {
      mouseXY.x = e.clientX;
      mouseXY.y = e.clientY;
    }, false);
  },
  methods: {
    drag: function (e) {
      let parentRect = document.getElementById('content').getBoundingClientRect();
      let mouseInGrid = false;
      if (((mouseXY.x > parentRect.left) && (mouseXY.x < parentRect.right)) && ((mouseXY.y > parentRect.top) && (mouseXY.y < parentRect.bottom))) {
        mouseInGrid = true;
      }
      if (mouseInGrid === true && (this.$refs.layout.layout.findIndex(item => item.i === 'drop')) === -1) {
        this.$refs.layout.layout.push({
          x: DragPos.x,
          y: DragPos.y, // puts it at the bottom
          w: 2,
          h: 2,
          i: 'drop',
        });
      }
      let index = this.$refs.layout.layout.findIndex(item => item.i === 'drop');

      if (index !== -1) {
        let el = this.$refs.layout.$refs.gridlayout.$children[index];

        el.dragging = {"top": mouseXY.y - parentRect.top, "left": mouseXY.x - parentRect.left};
        let new_pos = el.calcXY(mouseXY.y - parentRect.top, mouseXY.x - parentRect.left);

        if (mouseInGrid === true) {
          this.$refs.layout.$refs.gridlayout.dragEvent('dragstart', 'drop', new_pos.x, new_pos.y, 1, 1);
          DragPos.i = String(index);
          DragPos.x = this.$refs.layout.layout[index].x;
          DragPos.y = this.$refs.layout.layout[index].y;
        }
        if (mouseInGrid === false) {
          this.$refs.layout.$refs.gridlayout.dragEvent('dragend', 'drop', new_pos.x, new_pos.y, 1, 1);
          this.$refs.layout.layout = this.$refs.layout.layout.filter(obj => obj.i !== 'drop');
        }
      }
    },
    dragend: function (e) {
      let parentRect = document.getElementById('content').getBoundingClientRect();
      let mouseInGrid = false;
      if (((mouseXY.x > parentRect.left) && (mouseXY.x < parentRect.right)) && ((mouseXY.y > parentRect.top) && (mouseXY.y < parentRect.bottom))) {
        mouseInGrid = true;
      }
      if (mouseInGrid === true) {

        this.$refs.layout.$refs.gridlayout.dragEvent('dragend', 'drop', DragPos.x, DragPos.y, 1, 1);
        this.$refs.layout.layout = this.$refs.layout.layout.filter(obj => obj.i !== 'drop');
        this.$refs.layout.layout.push({
          x: DragPos.x,
          y: DragPos.y, // puts it at the bottom
          w: 2,
          h: 2,
          html: "<b>HI THERE!</b>",
          i: this.index,
        });
        this.index++;

        /*
          this.$refs.layout.layout.push({
              x: DragPos.x,
              y: DragPos.y, // puts it at the bottom
              w: 2,
              h: 2,
              i: this.$refs.layout.layout.length,
          });


          this.$refs.layout.$refs.gridlayout.dragEvent('dragend', DragPos.i, DragPos.x,DragPos.y,1,1);
          try {
              this.$refs.layout.$refs.gridlayout.$children[this.$refs.layout.layout.length].$refs.item.style.display="block";
          } catch {
          }
         */
      }
    },
    toggleLeftDrawer() {
      leftDrawerOpen.value = !leftDrawerOpen.value
    },
    fetch() {
      DataService.getMock().then((res) => {
        this.text = JSON.stringify(res.data)
      })
    }
  }
}
</script>
