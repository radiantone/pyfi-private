<template>
  <div>
    <q-table
      style="height:400px;width:100%"
      :data="this.properties"
      :columns="columns"
      row-key="property"
      :separator="separator"
      :rows-per-page-options="[6]"
      :pagination.sync="pagination"
      virtual-scroll
    >
      <template #body="props">
        <q-tr :props="props">
          <q-td
            key="property"
            :props="props"
            :width="150"
            :style="'background-color:'+props.row.background"
          >
            {{ props.row.property }}
            <q-popup-edit
              v-model="props.row.property"
              title="Property Name"
              buttons
            >
              <q-input
                type="string"
                v-model="props.row.property"
                dense
                autofocus
              />
            </q-popup-edit>
          </q-td>
          <q-td
            key="description"
            :props="props"
            :style="'background-color:'+props.row.background"
          >
            {{ props.row.description }}
            <q-popup-edit
              v-model="props.row.description"
              title="Property Description"
              buttons
            >
              <q-input
                type="string"
                v-model="props.row.description"
                dense
                autofocus
              />
            </q-popup-edit>
          </q-td>
          <q-td
            key="value"
            :width="200"
            :props="props"
          >
            {{ props.row.value }}
            <q-popup-edit
              v-model="props.row.value"
              title="Value"
              buttons
            >
              <q-input
                type="string"
                v-model="props.row.value"
                dense
                autofocus
              />
            </q-popup-edit>
          </q-td>
          <q-td
            key="type"
            :width="80"
            :props="props"
          >
            <q-select
              dense
              borderless
              v-model="props.row.type"
              :options="types"
              value="string"
            />
          </q-td>
          <q-td
            key="action"
            :props="props"
            style="width:25px"
          >
            <q-btn
              flat
              round
              dense
              size="md"
              class="bg-white text-primary"
              :id="props.row.id"
              @click="deleteProperty(props.row)"
              icon="delete"
            />
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
export default {
  name: 'Properties',
  props: ['properties'],
  created () {
    console.log('props', this.properties)
  },
  methods: {
    deleteProperty: function (obj) {
      console.log(obj)
      for (var i = 0; i < this.properties.length; i++) {
        if (this.properties[i] === obj) {
          break
        }
      }
      this.properties.splice(i, 1)
    },
    getProperties: function () {
      return this.properties
    },
    addProperty: function () {
      console.log('Adding property!')
      this.ids += 1
      this.properties.push({
        description: 'A new description',
        property: 'A New Property',
        value: 'None',
        id: 'property' + window.uuidv4()
      })
    }
  },
  data () {
    return {
      ids: 0,
      pagination: {
        page: 1,
        rowsPerPage: 6 // 0 means all rows
      },
      separator: 'vertical',
      types: [
        'number',
        'string',
        'boolean',
        'object'
      ],
      columns: [
        {
          name: 'property',
          required: true,
          label: 'Property',
          align: 'left',
          field: row => row.property,
          sortable: true
        },
        { name: 'description', align: 'center', label: 'Description', field: 'description' },
        { name: 'value', align: 'center', label: 'Value', field: 'value' },
        { name: 'type', align: 'center', label: 'Type', field: 'type' },
        { name: 'action', align: 'center', label: 'Action', icon: 'trashcan', sortable: true }
      ]
    }
  }
}
</script>
