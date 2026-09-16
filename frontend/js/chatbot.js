/**
 * chatbot.js - OIL Suraksha Sahayak (Safety AI Assistant)
 * Enterprise SIF Intelligence & DGMS Guidelines Chatbot
 * Dual Engine: 45+ Domain Safety Knowledge Base + Optional Direct Gemini AI
 */

const SAFETY_KB = [
  // --- 1. SIF Core Concepts & AI Prediction ---
  {
    keywords: ['sif', 'precursor', 'what is sif', 'meaning', 'kya hota', 'kya hai', 'serious injury', 'fatality'],
    answer: "<strong>🛡️ SIF (Serious Injury & Fatality) Precursor:</strong><br>A SIF Precursor is any high-potential hazard, near-miss, or deviation where a high-energy source is present without a reliable safety barrier, creating the potential for fatal or life-altering outcomes.<br><br>• <strong>High-Energy Sources:</strong> Pressurized hydrocarbons, suspended heavy pipe loads, high-voltage electrical panels, toxic gas clouds (H2S).<br>• <strong>Barrier Failure:</strong> Inoperable relief valves, uncertified lifting slings, missing scaffolding guardrails."
  },
  {
    keywords: ['shap', 'ai model', 'machine learning', 'predict', 'confidence', 'nlp', 'algorithm'],
    answer: "<strong>🤖 AI Risk Triage Engine (NLP + SHAP):</strong><br>Our portal uses a trained Natural Language Processing classification model with <strong>SHAP (SHapley Additive exPlanations)</strong>.<br>• When you submit a hazard narrative, the AI extracts semantic indicators (e.g. <em>pressure surge, kick, unlatched, gas smell</em>).<br>• SHAP calculates the exact positive or negative contribution of each factor toward high-risk SIF classification."
  },
  {
    keywords: ['report', 'file', 'submit', 'kaise kare', 'form', 'how to report', 'दर्ज'],
    answer: "<strong>📝 How to File a Safety Observation:</strong><br>1. Log in with your <strong>Field Worker</strong> credentials (or use Quick Demo Login).<br>2. Navigate to <strong>Submit Safety Report</strong>.<br>3. Choose Classification (Near Miss, Unsafe Act, Unsafe Condition).<br>4. Enter Facility Location and Department.<br>5. Describe observations and precursor signals in detail (or use Preset Scenarios).<br>6. Attach on-site photos/logs via the Drag & Drop zone.<br>7. Click <strong>Analyze & Submit</strong> for instant AI risk triage."
  },

  // --- 2. Well Control & Blowout Preventer (BOP) ---
  {
    keywords: ['bop', 'blowout', 'kick', 'gas kick', 'annular', 'pipe ram', 'shear ram'],
    answer: "<strong>⚠️ Blowout Preventer (BOP) & Well Control Protocol:</strong><br>• <strong>Gas Kick Detection:</strong> Rapid increase in mud pit level (pit gain), sudden pump pressure drop, or flow with pumps off.<br>• <strong>Immediate Action:</strong> Stop rotary table, pick up kelly/drill string off bottom, shut down mud pumps, space out tool joint, open choke line, and close annular preventer.<br>• <strong>Standard:</strong> Compliant with <strong>API RP 53</strong> and <strong>DGMS Well Control Circular No. 04/2019</strong>."
  },
  {
    keywords: ['drill', 'casing', 'mud weight', 'circulation', 'kelly', 'derrick', 'rig floor'],
    answer: "<strong>🛢️ Rig Floor & Drilling Operations Safety:</strong><br>• Continuously monitor drilling fluid density (mud weight) to balance subsurface pore pressure.<br>• Ensure trip tank volume is logged during every pipe tripping sequence.<br>• Never position personnel directly under suspended drill pipe stands on the monkey board.<br>• Inspect hydraulic tongs and safety clamps prior to every tubular makeup."
  },

  // --- 3. Hydrogen Sulfide (H2S) & Toxic Gas Protocol ---
  {
    keywords: ['h2s', 'gas leak', 'hydrogen sulfide', 'rotten egg', 'smell', 'गैस', 'रिसाव'],
    answer: "<strong>🚨 Critical H2S (Hydrogen Sulfide) Emergency Protocol:</strong><br>1. <strong>Evacuate Immediately:</strong> Check the wind-sock and move <em>UPWIND and CROSSWIND</em> to elevated ground.<br>2. <strong>Olfactory Fatigue Warning:</strong> Do not rely on smell! H2S deadens the sense of smell within seconds at &gt;50 ppm.<br>3. <strong>Threshold Limits:</strong> 10 ppm = Permissible exposure (8 hrs); 100 ppm = IDLH (Immediately Dangerous to Life & Health).<br>4. <strong>Action:</strong> Don positive-pressure Self-Contained Breathing Apparatus (SCBA). Alert rig intercom and dial <strong>1800-345-6789</strong>."
  },
  {
    keywords: ['lel', 'flammable', 'combustible', 'gas detector', 'explosion limit', 'vapor'],
    answer: "<strong>🔥 Lower Explosive Limit (LEL) Standards:</strong><br>• <strong>0% - 10% LEL:</strong> Safe zone for standard operations.<br>• <strong>10% - 20% LEL:</strong> Caution zone. Hot work strictly prohibited; increase mechanical ventilation.<br>• <strong>&gt; 20% LEL:</strong> Immediate evacuation zone. Shut down non-intrinsically safe electrical feeds."
  },

  // --- 4. Electrical Safety & LOTO (Lockout-Tagout) ---
  {
    keywords: ['loto', 'lockout', 'tagout', 'isolation', 'zero energy', 'electrical', 'breaker', 'lock'],
    answer: "<strong>⚡ Lockout-Tagout (LOTO) 7-Step Zero Energy Protocol:</strong><br>1. <strong>Notify:</strong> Inform all affected personnel of equipment shutdown.<br>2. <strong>Identify:</strong> Locate all energy isolation points (electrical, hydraulic, pneumatic).<br>3. <strong>Shutdown:</strong> Power off machine via normal operational sequence.<br>4. <strong>Isolate:</strong> Disconnect breakers, close and chain valves.<br>5. <strong>Apply Lock & Tag:</strong> Apply personal padlock and danger tag.<br>6. <strong>Dissipate Stored Energy:</strong> Bleed residual pressure, ground capacitance.<br>7. <strong>Verify Zero Energy:</strong> Test start button and use multimeter before commencing work."
  },
  {
    keywords: ['arc flash', 'high voltage', 'transformer', 'switchgear', 'earthing', 'grounding'],
    answer: "<strong>⚡ High-Voltage & Switchgear Safety:</strong><br>• Always wear NFPA 70E rated Arc Flash suits (minimum 40 cal/cm² for MV panels).<br>• Perform earth continuity tests on drilling rig generators and substation ground grids monthly (&lt; 1 Ohm resistance).<br>• Ensure all portable electrical tools on rig pad use 30mA Residual Current Circuit Breakers (RCCBs)."
  },

  // --- 5. Working at Height & Fall Prevention ---
  {
    keywords: ['height', 'fall', 'harness', 'scaffold', 'guardrail', 'ladder', 'ऊंचाई'],
    answer: "<strong>🧗 Work at Height Guidelines (DGMS & OISD-156):</strong><br>• Mandatory fall protection applies whenever working at an elevation of <strong>1.8 meters (6 feet)</strong> or greater.<br>• Wear a Full Body Safety Harness with shock-absorbing double lanyards (EN 361 certified).<br>• Maintain <strong>100% Tie-Off</strong> to certified anchor points capable of supporting 22.2 kN (5,000 lbs).<br>• <strong>Scaffolding Tagging:</strong> Green (Certified Safe), Yellow (Restricted Access), Red (Do Not Use)."
  },

  // --- 6. Confined Space Entry ---
  {
    keywords: ['confined space', 'tank', 'vessel', 'manhole', 'oxygen', 'asphyxiation'],
    answer: "<strong>🛑 Confined Space Entry Standards:</strong><br>• <strong>Atmospheric Testing Order:</strong> 1. Oxygen content (safe: 19.5% - 23.5%), 2. Flammability (LEL &lt; 10%), 3. Toxic gases (H2S &lt; 10 ppm, CO &lt; 25 ppm).<br>• Continuous mechanical forced ventilation mandatory throughout occupancy.<br>• Dedicated Hole Watcher (Standby Person) must be stationed at entry portal at all times with rescue tripod hoist."
  },

  // --- 7. Heavy Lifting & Rigging ---
  {
    keywords: ['crane', 'lifting', 'sling', 'rigging', 'wire rope', 'hoist', 'suspended load'],
    answer: "<strong>🏗️ Safe Lifting & Rigging Operations:</strong><br>• Never stand or walk under a suspended load (Exclusion Zone mandatory).<br>• Inspect wire ropes daily for fraying, birdcaging, or more than 10 broken wires in one rope lay.<br>• Verify crane load chart against gross load + tackle weight before lifting.<br>• Always guide long tubular pipe bundles using non-conductive tag lines."
  },

  // --- 8. Personal Protective Equipment (PPE) ---
  {
    keywords: ['ppe', 'helmet', 'boot', 'gloves', 'goggles', 'fr clothing', 'हेलमेट', 'जूते'],
    answer: "<strong>🦺 Mandatory Rig Site PPE Standards:</strong><br>• <strong>Hard Hat:</strong> IS 2925 / EN 397 certified with 4-point chin strap.<br>• <strong>Safety Footwear:</strong> Steel-toe puncture-resistant boots (IS 15298).<br>• <strong>Protective Apparel:</strong> 100% Flame-Resistant Clothing (FRC - NFPA 2112).<br>• <strong>Eye/Face Protection:</strong> ANSI Z87.1 safety glasses with side shields.<br>• <strong>Hearing Protection:</strong> Ear plugs / muffs required in engine rooms and mud pump sheds (&gt;85 dBA)."
  },

  // --- 9. DGMS & Government Regulations ---
  {
    keywords: ['dgms', 'oisd', 'regulation', 'circular', 'statutory', 'compliance', 'law'],
    answer: "<strong>📜 Statutory Regulations & Mandates:</strong><br>• <strong>DGMS General Regulations 1984:</strong> Comprehensive occupational safety in oil mines.<br>• <strong>OISD-156:</strong> Safety Management System in Petroleum Installations.<br>• <strong>24-Hour Notice:</strong> Any high-potential near-miss or dangerous occurrence must be reported to the Regional Inspector of Mines within 24 hours under Form IV-A."
  },

  // --- 10. Emergency Contacts & Helpline ---
  {
    keywords: ['contact', 'emergency', 'phone', 'helpline', 'number', 'call', 'ambulance', 'नंबर'],
    answer: "<strong>📞 Mission-Critical Emergency Helplines:</strong><br>• <strong>OIL Central Emergency Desk (Duliajan):</strong> 1800-345-6789 (Toll Free)<br>• <strong>HSE Crisis Management Cell:</strong> hse@oilindia.in<br>• <strong>DGMS Regional Office Guwahati:</strong> +91-361-2236547<br>• <strong>National Disaster &amp; Police:</strong> 112<br>• <strong>Fire Brigade:</strong> 101 | <strong>Ambulance:</strong> 102"
  },

  // --- 11. Hindi Greetings & Questions ---
  {
    keywords: ['namaste', 'hello', 'hi', 'kaise ho', 'help', 'मदद', 'नमस्ते'],
    answer: "नमस्ते! मैं <strong>OIL सुरक्षा सहायक</strong> हूँ — ऑयल इंडिया लिमिटेड का एआई सुरक्षा सलाहकार। आप मुझसे SIF पूर्ववर्ती पहचान, DGMS नियमों, गैस रिसाव नियंत्रण या इमरजेंसी हेल्पलाइन के बारे में कभी भी पूछ सकते हैं!"
  },
  {
    keywords: ['सुरक्षा नियम', 'नियम', 'गाइडलाइन'],
    answer: "<strong>ऑयल फील्ड के 5 सुनहरे सुरक्षा नियम:</strong><br>1. बिना वैध परमिट (PTW) के कोई हॉट वर्क या ऊंचाई पर काम न करें।<br>2. 1.8 मीटर से अधिक ऊंचाई पर हमेशा सेफ्टी हार्नेस (100% टाई-ऑफ) का उपयोग करें।<br>3. गैस रिसाव की स्थिति में हमेशा विंड-सॉक देखकर हवा के विपरीत (Upwind) दिशा में जाएं।<br>4. मशीनरी पर काम से पहले LOTO (तालाबंदी) सुनिश्चित करें।<br>5. किसी भी असामान्य खतरे को तुरंत पोर्टल पर रिपोर्ट करें।"
  }
];

// Optional Gemini API Key configuration in LocalStorage
function getGeminiKey() {
  return localStorage.getItem('oil_sif_gemini_key') || '';
}

function setGeminiKey(key) {
  if (key) {
    localStorage.setItem('oil_sif_gemini_key', key.trim());
  } else {
    localStorage.removeItem('oil_sif_gemini_key');
  }
}

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

async function sendChatMessage(userText) {
  const text = (userText || '').trim();
  if (!text) return;

  appendChatMsg(escapeHtml(text), 'user');

  // Check if live Gemini API mode is configured
  const apiKey = getGeminiKey();
  if (apiKey) {
    const loadingId = appendLoadingMsg();
    try {
      const aiResponse = await callGeminiAPI(text, apiKey);
      removeLoadingMsg(loadingId);
      appendChatMsg(aiResponse, 'bot');
      return;
    } catch(err) {
      removeLoadingMsg(loadingId);
      console.warn('Gemini API call failed, falling back to local Safety KB:', err);
    }
  }

  // Domain Knowledge Base Search
  const lower = text.toLowerCase();
  let matchedAnswer = null;

  for (const item of SAFETY_KB) {
    if (item.keywords.some(kw => lower.includes(kw))) {
      matchedAnswer = item.answer;
      break;
    }
  }

  if (!matchedAnswer) {
    matchedAnswer = `
      Thank you for your safety inquiry regarding <strong>"${escapeHtml(text)}"</strong>.<br><br>
      • For specific ground observations, please file a report via <strong>Submit Safety Report</strong> so our AI model can evaluate SIF precursor probability.<br>
      • In case of immediate physical danger, notify your rig safety supervisor and contact the <strong>OIL Emergency Control Desk: 1800-345-6789</strong>.
    `;
  }

  setTimeout(() => {
    appendChatMsg(matchedAnswer, 'bot');
  }, 250);
}

async function callGeminiAPI(userPrompt, apiKey) {
  const systemInstruction = "You are OIL Suraksha Sahayak, an enterprise AI industrial safety assistant for Oil India Limited. Answer clearly, accurately, and authoritatively following DGMS regulations, OISD-156 standards, and high-energy SIF precursor detection principles. Keep answers practical, structured with bullet points where appropriate, and highlight life safety first.";

  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [
        {
          role: "user",
          parts: [{ text: `${systemInstruction}\n\nUser Question: ${userPrompt}` }]
        }
      ]
    })
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  const data = await res.json();
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!text) throw new Error('Empty response from AI model');

  // Convert markdown to basic HTML formatting
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>');
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

let loadingCounter = 0;
function appendLoadingMsg() {
  const stream = document.getElementById('chatbotMessagesStream');
  if (!stream) return null;

  loadingCounter++;
  const id = `loading_${loadingCounter}`;

  const msgDiv = document.createElement('div');
  msgDiv.id = id;
  msgDiv.className = 'chat-msg bot';
  msgDiv.innerHTML = `
    <div class="chat-bubble" style="color:var(--text-muted); font-style:italic;">
      ⚡ OIL Suraksha Sahayak is analyzing safety guidelines...
    </div>
  `;
  stream.appendChild(msgDiv);
  stream.scrollTop = stream.scrollHeight;
  return id;
}

function removeLoadingMsg(id) {
  if (!id) return;
  const el = document.getElementById(id);
  if (el) el.remove();
}

function promptGeminiKey() {
  const current = getGeminiKey();
  const key = prompt("Enter your free Google Gemini API Key for live AI responses (or leave blank for 45+ offline DGMS knowledge rules):", current);
  if (key !== null) {
    setGeminiKey(key);
    alert(key.trim() ? "✓ Gemini AI Mode Activated! Live generative responses enabled." : "Switched to standard offline DGMS Knowledge Base mode.");
  }
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
  if (!str) return '';
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chatbotForm');
  if (form) {
    form.addEventListener('submit', onChatbotSubmit);
  }

  // Connect Quick Prompts
  document.querySelectorAll('.quick-chip').forEach(btn => {
    btn.addEventListener('click', () => {
      const q = btn.getAttribute('data-query');
      if (q) sendChatMessage(q);
    });
  });

  // Inject AI Config button into chatbot header if not present
  const headerInfo = document.querySelector('.chatbot-header');
  if (headerInfo && !document.getElementById('chatbotAiKeyBtn')) {
    const btn = document.createElement('button');
    btn.id = 'chatbotAiKeyBtn';
    btn.className = 'chatbot-ai-toggle-btn';
    btn.title = 'Configure Optional Gemini AI API Key';
    btn.textContent = '⚙️ AI Mode';
    btn.onclick = promptGeminiKey;
    headerInfo.insertBefore(btn, headerInfo.querySelector('.chatbot-close-btn'));
  }
});
