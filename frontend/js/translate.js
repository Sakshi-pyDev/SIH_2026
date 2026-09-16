/**
 * translate.js - 25 Languages Switcher & Google Translate Engine
 * SIF Precursor Detection System — Oil India Limited
 */

const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English (English)' },
  { code: 'hi', name: 'हिन्दी (Hindi)' },
  { code: 'as', name: 'অসমীয়া (Assamese)' },
  { code: 'bn', name: 'বাংলা (Bengali)' },
  { code: 'brx', name: 'बड़ो (Bodo)' },
  { code: 'doi', name: 'डोगरी (Dogri)' },
  { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
  { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
  { code: 'ks', name: 'कॉशुर (Kashmiri)' },
  { code: 'gom', name: 'कोंकणी (Konkani)' },
  { code: 'mai', name: 'मैथिली (Maithili)' },
  { code: 'ml', name: 'മലയാളം (Malayalam)' },
  { code: 'mni', name: 'মৈতৈলোন্ (Manipuri)' },
  { code: 'mr', name: 'मराठी (Marathi)' },
  { code: 'ne', name: 'नेपाली (Nepali)' },
  { code: 'or', name: 'ଓଡ଼ିଆ (Odia)' },
  { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
  { code: 'sa', name: 'संस्कृतम् (Sanskrit)' },
  { code: 'sat', name: 'संथाली (Santali)' },
  { code: 'sd', name: 'سنڌي (Sindhi)' },
  { code: 'ta', name: 'தமிழ் (Tamil)' },
  { code: 'te', name: 'తెలుగు (Telugu)' },
  { code: 'ur', name: 'اُردُو (Urdu)' },
  { code: 'fr', name: 'Français (French)' },
  { code: 'es', name: 'Español (Spanish)' }
];

function initLanguageSelector() {
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

  selectEl.addEventListener('change', (e) => {
    changePortalLanguage(e.target.value);
  });
}

function changePortalLanguage(langCode) {
  localStorage.setItem('oil_sif_lang', langCode);

  // Trigger Google Translate dropdown element if present
  const gtCombo = document.querySelector('.goog-te-combo');
  if (gtCombo) {
    gtCombo.value = langCode;
    gtCombo.dispatchEvent(new Event('change'));
  } else {
    // Set cookie for Google Translate
    document.cookie = `googtrans=/en/${langCode}; path=/; domain=${window.location.hostname}`;
    document.cookie = `googtrans=/en/${langCode}; path=/;`;
    if (langCode === 'en') {
      document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }
    // If not loaded yet, refresh or let engine pick it up
  }
}

// Google Translate Initialization
function googleTranslateElementInit() {
  if (window.google && window.google.translate) {
    new window.google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: SUPPORTED_LANGUAGES.map(l => l.code).join(','),
      autoDisplay: false
    }, 'google_translate_element');

    const saved = localStorage.getItem('oil_sif_lang');
    if (saved && saved !== 'en') {
      setTimeout(() => {
        changePortalLanguage(saved);
      }, 500);
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
  initLanguageSelector();
});
