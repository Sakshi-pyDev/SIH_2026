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

    if (isLoggedIn) {
      authBtns.forEach(el => el.style.display = 'none');
      userSession.forEach(el => el.style.display = 'flex');
      usernameDisplays.forEach(el => el.textContent = username);
      roleDisplays.forEach(el => el.textContent = (role || '').replace('_', ' ').toUpperCase());
    } else {
      authBtns.forEach(el => el.style.display = 'flex');
      userSession.forEach(el => el.style.display = 'none');
    }

    const activeUser = document.getElementById('activeUserLabel');
    if (activeUser) {
      activeUser.textContent = username ? `${username} (${(role || 'worker').replace('_', ' ')})` : 'worker1 (Field Worker)';
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

function handleLogout() {
  AuthState.clearSession();
  window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', () => {
  AuthState.updateUI();
});
