<script>
import axios from 'axios'

export default {
  name: 'ObjectService',
  async getFlow (id, user) {
    const token = user.accessToken
    try {
      const res = await axios.get(process.env.APISERVER + '/flow/' + id, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async getUserSettings (user) {
    const token = user.accessToken
    try {
      const res = await axios.get(process.env.APISERVER + '/usersettings', {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async updateUserSettings (settings, user) {
    const token = user.accessToken
    try {
      const res = await axios.post(process.env.APISERVER + '/usersettings', settings, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async getObject (collection, id, user) {
    const token = user.accessToken
    try {
      const res = await axios.get(process.env.APISERVER + '/get/' + collection + '/' + id, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async getObjects (collection, query, user) {
    try {
      const res = await axios.get(process.env.APISERVER + '/events')

      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async deleteObject (collection, object, user) {
    try {
      const token = user.accessToken
      const payload = {
        collection: collection,
        operation: 'delete',
        object: object
      }
      const res = await axios.post(process.env.APISERVER + '/files/object', payload, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async updateObject (collection, object, user) {
    try {
      const token = user.accessToken
      const payload = {
        collection: collection,
        operation: 'update',
        object: object
      }
      console.log('updateObject: ', object)
      const res = await axios.post(process.env.APISERVER + '/files/object', payload, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async createObject (collection, directory, object, user) {
    try {
      const token = user.accessToken
      object.parent = directory
      object.path = directory + '/' + object.name
      const payload = {
        collection: collection,
        operation: 'create',
        object: object
      }
      const res = await axios.post(process.env.APISERVER + '/files/object', payload, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async listFiles (collection, directory, user) {
    try {
      const token = user.accessToken
      console.log('USER:', user)
      const res = await axios.post(process.env.APISERVER + '/files?collection=' + collection, {
        parent: directory
      }, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async makeDirectory (collection, parent, directory, user) {
    try {
      const token = user.accessToken
      const payload = {
        collection: collection,
        operation: 'create',
        object: {
          path: parent + '/' + directory,
          name: directory,
          icon: 'folder',
          type: 'folder',
          parent: parent,
          date: new Date() + ''
        }
      }
      const res = await axios.post(process.env.APISERVER + '/files/object', payload, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async deleteObjects (collection, oid, user) {
    try {
      const res = await axios.get(process.env.APISERVER + '/events/' + eventId)
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  },
  async deleteDirectory (collection, directory, force, user) {
    try {
      const res = await axios.get(process.env.APISERVER + '/events/' + eventId)
      return res.data
    } catch (err) {
      window.global.root.$emit('show.alert', {
        color: 'negative',
        timeout: 2000,
        position: 'top',
        message: err.response.data.message,
        icon: 'save'
      })
    }
  }
}
</script>
