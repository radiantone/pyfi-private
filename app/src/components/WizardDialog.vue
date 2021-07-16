<template>
  <div >
    <q-dialog v-model="dialog" size="lg" id="wizarddialog" style="overflow:hidden;">
      <q-card style="max-width: 70vw;width:40vw;overflow:hidden">
        <q-card-section class=" bg-waves text-white" style="overflow:hidden;height:65px;padding-top:10px">
          <q-toolbar>
            <q-icon name="person" class="text-h5 text-white" style="opacity:0.8" size="lg" side/>
            <q-toolbar-title>
              <span class="text-weight-bold text-h5" style="opacity:0.8" >Wizard</span>
            </q-toolbar-title>
            <q-btn flat round dense icon="close" class="text-grey-8" v-close-popup></q-btn>
          </q-toolbar>
          <img src="~assets/images/uspto-seal.png" width="40%" style="opacity:0.3;float:left;position:absolute;right:10%;top:-50px;z-index:99999;display:inline-block"/>
        </q-card-section>

        <q-separator/>
        <div style="">
          <div style="padding:0px;overflow:hidden">
            <q-tabs
              v-model="tab"
              dense
              class="text-grey bg-grey-2"
              active-color="primary"
              indicator-color="primary"
              align="left"
              inline-label
              style="display:none"
            >
              <q-tab name="properties" selected icon="list" label="Properties">
                <q-tooltip content-class content-style="font-size: 16px" :offset="[10, 10]">Properties</q-tooltip>
              </q-tab>
              <q-tab name="behaviors" selected icon="rowing" label="Behaviors">
                <q-tooltip content-class content-style="font-size: 16px" :offset="[10, 10]">Behaviors</q-tooltip>
              </q-tab>

              <q-tab name="notes" selected icon="note" label="Notes">
                <q-tooltip content-class content-style="font-size: 16px" :offset="[10, 10]">Notes</q-tooltip>
              </q-tab>
            </q-tabs>

            <q-separator/>
            <q-tab-panels v-model="tab" animated ref="tabs">
              <q-tab-panel name="properties" style="padding:0px;height:40vh">

                Properties
              </q-tab-panel>
              <q-tab-panel name="behaviors" style="padding:0px;height:40vh">

                Behaviors
              </q-tab-panel>

              <q-tab-panel name="notes" style="padding:0px;height:40vh">

                Notes
              </q-tab-panel>

            </q-tab-panels>
          </div>
        </div>
        <q-separator/>
        <q-toolbar class="bottom bg-white text-primary">
          <q-btn flat label="Cancel" color="primary" v-close-popup/>
          <q-space/>

          <q-btn flat label="Prev" color="primary" @click="prev" :disable="prevDisable"/>
          <q-btn flat label="Next" class="bg-primary" :disable="nextDisable"
                 color="white" @click="next"/>
        </q-toolbar>
      </q-card>
    </q-dialog>

  </div>
</template>

<style scoped>
  .bg-waves {
    width: 100%;
    background-color: #0a3b5f;

  }

  .bg-waves:before {
    background-image: url('~assets/images/uspto-seal.png');
    background-repeat: no-repeat;
    background-position-x: 200px;
    opacity: 0.5;
  }

</style>

<script>

export default {
  name: 'NewSpeakerDialog',
  setup () {
  },
  components: {
  },
  mounted: function () {
    this.$root.$on('show.wizard.dialog', data => {
      this.dialog = true
    })
  },
  methods: {
    next () {
      this.prevDisable = false
      if ( this.step < this.tabs.length-1 ) {
        this.step++
      }
      if ( this.step == this.tabs.length-1 ) {
        this.nextDisable = true;
      }
      this.tab = this.tabs[this.step]
    },
    prev () {
      this.nextDisable = false
      if ( this.step > 0) {
        this.step--
      }
      if ( this.step == 0 ) {
        this.prevDisable = true
      }
      this.tab = this.tabs[this.step]
    }
  },
  data () {
    return {
      step:0,
      nextDisable: false,
      prevDisable: true,
      dialog: false,
      tab:'properties',
      tabs:['properties','behaviors','notes']
    }
  }
}
</script>
