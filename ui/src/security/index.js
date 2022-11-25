
import Vue from 'vue'

let instance

/** Returns the current instance of the SDK */
export const getInstance = () => instance

/** Creates an instance of the Auth0 SDK. If one has already been created, it returns that instance */
export const Security = ({
  ...options
}) => {
  if (instance) return instance

  // The 'instance' is simply a Vue object
  instance = new Vue({
    data () {
      return {
        level: 'LEVEL 1',
        auth: this.$auth,
        token: function () {
          // return this.$auth.getTokenSilently({ audience: 'http://localhost:8000/' })
          return this.$auth.getTokenSilently()
        },
        user: function () {
          return this.$auth.user
        }
      }
    },
    methods: {}
  })

  return instance
}

export const SecurityPlugin = {
  install (Vue, options) {
    Vue.prototype.security = Security(options)
    console.log('SECURITY INJECTION COMPLETE ', Vue.prototype.security)
  }
}
