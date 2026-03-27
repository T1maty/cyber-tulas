// ===== THEME TOGGLE =====

const THEME_KEY = 'cyber-tulas-theme';

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY) || 'dark';
  applyTheme(saved, false);
}

function applyTheme(theme, animate = true) {
  document.documentElement.setAttribute('data-theme', theme);
  const icon = document.getElementById('toggleIcon');
  const btn  = document.getElementById('themeToggle');

  if (icon) {
    icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  if (animate && btn) {
    btn.classList.add('spinning');
    setTimeout(() => btn.classList.remove('spinning'), 400);
  }

  localStorage.setItem(THEME_KEY, theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

document.getElementById('themeToggle').addEventListener('click', toggleTheme);

initTheme();
