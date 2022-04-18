<template>
  <div style="height:fit">

    <div
      class="bg-accent text-secondary"
      style="border-bottom: 1px solid #abbcc3; overflow: hidden; "
    >
    
      <q-breadcrumbs>
        <div style="padding: 16px">
        <q-breadcrumbs-el
          v-for="path in paths"
          @click="breadcrumbClick(path)"
          v-if="path.icon && showpath"
          :icon="path.icon"
          :key="path.id"
          :label="path.text"
        />
        <q-breadcrumbs-el
          v-for="path in paths"
          @click="breadcrumbClick(path)"
          v-if="!path.icon && showpath"
          :key="path.id"
          :label="path.text"
        />
        </div>
        <div v-if="showaddfolder" style="margin-left:-20px;padding:5px;margin-top:-16px;margin-bottom:0px">
        <q-toolbar style="margin-top:20px;margin-bottom:0px">
            <q-input dense flat class="bg-white text-primary"></q-input>
            <q-btn dense flat label="Add" @click="addFolder"/>
            <q-space/>
            <q-btn dense flat size="xs" icon="cancel" @click="showaddfolder=false; showpath=true" />
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
          style="padding: 0"
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
          style="padding: 0"
          @click="showpath=false; showaddfolder=true"
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
    <!--
       <q-table style="height:calc(100vh - 300px);width:100%" 
        :data="this.items"
        :columns="columns"
        row-key="property"
        :rows-per-page-options="[30]"
        virtual-scroll
        :id="objecttype+'table'"
      >
      <template v-slot:body="props">
        <q-tr :props="props" class="dragrow" :id="'row'+props.row.id">
          <q-td key="type" :props="props" >
            {{ props.row.type }}
          </q-td>
          <q-td key="name" :props="props" >
            {{ props.row.name }}
          </q-td>
          <q-td key="action" :props="props" >
            Icon
          </q-td>
          </q-tr>
      </template>
      </q-table>-->
    <q-scroll-area style="height:calc(100vh - 300px);width:100%">
      <q-list separator >
        <q-item v-for="item in items" :key="item.id" :id="'row'+item.id" class="dragrow" >
          <q-item-section avatar>
            <q-icon :name="item.icon" :class="darkStyle" />
          </q-item-section>
          <q-item-section
            ><a
              class="text-secondary"
              style="z-index:99999;cursor:pointer;width:100%;min-width:250px;font-size:1.3em"
              @click="selectFileOrFolder(item)"
              >{{ item.name }}</a
            >
          </q-item-section>
          <q-space />
          <q-toolbar>
            <q-space />

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
                {{ objecttype.charAt(0).toUpperCase() + objecttype.slice(1) }}
              </q-tooltip>
            </q-btn>
          </q-toolbar>
        </q-item>

      </q-list>
</q-scroll-area>

    <q-dialog v-model="saveflow" persistent>
      <q-card style="padding: 10px; padding-top: 30px; width:500px;height:200px">
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
              <q-icon class="text-primary" name="fas fa-save" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm" >
            Save flow to folder {{foldername}}?
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
            label="Save"
            class="bg-secondary text-white"
            color="primary"
            v-close-popup
            @click="saveFlow"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="deleteobject" persistent>
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
              <q-item-label>Delete {{deleteobjectname}}</q-item-label>
              <q-space />
              <q-icon class="text-primary" name="fas fa-trash" />
            </q-toolbar>
          </div>
        </q-card-section>
        <q-card-section class="row items-center" style="height: 120px;">
          <q-avatar
            icon="fas fa-exclamation"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm" >
            Are you sure you want to delete {{deleteobjectname}}?
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

    <q-dialog v-model="folderprompt" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">New Folder</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            dense
            v-model="newfolder"
            autofocus
            class="bg-white"
            @keyup.enter="folderprompt = false"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn flat label="Create" v-close-popup @click="newFolder" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>
<style>
a.text-secondary:hover {
  cursor: pointer;
  text-decoration: underline;
}

</style>
<script>
import ObjectService from "components/util/ObjectService";
import DataService from "components/util/DataService";

var dd = require("drip-drop");

export default {
  components: {},
  computed: {
    darkStyle: function() {
      if (this.$q.dark.mode) return "text-grey-6";
      else return "text-primary";
    }
  },
  props: ["objecttype", "collection", "icon", "toolbar"],
  mounted() {
    this.synchronize();
    this.$root.$on("update." + this.collection, this.synchronize);
    this.$root.$on("save.flow",this.saveFlowEvent);
  },
  methods: {
    saveFlow() {
      this.loading = true;

      //DataService call to create or save flow in foldername
      //with flowcode as the code
    },
    saveFlowEvent(flow) {
      this.saveflow = true;
      this.flowcode = flow
    },
    addFolder() {
      this.loading = true;

    },
    breadcrumbClick(crumb) {
      console.log("CRUMB:", crumb.path);
      var path = crumb.path;
      if (crumb.path[0] === "/") {
        path = path.substr(1);
      }

      var p = path.split("/");
      var paths = (this.paths = []);
      var _path = "";
      p.forEach(path => {
        _path += "/" + path;
        paths.push({
          text: path,
          path: _path,
          id: paths.length
        });
      });
      paths[0].icon = "home";
      this.navigate(path);
    },
    selectFileOrFolder(item) {
      console.log("selectFileOrFolder ", item, this.objecttype);
      if (item.type === this.objecttype) {
        console.log();
        this.$root.$emit("new." + this.objecttype + ".tab", {
          obj: item,
          folder: this.foldername
        });
      } else if (item.type === "folder") {
        this.foldername = item.path;
        var p = item.path.split("/");
        var paths = (this.paths = []);
        var _path = "";
        p.forEach(path => {
          _path += "/" + path;
          paths.push({
            text: path,
            path: _path,
            id: paths.length
          });
        });
        paths[0].icon = "home";
        this.paths = paths;
        console.log("PATHS:", this.paths);
        this.synchronize();
      }
    },
    notifyMessage(color, icon, message) {
      this.$q.notify({
        color: color,
        timeout: 2000,
        position: "top",
        message: message,
        icon: icon
      });
    },
    synchronize() {
      this.loading = true;
      var me = this;
      try {
        var files = DataService.getObjects(
          this.objecttype,
          this.foldername
        );
        files
          .then(function(result) {
            setTimeout(function() {
              me.loading = false;
            }, 100);
            console.log("LIST FILES:", result);
            result = result.data;
            me.items = result;

            setTimeout(() => {
              for (let i = 0; i < result.length; i++) {
                if (result[i].type === "folder") continue;
                //var el = document.querySelector("[id='" + result[i]._id + "']");
                var el = document.querySelector("[id='row" + result[i].id + "']");
                if (el) {
                  console.log(result[i]._id, el);

                  var draghandle = dd.drag(el, {
                    image: true // default drag image
                  });
                  if (!result[i].columns) result[i].columns = [];
                  draghandle.on("start", function(setData, e) {
                    console.log("drag:start:", el, e);
                    setData("object", JSON.stringify({ node: result[i] }));
                  });
                }
              }
            },800);
          })
          .catch(function(error) {
            console.log(error);
            me.loading = false;
            me.notifyMessage(
              "dark",
              "error",
              "There was an error synchronizing this view."
            );
          });
      } catch (error) {
        me.loading = false;
        me.notifyMessage(
          "dark",
          "error",
          "There was an error synchronizing this view."
        );
      }
    },
    editObject(object) {
      this.$root.$emit("new." + this.objecttype + ".dialog", {
        obj: object,
        mode: "edit",
        folder: this.foldername
      });
    },
    newObject() {
      console.log("new." + this.objecttype + ".dialog");
      this.$root.$emit("new." + this.objecttype + ".dialog", {
        obj: {
          name: "",
          icon: this.icon,
          description: "",
          grouped: false,
          type: this.objecttype,
          notes: [],
          properties: []
        },
        folder: this.foldername
      });
    },
    navigate(folder) {
      this.foldername = folder;
      this.synchronize();
    },
    async deleteObject(objectid) {
      console.log("DELETE: ", objectid);
      var me = this;
      try {
        var res = await ObjectService.deleteObject(
          this.collection,
          { _id: objectid },
          this.security.auth.user
        );
        me.loading = false;
        console.log(res);
        if (res.status === "error") {
          me.notifyMessage(
            "negative",
            "error",
            "There was an error deleting the object."
          );
        } else {
          me.$q.notify({
            color: "primary",
            timeout: 2000,
            position: "top",
            message: "Delete Succeeded",
            icon: "folder"
          });
          this.synchronize();
          this.$root.$emit("delete." + this.objecttype, { _id: objectid });
        }
      } catch (error) {
        console.log(error);
        me.loading = false;
        me.notifyMessage(
          "negative",
          "error",
          "There was an error deleting the " + this.objecttype + "."
        );
      }
    },
    showDeleteObject(item) {
      this.deleteobjectname = item.name;
      this.deleteobjectid = item._id;
      this.deleteobjecttype = item.type;
      this.deleteobject = true;
    },
    async newFolder() {
      var me = this;
      try {
        var res = await ObjectService.makeDirectory(
          this.collection,
          this.foldername,
          this.newfolder,
          this.security.auth.user
        );
        me.loading = false;
        console.log(res);
        if (res.status === "error") {
          me.notifyMessage(
            "negative",
            "error",
            "There was an error creating the new folder."
          );
        } else {
          me.$q.notify({
            color: "primary",
            timeout: 2000,
            position: "top",
            message: "Create Folder Succeeded",
            icon: "folder"
          });
          this.synchronize();
        }
      } catch (error) {
        console.log(error);
        me.loading = false;
        me.notifyMessage(
          "negative",
          "error",
          "There was an error creating the new folder."
        );
      }
    }
  },
  data() {
    return {
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
        { name: 'action', align: 'center', label: 'Action', icon: 'trashcan', sortable: true }
      ],
      folderprompt: false,
      foldername: "Home",
      newfolder: "",
      loading: false,
      deleteobject: false,
      deleteobjectname: null,
      deleteobjectid: null,
      deleteobjecttype: null,
      items: [],
      paths: [
        {
          text: "Home",
          icon: "home",
          id: 0
        }
      ]
    };
  }
};
</script>
