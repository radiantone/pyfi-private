import { RootState } from './RootState';
import { mapActions, mapGetters, mapState, Module } from 'vuex';
import { ActionTreeAdaptor, GetterTreeAdaptor } from '../util';
import Vue from 'vue';

const STORE_NAME = 'designer'
const SET_MESSAGE = 'setMessage';

const getters: GetterTreeAdaptor<StatusGetters, StatusState, RootState> = {
    getMessage (state: StatusState) {
        return state.message
    },
};

const actions: ActionTreeAdaptor<StatusActions, StatusState, RootState> = {
    async setMessage ({ commit }, { message }) {
        await new Promise<void>(resolve => {
            commit(SET_MESSAGE, message);
            resolve();
        });
    },
};

export const DesignerStore: Module<StatusState, RootState> = {
    namespaced: true,
    state: {
        message: "Ready",
    },
    getters,
    mutations: {
        setMessage (state: StatusState, message: string) {
            state.message = message;
        },
    },
    actions,
};

export const mappedStatusState = mapState(STORE_NAME, [
    'message',
]);

export interface StatusState {
    message: string;
}

export const mappedStatusGetters = mapGetters(STORE_NAME, [
    'getMessage',
]);

export interface StatusGetters {
    getMessage: string;
}

export const mappedStatusActions = mapActions(STORE_NAME, [
    'setMessage'
]);

export type StatusActions = {
    setMessage: (payload: { message: string }) => Promise<void>;
}

export const DesignerComponentBase = Vue.extend<void,
    StatusActions,
    StatusState & StatusGetters, void>({
    computed: {
        ...mappedStatusState,
        ...mappedStatusGetters,
    },
    methods: {
        ...mappedStatusActions,
        },
    
});


// This class will implement a variety of interfaces for each type of state used by the designer app
export class DesignerComponentBaseClass extends Vue implements StatusState, StatusGetters, StatusActions {
    getMessage!: StatusGetters['getMessage'];
    message!: StatusState['message'];
    setMessage!: (payload: { message: string }) => Promise<void>;
}