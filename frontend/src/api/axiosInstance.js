import axios from 'axios';
import API_URL from './general'

const axiosInstance = axios.create({
  baseURL: API_URL, // Set your API base URL here
  timeout: 5000, // Set a default timeout for requests in milliseconds
  headers: {
    'Content-Type': 'application/json', // Set default headers for requests
  },
});

export default axiosInstance;


