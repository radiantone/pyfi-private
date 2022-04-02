/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */

import { Dictionary } from 'jsplumbtoolkit';
import http from 'src/http-common'

class DataService {

    authenticated (): Promise<any> {
        return http.get('/authenticated');
    }

    login (data: any): Promise<any> {
        return http.post('/login', data);
    }

    logout (): Promise<any> {
        return http.get('/logout');
    }

    recentjobs (days : String): Promise<any> {
        return http.get('/recentjobs/' + days);
    }

    batchjobs (batch: String, page: any): Promise<any> {
        return http.get('/batch/'+batch+'/jobs?page=' + page['page'] + '&size=' + page['rowsPerPage'] + '&state=' + page['state'] + '&filter=' + page['filter'] + '&sort=' + page['sortBy'] + '&descend=' + page['descending']);
    }

    logs (jobid: String, page: any): Promise<any> {
        return http.get('/logs/' + jobid + '?page=' + page['page'] + '&size=' + page['rowsPerPage'] + '&state=' + page['state'] + '&filter=' + page['filter'] + '&sort=' + page['sortBy'] + '&descend=' + page['descending']);
    }

    appjobs (appid: String, page: any): Promise<any> {
        return http.get('/jobs?appid=' + appid + '&page=' + page['page'] + '&size=' + page['rowsPerPage'] + '&state=' + page['state'] + '&filter=' + page['filter'] + '&sort=' + page['sortBy'] + '&descend=' + page['descending']);
    }

    jobs (page: any): Promise<any> {
        return http.get('/jobs?page=' + page['page'] + '&size=' + page['rowsPerPage'] + '&state=' + page['state'] + '&filter=' + page['filter'] + '&sort=' + page['sortBy'] + '&descend=' + page['descending']);
    }

    sitebatches (site: String, page: any): Promise<any> {
        return http.get('/site/' + site + '/batches?page=' + page['page'] + '&size=' + page['rowsPerPage'] + '&filter=' + page['filter'] + '&sort=' + page['sortBy'] + '&descend=' + page['descending']);
    }

    batches (page: any): Promise<any> {
        return http.get('/batches?page=' + page['page'] + '&size=' + page['rowsPerPage'] + '&filter=' + page['filter'] + '&sort=' + page['sortBy'] + '&descend=' + page['descending']);
    }

    sites (page: any): Promise<any> {
        return http.get('/sites?page=' + page['page'] + '&size=' + page['rowsPerPage'] + '&filter=' + page['filter'] + '&sort=' + page['sortBy'] + '&descend=' + page['descending']);
    }

    apps (page: any): Promise<any> {
        return http.get('/apps?page=' + page['page'] + '&size=' + page['rowsPerPage'] + '&filter=' + page['filter'] + '&sort=' + page['sortBy'] + '&descend=' + page['descending']);
    }
}

export default new DataService();