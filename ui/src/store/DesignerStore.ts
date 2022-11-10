import { RootState } from './RootState'
import { mapActions, mapGetters, mapState, Module } from 'vuex'
import { ActionTreeAdaptor, GetterTreeAdaptor } from '../util'
import Vue from 'vue'

const STORE_NAME = 'designer'
const SET_MESSAGE = 'setMessage'
const SET_STREAMING = 'setStreaming'
const SET_CONNECTED = 'setConnected'
const SET_PYTHON = 'setPython'

const getters: GetterTreeAdaptor<StatusGetters, StatusState, RootState> = {
  getMessage (state: StatusState) {
    return state.message
  },
  getStreaming (state: StatusState) {
    return state.streaming
  },
  getConnected (state: StatusState) {
    return state.connected
  },
  getPython (state: StatusState) {
    return state.python
  },
  getVersion (state: StatusState) {
    return state.version
  }
}

const actions: ActionTreeAdaptor<StatusActions, StatusState, RootState> = {
  async setMessage ({ commit }, { message }) {
    await new Promise<void>(resolve => {
      commit(SET_MESSAGE, message)
      resolve()
    })
  },
  async setStreaming ({ commit }, { streaming }) {
    await new Promise<void>(resolve => {
      commit(SET_STREAMING, streaming)
      resolve()
    })
  },
  async setConnected ({ commit }, { connected }) {
    await new Promise<void>(resolve => {
      commit(SET_CONNECTED, connected)
      resolve()
    })
  },
  async setPython ({ commit }, { python }) {
    await new Promise<void>(resolve => {
      commit(SET_PYTHON, python)
      resolve()
    })
  }
}

export const DesignerStore: Module<StatusState, RootState> = {
  namespaced: true,
  state: {
    message: 'Ready',
    streaming: false,
    connected: false,
    python: false,
    version: <string>process.env.VERSION
  },
  getters,
  mutations: {
    setMessage (state: StatusState, message: string) {
      state.message = message
    },
    setStreaming (state: StatusState, streaming: boolean) {
      state.streaming = streaming
    },
    setConnected (state: StatusState, connected: boolean) {
      state.connected = connected
    },
    setPython (state: StatusState, python: boolean) {
      state.python = python
    }
  },
  actions
}

export const mappedStatusState = mapState(STORE_NAME, [
  'message', 'streaming', 'connected', 'python', 'version'
])

export interface StatusState {
    message: string;
    streaming: boolean;
    connected: boolean;
    python: boolean;
    version: string;
}

export const mappedStatusGetters = mapGetters(STORE_NAME, [
  'getMessage', 'getStreaming', 'getConnected', 'getPython', 'getVersion'
])

export interface StatusGetters {
    getMessage: string;
    getStreaming: boolean;
    getConnected: boolean;
    getVersion: string;
    getPython: boolean;
}

export const mappedStatusActions = mapActions(STORE_NAME, [
  'setMessage', 'setStreaming', 'setConnected', 'setPython', 'setVersion'
])

export type StatusActions = {
    setMessage: (payload: { message: string }) => Promise<void>;
    setStreaming: (payload: { streaming: boolean }) => Promise<void>;
    setConnected: (payload: { connected: boolean }) => Promise<void>;
    setPython: (payload: { python: boolean }) => Promise<void>;
}

export const DesignerComponentBase = Vue.extend<void,
    StatusActions,
    StatusState & StatusGetters, void>({
      computed: {
        ...mappedStatusState,
        ...mappedStatusGetters
      },
      methods: {
        ...mappedStatusActions
      }

    })

// This class will implement a variety of interfaces for each type of state used by the designer app
export class DesignerComponentBaseClass extends Vue implements StatusState, StatusGetters, StatusActions {
    getMessage!: StatusGetters['getMessage'];
    getStreaming!: StatusGetters['getStreaming'];
    getConnected!: StatusGetters['getConnected'];
    getPython!: StatusGetters['getPython'];
    getVersion!: StatusGetters['getVersion'];

    version!: StatusState['version'];
    message!: StatusState['message'];
    streaming!: StatusState['streaming'];
    connected!: StatusState['connected'];
    python!: StatusState['python'];

    setMessage!: (payload: { message: string }) => Promise<void>;
    setStreaming!: (payload: { streaming: boolean }) => Promise<void>;
    setConnected!: (payload: { connected: boolean }) => Promise<void>;
    setPython!: (payload: { python: boolean }) => Promise<void>;
}
