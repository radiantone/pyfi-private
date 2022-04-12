/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */

import { Dictionary } from 'jsplumbtoolkit';
import http from 'src/http-common'

class DataService {

    login (data: any): Promise<any> {
        return http.post('/login', data);
    }

    logout (): Promise<any> {
        return http.get('/logout');
    }

}

export default new DataService();