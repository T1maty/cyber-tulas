// ===== DASHBOARD LOGIC =====

const AVAILABLE_SERVERS = [
 {
    id: 'alpha-01',
    name: 'Alpha Node',
    description: 'Main computing node. High performance.',
    icon: '🖥️',
    region: 'EU-West',
  },
  {
    id: 'beta-02',
    name: 'Beta Cluster',
    description: 'Cluster for distributed tasks and balancing.',
    icon: '⚙️',
    region: 'US-East',
  },
  {
    id: 'gamma-03',
    name: 'Gamma Relay',
    description: 'Proxy server with minimal latency.',
    icon: '🌐',
    region: 'AS-Tokyo',
  },
  {
    id: 'delta-04',
    name: 'Delta Vault',
    description: 'Secure server for data storage.',
    icon: '🔒',
    region: 'EU-North',
  },
  {
    id: 'omega-05',
    name: 'Omega Edge',
    description: 'Edge node for CDN and content caching.',
    icon: '⚡',
    region: 'US-West',
  },
];

// ---- Open Dashboard ----
function openDashboard(username) {
  document.getElementById('authWrapper').classList.add('hidden');
  const dash = document.getElementById('dashboard');
  dash.classList.remove('hidden');

  document.getElementById('navUsername').textContent = username;
  document.getElementById('welcomeName').textContent = username;

  renderServerGrid(username);
}

// ---- Nav click ----
function navClick(el, section) {
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
  el.classList.add('active');
}

// ---- Get user servers ----
function getUserServers(username) {
  const users = getUsers();
  return (users[username] && users[username].servers) ? users[username].servers : [];
}

function setUserServers(username, servers) {
  const users = getUsers();
  if (users[username]) {
    users[username].servers = servers;
    saveUsers(users);
  }
}

// ---- Render server grid ----
function renderServerGrid(username) {
  const grid       = document.getElementById('serverGrid');
  const emptyState = document.getElementById('emptyState');
  const servers    = getUserServers(username);

  grid.innerHTML = '';

  if (servers.length === 0) {
    emptyState.classList.remove('hidden');
    return;
  }

  emptyState.classList.add('hidden');

  servers.forEach(serverId => {
    const server = AVAILABLE_SERVERS.find(s => s.id === serverId);
    if (!server) return;

    const card = document.createElement('div');
    card.className = 'server-card';
    card.innerHTML = `
      <div class="server-card-header">
        <span class="server-card-icon">${server.icon}</span>
        <div class="server-card-status">
          <span class="status-dot"></span>
          Online
        </div>
      </div>
      <div class="server-card-name">${server.name}</div>
      <div class="server-card-desc">${server.description}</div>
      <div class="server-card-footer">
        <span class="server-card-region">${server.region}</span>
        <button class="btn-remove" onclick="removeServer('${server.id}')">Delete</button>
      </div>
    `;
    grid.appendChild(card);
  });
}

// ---- Remove server ----
function removeServer(serverId) {
  const session = getSession();
  if (!session) return;

  let servers = getUserServers(session.username);
  servers = servers.filter(id => id !== serverId);
  setUserServers(session.username, servers);
  renderServerGrid(session.username);
}

// ---- Modal ----
function openServerModal() {
  const session = getSession();
  if (!session) return;

  const addedServers = getUserServers(session.username);
  const modal = document.getElementById('serverModal');
  const list  = document.getElementById('availableServersList');

  list.innerHTML = '';

  AVAILABLE_SERVERS.forEach(server => {
    const isAdded = addedServers.includes(server.id);
    const item = document.createElement('div');
    item.className = 'modal-server-item' + (isAdded ? ' added' : '');
    item.innerHTML = `
      <span class="item-icon">${server.icon}</span>
      <div class="item-info">
        <div class="item-name">${server.name}</div>
        <div class="item-desc">${server.description} · ${server.region}</div>
      </div>
      <button class="item-add-btn" ${isAdded ? 'disabled' : ''}>
        ${isAdded ? '✓ Added' : '+ Add'}
      </button>
    `;

    if (!isAdded) {
      item.addEventListener('click', () => addServer(server.id));
    }

    list.appendChild(item);
  });

  modal.classList.remove('hidden');
}

function closeServerModal() {
  document.getElementById('serverModal').classList.add('hidden');
}

// click outside modal to close
document.getElementById('serverModal').addEventListener('click', function(e) {
  if (e.target === this) closeServerModal();
});

// ---- Add server ----
function addServer(serverId) {
  const session = getSession();
  if (!session) return;

  const servers = getUserServers(session.username);
  if (!servers.includes(serverId)) {
    servers.push(serverId);
    setUserServers(session.username, servers);
  }

  closeServerModal();
  renderServerGrid(session.username);
}
