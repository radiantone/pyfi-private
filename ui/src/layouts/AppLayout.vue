<template>
  <q-layout
    view="lHh Lpr lFf"
    class="bg-white"
  >
    <q-header elevated>
      <q-toolbar class="bg-blue">
        <q-btn
          flat
          dense
          round
        @click="leftDrawerOpen=!leftDrawerOpen"
          aria-label="Menu"
          icon="menu"
        />

        <q-toolbar-title>
          Quasar App
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
        <q-item-label header>
          Essential Links
        </q-item-label>
        <q-item @drag="drag" @dragend="dragend" draggable="true"
             unselectable="on"
        >
          <q-item-section avatar>
            <q-icon name="school"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Banner</q-item-label>
            <q-item-label caption>
              Application Image Banner
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          clickable
          target="_blank"
          rel="noopener"
          href="https://github.quasar.dev"
        >
          <q-item-section avatar>
            <q-icon name="code"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>GitHub</q-item-label>
            <q-item-label caption>
              github.com/quasarframework
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          clickable
          target="_blank"
          rel="noopener"
          href="http://chat.quasar.dev"
        >
          <q-item-section avatar>
            <q-icon name="chat"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Discord Chat Channel</q-item-label>
            <q-item-label caption>
              https://chat.quasar.dev
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          clickable
          target="_blank"
          rel="noopener"
          href="https://forum.quasar.dev"
        >
          <q-item-section avatar>
            <q-icon name="record_voice_over"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Forum</q-item-label>
            <q-item-label caption>
              https://forum.quasar.dev
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          clickable
          target="_blank"
          rel="noopener"
          href="https://twitter.quasar.dev"
        >
          <q-item-section avatar>
            <q-icon name="rss_feed"/>
          </q-item-section>
          <q-item-section>
            <q-item-label>Twitter</q-item-label>
            <q-item-label caption>
              @quasarframework
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          clickable
          @click="$router.push('/')"
          rel="noopener"
        >
          <q-item-section avatar>
            <q-icon name="public"/>
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
      <div class="q-pa-md" style="max-width: 1200px; max-height:600px">
        <q-input
          v-model="text"
          filled
          type="textarea"
        />
        <q-btn label="Fetch" @click="fetch"></q-btn>
      </div>
      <LayoutTemplate ref="layout"/>
    </q-page-container>
  </q-layout>
</template>
<style>

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
      text: "No Data"
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
                    x: (this.$refs.layout.layout.length * 2) % (this.colNum || 12),
                    y: this.$refs.layout.layout.length + (this.colNum || 12), // puts it at the bottom
                    w: 1,
                    h: 1,
                    i: 'drop',
                });
            }
            let index = this.$refs.layout.layout.findIndex(item => item.i === 'drop');
            if (index !== -1) {
                try {
                    this.$refs.layout.$refs.gridlayout.$children[this.$refs.layout.layout.length].$refs.item.style.display = "none";
                } catch {
                }
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
                alert(`Dropped element props:\n${JSON.stringify(DragPos, ['x', 'y', 'w', 'h'], 2)}`);
                this.$refs.layout.$refs.gridlayout.dragEvent('dragend', 'drop', DragPos.x, DragPos.y, 1, 1);
                this.$refs.layout.layout = this.$refs.layout.layout.filter(obj => obj.i !== 'drop');

                // UNCOMMENT below if you want to add a grid-item
                /*
                this.$refs.layout.layout.push({
                    x: DragPos.x,
                    y: DragPos.y,
                    w: 1,
                    h: 1,
                    i: DragPos.i,
                });
                this.$refs.gridLayout.dragEvent('dragend', DragPos.i, DragPos.x,DragPos.y,1,1);
                try {
                    this.$refs.gridLayout.$children[this.$refs.layout.layout.length].$refs.item.style.display="block";
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
