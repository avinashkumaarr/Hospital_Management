import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Lucide script in head if not present
if "lucide@latest" not in content:
    content = content.replace(
        '  <link rel="stylesheet" href="/static/css/styles.css" />',
        '  <!-- Lucide Icons -->\n  <script src="https://unpkg.com/lucide@latest"></script>\n  <link rel="stylesheet" href="/static/css/styles.css" />'
    )

# 2. Define Landing and Login views
landing_and_login = """
  <!-- ====================================================================
       VIEW 1: MODERN LANDING HOMEPAGE (#view-landing)
       ==================================================================== -->
  <div id="view-landing" class="app-view active">
    <!-- Modern Sticky Navigation Bar -->
    <nav class="landing-nav">
      <div class="landing-nav-container">
        <a href="#hero" class="landing-brand">
          <div class="landing-brand-icon">⚕</div>
          <span>MediLink<span style="color:var(--primary); font-weight:800">.</span></span>
        </a>

        <ul class="landing-nav-links" id="landing-nav-links">
          <li><a href="#hero" onclick="toggleMobileMenu()">Home</a></li>
          <li><a href="#features" onclick="toggleMobileMenu()">Features</a></li>
          <li><a href="#how-it-works" onclick="toggleMobileMenu()">How It Works</a></li>
          <li><a href="#benefits" onclick="toggleMobileMenu()">Benefits</a></li>
          <li><a href="#preview" onclick="toggleMobileMenu()">Preview</a></li>
          <li><a href="#contact" onclick="toggleMobileMenu()">Contact</a></li>
        </ul>

        <div class="landing-nav-actions">
          <button class="btn-icon" onclick="toggleTheme()" title="Toggle Dark/Light Theme">🌓</button>
          <button class="btn btn-secondary btn-sm" onclick="switchView('login')">Sign In</button>
          <button class="btn btn-primary btn-sm" onclick="handleGetStarted()">Get Started</button>
          <button class="hamburger-btn" onclick="toggleMobileMenu()" aria-label="Toggle navigation menu">☰</button>
        </div>
      </div>
    </nav>

    <!-- Premium Hero Section -->
    <section class="hero-section" id="hero">
      <div class="hero-content">
        <div class="hero-badge">
          <span>●</span>
          <span>Enterprise Healthcare Platform v3.0</span>
        </div>
        <h1 class="hero-title">
          Smarter Healthcare.<br><span>Seamlessly Connected.</span>
        </h1>
        <p class="hero-subtitle">
          One intelligent platform to manage patients, medical records, appointments, hospital operations, and healthcare insights — all in one place.
        </p>
        <div class="hero-cta-group">
          <button class="btn btn-primary" onclick="handleGetStarted()" style="padding:0.8rem 1.6rem; font-size:1rem; font-weight:700;">
            Get Started →
          </button>
          <a href="#features" class="btn btn-secondary" style="padding:0.8rem 1.6rem; font-size:1rem; font-weight:600; text-decoration:none;">
            Explore Features
          </a>
        </div>
        <div class="hero-trust-row">
          <div class="hero-trust-item">
            <span class="hero-trust-num">6+</span>
            <span class="hero-trust-lbl">Tier-1 Nodes</span>
          </div>
          <div class="hero-trust-item">
            <span class="hero-trust-num">100%</span>
            <span class="hero-trust-lbl">CDSS Safety</span>
          </div>
          <div class="hero-trust-item">
            <span class="hero-trust-num">11</span>
            <span class="hero-trust-lbl">DBMS Entities</span>
          </div>
          <div class="hero-trust-item">
            <span class="hero-trust-num">Zero</span>
            <span class="hero-trust-lbl">Data Collisions</span>
          </div>
        </div>
      </div>

      <!-- Right Visual: CSS/SVG Hospital Dashboard Preview -->
      <div class="hero-visual-card">
        <div class="mock-window-bar">
          <span class="mock-dot"></span>
          <span class="mock-dot"></span>
          <span class="mock-dot"></span>
          <span style="font-size:0.75rem; color:var(--text-dim); margin-left:8px; font-family:var(--font-mono)">medilink.hospital/command-center</span>
        </div>
        <div class="mock-grid-kpis">
          <div class="mock-kpi">
            <div class="mock-kpi-title">Active Inpatients</div>
            <div class="mock-kpi-val" style="color:var(--primary)">284 / 320</div>
            <div style="font-size:0.7rem; color:var(--success); margin-top:2px;">● 88.7% Bed Occupancy</div>
          </div>
          <div class="mock-kpi">
            <div class="mock-kpi-title">OPD Live Queue</div>
            <div class="mock-kpi-val" style="color:var(--teal)">18 Waiting</div>
            <div style="font-size:0.7rem; color:var(--text-muted); margin-top:2px;">Avg Wait: 12 min</div>
          </div>
        </div>
        <!-- Illustrative Patient Encounter Card -->
        <div class="mock-timeline-item" style="border-left:3px solid var(--primary); background:var(--bg-alt);">
          <div style="font-size:1.1rem;">🩺</div>
          <div style="flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong>Cardiology Consultation</strong>
              <span class="badge badge-success" style="font-size:0.65rem;">Completed</span>
            </div>
            <div style="font-size:0.72rem; color:var(--text-muted);">Dr. Anita Verma • Verified Digital Rx Slip Issued</div>
          </div>
        </div>
        <div class="mock-timeline-item" style="border-left:3px solid var(--danger); background:var(--bg-alt);">
          <div style="font-size:1.1rem;">🚨</div>
          <div style="flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong>Trauma Triage ESI-1</strong>
              <span class="badge badge-danger" style="font-size:0.65rem;">Immediate</span>
            </div>
            <div style="font-size:0.72rem; color:var(--text-muted);">Red Bay Allocated • Crash Cart Ready</div>
          </div>
        </div>
        <div class="mock-timeline-item" style="border-left:3px solid var(--teal); background:var(--bg-alt);">
          <div style="font-size:1.1rem;">🧪</div>
          <div style="flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong>Digital Lab Diagnostics</strong>
              <span class="badge badge-info" style="font-size:0.65rem;">Verified</span>
            </div>
            <div style="font-size:0.72rem; color:var(--text-muted);">Automated Abnormal Value CDSS Trigger</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section (10 Cards with Lucide Icons) -->
    <section class="landing-section" id="features">
      <div class="section-header">
        <span class="section-tag">Clinical Intelligence &amp; Operations</span>
        <h2 class="section-title">Comprehensive Hospital Management Suite</h2>
        <p class="section-desc">
          Engineered for clinical precision, seamless patient flow, and institutional interoperability across modern tertiary care networks.
        </p>
      </div>

      <div class="features-grid">
        <!-- 1. Unified Patient Records -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="file-heart"></i>
          </div>
          <h3 class="feature-name">Unified Patient Records</h3>
          <p class="feature-desc">
            Single longitudinal EHR linked by 12-digit Aadhaar UID. Full encounter timelines, past diagnoses, and treatment notes across multiple hospital nodes.
          </p>
        </div>

        <!-- 2. Smart Appointment Scheduling -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="calendar-check"></i>
          </div>
          <h3 class="feature-name">Smart Appointment Scheduling</h3>
          <p class="feature-desc">
            Seamless multi-specialty slot booking with doctor availability validation, conflict prevention, real-time rescheduling, and automated status tracking.
          </p>
        </div>

        <!-- 3. Digital Prescriptions -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="pill"></i>
          </div>
          <h3 class="feature-name">Digital Prescriptions</h3>
          <p class="feature-desc">
            Clinical prescription generation with drug interaction checking, allergy alerts, dosage safety, and official printable PDF/hospital slip exports.
          </p>
        </div>

        <!-- 4. Doctor Management -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="stethoscope"></i>
          </div>
          <h3 class="feature-name">Doctor Management</h3>
          <p class="feature-desc">
            Specialist roster, department categorization, consultation fee schedules, active on-duty status, and linked encounter histories.
          </p>
        </div>

        <!-- 5. Hospital Bed Management -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="bed"></i>
          </div>
          <h3 class="feature-name">Hospital Bed Management</h3>
          <p class="feature-desc">
            Interactive ward layout covering ICU, General, Emergency, and Pediatric wards. Transactional admission, transfer, and discharge with zero collisions.
          </p>
        </div>

        <!-- 6. OPD Queue Management -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="users"></i>
          </div>
          <h3 class="feature-name">OPD Queue Management</h3>
          <p class="feature-desc">
            Persistent daily token numbering mechanism supporting Waiting, Serving, Completed, and Cancelled states for frictionless patient intake.
          </p>
        </div>

        <!-- 7. Hospital Analytics -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="trending-up"></i>
          </div>
          <h3 class="feature-name">Hospital Analytics</h3>
          <p class="feature-desc">
            Real-time visual charts for inpatient occupancy, outpatient volume trends, department workload distribution, and patient vitals progression.
          </p>
        </div>

        <!-- 8. Lab Report Management -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="flask-conical"></i>
          </div>
          <h3 class="feature-name">Lab Report Management</h3>
          <p class="feature-desc">
            Digital diagnostic report archiving with file upload, automated reference range flags, abnormal value alerts, and direct patient timeline linkage.
          </p>
        </div>

        <!-- 9. Emergency Care Coordination -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="ambulance"></i>
          </div>
          <h3 class="feature-name">Emergency Care Coordination</h3>
          <p class="feature-desc">
            5-level Emergency Severity Index (ESI) trauma triage with automated resuscitation bay recommendations and break-glass emergency record access.
          </p>
        </div>

        <!-- 10. Secure Role-Based Access -->
        <div class="feature-card">
          <div class="feature-icon-box">
            <i data-lucide="shield-check"></i>
          </div>
          <h3 class="feature-name">Secure Role-Based Access</h3>
          <p class="feature-desc">
            PBKDF2-secured token authentication with strict role permissions for Administrators, Doctors, Receptionists, and Emergency Staff with audit logging.
          </p>
        </div>
      </div>
    </section>

    <!-- How MediLink Works Section -->
    <section class="landing-section" style="background:var(--bg-alt);" id="how-it-works">
      <div class="section-header">
        <span class="section-tag">Operational Workflow</span>
        <h2 class="section-title">How MediLink Works</h2>
        <p class="section-desc">
          Four intuitive steps connecting administrative workflows, clinical diagnostics, and executive oversight.
        </p>
      </div>

      <div class="how-it-works-grid">
        <div class="step-card">
          <div class="step-num-badge">STEP 1</div>
          <div class="step-icon-wrap">
            <i data-lucide="key-round"></i>
          </div>
          <h4 class="step-title">Securely Sign In</h4>
          <p class="step-desc">
            Authenticate using institutional role credentials (Doctor, Admin, Receptionist, Emergency) with signed session tokens.
          </p>
        </div>

        <div class="step-card">
          <div class="step-num-badge">STEP 2</div>
          <div class="step-icon-wrap">
            <i data-lucide="layout-grid"></i>
          </div>
          <h4 class="step-title">Select Module</h4>
          <p class="step-desc">
            Navigate through dedicated clinical workspaces: OPD Queue, Unified EHR, Beds &amp; Wards, Consultations, or Appointments.
          </p>
        </div>

        <div class="step-card">
          <div class="step-num-badge">STEP 3</div>
          <div class="step-icon-wrap">
            <i data-lucide="activity"></i>
          </div>
          <h4 class="step-title">Manage Operations</h4>
          <p class="step-desc">
            Perform clinical actions: write prescriptions with CDSS interaction alerts, admit patients, and upload diagnostic tests.
          </p>
        </div>

        <div class="step-card">
          <div class="step-num-badge">STEP 4</div>
          <div class="step-icon-wrap">
            <i data-lucide="bar-chart-3"></i>
          </div>
          <h4 class="step-title">Access Insights</h4>
          <p class="step-desc">
            Review real-time hospital occupancy, export compliance CSV reports, inspect audit trails, and run SQL queries in the workbench.
          </p>
        </div>
      </div>
    </section>

    <!-- Benefits Section -->
    <section class="landing-section" id="benefits">
      <div class="section-header">
        <span class="section-tag">Institutional Advantages</span>
        <h2 class="section-title">Why Leading Facilities Rely on MediLink</h2>
        <p class="section-desc">
          Eliminating fragmented data silos to deliver faster care, lower administrative overhead, and higher clinical safety.
        </p>
      </div>

      <div class="benefits-grid">
        <div class="benefit-card">
          <div class="benefit-check">✓</div>
          <div>
            <h4 class="benefit-title">Streamlined Hospital Operations</h4>
            <p class="benefit-desc">Automated bed allocations, daily OPD token management, and doctor rosters minimize bottlenecks.</p>
          </div>
        </div>
        <div class="benefit-card">
          <div class="benefit-check">✓</div>
          <div>
            <h4 class="benefit-title">Centralized Medical Records</h4>
            <p class="benefit-desc">Longitudinal patient records synchronized across affiliated health facilities using national Aadhaar UID.</p>
          </div>
        </div>
        <div class="benefit-card">
          <div class="benefit-check">✓</div>
          <div>
            <h4 class="benefit-title">Reduced Administrative Complexity</h4>
            <p class="benefit-desc">Single-click appointment scheduling, instant bed transfers, and verified PDF prescriptions save staff hours.</p>
          </div>
        </div>
        <div class="benefit-card">
          <div class="benefit-check">✓</div>
          <div>
            <h4 class="benefit-title">Better Appointment Coordination</h4>
            <p class="benefit-desc">Eliminates double bookings with real-time schedule conflict validation across specialist clinics.</p>
          </div>
        </div>
        <div class="benefit-card">
          <div class="benefit-check">✓</div>
          <div>
            <h4 class="benefit-title">Organized Healthcare Data</h4>
            <p class="benefit-desc">11 normalized relational database entities ensuring data integrity, ACID transactions, and zero orphaned records.</p>
          </div>
        </div>
        <div class="benefit-card">
          <div class="benefit-check">✓</div>
          <div>
            <h4 class="benefit-title">Secure Access Control</h4>
            <p class="benefit-desc">Granular RBAC privileges, emergency break-glass protocols, and permanent cryptographic audit logging.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Dashboard Preview Section -->
    <section class="landing-section" style="background:var(--bg-alt);" id="preview">
      <div class="section-header">
        <span class="section-tag">Platform Showcase</span>
        <h2 class="section-title">Live Hospital Command Center Preview</h2>
        <p class="section-desc">
          Experience the intuitive, clinical-grade interface designed for rapid decision-making in high-pressure healthcare environments.
        </p>
      </div>

      <div class="preview-container">
        <div class="preview-topbar">
          <div style="display:flex; align-items:center; gap:8px;">
            <span class="mock-dot"></span>
            <span class="mock-dot"></span>
            <span class="mock-dot"></span>
            <strong style="font-size:0.85rem; margin-left:8px;">MediLink Command Center v3.0 — AIIMS Node</strong>
          </div>
          <button class="btn btn-primary btn-sm" onclick="handleGetStarted()">Launch Full Workspace →</button>
        </div>
        <div class="preview-body">
          <div class="metrics-grid" style="margin-bottom:1.5rem;">
            <div class="metric-card">
              <div>
                <div class="metric-title">Active Patients</div>
                <div class="metric-num">5</div>
                <div class="metric-sub">Linked with Aadhaar UID</div>
              </div>
              <div class="metric-icon-box">👥</div>
            </div>
            <div class="metric-card">
              <div>
                <div class="metric-title">Encounters Logged</div>
                <div class="metric-num">12</div>
                <div class="metric-sub">Verified Clinical EMR</div>
              </div>
              <div class="metric-icon-box">📑</div>
            </div>
            <div class="metric-card">
              <div>
                <div class="metric-title">Bed Occupancy</div>
                <div class="metric-num">5/16 (31%)</div>
                <div class="metric-sub">ICU: 2 • General: 2 • ER: 1</div>
              </div>
              <div class="metric-icon-box">🛏️</div>
            </div>
            <div class="metric-card">
              <div>
                <div class="metric-title">Live OPD Queue</div>
                <div class="metric-num">3 Waiting</div>
                <div class="metric-sub">Daily Auto-Sequenced</div>
              </div>
              <div class="metric-icon-box">🎫</div>
            </div>
          </div>
          <div class="panel">
            <div class="panel-header">
              <span class="panel-title">Recent Clinical Encounters</span>
              <span class="badge badge-primary">Sample Operational View</span>
            </div>
            <div class="panel-body" style="padding:0;">
              <table class="table">
                <thead>
                  <tr>
                    <th>Record ID</th>
                    <th>Patient Name</th>
                    <th>Diagnosis</th>
                    <th>Attending Doctor</th>
                    <th>Facility</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><code>REC-2024-001</code></td>
                    <td><strong>Priya Sharma</strong></td>
                    <td>Essential Hypertension (I10)</td>
                    <td>Dr. Anita Verma</td>
                    <td>Apollo Hospital</td>
                    <td><span class="badge badge-success">Completed</span></td>
                  </tr>
                  <tr>
                    <td><code>REC-2024-002</code></td>
                    <td><strong>Rahul Mehta</strong></td>
                    <td>Type 2 Diabetes Mellitus (E11)</td>
                    <td>Dr. Rajesh Gupta</td>
                    <td>Fortis Healthcare</td>
                    <td><span class="badge badge-success">Completed</span></td>
                  </tr>
                  <tr>
                    <td><code>REC-2024-003</code></td>
                    <td><strong>Ananya Iyer</strong></td>
                    <td>Bronchial Asthma (J45)</td>
                    <td>Dr. Anita Verma</td>
                    <td>Apollo Hospital</td>
                    <td><span class="badge badge-info">Follow-up</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Final Call-to-Action Section -->
    <section class="landing-section">
      <div class="cta-banner">
        <h2>Transform the Way You Manage Healthcare.</h2>
        <p>
          Experience unified patient care, frictionless clinical workflows, and enterprise-grade data management today.
        </p>
        <button class="btn btn-primary" onclick="handleGetStarted()" style="padding:0.85rem 2rem; font-size:1.05rem; font-weight:700; background:#fff; color:var(--primary); border:none; box-shadow:var(--shadow-lg);">
          Launch MediLink →
        </button>
      </div>
    </section>

    <!-- Clean Footer -->
    <footer class="landing-footer" id="contact">
      <div class="footer-container">
        <div class="footer-brand">
          <div class="landing-brand">
            <div class="landing-brand-icon">⚕</div>
            <span>MediLink<span style="color:var(--primary)">.</span></span>
          </div>
          <p>
            MediLink Enterprise is an interoperable, unified hospital management and electronic medical records platform engineered for modern healthcare institutions.
          </p>
        </div>

        <div>
          <div class="footer-col-title">Platform</div>
          <ul class="footer-links">
            <li><a href="#hero">Overview</a></li>
            <li><a href="#features">Features</a></li>
            <li><a href="#how-it-works">How It Works</a></li>
            <li><a href="#benefits">Institutional Benefits</a></li>
            <li><a href="#preview">Command Center Preview</a></li>
          </ul>
        </div>

        <div>
          <div class="footer-col-title">Modules</div>
          <ul class="footer-links">
            <li><a href="javascript:void(0)" onclick="switchView('login')">Patient Directory</a></li>
            <li><a href="javascript:void(0)" onclick="switchView('login')">OPD Queue System</a></li>
            <li><a href="javascript:void(0)" onclick="switchView('login')">Bed &amp; Ward Management</a></li>
            <li><a href="javascript:void(0)" onclick="switchView('login')">Diagnostic Labs</a></li>
            <li><a href="javascript:void(0)" onclick="switchView('login')">SQL Workbench</a></li>
          </ul>
        </div>

        <div>
          <div class="footer-col-title">Security &amp; Governance</div>
          <p style="font-size:0.82rem; color:var(--text-muted); line-height:1.6; margin-bottom:0.75rem;">
            Built with strict role-based access control, cryptographic PBKDF2 authentication, and immutable audit logs.
          </p>
          <div style="font-size:0.78rem; color:var(--text-dim);">
            DBMS Project Demonstration<br>FastAPI • SQLAlchemy • MySQL/SQLite
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div>© 2026 MediLink Enterprise v3.0. All rights reserved.</div>
        <div>Engineered for Healthcare Demonstration</div>
      </div>
    </footer>
  </div>

  <!-- ====================================================================
       VIEW 2: DEDICATED 2-COLUMN LOGIN VIEW (#view-login)
       ==================================================================== -->
  <div id="view-login" class="app-view">
    <div class="login-viewport">
      <div class="login-card-wrapper">
        <!-- Left Brand Side -->
        <div class="login-brand-side">
          <div>
            <div class="landing-brand" style="color:#fff; margin-bottom:1.5rem;">
              <div class="landing-brand-icon">⚕</div>
              <span>MediLink<span style="color:var(--primary); font-weight:800">.</span></span>
            </div>
            <h2 style="font-family:var(--font-heading); font-size:1.85rem; font-weight:800; line-height:1.25; margin-bottom:1rem;">
              Next-Generation Hospital Information System.
            </h2>
            <p style="color:#94a3b8; font-size:0.92rem; line-height:1.6; margin-bottom:2rem;">
              Securely access hospital command centers, patient records, clinical consultations, and live bed allocations with role-based governance.
            </p>
            <div style="display:flex; flex-direction:column; gap:0.75rem;">
              <div style="display:flex; align-items:center; gap:0.65rem; font-size:0.85rem; color:#cbd5e1;">
                <span style="color:var(--success); font-weight:800;">✓</span>
                <span>Zero Data Collision Bed Management</span>
              </div>
              <div style="display:flex; align-items:center; gap:0.65rem; font-size:0.85rem; color:#cbd5e1;">
                <span style="color:var(--success); font-weight:800;">✓</span>
                <span>Automated Drug-Allergy &amp; Drug-Drug CDSS</span>
              </div>
              <div style="display:flex; align-items:center; gap:0.65rem; font-size:0.85rem; color:#cbd5e1;">
                <span style="color:var(--success); font-weight:800;">✓</span>
                <span>Cryptographic PBKDF2 Access Control</span>
              </div>
              <div style="display:flex; align-items:center; gap:0.65rem; font-size:0.85rem; color:#cbd5e1;">
                <span style="color:var(--success); font-weight:800;">✓</span>
                <span>Dual MySQL 8.0 &amp; Zero-Config SQLite Fallback</span>
              </div>
            </div>
          </div>

          <div style="font-size:0.75rem; color:#64748b; border-top:1px solid #334155; padding-top:1.25rem;">
            Hospital Network Node v3.0 • Verified ABHA/Aadhaar Linked EMR
          </div>
        </div>

        <!-- Right Form Side -->
        <div class="login-form-side">
          <div class="login-header">
            <h2>Welcome to MediLink</h2>
            <p>Sign in to access your hospital command center</p>
          </div>

          <form id="login-form" onsubmit="handleLoginFormSubmit(event)">
            <div class="form-group" style="margin-bottom:1rem;">
              <label class="form-label" for="login-username">Workstation Username</label>
              <input type="text" id="login-username" class="form-control" placeholder="e.g. admin" required value="admin" />
            </div>

            <div class="form-group" style="margin-bottom:1.25rem;">
              <label class="form-label" for="login-password">Password</label>
              <div style="position:relative;">
                <input type="password" id="login-password" class="form-control" placeholder="Enter password" required value="admin123" style="padding-right:40px;" />
                <button type="button" class="btn-icon" id="btn-toggle-pw" onclick="togglePasswordVisibility()" style="position:absolute; right:8px; top:50%; transform:translateY(-50%); width:28px; height:28px; font-size:0.9rem;" title="Show/Hide Password">
                  👁️
                </button>
              </div>
            </div>

            <button type="submit" class="btn btn-primary" style="width:100%; padding:0.75rem; font-weight:700; font-size:0.95rem; justify-content:center;">
              Sign In to Workspace →
            </button>
          </form>

          <!-- Quick Demo Role Switcher -->
          <div class="demo-credentials-box">
            <div style="font-weight:700; color:var(--text); margin-bottom:0.4rem;">⚡ Quick Demo Profiles:</div>
            <div style="display:flex; flex-wrap:wrap; gap:4px;">
              <span class="demo-btn-pill" onclick="quickLogin('admin')">🔑 Admin</span>
              <span class="demo-btn-pill" onclick="quickLogin('doctor')">🩺 Doctor</span>
              <span class="demo-btn-pill" onclick="quickLogin('receptionist')">📋 Reception</span>
              <span class="demo-btn-pill" onclick="quickLogin('emergency')">🚑 Emergency</span>
            </div>
            <div style="font-size:0.7rem; color:var(--text-muted); margin-top:4px;">
              Click any role to auto-fill credentials and sign in instantly.
            </div>
          </div>

          <div style="text-align:center; margin-top:1.5rem;">
            <a href="javascript:void(0)" onclick="switchView('landing')" style="font-size:0.85rem; color:var(--primary); text-decoration:none; font-weight:600;">
              ← Return to Homepage
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ====================================================================
       VIEW 3: HOSPITAL COMMAND CENTER SHELL (#view-app)
       ==================================================================== -->
  <div id="view-app" class="app-view">
"""

# Insert View 1, View 2, and opening View 3 before #app-container
if 'id="view-landing"' not in content:
    content = content.replace(
        '<body>\n  <div id="app-container">',
        '<body>' + landing_and_login + '\n  <div id="app-container">'
    )

# Close #view-app right after #app-container closes
if '<!-- /#view-app -->' not in content:
    content = re.sub(
        r'(      </div>\s*</main>\s*</div>)(\s*<!-- ====================================================================\s*MODALS)',
        r'\1\n  </div> <!-- /#view-app -->\2',
        content
    )

# 3. Add Profile Avatar and Sign Out button to header right
header_avatar_html = """          <!-- Theme Toggle Button -->
          <button class="btn-icon" onclick="toggleTheme()" title="Toggle Clinical Night Shift / Light Theme">🌓</button>

          <!-- Staff Profile Avatar & Logout Button -->
          <div style="display:flex; align-items:center; gap:0.6rem; margin-left:0.5rem; padding-left:0.5rem; border-left:1px solid var(--border);">
            <div style="width:32px; height:32px; border-radius:var(--radius-full); background:var(--primary-light); color:var(--primary); font-weight:700; font-size:0.82rem; display:flex; align-items:center; justify-content:center;" id="header-avatar-initials">
              SA
            </div>
            <button class="btn btn-secondary btn-sm" onclick="logoutUser()" title="Sign Out of Workspace" style="font-size:0.75rem; padding:4px 10px;">
              Sign Out
            </button>
          </div>"""

if "header-avatar-initials" not in content:
    content = content.replace(
        '          <!-- Theme Toggle Button -->\n          <button class="btn-icon" onclick="toggleTheme()" title="Toggle Clinical Night Shift / Light Theme">🌓</button>',
        header_avatar_html
    )

# 4. Add Welcome Greeting Banner to page-home
welcome_banner_html = """        <!-- ==============================================================
             PAGE 1: COMMAND DASHBOARD & OVERVIEW
             ============================================================== -->
        <section id="page-home" class="page active">
          <!-- Welcome Greeting Banner -->
          <div class="welcome-banner" style="display:flex; justify-content:space-between; align-items:center; background:linear-gradient(135deg, rgba(37,99,235,0.08), rgba(13,148,136,0.08)); border:1px solid var(--border); border-radius:var(--radius-lg); padding:1.25rem 1.5rem; margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
            <div>
              <h2 style="font-family:var(--font-heading); font-size:1.35rem; font-weight:800; color:var(--text);">
                Welcome back, <span id="welcome-user-name">System Administrator</span> 👋
              </h2>
              <p style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">
                Hospital Operations &amp; Unified Clinical Records Network • Active Node: <span id="welcome-facility-node" style="font-weight:600; color:var(--primary);">AIIMS Delhi (Node 01)</span>
              </p>
            </div>
            <div style="display:flex; gap:0.6rem; align-items:center;">
              <button class="btn btn-secondary btn-sm" onclick="showPage('page-encounter')">
                🩺 + New Consultation
              </button>
              <button class="btn btn-primary btn-sm" onclick="showPage('page-register')">
                👥 Enroll Patient
              </button>
            </div>
          </div>

          <!-- Metric KPIs -->"""

if "welcome-banner" not in content:
    content = content.replace(
        '        <!-- ==============================================================\n             PAGE 1: COMMAND DASHBOARD & OVERVIEW\n             ============================================================== -->\n        <section id="page-home" class="page active">\n          <!-- Metric KPIs -->',
        welcome_banner_html
    )

# 5. Sidebar footer return home button
sidebar_footer_old = """      <div class="sidebar-footer">
        <div style="font-size:0.75rem; color:var(--text-muted);">
          <div><strong>MediLink v3.0</strong> Enterprise</div>
          <div style="color:var(--success); font-weight:600">● Relational Core Active</div>
        </div>
      </div>"""

sidebar_footer_new = """      <div class="sidebar-footer">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div style="font-size:0.75rem; color:var(--text-muted);">
            <div><strong>MediLink v3.0</strong> Enterprise</div>
            <div style="color:var(--success); font-weight:600">● Relational Core Active</div>
          </div>
          <button class="btn-icon" onclick="switchView('landing')" title="View Public Homepage" style="font-size:0.85rem; width:28px; height:28px;">
            🏠
          </button>
        </div>
      </div>"""

if "View Public Homepage" not in content:
    content = content.replace(sidebar_footer_old, sidebar_footer_new)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html successfully.")
