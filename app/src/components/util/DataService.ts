/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */

import { Dictionary } from 'jsplumbtoolkit';
import http from 'src/http-common'

class DataService {

    getFiles (collection: string, folder: string): Promise<any> {
        return http.get('/api/files/'+collection+'/'+folder);
    }

    newFile (collection: string, folder: string, fid: string, name: string, saveas: boolean, type: string, icon:string, file: string): Promise<any> {
        var path = encodeURI('/api/files/' + collection + '/' + folder);

        var promise = http.post(path, { 'saveas': saveas, 'name': name, 'id': fid, 'file': file, 'type': type, 'icon': icon });
        console.log(promise);
        return promise;
    }

    newFolder (collection: string, folder: string): Promise<any> {
        console.log("newFolder", folder);
        return http.get('/api/folder/' + collection + '/' + folder);
    }

    getNetworks (): Promise<any> {
        return http.get('/api/networks');
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