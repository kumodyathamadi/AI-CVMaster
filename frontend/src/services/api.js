import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const uploadResume = (file, onUploadProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    return api.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress,
    });
};

export default api;
