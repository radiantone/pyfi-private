<template>
  <div>
    <div
      :class="'node jtk-node text-primary'"
      style="
      text-size: 35px;
      max-width: 250px;
      border: black 1px;
      font-weight: bold;
    "
    >
      <div
        v-if="tooltips || tooltip"
        style="
        z-index: 99999;
        background: white !important;
        color: black;
        left: 80px;
        padding-left: 20px;
        font-size: 20px;
        font-family: 'Indie Flower', cursive;
        margin-top: 5px;
        width: 200px;
        border-left: 1px solid black;
      "
      >
        <span style="padding-top:10px;background-color: white">{{ obj.note }}
          <q-popup-edit
            v-model="obj.note"
            buttons
          >
            <q-input
              type="string"
              v-model="obj.note"
              dense
              autofocus
              color="white"
            />
          </q-popup-edit></span>
      </div>
    </div>
  </div>
</template>
<style scoped>
.q-item {
  margin-right: 0px;
}
.absolute {
  background-color: white !important;
}
</style>
<script>
/* eslint-disable @typescript-eslint/no-this-alias, @typescript-eslint/restrict-plus-operands, @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-call,@typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access */

import { BaseNodeComponent } from 'jsplumbtoolkit-vue2'

export default {
  name: 'StartTemplate',
  mixins: [BaseNodeComponent],
  components: {},
  created () {
    const me = this
    console.log('me.tooltips ', me.tooltips)
    console.log('start listening for show.tooltips')
    /*
    window.global.root.$on('show.tooltips', (value) => {
      console.log('start tooltips:', value);
      me.tooltips = value;
      if (value) {
        me.icon = 'fas fa-sticky-note';
      } else {
        me.icon = 'fas fa-sticky-note';
      }
      console.log('ME:', me);
      console.log('TOOLTIPS', me.tooltips);
    }); */
  },
  data () {
    return {
      obj: {
        note: 'A Handsome Note'
      },
      entityName: '',
      columnName: '',
      confirm: false,
      icon: 'fas fa-sticky-note',
      deleteSpeech: false,
      edit: false,
      deleteConfirm: false,
      tooltip: true,
      tooltips: false,
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
    showEdit () {
      this.edit = true
    },
    showTooltip (show) {
      this.tooltip = show
    }
  }
}
</script>
