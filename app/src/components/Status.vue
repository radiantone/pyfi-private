<script lang="ts">
declare global {
    interface Window { store: any; }
}
import { PropType } from 'vue';
import mixins from 'vue-typed-mixins';
import { Wrapper } from '../util';
import {
  DesignerComponentBase
} from '../store/DesignerStore';

import Store from '../store';

export default mixins(DesignerComponentBase).extend<
  Data,
  Methods,
  Computed,
  Props
>({
  created() {
    this.$store = window.store;
  },
  props: {
    wrapper: {
      type: Object as PropType<Wrapper>,
      default: () => ({ increment: 11 }),
    },
  },
  mounted() {
      console.log("this.$store",this.$store);
  }
});

interface Data {
  message: number;
}

interface Methods {
  // no need to mix with CountActions
}

interface Computed {
}

interface Props {
  wrapper: Wrapper;
}
</script>
