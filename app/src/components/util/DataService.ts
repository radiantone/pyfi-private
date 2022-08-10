/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
import http from 'src/http-common'
const crypto = require('crypto')


class DataService {
  getFiles (collection: string, folder: string): Promise<any> {
    return http.get('/api/files/' + collection + '/' + folder)
  }

  getObjects (object: string): Promise<any> {
    return http.get('/api/' + object)
  }

  purgeQueue (queue: string): Promise<any> {
    return http.delete('/api/queue/' + queue + '/contents')
  }

  getCommits (repo: string, file: string): Promise<any> {
    return http.post('/api/git', { repo: repo, file: file })
  }

  getCode (repo: string, hash: string): Promise<any> {
    return http.post('/api/git/code', { repo: repo, commit: hash })
  }

  loginProcessor (id: string, password: string): Promise<any> {
    return http.post('/api/login/' + id, { password: password })
  }

  getOutput (resultid: string): Promise<any> {
    return http.get('/api/output/' + resultid)
  }

  getResult (resultid: string): Promise<any> {
    return http.get('/api/result/' + resultid)
  }

  getCalls (processor: string): Promise<any> {
    return http.get('/api/calls/' + processor)
  }

  getVersions (flow: string): Promise<any> {
    return http.get('/api/versions/' + flow)
  }

  getDeployments (processor: string): Promise<any> {
    return http.get('/api/deployments/' + processor)
  }

  getWorkers (processor: string): Promise<any> {
    return http.get('/api/workers/' + processor)
  }

  getMessages (queue: string): Promise<any> {
    return http.get('/api/queue/messages/' + queue)
  }

  saveProcessor (processor: any): Promise<any> {
    processor['receipt'] = crypto.randomUUID()
    return http.post('/api/processor/' + processor.id, processor)
  }

  emptyAllQueues (): Promise<any> {
    return http.get('/api/emptyqueues/')
  }

  getProcessor (id: string): Promise<any> {
    return http.get('/api/processor/' + id)
  }

  getProcessors (): Promise<any> {
    return http.get('/api/processors')
  }

  newFile (collection: string, folder: string, fid: string, name: string, saveas: boolean, type: string, icon:string, file: string): Promise<any> {
    const path = encodeURI('/api/files/' + collection + '/' + folder)

    return http.post(path, { saveas: saveas, name: name, id: fid, file: file, type: type, icon: icon })
  }

  newFolder (collection: string, folder: string): Promise<any> {
    return http.get('/api/folder/' + collection + '/' + folder)
  }

  getPattern (name: string): Promise<any> {
    return http.get('/api/pattern/' + name)
  }

  getNetworks (): Promise<any> {
    return http.get('/api/networks')
  }

  getFile (id: string): Promise<any> {
    return http.get('/api/files/' + id)
  }

  deleteFile (id: string): Promise<any> {
    return http.delete('/api/files/' + id)
  }

  login (data: any): Promise<any> {
    return http.post('/api/login', data)
  }

  logout (): Promise<any> {
    return http.get('/api/logout')
  }
}

export default new DataService()
