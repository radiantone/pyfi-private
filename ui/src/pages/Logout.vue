<template>
  <div class="fullscreen bg-primary text-dark text-center q-pa-md flex flex-center jtk-surface">
    <div>
      <div
        class="text-h2"
        style="opacity:.4"
      >
        Logged out
      </div>
    </div>
  </div>
</template>
<style>
.jtk-surface {
  background-image: url('~assets/images/Graph-paper.svg');
  height: 100vh;
  overflow: hidden;
}
</style>
<script lang="ts">
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
  name: 'Logout',
  mounted () {
  }
})
</script>
