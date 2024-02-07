import { MutationTree } from 'vuex'
import { UserStateInterface } from './state'

const mutation: MutationTree<UserStateInterface> = {
  updateLoggedIn (state, val) {
    console.log('updatedLoggedIn:', val)
    state.logged_in = val
    console.log('updatedLoggedIn:', this.logged_in)
  }
}

export default mutation
