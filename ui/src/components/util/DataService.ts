/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
import http from 'src/http-common'

class DataService {
  getFiles (collection: string, folder: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/files/' + collection + '/' + folder, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getSubscriptions (email: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/subscriptions/' + email, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getObjects (object: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/' + object, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  purgeQueue (queue: string, token: string): Promise<any> {
    return http.delete('https://api.elasticcode.ai/queue/' + queue + '/contents', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getCommits (repo: string, file: string, token: string): Promise<any> {
    return http.post('https://api.elasticcode.ai/git', { repo: repo, file: file }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getCode (repo: string, hash: string, token: string): Promise<any> {
    return http.post('https://api.elasticcode.ai/git/code', { repo: repo, commit: hash }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  loginProcessor (id: string, password: string, token: string): Promise<any> {
    return http.post('https://api.elasticcode.ai/login/' + id, { password: password }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  askChat (question: string, token: string): Promise<any> {
    return http.post('https://api.elasticcode.ai/chatgpt', { question: question }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getOutput (resultid: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/output/' + resultid, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getResult (resultid: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/result/' + resultid, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getCalls (processor: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/calls/' + processor, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getVersions (flow: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/versions/' + flow, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getDeployments (processor: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/deployments/' + processor, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getWorkers (processor: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/workers/' + processor, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getMessages (queue: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/queue/messages/' + queue, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getQueues (token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/queues', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  saveProcessor (processor: any, token: string): Promise<any> {
    return http.post('https://api.elasticcode.ai/processor/' + processor.name, processor, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  emptyAllQueues (): Promise<any> {
    return http.get('https://api.elasticcode.ai/emptyqueues/')
  }

  getProcessor (id: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/processor/' + id, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getProcessors (token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/processors', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  newFile (collection: string, folder: string, fid: string, name: string, saveas: boolean, type: string, icon:string, file: string, token: string): Promise<any> {
    const path = encodeURI('https://api.elasticcode.ai/files/' + collection + '/' + folder)

    return http.post(path, { saveas: saveas, name: name, id: fid, file: file, type: type, icon: icon }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  newFolder (collection: string, folder: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/folder/' + collection + '/' + folder, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getPattern (name: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/pattern/' + name, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getNetworks (token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/networks', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getFile (id: string, token: string): Promise<any> {
    return http.get('https://api.elasticcode.ai/files/' + id, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  deleteFile (id: string, token: string): Promise<any> {
    return http.delete('https://api.elasticcode.ai/files/' + id, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  login (data: any): Promise<any> {
    return http.post('https://api.elasticcode.ai/login', data)
  }

  logout (): Promise<any> {
    return http.get('https://api.elasticcode.ai/logout')
  }
}

export default new DataService()
