// agentService.js
import axios from 'axios';

function getAuthHeaders() {
  const token = localStorage.getItem('token');
  return {
    headers: {
      authorization: `Bearer ${token}`
    }
  };
}

function handleError(err) {
  if (err.response) {
    console.error(`Server Error: Code=${err.response.status}`, err.response.data);
  } else if (err.request) {
    console.error('Request has no response: ', err.request);
  } else {
    console.error('Request setting error: ', err.message);
  }
  throw err;
}

export async function sendQueryToAgent(query) {
  try {
    const data = { query };
    const response = await axios.post('/api/agent/agent/', data, getAuthHeaders());
    return response.data;
  } catch (err) {
    handleError(err);
  }
}
