// ===== API LAYER =====
// Всі запити до бекенду тут. Змінюй BASE_URL під свій сервер.

const API_BASE_URL = 'http://localhost:8000'; // <- змінити на свій URL

const TOKEN_KEY = 'cyber-tulas-token';

// ---- Token helpers ----
function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

// ---- Base fetch wrapper ----
async function apiFetch(endpoint, options = {}) {
  const token = getToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Повертаємо { ok, status, data }
  let data = null;
  try {
    data = await response.json();
  } catch {
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
  const token = getToken();


  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch(`${API_BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    },
    body: formData.toString(),
  });

  let data = null;
  try { data = await response.json(); } catch { data = null; }

  return { ok: response.ok, status: response.status, data };


}