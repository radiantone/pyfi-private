import { RootState } from './RootState'
import { mapActions, mapGetters, mapState, Module } from 'vuex'
import { ActionTreeAdaptor, GetterTreeAdaptor } from '../util'
import Vue from 'vue'

const STORE_NAME = 'designer'
const SET_MESSAGE = 'setMessage'
const SET_STREAMING = 'setStreaming'
const SET_CONNECTED = 'setConnected'
const SET_TOKEN = 'setToken'
const SET_SUBSCRIPTION = 'setSubscription'
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
  },
  getToken (state: StatusState) {
    return state.token
  },
  getSubscription (state: StatusState) {
    return state.subscription
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
  },
  async setToken ({ commit }, { token }) {
    await new Promise<void>(resolve => {
      commit(SET_TOKEN, token)
      resolve()
    })
  },
  async setSubscription ({ commit }, { subscription }) {
    await new Promise<void>(resolve => {
      commit(SET_SUBSCRIPTION, subscription)
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
    version: <string>process.env.VERSION,
    token: 'none',
    subscription: 'none'
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
    },
    setToken (state: StatusState, token: string) {
      state.token = token
    },
    setSubscription (state: StatusState, subscription: string) {
      state.subscription = subscription
    }
  },
  actions
}

export const mappedStatusState = mapState(STORE_NAME, [
  'message', 'streaming', 'connected', 'python', 'version', 'token', 'subscription'
])

export interface StatusState {
    message: string;
    streaming: boolean;
    connected: boolean;
    python: boolean;
    version: string;
    token: string;
    subscription: string;
}

export const mappedStatusGetters = mapGetters(STORE_NAME, [
  'getMessage', 'getStreaming', 'getConnected', 'getPython', 'getVersion', 'getToken', 'getSubscription'
])

export interface StatusGetters {
    getMessage: string;
    getStreaming: boolean;
    getConnected: boolean;
    getVersion: string;
    getPython: boolean;
    getToken: string;
    getSubscription: string;
}

export const mappedStatusActions = mapActions(STORE_NAME, [
  'setMessage', 'setStreaming', 'setConnected', 'setPython', 'setVersion', 'setToken', 'setSubscription'
])

export type StatusActions = {
    setMessage: (payload: { message: string }) => Promise<void>;
    setStreaming: (payload: { streaming: boolean }) => Promise<void>;
    setConnected: (payload: { connected: boolean }) => Promise<void>;
    setPython: (payload: { python: boolean }) => Promise<void>;
    setToken: (payload: { token: string }) => Promise<void>;
    setSubscription: (payload: { subscription: string }) => Promise<void>;
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
    getToken!: StatusGetters['getToken'];
    getSubscription!: StatusGetters['getSubscription'];

    version!: StatusState['version'];
    message!: StatusState['message'];
    streaming!: StatusState['streaming'];
    connected!: StatusState['connected'];
    python!: StatusState['python'];
    token!: StatusState['token'];
    subscription!: StatusState['subscription'];

    setMessage!: (payload: { message: string }) => Promise<void>;
    setStreaming!: (payload: { streaming: boolean }) => Promise<void>;
    setConnected!: (payload: { connected: boolean }) => Promise<void>;
    setPython!: (payload: { python: boolean }) => Promise<void>;
    setToken!: (payload: { token: string }) => Promise<void>;
    setSubscription!: (payload: { subscription: string }) => Promise<void>;
}
