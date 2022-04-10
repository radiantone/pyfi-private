import axios, { AxiosInstance } from 'axios';

const apiClient: AxiosInstance = axios.create({
    baseURL: '/',
    headers: {
        'Content-type': 'application/json',
    },
});

export default apiClient;
