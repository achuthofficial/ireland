import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const assessUpload = async (file) => {
  const formData = new FormData();
  formData.append('contract', file);

  const response = await axios.post(`${API_BASE_URL}/assess/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const assessQuestionnaire = async (responses) => {
  const response = await api.post('/assess/questionnaire', { responses });
  return response.data;
};

export const compareContracts = async (files) => {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('contracts[]', file);
  });

  const response = await axios.post(`${API_BASE_URL}/compare`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const generateReport = async (assessment) => {
  const response = await api.post('/report/generate', { assessment }, {
    responseType: 'blob',
  });

  return response.data;
};

export const getOverviewStats = async () => {
  const response = await api.get('/stats/overview');
  return response.data;
};

export const getVendorList = async () => {
  const response = await api.get('/vendors/list');
  return response.data;
};

export const getTemplates = async () => {
  const response = await api.get('/templates/all');
  return response.data;
};

export default api;
