# The Nash Group Corporate Site
## Institutional Architecture Specification (v2.0 - November 2025)

> "Operations are conducted with precision. Continuity is enforced."

---

## DESIGN PHILOSOPHY: HERMETIC INSTITUTIONALISM

### The Transformation
- **Was:** "Stealth Wealth" - appears simple, secretly complex
- **Now:** "Institutional Authority" - appears austere, demonstrably powerful
- **Core Principle:** The Nash Group is not a company; it is an Institution with generational continuity

### The Visual System: Geometric Authority

```
Core: Astro 4.x (SSG with selective hydration)
Logic: TypeScript + Rust/WASM for session management
Styling: Vanilla CSS - Strict geometric grid system
Edge: Cloudflare Pages + Workers
Analytics: Custom surveillance implementation
Security: Institutional-grade CSP headers
IaC: Terraform for absolute control
```

**Why This Stack:**
- **Astro**: Zero client JS by default = perfect for institutional minimalism
- **Rust/WASM**: Enterprise-grade session management (not overkill, expected)
- **Cloudflare**: Global enforcement infrastructure
- **No frameworks**: Institutions don't follow trends

---

## PART I: PROJECT INITIALIZATION

### 1.1 Create Project Structure

```bash
# Initialize Astro project
npm create astro@latest the-nash-group -- --template minimal --typescript strict --no-install

cd the-nash-group

# Install dependencies
npm install

# Add required packages
npm install -D @astrojs/cloudflare wrangler terser

# Rust toolchain for session management
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup target add wasm32-unknown-unknown
cargo install wasm-pack
```

### 1.2 Project Structure

```
the-nash-group/
├── src/
│   ├── components/
│   │   ├── SessionMonitor.astro
│   │   ├── StatusIndicator.astro
│   │   ├── LegalFooter.astro
│   │   └── AccessNotice.astro
│   ├── layouts/
│   │   └── InstitutionalLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── capabilities.astro
│   │   ├── governance.astro
│   │   ├── access.astro
│   │   └── 404.astro
│   ├── lib/
│   │   ├── session-engine.ts
│   │   └── surveillance.ts
│   ├── styles/
│   │   └── institutional.css
│   └── rust/
│       ├── Cargo.toml
│       └── src/
│           └── lib.rs
├── public/
│   ├── favicon.svg
│   └── robots.txt
├── terraform/
│   ├── main.tf
│   ├── cloudflare.tf
│   └── variables.tf
├── astro.config.mjs
└── tsconfig.json
```

---

## PART II: THE SESSION ENGINE (INSTITUTIONAL GRADE)

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

[profile.release]
opt-level = "z"
lto = true
```

### 2.2 `src/rust/src/lib.rs`

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
                    jurisdiction: "SCOT".to_string(),
                },
                ContinuityAnchor {
                    epoch: 1622,
                    designation: "BETA".to_string(),
                    jurisdiction: "EAST".to_string(),
                },
                ContinuityAnchor {
                    epoch: 1746,
                    designation: "GAMMA".to_string(),
                    jurisdiction: "SCOT".to_string(),
                },
                ContinuityAnchor {
                    epoch: 1985,
                    designation: "DELTA".to_string(),
                    jurisdiction: "USNR".to_string(),
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
}

#[wasm_bindgen(start)]
pub fn initialize() {
    web_sys::console::log_1(&"SESSION ENGINE INITIALIZED".into());
}
```

### 2.3 Build WASM Module

```bash
cd src/rust
wasm-pack build --target web --out-dir ../../public/wasm
cd ../..
```

---

## PART III: CORE TYPESCRIPT LOGIC

### 3.1 `src/lib/session-engine.ts`

```typescript
/**
 * Nash Group Session Management System
 * Implements institutional-grade session tracking and access determination
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
    // Load WASM session engine
    const wasm = await import('/wasm/session_engine.js');
    await wasm.default();
    this.wasmEngine = new wasm.SessionEngine();

    // Generate session identifier
    const timestamp = Date.now();
    this.state.id = this.wasmEngine.generateSessionId(timestamp);

    // Determine access clearance
    const entropy = await this.measureBehavioralEntropy();
    this.state.clearance = this.wasmEngine.determineAccessLevel(entropy);

    // Establish jurisdiction
    await this.establishJurisdiction();

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

  private async establishJurisdiction(): Promise<void> {
    try {
      const response = await fetch('/api/geolocation');
      const data = await response.json();
      this.state.jurisdiction = `${data.country}/${data.region}`;
    } catch {
      this.state.jurisdiction = 'UNDETERMINED';
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

### 3.2 `src/lib/surveillance.ts`

```typescript
/**
 * Compliance and Monitoring System
 * Implements institutional observation protocols
 */

export function initializeComplianceLogging(): void {
  console.clear();

  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #000000; font-family: monospace; font-size: 12px;'
  );
  console.log(
    '%c  THE NASH GROUP',
    'color: #000000; font-family: monospace; font-size: 14px; font-weight: bold;'
  );
  console.log(
    '%c  ACCESS LOGGED',
    'color: #000000; font-family: monospace; font-size: 12px;'
  );
  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #000000; font-family: monospace; font-size: 12px;'
  );
  console.log('');
  console.log(
    '%c  SYSTEM STATUS:',
    'color: #000000; font-family: monospace; font-size: 12px;'
  );
  console.log(
    '%c  ● COVENANT .......... ENFORCED',
    'color: #00FF41; font-family: monospace; font-size: 11px;'
  );
  console.log(
    '%c  ● CITADEL ........... LOCKED',
    'color: #00FF41; font-family: monospace; font-size: 11px;'
  );
  console.log(
    '%c  ● NEXUS ............. ACTIVE',
    'color: #00FF41; font-family: monospace; font-size: 11px;'
  );
  console.log('');
  console.log(
    '%c  Developer tool access has been recorded.',
    'color: #000000; font-family: monospace; font-size: 11px; font-style: italic;'
  );
  console.log(
    '%c  Unauthorized reproduction of schemas is prohibited.',
    'color: #000000; font-family: monospace; font-size: 11px; font-style: italic;'
  );
  console.log(
    '%c ════════════════════════════════════════════════',
    'color: #000000; font-family: monospace; font-size: 12px;'
  );
}

export function detectComplianceViolations(): void {
  // Monitor for suspicious behavior patterns
  let suspiciousActivity = 0;

  // Rapid clicking detection
  let clickCount = 0;
  document.addEventListener('click', () => {
    clickCount++;
    setTimeout(() => clickCount = 0, 1000);
    if (clickCount > 10) {
      suspiciousActivity++;
      console.warn('%c COMPLIANCE ALERT: Anomalous interaction pattern detected',
        'color: #FF0000; font-weight: bold;');
    }
  });

  // Console inspection detection
  const threshold = 160;
  window.addEventListener('resize', () => {
    if (
      window.outerHeight - window.innerHeight > threshold ||
      window.outerWidth - window.innerWidth > threshold
    ) {
      console.log('%c NOTICE: Developer tools active. Session logged.',
        'color: #000000; font-style: italic;');
    }
  });
}
```

---

## PART IV: STYLING - GEOMETRIC AUTHORITY

### 4.1 `src/styles/institutional.css`

```css
/**
 * The Nash Group Institutional Stylesheet
 *
 * Design System: Hermetic Institutionalism
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
   DESIGN TOKENS
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

  /* Typography System */
  --font-primary: -apple-system, BlinkMacSystemFont, "Segoe UI",
                  "Helvetica Neue", Arial, sans-serif;
  --font-mono: "SF Mono", "Consolas", "Liberation Mono",
               "Courier New", monospace;

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
  cursor: pointer;
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
}
```

---

## PART V: ASTRO COMPONENTS

### 5.1 `src/layouts/InstitutionalLayout.astro`

```astro
---
interface Props {
  title: string;
  description?: string;
}

const {
  title,
  description = "Operations are conducted with precision."
} = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content={description} />
    <meta name="author" content="The Nash Group" />

    <title>{title} | The Nash Group</title>

    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="stylesheet" href="/src/styles/institutional.css" />

    <!-- Security Headers -->
    <meta http-equiv="Content-Security-Policy" content="
      default-src 'self';
      script-src 'self' 'wasm-unsafe-eval';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data:;
      font-src 'self';
      connect-src 'self';
    ">
  </head>
  <body>
    <!--
      UNIT: THE-NASH-GROUP/CORPORATE-INTERFACE
      STATUS: ACTIVE
      CLASSIFICATION: PUBLIC
    -->

    <header>
      <div class="logo">THE NASH GROUP</div>
      <div></div>
      <div class="session-display" id="session-display">
        SESSION: INITIALIZING
      </div>
    </header>

    <main class="container">
      <slot />
    </main>

    <footer>
      <div id="session-monitor">
SESSION: ────────────
DURATION: 00:00:00
CLEARANCE: ────
REQUESTS: 0
STATUS: INITIALIZING
      </div>

      <hr class="divider" />

      <div>
        <p>© THE NASH GROUP. ALL RIGHTS RESERVED.</p>
        <p style="margin-top: var(--space-2);">
          Access to this system is monitored and recorded.
          Unauthorized reproduction of proprietary schemas is prohibited.
          By continuing to navigate this interface, you acknowledge
          awareness of surveillance protocols and consent to information
          collection as defined in operational directives.
        </p>
      </div>
    </footer>

    <script>
      import { SessionManager } from '../lib/session-engine';
      import { initializeComplianceLogging, detectComplianceViolations } from '../lib/surveillance';

      // Initialize compliance logging
      initializeComplianceLogging();
      detectComplianceViolations();

      // Initialize session management
      const manager = new SessionManager();
      manager.initialize().then((state) => {
        const display = document.getElementById('session-display');
        if (display) {
          display.textContent = `SESSION: ${state.id}`;
        }

        // Update monitor every second
        setInterval(() => {
          manager.updateDisplay();
        }, 1000);
      });
    </script>
  </body>
</html>
```

### 5.2 `src/components/AccessNotice.astro`

```astro
---
// Displays on first session initialization
---

<div class="access-notice" id="access-notice">
  <pre>
┌──────────────────────────────────────────┐
│ ACCESS LOGGED                            │
│                                          │
│ Your session has been initialized and    │
│ assigned a unique identifier.            │
│                                          │
│ All interactions with this system are    │
│ recorded for compliance and security     │
│ purposes.                                │
│                                          │
│ Continued use constitutes acceptance     │
│ of monitoring protocols.                 │
└──────────────────────────────────────────┘
  </pre>
  <button onclick="this.parentElement.style.display='none'">
    ACKNOWLEDGED
  </button>
</div>

<script>
  const hasAcknowledged = sessionStorage.getItem('access-acknowledged');
  if (hasAcknowledged) {
    const notice = document.getElementById('access-notice');
    if (notice) notice.style.display = 'none';
  } else {
    sessionStorage.setItem('access-acknowledged', 'true');
  }
</script>
```

### 5.3 `src/components/StatusIndicator.astro`

```astro
---
interface Props {
  label: string;
  status: 'active' | 'alert' | 'inactive';
}

const { label, status } = Astro.props;
---

<div class="status-grid">
  <span class={`status-indicator ${status === 'alert' ? 'alert' : ''}`}></span>
  <span>{label}</span>
</div>
```

---

## PART VI: PAGES

### 6.1 `src/pages/index.astro`

```astro
---
import InstitutionalLayout from '../layouts/InstitutionalLayout.astro';
import AccessNotice from '../components/AccessNotice.astro';
import StatusIndicator from '../components/StatusIndicator.astro';
---

<InstitutionalLayout title="Home">
  <AccessNotice />

  <h1>The Nash Group</h1>

  <p>
    The Nash Group maintains operational continuity across
    infrastructure, governance, and systems architecture.
    Operations are conducted according to established protocols.
  </p>

  <div class="status-grid" style="margin-top: var(--space-6);">
    <StatusIndicator label="COVENANT .......... ENFORCED" status="active" />
    <StatusIndicator label="CITADEL ........... LOCKED" status="active" />
    <StatusIndicator label="NEXUS ............. ACTIVE" status="active" />
  </div>

  <h2>Access Points</h2>

  <table>
    <thead>
      <tr>
        <th>Unit</th>
        <th>Classification</th>
        <th>Access</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Capabilities</td>
        <td>PUBLIC</td>
        <td><a href="/capabilities">View</a></td>
      </tr>
      <tr>
        <td>Governance</td>
        <td>PUBLIC</td>
        <td><a href="/governance">View</a></td>
      </tr>
      <tr>
        <td>Access Protocols</td>
        <td>RESTRICTED</td>
        <td><a href="/access">View</a></td>
      </tr>
    </tbody>
  </table>

  <div class="legal">
    <p><strong>NOTICE:</strong></p>
    <p>
      This organization operates under a governance framework
      designed for multi-generational continuity. Access to
      certain resources requires appropriate clearance levels.
    </p>
  </div>
</InstitutionalLayout>
```

### 6.2 `src/pages/capabilities.astro`

```astro
---
import InstitutionalLayout from '../layouts/InstitutionalLayout.astro';
---

<InstitutionalLayout
  title="Capabilities"
  description="Operational capabilities maintained across domains."
>
  <h1>Capabilities</h1>

  <p>
    Operational capabilities are maintained across the following domains.
    Specific implementations are disclosed on a need-to-know basis.
  </p>

  <h2>Domain Overview</h2>

  <table>
    <thead>
      <tr>
        <th>Domain</th>
        <th>Status</th>
        <th>Classification</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Infrastructure Synthesis</td>
        <td>OPERATIONAL</td>
        <td>L2</td>
      </tr>
      <tr>
        <td>Governance Architecture</td>
        <td>OPERATIONAL</td>
        <td>L1</td>
      </tr>
      <tr>
        <td>Temporal Systems</td>
        <td>OPERATIONAL</td>
        <td>L3</td>
      </tr>
      <tr>
        <td>Organizational Topology</td>
        <td>OPERATIONAL</td>
        <td>L2</td>
      </tr>
    </tbody>
  </table>

  <h2>Operational Methodology</h2>

  <ul>
    <li>Multi-generational continuity planning</li>
    <li>Cumulative experience aggregation</li>
    <li>Strategic convergence protocols</li>
    <li>Singular governance enforcement</li>
  </ul>

  <div class="legal">
    <p><strong>CLEARANCE REQUIREMENT:</strong></p>
    <p>
      Detailed capability specifications require Beta clearance or higher.
      Unauthorized inquiries are logged and may result in access restriction.
    </p>
  </div>
</InstitutionalLayout>
```

### 6.3 `src/pages/governance.astro`

```astro
---
import InstitutionalLayout from '../layouts/InstitutionalLayout.astro';
---

<InstitutionalLayout
  title="Governance"
  description="Operational framework and governance protocols."
>
  <h1>Governance</h1>

  <p>
    All operations are conducted according to The Covenant,
    the constitutional framework establishing organizational
    principles and operational directives.
  </p>

  <h2>Governing Documents</h2>

  <table>
    <thead>
      <tr>
        <th>Document</th>
        <th>Classification</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>The Covenant</td>
        <td>RESTRICTED</td>
        <td>ENFORCED</td>
      </tr>
      <tr>
        <td>The Citadel</td>
        <td>CLASSIFIED</td>
        <td>LOCKED</td>
      </tr>
      <tr>
        <td>Reference Archives</td>
        <td>INTERNAL</td>
        <td>ACTIVE</td>
      </tr>
    </tbody>
  </table>

  <h2>Operational Hierarchy</h2>

  <ul>
    <li>Observability & Audit Division (Watchers)</li>
    <li>Technical Authority (Mentors)</li>
    <li>Operational Personnel (Immortals)</li>
  </ul>

  <h2>Governance Principles</h2>

  <p>
    The organizational framework is designed for indefinite continuity.
    Core principles include:
  </p>

  <ul>
    <li>Singular source of truth</li>
    <li>Cumulative knowledge transfer</li>
    <li>Mandatory observability</li>
    <li>Zero-trust architecture</li>
    <li>Immutable audit trails</li>
  </ul>

  <div class="legal">
    <p><strong>ACCESS RESTRICTION:</strong></p>
    <p>
      Full governance documentation is available only to authorized
      personnel. Requests for elevated access must be submitted
      through approved channels and are subject to review.
    </p>
  </div>
</InstitutionalLayout>
```

### 6.4 `src/pages/404.astro`

```astro
---
import InstitutionalLayout from '../layouts/InstitutionalLayout.astro';
---

<InstitutionalLayout title="Resource Not Found">
  <h1>Error 404</h1>

  <p>
    The requested resource could not be located within the
    accessible namespace.
  </p>

  <h2>Possible Causes</h2>

  <table>
    <thead>
      <tr>
        <th>Code</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>ERR_CLEARANCE</td>
        <td>Resource requires elevated clearance</td>
      </tr>
      <tr>
        <td>ERR_NAMESPACE</td>
        <td>Resource moved to restricted namespace</td>
      </tr>
      <tr>
        <td>ERR_RETIRED</td>
        <td>Resource has been retired from active service</td>
      </tr>
      <tr>
        <td>ERR_INVALID</td>
        <td>Resource identifier is malformed</td>
      </tr>
    </tbody>
  </table>

  <p style="margin-top: var(--space-5);">
    <a href="/">← Return to home</a>
  </p>
</InstitutionalLayout>
```

---

## PART VII: DEPLOYMENT CONFIGURATION

### 7.1 `astro.config.mjs`

```javascript
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'hybrid',
  adapter: cloudflare({
    mode: 'directory',
    functionPerRoute: false
  }),
  vite: {
    build: {
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: false
        },
        format: {
          comments: false
        }
      }
    }
  }
});
```

### 7.2 `wrangler.toml`

```toml
name = "the-nash-group"
compatibility_date = "2025-11-01"
pages_build_output_dir = "./dist"

[env.production]
route = "thenash.group/*"

[observability]
enabled = true

[[analytics_engine_datasets]]
binding = "SESSION_ANALYTICS"
```

### 7.3 `terraform/cloudflare.tf`

```hcl
# Institutional Infrastructure Configuration

terraform {
  required_version = ">= 1.6"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }

  backend "remote" {
    organization = "the-nash-group"
    workspaces {
      name = "citadel-production"
    }
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

# Zone Configuration
resource "cloudflare_zone" "main" {
  account_id = var.cloudflare_account_id
  zone       = var.domain
  plan       = "business"
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
      (http.user_agent contains "masscan")
    EOT
  }

  rules {
    action      = "challenge"
    description = "Challenge rapid sequential requests"
    expression  = "(cf.threat_score > 30)"
  }

  rules {
    action      = "log"
    description = "Log all access attempts"
    expression  = "(http.request.uri.path contains \"/access\")"
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
```

---

## PART VIII: BUILD & DEPLOYMENT

### 8.1 Local Development

```bash
# Install dependencies
npm install

# Build WASM session engine
cd src/rust
wasm-pack build --target web --out-dir ../../public/wasm
cd ../..

# Run development server
npm run dev
```

### 8.2 Production Build

```bash
# Build for production
npm run build

# Verify build
npm run preview
```

### 8.3 Deploy to Cloudflare

```bash
# Authenticate
npx wrangler login

# Deploy to Cloudflare Pages
npx wrangler pages deploy dist
```

### 8.4 Infrastructure Deployment

```bash
cd terraform

# Initialize Terraform
terraform init

# Review execution plan
terraform plan -out=tfplan

# Apply infrastructure changes (requires approval)
terraform apply tfplan
```

---

## PART IX: OPERATIONAL METRICS

### Performance Targets

```
Lighthouse Score:        100/100/100/100
First Contentful Paint:  < 400ms
Time to Interactive:     < 600ms
Total Bundle Size:       < 40KB (gzipped)
WASM Module:            < 15KB
Session Init Time:       < 100ms
```

### Security Requirements

```
CSP Violations:          0
HSTS Compliance:         Enforced
TLS Version:            1.3 minimum
Security Headers:        A+ rating
WAF Rule Coverage:       100%
```

### Monitoring Checklist

```markdown
- [ ] Review session analytics weekly
- [ ] Audit WAF logs for anomalies
- [ ] Verify Terraform state integrity
- [ ] Check CSP violation reports
- [ ] Validate WASM performance metrics
- [ ] Review access pattern distributions
```

---

## CONCLUSION

This specification implements Hermetic Institutionalism for The Nash Group's public interface:

**Technical Sophistication:**
- Enterprise-grade Rust/WASM session management
- Zero-trust security architecture
- Global edge distribution
- Comprehensive monitoring

**Institutional Aesthetic:**
- Geometric authority in visual design
- Informational austerity in content
- Bureaucratic intimidation in tone
- Temporal disconnection in presentation

**Lore Translation:**
- Highlander concepts → Corporate antiquity
- Fantasy terms → Asset management language
- Easter eggs → Compliance protocols

The result: A site that appears austere but demonstrates institutional permanence and technical authority.

**Status:** SPECIFICATION COMPLETE
**Next Phase:** GOVERNANCE RATIFICATION
