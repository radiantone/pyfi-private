<template>
<div style="height:calc(95vh - 225px)">
    <q-scroll-area class=" fit" >
      <q-list bordered separator class="fit" style="width:100%" id="patterns">
        <q-item v-for="item in items" :key="item.id" :id="item._id" class="pattern"
                data-node-icon="far fa-object-group"
            data-node-type="pattern"
            :data-node-name="item.name"
            :data-node-label="item.name"
            :data-node-pattern="item.pattern"
            data-node-description="A processor group description"
            data-node-package="my.python.package"
            data-node-id="pattern"
            jtk-is-group="true"
                >
          <q-item-section avatar>
            <q-icon :name="item.icon" />
          </q-item-section>
          <q-item-section>
              <table border="0" width="400px" >
                  <tr>
                      <td width="150px"><a style="color:#6b8791;z-index:99999;cursor:pointer;width:100%;min-width:250px" @click="selectFileOrFolder(item)" >{{item.name}}</a></td>
                      <td align="left"><img :src="item.image" height="55px"/></td>
                  </tr>
              </table>
          
          </q-item-section>
          <q-space/>
          <q-toolbar>
            <q-space/>

            <q-btn flat dense rounded icon="settings" style="color:#abbcc3" @click="editObject(item)"
                   >
              <q-tooltip content-style="font-size: 16px" :offset="[10, 10]">
                Edit
              </q-tooltip></q-btn>
            <q-btn flat dense rounded icon="delete" style="color:#abbcc3" @click="showDeleteObject(item)">
              <q-tooltip content-style="font-size: 16px" :offset="[10, 10]">
                Delete
              </q-tooltip>
            </q-btn>
          </q-toolbar>
        </q-item>
      </q-list>
    </q-scroll-area>
    </div>
</template>

<style scoped>
.q-item:hover {
        background-color: #e3e8ec
}
</style>

<script>
import { v4 as uuidv4 } from 'uuid'
var dd = require('drip-drop')

export default {
  name: 'Patterns',
  created () {

  },
  methods: {

  },
  mounted() {

    var groups = document.querySelectorAll(".pattern");

    groups.forEach((el) => {
        console.log("EL",el)
        el.data = {
            node: {
                pattern: true,
                patternid: el.getAttribute('data-node-pattern'),
                icon: "far fa-object-group",
                style: "size:50px",
                type: "pattern",
                name: el.getAttribute('data-node-name'),
                label: el.getAttribute('data-node-label'),
                description: "A processor group description",
                package: "my.python.package",
                disabled: false,
                group: true,
                columns: [],
                properties: [],
            },
        };

        var data = el.data;
        data.id = uuidv4();
        console.log("PATTERN FOUND ",el);
        var draghandle = dd.drag(el, {
            image: true, // default drag image
        });
        draghandle.on("start", function (setData, e) {
            console.log("drag:start:", el, e);
            setData("object", JSON.stringify(data));
        });
    });

  },
  data() {
      return {
          items: [
              {
                  id: 1,
                  name:'Pattern A',
                  pattern: 'patternA',
                  icon:'fa fas-home',
                  image:'images/pattern1.png'
                  
              },
              {
                  id: 2,
                  name:'Pattern B',
                  pattern: 'patternB',
                  icon:'fa fas-home',
                  image:'images/pattern2.png'
              }
          ]
      }
  }
}
</script>