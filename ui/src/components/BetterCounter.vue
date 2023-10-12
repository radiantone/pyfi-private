<script lang="ts">
declare global {
    interface Window { store: any; }
}
import { PropType } from 'vue'
import mixins from 'vue-typed-mixins'
import { Wrapper } from '../util'
import {
  CountComponentBase,
  CountComponentBaseClass,
  CountStore
} from '../store/CountStore'
import Store, { StateInterface } from '../store'
// import { MetaComponentBase } from '../store/MetaStore';
import { io, Socket } from 'socket.io-client'

interface ServerToClientEvents {
  noArg: () => void;
  basicEmit: (a: number, b: string, c: Buffer) => void;
  withAck: (d: string, callback: (e: number) => void) => void;
}

interface ClientToServerEvents {
  hello: (data: SocketData) => void;
}

interface SocketData {
  name: string;
  age: number;
}

const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(
  <string>process.env.SOCKETIO
)

export default mixins(CountComponentBase).extend<
  Data,
  Methods,
  Computed,
  Props
>({
  data () {
    return {
      delayMs: 1000
    }
  },
  created () {
    this.$store = window.store
  },
  props: {
    wrapper: {
      type: Object as PropType<Wrapper>,
      default: () => ({ increment: 11 })
    }
  },
  computed: {
    // These are implementations of the interface Computed
    getcount () {
      return this.count
    },
    buttonLabel () {
      return `Click here to increment (${this.delayMs}ms delay)`
    },
    countLabel () {
      return `The current count is an ${this.isEven ? 'even' : 'odd'} number: ${
        this.count
      } `
    }
  },
  mounted () {
    console.log('this.$store', this.$store)
  },
  methods: {
    // These are implementations of the interface Methods
    sayHello (data: any) {
      const person = <SocketData>data
      socket.emit('hello', person)
      setTimeout(() => {
        this.delayMs = 750
      }, 7000)
    },
    internalPerformAsyncIncrement () {
      this.performAsyncIncrement({ increment: 11, delayMs: this.delayMs })
    }
  }
})

interface Data {
  delayMs: number;
}

interface Methods {
  // no need to mix with CountActions
  internalPerformAsyncIncrement(): void;
  sayHello(data: any): void;
}

interface Computed {
  // no need to mix with CountState, MetaState and CountGetters
  buttonLabel: string;
  countLabel: string;
  getcount: number;
}

interface Props {
  wrapper: Wrapper;
}
</script>
