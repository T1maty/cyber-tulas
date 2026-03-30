const API_BASE_URL = ''; 

const TOKEN_KEY = 'cyber-tulas-token';

function getToken() { return localStorage.getItem(TOKEN_KEY); }
function saveToken(token) { localStorage.setItem(TOKEN_KEY, token); }
function removeToken() { localStorage.removeItem(TOKEN_KEY); }

async function apiFetch(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`/api${endpoint}`, {
    ...options,
    headers,
  });

  let data = null;
  try {
    data = await response.json();
  } catch (e) {
    data = null;
  }

  return { ok: response.ok, status: response.status, data };
}

async function apiRegister(username, email, password) {
  return apiFetch('/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password }),
  });
}

async function apiLogin(username, password) {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch(`/api/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });

  let data = null;
  try {
    data = await response.json();
    if (response.ok && data.access_token) {
      saveToken(data.access_token);
    }
  } catch (e) {
    data = null;
  }

  return { ok: response.ok, status: response.status, data };
}