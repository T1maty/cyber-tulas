// ===== APP INIT =====

(function init() {
 // comment opendashboard when you have backend ready and want to test auth flow
  openDashboard('dev-user');
  return;

  const session = getSession();
  if (session && session.username) {
    openDashboard(session.username);
  }

  const dashCSS = document.createElement('link');
  dashCSS.rel  = 'stylesheet';
  dashCSS.href = 'css/dashboard.css';
  document.head.appendChild(dashCSS);
})();