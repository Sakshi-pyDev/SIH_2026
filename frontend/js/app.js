/**
 * app.js - Core Application Logic
 * SIF Precursor Detection System — Oil India Limited
 */

// ========== THEME TOGGLE (LIGHT / DARK MODE) ==========
function initTheme() {
  const savedTheme = localStorage.getItem('oil_sif_theme') || 'light';
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
  } else {
    document.body.classList.remove('dark-mode');
  }
  updateThemeButtonText();
}

function toggleTheme() {
  const isDark = document.body.classList.toggle('dark-mode');
  localStorage.setItem('oil_sif_theme', isDark ? 'dark' : 'light');
  updateThemeButtonText();
}

function updateThemeButtonText() {
  const isDark = document.body.classList.contains('dark-mode');
  document.querySelectorAll('.btn-theme-toggle').forEach(btn => {
    btn.innerHTML = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  });
}

// ========== SPA NAVIGATION & ROUTING ==========
const PAGE_TITLES = {
  home: 'Welcome to SIF Precursor Portal',
  report: 'File Incident / Precursor Report',
  dashboard: 'Reports Telemetry Dashboard'
};

function navigateToPage(pageName, updateHash = true) {
  const target = document.getElementById(`page-${pageName}`);
  if (!target) return;

  // Toggle active section
  document.querySelectorAll('.page-section').forEach(sec => sec.classList.remove('active'));
  target.classList.add('active');

  // Update navigation links
  document.querySelectorAll('.gov-nav-links a').forEach(link => link.classList.remove('active'));
  const navLink = document.getElementById(`navLink${capitalize(pageName)}`);
  if (navLink) navLink.classList.add('active');

  // Update breadcrumb
  const breadcrumbCurrent = document.getElementById('breadcrumbCurrent');
  if (breadcrumbCurrent) {
    breadcrumbCurrent.textContent = PAGE_TITLES[pageName] || capitalize(pageName);
  }

  // Hash routing
  if (updateHash) {
    window.location.hash = pageName;
  }

  // Load specific page data
  if (pageName === 'dashboard') {
    loadDashboardReports();
  } else if (pageName === 'report') {
    checkReportPermissions();
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function handleHashChange() {
  const hash = window.location.hash.replace('#', '') || 'home';
  if (['home', 'report', 'dashboard'].includes(hash)) {
    navigateToPage(hash, false);
  }
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// ========== REPORT FILING & AUTOCOMPLETE ==========
let suggestDebounceTimer = null;

function onReportTextInput() {
  clearTimeout(suggestDebounceTimer);
  suggestDebounceTimer = setTimeout(async () => {
    const textarea = document.getElementById('repText');
    if (!textarea) return;

    const words = textarea.value.trim().split(/\s+/);
    const query = words.slice(-4).join(' ');
    if (query.length < 2) {
      hideSuggestions();
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/suggest?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      renderSuggestions(data.suggestions || []);
    } catch (e) {
      hideSuggestions();
    }
  }, 220);
}

function renderSuggestions(suggestions) {
  const box = document.getElementById('suggestBox');
  if (!box) return;

  if (!suggestions || suggestions.length === 0) {
    hideSuggestions();
    return;
  }

  box.innerHTML = suggestions.map(s => `
    <div class="suggest-option" onmousedown="applySuggestion('${s.replace(/'/g, "\\'")}')">
      🔍 ${s}
    </div>
  `).join('');
  box.style.display = 'block';
}

function applySuggestion(suggestionText) {
  const textarea = document.getElementById('repText');
  if (!textarea) return;

  const words = textarea.value.trim().split(/\s+/);
  const kept = words.slice(0, Math.max(0, words.length - 4)).join(' ');
  textarea.value = (kept ? kept + ' ' : '') + suggestionText + ' ';
  textarea.focus();
  hideSuggestions();
}

function hideSuggestions() {
  const box = document.getElementById('suggestBox');
  if (box) box.style.display = 'none';
}

document.addEventListener('click', (e) => {
  if (!e.target.closest('#repText') && !e.target.closest('#suggestBox')) {
    hideSuggestions();
  }
});

function checkReportPermissions() {
  if (!AuthState.isLoggedIn()) {
    window.location.href = 'login.html';
    return;
  }

  const role = AuthState.getRole();
  const notice = document.getElementById('reportRoleNotice');
  const btn = document.getElementById('submitReportBtn');

  if (role !== 'field_worker' && role !== 'admin') {
    if (notice) notice.style.display = 'flex';
    if (btn) btn.disabled = true;
  } else {
    if (notice) notice.style.display = 'none';
    if (btn) btn.disabled = false;
  }
}

async function submitIncidentReport() {
  clearAlert('reportAlert');
  if (!AuthState.isLoggedIn()) {
    window.location.href = 'login.html';
    return;
  }

  const repType = document.getElementById('repType').value;
  const location = document.getElementById('repLocation').value;
  const department = document.getElementById('repDept').value;
  const reportText = document.getElementById('repText').value.trim();

  if (!reportText) {
    showAlert('reportAlert', 'Please enter a detailed description of the observation.', 'error');
    return;
  }

  const submitBtn = document.getElementById('submitReportBtn');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Analyzing with SIF Model...';
  }

  try {
    const res = await fetch(`${API_BASE}/reports`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AuthState.getToken()}`
      },
      body: JSON.stringify({
        report_type: repType,
        location: location,
        department: department,
        report_text: reportText
      })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Failed to submit report.');
    }

    showAlert('reportAlert', 'Safety Report successfully submitted and analyzed by AI.', 'success');
    document.getElementById('repText').value = '';
    hideSuggestions();

    // Render result card with SHAP factor chips
    renderPredictionResult(data);
  } catch (err) {
    showAlert('reportAlert', err.message, 'error');
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit for AI Risk Classification →';
    }
  }
}

function renderPredictionResult(data) {
  const container = document.getElementById('predResultContainer');
  const box = document.getElementById('resultBox');
  const statusEl = document.getElementById('resultStatus');
  const probEl = document.getElementById('resultProb');
  const factorsEl = document.getElementById('resultFactors');

  if (!container || !box) return;

  const isHigh = data.predicted_label === 1;
  const prob = ((data.predicted_probability || 0) * 100).toFixed(1);

  let factors = [];
  try {
    factors = typeof data.top_factors === 'string' ? JSON.parse(data.top_factors) : (data.top_factors || []);
  } catch (e) {
    factors = [];
  }

  box.className = `result-box ${isHigh ? 'high-risk' : 'low-risk'}`;
  statusEl.innerHTML = isHigh
    ? '⚠️ <strong>SIF PRECURSOR DETECTED</strong> — High Severity Potential'
    : '✅ <strong>LOW RISK OBSERVATION</strong> — No SIF Precursor Indicators';

  probEl.textContent = `Calculated SIF Probability: ${prob}% (Confidence: ${prob > 70 ? 'High' : 'Moderate'})`;

  if (factors && factors.length > 0) {
    factorsEl.innerHTML = factors.slice(0, 5).map(f => {
      const clean = f.feature.replace('flag_', '').replace('count_', '').replace('tfidf_', '');
      const sign = f.impact > 0 ? '+' : '';
      return `<span class="factor-chip">${clean} (${sign}${f.impact})</span>`;
    }).join(' ');
  } else {
    factorsEl.innerHTML = '<span style="color:var(--text-muted); font-size:12px;">No anomalous risk drivers flagged</span>';
  }

  container.style.display = 'block';
  container.scrollIntoView({ behavior: 'smooth' });
}

// ========== DASHBOARD REPORTS LOADER ==========
async function loadDashboardReports() {
  if (!AuthState.isLoggedIn()) {
    window.location.href = 'login.html';
    return;
  }

  const tbody = document.getElementById('reportsTableBody');
  if (!tbody) return;

  tbody.innerHTML = '<tr><td colspan="9" class="empty-state">Loading reports from secure database...</td></tr>';

  try {
    const res = await fetch(`${API_BASE}/reports`, {
      headers: { 'Authorization': `Bearer ${AuthState.getToken()}` }
    });
    const reports = await res.json();
    if (!res.ok) {
      tbody.innerHTML = '<tr><td colspan="9" class="empty-state">Failed to retrieve reports telemetry.</td></tr>';
      return;
    }

    // Update statistics counters
    const total = reports.length;
    const highRisk = reports.filter(r => r.predicted_label === 1).length;
    const lowRisk = total - highRisk;

    const statTotal = document.getElementById('statTotalReports');
    const statHigh = document.getElementById('statHighRiskReports');
    const statLow = document.getElementById('statLowRiskReports');

    if (statTotal) statTotal.textContent = total;
    if (statHigh) statHigh.textContent = highRisk;
    if (statLow) statLow.textContent = lowRisk;

    if (total === 0) {
      tbody.innerHTML = '<tr><td colspan="9" class="empty-state">No hazard reports filed yet. Submit your first observation from the field.</td></tr>';
      return;
    }

    tbody.innerHTML = reports.map((r, idx) => {
      const isHigh = r.predicted_label === 1;
      const prob = r.predicted_probability !== null && r.predicted_probability !== undefined
        ? ((r.predicted_probability) * 100).toFixed(1) + '%'
        : '—';

      const dateStr = r.created_at ? new Date(r.created_at).toLocaleString('en-IN') : 'Recent';
      const excerpt = r.report_text && r.report_text.length > 85
        ? r.report_text.substring(0, 85) + '…'
        : (r.report_text || '—');

      let factors = [];
      try {
        factors = typeof r.top_factors === 'string' ? JSON.parse(r.top_factors || '[]') : (r.top_factors || []);
      } catch (e) { }

      const chips = factors.slice(0, 3).map(f => {
        const clean = f.feature.replace('flag_', '').replace('count_', '').replace('tfidf_', '');
        return `<span class="factor-chip">${clean}</span>`;
      }).join('');

      return `
        <tr>
          <td>${idx + 1}</td>
          <td><strong>${r.report_type || '—'}</strong></td>
          <td style="white-space:nowrap;">${r.location || '—'}</td>
          <td>${r.department || '—'}</td>
          <td title="${(r.report_text || '').replace(/"/g, '&quot;')}">${excerpt}</td>
          <td>
            <span class="badge-risk ${isHigh ? 'high' : 'low'}">
              ${isHigh ? '⚠️ SIF RISK' : '✅ LOW RISK'}
            </span>
            <div style="margin-top:4px;">${chips}</div>
          </td>
          <td><strong>${prob}</strong></td>
          <td>${r.submitted_by_username || '—'}</td>
          <td style="white-space:nowrap; font-size:11.5px;">${dateStr}</td>
        </tr>
      `;
    }).join('');
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-state">Error: ${e.message}</td></tr>`;
  }
}

// Helpers for Alerts
function showAlert(id, msg, type) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = msg;
  el.className = `alert alert-${type} show`;
}

function clearAlert(id) {
  const el = document.getElementById(id);
  if (el) el.className = 'alert';
}

// Startup Init
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  handleHashChange();
  window.addEventListener('hashchange', handleHashChange);
});
