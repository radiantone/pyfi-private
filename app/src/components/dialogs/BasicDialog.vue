<template>
  <div>
    <q-dialog v-model="dialog" size="lg" id="newspeechdialog">
      <q-card style="max-width: 70vw;width:40vw;overflow:hidden">
        <q-card-section class=" bg-waves text-white">
          <q-toolbar>
            <q-icon name="comment" class="text-h5 text-primary" side />

            <q-toolbar-title>
              <span class="text-weight-bold text-h5">Edit Argument</span>
            </q-toolbar-title>

            <q-btn
              flat
              round
              dense
              icon="close"
              class="text-grey-8"
              v-close-popup
            ></q-btn>
          </q-toolbar>
        </q-card-section>

        <q-separator />
        <div style="">
          <div style="padding:0px;overflow:hidden">
            <q-tabs
              v-model="tab"
              dense
              :class="darkStyle"
              active-color="primary"
              indicator-color="primary"
              align="left"
              inline-label
            >
              <q-tab name="attributes" selected icon="info" label="Attributes">
                <q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                  >Attributes</q-tooltip
                >
              </q-tab>

              <q-tab name="properties" selected icon="list" label="Properties">
                <q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                  >Properties</q-tooltip
                >
              </q-tab>

              <q-tab name="notes" selected icon="note" label="Notes">
                <q-tooltip
                  content-class
                  content-style="font-size: 16px"
                  :offset="[10, 10]"
                  >Notes</q-tooltip
                >
              </q-tab>
            </q-tabs>

            <q-separator />
            <q-tab-panels v-model="tab" animated>
              <q-tab-panel
                name="attributes"
                style="padding:20px;min-height:400px"
              >
                <br />

                <div class="row justify-start">
                  <div class="col-3">
                    <q-item-label
                      class="text-h6"
                      align="right"
                      style="margin-top:10px;margin-right:20px"
                      >Type</q-item-label
                    >
                  </div>
                  <div class="col-3">
                    <q-select
                      dense
                      class="justify-end"
                      outlined
                      v-model="obj.type"
                      label="Dialog Type"
                      stack-label
                      :options="types"
                      :options-dense="denseOpts"
                    >
                      <template v-slot:prepend>
                        <q-icon name="fas fa-comment" />
                      </template>
                    </q-select>
                  </div>
                  <div class="col-1">
                    <q-item-label
                      class="text-h6"
                      align="right"
                      style="margin-top:10px;margin-right:20px"
                    ></q-item-label>
                  </div>
                  <div class="col-3">
                    <q-select
                      dense
                      class="justify-end"
                      outlined
                      v-model="obj.evaluation"
                      label="Evaluation"
                      stack-label
                      :options="triggers"
                      :options-dense="denseOpts"
                    >
                    </q-select>
                  </div>
                </div>
                <br />
                <div class="row justify-start">
                  <div class="col-3">
                    <q-item-label
                      class="text-h6"
                      align="right"
                      style="margin-top:10px;margin-right:20px"
                      >Short Text</q-item-label
                    >
                  </div>
                  <div class="col-5">
                    <q-input
                      dense
                      square
                      outlined
                      v-model="obj.name"
                      hint="Abbreviated Text"
                    >
                      <template v-slot:append>
                        <q-avatar>
                          <q-icon name="comment" />
                        </q-avatar>
                      </template>
                    </q-input>
                  </div>
                  <div class="col-1"></div>
                  <div class="col-2">
                    <q-checkbox v-model="obj.sequence" label="Sequence" />
                  </div>
                </div>
                <br />
                <div class="row justify-start">
                  <div class="col-3">
                    <q-item-label
                      class="text-h6"
                      align="right"
                      style="margin-top:10px;margin-right:20px"
                      >Spoken Text</q-item-label
                    >
                  </div>
                  <div class="col-7">
                    <q-input
                      dense
                      square
                      outlined
                      v-model="obj.description"
                      type="textarea"
                      hint="Spoken Text"
                    >
                      <template v-slot:append>
                        <q-avatar>
                          <q-icon name="notes" />
                        </q-avatar>
                      </template>
                    </q-input>
                  </div>
                </div>
                <div class="row justify-start" style="margin-bottom:0px">
                  <div class="col-3">
                    <q-item-label
                      class="text-h6"
                      align="right"
                      style="margin-top:10px;margin-right:20px"
                      >Delay</q-item-label
                    >
                  </div>
                  <div class="col-1">
                    <q-slider v-model="delay" :min="0" :max="20" label />
                  </div>
                  <div class="col-4">
                    <q-select
                      dense
                      style="margin-left:50px"
                      class="justify-end"
                      outlined
                      v-model="obj.selection"
                      label="Story Beat"
                      stack-label
                      :options="storybeats"
                      :options-dense="denseOpts"
                    >
                      <template v-slot:prepend>
                        <q-icon name="fas fa-drum" />
                      </template>
                    </q-select>
                  </div>
                  <div class="col-1"></div>
                  <div class="col-2">
                    <q-checkbox v-model="obj.terminate" label="Terminate" />
                  </div>
                </div>
              </q-tab-panel>
              <q-tab-panel name="properties" style="padding:0px">
                <q-card>
                  <Properties
                    ref="properties"
                    :properties="this.obj.properties"
                  />
                </q-card>
              </q-tab-panel>
              <q-tab-panel name="notes" style="padding:0px">
                <q-card>
                  <Notes ref="notes" :notes="this.obj.notes" />
                </q-card>
              </q-tab-panel>
            </q-tab-panels>
          </div>
        </div>
        <q-separator />
        <q-toolbar class="bottom  text-primary">
          <q-btn
            flat
            v-if="tab === 'function'"
            label="Add"
            @click="newFunction"
            class="bg-primary"
            color="white"
          />
          <q-btn
            flat
            v-if="tab === 'properties'"
            label="Add"
            @click="newProperty"
            class="bg-primary"
            color="white"
          />
          <q-btn
            flat
            v-if="tab === 'when'"
            label="Add"
            @click="newRule"
            class="bg-primary"
            color="white"
          />
          <q-btn
            flat
            v-if="tab === 'notes'"
            label="Add"
            @click="newNote"
            class="bg-primary"
            color="white"
          />
          <q-space />

          <!--<q-btn flat label="Cancel" color="primary" v-close-popup/>-->
          <q-btn
            flat
            label="Done"
            v-if="this.titleMode === 'New'"
            class="bg-primary"
            @click="createSpeech"
            :disable="this.disabled()"
            color="white"
            v-close-popup
          />
          <q-btn
            flat
            label="Done"
            v-if="this.titleMode === 'Edit'"
            class="bg-primary"
            @click="notifyDirty"
            :disable="this.disabled()"
            color="white"
            v-close-popup
          />
          <!--<q-btn flat label="Update" v-if="this.titleMode === 'Edit'" class="bg-primary" @click="updateSpeech"  color="white" v-close-popup />-->
        </q-toolbar>
      </q-card>
    </q-dialog>
    <q-dialog
      v-model="iconDialog"
      transition-show="scale"
      transition-hide="scale"
    >
      <q-card class="" style="width: 300px">
        <q-card-section>
          <IconSelectDialog />
        </q-card-section>
        <q-card-actions align="right" class="bg-white text-white">
          <q-btn flat label="Close" class="bg-primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<style scoped>
.bg-waves {
  width: 100%;
  background-repeat: no-repeat;
  background-color: black;
}
</style>

<script>
import Properties from "components/Properties";
import Notes from "components/Notes";

export default {
  name: "NewSpeechDialog",
  components: {
    Properties: Properties,
    Notes: Notes,
    editor: require("vue2-ace-editor")
  },
  computed: {
    darkStyle: function() {
      if (this.$q.dark.mode) return "text-grey bg-black";
      else return "text-grey bg-grey-2";
    }
  },
  mounted() {
    console.log("new speech dialog mounted");
    this.$root.$on("new.speech.dialog", data => {
      console.log("new speech dialog...data:", data);
      this.dialog = true;
      if (data && data.obj) {
        this.obj = data.obj; // JSON.parse(JSON.stringify(data.obj));
        if (!this.obj.functions) this.obj.functions = [];
        if (data.callback) {
          this.callback = data.callback;
        }
      } else {
        this.obj = {
          name: "Test",
          icon: "fas fa-cube",
          display: "Always",
          description: "A description",
          grouped: false,
          type: "Speech",
          strategy: [],
          entityClass: "Spoken",
          properties: [],
          functions: [],
          rules: [],
          events: [],
          callbacks: [],
          facts: [],
          notes: []
        };
      }

      console.log("obj:", this.obj);
      if (data && data.mode === "edit") {
        this.titleMode = "Edit";
      } else {
        this.titleMode = "New";
      }
    });
  },
  methods: {
    notifyDirty() {
      window.global.root.$emit("toolkit.dirty", true);
    },
    newRule: function() {
      this.$refs.when.addRule();
    },
    newNote: function() {
      this.$refs.notes.addNote();
    },
    editorInit: function() {
      require("brace/ext/language_tools"); // language extension prerequsite...
      require("brace/mode/html");
      require("brace/mode/javascript"); // language
      require("brace/mode/less");
      require("brace/theme/chrome");
      require("brace/snippets/javascript"); // snippet
    },
    disabled: function() {
      var name = this.obj.name && this.obj.name.length > 0;
      var description = this.obj.description && this.obj.description.length > 0;
      var type = this.obj.type;

      if (name === undefined) name = false;
      if (description === undefined) description = false;
      if (type === undefined) type = false;

      console.log(type, name, description, !name && !description);
      return !name || !description || !type;
    },
    selectClass: function() {
      console.log("selectClass");
    },
    updateSpeech: function() {
      if (this.callback) {
        console.log("Calling callback!");
        this.callback(this.obj);
      } else {
        console.log("No callback!");
      }
    },
    createSpeech: function() {
      this.callback(this.obj);
    },
    newFunction: function() {
      this.$refs.functions.addFunction();
    },
    newProperty: function() {
      this.$refs.properties.addProperty();
    },
    showDialog: function(obj, mode, callback) {
      this.dialog = true;
      this.callback = callback;
      this.titleMode = mode;
      if (obj) {
        if (!obj.functions) obj.functions = [];
        this.obj = obj;
      }
    },
    hideDialog: function() {
      this.dialog = false;
    }
  },
  data() {
    return {
      color: "",
      width: "200px",
      titleMode: "New",
      content: "",
      obj: {
        name: "Test",
        icon: "fas fa-cube",
        display: "Always",
        description: "A description",
        grouped: false,
        type: "Spoken",
        properties: [],
        functions: [],
        rules: [],
        facts: [],
        notes: []
      },
      data: [],
      iconDialog: false,
      agentDialog: false,
      dense: false,
      denseOpts: true,
      tab: "attributes",
      fixed: false,
      delay: 2,
      sequence: false,
      display: "Always",
      storybeats: [
        "Introduction",
        "Exposition",
        "Hook",
        "Tension",
        "Betrayal",
        "Request",
        "Discovery",
        "Offering",
        "Refusal",
        "Climax"
      ],
      triggers: ["Always", "Rules", "Probability", "Function", "Skills"],
      types: ["Spoken", "Thought", "Action", "Perception", "Aside"],
      name: "",
      dialog: false
    };
  }
};
</script>
