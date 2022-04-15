<template>
  <div style="height:fit">

    <div
      class="q-pa-md q-gutter-md bg-accent text-secondary"
      style="border-bottom: 1px solid #abbcc3; overflow: hidden; "
    >
      <q-breadcrumbs>
        <q-breadcrumbs-el
          v-for="path in paths"
          @click="breadcrumbClick(path)"
          v-if="path.icon"
          :icon="path.icon"
          :key="path.id"
          :label="path.text"
        />
        <q-breadcrumbs-el
          v-for="path in paths"
          @click="breadcrumbClick(path)"
          v-if="!path.icon"
          :key="path.id"
          :label="path.text"
        />
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
          @click="synchronize"
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
    <!--<q-scroll-area class=" fit">-->
      <q-scroll-area style="height:75vh">
      <q-list separator class="fit">
        <q-item v-for="item in items" :key="item.id" :id="item._id">
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
              v-if="item.type === objecttype"
              flat
              dense
              rounded
              icon="settings"
              @click="editObject(item)"
              :class="darkStyle"
            >
              <q-tooltip content-style="font-size: 16px" :offset="[10, 10]">
                Edit
                {{ objecttype.charAt(0).toUpperCase() + objecttype.slice(1) }}
              </q-tooltip></q-btn
            >
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
    <!--</q-scroll-area>-->
</q-scroll-area>


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
            @keyup.enter="folderprompt = false"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn flat label="Create" v-close-popup @click="newFolder" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-inner-loading :showing="visible">
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
  },
  methods: {
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
      this.visible = true;
      var me = this;
      try {
        var files = DataService.getObjects(
          this.objecttype,
          this.foldername
        );
        files
          .then(function(result) {
            setTimeout(function() {
              me.visible = false;
            }, 100);
            console.log("LIST FILES:", result);
            result = result.data;
            me.items = result;

            setTimeout(() => {
              for (let i = 0; i < result.length; i++) {
                if (result[i].type === "folder") continue;
                var el = document.querySelector("[id='" + result[i]._id + "']");
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
            });
          })
          .catch(function(error) {
            console.log(error);
            me.visible = false;
            me.notifyMessage(
              "dark",
              "error",
              "There was an error synchronizing this view."
            );
          });
      } catch (error) {
        me.visible = false;
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
        me.visible = false;
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
        me.visible = false;
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
        me.visible = false;
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
        me.visible = false;
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
      folderprompt: false,
      foldername: "Home",
      newfolder: "",
      visible: false,
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
