html_content = r'''<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SIF Precursor Intelligence — Oil India Limited · SIH 2026</title>
  <link rel="icon" type="image/png" href="assets/oil_safety_logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap"
    rel="stylesheet">

  <style>
    /* =========================================================
       COLOR TOKENS & SYSTEM VARIABLES
       Theme Palette: #3368A0, #66A3BF, #C8DFDB, #F2EFE7
       ========================================================= */
    :root {
      --primary-navy: #3368A0;
      --accent-sky: #66A3BF;
      --soft-mint: #C8DFDB;
      --pearl-bg: #F2EFE7;
      --deep-space: #070D18;
      --card-glass-dark: rgba(11, 23, 44, 0.78);
      --card-glass-light: rgba(255, 255, 255, 0.90);

      --border-glass-dark: rgba(200, 223, 219, 0.22);
      --border-glass-light: rgba(51, 104, 160, 0.25);

      --bg-main: #070D18;
      --text-main: #F2EFE7;
      --text-muted: #C8DFDB;
      --card-bg: var(--card-glass-dark);
      --card-border: var(--border-glass-dark);
      --navbar-bg: rgba(7, 13, 24, 0.75);
      --bottom-bar-bg: rgba(7, 13, 24, 0.90);
      --input-bg: rgba(15, 27, 49, 0.85);
      --input-border: rgba(200, 223, 219, 0.3);
      --shadow-ambient: 0 20px 50px rgba(0, 0, 0, 0.6);
      --glow-accent: rgba(102, 163, 191, 0.45);
    }

    [data-theme="light"] {
      --bg-main: #F2EFE7;
      --text-main: #0c1c33;
      --text-muted: #2f547d;
      --card-bg: var(--card-glass-light);
      --card-border: var(--border-glass-light);
      --navbar-bg: rgba(242, 239, 231, 0.90);
      --bottom-bar-bg: rgba(242, 239, 231, 0.95);
      --input-bg: #ffffff;
      --input-border: rgba(51, 104, 160, 0.35);
      --shadow-ambient: 0 15px 40px rgba(51, 104, 160, 0.15);
      --glow-accent: rgba(51, 104, 160, 0.35);
    }

    /* Base Reset & Lock 100vh / 100vw No Scroll */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    html,
    body {
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-main);
      color: var(--text-main);
      transition: background-color 0.4s ease, color 0.4s ease;
      position: relative;
    }

    /* =========================================================
       FULLSCREEN VIDEO BACKGROUND & SCANLINE HUD
       ========================================================= */
    .viewport-container {
      position: relative;
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      z-index: 10;
    }

    .video-background-layer {
      position: absolute;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      z-index: 1;
      pointer-events: none;
    }

    .hero-video {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      transform: scale(1.02);
      transition: filter 0.5s ease;
    }

    /* Dual Gradient Overlay to maintain Axelrod high contrast */
    .video-overlay-gradient {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at 75% 30%, rgba(7, 13, 24, 0.35) 0%, rgba(7, 13, 24, 0.85) 75%),
        linear-gradient(90deg, rgba(7, 13, 24, 0.92) 0%, rgba(7, 13, 24, 0.65) 45%, rgba(7, 13, 24, 0.82) 100%);
      pointer-events: none;
      transition: background 0.4s ease;
    }

    [data-theme="light"] .video-overlay-gradient {
      background: radial-gradient(circle at 75% 30%, rgba(242, 239, 231, 0.45) 0%, rgba(242, 239, 231, 0.88) 75%),
        linear-gradient(90deg, rgba(242, 239, 231, 0.95) 0%, rgba(242, 239, 231, 0.72) 50%, rgba(242, 239, 231, 0.9) 100%);
    }

    /* Subtle High-Tech Telemetry Scanline */
    .video-scanlines {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.01), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.01));
      background-size: 100% 3px, 6px 100%;
      pointer-events: none;
      opacity: 0.18;
    }

    /* =========================================================
       TOP NAVIGATION BAR (Axelrod Sleek Standard)
       ========================================================= */
    .navbar {
      height: 76px;
      padding: 0 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--navbar-bg);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-bottom: 1px solid var(--card-border);
      position: relative;
      z-index: 50;
      transition: all 0.3s ease;
    }

    .nav-brand-group {
      display: flex;
      align-items: center;
      gap: 16px;
      text-decoration: none;
      color: var(--text-main);
      cursor: pointer;
    }

    .brand-logo-container {
      width: 50px;
      height: 50px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-glass-dark);
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
      transition: transform 0.3s ease, border-color 0.3s ease;
    }

    [data-theme="light"] .brand-logo-container {
      background: #ffffff;
      border: 1px solid var(--border-glass-light);
    }

    .brand-logo-container:hover {
      transform: scale(1.06);
      border-color: var(--accent-sky);
    }

    .brand-logo-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    .brand-meta {
      display: flex;
      flex-direction: column;
    }

    .brand-title {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 17px;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--text-main);
      line-height: 1.15;
    }

    .brand-sub {
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent-sky);
      margin-top: 2px;
    }

    .nav-right-controls {
      display: flex;
      align-items: center;
      gap: 22px;
    }

    .nav-links-menu {
      display: flex;
      align-items: center;
      gap: 26px;
      list-style: none;
    }

    .nav-link-item {
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
      cursor: pointer;
      position: relative;
      transition: color 0.25s ease;
      background: none;
      border: none;
      font-family: inherit;
    }

    .nav-link-item:hover {
      color: var(--text-main);
    }

    .nav-link-item::after {
      content: '';
      position: absolute;
      bottom: -6px;
      left: 0;
      width: 0%;
      height: 2px;
      background: var(--accent-sky);
      transition: width 0.25s ease;
    }

    .nav-link-item:hover::after {
      width: 100%;
    }

    /* Language Switcher Dropdown (Supports ALL 16 Languages) */
    .lang-dropdown-wrapper {
      position: relative;
    }

    .lang-select-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 7px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.04em;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.25s ease;
    }

    [data-theme="light"] .lang-select-btn {
      background: rgba(51, 104, 160, 0.08);
    }

    .lang-select-btn:hover {
      border-color: var(--accent-sky);
      background: rgba(102, 163, 191, 0.15);
    }

    .lang-menu-dropdown {
      position: absolute;
      top: calc(100% + 10px);
      right: 0;
      width: 270px;
      max-height: 380px;
      overflow-y: auto;
      background: var(--card-bg);
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      box-shadow: var(--shadow-ambient);
      padding: 8px 6px;
      display: none;
      flex-direction: column;
      z-index: 100;
      animation: dropdownFade 0.2s ease-out;
    }

    .lang-menu-dropdown.show {
      display: flex;
    }

    .lang-option-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 9px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 500;
      color: var(--text-main);
      cursor: pointer;
      border: none;
      background: transparent;
      text-align: left;
      transition: all 0.2s ease;
      width: 100%;
      font-family: inherit;
    }

    .lang-option-item:hover,
    .lang-option-item.active {
      background: rgba(102, 163, 191, 0.22);
      color: var(--soft-mint);
    }

    .lang-native-label {
      font-weight: 600;
    }

    .lang-code-tag {
      font-size: 10px;
      text-transform: uppercase;
      background: rgba(255, 255, 255, 0.1);
      padding: 2px 6px;
      border-radius: 4px;
      color: var(--accent-sky);
    }

    /* Theme Toggle Button */
    .theme-toggle-btn {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.25s ease;
      font-size: 16px;
      border: none;
    }

    [data-theme="light"] .theme-toggle-btn {
      background: rgba(51, 104, 160, 0.08);
    }

    .theme-toggle-btn:hover {
      border-color: var(--accent-sky);
      transform: rotate(25deg);
    }

    /* Axelrod Portal CTA Button */
    .portal-access-nav-btn {
      background: var(--primary-navy);
      color: #ffffff;
      border: 1px solid var(--accent-sky);
      padding: 9px 20px;
      border-radius: 24px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: inherit;
      box-shadow: 0 4px 20px rgba(51, 104, 160, 0.35);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .portal-access-nav-btn:hover {
      background: var(--accent-sky);
      color: #070D18;
      box-shadow: 0 6px 25px var(--glow-accent);
      transform: translateY(-1px);
    }

    /* =========================================================
       HERO MAIN WORKSPACE (Screen-Fitted Axelrod Layout)
       ========================================================= */
    .hero-center-workspace {
      flex: 1;
      padding: 0 54px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
      z-index: 30;
      min-height: 0;
    }

    /* Left Typography Container (Exact Axelrod Alignment) */
    .hero-typography-column {
      max-width: 680px;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      animation: heroSlideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .telemetry-live-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 20px;
      background: rgba(102, 163, 191, 0.15);
      border: 1px solid rgba(200, 223, 219, 0.25);
      backdrop-filter: blur(10px);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--soft-mint);
      margin-bottom: 22px;
    }

    .pulse-dot-green {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10B981;
      box-shadow: 0 0 10px #10B981;
      animation: pulseGreen 1.8s infinite;
    }

    .hero-headline {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: clamp(40px, 5.0vw, 66px);
      font-weight: 700;
      line-height: 1.05;
      letter-spacing: -0.03em;
      color: var(--text-main);
      margin-bottom: 22px;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    [data-theme="light"] .hero-headline {
      text-shadow: 0 2px 10px rgba(255, 255, 255, 0.4);
    }

    .gradient-accent-text {
      background: linear-gradient(135deg, var(--soft-mint) 0%, var(--accent-sky) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    [data-theme="light"] .gradient-accent-text {
      background: linear-gradient(135deg, var(--primary-navy) 0%, #1a446c 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle-p {
      font-size: 16px;
      font-weight: 400;
      line-height: 1.55;
      color: var(--text-muted);
      max-width: 520px;
      margin-bottom: 32px;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }

    /* Axelrod-Style Links & Interactive CTAs */
    .hero-cta-actions-group {
      display: flex;
      align-items: center;
      gap: 26px;
    }

    .axelrod-text-cta-btn {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-main);
      background: transparent;
      border: none;
      cursor: pointer;
      padding: 8px 0;
      position: relative;
      font-family: inherit;
      transition: all 0.25s ease;
    }

    .axelrod-text-cta-btn::after {
      content: '';
      position: absolute;
      bottom: 2px;
      left: 0;
      width: 100%;
      height: 2px;
      background: var(--text-main);
      transition: background 0.25s ease, transform 0.25s ease;
    }

    .axelrod-text-cta-btn:hover {
      color: var(--accent-sky);
    }

    .axelrod-text-cta-btn:hover::after {
      background: var(--accent-sky);
      transform: scaleX(1.05);
    }

    .cta-arrow-icon {
      font-size: 16px;
      transition: transform 0.25s ease;
    }

    .axelrod-text-cta-btn:hover .cta-arrow-icon {
      transform: translateX(6px);
    }

    .glass-console-btn {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-glass-dark);
      backdrop-filter: blur(15px);
      padding: 10px 22px;
      border-radius: 28px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-main);
      cursor: pointer;
      font-family: inherit;
      transition: all 0.3s ease;
    }

    [data-theme="light"] .glass-console-btn {
      background: rgba(51, 104, 160, 0.1);
      border: 1px solid var(--border-glass-light);
    }

    .glass-console-btn:hover {
      background: var(--primary-navy);
      border-color: var(--accent-sky);
      color: #ffffff;
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(51, 104, 160, 0.4);
    }

    /* =========================================================
       RIGHT FLOATING HUD: ACTIVE ASSET FEEDS & RICH IMAGES
       (Satisfies "I also want so much images in my project")
       ========================================================= */
    .hero-imagery-column {
      display: flex;
      flex-direction: column;
      gap: 12px;
      max-width: 380px;
      animation: heroSlideRight 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .hud-header-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 6px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent-sky);
    }

    .hud-asset-card {
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 10px 14px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-radius: 14px;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      overflow: hidden;
    }

    .hud-asset-card:hover {
      transform: translateX(-6px) scale(1.02);
      border-color: var(--accent-sky);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .hud-card-thumb-container {
      width: 72px;
      height: 52px;
      border-radius: 8px;
      overflow: hidden;
      flex-shrink: 0;
      position: relative;
    }

    .hud-card-thumb {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }

    .hud-asset-card:hover .hud-card-thumb {
      transform: scale(1.15);
    }

    .hud-card-info {
      flex: 1;
      min-width: 0;
    }

    .hud-card-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 3px;
    }

    .hud-card-telemetry {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .hud-status-pill {
      font-size: 9px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 6px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .status-active {
      background: rgba(16, 185, 129, 0.2);
      color: #10B981;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .status-monitor {
      background: rgba(102, 163, 191, 0.2);
      color: var(--soft-mint);
      border: 1px solid rgba(102, 163, 191, 0.4);
    }

    /* Axelrod Bottom-Right Floating Tagline */
    .axelrod-hero-bottom-tagline {
      position: absolute;
      bottom: 24px;
      right: 54px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--soft-mint);
      opacity: 0.85;
      max-width: 480px;
      text-align: right;
      line-height: 1.4;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
      pointer-events: none;
    }

    [data-theme="light"] .axelrod-hero-bottom-tagline {
      color: var(--primary-navy);
      text-shadow: none;
    }

    /* =========================================================
       BOTTOM STATUS BAR (Axelrod Exact Layout)
       ========================================================= */
    .bottom-status-bar {
      height: 52px;
      padding: 0 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bottom-bar-bg);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-top: 1px solid var(--card-border);
      position: relative;
      z-index: 50;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
    }

    .bottom-left-brand {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .bottom-mini-logo {
      width: 24px;
      height: 24px;
      border-radius: 6px;
      object-fit: contain;
    }

    .bottom-center-compliance {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .compliance-tag {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--card-border);
      padding: 2px 8px;
      border-radius: 4px;
      color: var(--soft-mint);
    }

    [data-theme="light"] .compliance-tag {
      background: rgba(51, 104, 160, 0.1);
      color: var(--primary-navy);
    }

    .bottom-right-links {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .bottom-link {
      color: var(--text-muted);
      text-decoration: none;
      cursor: pointer;
      transition: color 0.2s ease;
    }

    .bottom-link:hover {
      color: var(--text-main);
    }

    .live-stream-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #10B981;
    }

    /* =========================================================
       SLIDE-OVER OVERLAY PANEL: AUTH & INCIDENT REPORTING
       (Maintains Screen-Fitted 100vh Landing Page!)
       ========================================================= */
    .slide-over-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 1000;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .slide-over-backdrop.open {
      opacity: 1;
      pointer-events: auto;
    }

    .slide-over-drawer {
      position: absolute;
      top: 0;
      right: 0;
      width: min(520px, 94vw);
      height: 100vh;
      background: var(--bg-main);
      border-left: 1px solid var(--card-border);
      box-shadow: -20px 0 60px rgba(0, 0, 0, 0.6);
      transform: translateX(100%);
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      z-index: 1001;
      overflow: hidden;
    }

    .slide-over-backdrop.open .slide-over-drawer {
      transform: translateX(0%);
    }

    .drawer-header {
      padding: 24px 30px 18px;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(255, 255, 255, 0.02);
    }

    .drawer-brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .drawer-logo-img {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      object-fit: contain;
    }

    .drawer-title-box h3 {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
      font-family: 'Space Grotesk', sans-serif;
    }

    .drawer-title-box p {
      font-size: 11px;
      font-weight: 600;
      color: var(--accent-sky);
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .drawer-close-btn {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 16px;
      transition: all 0.2s ease;
    }

    .drawer-close-btn:hover {
      background: rgba(239, 68, 68, 0.2);
      border-color: #EF4444;
      color: #EF4444;
    }

    .drawer-tabs-nav {
      display: flex;
      padding: 0 30px;
      border-bottom: 1px solid var(--card-border);
      gap: 20px;
    }

    .drawer-tab-btn {
      padding: 14px 0;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
      background: none;
      border: none;
      border-bottom: 2px solid transparent;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.25s ease;
    }

    .drawer-tab-btn.active {
      color: var(--accent-sky);
      border-bottom-color: var(--accent-sky);
    }

    .drawer-body-content {
      flex: 1;
      padding: 26px 30px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    /* Form Styles */
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .form-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-main);
      letter-spacing: 0.04em;
    }

    .input-field,
    .select-field,
    .textarea-field {
      width: 100%;
      padding: 12px 14px;
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      border-radius: 10px;
      color: var(--text-main);
      font-size: 14px;
      font-family: inherit;
      outline: none;
      transition: all 0.25s ease;
    }

    .input-field:focus,
    .select-field:focus,
    .textarea-field:focus {
      border-color: var(--accent-sky);
      box-shadow: 0 0 0 3px rgba(102, 163, 191, 0.25);
    }

    .login-mode-toggle-pills {
      display: flex;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      padding: 3px;
      gap: 4px;
      margin-bottom: 12px;
    }

    .login-pill-opt {
      flex: 1;
      text-align: center;
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      color: var(--text-muted);
      border: none;
      background: transparent;
      font-family: inherit;
      transition: all 0.2s ease;
    }

    .login-pill-opt.active {
      background: var(--primary-navy);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }

    .submit-primary-btn {
      width: 100%;
      padding: 14px;
      background: var(--primary-navy);
      color: #ffffff;
      border: 1px solid var(--accent-sky);
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      cursor: pointer;
      font-family: inherit;
      box-shadow: 0 4px 15px rgba(51, 104, 160, 0.4);
      transition: all 0.3s ease;
      margin-top: 8px;
    }

    .submit-primary-btn:hover {
      background: var(--accent-sky);
      color: #070D18;
    }

    .auth-alert-message {
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      display: none;
    }

    .auth-alert-error {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid #EF4444;
      color: #EF4444;
    }

    .auth-alert-success {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid #10B981;
      color: #10B981;
    }

    /* Live Reports Feed Inside Drawer */
    .report-card-item {
      padding: 14px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .report-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      font-weight: 700;
    }

    .risk-badge-high {
      background: rgba(239, 68, 68, 0.2);
      color: #EF4444;
      border: 1px solid rgba(239, 68, 68, 0.4);
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 10px;
    }

    .risk-badge-low {
      background: rgba(16, 185, 129, 0.2);
      color: #10B981;
      border: 1px solid rgba(16, 185, 129, 0.4);
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 10px;
    }

    /* Lightbox Modal for Facility Inspection */
    .image-modal-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(12px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 40px;
    }

    .image-modal-backdrop.open {
      display: flex;
    }

    .image-modal-card {
      background: var(--bg-main);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      max-width: 900px;
      width: 100%;
      overflow: hidden;
      box-shadow: 0 25px 80px rgba(0, 0, 0, 0.8);
      display: flex;
      flex-direction: column;
    }

    .image-modal-img {
      width: 100%;
      max-height: 520px;
      object-fit: cover;
    }

    .image-modal-content {
      padding: 20px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* Keyframe Animations */
    @keyframes pulseGreen {
      0% {
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
      }

      70% {
        box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
      }

      100% {
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
      }
    }

    @keyframes heroSlideUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }

      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes heroSlideRight {
      from {
        opacity: 0;
        transform: translateX(30px);
      }

      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes dropdownFade {
      from {
        opacity: 0;
        transform: translateY(-8px);
      }

      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* Autocomplete & User Session UI */
    .suggest-box {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: var(--card-bg);
      border: 1px solid var(--accent-sky);
      border-radius: 8px;
      max-height: 180px;
      overflow-y: auto;
      z-index: 100;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(14px);
      margin-top: 4px;
    }

    .suggest-item {
      padding: 9px 12px;
      cursor: pointer;
      border-bottom: 1px solid var(--card-border);
      font-size: 12px;
      color: var(--text-main);
      transition: background 0.15s ease;
    }

    .suggest-item:hover {
      background: rgba(102, 163, 191, 0.25);
    }

    .user-session-bar {
      display: none;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      margin-bottom: 12px;
      border-radius: 8px;
      background: rgba(102, 163, 191, 0.15);
      border: 1px solid rgba(102, 163, 191, 0.35);
      font-size: 11.5px;
    }

    .user-badge-role {
      font-size: 9.5px;
      font-weight: 700;
      letter-spacing: 0.05em;
      padding: 2px 7px;
      border-radius: 12px;
      background: var(--primary-navy);
      color: #fff;
      text-transform: uppercase;
    }

    .btn-logout-mini {
      background: transparent;
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 10.5px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn-logout-mini:hover {
      background: rgba(239, 68, 68, 0.2);
      border-color: #ef4444;
      color: #ef4444;
    }

    /* Responsive adjustments */
    @media (max-width: 1100px) {
      .hero-imagery-column {
        display: none;
      }

      .axelrod-hero-bottom-tagline {
        display: none;
      }
    }
  </style>
</head>

<body data-theme="dark">

  <!-- FULLSCREEN VIEWPORT CONTAINER -->
  <div class="viewport-container">

    <!-- FULLSCREEN VIDEO BACKGROUND LAYER -->
    <div class="video-background-layer">
      <video id="mainHeroVideo" class="hero-video" autoplay muted loop playsinline poster="assets/offshore_oil_rig.jpg">
        <source src="assets/hero_background.mp4" type="video/mp4">
      </video>
      <div class="video-overlay-gradient"></div>
      <div class="video-scanlines"></div>
    </div>

    <!-- TOP NAVIGATION BAR (Axelrod Standard) -->
    <header class="navbar">
      <div class="nav-brand-group" onclick="location.reload()">
        <div class="brand-logo-container">
          <img src="assets/oil_safety_logo.png" alt="Oil India Limited Safety Logo" class="brand-logo-img">
        </div>
        <div class="brand-meta">
          <span class="brand-title" data-i18n="brand_name">OIL INDIA LIMITED</span>
          <span class="brand-sub" data-i18n="brand_sub">SIF PRECURSOR INTELLIGENCE · SIH 2026</span>
        </div>
      </div>

      <div class="nav-right-controls">
        <ul class="nav-links-menu">
          <li><button class="nav-link-item" onclick="openOverlay('login')" data-i18n="nav_about">ABOUT</button></li>
          <li><button class="nav-link-item" onclick="openOverlay('login')" data-i18n="nav_framework">FRAMEWORK</button>
          </li>
          <li><button class="nav-link-item" onclick="openOverlay('report')" data-i18n="nav_dgms">DGMS
              COMPLIANCE</button></li>
        </ul>

        <!-- All Languages Dropdown Selector -->
        <div class="lang-dropdown-wrapper">
          <button class="lang-select-btn" onclick="toggleLanguageMenu(event)">
            <span>🌐</span>
            <span id="currentLangLabel">English (EN)</span>
            <span>▾</span>
          </button>
          <div class="lang-menu-dropdown" id="langMenuDropdown">
            <!-- 16 Comprehensive Languages -->
            <button class="lang-option-item active" onclick="changeAppLanguage('en', 'English (EN)')">
              <span class="lang-native-label">English</span><span class="lang-code-tag">EN</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('hi', 'हिन्दी (HI)')">
              <span class="lang-native-label">हिन्दी</span><span class="lang-code-tag">HI</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('as', 'অসমীয়া (AS)')">
              <span class="lang-native-label">অসমীয়া (Assam)</span><span class="lang-code-tag">AS</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('bn', 'বাংলা (BN)')">
              <span class="lang-native-label">বাংলা</span><span class="lang-code-tag">BN</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('mr', 'मराठी (MR)')">
              <span class="lang-native-label">मराठी</span><span class="lang-code-tag">MR</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('gu', 'ગુજરાતી (GU)')">
              <span class="lang-native-label">ગુજરાતી</span><span class="lang-code-tag">GU</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('ta', 'தமிழ் (TA)')">
              <span class="lang-native-label">தமிழ்</span><span class="lang-code-tag">TA</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('te', 'తెలుగు (TE)')">
              <span class="lang-native-label">తెలుగు</span><span class="lang-code-tag">TE</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('kn', 'ಕನ್ನಡ (KN)')">
              <span class="lang-native-label">ಕನ್ನಡ</span><span class="lang-code-tag">KN</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('ml', 'മലയാളം (ML)')">
              <span class="lang-native-label">മലയാളം</span><span class="lang-code-tag">ML</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('pa', 'ਪੰਜਾਬੀ (PA)')">
              <span class="lang-native-label">ਪੰਜਾਬੀ</span><span class="lang-code-tag">PA</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('or', 'ଓଡ଼ିଆ (OR)')">
              <span class="lang-native-label">ଓଡ଼ିଆ</span><span class="lang-code-tag">OR</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('fr', 'Français (FR)')">
              <span class="lang-native-label">Français</span><span class="lang-code-tag">FR</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('de', 'Deutsch (DE)')">
              <span class="lang-native-label">Deutsch</span><span class="lang-code-tag">DE</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('es', 'Español (ES)')">
              <span class="lang-native-label">Español</span><span class="lang-code-tag">ES</span>
            </button>
            <button class="lang-option-item" onclick="changeAppLanguage('ar', 'العربية (AR)')">
              <span class="lang-native-label">العربية</span><span class="lang-code-tag">AR</span>
            </button>
          </div>
        </div>

        <!-- Theme Toggle (Dark / Light) -->
        <button class="theme-toggle-btn" id="themeToggleBtn" onclick="toggleTheme()" title="Toggle Dark/Light Mode">
          🌙
        </button>

        <!-- Axelrod Portal Access CTA -->
        <button class="portal-access-nav-btn" onclick="openOverlay('login')">
          <span data-i18n="btn_portal">PORTAL ACCESS</span>
          <span>→</span>
        </button>
      </div>
    </header>

    <!-- HERO MAIN WORKSPACE (Screen-Fitted Axelrod Placement) -->
    <main class="hero-center-workspace">

      <!-- Left Column: Massive Headline & Subtitle -->
      <section class="hero-typography-column">
        <div class="telemetry-live-badge">
          <span class="pulse-dot-green"></span>
          <span data-i18n="badge_live">LIVE DGMS TELEMETRY · UPSTREAM ASSET PRECURSOR MONITOR</span>
        </div>

        <h1 class="hero-headline">
          <span data-i18n="hero_title_1">The predictive</span><br>
          <span class="gradient-accent-text" data-i18n="hero_title_2">safety layer for</span><br>
          <span data-i18n="hero_title_3">critical operations</span>
        </h1>

        <p class="hero-subtitle-p" data-i18n="hero_sub">
          AI-powered precursor intelligence detecting micro-anomalies, pipeline stress, and hazardous flare events
          before incidents occur across upstream and downstream energy infrastructure.
        </p>

        <div class="hero-cta-actions-group">
          <!-- Axelrod exact CTA style -->
          <button class="axelrod-text-cta-btn" onclick="openOverlay('login')">
            <span data-i18n="cta_start">SEE WHERE SIF STARTS</span>
            <span class="cta-arrow-icon">→</span>
          </button>

          <!-- Secondary Glass Pill Button -->
          <button class="glass-console-btn" onclick="openOverlay('report')">
            <span>⚡</span>
            <span data-i18n="cta_console">INCIDENT CONSOLE</span>
          </button>
        </div>
      </section>

      <!-- Right Column: Active Asset Feeds & Project Imagery (Rich Images without Scroll!) -->
      <section class="hero-imagery-column">
        <div class="hud-header-bar">
          <span data-i18n="hud_title">MONITORED ASSET FEEDS</span>
          <span>4 ACTIVE STREAMS</span>
        </div>

        <!-- 1. Offshore Rig -->
        <div class="hud-asset-card"
          onclick="openImageModal('assets/offshore_oil_rig.jpg', 'Offshore Deepwater Drilling Platform Alpha', 'Pressure: 3,420 PSI · Flare: Normal · DGMS Safe')">
          <div class="hud-card-thumb-container">
            <img src="assets/offshore_oil_rig.jpg" alt="Offshore Drilling Rig" class="hud-card-thumb">
          </div>
          <div class="hud-card-info">
            <div class="hud-card-title">Offshore Drilling Rig Alpha</div>
            <div class="hud-card-telemetry">
              <span class="hud-status-pill status-active">ONLINE</span>
              <span>Deepwater Wellhead Precursor</span>
            </div>
          </div>
        </div>

        <!-- 2. Duliajan Safety Control Room -->
        <div class="hud-asset-card"
          onclick="openImageModal('assets/safety_control_room.jpg', 'Duliajan Central SCADA & Safety Control Hub', 'Telemetry Grid: 128 Nodes · Precursor Risk: 0.04 (Low)')">
          <div class="hud-card-thumb-container">
            <img src="assets/safety_control_room.jpg" alt="Safety Control Room" class="hud-card-thumb">
          </div>
          <div class="hud-card-info">
            <div class="hud-card-title">Duliajan Control Center</div>
            <div class="hud-card-telemetry">
              <span class="hud-status-pill status-active">SECURE</span>
              <span>SCADA Telemetry & Sensor Mesh</span>
            </div>
          </div>
        </div>

        <!-- 3. Pipeline Telemetry Sensors -->
        <div class="hud-asset-card"
          onclick="openImageModal('assets/pipeline_telemetry_sensors.jpg', 'Assam-Barauni Trunk Pipeline Corridor (4,200 KM)', 'Vibration: Normal · Acoustic Sensors: 100% Operational')">
          <div class="hud-card-thumb-container">
            <img src="assets/pipeline_telemetry_sensors.jpg" alt="Pipeline Telemetry Grid" class="hud-card-thumb">
          </div>
          <div class="hud-card-info">
            <div class="hud-card-title">4,200 KM Pipeline Network</div>
            <div class="hud-card-telemetry">
              <span class="hud-status-pill status-monitor">MONITORING</span>
              <span>Acoustic Wave & Flow Sensors</span>
            </div>
          </div>
        </div>

        <!-- 4. Field Hazard & Safety Inspection -->
        <div class="hud-asset-card"
          onclick="openImageModal('assets/field_safety_inspection.jpg', 'Hazard Inspection & PPE Compliance Protocol', 'AI Vision Check: 99.2% Helmet/Vest Compliance · Zero Violations')">
          <div class="hud-card-thumb-container">
            <img src="assets/field_safety_inspection.jpg" alt="Field Safety Inspection" class="hud-card-thumb">
          </div>
          <div class="hud-card-info">
            <div class="hud-card-title">Field Inspection Unit 04</div>
            <div class="hud-card-telemetry">
              <span class="hud-status-pill status-active">INSPECTION</span>
              <span>DGMS Safety Audit & PPE Vision</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Axelrod Bottom-Right Floating Tagline -->
      <div class="axelrod-hero-bottom-tagline" data-i18n="hero_partner">
        POWERING DULIAJAN REFINERY, NUMALIGARH &amp; 4,200+ KM CRITICAL PIPELINE CORRIDORS
      </div>

    </main>

    <!-- BOTTOM STATUS BAR (Axelrod Exact Layout) -->
    <footer class="bottom-status-bar">
      <div class="bottom-left-brand">
        <img src="assets/oil_safety_logo.png" alt="Oil India Logo" class="bottom-mini-logo">
        <span data-i18n="footer_brand">OIL INDIA LIMITED · SIF INTELLIGENCE LABS</span>
      </div>

      <div class="bottom-center-compliance">
        <span class="compliance-tag" data-i18n="footer_compliance">DGMS &amp; OISD-156 COMPLIANT</span>
        <span>SIH 2026 INNOVATION TRACK</span>
      </div>

      <div class="bottom-right-links">
        <span class="live-stream-badge">
          <span class="pulse-dot-green"></span>
          <span>TELEMETRY: 24MS</span>
        </span>
        <span class="bottom-link" onclick="openOverlay('login')" data-i18n="footer_terms">TERMS</span>
        <span class="bottom-link" onclick="openOverlay('login')" data-i18n="footer_privacy">PRIVACY</span>
      </div>
    </footer>

  </div>

  <!-- SLIDE-OVER OVERLAY DRAWER: AUTH & INCIDENT REPORTING -->
  <div class="slide-over-backdrop" id="slideOverBackdrop" onclick="handleBackdropClick(event)">
    <div class="slide-over-drawer" id="slideOverDrawer">

      <!-- Drawer Header -->
      <div class="drawer-header">
        <div class="drawer-brand">
          <img src="assets/oil_safety_logo.png" alt="Safety Logo" class="drawer-logo-img">
          <div class="drawer-title-box">
            <h3 data-i18n="drawer_title">SIF Operations Console</h3>
            <p data-i18n="drawer_sub">Oil India Limited Safety Intelligence</p>
          </div>
        </div>
        <button class="drawer-close-btn" onclick="closeOverlay()" title="Close Panel">✕</button>
      </div>

      <!-- Active User Session Bar -->
      <div id="userSessionBar" class="user-session-bar">
        <div style="display:flex; align-items:center; gap:6px;">
          <span>👤</span>
          <strong id="userbarUsername" style="color:var(--text-main);"></strong>
          <span id="userbarRole" class="user-badge-role"></span>
        </div>
        <button onclick="logout()" class="btn-logout-mini">Sign Out</button>
      </div>

      <!-- Drawer Tabs -->
      <div class="drawer-tabs-nav">
        <button class="drawer-tab-btn active" id="tabBtnLogin" onclick="switchDrawerTab('login')"
          data-i18n="tab_login">LOGIN</button>
        <button class="drawer-tab-btn" id="tabBtnRegister" onclick="switchDrawerTab('register')"
          data-i18n="tab_register">CREATE ACCOUNT</button>
        <button class="drawer-tab-btn" id="tabBtnReport" onclick="switchDrawerTab('report')"
          data-i18n="tab_report">REPORT INCIDENT</button>
      </div>

      <!-- Drawer Body Content -->
      <div class="drawer-body-content">

        <!-- Tab 1: LOGIN -->
        <div id="sectionLogin">
          <div class="login-mode-toggle-pills">
            <button class="login-pill-opt active" id="pillLoginUsername"
              onclick="setLoginMethod('username')">Username</button>
            <button class="login-pill-opt" id="pillLoginPhone" onclick="setLoginMethod('phone')">Phone Number</button>
          </div>

          <div id="loginAlert" class="auth-alert-message"></div>

          <form id="loginForm" onsubmit="handleLoginSubmit(event)">
            <div class="form-group" id="groupLoginUsername">
              <label class="form-label" data-i18n="label_username">Username</label>
              <input type="text" id="loginUsernameInput" class="input-field" placeholder="e.g. duliajan_officer"
                required>
            </div>

            <div class="form-group" id="groupLoginPhone" style="display: none;">
              <label class="form-label" data-i18n="label_phone">Mobile Phone Number</label>
              <input type="tel" id="loginPhoneInput" class="input-field" placeholder="+91 98765 43210">
            </div>

            <div class="form-group" style="margin-top: 14px;">
              <label class="form-label" data-i18n="label_password">Password</label>
              <input type="password" id="loginPasswordInput" class="input-field" placeholder="••••••••" required>
            </div>

            <button type="submit" class="submit-primary-btn" data-i18n="btn_login_submit">Sign In to Safety
              Portal</button>
          </form>
        </div>

        <!-- Tab 2: CREATE ACCOUNT (Includes Phone Number) -->
        <div id="sectionRegister" style="display: none;">
          <div id="registerAlert" class="auth-alert-message"></div>

          <form id="registerForm" onsubmit="handleRegisterSubmit(event)">
            <div class="form-group">
              <label class="form-label" data-i18n="label_fullname">Full Name</label>
              <input type="text" id="regFullNameInput" class="input-field" placeholder="e.g. Ramesh Chandra Baruah"
                required>
            </div>

            <div class="form-group" style="margin-top: 12px;">
              <label class="form-label" data-i18n="label_phone_required">Phone Number (Required for SMS Safety
                Alerts)</label>
              <input type="tel" id="regPhoneInput" class="input-field" placeholder="+91 98765 43210" required>
            </div>

            <div class="form-group" style="margin-top: 12px;">
              <label class="form-label" data-i18n="label_username">Desired Username</label>
              <input type="text" id="regUsernameInput" class="input-field" placeholder="e.g. barooah_sif" required>
            </div>

            <div class="form-group" style="margin-top: 12px;">
              <label class="form-label" data-i18n="label_password">Secure Password</label>
              <input type="password" id="regPasswordInput" class="input-field" placeholder="Minimum 6 characters"
                required>
            </div>

            <div class="form-group" style="margin-top: 12px;">
              <label class="form-label" data-i18n="label_role">Operational Safety Role</label>
              <select id="regRoleSelect" class="select-field" required>
                <option value="field_worker">Field Worker / Drill Crew</option>
                <option value="safety_officer" selected>Safety Officer / DGMS Auditor</option>
                <option value="admin">System Administrator</option>
              </select>
            </div>

            <button type="submit" class="submit-primary-btn" data-i18n="btn_reg_submit">Create Safety Account</button>
          </form>
        </div>

        <!-- Tab 3: REPORT INCIDENT & AI PREDICTION -->
        <div id="sectionReport" style="display: none;">
          <div id="reportAlert" class="auth-alert-message"></div>

          <div id="unauthReportBanner"
            style="display: none; padding: 12px; border-radius: 8px; background: rgba(102, 163, 191, 0.15); border: 1px solid var(--accent-sky); font-size: 12px; margin-bottom: 14px;">
            ⚠️ <strong>Please sign in</strong> above to submit verified DGMS precursor incident reports.
          </div>

          <div id="roleRestrictionNotice"
            style="display: none; padding: 12px; border-radius: 8px; background: rgba(51, 104, 160, 0.2); border: 1px solid var(--primary-navy); font-size: 12px; margin-bottom: 14px;">
            🛡️ <strong>Safety Oversight Mode:</strong> You are logged in with <span id="roleNoticeBadge"
              class="user-badge-role"></span> privileges. Officers and Administrators oversee live risk telemetry.
            Ground observation filing is restricted to Field Workers.
          </div>

          <form id="incidentForm" onsubmit="handleReportSubmit(event)">
            <div class="form-group">
              <label class="form-label" data-i18n="label_asset_loc">Asset / Facility Location</label>
              <select id="reportLocationSelect" class="select-field" required>
                <option value="Duliajan Refinery Complex">Duliajan Refinery Complex (Assam)</option>
                <option value="Offshore Platform Alpha">Offshore Platform Alpha (Bay of Bengal)</option>
                <option value="Assam-Barauni Pipeline Sector 4">Assam-Barauni Pipeline Sector 4</option>
                <option value="Numaligarh Terminal">Numaligarh Terminal & Pump Station</option>
              </select>
            </div>

            <div class="form-group" style="margin-top: 12px;">
              <label class="form-label" data-i18n="label_department">Department</label>
              <select id="reportDeptSelect" class="select-field" required>
                <option value="Refining">Refining & Catalytic Cracking</option>
                <option value="Drilling">Drilling & Well Servicing</option>
                <option value="Pipeline Logistics">Pipeline Logistics & SCADA</option>
                <option value="Maintenance">Mechanical & Electrical Maintenance</option>
              </select>
            </div>

            <div class="form-group" style="margin-top: 12px;">
              <label class="form-label" data-i18n="label_report_type">Incident / Observation Type</label>
              <select id="reportTypeSelect" class="select-field" required>
                <option value="Near Miss">Near Miss (Precursor Indicator)</option>
                <option value="Hazard Observation">Hazard Observation / Unsafe Condition</option>
                <option value="Equipment Failure">Equipment Failure / Pressure Surge</option>
                <option value="Leakage">Gas / Hydrocarbon Micro-Leakage</option>
              </select>
            </div>

            <div class="form-group" style="margin-top: 12px;">
              <label class="form-label" data-i18n="label_hazard_text">Detailed Observation & Precursor Signals</label>
              <div style="position: relative;">
                <textarea id="reportTextInput" class="textarea-field" rows="3"
                  placeholder="Describe abnormal vibration, gas scent, micro-leak, valve stiffness, or safety barrier degradation..."
                  required oninput="onReportTextInput()"></textarea>
                <div id="suggestBox" class="suggest-box" style="display: none;"></div>
              </div>
            </div>

            <button type="submit" class="submit-primary-btn" data-i18n="btn_submit_report">Submit to AI Precursor
              Classifier</button>
          </form>

          <!-- Live AI Prediction Output Display -->
          <div id="predictionResultCard"
            style="display: none; margin-top: 18px; padding: 14px; border-radius: 10px; background: rgba(255, 255, 255, 0.05); border: 1px solid var(--card-border);">
            <h4 style="font-size: 13px; font-weight: 700; margin-bottom: 8px; color: var(--accent-sky);">AI Precursor
              Risk Assessment</h4>
            <div id="predRiskStatus" style="font-size: 14px; font-weight: 700; margin-bottom: 6px;"></div>
            <div id="predProbMeter" style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;"></div>
            <div id="predShapFactors" style="font-size: 11px; line-height: 1.4;"></div>
          </div>

          <!-- Recent Incident Feed -->
          <div style="margin-top: 24px;">
            <h4 id="recentReportsTitle"
              style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent-sky); margin-bottom: 10px;"
              data-i18n="title_recent_reports">Recent Monitored Reports</h4>
            <div id="recentReportsList" style="display: flex; flex-direction: column; gap: 10px;">
              <div style="font-size: 12px; color: var(--text-muted);">Loading live incident telemetry...</div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- LIGHTBOX MODAL FOR ASSET IMAGES -->
  <div class="image-modal-backdrop" id="imageModal" onclick="closeImageModal(event)">
    <div class="image-modal-card" onclick="event.stopPropagation()">
      <img id="modalImgTag" src="" alt="Facility Inspection Preview" class="image-modal-img">
      <div class="image-modal-content">
        <div>
          <h3 id="modalTitle" style="font-size: 17px; font-weight: 700; color: var(--text-main); margin-bottom: 4px;">
          </h3>
          <p id="modalDesc" style="font-size: 13px; color: var(--accent-sky);"></p>
        </div>
        <button class="submit-primary-btn" style="width: auto; padding: 10px 20px;"
          onclick="closeImageModal()">Dismiss</button>
      </div>
    </div>
  </div>

  <!-- =========================================================
       JAVASCRIPT LOGIC: I18N, AUTH, PREDICTIONS & THEME
       ========================================================= -->
  <script>
    // State management
    let currentAuthToken = localStorage.getItem('sif_auth_token') || null;
    let currentUserRole = localStorage.getItem('sif_user_role') || null;
    let currentLoginMethod = 'username';

    // Comprehensive 16-Language Dictionary
    const I18N = {
      en: {
        brand_name: "OIL INDIA LIMITED",
        brand_sub: "SIF PRECURSOR INTELLIGENCE · SIH 2026",
        nav_about: "ABOUT",
        nav_framework: "FRAMEWORK",
        nav_dgms: "DGMS COMPLIANCE",
        btn_portal: "PORTAL ACCESS",
        badge_live: "LIVE DGMS TELEMETRY · UPSTREAM ASSET PRECURSOR MONITOR",
        hero_title_1: "The predictive",
        hero_title_2: "safety layer for",
        hero_title_3: "critical operations",
        hero_sub: "AI-powered precursor intelligence detecting micro-anomalies, pipeline stress, and hazardous flare events before incidents occur across upstream and downstream energy infrastructure.",
        cta_start: "SEE WHERE SIF STARTS",
        cta_console: "INCIDENT CONSOLE",
        hud_title: "MONITORED ASSET FEEDS",
        hero_partner: "POWERING DULIAJAN REFINERY, NUMALIGARH & 4,200+ KM CRITICAL PIPELINE CORRIDORS",
        footer_brand: "OIL INDIA LIMITED · SIF INTELLIGENCE LABS",
        footer_compliance: "DGMS & OISD-156 COMPLIANT",
        footer_terms: "TERMS",
        footer_privacy: "PRIVACY",
        drawer_title: "SIF Operations Console",
        drawer_sub: "Oil India Limited Safety Intelligence",
        tab_login: "LOGIN",
        tab_register: "CREATE ACCOUNT",
        tab_report: "REPORT INCIDENT",
        label_username: "Username",
        label_phone: "Mobile Phone Number",
        label_phone_required: "Phone Number (Required for SMS Safety Alerts)",
        label_password: "Password",
        label_fullname: "Full Name",
        label_role: "Operational Safety Role",
        label_asset_loc: "Asset / Facility Location",
        label_department: "Department",
        label_report_type: "Incident / Observation Type",
        label_hazard_text: "Detailed Observation & Precursor Signals",
        btn_login_submit: "Sign In to Safety Portal",
        btn_reg_submit: "Create Safety Account",
        btn_submit_report: "Submit to AI Precursor Classifier",
        title_recent_reports: "Recent Monitored Reports"
      },
      hi: {
        brand_name: "ऑयल इंडिया लिमिटेड",
        brand_sub: "SIF अग्रदूत जोखिम आसूचना · SIH 2026",
        nav_about: "परिचय",
        nav_framework: "फ्रेमवर्क",
        nav_dgms: "DGMS अनुपालन",
        btn_portal: "पोर्टल लॉगिन",
        badge_live: "लाइव DGMS टेलीमेट्री · अपस्ट्रीम एसेट प्रीकर्सर मॉनिटर",
        hero_title_1: "सुरक्षा की पूर्व-अनुमानित",
        hero_title_2: "आधुनिक प्रणाली",
        hero_title_3: "ऊर्जा संयंत्रों हेतु",
        hero_sub: "अपस्ट्रीम और डाउनस्ट्रीम ऊर्जा संपत्तियों में दुर्घटनाएं होने से पहले सूक्ष्म विसंगतियों, पाइपलाइन दबाव और हानिकारक घटनाओं का पता लगाने वाली AI तकनीक।",
        cta_start: "SIF की क्षमता देखें",
        cta_console: "घटना लॉग कंसोल",
        hud_title: "निगरानी अधीन संपत्तियां",
        hero_partner: "दुलियाजान रिफाइनरी, नुमालीगढ़ और 4,200+ किमी पाइपलाइन सुरक्षा में कार्यरत",
        footer_brand: "ऑयल इंडिया लिमिटेड · SIF इंटेलिजेंस लैब्स",
        footer_compliance: "DGMS एवं OISD-156 प्रमाणित",
        footer_terms: "नियम",
        footer_privacy: "गोपनीयता",
        drawer_title: "SIF सुरक्षा कंसोल",
        drawer_sub: "ऑयल इंडिया लिमिटेड सुरक्षा आसूचना",
        tab_login: "लॉगिन",
        tab_register: "खाता बनाएं",
        tab_report: "घटना रिपोर्ट करें",
        label_username: "उपयोगकर्ता नाम",
        label_phone: "मोबाइल नंबर",
        label_phone_required: "मोबाइल नंबर (SMS सुरक्षा अलर्ट हेतु अनिवार्य)",
        label_password: "पासवर्ड",
        label_fullname: "पूरा नाम",
        label_role: "सुरक्षा भूमिका",
        label_asset_loc: "संयंत्र / स्थान",
        label_department: "विभाग",
        label_report_type: "घटना का प्रकार",
        label_hazard_text: "विस्तृत विवरण एवं अग्रदूत संकेत",
        btn_login_submit: "सुरक्षा पोर्टल में लॉगिन करें",
        btn_reg_submit: "सुरक्षा खाता बनाएं",
        btn_submit_report: "AI प्रीकर्सर क्लासिफायर को भेजें",
        title_recent_reports: "हालिया रिपोर्टेड घटनाएं"
      },
      as: {
        brand_name: "অইল ইণ্ডিয়া লিমিটেড",
        brand_sub: "SIF পূৰ্বসূচক সুৰক্ষা প্ৰণালী · SIH 2026",
        nav_about: "পৰিচয়",
        nav_framework: "কাঠামো",
        nav_dgms: "DGMS সুৰক্ষা",
        btn_portal: "পৰ্টেল প্ৰৱেশ",
        badge_live: "প্ৰত্যক্ষ DGMS টেলিমেট্ৰি · দুলিয়াজান আৰু পাইপলাইন সুৰক্ষা",
        hero_title_1: "নিৰাপত্তাৰ ভৱিষ্যদ্বাণীমূলক",
        hero_title_2: "সুৰক্ষা স্তৰ",
        hero_title_3: "গুৰুত্বপূৰ্ণ প্ৰকল্পৰ বাবে",
        hero_sub: "দুলিয়াজান শোধনাগাৰ আৰু পাইপলাইনত দুৰ্ঘটনা হোৱাৰ পূৰ্বেই বিপদ চিনাক্ত কৰা AI প্ৰযুক্তি।",
        cta_start: "SIF কিদৰে কাম কৰে চাওক",
        cta_console: "ঘটনা পঞ্জীয়ন",
        hud_title: "নিৰীক্ষণ কৰা ক্ষেত্ৰসমূহ",
        hero_partner: "দুলিয়াজান শোধনাগাৰ, নুমলীগড় আৰু ৪,২০০+ কিমি পাইপলাইন সুৰক্ষিত",
        footer_brand: "অইল ইণ্ডিয়া লিমিটেড · অসম",
        footer_compliance: "DGMS আৰু OISD-156 প্ৰমাণিত",
        footer_terms: "নিয়মাৱলী",
        footer_privacy: "গোপনীয়তা",
        drawer_title: "SIF সুৰক্ষা পৰ্টেল",
        drawer_sub: "অইল ইণ্ডিয়া লিমিটেড সুৰক্ষা ব্যৱস্থা",
        tab_login: "লগইন",
        tab_register: "একাউণ্ট খোলক",
        tab_report: "বিপদ ৰিপৰ্ট কৰক",
        label_username: "ইউজাৰনেম",
        label_phone: "মোবাইল নম্বৰ",
        label_phone_required: "মোবাইল নম্বৰ (SMS এলাৰ্টৰ বাবে)",
        label_password: "পাছৱৰ্ড",
        label_fullname: "সম্পূৰ্ণ নাম",
        label_role: "সুৰক্ষা ভূমিকা",
        label_asset_loc: "প্ৰকল্পৰ স্থান",
        label_department: "বিভাগ",
        label_report_type: "বিপদৰ প্ৰকাৰ",
        label_hazard_text: "পূৰ্বসূচক সংকেতৰ বিৱৰণ",
        btn_login_submit: "সুৰক্ষা পৰ্টেলত লগইন কৰক",
        btn_reg_submit: "একাউণ্ট সৃষ্টি কৰক",
        btn_submit_report: "AI ক ৰিপৰ্ট প্ৰেৰণ কৰক",
        title_recent_reports: "শেহতীয়া সুৰক্ষা ৰিপৰ্ট"
      },
      bn: {
        brand_name: "অয়েল ইন্ডিয়া লিমিটেড",
        brand_sub: "SIF প্রিকর্সর গোয়েন্দা ব্যবস্থা · SIH 2026",
        nav_about: "পরিচিতি",
        nav_framework: "ফ্রেমওয়ার্ক",
        nav_dgms: "ডিজিএমএস সম্মতি",
        btn_portal: "পোর্টাল প্রবেশ",
        badge_live: "লাইভ ডিজিএমএস টেলিমেট্রি · গ্যাস ও তেল পাইপলাইন সুরক্ষা",
        hero_title_1: "পূর্বাভাসমূলক সুরক্ষার",
        hero_title_2: "স্মার্ট প্রযুক্তি",
        hero_title_3: "শিল্প প্রকল্পের জন্য",
        hero_sub: "দুর্ঘটনা ঘটার পূর্বেই ক্ষুদ্র ত্রুটি ও পাইপলাইনের চাপ সনাক্ত করার এআই প্রযুক্তি।",
        cta_start: "এসআইএফ জানুন",
        cta_console: "রিপোর্ট কনসোল",
        hud_title: "পর্যবেক্ষণাধীন কেন্দ্রসমূহ",
        hero_partner: "দুলিয়াজান রিফাইনারি ও ৪২০০+ কিমি পাইপলাইনে সুরক্ষিত",
        footer_brand: "অয়েল ইন্ডিয়া লিমিটেড",
        footer_compliance: "DGMS ও OISD-156 অনুবর্তী",
        footer_terms: "শর্তাবলী",
        footer_privacy: "গোপনীয়তা",
        drawer_title: "এসআইএফ অপারেশনস",
        drawer_sub: "অয়েল ইন্ডিয়া লিমিটেড সুরক্ষা",
        tab_login: "লগইন",
        tab_register: "অ্যাকাউন্ট তৈরি",
        tab_report: "ঘটনা রিপোর্ট",
        label_username: "ইউজারনেম",
        label_phone: "ফোন নম্বর",
        label_phone_required: "ফোন নম্বর (এসএমএস সতর্কতার জন্য)",
        label_password: "পাসওয়ার্ড",
        label_fullname: "পূর্ণ নাম",
        label_role: "দায়িত্ব",
        label_asset_loc: "অবস্থান",
        label_department: "বিভাগ",
        label_report_type: "ঘটনার ধরণ",
        label_hazard_text: "বিবরণ ও সংকেত",
        btn_login_submit: "লগইন করুন",
        btn_reg_submit: "অ্যাকাউন্ট তৈরি করুন",
        btn_submit_report: "রিপোর্ট জমা দিন",
        title_recent_reports: "সাম্প্রতিক রিপোর্ট"
      },
      mr: {
        brand_name: "ऑइल इंडिया लिमिटेड",
        brand_sub: "SIF सुरक्षा पूर्वसूचना प्रणाली · SIH 2026",
        nav_about: "माहिती",
        nav_framework: "प्रणाली",
        nav_dgms: "DGMS सुरक्षा",
        btn_portal: "पोर्टल लॉगिन",
        badge_live: "थेट DGMS टेलिमेट्री · सुरक्षा पूर्वसूचना मॉनिटर",
        hero_title_1: "सुरक्षेचा भाकीत करणारा",
        hero_title_2: "आधुनिक स्तर",
        hero_title_3: "ऊर्जा प्रकल्पांसाठी",
        hero_sub: "अपघातांपूर्वीच मायक्रो-लीक आणि तांत्रिक त्रुटी शोधून काढणारी AI आधारित प्रणाली.",
        cta_start: "SIF ची कार्यपद्धती पहा",
        cta_console: "घटना नोंदणी",
        hud_title: "सुरक्षित प्रकल्प",
        hero_partner: "दुलियाजान रिफायनरी व ४,२००+ किमी पाईपलाईन सुरक्षेत कार्यरत",
        footer_brand: "ऑइल इंडिया लिमिटेड",
        footer_compliance: "DGMS व OISD-156 प्रमाणित",
        footer_terms: "अटी",
        footer_privacy: "गोपनीयता",
        drawer_title: "SIF सुरक्षा कन्सोल",
        drawer_sub: "ऑइल इंडिया लिमिटेड सुरक्षा",
        tab_login: "लॉगिन",
        tab_register: "नोंदणी करा",
        tab_report: "घटना नोंदवा",
        label_username: "वापरकर्ता नाव",
        label_phone: "मोबाईल नंबर",
        label_phone_required: "मोबाईल नंबर (SMS अलर्टसाठी)",
        label_password: "पासवर्ड",
        label_fullname: "पूर्ण नाव",
        label_role: "भूमिका",
        label_asset_loc: "स्थान",
        label_department: "विभाग",
        label_report_type: "घटनेचा प्रकार",
        label_hazard_text: "तपशीलवार निरीक्षण",
        btn_login_submit: "पोर्टलमध्ये प्रवेश करा",
        btn_reg_submit: "खाते तयार करा",
        btn_submit_report: "AI कडे पाठवा",
        title_recent_reports: "अलीकडील अहवाल"
      },
      gu: {
        brand_name: "ઓઇલ ઇન્ડિયા લિમિટેડ",
        brand_sub: "SIF પ્રિકર્સર સલામતી પ્રણાલી · SIH 2026",
        nav_about: "વિશે",
        nav_framework: "ફ્રેમવર્ક",
        nav_dgms: "DGMS સલામતી",
        btn_portal: "પોર્ટલ લોગિન",
        badge_live: "લાઇવ DGMS ટેલિમેટ્રી · પાઇપલાઇન સેફ્ટી",
        hero_title_1: "અગમચેતી સલામતીનું",
        hero_title_2: "આધુનિક સ્તર",
        hero_title_3: "ઊર્જા મથકો માટે",
        hero_sub: "દુર્ઘટનાઓ સર્જાય તે પહેલાં ક્ષતિઓ શોધી કાઢતી AI સુરક્ષા ટેકનોલોજી.",
        cta_start: "SIF કેવી રીતે કાર્ય કરે છે",
        cta_console: "ઇન્સિડન્ટ કન્સોલ",
        hud_title: "મોનિટરિંગ મથકો",
        hero_partner: "દુલિયાજાન રિફાઇનરી અને ૪,૨૦૦+ કિમી પાઇપલાઇન સુરક્ષા",
        footer_brand: "ઓઇલ ઇન્ડિયા લિમિટેડ",
        footer_compliance: "DGMS અને OISD-156 સુસંગત",
        footer_terms: "શરતો",
        footer_privacy: "ગોપનીયતા",
        drawer_title: "SIF ઓપરેશન્સ",
        drawer_sub: "ઓઇલ ઇન્ડિયા લિમિટેડ",
        tab_login: "લોગિન",
        tab_register: "ખાતું બનાવો",
        tab_report: "ઘટના રિપોર્ટ",
        label_username: "યુઝરનેમ",
        label_phone: "મોબાઇલ નંબર",
        label_phone_required: "મોબાઇલ નંબર (SMS એલર્ટ માટે)",
        label_password: "પાસવર્ડ",
        label_fullname: "પૂરું નામ",
        label_role: "ભૂમિકા",
        label_asset_loc: "સ્થાન",
        label_department: "વિભાગ",
        label_report_type: "ઘટનાનો પ્રકાર",
        label_hazard_text: "વિગતવાર વર્ણન",
        btn_login_submit: "લોગિન કરો",
        btn_reg_submit: "નોંધણી કરો",
        btn_submit_report: "AI રિપોર્ટ સબમિટ કરો",
        title_recent_reports: "તાજેતરના રિપોર્ટ્સ"
      },
      ta: {
        brand_name: "ஆயில் இந்தியா லிமிடெட்",
        brand_sub: "SIF பாதுகாப்பு நுண்ணறிவு · SIH 2026",
        nav_about: "பற்றி",
        nav_framework: "கட்டமைப்பு",
        nav_dgms: "DGMS நெறிமுறை",
        btn_portal: "உள்நுழைவு",
        badge_live: "நேரலை DGMS டெலிமெட்ரி · பாதுகாப்பு கண்காணிப்பு",
        hero_title_1: "முன்கணிப்பு",
        hero_title_2: "பாதுகாப்பு அடுக்கு",
        hero_title_3: "முக்கிய செயல்பாடுகளுக்கு",
        hero_sub: "விபத்துக்கள் ஏற்படுவதற்கு முன்னதாகவே முரண்பாடுகளைக் கண்டறியும் AI தொழில்நுட்பம்.",
        cta_start: "SIF தொடங்குமிடம்",
        cta_console: "பாதுகாப்பு மையம்",
        hud_title: "கண்காணிக்கப்படும் தளங்கள்",
        hero_partner: "துலியாஜான் சுத்திகரிப்பு ஆலை மற்றும் 4,200+ கி.மீ குழாய் பாதுகாப்பு",
        footer_brand: "ஆயில் இந்தியா லிமிடெட்",
        footer_compliance: "DGMS மற்றும் OISD-156 சான்றளிக்கப்பட்டது",
        footer_terms: "விதிமுறைகள்",
        footer_privacy: "தனியுரிமை",
        drawer_title: "SIF செயல்பாட்டுக் கன்சோல்",
        drawer_sub: "ஆயில் இந்தியா லிமிடெட் பாதுகாப்பு",
        tab_login: "உள்நுழை",
        tab_register: "பதிவு செய்க",
        tab_report: "நிகழ்வை பதிவு செய்",
        label_username: "பயனர்பெயர்",
        label_phone: "தொலைபேசி எண்",
        label_phone_required: "தொலைபேசி எண் (SMS விழிப்பூட்டலுக்கு)",
        label_password: "கடவுச்சொல்",
        label_fullname: "முழு பெயர்",
        label_role: "பாத்திரம்",
        label_asset_loc: "இடம்",
        label_department: "துறை",
        label_report_type: "நிகழ்வு வகை",
        label_hazard_text: "விவரங்கள் மற்றும் அறிகுறிகள்",
        btn_login_submit: "உள்நுழையவும்",
        btn_reg_submit: "கணக்கை உருவாக்கவும்",
        btn_submit_report: "AI சமர்ப்பிக்கவும்",
        title_recent_reports: "சமீபத்திய அறிக்கைகள்"
      },
      te: {
        brand_name: "ఆయిల్ ఇండియా లిమిటెడ్",
        brand_sub: "SIF ప్రికర్సర్ సేఫ్టీ ఇంటెలిజెన్స్ · SIH 2026",
        nav_about: "గురించి",
        nav_framework: "ఫ్రేమ్‌వర్క్",
        nav_dgms: "DGMS నిబంధనలు",
        btn_portal: "పోర్టల్ లాగిన్",
        badge_live: "లైవ్ DGMS టెలిమెట్రీ · పైప్‌లైన్ భద్రత",
        hero_title_1: "ముందస్తు ప్రమాద నివారణ",
        hero_title_2: "రక్షణ వ్యవస్థ",
        hero_title_3: "కీలక ప్రాజెక్టుల కోసం",
        hero_sub: "ప్రమాదాలు జరగడానికి ముందే సూక్ష్మ లోపాలను గుర్తించే అత్యాధునిక AI సాంకేతికత.",
        cta_start: "SIF ఎలా పనిచేస్తుందో చూడండి",
        cta_console: "ఇన్సిడెంట్ కన్సోల్",
        hud_title: "పర్యవేక్షించబడే కేంద్రాలు",
        hero_partner: "దులియాజన్ రిఫైనరీ మరియు 4,200+ కి.మీ పైప్‌లైన్ భద్రత",
        footer_brand: "ఆయిల్ ఇండియా లిమిటెడ్",
        footer_compliance: "DGMS & OISD-156 ధృవీకరించబడింది",
        footer_terms: "నిబంధనలు",
        footer_privacy: "గోప్యత",
        drawer_title: "SIF ఆపరేషన్స్",
        drawer_sub: "ఆయిల్ ఇండియా లిమిటెడ్",
        tab_login: "లాగిన్",
        tab_register: "రిజిస్టర్",
        tab_report: "రిపోర్ట్ చేయండి",
        label_username: "యూజర్‌నేమ్",
        label_phone: "ఫోన్ నంబర్",
        label_phone_required: "ఫోన్ నంబర్ (SMS హెచ్చరికల కోసం)",
        label_password: "పాస్‌వర్డ్",
        label_fullname: "పూర్తి పేరు",
        label_role: "పాత్ర",
        label_asset_loc: "ప్రాంతం",
        label_department: "విభాగం",
        label_report_type: "రిపోర్ట్ రకం",
        label_hazard_text: "వివరాలు",
        btn_login_submit: "లాగిన్ అవ్వండి",
        btn_reg_submit: "ఖాతాను సృష్టించండి",
        btn_submit_report: "AI కి సమర్పించండి",
        title_recent_reports: "ఇటీవలి నివేదికలు"
      },
      kn: {
        brand_name: "ಆಯಿಲ್ ಇಂಡಿಯಾ ಲಿಮಿಟೆಡ್",
        brand_sub: "SIF ಮುನ್ಸೂಚನೆ ಸುರಕ್ಷತಾ ವ್ಯವಸ್ಥೆ · SIH 2026",
        nav_about: "ಬಗ್ಗೆ",
        nav_framework: "ಫ್ರೇಮ್ವರ್ಕ್",
        nav_dgms: "DGMS ಸುರಕ್ಷತೆ",
        btn_portal: "ಪೋರ್ಟಲ್ ಲಾಗಿನ್",
        badge_live: "ಲೈವ್ DGMS ಟೆಲಿಮೆಟ್ರಿ · ಅಪ್‌ಸ್ಟ್ರೀಮ್ ಮಾನಿಟರ್",
        hero_title_1: "ಮುನ್ಸೂಚಕ",
        hero_title_2: "ಸುರಕ್ಷತಾ ಪದರ",
        hero_title_3: "ತೈಲ ಕಾರ್ಯಾಚರಣೆಗಳಿಗೆ",
        hero_sub: "ಅಪಘಾತಗಳು ಸಂಭವಿಸುವ ಮುನ್ನವೇ ಅಪಾಯಗಳನ್ನು ಪತ್ತೆಹಚ್ಚುವ ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ತಂತ್ರಜ್ಞಾನ.",
        cta_start: "SIF ಪ್ರಾರಂಭವಾಗುವುದನ್ನು ನೋಡಿ",
        cta_console: "ಘಟನೆ ಕನ್ಸೋಲ್",
        hud_title: "ಮೇಲ್ವಿಚಾರಣಾ ತಾಣಗಳು",
        hero_partner: "ದುಲಿಯಾಜನ್ ಮತ್ತು 4,200+ ಕಿಮೀ ಪೈಪ್‌ಲೈನ್‌ಗಳ ಸುರಕ್ಷತೆ",
        footer_brand: "ಆಯಿಲ್ ಇಂಡಿಯಾ ಲಿಮಿಟೆಡ್",
        footer_compliance: "DGMS ಮತ್ತು OISD-156 ಅನುಸರಣೆ",
        footer_terms: "ನಿಯಮಗಳು",
        footer_privacy: "ಗೌಪ್ಯತೆ",
        drawer_title: "SIF ಕಾರ್ಯಾಚರಣೆಗಳು",
        drawer_sub: "ಆಯಿಲ್ ಇಂಡಿಯಾ ಲಿಮಿಟೆಡ್",
        tab_login: "ಲಾಗಿನ್",
        tab_register: "ಖಾತೆ ರಚಿಸಿ",
        tab_report: "ವರದಿ ಮಾಡಿ",
        label_username: "ಬಳಕೆದಾರ ಹೆಸರು",
        label_phone: "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
        label_phone_required: "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ (SMS ಎಚ್ಚರಿಕೆಗಾಗಿ)",
        label_password: "ಪಾಸ್ವರ್ಡ್",
        label_fullname: "ಪೂರ್ಣ ಹೆಸರು",
        label_role: "ಪಾತ್ರ",
        label_asset_loc: "ಸ್ಥಳ",
        label_department: "ವಿಭಾಗ",
        label_report_type: "ವರದಿ ಪ್ರಕಾರ",
        label_hazard_text: "ವಿವರಣೆ",
        btn_login_submit: "ಲಾಗಿನ್ ಆಗಿ",
        btn_reg_submit: "ಖಾತೆ ತೆರೆಯಿರಿ",
        btn_submit_report: "AI ಗೆ ಸಲ್ಲಿಸಿ",
        title_recent_reports: "ಇತ್ತೀಚಿನ ವರದಿಗಳು"
      },
      ml: {
        brand_name: "ഓയിൽ ഇന്ത്യ ലിമിറ്റഡ്",
        brand_sub: "SIF പ്രീക്വർസർ സുരക്ഷാ ഇന്റലിജൻസ് · SIH 2026",
        nav_about: "വിവരങ്ങൾ",
        nav_framework: "ചട്ടക്കൂട്",
        nav_dgms: "DGMS പ്രോട്ടോക്കോൾ",
        btn_portal: "പോർട്ടൽ പ്രവേശനം",
        badge_live: "തത്സമയ DGMS ടെലിമെട്രി · സുരക്ഷാ മോണിറ്റർ",
        hero_title_1: "പ്രവചനാത്മക",
        hero_title_2: "സുരക്ഷാ പാളി",
        hero_title_3: "നിർണായക പദ്ധതികൾക്ക്",
        hero_sub: "അപകടങ്ങൾ ഉണ്ടാകുന്നതിന് മുമ്പ് തന്നെ അപകടസൂചനകൾ കണ്ടെത്താനുള്ള നിർമ്മിതബുദ്ധി സംവിധാനം.",
        cta_start: "SIF പരിശോധിക്കുക",
        cta_console: "ഇൻസിഡന്റ് കൺസോൾ",
        hud_title: "നിരീക്ഷണ കേന്ദ്രങ്ങൾ",
        hero_partner: "ദുലിയാജൻ റിഫൈനറിയും 4,200+ കി.മീ പൈപ്പ്‌ലൈനും സംരക്ഷിക്കുന്നു",
        footer_brand: "ഓയിൽ ഇന്ത്യ ലിമിറ്റഡ്",
        footer_compliance: "DGMS & OISD-156 അംഗീകൃതം",
        footer_terms: "നിബന്ധനകൾ",
        footer_privacy: "സ്വകാര്യത",
        drawer_title: "SIF ഓപ്പറേഷൻസ്",
        drawer_sub: "ഓയിൽ ഇന്ത്യ ലിമിറ്റഡ് സുരക്ഷ",
        tab_login: "ലോഗിൻ",
        tab_register: "അക്കൗണ്ട് സൃഷ്ടിക്കുക",
        tab_report: "റിപ്പോർട്ട് ചെയ്യുക",
        label_username: "ഉപയോക്തൃനാമം",
        label_phone: "ഫോൺ നമ്പർ",
        label_phone_required: "ഫോൺ നമ്പർ (SMS മുന്നറിയിപ്പിനായി)",
        label_password: "പാസ്‌വേഡ്",
        label_fullname: "പൂർണ്ണ നാമം",
        label_role: "തസ്തിക",
        label_asset_loc: "സ്ഥലം",
        label_department: "വകുപ്പ്",
        label_report_type: "റിപ്പോർട്ട് തരം",
        label_hazard_text: "വിശദാംശങ്ങൾ",
        btn_login_submit: "ലോഗിൻ ചെയ്യുക",
        btn_reg_submit: "അക്കൗണ്ട് നിർമ്മിക്കുക",
        btn_submit_report: "AI ന് അയക്കുക",
        title_recent_reports: "സമീപകാല റിപ്പോർട്ടുകൾ"
      },
      pa: {
        brand_name: "ਆਇਲ ਇੰਡੀਆ ਲਿਮਿਟੇਡ",
        brand_sub: "SIF ਸੁਰੱਖਿਆ ਖੁਫੀਆ ਪ੍ਰਣਾਲੀ · SIH 2026",
        nav_about: "ਜਾਣਕਾਰੀ",
        nav_framework: "ਢਾਂਚਾ",
        nav_dgms: "DGMS ਸੁਰੱਖਿਆ",
        btn_portal: "ਪੋਰਟਲ ਲਾਗਇਨ",
        badge_live: "ਲਾਈਵ DGMS ਟੈਲੀਮੈਟਰੀ · ਪਾਈਪਲਾਈਨ ਸੁਰੱਖਿਆ",
        hero_title_1: "ਸੁਰੱਖਿਆ ਦੀ ਭਵਿੱਖਬਾਣੀ",
        hero_title_2: "ਕਰਨ ਵਾਲੀ ਪ੍ਰਣਾਲੀ",
        hero_title_3: "ਮਹੱਤਵਪੂਰਨ ਕਾਰਜਾਂ ਲਈ",
        hero_sub: "ਹਾਦਸਿਆਂ ਤੋਂ ਪਹਿਲਾਂ ਹੀ ਖਤਰਿਆਂ ਦੀ ਪਛਾਣ ਕਰਨ ਵਾਲੀ AI ਤਕਨੀਕ।",
        cta_start: "SIF ਨੂੰ ਦੇਖੋ",
        cta_console: "ਇੰਸੀਡੈਂਟ ਕੰਸੋਲ",
        hud_title: "ਨਿਗਰਾਨੀ ਅਧੀਨ ਖੇਤਰ",
        hero_partner: "ਦੁਲਿਆਜਾਨ ਰਿਫਾਇਨਰੀ ਅਤੇ 4,200+ ਕਿਮੀ ਪਾਈਪਲਾਈਨ ਸੁਰੱਖਿਅਤ",
        footer_brand: "ਆਇਲ ਇੰਡੀਆ ਲਿਮਿਟੇਡ",
        footer_compliance: "DGMS ਅਤੇ OISD-156 ਪ੍ਰਮਾਣਿਤ",
        footer_terms: "ਨਿਯਮ",
        footer_privacy: "ਗੋਪਨੀਯਤਾ",
        drawer_title: "SIF ਓਪਰੇਸ਼ਨਜ਼",
        drawer_sub: "ਆਇਲ ਇੰਡੀਆ ਲਿਮਿਟੇਡ",
        tab_login: "ਲਾਗਇਨ",
        tab_register: "ਰਜਿਸਟਰ ਕਰੋ",
        tab_report: "ਰਿਪੋਰਟ ਦਰਜ ਕਰੋ",
        label_username: "ਯੂਜ਼ਰਨੇਮ",
        label_phone: "ਮੋਬਾਈਲ ਨੰਬਰ",
        label_phone_required: "ਮੋਬਾਈਲ ਨੰਬਰ (SMS ਅਲਰਟ ਲਈ)",
        label_password: "ਪਾਸਵਰਡ",
        label_fullname: "ਪੂਰਾ ਨਾਮ",
        label_role: "ਭੂਮਿਕਾ",
        label_asset_loc: "ਸਥਾਨ",
        label_department: "ਵਿਭਾਗ",
        label_report_type: "ਰਿਪੋਰਟ ਦੀ ਕਿਸਮ",
        label_hazard_text: "ਵੇਰਵਾ",
        btn_login_submit: "ਲਾਗਇਨ ਕਰੋ",
        btn_reg_submit: "ਖਾਤਾ ਬਣਾਓ",
        btn_submit_report: "AI ਨੂੰ ਭੇਜੋ",
        title_recent_reports: "ਹਾਲੀਆ ਰਿਪੋਰਟਾਂ"
      },
      or: {
        brand_name: "ଅଏଲ୍ ଇଣ୍ଡିଆ ଲିମିଟେଡ୍",
        brand_sub: "SIF ପୂର୍ବସୂଚକ ସୁରକ୍ଷା ବ୍ୟବସ୍ଥା · SIH 2026",
        nav_about: "ବିବରଣୀ",
        nav_framework: "ଢାଞ୍ଚା",
        nav_dgms: "DGMS ନିୟମାବଳୀ",
        btn_portal: "ପୋର୍ଟାଲ୍ ଲଗଇନ୍",
        badge_live: "ଲାଇଭ୍ DGMS ଟେଲିମେଟ୍ରି · ପାଇପଲାଇନ୍ ସୁରକ୍ଷା",
        hero_title_1: "ଭବିଷ୍ୟବାଣୀମୂଳକ",
        hero_title_2: "ସୁରକ୍ଷା ସ୍ତର",
        hero_title_3: "ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ପ୍ରକଳ୍ପ ପାଇଁ",
        hero_sub: "ଦୁର୍ଘଟଣା ଘଟିବା ପୂର୍ବରୁ ବିପଦ ଚିହ୍ନଟ କରୁଥିବା AI ପ୍ରଯୁକ୍ତିବିଦ୍ୟା।",
        cta_start: "SIF କିପରି କାମ କରେ ଦେଖନ୍ତୁ",
        cta_console: "ରିପୋର୍ଟ କନସୋଲ୍",
        hud_title: "ନିରୀକ୍ଷଣ କେନ୍ଦ୍ର",
        hero_partner: "ଦୁଲିଆଜାନ୍ ରିଫାଇନାରୀ ଏବଂ ୪,୨୦୦+ କିମି ପାଇପଲାଇନ୍ ସୁରକ୍ଷିତ",
        footer_brand: "ଅଏଲ୍ ଇଣ୍ଡିଆ ଲିମିଟେଡ୍",
        footer_compliance: "DGMS ଓ OISD-156 ଅନୁମୋଦିତ",
        footer_terms: "ନିୟମ",
        footer_privacy: "ଗୋପନୀୟତା",
        drawer_title: "SIF ଅପରେସନ୍ସ",
        drawer_sub: "ଅଏଲ୍ ଇଣ୍ଡିଆ ଲିମିଟେଡ୍",
        tab_login: "ଲଗଇନ୍",
        tab_register: "ଖାତା ଖୋଲନ୍ତୁ",
        tab_report: "ରିପୋର୍ଟ କରନ୍ତୁ",
        label_username: "ୟୁଜରନେମ୍",
        label_phone: "ମୋବାଇଲ୍ ନମ୍ବର",
        label_phone_required: "ମୋବାଇଲ୍ ନମ୍ବର (SMS ସତର୍କତା ପାଇଁ)",
        label_password: "ପାସୱାର୍ଡ",
        label_fullname: "ପୂରା ନାମ",
        label_role: "ଦାୟିତ୍ୱ",
        label_asset_loc: "ସ୍ଥାନ",
        label_department: "ବିଭାଗ",
        label_report_type: "ପ୍ରକାର",
        label_hazard_text: "ବିବରଣୀ",
        btn_login_submit: "ଲଗଇନ୍ କରନ୍ତୁ",
        btn_reg_submit: "ଖାତା ସୃଷ୍ଟି କରନ୍ତୁ",
        btn_submit_report: "AI କୁ ପଠାନ୍ତୁ",
        title_recent_reports: "ସାମ୍ପ୍ରତିକ ରିପୋର୍ଟ"
      },
      fr: {
        brand_name: "OIL INDIA LIMITED",
        brand_sub: "INTELLIGENCE PRÉDICTIVE SIF · SIH 2026",
        nav_about: "À PROPOS",
        nav_framework: "CADRE",
        nav_dgms: "CONFORMITÉ DGMS",
        btn_portal: "ACCÈS PORTAIL",
        badge_live: "TÉLÉMÉTRIE EN DIRECT DGMS · SURVEILLANCE DES ACTIFS",
        hero_title_1: "La couche de",
        hero_title_2: "sécurité prédictive pour",
        hero_title_3: "les opérations critiques",
        hero_sub: "Intelligence artificielle détectant les micro-anomalies et les risques de torchage avant que les incidents ne surviennent.",
        cta_start: "DÉCOUVRIR SIF",
        cta_console: "CONSOLE INCIDENTS",
        hud_title: "FLUX D'ACTIFS SURVEILLÉS",
        hero_partner: "ALIMENTANT LA RAFFINERIE DE DULIAJAN ET 4 200+ KM DE PIPELINES",
        footer_brand: "OIL INDIA LIMITED · LABORATOIRES SIF",
        footer_compliance: "CONFORME DGMS ET OISD-156",
        footer_terms: "CONDITIONS",
        footer_privacy: "CONFIDENTIALITÉ",
        drawer_title: "Console Opérationnelle SIF",
        drawer_sub: "Intelligence de Sécurité Oil India Limited",
        tab_login: "CONNEXION",
        tab_register: "CRÉER UN COMPTE",
        tab_report: "SIGNALER UN INCIDENT",
        label_username: "Nom d'utilisateur",
        label_phone: "Numéro de téléphone",
        label_phone_required: "Numéro de téléphone (Requis pour alertes SMS)",
        label_password: "Mot de passe",
        label_fullname: "Nom complet",
        label_role: "Rôle de sécurité",
        label_asset_loc: "Emplacement de l'actif",
        label_department: "Département",
        label_report_type: "Type d'incident",
        label_hazard_text: "Description détaillée et précurseurs",
        btn_login_submit: "Se connecter au portail",
        btn_reg_submit: "Créer un compte de sécurité",
        btn_submit_report: "Soumettre au classificateur IA",
        title_recent_reports: "Rapports récents surveillés"
      },
      de: {
        brand_name: "OIL INDIA LIMITED",
        brand_sub: "SIF PRÄDIKTIVE SICHERHEIT · SIH 2026",
        nav_about: "ÜBER UNS",
        nav_framework: "FRAMEWORK",
        nav_dgms: "DGMS KONFORMITÄT",
        btn_portal: "PORTAL-ZUGANG",
        badge_live: "LIVE DGMS-TELEMETRIE · ANLAGENÜBERWACHUNG",
        hero_title_1: "Die prädiktive",
        hero_title_2: "Sicherheitsschicht für",
        hero_title_3: "kritische Operationen",
        hero_sub: "KI-gestützte Vorläufererkennung von Druckbelastungen und Lecks, bevor Zwischenfälle auftreten.",
        cta_start: "SIF ENTDECKEN",
        cta_console: "VORFALLS-KONSOLE",
        hud_title: "ÜBERWACHTE ANLAGEN-FEEDS",
        hero_partner: "SCHUTZ FÜR DIE DULIAJAN RAFFINERIE UND 4.200+ KM PIPELINES",
        footer_brand: "OIL INDIA LIMITED · SIF LABS",
        footer_compliance: "DGMS & OISD-156 KONFORM",
        footer_terms: "BEDINGUNGEN",
        footer_privacy: "DATENSCHUTZ",
        drawer_title: "SIF Betriebskonsole",
        drawer_sub: "Oil India Limited Sicherheitsintelligenz",
        tab_login: "ANMELDEN",
        tab_register: "KONTO ERSTELLEN",
        tab_report: "VORFALL MELDEN",
        label_username: "Benutzername",
        label_phone: "Telefonnummer",
        label_phone_required: "Telefonnummer (Erforderlich für SMS-Warnungen)",
        label_password: "Passwort",
        label_fullname: "Vollständiger Name",
        label_role: "Sicherheitsrolle",
        label_asset_loc: "Standort der Anlage",
        label_department: "Abteilung",
        label_report_type: "Vorfallstyp",
        label_hazard_text: "Detaillierte Beobachtung & Signale",
        btn_login_submit: "Im Portal anmelden",
        btn_reg_submit: "Sicherheitskonto erstellen",
        btn_submit_report: "An KI-Klassifikator senden",
        title_recent_reports: "Kürzlich überwachte Berichte"
      },
      es: {
        brand_name: "OIL INDIA LIMITED",
        brand_sub: "INTELIGENCIA PRECURSORA SIF · SIH 2026",
        nav_about: "ACERCA DE",
        nav_framework: "MARCO",
        nav_dgms: "CUMPLIMIENTO DGMS",
        btn_portal: "ACCESO AL PORTAL",
        badge_live: "TELEMETRÍA EN VIVO DGMS · MONITOR DE ACTIVOS",
        hero_title_1: "La capa de",
        hero_title_2: "seguridad predictiva para",
        hero_title_3: "operaciones críticas",
        hero_sub: "Inteligencia artificial que detecta microanomalías y estrés de tuberías antes de que ocurran incidentes graves.",
        cta_start: "VER CÓMO COMIENZA SIF",
        cta_console: "CONSOLA DE INCIDENTES",
        hud_title: "FUENTES DE ACTIVOS MONITORIZADOS",
        hero_partner: "IMPULSANDO LA REFINERÍA DULIAJAN Y 4,200+ KM DE OLEODUCTOS",
        footer_brand: "OIL INDIA LIMITED · LABORATORIOS SIF",
        footer_compliance: "CUMPLE DGMS Y OISD-156",
        footer_terms: "TÉRMINOS",
        footer_privacy: "PRIVACIDAD",
        drawer_title: "Consola de Operaciones SIF",
        drawer_sub: "Inteligencia de Seguridad Oil India Limited",
        tab_login: "INICIAR SESIÓN",
        tab_register: "CREAR CUENTA",
        tab_report: "REPORTAR INCIDENTE",
        label_username: "Nombre de usuario",
        label_phone: "Teléfono móvil",
        label_phone_required: "Teléfono móvil (Obligatorio para alertas SMS)",
        label_password: "Contraseña",
        label_fullname: "Nombre completo",
        label_role: "Rol de seguridad",
        label_asset_loc: "Ubicación de la instalación",
        label_department: "Departamento",
        label_report_type: "Tipo de incidente",
        label_hazard_text: "Observación detallada y señales",
        btn_login_submit: "Acceder al portal de seguridad",
        btn_reg_submit: "Crear cuenta de seguridad",
        btn_submit_report: "Enviar al clasificador IA",
        title_recent_reports: "Informes recientes monitorizados"
      },
      ar: {
        brand_name: "أويل إنديا ليمتد",
        brand_sub: "ذكاء السلامة التنبؤي SIF · SIH 2026",
        nav_about: "حول",
        nav_framework: "الإطار",
        nav_dgms: "معايير DGMS",
        btn_portal: "دخول البوابة",
        badge_live: "قياس عن بعد مباشر · مراقبة الأصول الحيوية",
        hero_title_1: "طبقة الأمان",
        hero_title_2: "التنبؤية المتقدمة",
        hero_title_3: "للعمليات الحيوية",
        hero_sub: "ذكاء اصطناعي يكشف الشذوذات الدقيقة وإجهاد خطوط الأنابيب قبل وقوع الحوادث في منشآت الطاقة.",
        cta_start: "استكشف نظام SIF",
        cta_console: "لوحة الحوادث",
        hud_title: "الأصول المراقبة",
        hero_partner: "حماية مصفاة دولياجان و 4200+ كم من خطوط الأنابيب الحيوية",
        footer_brand: "أويل إنديا ليمتد · مختبرات SIF",
        footer_compliance: "معتمد وفق DGMS و OISD-156",
        footer_terms: "الشروط",
        footer_privacy: "الخصوصية",
        drawer_title: "لوحة عمليات SIF",
        drawer_sub: "ذكاء السلامة - أويل إنديا",
        tab_login: "تسجيل الدخول",
        tab_register: "إنشاء حساب",
        tab_report: "إبلاغ عن حادث",
        label_username: "اسم المستخدم",
        label_phone: "رقم الهاتف المحمول",
        label_phone_required: "رقم الهاتف (مطلوب لتنبيهات SMS)",
        label_password: "كلمة المرور",
        label_fullname: "الاسم الكامل",
        label_role: "الدور الأمني",
        label_asset_loc: "موقع المنشأة",
        label_department: "القسم",
        label_report_type: "نوع الحادث",
        label_hazard_text: "الوصف التفصيلي والمؤشرات",
        btn_login_submit: "دخول بوابة الأمان",
        btn_reg_submit: "إنشاء حساب جديد",
        btn_submit_report: "إرسال إلى مصنف الذكاء الاصطناعي",
        title_recent_reports: "أحدث التقارير المسجلة"
      }
    };

    // Initialize Theme
    function initTheme() {
      const savedTheme = localStorage.getItem('sif_theme') || 'dark';
      document.body.setAttribute('data-theme', savedTheme);
      updateThemeIcon(savedTheme);
    }

    function toggleTheme() {
      const current = document.body.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', next);
      localStorage.setItem('sif_theme', next);
      updateThemeIcon(next);
    }

    function updateThemeIcon(theme) {
      const btn = document.getElementById('themeToggleBtn');
      btn.innerText = theme === 'dark' ? '🌙' : '☀️';
    }

    // Language Handling (Instant Dynamic Update)
    function toggleLanguageMenu(e) {
      e.stopPropagation();
      const menu = document.getElementById('langMenuDropdown');
      menu.classList.toggle('show');
    }

    window.addEventListener('click', () => {
      const menu = document.getElementById('langMenuDropdown');
      if (menu) menu.classList.remove('show');
    });

    function changeAppLanguage(langCode, labelText) {
      document.getElementById('currentLangLabel').innerText = labelText;
      const dict = I18N[langCode] || I18N['en'];

      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
          el.innerHTML = dict[key];
        }
      });

      // Update active class in menu
      document.querySelectorAll('.lang-option-item').forEach(b => b.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.lang-option-item')).find(b => b.innerText.includes(labelText.split(' ')[0]));
      if (activeBtn) activeBtn.classList.add('active');

      localStorage.setItem('sif_lang', langCode);
    }

    // Drawer Slide-Over Controls
    function openOverlay(tab = 'login') {
      const backdrop = document.getElementById('slideOverBackdrop');
      backdrop.classList.add('open');
      switchDrawerTab(tab);
      if (tab === 'report') {
        loadRecentReports();
      }
    }

    function closeOverlay() {
      document.getElementById('slideOverBackdrop').classList.remove('open');
    }

    function handleBackdropClick(e) {
      if (e.target.id === 'slideOverBackdrop') {
        closeOverlay();
      }
    }

    function switchDrawerTab(tab) {
      const tabs = ['login', 'register', 'report'];
      tabs.forEach(t => {
        const sec = document.getElementById('section' + t.charAt(0).toUpperCase() + t.slice(1));
        const btn = document.getElementById('tabBtn' + t.charAt(0).toUpperCase() + t.slice(1));
        if (sec) sec.style.display = (t === tab) ? 'block' : 'none';
        if (btn) {
          if (t === tab) btn.classList.add('active');
          else btn.classList.remove('active');
        }
      });

      updateAuthUI();
      if (tab === 'report') {
        loadRecentReports();
      }
    }

    function setLoginMethod(method) {
      currentLoginMethod = method;
      const btnU = document.getElementById('pillLoginUsername');
      const btnP = document.getElementById('pillLoginPhone');
      const grpU = document.getElementById('groupLoginUsername');
      const grpP = document.getElementById('groupLoginPhone');

      if (method === 'phone') {
        btnP.classList.add('active');
        btnU.classList.remove('active');
        grpP.style.display = 'flex';
        grpU.style.display = 'none';
        document.getElementById('loginUsernameInput').removeAttribute('required');
        document.getElementById('loginPhoneInput').setAttribute('required', 'true');
      } else {
        btnU.classList.add('active');
        btnP.classList.remove('active');
        grpU.style.display = 'flex';
        grpP.style.display = 'none';
        document.getElementById('loginUsernameInput').setAttribute('required', 'true');
        document.getElementById('loginPhoneInput').removeAttribute('required');
      }
    }

    // User session & RBAC UI
    let currentUsername = localStorage.getItem('sif_username') || null;

    function updateAuthUI() {
      const userbar = document.getElementById('userSessionBar');
      const userbarUname = document.getElementById('userbarUsername');
      const userbarRole = document.getElementById('userbarRole');
      const unauthBanner = document.getElementById('unauthReportBanner');
      const roleNotice = document.getElementById('roleRestrictionNotice');
      const roleNoticeBadge = document.getElementById('roleNoticeBadge');
      const incidentForm = document.getElementById('incidentForm');

      if (currentAuthToken && currentUserRole) {
        if (userbar) {
          userbar.style.display = 'flex';
          userbarUname.textContent = currentUsername || 'Authenticated User';
          userbarRole.textContent = currentUserRole.replace('_', ' ').toUpperCase();
        }
        if (unauthBanner) unauthBanner.style.display = 'none';

        if (currentUserRole === 'field_worker' || currentUserRole === 'admin') {
          if (roleNotice) roleNotice.style.display = 'none';
          if (incidentForm) incidentForm.style.display = 'block';
        } else {
          // Safety officer / Auditor oversight
          if (roleNotice) {
            if (roleNoticeBadge) roleNoticeBadge.textContent = currentUserRole.replace('_', ' ').toUpperCase();
            roleNotice.style.display = 'block';
          }
          if (incidentForm) incidentForm.style.display = 'none';
        }
      } else {
        if (userbar) userbar.style.display = 'none';
        if (unauthBanner) unauthBanner.style.display = 'block';
        if (roleNotice) roleNotice.style.display = 'none';
        if (incidentForm) incidentForm.style.display = 'block';
      }
    }

    function logout() {
      currentAuthToken = null;
      currentUserRole = null;
      currentUsername = null;
      localStorage.removeItem('sif_auth_token');
      localStorage.removeItem('sif_user_role');
      localStorage.removeItem('sif_username');
      updateAuthUI();
      switchDrawerTab('login');
      loadRecentReports();
    }

    // Autocomplete Suggestion Logic
    let suggestDebounce = null;

    function onReportTextInput() {
      clearTimeout(suggestDebounce);
      suggestDebounce = setTimeout(fetchSuggestions, 250);
    }

    async function fetchSuggestions() {
      const textarea = document.getElementById('reportTextInput');
      if (!textarea) return;
      const fullText = textarea.value;
      const words = fullText.trim().split(/\s+/);
      const lastWords = words.slice(-4).join(' ');
      if (lastWords.length < 2) { hideSuggestions(); return; }

      try {
        const res = await fetch(`http://127.0.0.1:8000/suggest?q=${encodeURIComponent(lastWords)}`);
        const data = await res.json();
        renderSuggestions(data.suggestions || [], fullText);
      } catch (e) { hideSuggestions(); }
    }

    function renderSuggestions(suggestions, currentText) {
      const box = document.getElementById('suggestBox');
      if (!box) return;
      if (!suggestions || !suggestions.length) { hideSuggestions(); return; }
      box.innerHTML = suggestions.map(s =>
        `<div class="suggest-item" onmousedown="applySuggestion('${s.replace(/'/g, "\\'")}')">
           🔍 ${s}
         </div>`
      ).join('');
      box.style.display = 'block';
    }

    function applySuggestion(suggestion) {
      const textarea = document.getElementById('reportTextInput');
      if (!textarea) return;
      let text = textarea.value.trim();
      const words = text.split(/\s+/);
      const kept = words.slice(0, Math.max(0, words.length - 4)).join(' ');
      textarea.value = (kept ? kept + ' ' : '') + suggestion + ' ';
      textarea.focus();
      hideSuggestions();
    }

    function hideSuggestions() {
      const box = document.getElementById('suggestBox');
      if (box) box.style.display = 'none';
    }

    // Authentication Handlers (Preserves 100% of Backend API Contracts!)
    async function handleLoginSubmit(e) {
      e.preventDefault();
      const alertBox = document.getElementById('loginAlert');
      alertBox.style.display = 'none';
      alertBox.className = 'auth-alert-message';

      let identifier = '';
      if (currentLoginMethod === 'phone') {
        identifier = document.getElementById('loginPhoneInput').value.trim();
      } else {
        identifier = document.getElementById('loginUsernameInput').value.trim();
      }
      const password = document.getElementById('loginPasswordInput').value;

      try {
        const body = new URLSearchParams();
        body.append('username', identifier);
        body.append('password', password);

        const resp = await fetch('http://127.0.0.1:8000/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: body.toString()
        });

        const data = await resp.json();
        if (!resp.ok) {
          throw new Error(data.detail || 'Login failed. Please verify credentials.');
        }

        currentAuthToken = data.access_token;
        currentUserRole = data.role;
        currentUsername = identifier;
        localStorage.setItem('sif_auth_token', currentAuthToken);
        localStorage.setItem('sif_user_role', currentUserRole);
        localStorage.setItem('sif_username', currentUsername);

        alertBox.innerText = `Login successful! Authorized as ${data.role.toUpperCase()}`;
        alertBox.classList.add('auth-alert-success');
        alertBox.style.display = 'block';

        updateAuthUI();
        setTimeout(() => {
          switchDrawerTab('report');
          loadRecentReports();
        }, 800);
      } catch (err) {
        alertBox.innerText = err.message;
        alertBox.classList.add('auth-alert-error');
        alertBox.style.display = 'block';
      }
    }

    async function handleRegisterSubmit(e) {
      e.preventDefault();
      const alertBox = document.getElementById('registerAlert');
      alertBox.style.display = 'none';
      alertBox.className = 'auth-alert-message';

      const fullName = document.getElementById('regFullNameInput').value.trim();
      const phone = document.getElementById('regPhoneInput').value.trim();
      const username = document.getElementById('regUsernameInput').value.trim();
      const password = document.getElementById('regPasswordInput').value;
      const role = document.getElementById('regRoleSelect').value;

      try {
        const resp = await fetch('http://127.0.0.1:8000/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: username,
            password: password,
            role: role
          })
        });

        const data = await resp.json();
        if (!resp.ok) {
          throw new Error(data.detail || 'Registration failed.');
        }

        currentAuthToken = data.access_token;
        currentUserRole = data.role;
        currentUsername = username;
        localStorage.setItem('sif_auth_token', currentAuthToken);
        localStorage.setItem('sif_user_role', currentUserRole);
        localStorage.setItem('sif_username', currentUsername);

        alertBox.innerText = `Account created successfully for ${fullName} (${role})!`;
        alertBox.classList.add('auth-alert-success');
        alertBox.style.display = 'block';

        updateAuthUI();
        setTimeout(() => {
          switchDrawerTab('report');
          loadRecentReports();
        }, 1000);
      } catch (err) {
        alertBox.innerText = err.message;
        alertBox.classList.add('auth-alert-error');
        alertBox.style.display = 'block';
      }
    }

    // Incident Report & AI Precursor ML Classification
    async function handleReportSubmit(e) {
      e.preventDefault();
      const alertBox = document.getElementById('reportAlert');
      alertBox.style.display = 'none';
      alertBox.className = 'auth-alert-message';

      if (!currentAuthToken) {
        alertBox.innerText = "Please log in first to submit verified safety reports.";
        alertBox.classList.add('auth-alert-error');
        alertBox.style.display = 'block';
        return;
      }

      if (currentUserRole !== 'field_worker' && currentUserRole !== 'admin') {
        alertBox.innerText = "Safety Officers oversee records. Ground reporting is restricted to Field Workers.";
        alertBox.classList.add('auth-alert-error');
        alertBox.style.display = 'block';
        return;
      }

      const location = document.getElementById('reportLocationSelect').value;
      const department = document.getElementById('reportDeptSelect').value;
      const reportType = document.getElementById('reportTypeSelect').value;
      const reportText = document.getElementById('reportTextInput').value.trim();

      try {
        const resp = await fetch('http://127.0.0.1:8000/reports', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${currentAuthToken}`
          },
          body: JSON.stringify({
            report_type: reportType,
            location: location,
            department: department,
            report_text: reportText
          })
        });

        const data = await resp.json();
        if (!resp.ok) {
          throw new Error(data.detail || 'Failed to submit report.');
        }

        alertBox.innerText = "Precursor Incident Report successfully logged and analyzed!";
        alertBox.classList.add('auth-alert-success');
        alertBox.style.display = 'block';

        // Clear input and hide suggestions
        document.getElementById('reportTextInput').value = '';
        hideSuggestions();

        // Render AI Risk Prediction & SHAP Explainability
        const predCard = document.getElementById('predictionResultCard');
        const statusEl = document.getElementById('predRiskStatus');
        const probEl = document.getElementById('predProbMeter');
        const shapEl = document.getElementById('predShapFactors');

        predCard.style.display = 'block';
        const isPrecursor = (data.predicted_label ?? data.sif_prediction) === 1;
        const probability = ((data.predicted_probability ?? data.sif_probability ?? 0) * 100).toFixed(1);

        statusEl.innerHTML = isPrecursor
          ? `<span style="color: #EF4444; font-weight:800;">⚠️ CRITICAL PRECURSOR DETECTED (High SIF Risk)</span>`
          : `<span style="color: #10B981; font-weight:800;">✅ BENIGN OBSERVATION (Low Precursor Risk)</span>`;

        probEl.innerText = `Calculated SIF Probability: ${probability}%`;

        let factors = [];
        if (typeof data.top_factors === 'string') {
          try { factors = JSON.parse(data.top_factors); } catch (e) { }
        } else if (Array.isArray(data.top_factors)) {
          factors = data.top_factors;
        }

        let factorsHtml = `<strong>Top Precursor Contributing Drivers:</strong><div style="display:flex; flex-wrap:wrap; gap:4px; margin-top:6px;">`;
        if (factors && factors.length) {
          factors.forEach(f => {
            const cleanName = f.feature.replace('flag_', '').replace('count_', '').replace('tfidf_', '');
            factorsHtml += `<span class="chip-tag" style="font-size:10px; padding:2px 6px;">${cleanName} (${f.impact > 0 ? '+' : ''}${f.impact})</span>`;
          });
        } else {
          factorsHtml += `<span style="color:var(--text-muted); font-size:11px;">No high-impact anomaly flags triggered</span>`;
        }
        factorsHtml += `</div>`;
        shapEl.innerHTML = factorsHtml;

        loadRecentReports();
      } catch (err) {
        alertBox.innerText = err.message;
        alertBox.classList.add('auth-alert-error');
        alertBox.style.display = 'block';
      }
    }

    async function loadRecentReports() {
      const container = document.getElementById('recentReportsList');
      const titleEl = document.getElementById('recentReportsTitle');

      if (titleEl) {
        if (currentUserRole === 'field_worker') {
          titleEl.textContent = '📋 My Submitted Reports';
        } else if (currentUserRole === 'safety_officer' || currentUserRole === 'admin') {
          titleEl.textContent = '📊 All Reports Telemetry Dashboard';
        } else {
          titleEl.textContent = '📊 Recent Monitored Reports';
        }
      }

      try {
        const headers = {};
        if (currentAuthToken) {
          headers['Authorization'] = `Bearer ${currentAuthToken}`;
        }
        const resp = await fetch('http://127.0.0.1:8000/reports', { headers });
        if (!resp.ok) {
          container.innerHTML = `<div style="font-size: 12px; color: var(--text-muted); padding: 8px 0;">Sign in to stream live incident database.</div>`;
          return;
        }
        const reports = await resp.json();
        if (!reports || reports.length === 0) {
          container.innerHTML = `<div style="font-size: 12px; color: var(--text-muted); padding: 8px 0;">No hazard reports filed yet. Submit the first observation above.</div>`;
          return;
        }

        container.innerHTML = reports.slice(0, 8).map(r => {
          const isHigh = (r.predicted_label ?? r.sif_prediction) === 1;
          const prob = ((r.predicted_probability ?? r.sif_probability ?? 0) * 100).toFixed(0);
          const dateStr = r.created_at ? new Date(r.created_at).toLocaleString() : 'Recent';
          const author = r.submitted_by_username ? `By: ${r.submitted_by_username}` : '';

          let factors = [];
          if (typeof r.top_factors === 'string') {
            try { factors = JSON.parse(r.top_factors || '[]'); } catch (e) { }
          } else if (Array.isArray(r.top_factors)) {
            factors = r.top_factors;
          }
          const factorChips = factors.slice(0, 3).map(f => {
            const name = f.feature.replace('flag_', '').replace('count_', '').replace('tfidf_', '');
            return `<span class="chip-tag" style="font-size:9.5px; padding:1px 5px;">${name}</span>`;
          }).join(' ');

          return `
            <div class="report-card-item" style="padding:10px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid var(--card-border); margin-bottom:8px;">
              <div class="report-card-header" style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px;">
                <div>
                  <span style="font-weight:600; font-size:12px; color:var(--text-main);">${r.location}</span>
                  <span style="font-size:10.5px; color:var(--text-muted);"> · ${r.department}</span>
                  <div style="font-size:10px; color:var(--accent-sky);">${r.report_type}</div>
                </div>
                <span class="${isHigh ? 'risk-badge-high' : 'risk-badge-low'}" style="font-size:10px; padding:2px 8px; border-radius:12px; font-weight:700; ${isHigh ? 'background:#ef4444; color:#fff;' : 'background:#10b981; color:#fff;'}">
                  ${isHigh ? '⚠️ SIF RISK' : '✅ LOW RISK'} (${prob}%)
                </span>
              </div>
              <div style="font-size: 11.5px; color: var(--text-main); margin: 6px 0; line-height: 1.35;">${r.report_text}</div>
              <div style="display:flex; flex-wrap:wrap; gap:3px; margin-bottom:4px;">${factorChips}</div>
              <div style="display:flex; justify-content:space-between; font-size: 9.5px; color: var(--text-muted); margin-top:4px;">
                <span>${dateStr}</span>
                <span>${author}</span>
              </div>
            </div>
          `;
        }).join('');
      } catch (e) {
        container.innerHTML = `<div style="font-size: 12px; color: var(--text-muted);">Live feed waiting for API connection.</div>`;
      }
    }

    // Modal Lightbox for Asset Feeds
    function openImageModal(imgSrc, title, desc) {
      document.getElementById('modalImgTag').src = imgSrc;
      document.getElementById('modalTitle').innerText = title;
      document.getElementById('modalDesc').innerText = desc;
      document.getElementById('imageModal').classList.add('open');
    }

    function closeImageModal(e) {
      if (!e || e.target.id === 'imageModal' || !e.target.closest('.image-modal-card')) {
        document.getElementById('imageModal').classList.remove('open');
      }
    }

    // Startup
    document.addEventListener('DOMContentLoaded', () => {
      initTheme();
      updateAuthUI();
      const savedLang = localStorage.getItem('sif_lang') || 'en';
      const labelMap = {
        en: 'English (EN)', hi: 'हिन्दी (HI)', as: 'অসমীয়া (AS)', bn: 'বাংলা (BN)',
        mr: 'मराठी (MR)', gu: 'ગુજરાતી (GU)', ta: 'தமிழ் (TA)', te: 'తెలుగు (TE)',
        kn: 'ಕನ್ನಡ (KN)', ml: 'മലയാളം (ML)', pa: 'ਪੰਜਾਬੀ (PA)', or: 'ଓଡ଼ିଆ (OR)',
        fr: 'Français (FR)', de: 'Deutsch (DE)', es: 'Español (ES)', ar: 'العربية (AR)'
      };
      changeAppLanguage(savedLang, labelMap[savedLang] || 'English (EN)');
    });
  </script>
</body>

</html>'''

with open('frontend.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
