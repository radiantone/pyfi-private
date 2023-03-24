/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
import http from 'src/http-common'

class DataService {
  getFiles (collection: string, folder: string, token: string): Promise<any> {
    return http.get('/api/files/' + collection + '/' + folder, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getSubscriptions (email: string, token: string): Promise<any> {
    return http.get('/api/subscriptions/' + email, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  createSchema(schema: string, token: string): Promise<any> {
    return http.post('/api/db/schema', { schema: schema }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getObjects (object: string, token: string): Promise<any> {
    return http.get('/api/' + object, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  purgeQueue (queue: string, token: string): Promise<any> {
    return http.delete('/api/queue/' + queue + '/contents', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getCommits (repo: string, file: string, token: string): Promise<any> {
    return http.post('/api/git', { repo: repo, file: file }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getCode (repo: string, hash: string, token: string): Promise<any> {
    return http.post('/api/git/code', { repo: repo, commit: hash }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  loginProcessor (id: string, password: string, token: string): Promise<any> {
    return http.post('/api/login/' + id, { password: password }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  askChat (question: string, token: string): Promise<any> {
    return http.post('/api/chatgpt', { question: question }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getOutput (resultid: string, token: string): Promise<any> {
    return http.get('/api/output/' + resultid, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getResult (resultid: string, token: string): Promise<any> {
    return http.get('/api/result/' + resultid, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getCalls (processor: string, token: string): Promise<any> {
    return http.get('/api/calls/' + processor, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getVersions (flow: string, token: string): Promise<any> {
    return http.get('/api/versions/' + flow, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getDeployments (processor: string, token: string): Promise<any> {
    return http.get('/api/deployments/' + processor, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  runBlock (block: any, call: string, token: string): Promise<any> {
    return http.post('/api/runblock', { block: block, call: call }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getWorkers (processor: string, token: string): Promise<any> {
    return http.get('/api/workers/' + processor, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getMessages (queue: string, token: string): Promise<any> {
    return http.get('/api/queue/messages/' + queue, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getCommit (): Promise<any> {
    return http.get('/commit')
  }

  getQueues (token: string): Promise<any> {
    return http.get('/api/queues', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  saveProcessor (processor: any, token: string): Promise<any> {
    return http.post('/api/processor/' + processor.name, processor, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  emptyAllQueues (): Promise<any> {
    return http.get('/api/emptyqueues/')
  }

  getProcessor (id: string, token: string): Promise<any> {
    return http.get('/api/processor/' + id, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getProcessors (token: string): Promise<any> {
    return http.get('/api/processors', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  newFile (collection: string, folder: string, fid: string, name: string, saveas: boolean, type: string, icon:string, file: string, token: string): Promise<any> {
    const path = encodeURI('/api/files/' + collection + '/' + folder)

    const auth_string = 'Bearer ' + token
    console.log('AUTH_STRING', auth_string)
    return http.post(path, { saveas: saveas, name: name, id: fid, file: file, type: type, icon: icon }, {
      headers: {
        Authorization: auth_string
      }
    })
  }

  newFolder (collection: string, folder: string, token: string): Promise<any> {
    return http.get('/api/folder/' + collection + '/' + folder, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getPattern (name: string, token: string): Promise<any> {
    return http.get('/api/pattern/' + name, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getNetworks (token: string): Promise<any> {
    return http.get('/api/networks', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getFile (id: string, token: string): Promise<any> {
    return http.get('/api/files/' + id, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  deleteFile (id: string, token: string): Promise<any> {
    return http.delete('/api/files/' + id, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  login (data: any): Promise<any> {
    return http.post('/api/login', data)
  }

  logout (): Promise<any> {
    return http.get('/api/logout')
  }
}

export default new DataService()
