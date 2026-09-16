/**
 * app.js - Core SIF Application Logic
 * Oil India Limited — SIF Precursor Detection System
 */

// ========== THEME MANAGEMENT ==========
function initTheme() {
  const saved = localStorage.getItem('oil_sif_theme') || 'light';
  if (saved === 'dark') {
    document.body.classList.add('dark-mode');
  } else {
    document.body.classList.remove('dark-mode');
  }
  updateThemeButtons();
}

function toggleTheme() {
  const isDark = document.body.classList.toggle('dark-mode');
  localStorage.setItem('oil_sif_theme', isDark ? 'dark' : 'light');
  updateThemeButtons();
}

function updateThemeButtons() {
  const isDark = document.body.classList.contains('dark-mode');
  document.querySelectorAll('.btn-theme-toggle').forEach(b => {
    b.innerHTML = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  });
}

// ========== OPERATIONAL CAROUSEL CONTROLLER ==========
let currentCarouselIndex = 0;
let carouselTimer = null;
const TOTAL_CAROUSEL_SLIDES = 4;

function initCarousel() {
  const slides = document.querySelectorAll('.carousel-slide');
  if (!slides.length) return;

  setCarouselSlide(0);
  startCarouselAutoPlay();

  const container = document.querySelector('.oil-carousel-card');
  if (container) {
    container.addEventListener('mouseenter', stopCarouselAutoPlay);
    container.addEventListener('mouseleave', startCarouselAutoPlay);
  }
}

function setCarouselSlide(idx) {
  currentCarouselIndex = (idx + TOTAL_CAROUSEL_SLIDES) % TOTAL_CAROUSEL_SLIDES;

  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.carousel-dot');
  const counter = document.getElementById('carouselSlideCounter');

  slides.forEach((s, i) => {
    s.classList.toggle('active', i === currentCarouselIndex);
  });

  dots.forEach((d, i) => {
    d.classList.toggle('active', i === currentCarouselIndex);
  });

  if (counter) {
    counter.textContent = `${currentCarouselIndex + 1} / ${TOTAL_CAROUSEL_SLIDES}`;
  }
}

function nextCarouselSlide() {
  setCarouselSlide(currentCarouselIndex + 1);
}

function prevCarouselSlide() {
  setCarouselSlide(currentCarouselIndex - 1);
}

function startCarouselAutoPlay() {
  stopCarouselAutoPlay();
  carouselTimer = setInterval(nextCarouselSlide, 4500);
}

function stopCarouselAutoPlay() {
  if (carouselTimer) {
    clearInterval(carouselTimer);
    carouselTimer = null;
  }
}

// ========== AUTOCOMPLETE SUGGESTIONS ==========
let suggestDebounce = null;

function onReportTextInput() {
  clearTimeout(suggestDebounce);
  suggestDebounce = setTimeout(async () => {
    const ta = document.getElementById('repText');
    if (!ta) return;

    const words = ta.value.trim().split(/\s+/);
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

function renderSuggestions(list) {
  const box = document.getElementById('suggestBox');
  if (!box) return;

  if (!list || list.length === 0) {
    hideSuggestions();
    return;
  }

  box.innerHTML = list.map(s => `
    <div class="suggest-option" onmousedown="applySuggestion('${s.replace(/'/g, "\\'")}')">
      🔍 ${s}
    </div>
  `).join('');
  box.style.display = 'block';
}

function applySuggestion(text) {
  const ta = document.getElementById('repText');
  if (!ta) return;

  const words = ta.value.trim().split(/\s+/);
  const kept = words.slice(0, Math.max(0, words.length - 4)).join(' ');
  ta.value = (kept ? kept + ' ' : '') + text + ' ';
  ta.focus();
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

// ========== QUICK DEMO WORKER AUTHENTICATION ==========
async function quickDemoLogin() {
  try {
    const form = new URLSearchParams();
    form.append('username', 'worker1');
    form.append('password', 'password');

    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form
    });

    if (res.ok) {
      const data = await res.json();
      AuthState.setSession(data.access_token, data.role, 'worker1');
      updateUserLabel();
      alert('Logged in as Field Worker (worker1)! You can now submit reports.');
    } else {
      // Try registering worker1 if doesn't exist
      const reg = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'worker1', password: 'password', role: 'field_worker' })
      });
      const data = await reg.json();
      AuthState.setSession(data.access_token, data.role, 'worker1');
      updateUserLabel();
    }
  } catch (e) {
    console.error('Quick demo login:', e);
  }
}

function updateUserLabel() {
  const label = document.getElementById('activeUserLabel');
  if (label) {
    label.textContent = AuthState.getUsername() || 'guest_worker';
  }
}

// ========== RESTORED REPORT SUBMISSION (EXACT COMMIT ad25296 MATCH) ==========
async function submitReportFromPortal() {
  const alertEl = document.getElementById('reportAlert');
  if (alertEl) {
    alertEl.className = 'alert';
    alertEl.style.display = 'none';
  }

  const reportText = document.getElementById('repText').value.trim();
  if (!reportText) {
    if (alertEl) {
      alertEl.textContent = 'Please enter detailed hazard observations before submitting.';
      alertEl.className = 'alert alert-error show';
    }
    return;
  }

  // Ensure authenticated token; auto-acquire worker token if needed
  let token = AuthState.getToken();
  if (!token) {
    try {
      const form = new URLSearchParams();
      form.append('username', 'worker1');
      form.append('password', 'password');
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: form
      });
      if (res.ok) {
        const data = await res.json();
        AuthState.setSession(data.access_token, data.role, 'worker1');
        token = data.access_token;
      }
    } catch (e) { }
  }

  const body = {
    report_type: document.getElementById('repType').value,
    location: document.getElementById('repLocation').value,
    department: document.getElementById('repDept').value,
    report_text: reportText,
  };

  const submitBtn = document.getElementById('submitReportBtn');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Evaluating SIF Precursor Risk...';
  }

  try {
    const res = await fetch(`${API_BASE}/reports`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "Submission failed. Please check credentials.");
    }

    // Render Exact Prediction Result Box from Commit ad25296
    const resultEl = document.getElementById('predictResult');
    resultEl.style.display = 'block';

    const isHigh = data.predicted_label === 1;
    let factors = [];
    try {
      factors = typeof data.top_factors === 'string' ? JSON.parse(data.top_factors || "[]") : (data.top_factors || []);
    } catch (e) {
      factors = [];
    }

    resultEl.innerHTML = `
      <div class="result-box ${isHigh ? 'high-risk' : 'low-risk'}">
        <div class="result-status-title">
          ${isHigh ? '⚠️ SIF PRECURSOR DETECTED' : '✅ Low Risk Observation'}
          <span style="font-size:12px; font-weight:normal; opacity:0.85;">(AI Confidence: ${(data.predicted_probability * 100).toFixed(1)}%)</span>
        </div>
        <div style="font-size:12px; margin-top:6px; color:var(--text-main);">
          <strong>Top Contributing Risk Drivers (SHAP Attribution):</strong>
          <div style="margin-top:4px;">
            ${factors.length ? factors.map(f => `<span class="factor-chip">${f.feature.replace('flag_', '').replace('count_', '').replace('tfidf_', 'word: ')} (${f.impact > 0 ? '+' : ''}${f.impact})</span>`).join('') : '<span style="color:var(--text-muted); font-size:11px;">No high-impact hazard flags triggered</span>'}
          </div>
        </div>
      </div>
    `;

    document.getElementById('repText').value = "";
    hideSuggestions();
    loadReports();

    resultEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (err) {
    if (alertEl) {
      alertEl.textContent = err.message;
      alertEl.className = 'alert alert-error show';
    }
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = '⚡ Analyze & Submit Safety Report';
    }
  }
}

// ========== RESTORED DASHBOARD LOADER (EXACT COMMIT ad25296 MATCH) ==========
async function loadReports() {
  const token = AuthState.getToken();
  const headers = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const tbody = document.getElementById('reportsTableBody');
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/reports`, { headers });
    const data = await res.json();
    if (!res.ok) {
      tbody.innerHTML = `<tr><td colspan="5" class="empty-state">Sign in to view live incident surveillance feed.</td></tr>`;
      return;
    }

    if (!data || data.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="empty-state">No hazard reports filed yet. Submit your first observation above!</td></tr>`;
      return;
    }

    tbody.innerHTML = data.map(r => {
      const isHigh = r.predicted_label === 1;
      let factors = [];
      try {
        factors = (typeof r.top_factors === 'string' ? JSON.parse(r.top_factors || "[]") : (r.top_factors || [])).slice(0, 3);
      } catch (e) {
        factors = [];
      }

      const prob = r.predicted_probability !== null ? (r.predicted_probability * 100).toFixed(1) + '%' : '—';

      return `
        <tr>
          <td><strong>${r.report_type || 'Near Miss'}</strong></td>
          <td>
            <strong>${r.location || '—'}</strong><br>
            <span style="color:var(--text-muted); font-size:11px;">${r.department || '—'}</span>
          </td>
          <td style="max-width:320px; line-height:1.4;">${r.report_text || '—'}</td>
          <td>
            <span class="badge-risk ${isHigh ? 'high' : 'low'}">
              ${isHigh ? '⚠️ SIF RISK' : '✅ LOW RISK'}
            </span>
            <div style="margin-top:4px; font-size:11px; color:var(--text-secondary);">
              ${prob} &bull;
              ${factors.map(f => `<span class="factor-chip">${f.feature.replace('flag_', '').replace('count_', '').replace('tfidf_', '')}</span>`).join('')}
            </div>
          </td>
          <td>${r.submitted_by_username || 'field_worker'}</td>
        </tr>
      `;
    }).join('');
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="5" class="empty-state">Live feed waiting for API connection (${e.message}).</td></tr>`;
  }
}

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initCarousel();
  updateUserLabel();
  loadReports();
});
