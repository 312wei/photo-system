import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const uploadImages = async (formData) => {
  const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data.uploaded_files;
};

export const fetchImages = async () => {
  const response = await axios.get(`${API_BASE_URL}/images/`);
  return response.data;
};