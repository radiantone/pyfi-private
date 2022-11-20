<template>
  <div style="height: fit">

    <q-scroll-area style="height: calc(100vh - 180px); width: 100%;">
      <q-list separator>
        <q-item
          v-for="item in items"
          :key="item.id"
          :id="'row' + item.id"
          class="dragrow"
        >
        </q-item>
      </q-list>
    </q-scroll-area>

  </div>
</template>
<style>
.breadcrumb:hover {
  cursor: pointer;
  text-decoration: underline;
}

a.text-secondary:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>
<script>
import DataService from 'components/util/DataService'

export default {
  components: {},
  computed: {
  },
  props: [],
  mounted () {
  },
  methods: {

    notifyMessage (color, icon, message) {
      this.$q.notify({
        color: color,
        timeout: 2000,
        position: 'top',
        message: message,
        icon: icon
      })
    }
  },
  data () {
    return {
      items: [
        {
          url: ''
        }
      ]
    }
  }
}
</script>
