<template>
    
        <q-btn-dropdown
          flat
          content-class="text-dark bg-white"
          dense
          color="secondary"
          label="Query"
          padding="0px"
          size=".8em"
        >
          <q-list dense>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-question"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Query 1
              </q-item-section>
            </q-item>
            <q-item
              clickable
              v-close-popup
            >
              <q-item-section side>
                <q-icon name="fas fa-question"></q-icon>
              </q-item-section>
              <q-item-section side class="text-blue-grey-8">
                Query 2
              </q-item-section>
            </q-item>
            </q-list>
            </q-btn-dropdown>   
</template>

<style></style>

<script>
import { BaseNodeComponent } from 'jsplumbtoolkit-vue2';

export default {
  name: 'QueueSelectTemplate',
  mixins: [BaseNodeComponent],
  components: {
  }
}
</script>