/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
import http from 'src/http-common'

class DataService {
  clearData (viewtable: string, database: string, url: string, schema: string, token: string): Promise<any> {
    return http.post('/api/db/clear', { viewtable: viewtable, database: database, url: url }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getRows (viewtable: string, database: string, url: string, schema: string, token: string): Promise<any> {
    return http.post('/api/db/rows', { viewtable: viewtable, database: database, url: url }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

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

  testConnection (type: string, url: string, token: string): Promise<any> {
    return http.post('/api/db/test', { type: type, url: url }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  deleteProject (name: string, token: string): Promise<any> {
    return http.delete('/api/minds/project/' + name, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  createProject (name: string, token: string): Promise<any> {
    return http.post('/api/minds/project/' + name, {}, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  listProjects (token: string): Promise<any> {
    return http.get('/api/minds/projects', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  listDatabases (token: string): Promise<any> {
    return http.get('/api/minds/databases', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  listTables (database: string, token: string): Promise<any> {
    return http.get('/api/minds/' + database + '/tables', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  listModels (project: string, token: string): Promise<any> {
    return http.get('/api/minds/' + project + '/models', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getModel (model: string, token: string): Promise<any> {
    return http.get('/api/minds/models/' + model, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  listJobs (project: string, token: string): Promise<any> {
    return http.get('/api/minds/' + project + '/jobs', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getJob (job: string, token: string): Promise<any> {
    return http.get('/api/minds/jobs/' + job, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getProject (project: string, token: string): Promise<any> {
    return http.get('/api/minds/projects/' + project, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  listViews (project: string, token: string): Promise<any> {
    return http.get('/api/minds/' + project + '/views', {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getView (view: string, token: string): Promise<any> {
    return http.get('/api/minds/views/' + view, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  getMock (): Promise<any> {
    return http.get('/apitest/')
  }

  createSchema (type: string, url: string, schema: string, token: string): Promise<any> {
    return http.post('/api/db/schema', { type: type, url: url, schema: schema }, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  fetchTables (type: string, url: string, schema: string, token: string): Promise<any> {
    return http.post('/api/db/tables', { type: type, url: url, schema: schema }, {
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
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
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

  // name: string, dbtype: string, user: string, pwd: string, host: string, port: string, dbname: string
  createDatabase (mindsobj: any, token: string): Promise<any> {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access,@typescript-eslint/restrict-plus-operands
    return http.post('/api/minds/database', mindsobj, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
  }

  saveProcessor (processor: any, token: string): Promise<any> {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access,@typescript-eslint/restrict-plus-operands
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

  newFile (collection: string, folder: string, fid: string, name: string, saveas: boolean, type: string, icon: string, file: string, token: string): Promise<any> {
    const path = encodeURI('/api/files/' + collection + '/' + folder)

    const authString = 'Bearer ' + token
    console.log('AUTH_STRING', authString)
    return http.post(path, { saveas: saveas, name: name, id: fid, file: file, type: type, icon: icon }, {
      headers: {
        Authorization: authString
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
