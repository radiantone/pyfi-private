<template>
<div style="box-shadow: 0 0 5px grey;background-color:rgb(244, 246, 247); z-index:999999; width: 200px; height:40px; padding: 3px; font-size: 12px"> Name 
<span style="font-weight: bold; color: #775351" :data-source="node">{{name}}</span>
<!--<i class="pull-right fas fa-cog text-primary" @click="clickMe"/>-->
<q-btn-dropdown
          flat
          content-class="text-dark bg-white"
          dense
          color="secondary"
          dropdown-icon="fas fa-cog"
          padding="0px"
          size=".6em"
        >
          <q-list dense>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-database"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Database
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fab fa-python"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Script
              </q-item-section>
            </q-item>
            </q-list>
            </q-btn-dropdown>

<div style="color:black;font-weight:normal;font-family: 'Roboto', '-apple-system', 'Helvetica Neue', Helvetica, Arial, sans-serif;background-color: white; border-top: 1px solid #abbcc3; width:200px;height:20px; position:absolute; top:20px; left:0px; padding: 1px; padding-left: 3px;font-size: 12px;padding-top:3px"> 
Queued
<span style="font-weight: bold; color: #775351">0 (0 bytes)</span>
</div></div>

</template>
<script>
 export default {
   name: 'Button',
   props: [ 'node','name' ],
   methods: {
       clickMe() {
           console.log('clicked')
       }
   }
 }
</script>