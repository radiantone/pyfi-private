<template>
<div>
  
  <div
    :class="'node jtk-node text-primary'"
    style="
      color: primary;
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
        background: white;
        color: black;
        position: relative;
        top: -100px;
        left: 80px;
        padding-left: 20px;
        font-size: 20px;
        font-family: 'Indie Flower', cursive;
        margin-top: 5px;
        width: 200px;
        border-left: 1px solid black;
      "
    >
      <q-scroll-area
        style="height: 150px; width: 100%;padding:5px"
        :content-style="contentStyle"
        :thumb-style="thumbStyle"
        :content-active-style="contentActiveStyle"
        ><span style="padding-top:10px">{{ note }}            
        <q-popup-edit v-model="note" buttons >
              <q-input type="string" v-model="note" dense autofocus />
            </q-popup-edit></span></q-scroll-area
      >
    </div>

  </div>

  </div>
</template>
<style scoped>
.q-item {
  margin-right: 0px;
}
</style>
<script>
import { BaseNodeComponent } from 'jsplumbtoolkit-vue2';

export default {
  name: 'StartTemplate',
  mixins: [BaseNodeComponent],
  components: {},
  created() {
    var me = this;
    console.log('me.tooltips ', me.tooltips);
    console.log('start listening for show.tooltips');
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
    });
  },
  data() {
    return {
      entityName: '',
      columnName: '',
      confirm: false,
      icon: 'fas fa-sticky-note',
      deleteSpeech: false,
      edit: false,
      deleteConfirm: false,
      note: 'A Handsome Note',
      tooltip: true,
      tooltips: false,
      prompt: false,

      contentStyle: {
        backgroundColor: 'rgba(0,0,0,0.02)',
        color: '#555',
      },

      contentActiveStyle: {
        backgroundColor: '#eee',
        color: 'black',
      },

      thumbStyle: {
        right: '2px',
        borderRadius: '5px',
        backgroundColor: '#027be3',
        width: '5px',
        opacity: 0.75,
      },
    };
  },
  methods: {
    showEdit() {
      this.edit = true;
    },
    showTooltip(show) {
      this.tooltip = show;
    },
  },
};
</script>
