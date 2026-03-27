
function switchTab(tab) {
  const loginForm    = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const loginTab     = document.getElementById('loginTab');
  const registerTab  = document.getElementById('registerTab');
  const indicator    = document.getElementById('tabIndicator');

  clearErrors();

  if (tab === 'login') {
    loginForm.classList.remove('hidden');
    registerForm.classList.add('hidden');
    loginTab.classList.add('active');
    registerTab.classList.remove('active');
    indicator.classList.remove('right');
  } else {
    registerForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
    registerTab.classList.add('active');
    loginTab.classList.remove('active');
    indicator.classList.add('right');
  }
}

function clearErrors() {
  document.querySelectorAll('.error-msg').forEach(el => el.textContent = '');
}

function showError(id, msg) {
  const el = document.getElementById(id);
  if (el) el.textContent = msg;
}

function setButtonLoading(btn, loading) {
  btn.disabled = loading;
  btn.style.opacity = loading ? '0.6' : '1';
}

function extractErrorMessage(data) {
  if (!data) return 'Помилка з\'єднання з сервером';
  if (typeof data.detail === 'string') return data.detail;
  if (Array.isArray(data.detail)) {
    return data.detail.map(e => e.msg).join(', ');
  }
  if (data.message) return data.message;
  return 'Невідома помилка';
}

// ---- Register ----
async function handleRegister() {
  const username = document.getElementById('regUsername').value.trim();
  const email    = document.getElementById('regEmail').value.trim();
  const password = document.getElementById('regPassword').value;
  const confirm  = document.getElementById('regConfirm').value;

  clearErrors();

  if (!username || !email || !password || !confirm) {
    return showError('registerError', 'Please fill in all fields');
  }

  if (password !== confirm) {
    return showError('registerError', 'Passwords do not match');
  }

  const btn = document.querySelector('#registerForm .btn-primary');
  setButtonLoading(btn, true);

  const { ok, data } = await apiRegister(username, email, password);

  setButtonLoading(btn, false);

  if (!ok) {
    return showError('registerError', extractErrorMessage(data));
  }

  if (data.access_token) {
    saveToken(data.access_token);
  }

  const displayName = data.username || username;
  saveSession({ username: displayName, email });
  openDashboard(displayName);
}

// ---- Login ----
async function handleLogin() {
  const username = document.getElementById('loginUsername').value.trim();
  const password = document.getElementById('loginPassword').value;

  clearErrors();

  if (!username || !password) {
    return showError('loginError', 'Please enter both username and password');
  }

  const btn = document.querySelector('#loginForm .btn-primary');
  setButtonLoading(btn, true);

  const { ok, data } = await apiLogin(username, password);

  setButtonLoading(btn, false);

  if (!ok) {
    return showError('loginError', extractErrorMessage(data));
  }

  if (data.access_token) {
    saveToken(data.access_token);
  }

  const displayName = data.username || username;
  saveSession({ username: displayName, email: data.email || '' });
  openDashboard(displayName);
}

// ---- Logout ----
function handleLogout() {
  removeToken();
  clearSession();

  document.getElementById('dashboard').classList.add('hidden');
  document.getElementById('authWrapper').classList.remove('hidden');

  ['loginUsername','loginPassword','regUsername','regEmail','regPassword','regConfirm']
    .forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });

  clearErrors();
  switchTab('login');
}

const SESSION_KEY = 'cyber-tulas-session';

function getSession() {
  try { return JSON.parse(localStorage.getItem(SESSION_KEY)); }
  catch { return null; }
}

function saveSession(user) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem(SESSION_KEY);
}