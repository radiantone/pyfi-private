import { store } from 'quasar/wrappers'
import Vuex from 'vuex'

import client from './client'
import { State } from './Store'
import { CountStore } from './CountStore'

import state, { UserStateInterface } from './client/state';
// import example from './module-example';
// import { ExampleStateInterface } from './module-example/state';

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export interface StateInterface {
  // Define your own store structure, using submodules if needed
  // example: ExampleStateInterface;
  // Declared as unknown to avoid linting issue. Best to strongly type as per the line above.
  client: UserStateInterface,
  count: State,
}

let count = CountStore;

export default store(({ Vue }) => {
  Vue.use(Vuex)

  const Store = new Vuex.Store<StateInterface>({
    modules: {
      client,
      count
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: !!process.env.DEBUGGING
  })

  return Store
})

