# MediLink: Aadhaar-Based Unified Medical Records System
> **An Intelligent, Interoperable Electronic Medical Record (EMR) & Hospital Management System**  
> Compliant with the Ayushman Bharat Digital Mission (ABDM) & DISHA/HIPAA standards.

![MediLink Banner](https://img.shields.io/badge/System-MediLink_v2.4_Enterprise-06b6d4?style=for-the-badge&logo=medicare)
![Status](https://img.shields.io/badge/Status-Production_Ready-10b981?style=for-the-badge)
![DBMS Project](https://img.shields.io/badge/Database-MySQL_Relational_Schema-6366f1?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-amber?style=for-the-badge)

---

## 🌟 Executive Overview

**MediLink** addresses a fundamental challenge in national healthcare systems: **fragmented patient records**. When patients visit different hospitals (e.g., AIIMS, Apollo, Fortis, Max), their vital medical history, previous drug allergies, surgical notes, and diagnostic test reports are scattered across disconnected systems.

With **MediLink**, every citizen is identified via their verified **12-digit Aadhaar UID** linked to an ABDM Health ID. Any authorized hospital node can retrieve a patient's lifelong health timeline in milliseconds, preventing catastrophic medical errors, duplicate lab investigations, and adverse drug reactions.

---

## 🧠 Intelligent & Clinical Features

### 1. 🛡️ AI Clinical Decision Support (CDSS) & Allergy Protection
- **Real-Time Cross-Allergy Detection**: Scans entered prescriptions in real-time against patient allergens. For example, if a patient has a documented **Penicillin** allergy, prescribing *Amoxicillin*, *Ampicillin*, or *Augmentin* immediately raises a high-priority red alert explaining the beta-lactam anaphylactic risk.
- **Drug-Drug Interaction Checker**: Evaluates dangerous pharmacological combinations (e.g., *Warfarin + Aspirin* [major bleeding hazard], *Metformin + Contrast dye* [lactic acidosis risk], *Sildenafil + Nitrates* [fatal hypotension]).
- **Vitals Anomaly Tagger**: Live analyzer evaluating Systolic/Diastolic BP, Heart Rate, SpO2, and Temperature, flagging Stage 2 Hypertension, Tachycardia, or Hypoxia with clinical tags.

### 2. 🚑 Emergency Severity Index (ESI 1–5) Triage Engine
- Algorithmic emergency triage calculator based on the 5-level **Emergency Severity Index (ESI)** used in top trauma centers:
  - **ESI 1 (Resuscitation)**: Immediate life-saving intervention needed (Trauma Resuscitation Bay 1).
  - **ESI 2 (Emergent)**: High-risk presentation, severe pain, or unstable vitals (Acute Monitored Bed).
  - **ESI 3 (Urgent)**: Stable vitals requiring 2+ diagnostic/therapeutic resources (Observation Ward).
  - **ESI 4 (Less Urgent)**: Single resource required (Fast Track / Minor Treatment).
  - **ESI 5 (Non-urgent)**: Routine exam or medication refill (Standard OPD).

### 3. 🎙️ Clinical Voice-to-Text Dictation
- Integrated **Web Speech Recognition** tool allowing physicians to speak clinical notes and physical examination findings hands-free with real-time transcription.

### 4. 🏷️ Smart ICD-10 Code & Guideline Suggester
- As doctors type diagnoses (e.g., *Hypertension*, *Type 2 Diabetes*, *Acute Appendicitis*, *Asthma*), official ICD-10 codes (*I10*, *E11.9*, *K35.80*, *J45.909*) are suggested with 1-click evidence-based prescription templates.

### 5. 🚨 Break-Glass Emergency Access Protocol
- Instant one-click clinical snapshot for emergency doctors & trauma surgeons: retrieves critical life-saving information (blood group, fatal allergies, chronic conditions, active medications, emergency contacts) and records an immutable audit log entry.

### 6. 🖨️ Official Prescription Slip & Discharge Summary
- Generates official, print-ready encounter slips complete with hospital header, NABH accreditation badge, patient demographics, clinical diagnosis, Rx medications table, verification barcode, and doctor's digital signature block.

### 7. 🪪 Digital ABHA / Aadhaar Smart Health Card
- Generates a physical-look digital health ID card complete with patient photo avatar, gold security chip graphic, blood group badge, demographic info, barcode, and interoperable QR code.

---

## 🏥 Hospital Management Operations

| Module | Capability Description |
| :--- | :--- |
| **Ward & Bed Management** | Interactive bed occupancy matrix across Emergency Trauma Bay, ICU, Cardiac HDU, and Surgical Post-Op. Color-coded (Occupied, Vacant, Cleaning) with 1-click patient admission & discharge. |
| **OPD Live Token Queue** | Public consultation room token calling screen with auditory chime notification, now-serving hero board, and walk-in token issuance. |
| **Hospital Network Analytics** | Interactive Chart.js visualizations: Department volume distribution, cross-hospital network activity, and 1-click encounter ledger export to CSV. |
| **Audit Trail (HIPAA/DISHA)** | Comprehensive access log recording timestamp, accessing clinician, hospital node, purpose, IP address, and authorization status. |
| **SQL Query Workbench** | Interactive schema viewer + live SQL query runner executing the 5 core DBMS course queries with tabulated results and execution benchmarking. |
| **Data Engine & Backup** | Browser-persistent `localStorage` engine with JSON export, backup restore, and factory reset capabilities. |

---

## 🗄️ Relational Database Architecture (`schema.sql`)

The database architecture consists of 7 normalized relational tables:

```
+---------------+        1:N        +------------------+
|    PATIENT    | <---------------- |  MEDICAL_RECORD  |
|  (Aadhaar PK) |                   |   (Central Fact) |
+---------------+                   +------------------+
        |                                     |
        | 1:N                                 | 1:N
        v                                     v
+---------------+                   +------------------+
|  ACCESS_LOG   |                   |    LAB_REPORT    |
| (Audit Trail) |                   |   (Diagnostic)   |
+---------------+                   +------------------+
        ^                                     ^
        |                                     |
+---------------+        1:N        +------------------+
|   HOSPITAL    | ----------------> |      DOCTOR      |
| (Facility PK) |                   |    (Staff FK)    |
+---------------+                   +------------------+
        |
        | 1:N
        v
+------------------+
|  BED_ALLOCATION  |
|    (Resources)   |
+------------------+
```

### Table Overview
1. **`patient`**: Primary key `aadhaar_number` (CHAR 12). Stores demographics, blood group, documented allergies, chronic conditions, and emergency contacts.
2. **`hospital`**: Facility details, registration numbers, types (Government, Private, Trust), and locations.
3. **`doctor`**: Medical practitioners with hospital foreign key, specializations, qualifications, and license numbers.
4. **`medical_record`**: Central fact table storing visits, departments, chief complaints, ICD-10 diagnosis, vital signs, prescriptions, and follow-ups.
5. **`lab_report`**: Laboratory investigations linked to both patient and medical record, with reference intervals and abnormal flags (`is_abnormal`).
6. **`access_log`**: Security audit trail recording every cross-hospital query.
7. **`bed_allocation`**: Ward room and bed status management (`Occupied`, `Vacant`, `Cleaning`, `Reserved`).

---

## 🚀 Quick Start Guide

### Option 1: Open Directly in Any Browser
No installations or dependencies required!
- Simply double-click **`index.html`** or open it in Chrome, Edge, Safari, or Firefox.

### Option 2: Run with Python Local Server
```bash
# Clone the repository
git clone https://github.com/avinashkumaarr/Hospital_Management.git
cd Hospital_Management

# Launch local preview server
python server.py
```
Open **`http://localhost:8000`** in your browser.

### Option 3: Deploy to GitHub Pages
1. Go to repository **Settings** → **Pages**.
2. Select **Branch: master**, Folder: `/ (root)`.
3. Click **Save** — MediLink will be deployed live worldwide with zero configuration!

---

## 🧪 Pre-Configured Sample Patients

You can test the system immediately using any of these pre-loaded demo profiles:

| Name | Aadhaar Number | Clinical Highlights |
| :--- | :--- | :--- |
| **Priya Sharma** | `2345 6789 0123` | Essential Hypertension, **Penicillin Allergy** (Test CDSS alert by prescribing Amoxicillin!) |
| **Arjun Kapoor** | `1111 2222 3333` | Post-Knee Arthroscopy, Type-2 Diabetes, **Sulfa Drug Allergy** |
| **Rajesh Verma** | `5555 6666 7777` | Acute Coronary Syndrome (NSTEMI), **Aspirin / NSAID Allergy**, ICU Admitted |
| **Ananya Patel** | `4444 3333 2222` | Bronchial Asthma, **Latex Allergy**, Spirometry Lab Reports |
| **Meera Iyer** | `9999 8888 7777` | Clean Profile for testing new visit and token allocation workflows |

---

## 💡 DBMS Course Evaluation Queries (Q1–Q5)

All 5 core course evaluation queries are pre-configured in the interactive **SQL Workbench**:
- **Q1**: Retrieve lifelong medical history of any patient across all hospitals using Aadhaar UID (`JOIN patient`, `hospital`, `doctor`).
- **Q2**: Aggregate patient visit volume and identify most recent consultation date.
- **Q3**: Query all abnormal lab test values across all facilities with reference intervals.
- **Q4**: Compute hospital-wise consultation volume and unique patient reach.
- **Q5**: Filter all emergency triage visits in the past 90 days.

---

## 📄 License
This project is open-source under the MIT License. Developed for DBMS / Medical Informatics research and academic demonstration.
