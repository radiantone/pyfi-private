/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */

import { Dictionary } from 'jsplumbtoolkit';
import http from 'src/http-common'

class DataService {

    getFiles (collection: string, folder: string): Promise<any> {
        return http.get('/api/files/'+collection+'/'+folder);
    }

    newFile (collection: string, folder: string, name: string, type: string, icon:string, file: string): Promise<any> {
        var path = encodeURI('/api/files/' + collection + '/' + folder);
        console.log("newFile", path);

        return http.post(path, { 'name': name, 'file': file, 'type':type, 'icon':icon});
    }

    getFile (id: string): Promise<any> {
        return http.get('/api/files/' + id);
    }

    deleteFile (id: string): Promise<any> {
        return http.delete('/api/files/' + id);
    }


    login (data: any): Promise<any> {
        return http.post('/api/login', data);
    }

    logout (): Promise<any> {
        return http.get('/api/logout');
    }

}

export default new DataService();