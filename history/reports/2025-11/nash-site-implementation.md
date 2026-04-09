# Nash Group Site - Technical Implementation Guide v2.1
## Incorporating Architectural Refinements

> "Approved for implementation. Sovereign state. Institutional precision."

---

## TECHNICAL ADVISORY INTEGRATION

This document incorporates all architectural refinements from the technical review, ensuring the deployment matches the severity of the specification.

---

## PART I: PROJECT INITIALIZATION (REFINED)

### 1.1 Enhanced Dependencies

```bash
# Initialize Astro project
npm create astro@latest the-nash-group -- --template minimal --typescript strict --no-install

cd the-nash-group

# Core dependencies
npm install

# Cloudflare adapter
npm install -D @astrojs/cloudflare wrangler

# Build optimization
npm install -D terser

# WASM integration (CRITICAL REFINEMENT)
npm install -D vite-plugin-wasm vite-plugin-top-level-await

# Font management
npm install -D @fontsource/ibm-plex-mono @fontsource/ibm-plex-sans

# Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup target add wasm32-unknown-unknown
cargo install wasm-pack
```

### 1.2 Enhanced Configuration

#### `astro.config.mjs` (REFINED)

```javascript
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';
import wasm from 'vite-plugin-wasm';
import topLevelAwait from 'vite-plugin-top-level-await';

export default defineConfig({
  output: 'hybrid',
  adapter: cloudflare({
    mode: 'directory',
    functionPerRoute: false
  }),
  vite: {
    plugins: [
      wasm(),           // WASM integration into build pipeline
      topLevelAwait()   // Required for async WASM initialization
    ],
    build: {
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: false // Surveillance messages are features
        },
        format: {
          comments: false
        }
      },
      rollupOptions: {
        output: {
          // Ensure WASM files are properly hashed
          assetFileNames: (assetInfo) => {
            if (assetInfo.name.endsWith('.wasm')) {
              return 'assets/[name].[hash][extname]';
            }
            return 'assets/[name].[hash][extname]';
          }
        }
      }
    }
  }
});
```

**Rationale:** This ensures the WASM binary is hashed and cached correctly (`session_engine.[hash].wasm`), preventing stale logic during updates. The build pipeline now has full visibility into the WASM module.

---

## PART II: RUST SESSION ENGINE (REFINED)

### 2.1 `src/rust/Cargo.toml`

```toml
[package]
name = "session-engine"
version = "1.0.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2"
getrandom = { version = "0.2", features = ["js"] }
serde = { version = "1.0", features = ["derive"] }
serde-wasm-bindgen = "0.6"
web-sys = { version = "0.3", features = ["console"] }

[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
strip = true
```

### 2.2 `src/rust/src/lib.rs` (REFINED)

```rust
use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};

/// Continuity Anchor - Historical reference points for session derivation
#[derive(Serialize, Deserialize)]
pub struct ContinuityAnchor {
    epoch: u16,
    designation: String,
    jurisdiction: String,
}

/// Session Management Engine
/// Implements multi-generational session tracking
#[wasm_bindgen]
pub struct SessionEngine {
    anchors: Vec<ContinuityAnchor>,
}

#[wasm_bindgen]
impl SessionEngine {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        Self {
            anchors: vec![
                ContinuityAnchor {
                    epoch: 1518,
                    designation: "ALPHA".to_string(),
                    jurisdiction: "SCOT/GLEN".to_string(),
                },
                ContinuityAnchor {
                    epoch: 1622,
                    designation: "BETA".to_string(),
                    jurisdiction: "SCOT/HIGH".to_string(),
                },
                ContinuityAnchor {
                    epoch: 1746,
                    designation: "GAMMA".to_string(),
                    jurisdiction: "SCOT/CULL".to_string(),
                },
                ContinuityAnchor {
                    epoch: 1985,
                    designation: "DELTA".to_string(),
                    jurisdiction: "NYC/ZERO".to_string(), // REFINED: Gathering epicenter
                },
            ],
        }
    }

    /// Generates session identifier using temporal derivation
    #[wasm_bindgen(js_name = generateSessionId)]
    pub fn generate_session_id(&self, timestamp: f64) -> String {
        let index = (timestamp as usize) % self.anchors.len();
        let anchor = &self.anchors[index];
        format!("{}-{}", anchor.epoch, anchor.designation)
    }

    /// Determines access clearance based on behavioral entropy
    #[wasm_bindgen(js_name = determineAccessLevel)]
    pub fn determine_access_level(&self, entropy: f64) -> String {
        match entropy {
            e if e > 0.8 => "ALPHA".to_string(),
            e if e > 0.5 => "BETA".to_string(),
            e if e > 0.2 => "GAMMA".to_string(),
            _ => "DELTA".to_string(),
        }
    }

    /// Returns jurisdiction for given session
    #[wasm_bindgen(js_name = getJurisdiction)]
    pub fn get_jurisdiction(&self, timestamp: f64) -> String {
        let index = (timestamp as usize) % self.anchors.len();
        self.anchors[index].jurisdiction.clone()
    }
}

#[wasm_bindgen(start)]
pub fn initialize() {
    web_sys::console::log_1(&"SESSION ENGINE INITIALIZED".into());
}
```

### 2.3 Build WASM Module

```bash
cd src/rust
wasm-pack build --target web --out-dir ../../src/wasm
cd ../..
```

**Note:** Output to `src/wasm` (not `public/wasm`) so Vite can process it through the build pipeline.

---

## PART III: ENHANCED SURVEILLANCE SYSTEM

### 3.1 `src/lib/surveillance.ts` (REFINED)

```typescript
/**
 * Compliance and Monitoring System
 * Implements institutional observation protocols with enhanced honeypot
 */

export function initializeComplianceLogging(): void {
  console.clear();

  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 12px;'
  );
  console.log(
    '%c  THE NASH GROUP',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 14px; font-weight: bold;'
  );
  console.log(
    '%c  ACCESS LOGGED',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 12px;'
  );
  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 12px;'
  );
  console.log('');
  console.log(
    '%c  SYSTEM STATUS:',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 12px;'
  );
  console.log(
    '%c  ● COVENANT .......... ENFORCED',
    'color: #00FF41; font-family: "IBM Plex Mono", monospace; font-size: 11px;'
  );
  console.log(
    '%c  ● CITADEL ........... LOCKED',
    'color: #00FF41; font-family: "IBM Plex Mono", monospace; font-size: 11px;'
  );
  console.log(
    '%c  ● NEXUS ............. ACTIVE',
    'color: #00FF41; font-family: "IBM Plex Mono", monospace; font-size: 11px;'
  );
  console.log('');
  console.log(
    '%c  Developer tool access has been recorded.',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 11px; font-style: italic;'
  );
  console.log(
    '%c  Unauthorized reproduction of schemas is prohibited.',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 11px; font-style: italic;'
  );
  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 12px;'
  );
}

// REFINED: Enhanced honeypot for technical curiosity
export function displayRecruitmentNotice(): void {
  const traceId = crypto.randomUUID();

  console.log('');
  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #FF0000; font-family: "IBM Plex Mono", monospace; font-size: 12px;'
  );
  console.log(
    '%c  SUBJECT: TECHNICAL CURIOSITY DETECTED',
    'color: #FF0000; font-family: "IBM Plex Mono", monospace; font-size: 12px; font-weight: bold;'
  );
  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #FF0000; font-family: "IBM Plex Mono", monospace; font-size: 12px;'
  );
  console.log('');
  console.log(
    '%c  You have breached the presentation layer.',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 11px;'
  );
  console.log('');
  console.log(
    '%c  If you are looking for vulnerabilities:',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 11px;'
  );
  console.log(
    '%c  > None exist. State is immutable.',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 11px;'
  );
  console.log('');
  console.log(
    '%c  If you are looking for answers:',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 11px;'
  );
  console.log(
    '%c  > admin@thenash.group',
    'color: #000000; font-family: "IBM Plex Mono", monospace; font-size: 11px;'
  );
  console.log('');
  console.log(
    '%c  TRACE_ID: ' + traceId,
    'color: #888888; font-family: "IBM Plex Mono", monospace; font-size: 10px; font-style: italic;'
  );
  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #FF0000; font-family: "IBM Plex Mono", monospace; font-size: 12px;'
  );
}

export function detectComplianceViolations(): void {
  let suspiciousActivity = 0;
  let consoleOpened = false;

  // Rapid clicking detection
  let clickCount = 0;
  document.addEventListener('click', () => {
    clickCount++;
    setTimeout(() => clickCount = 0, 1000);
    if (clickCount > 10) {
      suspiciousActivity++;
      console.warn(
        '%c COMPLIANCE ALERT: Anomalous interaction pattern detected',
        'color: #FF0000; font-weight: bold; font-family: "IBM Plex Mono", monospace;'
      );
    }
  });

  // Console inspection detection
  const threshold = 160;
  const checkConsole = () => {
    if (
      window.outerHeight - window.innerHeight > threshold ||
      window.outerWidth - window.innerWidth > threshold
    ) {
      if (!consoleOpened) {
        consoleOpened = true;
        displayRecruitmentNotice();
      }
    }
  };

  window.addEventListener('resize', checkConsole);

  // Also check on devtools shortcut keys
  document.addEventListener('keydown', (e) => {
    // F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C
    if (
      e.key === 'F12' ||
      (e.ctrlKey && e.shiftKey && ['I', 'J', 'C'].includes(e.key))
    ) {
      setTimeout(checkConsole, 100);
    }
  });

  // Initial check
  checkConsole();
}
```

---

## PART IV: INSTITUTIONAL STYLING (REFINED)

### 4.1 Font Installation

```typescript
// src/layouts/InstitutionalLayout.astro
---
// Import IBM Plex fonts
import '@fontsource/ibm-plex-sans/400.css';
import '@fontsource/ibm-plex-sans/600.css';
import '@fontsource/ibm-plex-mono/400.css';
import '@fontsource/ibm-plex-mono/600.css';
---
```

### 4.2 `src/styles/institutional.css` (REFINED)

```css
/**
 * The Nash Group Institutional Stylesheet
 *
 * Design System: Hermetic Institutionalism
 * Typeface: IBM Plex (Mid-century bureaucratic authority)
 * Grid: Strict geometric alignment
 * Palette: Absolute monochrome
 */

/* ════════════════════════════════════════════════════
   RESET & FOUNDATION
   ════════════════════════════════════════════════════ */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ════════════════════════════════════════════════════
   DESIGN TOKENS (REFINED)
   ════════════════════════════════════════════════════ */

:root {
  /* Institutional Palette */
  --bg: #FFFFFF;
  --text: #000000;
  --border: #E5E5E5;
  --status-active: #00FF41;
  --status-alert: #FF0000;

  /* Geometric Spacing (8px base grid) */
  --space-1: 0.5rem;   /* 8px */
  --space-2: 1rem;     /* 16px */
  --space-3: 1.5rem;   /* 24px */
  --space-4: 2rem;     /* 32px */
  --space-5: 3rem;     /* 48px */
  --space-6: 4rem;     /* 64px */
  --space-8: 6rem;     /* 96px */

  /* Typography System (REFINED: IBM Plex) */
  --font-primary: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont,
                  "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  --font-mono: 'IBM Plex Mono', "SF Mono", "Consolas",
               "Liberation Mono", "Courier New", monospace;

  /* Grid System */
  --grid-unit: 8px;
  --content-width: 72ch;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--font-primary);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text);
  background: var(--bg);
  cursor: crosshair; /* REFINED: Precision targeting */
}

/* ════════════════════════════════════════════════════
   CURSOR DIRECTIVES (REFINED)
   ════════════════════════════════════════════════════ */

a, button {
  cursor: help; /* Indicates "Querying" the element */
}

input, textarea, select {
  cursor: text;
}

.status-indicator {
  cursor: default;
}

/* ════════════════════════════════════════════════════
   LAYOUT SYSTEM
   ════════════════════════════════════════════════════ */

.container {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: var(--space-8) var(--space-4);
  min-height: 100vh;
}

/* ════════════════════════════════════════════════════
   HEADER - STATUS BAR
   ════════════════════════════════════════════════════ */

header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: calc(var(--grid-unit) * 6);
  padding: 0 var(--space-4);
  background: var(--bg);
  border-bottom: 1px solid var(--text);
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  z-index: 1000;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

header .logo {
  justify-self: start;
}

header .session-display {
  justify-self: end;
  text-align: right;
}

main {
  margin-top: calc(var(--grid-unit) * 8);
}

/* ════════════════════════════════════════════════════
   TYPOGRAPHY
   ════════════════════════════════════════════════════ */

h1, h2, h3, h4, h5, h6 {
  font-weight: 400;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

h1 {
  font-size: 2rem;
  margin-bottom: var(--space-6);
  border-bottom: 1px solid var(--text);
  padding-bottom: var(--space-2);
}

h2 {
  font-size: 1.5rem;
  margin-top: var(--space-6);
  margin-bottom: var(--space-3);
}

h3 {
  font-size: 1.125rem;
  margin-top: var(--space-4);
  margin-bottom: var(--space-2);
}

p {
  margin-bottom: var(--space-3);
}

/* ════════════════════════════════════════════════════
   LINKS - NO AFFORDANCE
   ════════════════════════════════════════════════════ */

a {
  color: inherit;
  text-decoration: none;
  position: relative;
}

a::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--text);
  transition: width 150ms ease;
}

a:hover::after {
  width: 100%;
}

/* ════════════════════════════════════════════════════
   LISTS - TECHNICAL MARKERS
   ════════════════════════════════════════════════════ */

ul {
  list-style: none;
  margin: var(--space-3) 0;
}

li {
  margin: var(--space-2) 0;
  padding-left: var(--space-3);
  position: relative;
}

li::before {
  content: '●';
  position: absolute;
  left: 0;
  font-size: 0.5em;
  top: 0.4em;
}

/* ════════════════════════════════════════════════════
   TABLES - DATA STRUCTURES
   ════════════════════════════════════════════════════ */

table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--space-4) 0;
  font-family: var(--font-mono);
  font-size: 0.875rem;
}

th, td {
  border: 1px solid var(--border);
  padding: var(--space-2);
  text-align: left;
}

th {
  background: var(--text);
  color: var(--bg);
  font-weight: 400;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ════════════════════════════════════════════════════
   SESSION MONITOR
   ════════════════════════════════════════════════════ */

#session-monitor {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  line-height: 1.4;
  white-space: pre;
  color: var(--text);
  background: var(--bg);
  border: 1px solid var(--border);
  padding: var(--space-3);
  margin: var(--space-4) 0;
}

/* ════════════════════════════════════════════════════
   STATUS INDICATORS
   ════════════════════════════════════════════════════ */

.status-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: var(--space-2);
  font-family: var(--font-mono);
  font-size: 0.875rem;
  margin: var(--space-4) 0;
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--status-active);
}

.status-indicator.alert {
  background: var(--status-alert);
}

/* ════════════════════════════════════════════════════
   ACCESS NOTICE
   ════════════════════════════════════════════════════ */

.access-notice {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--bg);
  border: 2px solid var(--text);
  padding: var(--space-5);
  max-width: 50ch;
  font-family: var(--font-mono);
  font-size: 0.875rem;
  z-index: 2000;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.access-notice pre {
  font-family: inherit;
  margin-bottom: var(--space-3);
  line-height: 1.4;
}

.access-notice button {
  margin-top: var(--space-3);
  padding: var(--space-2) var(--space-4);
  background: var(--text);
  color: var(--bg);
  border: none;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: help;
  width: 100%;
  transition: opacity 150ms;
}

.access-notice button:hover {
  opacity: 0.8;
}

/* ════════════════════════════════════════════════════
   LEGAL SECTIONS
   ════════════════════════════════════════════════════ */

.legal {
  font-size: 0.875rem;
  border: 1px solid var(--border);
  padding: var(--space-3);
  margin: var(--space-5) 0;
  background: var(--bg);
}

.legal p {
  margin-bottom: var(--space-2);
}

/* ════════════════════════════════════════════════════
   FOOTER
   ════════════════════════════════════════════════════ */

footer {
  margin-top: var(--space-8);
  padding-top: var(--space-4);
  border-top: 1px solid var(--text);
  font-family: var(--font-mono);
  font-size: 0.75rem;
}

footer .divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: var(--space-3) 0;
}

/* ════════════════════════════════════════════════════
   RESPONSIVE
   ════════════════════════════════════════════════════ */

@media (max-width: 768px) {
  :root {
    font-size: 14px;
  }

  .container {
    padding: var(--space-6) var(--space-3);
  }

  header {
    grid-template-columns: 1fr;
    text-align: center;
    height: auto;
    padding: var(--space-2);
  }

  header .session-display {
    justify-self: center;
    margin-top: var(--space-1);
  }
}

/* ════════════════════════════════════════════════════
   PRINT
   ════════════════════════════════════════════════════ */

@media print {
  header {
    position: static;
  }

  .access-notice {
    display: none;
  }

  a::after {
    display: none;
  }

  body {
    cursor: default;
  }
}
```

---

## PART V: SESSION MANAGEMENT (REFINED)

### 5.1 `src/lib/session-engine.ts` (REFINED)

```typescript
/**
 * Nash Group Session Management System
 * Implements institutional-grade session tracking with WASM integration
 */

interface SessionState {
  id: string;
  clearance: string;
  initiated: string;
  requests: number;
  jurisdiction: string;
  status: 'ACTIVE' | 'MONITORED' | 'RESTRICTED';
}

export class SessionManager {
  private state: SessionState;
  private wasmEngine: any;

  constructor() {
    this.state = {
      id: '',
      clearance: 'DELTA',
      initiated: new Date().toISOString(),
      requests: 0,
      jurisdiction: 'UNDETERMINED',
      status: 'ACTIVE'
    };
  }

  async initialize(): Promise<SessionState> {
    // REFINED: Import WASM directly from build pipeline
    const wasm = await import('../wasm/session_engine');
    await wasm.default();
    this.wasmEngine = new wasm.SessionEngine();

    // Generate session identifier
    const timestamp = Date.now();
    this.state.id = this.wasmEngine.generateSessionId(timestamp);

    // Get jurisdiction from WASM engine
    this.state.jurisdiction = this.wasmEngine.getJurisdiction(timestamp);

    // Determine access clearance
    const entropy = await this.measureBehavioralEntropy();
    this.state.clearance = this.wasmEngine.determineAccessLevel(entropy);

    // Enhance jurisdiction with geolocation if available
    await this.enhanceJurisdiction();

    // Initialize monitoring
    this.activateMonitoring();

    return this.state;
  }

  private async measureBehavioralEntropy(): Promise<number> {
    return new Promise((resolve) => {
      let samples = 0;
      let variance = 0;
      let lastX = 0, lastY = 0;

      const handler = (e: MouseEvent) => {
        if (samples > 0) {
          const delta = Math.sqrt(
            Math.pow(e.clientX - lastX, 2) +
            Math.pow(e.clientY - lastY, 2)
          );
          variance += delta;
        }
        lastX = e.clientX;
        lastY = e.clientY;
        samples++;
      };

      document.addEventListener('mousemove', handler);

      setTimeout(() => {
        document.removeEventListener('mousemove', handler);
        const entropy = samples > 0 ?
          Math.min(variance / (samples * 100), 1) : 0.1;
        resolve(entropy);
      }, 2000);
    });
  }

  private async enhanceJurisdiction(): Promise<void> {
    try {
      // Cloudflare Workers provides geolocation automatically
      const response = await fetch('/api/geolocation');
      const data = await response.json();

      // Append to existing jurisdiction from WASM
      this.state.jurisdiction = `${this.state.jurisdiction} (${data.country}/${data.region})`;
    } catch {
      // If geolocation fails, keep WASM-derived jurisdiction
    }
  }

  private activateMonitoring(): void {
    // Monitor all network requests
    const originalFetch = window.fetch;
    window.fetch = (...args) => {
      this.state.requests++;
      this.updateDisplay();
      return originalFetch(...args);
    };

    // Monitor navigation
    const originalPushState = history.pushState;
    history.pushState = (...args) => {
      this.state.requests++;
      this.updateDisplay();
      return originalPushState.apply(history, args);
    };
  }

  updateDisplay(): void {
    const monitor = document.getElementById('session-monitor');
    if (monitor) {
      const duration = this.calculateDuration();
      monitor.textContent = `
SESSION: ${this.state.id}
DURATION: ${duration}
CLEARANCE: ${this.state.clearance}
JURISDICTION: ${this.state.jurisdiction}
REQUESTS: ${this.state.requests}
STATUS: ${this.state.status}
      `.trim();
    }
  }

  private calculateDuration(): string {
    const start = new Date(this.state.initiated);
    const now = new Date();
    const diff = now.getTime() - start.getTime();

    const hours = Math.floor(diff / 3600000);
    const minutes = Math.floor((diff % 3600000) / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);

    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  }

  getState(): SessionState {
    return this.state;
  }
}
```

---

## PART VI: TERRAFORM STATE SOVEREIGNTY (REFINED)

### 6.1 Cloudflare R2 Setup

```bash
# Create R2 bucket via Cloudflare dashboard or wrangler
wrangler r2 bucket create nash-group-terraform-state

# Generate R2 API token with read/write access to the bucket
# Store credentials as environment variables:
export AWS_ACCESS_KEY_ID="<R2_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<R2_SECRET_ACCESS_KEY>"
export AWS_ENDPOINT_URL="https://<ACCOUNT_ID>.r2.cloudflarestorage.com"
```

### 6.2 `terraform/main.tf` (REFINED)

```hcl
# Nash Group Infrastructure Configuration
# State Sovereignty: Cloudflare R2

terraform {
  required_version = ">= 1.6"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }

  # REFINED: Use Cloudflare R2 for state (sovereign state management)
  backend "s3" {
    bucket = "nash-group-terraform-state"
    key    = "citadel/production.tfstate"
    region = "auto"

    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true

    # Credentials provided via environment variables:
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    # Endpoint set via AWS_ENDPOINT_URL environment variable
  }
}

variable "cloudflare_account_id" {
  type        = string
  description = "Cloudflare account identifier"
}

variable "domain" {
  type    = string
  default = "thenash.group"
}
```

**Rationale:** This keeps the state file within the same perimeter as the enforcement infrastructure. No external dependencies on Terraform Cloud.

---

## PART VII: ENHANCED WAF CONFIGURATION (REFINED)

### 7.1 `terraform/cloudflare.tf` (REFINED)

```hcl
# Institutional Infrastructure Configuration with Enhanced Security

resource "cloudflare_zone" "main" {
  account_id = var.cloudflare_account_id
  zone       = var.domain
  plan       = "business"
}

# REFINED: Enable DNSSEC for zone integrity
resource "cloudflare_zone_dnssec" "main" {
  zone_id = cloudflare_zone.main.id
}

# Institutional Security Headers
resource "cloudflare_page_rule" "security_headers" {
  zone_id  = cloudflare_zone.main.id
  target   = "${var.domain}/*"
  priority = 1

  actions {
    security_header {
      enabled = true

      strict_transport_security {
        enabled            = true
        max_age            = 31536000
        include_subdomains = true
        preload            = true
      }

      content_type_nosniff = true
      x_frame_options      = "DENY"
      referrer_policy      = "no-referrer"
    }
  }
}

# REFINED: Geo-blocking for high-risk regions
resource "cloudflare_filter" "geo_block" {
  zone_id     = cloudflare_zone.main.id
  description = "Block high-risk jurisdictions"
  expression  = "(ip.geoip.country in {\"CN\" \"RU\" \"KP\" \"IR\"})"
}

resource "cloudflare_firewall_rule" "geo_block" {
  zone_id     = cloudflare_zone.main.id
  description = "Enforce geographic access restrictions"
  filter_id   = cloudflare_filter.geo_block.id
  action      = "block"
  priority    = 1
}

# WAF Configuration
resource "cloudflare_ruleset" "waf_institutional" {
  zone_id     = cloudflare_zone.main.id
  name        = "Institutional Access Control"
  description = "Enforces access policies and threat mitigation"
  kind        = "zone"
  phase       = "http_request_firewall_custom"

  rules {
    action      = "block"
    description = "Block known malicious patterns"
    expression  = <<-EOT
      (http.user_agent contains "sqlmap") or
      (http.user_agent contains "nikto") or
      (http.user_agent contains "masscan") or
      (http.user_agent contains "nmap")
    EOT
  }

  rules {
    action      = "challenge"
    description = "Challenge suspicious behavior"
    expression  = "(cf.threat_score > 30) or (cf.bot_management.score < 30)"
  }

  rules {
    action      = "log"
    description = "Log all access attempts to restricted paths"
    expression  = "(http.request.uri.path contains \"/access\") or (http.request.uri.path contains \"/governance\")"
  }
}

# REFINED: Cache rules for WASM optimization
resource "cloudflare_ruleset" "cache_rules" {
  zone_id     = cloudflare_zone.main.id
  name        = "Asset Caching Strategy"
  description = "Optimizes caching for static assets and WASM modules"
  kind        = "zone"
  phase       = "http_request_cache_settings"

  rules {
    action = "set_cache_settings"
    description = "Aggressive caching for static assets except WASM"
    expression = "(http.request.uri.path matches \"\\.(css|js|svg|jpg|png|webp)$\") and not (http.request.uri.path matches \"\\.wasm$\")"
    action_parameters {
      cache = true
      edge_ttl {
        mode = "override_origin"
        default = 86400  # 24 hours
      }
      browser_ttl {
        mode = "override_origin"
        default = 3600   # 1 hour
      }
    }
  }

  rules {
    action = "set_cache_settings"
    description = "Conservative caching for WASM modules"
    expression = "(http.request.uri.path matches \"\\.wasm$\")"
    action_parameters {
      cache = true
      edge_ttl {
        mode = "override_origin"
        default = 3600   # 1 hour
      }
      browser_ttl {
        mode = "respect_origin"
      }
    }
  }
}

# Rate Limiting
resource "cloudflare_rate_limit" "api_protection" {
  zone_id   = cloudflare_zone.main.id
  threshold = 100
  period    = 60
  match {
    request {
      url_pattern = "${var.domain}/*"
    }
  }
  action {
    mode    = "challenge"
    timeout = 3600
  }
}

# Analytics Engine
resource "cloudflare_workers_kv_namespace" "session_logs" {
  account_id = var.cloudflare_account_id
  title      = "session-surveillance-logs"
}

output "zone_id" {
  value       = cloudflare_zone.main.id
  description = "Cloudflare zone identifier"
}

output "nameservers" {
  value       = cloudflare_zone.main.name_servers
  description = "Authoritative nameservers"
}

output "dnssec_status" {
  value       = cloudflare_zone_dnssec.main.status
  description = "DNSSEC validation status"
}
```

---

## PART VIII: DEPLOYMENT CHECKLIST (REFINED)

### 8.1 Pre-Deployment Verification

```bash
# 1. Build WASM module
cd src/rust
wasm-pack build --target web --out-dir ../../src/wasm
cd ../..

# 2. Verify WASM integration
npm run dev
# Check console for "SESSION ENGINE INITIALIZED"
# Check Network tab for hashed WASM file

# 3. Build production bundle
npm run build

# 4. Verify build artifacts
ls -lh dist/
# Ensure WASM files are hashed: session_engine.[hash].wasm

# 5. Test production build locally
npm run preview
```

### 8.2 Infrastructure Deployment

```bash
# 1. Set R2 credentials
export AWS_ACCESS_KEY_ID="<R2_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<R2_SECRET_ACCESS_KEY>"
export AWS_ENDPOINT_URL="https://<ACCOUNT_ID>.r2.cloudflarestorage.com"

# 2. Initialize Terraform with R2 backend
cd terraform
terraform init

# 3. Review execution plan
terraform plan -out=tfplan

# 4. Verify critical resources
# - DNSSEC is enabled
# - Geo-blocking rules are present
# - Cache rules include WASM optimization
# - Rate limiting is configured

# 5. Apply infrastructure changes
terraform apply tfplan

# 6. Verify DNS propagation
dig thenash.group +dnssec
```

### 8.3 Site Deployment

```bash
# 1. Deploy to Cloudflare Pages
npx wrangler pages deploy dist --project-name=the-nash-group

# 2. Verify deployment
curl -I https://thenash.group
# Check headers for HSTS, CSP, etc.

# 3. Test session initialization
# Open site in browser
# Check console for compliance logging
# Verify session monitor displays correctly

# 4. Test WASM loading
# Check Network tab
# Verify session_engine.[hash].wasm loads successfully
# Check console for "SESSION ENGINE INITIALIZED"
```

### 8.4 Security Verification

```bash
# 1. Test DNSSEC
dig thenash.group +dnssec @1.1.1.1

# 2. Test geo-blocking (using VPN/proxy)
curl -I https://thenash.group -x socks5://proxy-in-blocked-country

# 3. Test WAF rules
curl https://thenash.group -A "sqlmap/1.0"
# Should return 403

# 4. Test rate limiting
for i in {1..150}; do curl -I https://thenash.group; done
# Should trigger challenge after ~100 requests

# 5. Security header audit
curl -I https://thenash.group | grep -E "Strict-Transport|X-Frame|Content-Security"
```

---

## PART IX: OPERATIONAL METRICS (REFINED)

### 9.1 Performance Targets

```
Lighthouse Score:        100/100/100/100
First Contentful Paint:  < 400ms
Time to Interactive:     < 600ms
Total Bundle Size:       < 40KB (gzipped)
WASM Module Size:        < 15KB
Session Init Time:       < 100ms
WASM Load Time:         < 50ms
```

### 9.2 Security Metrics

```
CSP Violations:          0
DNSSEC Status:          Validated
TLS Version:            1.3 minimum
Security Headers:        A+ rating (securityheaders.com)
WAF Rule Coverage:       100%
Geo-Block Effectiveness: > 99%
Rate Limit Triggers:     < 10/day (legitimate traffic)
```

### 9.3 Monitoring Dashboard

```bash
# Create monitoring dashboard in Cloudflare
# Metrics to track:
- Request volume by country
- WAF rule triggers
- Rate limit challenges issued
- WASM load success rate
- Session initialization time
- Console access frequency (via custom analytics)
```

---

## PART X: POST-DEPLOYMENT VALIDATION

### 10.1 Functional Tests

```javascript
// tests/session-engine.test.js
import { SessionManager } from '../src/lib/session-engine';

describe('Session Engine', () => {
  test('initializes with WASM module', async () => {
    const manager = new SessionManager();
    const state = await manager.initialize();

    expect(state.id).toMatch(/^\d{4}-[A-Z]+$/);
    expect(state.clearance).toMatch(/^(ALPHA|BETA|GAMMA|DELTA)$/);
    expect(state.jurisdiction).toBeTruthy();
  });

  test('generates consistent session IDs', async () => {
    const manager = new SessionManager();
    await manager.initialize();
    const state1 = manager.getState();

    // ID should remain stable during session
    await new Promise(resolve => setTimeout(resolve, 100));
    const state2 = manager.getState();

    expect(state1.id).toBe(state2.id);
  });
});
```

### 10.2 Security Tests

```bash
# Test geo-blocking
curl -I https://thenash.group \
  -H "CF-IPCountry: CN" \
  --resolve thenash.group:443:1.1.1.1

# Expected: 403 Forbidden

# Test malicious user agent
curl -I https://thenash.group \
  -A "sqlmap/1.0"

# Expected: 403 Forbidden

# Test DNSSEC
dig thenash.group +dnssec @1.1.1.1 | grep "ad"

# Expected: flags: qr rd ra ad
```

### 10.3 Performance Tests

```bash
# Lighthouse audit
npx lighthouse https://thenash.group \
  --output json \
  --output-path ./lighthouse-report.json

# WebPageTest
# https://www.webpagetest.org/
# Run tests from multiple global locations

# WASM load time verification
curl -w "@curl-format.txt" -o /dev/null -s \
  https://thenash.group/_astro/session_engine.[hash].wasm
```

---

## PART XI: MAINTENANCE PROCEDURES

### 11.1 Weekly Tasks

```bash
# 1. Review WAF logs
# Cloudflare Dashboard > Security > Events

# 2. Check DNSSEC status
dig thenash.group +dnssec

# 3. Review rate limit triggers
# Cloudflare Dashboard > Security > Rate Limiting

# 4. Verify WASM cache hit rate
# Cloudflare Dashboard > Analytics > Cache
```

### 11.2 Monthly Tasks

```bash
# 1. Update dependencies
npm update
cd src/rust && cargo update && cd ../..

# 2. Rebuild WASM module
cd src/rust
wasm-pack build --target web --out-dir ../../src/wasm
cd ../..

# 3. Run full test suite
npm test

# 4. Security audit
npm audit
cargo audit

# 5. Performance baseline
npx lighthouse https://thenash.group --output json
```

### 11.3 Quarterly Tasks

```bash
# 1. Review and update geo-blocking rules
# terraform/cloudflare.tf - Update blocked countries if needed

# 2. Review Terraform state
cd terraform
terraform plan
# Ensure no unexpected drift

# 3. Backup state file
aws s3 cp s3://nash-group-terraform-state/citadel/production.tfstate \
  ./backups/production-$(date +%Y%m%d).tfstate \
  --endpoint-url=$AWS_ENDPOINT_URL

# 4. Review and update CSP headers if needed
```

---

## PART XII: TROUBLESHOOTING GUIDE

### 12.1 WASM Module Not Loading

**Symptom:** Console shows WASM import error

**Solution:**
```bash
# 1. Verify WASM file exists
ls -lh dist/_astro/session_engine.*.wasm

# 2. Check MIME type configuration in wrangler.toml
# Add to wrangler.toml:
[[headers]]
pattern = "*.wasm"
headers = { "Content-Type" = "application/wasm" }

# 3. Rebuild with verbose output
npm run build -- --verbose
```

### 12.2 Session Monitor Not Updating

**Symptom:** Session display shows "INITIALIZING" indefinitely

**Solution:**
```javascript
// Check browser console for errors
// Common issues:
// 1. WASM not loaded - see above
// 2. JavaScript disabled
// 3. CSP blocking execution

// Test WASM manually:
import('../wasm/session_engine.js').then(wasm => {
  wasm.default().then(() => {
    const engine = new wasm.SessionEngine();
    console.log('Engine:', engine);
  });
});
```

### 12.3 Geo-Blocking Not Working

**Symptom:** Blocked countries can access site

**Solution:**
```bash
# 1. Verify firewall rule is active
cd terraform
terraform show | grep -A 10 "cloudflare_firewall_rule.geo_block"

# 2. Check rule priority
# Ensure geo_block rule has priority = 1

# 3. Test with Cloudflare API
curl -X GET "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/firewall/rules" \
  -H "Authorization: Bearer ${CF_API_TOKEN}"
```

---

## CONCLUSION

This refined implementation guide incorporates all technical advisories to ensure the deployment matches the institutional severity of the specification:

**Key Refinements:**
1. ✅ WASM integrated into build pipeline (vite-plugin-wasm)
2. ✅ State sovereignty via Cloudflare R2
3. ✅ Institutional cursor directives
4. ✅ IBM Plex typeface for bureaucratic authority
5. ✅ Refined jurisdiction codes (NYC/ZERO)
6. ✅ Enhanced console honeypot
7. ✅ DNSSEC enforcement
8. ✅ Geo-blocking implementation
9. ✅ Optimized cache rules for WASM

**Status:** APPROVED FOR IMPLEMENTATION
**Next Action:** Execute Phase 1 (Project Initialization)

════════════════════════════════════════════════
© THE NASH GROUP. ALL RIGHTS RESERVED.
SPECIFICATION v2.1 - TECHNICAL REFINEMENTS INCORPORATED
════════════════════════════════════════════════
