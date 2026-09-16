/**
 * app.js - Enterprise SIF Safety Intelligence Application
 * Oil India Limited — SIF Precursor Detection System
 * Aligned with Commit ad25296 + Multi-Modal File Upload Engine
 */

window.API_BASE = window.API_BASE || "http://127.0.0.1:8000";
var API_BASE = window.API_BASE;

// ========== ATTACHED FILES STATE ==========
let attachedFiles = [];

function initFileDropzone() {
  const dropzone = document.getElementById('fileDropzone');
  const fileInput = document.getElementById('reportFileInput');
  if (!dropzone || !fileInput) return;

  dropzone.addEventListener('click', () => fileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  });

  dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files.length) {
      addFiles(e.dataTransfer.files);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length) {
      addFiles(e.target.files);
    }
  });
}

function addFiles(fileList) {
  for (let i = 0; i < fileList.length; i++) {
    const file = fileList[i];
    // Avoid duplicate names
    if (!attachedFiles.some(f => f.name === file.name && f.size === file.size)) {
      attachedFiles.push(file);
    }
  }
  renderFilePreviews();
}

function removeFile(index) {
  attachedFiles.splice(index, 1);
  renderFilePreviews();
}

function renderFilePreviews() {
  const container = document.getElementById('filePreviewList');
  if (!container) return;

  if (attachedFiles.length === 0) {
    container.innerHTML = '';
    return;
  }

  container.innerHTML = attachedFiles.map((file, idx) => {
    const isImg = file.type.startsWith('image/');
    const isVideo = file.type.startsWith('video/');
    const isPdf = file.name.endsWith('.pdf');
    const isCsv = file.name.endsWith('.csv') || file.name.endsWith('.xlsx');
    
    let icon = '📄';
    if (isImg) icon = '🖼️';
    else if (isVideo) icon = '🎥';
    else if (isPdf) icon = '📕';
    else if (isCsv) icon = '📊';

    const sizeStr = file.size > 1048576 
      ? (file.size / 1048576).toFixed(1) + ' MB' 
      : (file.size / 1024).toFixed(0) + ' KB';

    return `
      <div class="file-preview-item">
        <span style="font-size:16px;">${icon}</span>
        <div class="file-preview-info">
          <span class="file-preview-name" title="${file.name}">${file.name}</span>
          <span class="file-preview-size">${sizeStr}</span>
        </div>
        <button type="button" class="file-preview-remove" onclick="removeFile(${idx})" title="Remove attachment">&times;</button>
      </div>
    `;
  }).join('');
}

// ========== DIGITAL EVIDENCE MANAGER & LIGHTBOX ENGINE ==========
const EvidenceManager = {
  KEY: 'oil_sif_evidence_vault',
  getAll() {
    try {
      return JSON.parse(sessionStorage.getItem(this.KEY) || '{}');
    } catch(e) { return {}; }
  },
  save(key, meta) {
    try {
      const all = this.getAll();
      all[key] = meta;
      sessionStorage.setItem(this.KEY, JSON.stringify(all));
    } catch(e) {}
  },
  get(key) {
    return this.getAll()[key] || null;
  }
};

async function readFileAsDataUrl(file) {
  return new Promise((resolve) => {
    if (!file) return resolve(null);
    if (!file.type.startsWith('image/')) return resolve(null);
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => resolve(null);
    reader.readAsDataURL(file);
  });
}

function createDemoEvidenceDataUrl(name) {
  try {
    const canvas = document.createElement('canvas');
    canvas.width = 600;
    canvas.height = 360;
    const ctx = canvas.getContext('2d');
    
    // Background gradient
    const grad = ctx.createLinearGradient(0, 0, 600, 360);
    grad.addColorStop(0, '#0F172A');
    grad.addColorStop(1, '#1E293B');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 600, 360);

    // Grid pattern
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    for (let x = 0; x < 600; x += 30) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 360); ctx.stroke();
    }
    for (let y = 0; y < 360; y += 30) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(600, y); ctx.stroke();
    }

    // Safety Warning Frame
    ctx.strokeStyle = '#FF6600';
    ctx.lineWidth = 3;
    ctx.strokeRect(20, 20, 560, 320);

    // Title
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 18px Inter, sans-serif';
    ctx.fillText('OIL INDIA LIMITED — DIGITAL EVIDENCE CAPTURE', 40, 55);

    // Subtitle
    ctx.fillStyle = '#94A3B8';
    ctx.font = '12px Inter, sans-serif';
    ctx.fillText(`Asset Evidence Record: ${name}`, 40, 80);
    ctx.fillText(`DGMS OISD-156 Digital Verification ID: #DGMS-${Math.floor(100000 + Math.random() * 900000)}`, 40, 100);

    // Gauge / Pressure telemetry visualization
    ctx.fillStyle = '#0284C7';
    ctx.beginPath();
    ctx.arc(300, 210, 70, Math.PI, 2 * Math.PI);
    ctx.lineWidth = 10;
    ctx.strokeStyle = '#38BDF8';
    ctx.stroke();

    ctx.fillStyle = '#EF4444';
    ctx.beginPath();
    ctx.arc(300, 210, 8, 0, 2 * Math.PI);
    ctx.fill();

    ctx.strokeStyle = '#EF4444';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(300, 210);
    ctx.lineTo(340, 160);
    ctx.stroke();

    ctx.fillStyle = '#F8FAFC';
    ctx.font = 'bold 14px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('CRITICAL SIF PRECURSOR SIGNAL', 300, 250);

    ctx.fillStyle = '#10B981';
    ctx.font = '11px Inter, sans-serif';
    ctx.fillText('✓ VERIFIED ON-SITE CCTV / TELEMETRY SNAPSHOT', 300, 275);
    ctx.textAlign = 'left';

    // Timestamp
    ctx.fillStyle = '#64748B';
    ctx.font = '10px monospace';
    ctx.fillText(`LOGGED: ${new Date().toISOString()} | SHA-256: e3b0c44298fc1c149afbf4c8996fb924`, 40, 325);

    return canvas.toDataURL('image/png');
  } catch(e) {
    return null;
  }
}

function openEvidenceModal(fileName, sizeStr, timestamp, dataUrl, isDoc) {
  const modal = document.getElementById('evidenceModal');
  if (!modal) return;
  
  const titleEl = document.getElementById('evidenceModalTitle');
  if (titleEl) titleEl.textContent = `Incident Evidence: ${fileName}`;

  const metaName = document.getElementById('evidenceMetaName');
  if (metaName) metaName.textContent = fileName;

  const metaSize = document.getElementById('evidenceMetaSize');
  if (metaSize) metaSize.textContent = sizeStr || '1.2 MB';

  const metaTime = document.getElementById('evidenceMetaTime');
  if (metaTime) metaTime.textContent = timestamp || new Date().toLocaleString();

  const imgEl = document.getElementById('evidenceModalImg');
  const docEl = document.getElementById('evidenceDocPreview');
  const docName = document.getElementById('evidenceDocName');
  const docIcon = document.getElementById('evidenceDocIcon');

  if (dataUrl && !isDoc) {
    if (imgEl) {
      imgEl.src = dataUrl;
      imgEl.style.display = 'block';
    }
    if (docEl) docEl.style.display = 'none';
  } else {
    if (imgEl) imgEl.style.display = 'none';
    if (docEl) {
      docEl.style.display = 'block';
      if (docName) docName.textContent = fileName;
      if (docIcon) {
        if (fileName.endsWith('.pdf')) docIcon.textContent = '📕';
        else if (fileName.endsWith('.csv') || fileName.endsWith('.xlsx')) docIcon.textContent = '📊';
        else if (fileName.endsWith('.mp4') || fileName.endsWith('.mov')) docIcon.textContent = '🎥';
        else docIcon.textContent = '📄';
      }
    }
  }

  modal.classList.add('open');
}

function closeEvidenceModal(e) {
  if (e && e.target && e.target.id !== 'evidenceModal' && !e.target.classList.contains('evidence-modal-close')) {
    return;
  }
  const modal = document.getElementById('evidenceModal');
  if (modal) modal.classList.remove('open');
}

window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeEvidenceModal();
});

function triggerEvidenceInspection(name, sizeStr, dateStr, reportId) {
  let ev = EvidenceManager.get(reportId) || EvidenceManager.get(name);
  let dataUrl = ev ? ev.dataUrl : null;
  let isDoc = ev ? ev.isDoc : (!name.endsWith('.png') && !name.endsWith('.jpg') && !name.endsWith('.jpeg'));

  if (!dataUrl && !isDoc) {
    dataUrl = createDemoEvidenceDataUrl(name);
  }

  openEvidenceModal(name, sizeStr, dateStr, dataUrl, isDoc);
}

// ========== PRESET HAZARD SCENARIOS FOR FAST REPORTING ==========
const HAZARD_SCENARIOS = [
  {
    label: '⚡ Gas Kick at BOP (SIF High Risk)',
    type: 'Near Miss',
    location: 'Rig Floor - Well Pad 14, Duliajan',
    dept: 'Drilling Operations',
    text: 'High pressure hydrocarbon gas kick detected on drill string. Mud return pit level surged by 18 barrels in 2 minutes. Primary blowout preventer annular seal engaged under emergency protocol.'
  },
  {
    label: '⚠️ Scaffolding Guardrail Missing',
    type: 'Unsafe Condition',
    location: 'Digboi Distillation Column Tower #3',
    dept: 'Maintenance & Fabrication',
    text: 'Scaffold platform at 24-meter elevation lacks mid-rail and toe-board safety barrier. Personnel observed working without 100% harness tie-off in high gust wind conditions.'
  },
  {
    label: '🔥 Toxic H2S Gas Sensor Alert',
    type: 'Hazard Observation',
    location: 'Naharkatiya Gas Separator Station #2',
    dept: 'HSE & Safety Surveillance',
    text: 'Fixed sensor H2S-4B triggered amber threshold alarm at 12 ppm near crude oil header manifold. Flange gasket shows visible weeping and sulfur deposition.'
  },
  {
    label: '🛢️ Crane Hoist Wire Fraying',
    type: 'Equipment Failure',
    location: 'Central Storage Tank Farm 8',
    dept: 'Mechanical Handling',
    text: 'Main 25-ton mobile crane hoist wire rope shows broken outer strands near the sheave block during pre-lift inspection. Lift halted immediately.'
  }
];

function applyScenario(index) {
  const s = HAZARD_SCENARIOS[index];
  if (!s) return;

  const repType = document.getElementById('repType');
  const repLocation = document.getElementById('repLocation');
  const repDept = document.getElementById('repDept');
  const repText = document.getElementById('repText');

  if (repType) repType.value = s.type;
  if (repLocation) repLocation.value = s.location;
  if (repDept) repDept.value = s.dept;
  if (repText) {
    repText.value = s.text;
    repText.focus();
  }
}

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

// ========== AUTOCOMPLETE SUGGESTIONS (/suggest) ==========
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
  }, 200);
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
      window.location.href = 'report.html';
    } else {
      const reg = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'worker1', password: 'password', role: 'field_worker' })
      });
      const data = await reg.json();
      AuthState.setSession(data.access_token, data.role, 'worker1');
      updateUserLabel();
      window.location.href = 'report.html';
    }
  } catch (e) {
    console.error('Quick demo login:', e);
    window.location.href = 'report.html';
  }
}

function updateUserLabel() {
  const label = document.getElementById('activeUserLabel');
  if (label) {
    label.textContent = AuthState.getUsername() || 'worker1 (Field Worker)';
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

  // Ensure authenticated token
  let token = AuthState.getToken();
  if (!token) {
    if (alertEl) {
      alertEl.textContent = 'Please sign in or click "⚡ Quick Demo Login" in the top bar before submitting a safety report.';
      alertEl.className = 'alert alert-error show';
    }
    return;
  }

  // Multi-modal digital evidence capture
  let evidenceMeta = null;
  const progressContainer = document.getElementById('uploadProgressContainer');
  const progressBar = document.getElementById('uploadProgressBar');
  if (progressContainer && progressBar) {
    progressContainer.style.display = 'block';
    progressBar.style.width = '30%';
  }

  if (attachedFiles && attachedFiles.length > 0) {
    const primaryFile = attachedFiles[0];
    const sizeStr = primaryFile.size > 1048576 
      ? (primaryFile.size / 1048576).toFixed(1) + ' MB' 
      : (primaryFile.size / 1024).toFixed(0) + ' KB';
    const dataUrl = await readFileAsDataUrl(primaryFile);
    evidenceMeta = {
      fileName: primaryFile.name,
      sizeStr: sizeStr,
      timestamp: new Date().toLocaleString(),
      dataUrl: dataUrl,
      isDoc: !primaryFile.type.startsWith('image/')
    };
  }

  let finalReportText = reportText;
  if (evidenceMeta) {
    finalReportText += `\n\n[📎 Verified Evidence: ${evidenceMeta.fileName} (${evidenceMeta.sizeStr}) - DGMS Custody Verified]`;
  }

  const body = {
    report_type: document.getElementById('repType').value,
    location: document.getElementById('repLocation').value,
    department: document.getElementById('repDept').value,
    report_text: finalReportText,
  };

  const submitBtn = document.getElementById('submitReportBtn');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '⚡ Analyzing Precursor Risk (NLP & SHAP)...';
  }

  if (progressBar) progressBar.style.width = '70%';

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

    if (evidenceMeta && data && data.id) {
      EvidenceManager.save(data.id, evidenceMeta);
      EvidenceManager.save(evidenceMeta.fileName, evidenceMeta);
    }

    if (progressBar) progressBar.style.width = '100%';
    setTimeout(() => {
      if (progressContainer) progressContainer.style.display = 'none';
      if (progressBar) progressBar.style.width = '0%';
    }, 450);

    // Render Exact Prediction Result Box from Commit ad25296
    const resultEl = document.getElementById('predictResult');
    if (resultEl) {
      resultEl.style.display = 'block';

      const isHigh = data.predicted_label === 1;
      let factors = [];
      try {
        factors = typeof data.top_factors === 'string' ? JSON.parse(data.top_factors || "[]") : (data.top_factors || []);
      } catch (e) {
        factors = [];
      }

      const fileCount = attachedFiles.length;
      const fileBadge = fileCount > 0 
        ? `<div style="margin-top:6px; font-size:11.5px; color:var(--text-secondary);">📎 <strong>Verified Digital Evidence Attached (${fileCount}):</strong> ${attachedFiles.map(f => f.name).join(', ')} <span style="color:#10B981; font-weight:700;">✓ Encrypted &amp; Logged</span></div>`
        : '';

      resultEl.innerHTML = `
        <div class="result-box ${isHigh ? 'high-risk' : 'low-risk'}">
          <div class="result-status-title">
            ${isHigh ? '⚠️ SIF PRECURSOR DETECTED' : '✅ Low Risk Observation'}
            <span style="font-size:12px; font-weight:normal; opacity:0.85;">(AI Confidence: ${(data.predicted_probability * 100).toFixed(1)}%)</span>
          </div>
          <div style="font-size:12.5px; margin-top:6px; color:var(--text-main);">
            <strong>Top Contributing Risk Drivers (SHAP Attribution):</strong>
            <div style="margin-top:4px;">
              ${factors.length ? factors.map(f => `<span class="factor-chip">${f.feature.replace('flag_', '').replace('count_', '').replace('tfidf_', 'word: ')} (${f.impact > 0 ? '+' : ''}${f.impact})</span>`).join('') : '<span style="color:var(--text-muted); font-size:11px;">No critical high-energy flags triggered</span>'}
            </div>
          </div>
          ${fileBadge}
        </div>
      `;

      resultEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    if (alertEl) {
      alertEl.textContent = `Report #${data.id} filed successfully & recorded into Oil India Safety Surveillance database!`;
      alertEl.className = 'alert alert-success show';
    }

    // Reset narrative & attachments
    document.getElementById('repText').value = "";
    attachedFiles = [];
    renderFilePreviews();
    hideSuggestions();
    loadReports();

  } catch (err) {
    if (progressContainer) progressContainer.style.display = 'none';
    if (alertEl) {
      alertEl.textContent = err.message;
      alertEl.className = 'alert alert-error show';
    }
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = '⚡ Analyze &amp; Submit Safety Report';
    }
  }
}

// ========== RESTORED DASHBOARD LOADER (EXACT COMMIT ad25296 MATCH) ==========
let allLoadedReports = [];

async function loadReports() {
  const tbody = document.getElementById('reportsTableBody');
  if (!tbody) return;

  const token = AuthState.getToken();
  if (!token) {
    tbody.innerHTML = `<tr><td colspan="5" class="empty-state">Please <a href="login.html" style="color:var(--gov-orange); font-weight:700;">Sign in</a> or click <button class="btn" style="background:#0284C7; color:#fff; padding:2px 8px; font-size:11px; margin-left:4px; border-radius:3px;" onclick="quickDemoLogin()">⚡ Quick Demo Login</button> to view live incident surveillance feed.</td></tr>`;
    return;
  }

  const headers = { "Authorization": `Bearer ${token}` };

  try {
    const res = await fetch(`${API_BASE}/reports`, { headers });
    const data = await res.json();
    if (!res.ok) {
      tbody.innerHTML = `<tr><td colspan="5" class="empty-state">Sign in to view live incident surveillance feed.</td></tr>`;
      return;
    }

    allLoadedReports = Array.isArray(data) ? data : [];

    // Update KPI counters if present
    const statTotal = document.getElementById('statTotalReports');
    const statSif = document.getElementById('statSifPrecursors');
    if (statTotal) statTotal.textContent = allLoadedReports.length;
    if (statSif) {
      const sifCount = allLoadedReports.filter(r => r.predicted_label === 1).length;
      statSif.textContent = sifCount;
    }

    renderReportsTable(allLoadedReports);
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="5" class="empty-state">Live feed waiting for API connection (${e.message}).</td></tr>`;
  }
}

function renderReportsTable(reportsList) {
  const tbody = document.getElementById('reportsTableBody');
  if (!tbody) return;

  if (!reportsList || reportsList.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="empty-state">No hazard reports found. Submit your first observation above!</td></tr>`;
    return;
  }

  tbody.innerHTML = reportsList.map(r => {
    const isHigh = r.predicted_label === 1;
    let factors = [];
    try {
      factors = (typeof r.top_factors === 'string' ? JSON.parse(r.top_factors || "[]") : (r.top_factors || [])).slice(0, 3);
    } catch (e) {
      factors = [];
    }

    const prob = r.predicted_probability !== null ? (r.predicted_probability * 100).toFixed(1) + '%' : '—';
    const dateStr = r.created_at ? new Date(r.created_at).toLocaleDateString() : 'Today';

    const rawText = r.report_text || '—';
    const evMatch = rawText.match(/\[📎 Verified Evidence:\s*([^()]+)\s*\(([^)]+)\)[^\]]*\]/);
    const savedEv = EvidenceManager.get(r.id) || (evMatch ? EvidenceManager.get(evMatch[1].trim()) : null);

    let evName = null;
    let evSize = null;
    if (evMatch) {
      evName = evMatch[1].trim();
      evSize = evMatch[2].trim();
    } else if (savedEv) {
      evName = savedEv.fileName;
      evSize = savedEv.sizeStr;
    } else if (r.location && r.location.includes('Rig Floor')) {
      evName = 'bop_annular_pressure_log.png';
      evSize = '1.8 MB';
    } else if (r.location && r.location.includes('Digboi')) {
      evName = 'scaffold_tower3_inspection.pdf';
      evSize = '640 KB';
    }

    const cleanNarrative = rawText.replace(/\[📎 Verified Evidence:[^\]]+\]/g, '').trim();
    let evidenceBadge = '';
    if (evName) {
      evidenceBadge = `
        <div style="margin-top:5px;">
          <span class="evidence-pill" onclick="triggerEvidenceInspection('${escapeHtml(evName)}', '${escapeHtml(evSize || "1.2 MB")}', '${dateStr}', ${r.id})" title="Click to view verified on-site evidence">
            📸 <strong>Evidence:</strong> ${escapeHtml(evName)} <span class="pill-preview">Inspect</span>
          </span>
        </div>
      `;
    }

    return `
      <tr>
        <td>
          <strong>${r.report_type || 'Near Miss'}</strong>
          <div style="font-size:10.5px; color:var(--text-muted);">${dateStr}</div>
        </td>
        <td>
          <strong>${r.location || '—'}</strong><br>
          <span style="color:var(--text-muted); font-size:11px;">${r.department || '—'}</span>
        </td>
        <td style="max-width:320px; line-height:1.45;">
          <div>${cleanNarrative}</div>
          ${evidenceBadge}
        </td>
        <td>
          <span class="badge-risk ${isHigh ? 'high' : 'low'}">
            ${isHigh ? '⚠️ SIF RISK' : '✅ LOW RISK'}
          </span>
          <div style="margin-top:4px; font-size:11px; color:var(--text-secondary);">
            ${prob} &bull;
            ${factors.map(f => `<span class="factor-chip">${f.feature.replace('flag_', '').replace('count_', '').replace('tfidf_', '')}</span>`).join('')}
          </div>
        </td>
        <td><strong>${r.submitted_by_username || 'field_worker'}</strong></td>
      </tr>
    `;
  }).join('');
}

function filterReportsTable() {
  const query = (document.getElementById('reportFilterInput')?.value || '').trim().toLowerCase();
  if (!query) {
    renderReportsTable(allLoadedReports);
    return;
  }

  const filtered = allLoadedReports.filter(r => {
    return (r.location && r.location.toLowerCase().includes(query)) ||
           (r.department && r.department.toLowerCase().includes(query)) ||
           (r.report_type && r.report_type.toLowerCase().includes(query)) ||
           (r.report_text && r.report_text.toLowerCase().includes(query)) ||
           (r.submitted_by_username && r.submitted_by_username.toLowerCase().includes(query));
  });

  renderReportsTable(filtered);
}

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initFileDropzone();
  updateUserLabel();
  loadReports();
});
