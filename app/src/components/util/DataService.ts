/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */

import { Dictionary } from 'jsplumbtoolkit';
import http from 'src/http-common'

class DataService {

    getObjects (collection: string, folder: string): Promise<any> {
        return http.get('/api/files/'+collection+'/'+folder);
    }
    login (data: any): Promise<any> {
        return http.post('/api/login', data);
    }

    logout (): Promise<any> {
        return http.get('/api/logout');
    }

}

export default new DataService();