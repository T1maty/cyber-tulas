// ===== APP INIT =====

(function init() {
  // Check for existing session on page load
  const session = getSession();

  if (session && session.username) {
   
    openDashboard(session.username);
  }


  const dashCSS = document.createElement('link');
  dashCSS.rel  = 'stylesheet';
  dashCSS.href = 'css/dashboard.css';
  document.head.appendChild(dashCSS);
})();
