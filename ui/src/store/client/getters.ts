import { GetterTree } from 'vuex'
import { StateInterface } from '../index'
import { UserStateInterface } from './state'

const getters: GetterTree<UserStateInterface, StateInterface> = {
  getLoggedIn () {
    console.log('getLoggedIn ', this.logged_in)
    return this.logged_in
  }
}

export default getters
