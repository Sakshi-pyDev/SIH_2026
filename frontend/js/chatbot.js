/**
 * chatbot.js - OIL Suraksha Sahayak (Safety AI Assistant)
 * Interactive Field Safety & DGMS Guidelines Chatbot
 */

const SAFETY_KB = [
  {
    keywords: ['sif', 'precursor', 'what is', 'meaning', 'kya hota', 'kya hai'],
    answer: "<strong>SIF (Serious Injury & Fatality) Precursor</strong> is any high-potential hazard or near-miss event where an energized system, mechanical failure, or unsafe condition lacked a reliable barrier, creating the potential for a catastrophic incident. Examples: hydrocarbon leaks, crane cable fraying, pressure relief valve failure, or work at height without fall arrest."
  },
  {
    keywords: ['report', 'file', 'submit', 'kaise kare', 'form', 'how to report'],
    answer: "To file a safety report:<br>1. Log in with your <strong>Field Worker</strong> credentials.<br>2. Click on <strong>'File Incident Report'</strong> in the top menu.<br>3. Select your Asset location, Department, and Report Type.<br>4. Enter a detailed observation of what you saw.<br>5. Click <strong>'Submit for AI Risk Classification'</strong> to receive immediate SIF risk feedback and SHAP factor analysis."
  },
  {
    keywords: ['gas', 'leak', 'h2s', 'smell', 'rotten', 'hydrogen sulfide'],
    answer: "<strong>⚠️ Immediate Gas/H2S Leak Action:</strong><br>1. Evacuate UPWIND immediately, checking the wind-sock.<br>2. Do NOT operate electrical switches or motor vehicles.<br>3. Sound the evacuation alarm / alert fellow crew.<br>4. Don your Self-Contained Breathing Apparatus (SCBA).<br>5. Contact the OIL Emergency Control Room: <strong>1800-345-6789</strong>."
  },
  {
    keywords: ['dgms', 'oisd', 'compliance', 'regulation', 'rules', 'law'],
    answer: "<strong>Regulatory Standards:</strong><br>• <strong>DGMS</strong> (Directorate General of Mines Safety) General Regulations, 1984.<br>• <strong>OISD-156</strong>: Safety Management System for Petroleum & Natural Gas installations.<br>• <strong>Petroleum Act 1934 & Rules 2002</strong>.<br>All incidents and high-potential near-misses must be formally reported within 24 hours."
  },
  {
    keywords: ['contact', 'emergency', 'phone', 'help', 'number', 'call', 'ambulance'],
    answer: "<strong>📞 Important Emergency Contacts:</strong><br>• <strong>OIL Emergency Control Room:</strong> 1800-345-6789 (Toll Free)<br>• <strong>DGMS Regional Office Guwahati:</strong> +91-361-2236547<br>• <strong>HSE Central Desk:</strong> hse@oilindia.in<br>• <strong>National Emergency:</strong> 112"
  },
  {
    keywords: ['shap', 'ai', 'model', 'machine learning', 'predict', 'confidence'],
    answer: "<strong>AI Risk Engine:</strong> The system uses a trained NLP classification model combined with <strong>SHAP (SHapley Additive exPlanations)</strong>. When a field report is submitted, SHAP calculates the exact impact (positive or negative) that key keywords, hazard flags, and equipment telemetry contributed to the risk score."
  },
  {
    keywords: ['hello', 'hi', 'namaste', 'hey', 'kaise ho', 'help me'],
    answer: "Namaste! I am <strong>OIL Suraksha Sahayak</strong>, your AI safety assistant for Oil India Limited operations. How may I assist you with safety guidelines, reporting, or emergency procedures today?"
  }
];

function toggleChatbot(forceState) {
  const windowEl = document.getElementById('oilChatbotWindow');
  if (!windowEl) return;

  const shouldOpen = forceState !== undefined ? forceState : !windowEl.classList.contains('open');
  if (shouldOpen) {
    windowEl.classList.add('open');
    const input = document.getElementById('chatbotInput');
    if (input) input.focus();
  } else {
    windowEl.classList.remove('open');
  }
}

function sendChatMessage(userText) {
  const text = (userText || '').trim();
  if (!text) return;

  appendChatMsg(text, 'user');

  // Generate bot answer
  const lower = text.toLowerCase();
  let matchedAnswer = null;

  for (const item of SAFETY_KB) {
    if (item.keywords.some(kw => lower.includes(kw))) {
      matchedAnswer = item.answer;
      break;
    }
  }

  if (!matchedAnswer) {
    matchedAnswer = `Thank you for your inquiry regarding <em>"${escapeHtml(text)}"</em>. For specific field questions, please ensure all safety observations are filed via the <strong>File Incident Report</strong> portal, or contact the HSE Department at <strong>hse@oilindia.in</strong>. In case of imminent hazards, alert your safety supervisor immediately.`;
  }

  setTimeout(() => {
    appendChatMsg(matchedAnswer, 'bot');
  }, 350);
}

function appendChatMsg(content, sender) {
  const stream = document.getElementById('chatbotMessagesStream');
  if (!stream) return;

  const msgDiv = document.createElement('div');
  msgDiv.className = `chat-msg ${sender}`;

  const bubble = document.createElement('div');
  bubble.className = 'chat-bubble';
  bubble.innerHTML = content;

  const time = document.createElement('div');
  time.className = 'chat-time';
  time.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  msgDiv.appendChild(bubble);
  msgDiv.appendChild(time);
  stream.appendChild(msgDiv);

  stream.scrollTop = stream.scrollHeight;
}

function onChatbotSubmit(e) {
  if (e) e.preventDefault();
  const input = document.getElementById('chatbotInput');
  if (!input) return;
  const val = input.value;
  input.value = '';
  sendChatMessage(val);
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chatbotForm');
  if (form) {
    form.addEventListener('submit', onChatbotSubmit);
  }

  // Quick prompt buttons
  document.querySelectorAll('.quick-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      const q = btn.getAttribute('data-query');
      if (q) sendChatMessage(q);
    });
  });
});
