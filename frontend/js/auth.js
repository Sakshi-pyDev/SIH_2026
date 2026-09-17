/**
 * auth.js - Authentication and Session Management
 * SIF Precursor Detection System — Oil India Limited
 */

window.API_BASE = window.API_BASE || "http://127.0.0.1:8000";

const AuthState = {
  getToken: () => localStorage.getItem('oil_sif_token'),
  getRole: () => localStorage.getItem('oil_sif_role'),
  getUsername: () => localStorage.getItem('oil_sif_username'),
  isLoggedIn: () => !!localStorage.getItem('oil_sif_token'),

  setSession: (token, role, username) => {
    localStorage.setItem('oil_sif_token', token);
    localStorage.setItem('oil_sif_role', role);
    localStorage.setItem('oil_sif_username', username);
    AuthState.updateUI();
  },

  clearSession: () => {
    localStorage.removeItem('oil_sif_token');
    localStorage.removeItem('oil_sif_role');
    localStorage.removeItem('oil_sif_username');
    AuthState.updateUI();
  },

  updateUI: () => {
    const isLoggedIn = AuthState.isLoggedIn();
    const role = AuthState.getRole();
    const username = AuthState.getUsername();

    // Elements in navbar
    const authBtns = document.querySelectorAll('.nav-auth-buttons');
    const userSession = document.querySelectorAll('.nav-user-session');
    const usernameDisplays = document.querySelectorAll('.user-name-display');
    const roleDisplays = document.querySelectorAll('.user-role-display');

    // Hero section buttons on the landing page (index.html) - role-based
    const heroGuest = document.querySelectorAll('.hero-actions-guest');
    const heroReport = document.querySelectorAll('.hero-actions-report');   // field_worker + admin
    const heroDashboard = document.querySelectorAll('.hero-actions-dashboard'); // safety_officer + admin

    if (isLoggedIn) {
      authBtns.forEach(el => el.style.display = 'none');
      userSession.forEach(el => el.style.display = 'flex');
      usernameDisplays.forEach(el => el.textContent = username);
      roleDisplays.forEach(el => el.textContent = (role || '').replace('_', ' ').toUpperCase());

      heroGuest.forEach(el => el.style.display = 'none');

      const canReport = (role === 'field_worker' || role === 'admin');
      const canViewDashboard = (role === 'safety_officer' || role === 'admin');

      heroReport.forEach(el => el.style.display = canReport ? 'flex' : 'none');
      heroDashboard.forEach(el => el.style.display = canViewDashboard ? 'flex' : 'none');
    } else {
      authBtns.forEach(el => el.style.display = 'flex');
      userSession.forEach(el => el.style.display = 'none');

      heroGuest.forEach(el => el.style.display = 'flex');
      heroReport.forEach(el => el.style.display = 'none');
      heroDashboard.forEach(el => el.style.display = 'none');
    }

    const activeUser = document.getElementById('activeUserLabel');
    if (activeUser) {
      activeUser.textContent = username ? `${username} (${(role || 'worker').replace('_', ' ')})` : 'worker1 (Field Worker)';
    }

    // Nav bar "Submit Safety Report" / "Surveillance Dashboard" links - role based
    const navReport = document.getElementById('navLinkReport');
    const navDashboard = document.getElementById('navLinkDashboard');
    const canReportNav = isLoggedIn && (role === 'field_worker' || role === 'admin');
    const canDashboardNav = isLoggedIn && (role === 'safety_officer' || role === 'admin');
    if (navReport) navReport.style.display = canReportNav ? '' : 'none';
    if (navDashboard) navDashboard.style.display = canDashboardNav ? '' : 'none';

    // Dynamic Admin Console link injection for admin users
    const navLinks = document.querySelector('.gov-nav-links');
    if (navLinks) {
      let adminLink = document.getElementById('navLinkAdmin');
      if (role === 'admin') {
        if (!adminLink) {
          adminLink = document.createElement('a');
          adminLink.id = 'navLinkAdmin';
          adminLink.href = 'admin.html';
          adminLink.innerHTML = '👑 Admin Console';
          adminLink.style.color = '#8B5CF6';
          adminLink.style.fontWeight = '700';
          if (window.location.pathname.endsWith('admin.html')) {
            adminLink.className = 'active';
          }
          navLinks.appendChild(adminLink);
        }
      } else if (adminLink) {
        adminLink.remove();
      }
    }
  }
};

async function handleLogin(username, password) {
  const form = new URLSearchParams();
  form.append('username', username);
  form.append('password', password);

  const res = await fetch(`${window.API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Login failed. Invalid username or password.');
  }

  AuthState.setSession(data.access_token, data.role, username);
  return data;
}

async function handleRegister(username, password, role) {
  const res = await fetch(`${window.API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, role })
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || 'Registration failed.');
  }

  AuthState.setSession(data.access_token, data.role, username);
  return data;
}

async function quickAdminLogin() {
  try {
    const form = new URLSearchParams();
    form.append('username', 'admin');
    form.append('password', 'password');

    let res = await fetch(`${window.API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form
    });

    // If admin not yet created, register it
    if (!res.ok) {
      await fetch(`${window.API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'admin', password: 'password', role: 'admin' })
      });
      res = await fetch(`${window.API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: form
      });
    }

    if (res.ok) {
      const data = await res.json();
      AuthState.setSession(data.access_token, data.role, 'admin');
      window.location.href = 'admin.html';
    }
  } catch(e) {
    console.error('Quick admin login failed', e);
  }
}

function handleLogout() {
  AuthState.clearSession();
  localStorage.removeItem('oil_sif_token');
  localStorage.removeItem('oil_sif_role');
  localStorage.removeItem('oil_sif_username');
  AuthState.updateUI();

  if (window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/')) {
    window.location.reload();
  } else {
    window.location.href = 'index.html';
  }
}

// Global click listener for Sign Out buttons
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.btn-nav-logout');
  if (btn) {
    e.preventDefault();
    handleLogout();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  AuthState.updateUI();
});
