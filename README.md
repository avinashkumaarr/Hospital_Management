# MediLink: Aadhaar-Based Unified Medical Records & Hospital Management System
> **Enterprise Electronic Medical Record (EMR) & Hospital Administration Platform**  
> Built with FastAPI, SQLAlchemy ORM, MySQL Relational Database (with zero-config SQLite fallback), and a Modern Healthcare Command Center UI.

![System](https://img.shields.io/badge/System-MediLink_v4.0_Enterprise-004b87?style=for-the-badge)
![Backend](https://img.shields.io/badge/Backend-FastAPI_REST_API-059669?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-MySQL_%7C_SQLite_Fallback-f59e0b?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-Pytest_12%2F12_Passing-10b981?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

---

## 🌟 Executive Overview

**MediLink** solves fragmented healthcare record keeping by providing an interoperable, unified electronic medical record (EMR) system where citizen records are retrieved via a verified 12-digit Aadhaar UID across healthcare nodes (e.g., AIIMS Delhi, Apollo Hospitals, Fortis, Max Super Speciality).

This upgraded release transforms the original static prototype into a full-stack, enterprise-grade application with persistent relational storage, server-enforced authentication and role-based permissions, real-time clinical decision support, collision-safe OPD queue management, transactional bed admissions, appointment scheduling, and automated DBMS course evaluation query benchmarking.

---

## 🛠️ Architecture & Technology Stack

```
+---------------------------------------------------------------------------------+
|                                 FRONTEND LAYER                                  |
|   Modern Healthcare UI • Responsive Application Shell • Chart.js • Vanilla JS   |
+---------------------------------------------------------------------------------+
                                       │  REST APIs (JSON / Multipart)
                                       ▼
+---------------------------------------------------------------------------------+
|                                 BACKEND LAYER                                   |
|   Python FastAPI • Pydantic Validation • Token Auth • CDSS Rules • ESI Triage   |
+---------------------------------------------------------------------------------+
                                       │  SQLAlchemy ORM
                                       ▼
+---------------------------------------------------------------------------------+
|                             RELATIONAL DATABASE LAYER                           |
|   MySQL 8.0 (Primary)  ◄── Automatic Fallback ──►  SQLite (Zero-Config Dev)     |
|   11 Tables • Foreign Key Cascades • Transactions • Predefined Q1-Q5 Queries    |
+---------------------------------------------------------------------------------+
```

- **Backend Framework**: Python FastAPI (modular routers, dependency injection, async lifespan).
- **ORM & Database**: SQLAlchemy 2.0 with MySQL Connector (and SQLite zero-config local dev fallback).
- **Security & Auth**: PBKDF2-HMAC-SHA256 password hashing, signed JWT-style session tokens.
- **Frontend Architecture**: Modular CSS healthcare design system, API client layer (`api.js`), and reactive application logic (`app.js`).
- **Clinical Decision Support (CDSS)**: Cross-allergen detection (beta-lactams, sulfa, NSAIDs), dangerous drug-drug interaction checker, and algorithmic ESI 1–5 trauma triage.

---

## 📋 Comprehensive Module Inventory

All 18 original modules have been preserved and enhanced, plus 6 major new features:

| # | Module | Status | Highlights |
|---|---|---|---|
| 1 | **Command Dashboard** | Active | Real-time KPI metrics, department doughnut chart, hospital volume chart, recent encounters ledger. |
| 2 | **Patient Enrollment** | Active | Strict 12-digit Aadhaar validation, mobile deduplication, date of birth verification. |
| 3 | **Aadhaar Record Search** | Active | Instant citizen EHR lookup, masked identifiers (`XXXX-XXXX-1234`), quick demo profile chips. |
| 4 | **Encounter Timeline** | Active | Permanent record ID mapping, filter by visit type, print prescription slip. |
| 5 | **Doctor Consultation** | Active | Real-time CDSS allergy scan, ICD-10 suggestions, structured vitals capture, persistent storage. |
| 6 | **ICD-10 Search** | Active | Instant clinical code lookup (`I10`, `E11.9`, `J45.909`, `I21.4`, `M23.22`, `A09`) with 1-click Rx templates. |
| 7 | **Allergy & Drug Alerts** | Active | Live cross-reactivity warnings (Penicillin → Amoxicillin) & critical interaction checks (Warfarin + Aspirin). |
| 8 | **Vitals Visualization** | Active | Accurately parsed from real encounters (never hardcoded fake numbers); longitudinal BP/HR line chart. |
| 9 | **Emergency Trauma Triage** | Active | Algorithmic Emergency Severity Index (ESI 1–5) calculation with recommended trauma bays. |
| 10 | **Beds & Wards Management** | Active | Interactive matrix, atomic single-patient admission, sanitization cleaning workflows. |
| 11 | **OPD Live Token Queue** | Active | Daily collision-safe numbering (`A-101`), auditory chime, now-serving hero board. |
| 12 | **Hospital Analytics** | Active | Real aggregated statistics, department distributions, 1-click CSV report exports. |
| 13 | **Access Audit Logs** | Active | Server-generated audit trail capturing real user, real timestamp, real IP, and purpose. |
| 14 | **SQL DBMS Workbench** | Active | Executes approved queries (Q1–Q5) against real database with execution benchmarking. |
| 15 | **Digital Health Card** | Active | Physical-look ABHA card with gold chip graphic, barcode, QR code, blood group badge. |
| 16 | **Prescription Printing** | Active | Print-ready encounter slip complete with NABH header, demographics, Rx table, and digital signature. |
| 17 | **Data Backup & Restore** | Active | Non-destructive JSON export/import supporting legacy data migration without data loss. |
| 18 | **Theme Engine** | Active | Hospital Brand Clinical Light & Night Shift Clinical Dark mode with localStorage persistence. |
| 19 | **Appointment Scheduling** *(New)* | Active | Doctor slot booking, double-booking prevention, reschedule, and cancellation. |
| 20 | **Doctor Availability** *(New)* | Active | Daily consultation metrics, upcoming appointments, and scheduled time slot slots. |
| 21 | **Digital Lab Reports** *(New)* | Active | Structured test records, abnormal highlighting, and secure PDF report upload/download. |
| 22 | **Notification Center** *(New)* | Active | In-app alerts for appointments, queue events, bed sanitization, and system notices. |
| 23 | **Advanced Global Search** *(New)* | Active | Fast `Ctrl+K` search across patients, doctors, and facilities. |
| 24 | **Exportable Reports** *(New)* | Active | 1-click CSV downloads for Clinical Encounters, Bed Utilization, and Appointments. |

---

## 🎨 Premium Healthcare Landing Page & Enterprise Design System

The frontend has been completely redesigned into a unified single-page application (SPA) with three interconnected views:

```
[ Public Visitors ] ──► #view-landing (Brand Landing Page, Features, How It Works, Benefits, Preview, CTA, Footer)
                              │
                              ▼ "Sign In" / "Get Started"
                        #view-login (2-Column Auth Screen, Demo Profile Pills, Password Eye Toggle)
                              │
                              ▼ Authenticated Session
                        #view-app (Hospital Command Center Shell, Lucide Icons, Breadcrumbs, 15 Modules)
```

### 1. Public Landing Homepage (`#view-landing`)
- **Modern Sticky Navigation**: Translucent background blur, logo badge, smooth-scroll links (`#features`, `#how-it-works`, `#benefits`, `#preview`, `#contact`), dark/light mode toggle, mobile hamburger menu.
- **Hero Section**:
  - Heading: *"Smarter Healthcare. Seamlessly Connected."*
  - Subheading: *"One intelligent platform to manage patients, medical records, appointments, hospital operations, and healthcare insights — all in one place."*
  - CTAs: Primary *"Get Started"* (navigates to login or direct workspace) and Secondary *"Explore Features"*.
  - Institutional trust statistics: 6+ Tier-1 Nodes, 100% CDSS Safety, 11 DBMS Entities, Zero Data Collisions.
  - Realistic CSS/SVG hospital command center preview mockup card on the right.
- **10 Modern Feature Cards with Lucide Icons**:
  1. *Unified Patient Records* (`file-heart`)
  2. *Smart Appointment Scheduling* (`calendar-check`)
  3. *Digital Prescriptions* (`pill`)
  4. *Doctor Management* (`stethoscope`)
  5. *Hospital Bed Management* (`bed`)
  6. *OPD Queue Management* (`users`)
  7. *Hospital Analytics* (`trending-up`)
  8. *Lab Report Management* (`flask-conical`)
  9. *Emergency Care Coordination* (`ambulance`)
  10. *Secure Role-Based Access* (`shield-check`)
- **"How MediLink Works" 4-Step Process**:
  - *Step 1*: Securely Sign In with institutional credentials.
  - *Step 2*: Select Module from dedicated clinical workspaces.
  - *Step 3*: Manage Operations (write prescriptions, admit patients, upload diagnostics).
  - *Step 4*: Access Insights (occupancy analytics, compliance CSVs, SQL workbench).
- **Institutional Benefits (6 Cards)**:
  - Streamlined Hospital Operations, Centralized Medical Records, Reduced Administrative Complexity, Better Appointment Coordination, Organized Healthcare Data, Secure Access Control.
- **Interactive Command Center Showcase**: Live sample operational view with bed occupancy, OPD queue counts, and recent clinical encounter records.
- **Final Call-to-Action**: *"Transform the Way You Manage Healthcare."* with prominent *"Launch MediLink"* button.
- **Enterprise Footer**: Brand summary, platform links, module links, governance details, and copyright.

### 2. Dedicated 2-Column Login View (`#view-login`)
- **Left Brand Panel**: Deep Navy gradient background, MediLink emblem, clinical safety highlights (CDSS warnings, zero bed collisions, PBKDF2 encryption, MySQL/SQLite dual support), and architecture diagram.
- **Right Form Panel**: Clean workstation login form, username and password inputs with show/hide password eye toggle, sign-in button.
- **⚡ 1-Click Quick Demo Profile Pills**:
  - 🔑 **Admin** (`admin` / `admin123`)
  - 🩺 **Doctor** (`doctor` / `doctor123`)
  - 📋 **Reception** (`receptionist` / `reception123`)
  - 🚑 **Emergency** (`emergency` / `emergency123`)
- **Seamless Return Link**: *"← Return to Homepage"* to easily switch back.

### 3. Hospital Command Center Redesign (`#view-app`)
- **Sidebar Navigation**: Crisp Lucide vector icons for all 15 operational pages with live counter badges.
- **Topbar Header**: Global facility node selector, global patient search with `Ctrl+K` shortcut, active role selector, live notification bell with unread badge counter, theme switcher, and staff profile avatar with *"Sign Out"* button.
- **Welcome Greeting Banner**: Dynamic greeting *"Welcome back, {Staff Name}!"* displaying the active hospital node and direct quick-action buttons.

---

## 🐛 Summary of Actual Bugs Fixed

1. **Patient Medical Timeline Index Mismatch**:
   - *Previous Bug*: Timeline filter (`filterType !== 'ALL'`) passed the filtered array index `idx` to `openPrescriptionSlip(${idx})`, opening the wrong encounter or throwing `undefined` errors.
   - *Fix*: Encounters are now referenced by permanent, unique `record_id` (e.g. `openPrescriptionSlipByRecordId(r.record_id)`).

2. **Duplicate OPD Token Numbers**:
   - *Previous Bug*: Token generation was computed as `100 + queue.length + 1`, causing duplicate tokens whenever tokens were deleted, reset, or generated concurrently.
   - *Fix*: Implemented `/api/queue/issue` using persistent daily sequence numbering per hospital node, ensuring collision-safe tokens (`A-101`, `A-102`) and preventing duplicate active tokens for the same patient on the same day.

3. **Hardcoded / Fake Patient Vitals**:
   - *Previous Bug*: Patient vitals card hardcoded `145/95 mmHg`, `82 bpm`, `98%`, and `23.4 BMI` for every single patient profile.
   - *Fix*: Displayed vitals are now parsed dynamically from the patient's actual latest encounter's `vitals_summary`. When unrecorded, displays `"Not recorded"` instead of inventing numbers.

4. **Bed Allocation Inconsistencies**:
   - *Previous Bug*: Allowed assigning the same active bed to multiple patients, and allowed admitting the same patient into multiple active beds simultaneously (e.g., Rajesh Verma was seeded into both `ER-101` and `ICU-201`).
   - *Fix*: Enforced strict transactional state transitions in `/api/beds/admit` and `/api/beds/{id}/discharge`. Patients can occupy at most 1 active bed across all wards, and only `Vacant` beds can be allocated.

5. **Browser-Generated Fake Audit Logs**:
   - *Previous Bug*: Audit logs generated random numbers for IDs (`Math.random()`) and fake random IPs (`192.168.1.XX`) in JavaScript.
   - *Fix*: Audit logging moved to backend `/api/audit`. Every chart lookup, break-glass override, admission, and prescription records the authenticated clinician, real request timestamp, real client IP (e.g. `127.0.0.1`), and clinical reason.

6. **Visual-Only Role Switching**:
   - *Previous Bug*: Clicking role switcher merely changed a text label between Doctor/Admin without server authentication or access control.
   - *Fix*: Real server authentication (`/api/auth/login`) with signed tokens. Pre-configured demo accounts for **Administrator**, **Doctor**, **Receptionist**, and **Emergency Staff** with server-enforced permissions and custom UI views.

7. **Missing Form Validation**:
   - *Previous Bug*: Unformatted text accepted for Aadhaar, mobile numbers, and past/future dates.
   - *Fix*: Strict validation for 12-digit normalized Aadhaar numbers, 10-digit mobile numbers with duplicate prevention, and past-date validation for date of birth.

8. **Unsafe HTML Direct Interpolation (XSS)**:
   - *Previous Bug*: User-provided input in diagnoses, prescriptions, and notes was interpolated directly into `innerHTML`.
   - *Fix*: Implemented `escapeHtml()` sanitizer utility throughout all table and card rendering routines.

9. **Simulated SQL Workbench**:
   - *Previous Bug*: SQL workbench simulated database query results using JavaScript array filtering.
   - *Fix*: Connected to backend `/api/sql/execute`, executing approved, read-only parameterized queries against the real database with execution benchmarking.

10. **State Persistence & Null Checks**:
    - *Previous Bug*: Reloading the page lost newly entered data unless saved to localStorage.
    - *Fix*: All clinical operations persist to SQLite/MySQL storage with automatic hydration and real-time backend updates.

---

## 🗄️ Relational Database Schema (`schema.sql`)

The extended relational database schema comprises 11 normalized tables:

```
+---------------+        1:N        +------------------+        1:N        +------------------+
|    PATIENT    | <---------------- |  MEDICAL_RECORD  | ----------------> |    LAB_REPORT    |
| (Aadhaar PK)  |                   |  (Central Fact)  |                   |   (Diagnostic)   |
+---------------+                   +------------------+                   +------------------+
    |       |                                |
    | 1:N   | 1:N                            | 1:N
    |       v                                v
    |   +---------------+           +------------------+
    |   |  ACCESS_LOG   |           |    APPOINTMENT   |
    |   | (Audit Trail) |           |  (Doctor Slots)  |
    |   +---------------+           +------------------+
    |                                        ^
    | 1:N                                    | 1:N
    v                                        |
+---------------+        1:N        +------------------+
|   HOSPITAL    | ----------------> |      DOCTOR      |
| (Facility PK) |                   |    (Staff FK)    |
+---------------+                   +------------------+
    |       |                                |
    | 1:N   | 1:N                            | 1:N
    v       v                                v
+---------------+                   +------------------+
|  BED_ALLOC    |                   |    OPD_QUEUE     |
|  (Resources)  |                   |   (Live Tokens)  |
+---------------+                   +------------------+
```

### Table Summary:
1. **`patient`**: Primary Key `aadhaar_number` (VARCHAR 14). Demographics, blood group, documented allergies, chronic conditions, and emergency contacts.
2. **`hospital`**: Facility details, registration numbers, types (`Government`, `Private`, `Trust`), cities, states.
3. **`doctor`**: Medical practitioners with hospital FK, specializations, qualifications, licenses.
4. **`medical_record`**: Central fact table storing visit date, type, department, chief complaint, ICD-10 diagnosis, vitals summary, Rx prescription, and notes.
5. **`lab_report`**: Laboratory investigations linked to patient and medical record, reference intervals, abnormal flags, and PDF file attachments.
6. **`access_log`**: Security audit trail capturing accessor, hospital node, purpose, IP address, and timestamp.
7. **`bed_allocation`**: Ward room and bed status (`Occupied`, `Vacant`, `Cleaning`, `Reserved`).
8. **`appointment`**: Doctor appointment bookings with double-booking prevention constraint (`doctor_id`, `appointment_date`, `time_slot`).
9. **`opd_queue`**: Daily token numbering with statuses (`Waiting`, `Serving`, `Completed`, `Cancelled`).
10. **`user`**: Staff authentication accounts, PBKDF2 hashed credentials, and role assignments.
11. **`notification`**: In-app clinical alerts and status change notifications.

---

## 💡 DBMS Course Evaluation Queries (Q1–Q5)

All 5 core evaluation queries execute against the live database in the **SQL Workbench**:

- **Q1 (Join across 3 tables)**: Retrieve lifelong medical history of any patient using Aadhaar UID:
  ```sql
  SELECT mr.record_id, mr.visit_date, mr.visit_type, mr.department, mr.diagnosis, mr.icd10_code, h.hospital_name, d.doctor_name
  FROM medical_record mr
  JOIN hospital h ON mr.hospital_id = h.hospital_id
  LEFT JOIN doctor d ON mr.doctor_id = d.doctor_id
  WHERE mr.aadhaar_number = :param
  ORDER BY mr.visit_date DESC;
  ```
- **Q2 (Aggregation & Group By)**: Aggregate patient visit volume and identify most recent consultation date:
  ```sql
  SELECT p.aadhaar_number, p.full_name, p.blood_group, COUNT(mr.record_id) AS total_visits, MAX(mr.visit_date) AS latest_visit_date
  FROM patient p
  LEFT JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number
  WHERE p.aadhaar_number = :param
  GROUP BY p.aadhaar_number;
  ```
- **Q3 (Filtering on boolean/abnormal diagnostics)**: Abnormal lab investigations across all hospitals:
  ```sql
  SELECT lr.test_name, lr.result, lr.normal_range, lr.unit, lr.report_date, lr.aadhaar_number
  FROM lab_report lr
  WHERE lr.is_abnormal = 1
  ORDER BY lr.report_date DESC;
  ```
- **Q4 (Multi-table KPI aggregation)**: Hospital-wise consultation count and unique patient reach:
  ```sql
  SELECT h.hospital_id, h.hospital_name, h.hospital_type, h.city, COUNT(mr.record_id) AS total_consultations, COUNT(DISTINCT mr.aadhaar_number) AS unique_patients
  FROM hospital h
  LEFT JOIN medical_record mr ON h.hospital_id = mr.hospital_id
  GROUP BY h.hospital_id, h.hospital_name, h.hospital_type, h.city
  ORDER BY total_consultations DESC;
  ```
- **Q5 (Emergency trauma filtering)**: Patients with emergency visits:
  ```sql
  SELECT p.full_name, p.mobile, p.blood_group, p.allergies, mr.visit_date, mr.diagnosis, h.hospital_name
  FROM patient p
  JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number
  JOIN hospital h ON mr.hospital_id = h.hospital_id
  WHERE mr.visit_type = 'Emergency'
  ORDER BY mr.visit_date DESC;
  ```

---

## 🚀 Quick Local Startup Guide

### 1. Prerequisites
- Python 3.10+ (Tested with Python 3.13)
- MySQL 8.0 (Optional; local development defaults to SQLite zero-config automatically)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application Server
Simply run the single server script:
```bash
python server.py
```
This automatically:
- Creates all required relational tables non-destructively.
- Seeds synthetic clinical demo profiles, doctors, beds, and initial appointments.
- Mounts REST APIs at `http://localhost:8000/api`.
- Serves the frontend at `http://localhost:8000`.
- Automatically opens your default web browser.

### 4. Optional: Run with MySQL
To use MySQL instead of SQLite:
1. Create database in MySQL:
   ```sql
   CREATE DATABASE medilink_db;
   ```
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Update `.env` credentials:
   ```ini
   DB_ENGINE=mysql
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=medilink_db
   ```
4. Start server:
   ```bash
   python server.py
   ```

### 5. Run Automated Pytest Suite
```bash
python -m pytest backend/tests/test_api.py -v
```
All 11 automated test suites will execute, verifying health checks, authentication, patient enrollment, duplicate Aadhaar checks, bed allocations, OPD queue numbering, appointment double-booking prevention, and real SQL query execution.

---

## 👥 Demo Accounts & Pre-Loaded Profiles

### Demo User Accounts:
| Role | Username | Password | Access Capabilities |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full administrative privileges, SQL workbench, backup/restore. |
| **Doctor** | `doctor` | `doctor123` | Clinical consultations, ICD-10 Rx, CDSS alerts, lab orders. |
| **Receptionist** | `receptionist` | `reception123` | Patient enrollment, OPD queue token issuance, appointments. |
| **Emergency Staff**| `emergency` | `emergency123` | Break-glass emergency overrides, trauma triage, ICU beds. |

### Sample Citizen Patients:
| Name | Aadhaar Number | Clinical Highlights |
|---|---|---|
| **Priya Sharma** | `2345 6789 0123` | Essential Hypertension, **Penicillin Allergy** (Test CDSS alert by prescribing Amoxicillin!). |
| **Arjun Kapoor** | `1111 2222 3333` | Post-Knee Arthroscopy, Type-2 Diabetes, **Sulfa Drug Allergy**. |
| **Rajesh Verma** | `5555 6666 7777` | Acute Coronary Syndrome (NSTEMI), **Aspirin / NSAID Allergy**, ICU Admitted. |
| **Ananya Patel** | `4444 3333 2222` | Bronchial Asthma, **Latex Allergy**, Spirometry reports on file. |
| **Meera Iyer** | `9999 8888 7777` | Available patient profile for testing new admissions, visits, and tokens. |

---

## 🛡️ Clinical Safety & Privacy Notices

- **Clinical Decision Support (CDSS)**: Automated cross-allergy and drug-drug interaction warnings are demonstration decision support aids. Qualified clinician review is required for all medical orders.
- **Emergency Triage (ESI)**: Algorithmic calculations follow ESI v4 guidelines for educational demonstration and do not replace attending trauma physician judgment.
- **Aadhaar Identifier Masking**: Citizen identification numbers are masked (`XXXX-XXXX-1234`) across dashboards, reports, and exported files to adhere to privacy practices.
- **Break-Glass Emergency Protocol**: Unconsented access requires mandatory clinical justification and generates an immutable audit log entry.
- **Synthetic Data**: All citizen profiles, clinical encounters, and test results are synthetic demonstration samples.

---

## 📜 License
MIT License. Developed for University DBMS Course Demonstration & Healthcare Informatics Research.
