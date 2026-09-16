/**
 * translate.js - Silent, Bannerless Multi-Language Engine
 * SIF Precursor Detection System — Oil India Limited
 * DGMS & OISD-156 Compliant
 */

// Comprehensive 25-Language Registry
const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English (English)' },
  { code: 'hi', name: 'हिन्दी (Hindi)' },
  { code: 'as', name: 'অসমীয়া (Assamese)' },
  { code: 'bn', name: 'বাংলা (Bengali)' },
  { code: 'mr', name: 'मराठी (Marathi)' },
  { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
  { code: 'ta', name: 'தமிழ் (Tamil)' },
  { code: 'te', name: 'తెలుగు (Telugu)' },
  { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
  { code: 'ml', name: 'മലയാളം (Malayalam)' },
  { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
  { code: 'or', name: 'ଓଡ଼ିଆ (Odia)' },
  { code: 'ur', name: 'اُردُو (Urdu)' },
  { code: 'sa', name: 'संस्कृतम् (Sanskrit)' },
  { code: 'mai', name: 'मैथिली (Maithili)' },
  { code: 'ks', name: 'कॉशुर (Kashmiri)' },
  { code: 'brx', name: 'बड़ो (Bodo)' },
  { code: 'doi', name: 'डोगरी (Dogri)' },
  { code: 'gom', name: 'कोंकणी (Konkani)' },
  { code: 'mni', name: 'মৈতৈলোন্ (Manipuri)' },
  { code: 'ne', name: 'नेपाली (Nepali)' },
  { code: 'sat', name: 'संथाली (Santali)' },
  { code: 'sd', name: 'سنڌي (Sindhi)' },
  { code: 'fr', name: 'Français (French)' },
  { code: 'es', name: 'Español (Spanish)' }
];

// Instant local UI translations for key UI controls for zero-lag smooth switching
const LOCAL_UI_DICTIONARY = {
  'en': {
    navHome: '🏠 Portal Home',
    navReport: '📝 Submit Safety Report',
    navDashboard: '📊 Surveillance Dashboard',
    btnDemo: '⚡ Quick Demo Login',
    btnLogin: '🔐 Login',
    btnRegister: 'Register',
    heroKicker: '🛡️ Ministry of Petroleum & Natural Gas • DGMS & OISD-156 Compliant • SIH 2026',
    heroTitle: 'AI-Powered Serious Injury & Fatality (SIF)',
    heroHighlight: 'Precursor Detection Platform',
    heroDesc: 'A mission-critical safety intelligence system for Oil India Limited frontline operations — analyzing unstructured field hazard observations, near-miss narratives, and SCADA telemetry to proactively detect high-energy SIF precursor events before catastrophic escalations occur.',
    btnSubmit: '📝 Submit Safety Report →',
    btnDashboard: '📊 Open Surveillance Dashboard →',
    btnFieldDemo: '⚡ Quick Field Worker Demo',
    navAdmin: '👑 Admin Console',
    scenarioBop: '⚡ Gas Kick at BOP (High Energy SIF)',
    scenarioScaffold: '⚠️ Scaffolding Guardrail Missing',
    scenarioH2S: '🔥 Toxic H2S Sensor Alert',
    scenarioCrane: '🛢️ Crane Hoist Wire Fraying',
    dropzoneTitle: 'Click or Drag & Drop Incident Evidence Files Here',
    btnSubmitReport: '⚡ Analyze & Submit Safety Report',
    marqueeTitle: 'AFFILIATED MINISTRIES, REGULATORY AUTHORITIES & PETROLEUM PSUs',
    marqueeSub: '| संबद्ध मंत्रालय, नियामक एवं सार्वजनिक उपक्रम',
    marqueeTag: '● 11 INTEGRATED ENTITIES • LIVE ECOSYSTEM'
  },
  'hi': {
    navHome: '🏠 पोर्टल होम',
    navReport: '📝 सुरक्षा रिपोर्ट दर्ज करें',
    navDashboard: '📊 निगरानी डैशबोर्ड',
    navAdmin: '👑 प्रशासनिक कंसोल',
    btnDemo: '⚡ त्वरित डेमो लॉगिन',
    btnLogin: '🔐 लॉगिन करें',
    btnRegister: 'पंजीकरण',
    scenarioBop: '⚡ बीओपी पर गैस किक (उच्च जोखिम SIF)',
    scenarioScaffold: '⚠️ मचान पर गार्डरेल गायब (गंभीर खतरा)',
    scenarioH2S: '🔥 विषैली H2S गैस सेंसर अलर्ट',
    scenarioCrane: '🛢️ क्रेन होइस्ट वायर रोप कटना',
    dropzoneTitle: 'घटना साक्ष्य की तस्वीरें व दस्तावेज यहाँ खींचें या क्लिक करें',
    btnSubmitReport: '⚡ एआई विश्लेषण एवं सुरक्षा रिपोर्ट दर्ज करें',
    heroKicker: '🛡️ पेट्रोलियम एवं प्राकृतिक गैस मंत्रालय • DGMS एवं OISD-156 अनुपालित • SIH 2026',
    heroTitle: 'एआई-संचालित गंभीर चोट एवं घातकता (SIF)',
    heroHighlight: 'पूर्ववर्ती जोखिम पहचान प्रणाली',
    heroDesc: 'ऑयल इंडिया लिमिटेड के अग्रिम सुरक्षा परिचालनों के लिए मिशन-महत्वपूर्ण सुरक्षा विश्लेषण प्रणाली — अप्रत्याशित दुर्घटनाओं और घातक घटनाओं को रोकने के लिए एआई आधारित पूर्ववर्ती पहचान मंच।',
    btnSubmit: '📝 सुरक्षा रिपोर्ट दर्ज करें →',
    btnDashboard: '📊 निगरानी डैशबोर्ड खोलें →',
    btnFieldDemo: '⚡ त्वरित फील्ड वर्कर डेमो',
    marqueeTitle: 'संबद्ध मंत्रालय, नियामक प्राधिकरण एवं पेट्रोलियम सार्वजनिक उपक्रम (PSUs)',
    marqueeSub: '| भारत सरकार के उपक्रम',
    marqueeTag: '● 11 एकीकृत इकाइयाँ • लाइव इकोसिस्टम'
  },
  'as': {
    navHome: '🏠 প’ৰ্টেল গৃহ',
    navReport: '📝 সুৰক্ষা প্ৰতিবেদন দাখিল',
    navDashboard: '📊 নিৰীক্ষণ ডেছব’ৰ্ড',
    btnDemo: '⚡ তাৎক্ষণিক ডেম’ লগইন',
    btnLogin: '🔐 প্ৰৱেশ (লগইন)',
    btnRegister: 'পঞ্জীয়ন',
    heroKicker: '🛡️ পেট্ৰ’লিয়াম আৰু প্ৰাকৃতিক গেছ মন্ত্ৰালয় • DGMS & OISD-156 • SIH 2026',
    heroTitle: 'AI-চালিত গুৰুতৰ আঘাত আৰু প্ৰাণহানি (SIF)',
    heroHighlight: 'পূৰ্বৱৰ্তী বিপদ চিনাক্তকৰণ মঞ্চ',
    heroDesc: 'অইল ইণ্ডিয়া লিমিটেডৰ কৰ্মীসকলৰ সুৰক্ষাৰ বাবে অত্যাধুনিক কৃত্ৰিম বুদ্ধিমত্তা চালিত নিৰীক্ষণ আৰু আগতীয়া সতৰ্কবাণী ব্যৱস্থা।',
    btnSubmit: '📝 সুৰক্ষা প্ৰতিবেদন দাখিল কৰক →',
    btnDashboard: '📊 নিৰীক্ষণ ডেছব’ৰ্ড খোলক →',
    btnFieldDemo: '⚡ ফিল্ড ৱৰ্কাৰ ডেম’',
    marqueeTitle: 'সম্পৰ্কিত মন্ত্ৰালয়, নিয়ন্ত্ৰক কৰ্তৃপক্ষ আৰু পেট্ৰ’লিয়াম পিএছইউসমূহ',
    marqueeSub: '| ভাৰত চৰকাৰৰ উদ্যোগ',
    marqueeTag: '● ১১টা একত্ৰিত প্ৰতিষ্ঠান • লাইভ'
  },
  'bn': {
    navHome: '🏠 পোর্টাল হোম',
    navReport: '📝 সুরক্ষা রিপোর্ট জমা দিন',
    navDashboard: '📊 নজরদারি ড্যাশবোর্ড',
    btnDemo: '⚡ কুইক ডেমো লগইন',
    btnLogin: '🔐 লগইন করুন',
    btnRegister: 'নিবন্ধন',
    heroKicker: '🛡️ পেট্রোলিয়াম ও প্রাকৃতিক গ্যাস মন্ত্রক • DGMS ও OISD-156 • SIH 2026',
    heroTitle: 'এআই-চালিত গুরুতর আঘাত ও প্রাণহানি (SIF)',
    heroHighlight: 'পূর্ববর্তী ঝুঁকি শনাক্তকরণ প্ল্যাটফর্ম',
    heroDesc: 'অয়েল ইন্ডিয়া লিমিটেডের ক্ষেত্র নিরাপত্তা পর্যবেক্ষণের জন্য এআই-চালিত প্রাথমিক ঝুঁকি শনাক্তকরণ বুদ্ধিমত্তা সিস্টেম।',
    btnSubmit: '📝 সুরক্ষা রিপোর্ট জমা দিন →',
    btnDashboard: '📊 ড্যাশবোর্ড খুলুন →',
    btnFieldDemo: '⚡ ফিল্ড ওয়ার্কার ডেমো',
    marqueeTitle: 'সংযুক্ত মন্ত্রক, নিয়ন্ত্রক কর্তৃপক্ষ ও পেট্রোলিয়াম পিএসইউ',
    marqueeSub: '| ভারত সরকার সংস্থা',
    marqueeTag: '● ১১টি সমন্বিত প্রতিষ্ঠান • লাইভ'
  },
  'mr': {
    navHome: '🏠 पोर्टल होम',
    navReport: '📝 सुरक्षा अहवाल सादर करा',
    navDashboard: '📊 देखरेख डॅशबोर्ड',
    btnDemo: '⚡ झटपट डेमो लॉगिन',
    btnLogin: '🔐 लॉगिन करा',
    btnRegister: 'नोंदणी',
    heroKicker: '🛡️ पेट्रोलियम आणि नैसर्गिक वायू मंत्रालय • DGMS आणि OISD-156 • SIH 2026',
    heroTitle: 'एआय-सक्षम गंभीर दुखापत आणि जीवितहानी (SIF)',
    heroHighlight: 'पूर्वसूचक ओळख प्रणाली',
    heroDesc: 'ऑइल इंडिया लिमिटेडसाठी कृत्रिम बुद्धिमत्ता आधारित सुरक्षा विश्लेषण आणि संभाव्य जोखीम निवारण व्यासपीठ.',
    btnSubmit: '📝 सुरक्षा अहवाल सादर करा →',
    btnDashboard: '📊 देखरेख डॅशबोर्ड उघडा →',
    btnFieldDemo: '⚡ फील्ड वर्कर डेमो',
    marqueeTitle: 'संबंधित मंत्रालये, नियामक प्राधिकरणे आणि पेट्रोलियम पीएसयू',
    marqueeSub: '| भारत सरकारचे उपक्रम',
    marqueeTag: '● ११ एकात्मिक संस्था • थेट'
  },
  'gu': {
    navHome: '🏠 પોર્ટલ હોમ',
    navReport: '📝 સુરક્ષા રિપોર્ટ સબમિટ કરો',
    navDashboard: '📊 સર્વેલન્સ ડેશબોર્ડ',
    btnDemo: '⚡ ઝડપી ડેમો લૉગિન',
    btnLogin: '🔐 લૉગિન',
    btnRegister: 'નોંધણી',
    heroKicker: '🛡️ પેટ્રોલિયમ અને કુદરતી ગેસ મંત્રાલય • DGMS & OISD-156 • SIH 2026',
    heroTitle: 'AI-સંચાલિત ગંભીર ઇજા અને મૃત્યુ (SIF)',
    heroHighlight: 'પૂર્વસૂચક જોખમ શોધ સિસ્ટમ',
    heroDesc: 'ઑઇલ ઇન્ડિયા લિમિટેડ માટે અદ્યતન એઆઈ-આધારિત ક્ષેત્ર સુરક્ષા વિશ્લેષણ અને જોખમ ચેતવણી પ્લેટફોર્મ.',
    btnSubmit: '📝 સુરક્ષા રિપોર્ટ મોકલો →',
    btnDashboard: '📊 ડેશબોર્ડ ખોલો →',
    btnFieldDemo: '⚡ ફીલ્ડ વર્કર ડેમો',
    marqueeTitle: 'સંબંધિત મંત્રાલયો, નિયમનકારી સત્તામંડળો અને પેટ્રોલીયમ PSUs',
    marqueeSub: '| ભારત સરકાર',
    marqueeTag: '● ૧૧ સંકલિત એકમો • લાઈવ'
  },
  'ta': {
    navHome: '🏠 முகப்பு',
    navReport: '📝 பாதுகாப்பு அறிக்கை சமர்ப்பிக்கவும்',
    navDashboard: '📊 கண்காணிப்பு டாஷ்போர்டு',
    btnDemo: '⚡ விரைவு டெமோ உள்நுழைவு',
    btnLogin: '🔐 உள்நுழைக',
    btnRegister: 'பதிவு செய்க',
    heroKicker: '🛡️ பெட்ரோலியம் மற்றும் இயற்கை எரிவாயு அமைச்சகம் • DGMS & OISD-156 • SIH 2026',
    heroTitle: 'AI-இயங்கும் கடுமையான காயம் மற்றும் இறப்பு (SIF)',
    heroHighlight: 'முன்னறிவிப்பு கண்டறிதல் தளம்',
    heroDesc: 'ஆயில் இந்தியா லிமிடெட் களப் பணிகளுக்கான செயற்கை நுண்ணறிவு பாதுகாப்பு கண்காணிப்பு தளம்.',
    btnSubmit: '📝 அறிக்கை சமர்ப்பிக்கவும் →',
    btnDashboard: '📊 டாஷ்போர்டைத் திறக்கவும் →',
    btnFieldDemo: '⚡ களப்பணியாளர் டெமோ',
    marqueeTitle: 'இணைந்த அமைச்சகங்கள், ஒழுங்குமுறை அதிகாரங்கள் மற்றும் பொதுத்துறை நிறுவனங்கள்',
    marqueeSub: '| இந்திய அரசு',
    marqueeTag: '● 11 ஒருங்கிணைந்த நிறுவனங்கள் • நேரலை'
  },
  'te': {
    navHome: '🏠 పోర్టల్ హోమ్',
    navReport: '📝 భద్రతా నివేదికను సమర్పించండి',
    navDashboard: '📊 పర్యవేక్షణ డాష్‌బోర్డ్',
    btnDemo: '⚡ శీఘ్ర డెమో లాగిన్',
    btnLogin: '🔐 లాగిన్',
    btnRegister: 'రిజిస్టర్',
    heroKicker: '🛡️ పెట్రోలియం మరియు సహజ వాయువు మంత్రిత్వ శాఖ • DGMS & OISD-156 • SIH 2026',
    heroTitle: 'AI-ఆధారిత తీవ్రమైన గాయం మరియు మరణం (SIF)',
    heroHighlight: 'ముందస్తు ప్రమాద గుర్తింపు ప్లాట్‌ఫారమ్',
    heroDesc: 'ఆయిల్ ఇండియా లిమిటెడ్ కార్యకలాపాల కోసం అధునాతన కృత్రిమ మేధస్సు భద్రతా విశ్లేషణ వేదిక.',
    btnSubmit: '📝 నివేదికను సమర్పించండి →',
    btnDashboard: '📊 డాష్‌బోర్డ్ తెరవండి →',
    btnFieldDemo: '⚡ ఫీల్డ్ వర్కర్ డెమో',
    marqueeTitle: 'అనుబంధ మంత్రిత్వ శాఖలు, నియంత్రణ సంస్థలు మరియు పెట్రోలియం పీఎస్‌యూలు',
    marqueeSub: '| భారత ప్రభుత్వం',
    marqueeTag: '● 11 సమగ్ర సంస్థలు • లైవ్'
  }
};

/**
 * Suppress all Google Translate banners and iframe artifacts permanently
 */
function suppressGoogleTranslateBanner() {
  // 1. Inject override styles directly into head
  let styleEl = document.getElementById('suppress-gt-style');
  if (!styleEl) {
    styleEl = document.createElement('style');
    styleEl.id = 'suppress-gt-style';
    styleEl.textContent = `
      .goog-te-banner-frame.skiptranslate,
      .goog-te-banner-frame,
      iframe.goog-te-banner-frame,
      .goog-te-banner,
      #goog-gt-tt,
      .goog-te-balloon-frame,
      .goog-tooltip,
      .goog-tooltip:hover,
      .goog-text-highlight,
      .goog-te-spinner-pos,
      .VIpgJd-ZVi9od-ORHb-OEVmcd,
      .VIpgJd-ZVi9od-aZ2wEe-wOHMyf,
      .VIpgJd-ZVi9od-l4eHX-hSRGPd {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0px !important;
        width: 0px !important;
        border: none !important;
        pointer-events: none !important;
        z-index: -9999 !important;
      }
      body {
        top: 0px !important;
        position: static !important;
      }
      body.landing-page-body {
        top: 0px !important;
        position: relative !important;
      }
      font {
        background-color: transparent !important;
        box-shadow: none !important;
      }
      #google_translate_element {
        display: none !important;
      }
    `;
    document.head.appendChild(styleEl);
  }

  // 2. Clear any inline top style on body whenever Google Translate tries to push page down
  const resetBodyTop = () => {
    if (document.body && document.body.style.top && document.body.style.top !== '0px') {
      document.body.style.top = '0px';
    }
    // Remove injected Google Translate top banners
    const frames = document.querySelectorAll('iframe.goog-te-banner-frame, .goog-te-banner-frame, .VIpgJd-ZVi9od-ORHb-OEVmcd');
    frames.forEach(f => {
      f.style.display = 'none';
      f.style.visibility = 'hidden';
      f.style.height = '0px';
    });
  };

  resetBodyTop();
  window.addEventListener('scroll', resetBodyTop, { passive: true });
  setInterval(resetBodyTop, 300);

  // 3. MutationObserver to catch when Google Translate touches body style
  if (window.MutationObserver) {
    const observer = new MutationObserver(() => {
      resetBodyTop();
    });
    observer.observe(document.documentElement, { attributes: true, childList: true, subtree: true, attributeFilter: ['style', 'class'] });
  }
}

/**
 * Apply local instant UI translations if available
 */
function applyInstantTranslations(langCode) {
  const dict = LOCAL_UI_DICTIONARY[langCode] || LOCAL_UI_DICTIONARY['en'];
  if (!dict) return;

  // Nav links
  const navHome = document.querySelector('.gov-nav-links a[href="index.html"]');
  if (navHome && dict.navHome) navHome.innerHTML = dict.navHome;

  const navReport = document.getElementById('navLinkReport') || document.querySelector('.gov-nav-links a[href="report.html"]');
  if (navReport && dict.navReport) navReport.innerHTML = dict.navReport;

  const navDashboard = document.getElementById('navLinkDashboard') || document.querySelector('.gov-nav-links a[href="dashboard.html"]');
  if (navDashboard && dict.navDashboard) navDashboard.innerHTML = dict.navDashboard;

  // Buttons
  const btnLogin = document.querySelector('.btn-nav-login');
  if (btnLogin && dict.btnLogin) btnLogin.innerHTML = dict.btnLogin;

  const btnRegister = document.querySelector('.btn-nav-register');
  if (btnRegister && dict.btnRegister) btnRegister.innerHTML = dict.btnRegister;

  // Hero section elements
  const kicker = document.querySelector('.landing-kicker');
  if (kicker && dict.heroKicker) kicker.innerHTML = dict.heroKicker;

  const heroH1 = document.querySelector('.landing-hero-content h1');
  if (heroH1 && dict.heroTitle) {
    heroH1.innerHTML = `${dict.heroTitle}<br><span class="hero-highlight">${dict.heroHighlight}</span>`;
  }

  const heroDesc = document.querySelector('.landing-hero-content .hero-desc');
  if (heroDesc && dict.heroDesc) heroDesc.textContent = dict.heroDesc;

  const ctaSubmit = document.querySelector('.hero-actions a[href="report.html"]');
  if (ctaSubmit && dict.btnSubmit) ctaSubmit.innerHTML = dict.btnSubmit;

  const ctaDashboard = document.querySelector('.hero-actions a[href="dashboard.html"]');
  if (ctaDashboard && dict.btnDashboard) ctaDashboard.innerHTML = dict.btnDashboard;

  const ctaDemo = document.querySelector('.hero-actions button');
  if (ctaDemo && dict.btnFieldDemo) ctaDemo.innerHTML = dict.btnFieldDemo;

  // Marquee header
  const marqTitle = document.querySelector('.marquee-title-text');
  if (marqTitle && dict.marqueeTitle) marqTitle.textContent = dict.marqueeTitle;

  const marqTag = document.querySelector('.marquee-tag');
  if (marqTag && dict.marqueeTag) marqTag.textContent = dict.marqueeTag;

  // Admin nav link
  const navAdmin = document.getElementById('navLinkAdmin');
  if (navAdmin && dict.navAdmin) navAdmin.innerHTML = dict.navAdmin;

  // Report page dropzone & submit button
  const dropTitle = document.querySelector('.dropzone-title');
  if (dropTitle && dict.dropzoneTitle) dropTitle.textContent = dict.dropzoneTitle;

  const repBtn = document.getElementById('submitReportBtn');
  if (repBtn && dict.btnSubmitReport && !repBtn.disabled) repBtn.innerHTML = dict.btnSubmitReport;

  // Preset Scenario Chips
  const presetChips = document.querySelectorAll('.preset-chip');
  if (presetChips.length >= 4) {
    if (dict.scenarioBop) presetChips[0].innerHTML = dict.scenarioBop;
    if (dict.scenarioScaffold) presetChips[1].innerHTML = dict.scenarioScaffold;
    if (dict.scenarioH2S) presetChips[2].innerHTML = dict.scenarioH2S;
    if (dict.scenarioCrane) presetChips[3].innerHTML = dict.scenarioCrane;
  }
}

/**
 * Initialize Language Dropdown
 */
function initLanguageSelector() {
  suppressGoogleTranslateBanner();

  const selectEl = document.getElementById('oilLanguageSelect');
  if (!selectEl) return;

  selectEl.innerHTML = '';
  SUPPORTED_LANGUAGES.forEach(lang => {
    const opt = document.createElement('option');
    opt.value = lang.code;
    opt.textContent = lang.name;
    selectEl.appendChild(opt);
  });

  const savedLang = localStorage.getItem('oil_sif_lang') || 'en';
  selectEl.value = savedLang;

  // Apply initial local dictionary
  applyInstantTranslations(savedLang);

  selectEl.addEventListener('change', (e) => {
    changePortalLanguage(e.target.value);
  });
}

/**
 * Trigger smooth, bannerless translation
 */
function changePortalLanguage(langCode) {
  localStorage.setItem('oil_sif_lang', langCode);

  // 1. Instant local dictionary UI swap
  applyInstantTranslations(langCode);

  // 2. Set Google Translate Cookie silently
  const host = window.location.hostname;
  if (langCode === 'en') {
    document.cookie = `googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${host}`;
    document.cookie = `googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
  } else {
    document.cookie = `googtrans=/en/${langCode}; path=/; domain=${host}`;
    document.cookie = `googtrans=/en/${langCode}; path=/;`;
  }

  // 3. Trigger Google Translate dropdown element silently if loaded
  const gtCombo = document.querySelector('.goog-te-combo');
  if (gtCombo) {
    gtCombo.value = langCode;
    gtCombo.dispatchEvent(new Event('change'));
  }

  // 4. Immediately suppress any popped banner
  setTimeout(suppressGoogleTranslateBanner, 50);
  setTimeout(suppressGoogleTranslateBanner, 200);
  setTimeout(suppressGoogleTranslateBanner, 600);
}

/**
 * Google Translate Element Init Callback
 */
function googleTranslateElementInit() {
  if (window.google && window.google.translate) {
    new window.google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: SUPPORTED_LANGUAGES.map(l => l.code).join(','),
      autoDisplay: false,
      layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');

    suppressGoogleTranslateBanner();

    const saved = localStorage.getItem('oil_sif_lang');
    if (saved && saved !== 'en') {
      setTimeout(() => {
        changePortalLanguage(saved);
      }, 300);
    }
  }
}

// Load Google Translate script dynamically
(function loadGoogleTranslate() {
  if (document.getElementById('google-translate-script')) return;
  const s = document.createElement('script');
  s.id = 'google-translate-script';
  s.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
  s.async = true;
  document.head.appendChild(s);
})();

document.addEventListener('DOMContentLoaded', () => {
  suppressGoogleTranslateBanner();
  initLanguageSelector();
});
