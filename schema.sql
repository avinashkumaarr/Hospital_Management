-- ============================================================
--  MediLink: Aadhaar-Based Unified Medical Records System
--  DBMS Course Project | SQL Schema & Complete Production Data
-- ============================================================

CREATE DATABASE IF NOT EXISTS medilink_db;
USE medilink_db;

-- Drop existing tables in reverse dependency order
DROP TABLE IF EXISTS access_log;
DROP TABLE IF EXISTS lab_report;
DROP TABLE IF EXISTS bed_allocation;
DROP TABLE IF EXISTS medical_record;
DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS hospital;
DROP TABLE IF EXISTS patient;

-- ============================================================
-- TABLE 1: PATIENT (core entity, identified by Aadhaar)
-- ============================================================
CREATE TABLE patient (
    aadhaar_number  CHAR(12)        NOT NULL,
    full_name       VARCHAR(100)    NOT NULL,
    date_of_birth   DATE            NOT NULL,
    gender          ENUM('Male','Female','Other') NOT NULL,
    blood_group     VARCHAR(5),
    mobile          VARCHAR(15),
    email           VARCHAR(100),
    address         TEXT,
    allergies       TEXT,
    chronic_conditions TEXT,
    emergency_contact VARCHAR(100),
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (aadhaar_number),
    UNIQUE KEY uk_mobile (mobile),
    INDEX idx_name (full_name)
);

-- ============================================================
-- TABLE 2: HOSPITAL
-- ============================================================
CREATE TABLE hospital (
    hospital_id         INT             AUTO_INCREMENT,
    hospital_name       VARCHAR(100)    NOT NULL,
    registration_no     VARCHAR(50)     UNIQUE,
    hospital_type       ENUM('Government','Private','Trust','Clinic') DEFAULT 'Private',
    city                VARCHAR(50),
    state               VARCHAR(50),
    pincode             CHAR(6),
    contact             VARCHAR(15),
    email               VARCHAR(100),
    is_active           BOOLEAN         DEFAULT TRUE,
    registered_at       DATETIME        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (hospital_id),
    INDEX idx_city (city),
    INDEX idx_state (state)
);

-- ============================================================
-- TABLE 3: DOCTOR
-- ============================================================
CREATE TABLE doctor (
    doctor_id       INT             AUTO_INCREMENT,
    hospital_id     INT             NOT NULL,
    doctor_name     VARCHAR(100)    NOT NULL,
    specialization  VARCHAR(50),
    qualification   VARCHAR(100),
    license_no      VARCHAR(30)     UNIQUE,
    contact         VARCHAR(15),
    email           VARCHAR(100),
    is_active       BOOLEAN         DEFAULT TRUE,

    PRIMARY KEY (doctor_id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(hospital_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_specialization (specialization)
);

-- ============================================================
-- TABLE 4: MEDICAL_RECORD (central fact table)
-- ============================================================
CREATE TABLE medical_record (
    record_id       INT             AUTO_INCREMENT,
    aadhaar_number  CHAR(12)        NOT NULL,
    hospital_id     INT             NOT NULL,
    doctor_id       INT,
    visit_date      DATE            NOT NULL,
    visit_type      ENUM('OPD Consultation','Emergency','Surgery',
                         'Inpatient Admission','Routine Checkup','Lab Tests')
                    NOT NULL,
    department      VARCHAR(50),
    chief_complaint TEXT,
    diagnosis       TEXT            NOT NULL,
    icd10_code      VARCHAR(20),
    vitals_summary  VARCHAR(255),
    prescription    TEXT,
    notes           TEXT,
    follow_up_date  DATE,
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (record_id),
    FOREIGN KEY (aadhaar_number) REFERENCES patient(aadhaar_number)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (hospital_id)   REFERENCES hospital(hospital_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (doctor_id)     REFERENCES doctor(doctor_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_aadhaar   (aadhaar_number),
    INDEX idx_date      (visit_date),
    INDEX idx_hospital  (hospital_id)
);

-- ============================================================
-- TABLE 5: LAB_REPORT (linked to a record)
-- ============================================================
CREATE TABLE lab_report (
    report_id       INT             AUTO_INCREMENT,
    record_id       INT             NOT NULL,
    aadhaar_number  CHAR(12)        NOT NULL,
    test_name       VARCHAR(100)    NOT NULL,
    result          TEXT,
    normal_range    VARCHAR(50),
    unit            VARCHAR(20),
    is_abnormal     BOOLEAN         DEFAULT FALSE,
    report_date     DATE            NOT NULL,
    file_path       VARCHAR(255),
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (report_id),
    FOREIGN KEY (record_id)      REFERENCES medical_record(record_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (aadhaar_number) REFERENCES patient(aadhaar_number)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_aadhaar (aadhaar_number),
    INDEX idx_test    (test_name)
);

-- ============================================================
-- TABLE 6: ACCESS_LOG (audit trail for inter-operability)
-- ============================================================
CREATE TABLE access_log (
    log_id          INT             AUTO_INCREMENT,
    aadhaar_number  CHAR(12)        NOT NULL,
    hospital_id     INT             NOT NULL,
    accessed_by     VARCHAR(100)    NOT NULL,
    access_time     DATETIME        DEFAULT CURRENT_TIMESTAMP,
    purpose         VARCHAR(100),
    ip_address      VARCHAR(45),
    status          VARCHAR(20)     DEFAULT 'Authorized',

    PRIMARY KEY (log_id),
    FOREIGN KEY (aadhaar_number) REFERENCES patient(aadhaar_number)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (hospital_id)   REFERENCES hospital(hospital_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_aadhaar   (aadhaar_number),
    INDEX idx_time      (access_time)
);

-- ============================================================
-- TABLE 7: BED_ALLOCATION (hospital resource management)
-- ============================================================
CREATE TABLE bed_allocation (
    allocation_id   INT             AUTO_INCREMENT,
    hospital_id     INT             NOT NULL,
    ward_name       VARCHAR(50)     NOT NULL,
    bed_number      VARCHAR(20)     NOT NULL,
    aadhaar_number  CHAR(12),
    status          ENUM('Occupied', 'Vacant', 'Maintenance', 'Reserved') DEFAULT 'Vacant',
    admitted_at     DATETIME,
    expected_discharge DATE,

    PRIMARY KEY (allocation_id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(hospital_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (aadhaar_number) REFERENCES patient(aadhaar_number)
        ON DELETE SET NULL ON UPDATE CASCADE,
    UNIQUE KEY uk_hospital_bed (hospital_id, bed_number)
);

-- ============================================================
-- SEED DATA: HOSPITALS
-- ============================================================
INSERT INTO hospital (hospital_id, hospital_name, registration_no, hospital_type, city, state, pincode, contact, email) VALUES
(1, 'AIIMS Delhi',           'REG-AIIMS-001', 'Government', 'New Delhi', 'Delhi',       '110029', '011-26588500', 'director@aiims.edu'),
(2, 'Apollo Hospitals',      'REG-APL-002',   'Private',    'New Delhi', 'Delhi',       '110076', '011-26925858', 'helpdesk@apollo.com'),
(3, 'Fortis Healthcare',     'REG-FRT-003',   'Private',    'Gurugram',  'Haryana',     '122002', '0124-4921021', 'care@fortis.com'),
(4, 'Max Super Speciality',  'REG-MAX-004',   'Private',    'New Delhi', 'Delhi',       '110017', '011-26515050', 'support@maxhealthcare.com'),
(5, 'PGIMER Chandigarh',     'REG-PGI-005',   'Government', 'Chandigarh','Chandigarh',  '160012', '0172-2746018', 'admin@pgimer.edu.in'),
(6, 'Manipal Hospital',      'REG-MAN-006',   'Private',    'Bengaluru', 'Karnataka',   '560017', '080-25024444', 'info@manipalhospitals.com');

-- ============================================================
-- SEED DATA: DOCTORS
-- ============================================================
INSERT INTO doctor (doctor_id, hospital_id, doctor_name, specialization, qualification, license_no, contact, email) VALUES
(1, 1, 'Dr. Ramesh Gupta',    'Cardiology',          'MBBS, MD, DM (Cardio)',  'DMC-CARD-1049', '9811122334', 'ramesh.gupta@aiims.edu'),
(2, 2, 'Dr. Anita Verma',     'General Medicine',    'MBBS, MD (Internal Med)','DMC-GEN-2201',  '9822233445', 'anita.verma@apollo.com'),
(3, 3, 'Dr. Sanjay Mehta',     'Pathology',           'MBBS, MD (Pathology)',   'HMC-PATH-9811', '9833344556', 'sanjay.mehta@fortis.com'),
(4, 4, 'Dr. Vikram Singh',    'Orthopaedics',        'MBBS, MS (Orthopaedics)','DMC-ORTH-5541', '9844455667', 'vikram.singh@max.com'),
(5, 5, 'Dr. Priya Nair',      'Neurology',           'MBBS, MD, DM (Neuro)',   'PMC-NEUR-7782', '9855566778', 'priya.nair@pgimer.edu.in'),
(6, 6, 'Dr. Rajesh Kulkarni', 'Emergency Medicine',  'MBBS, MD (Emergency)',   'KMC-EMER-3390', '9866677889', 'rajesh.k@manipal.com');

-- ============================================================
-- SEED DATA: PATIENTS
-- ============================================================
INSERT INTO patient (aadhaar_number, full_name, date_of_birth, gender, blood_group, mobile, email, address, allergies, chronic_conditions, emergency_contact) VALUES
('234567890123', 'Priya Sharma',  '1990-05-14', 'Female', 'B+',  '9876543210', 'priya.sharma@gmail.com',  'B-14, Sector 62, Noida, UP',      'Penicillin, Amoxicillin', 'Hypertension (Grade 1)', 'Sunil Sharma (Husband): 9876543219'),
('111122223333', 'Arjun Kapoor',  '1985-11-30', 'Male',   'O+',  '7777788888', 'arjun.kapoor@outlook.com', 'Flat 402, Palm Heights, Gurugram','Sulfa drugs, Septra',   'Type-2 Diabetes Mellitus', 'Renu Kapoor (Wife): 7777788889'),
('999988887777', 'Meera Iyer',    '2001-03-22', 'Female', 'A+',  '9900112233', 'meera.iyer@gmail.com',    '12/4 Indiranagar, Bengaluru, KA', 'None',                    'None',                    'K. Iyer (Father): 9900112244'),
('555566667777', 'Rajesh Verma',  '1968-08-19', 'Male',   'AB+', '9812345678', 'rajesh.verma@corp.in',    '77 Civil Lines, New Delhi',       'Aspirin, Ibuprofen (NSAIDs)','Coronary Artery Disease', 'Anita Verma (Wife): 9812345679'),
('444433332222', 'Ananya Patel',  '1995-12-04', 'Female', 'O-',  '9765432100', 'ananya.p@design.io',      '201 Sunrise Apts, Chandigarh',    'Latex',                   'Bronchial Asthma',        'Deepak Patel (Brother): 9765432101');

-- ============================================================
-- SEED DATA: MEDICAL RECORDS
-- ============================================================
INSERT INTO medical_record (record_id, aadhaar_number, hospital_id, doctor_id, visit_date, visit_type, department, chief_complaint, diagnosis, icd10_code, vitals_summary, prescription, notes, follow_up_date) VALUES
(1, '234567890123', 2, 2, '2024-01-10', 'OPD Consultation',   'Cardiology',       'Persistent headaches, evening dizziness', 'Hypertension (Grade 1)', 'I10',     'BP: 145/95 mmHg, HR: 82 bpm, SpO2: 98%', 'Tab Amlodipine 5mg OD morning, Low sodium diet, 30 min daily brisk walk', 'Patient advised to monitor BP daily and record readings in app.', '2024-02-10'),
(2, '234567890123', 1, 1, '2023-07-22', 'Routine Checkup',    'General Medicine', 'Executive annual checkup',                 'Vitamin D Deficiency',   'E55.9',   'BP: 128/84 mmHg, HR: 74 bpm, SpO2: 99%', 'Cap Vitamin D3 60,000 IU weekly x 8 weeks, then monthly', 'All other metabolic parameters within acceptable limits.', '2024-01-20'),
(3, '234567890123', 3, 3, '2022-03-05', 'Lab Tests',          'Pathology',        'Routine health screening panel',          'Borderline Dyslipidemia','E78.5',   'BP: 130/85 mmHg, HR: 76 bpm, SpO2: 98%', 'Dietary modifications, reduce saturated fats, retest lipid profile in 6 months', 'HbA1c normal (5.6%). Total Cholesterol mildly elevated.', '2022-09-05'),
(4, '111122223333', 4, 4, '2024-03-18', 'Surgery',            'Orthopaedics',     'Right knee lock and acute pain after sports injury', 'Meniscus Tear (Right Knee) - Post Arthroscopy', 'M23.22', 'BP: 122/80 mmHg, HR: 78 bpm, SpO2: 99%', 'Tab Paracetamol 650mg TDS PRN, Ice pack application, Physiotherapy 3x/week x 6 weeks', 'Arthroscopic partial meniscectomy performed uneventfully.', '2024-04-15'),
(5, '111122223333', 6, 6, '2023-12-01', 'Emergency',          'Emergency Medicine', 'Severe abdominal cramps, vomiting and dehydration', 'Acute Gastroenteritis with Moderate Dehydration', 'A09', 'BP: 105/70 mmHg, HR: 102 bpm, SpO2: 98%', 'IV Normal Saline 1000ml stat, Tab Ondansetron 4mg TDS, ORS sachet ad libitum', 'Patient stabilized in emergency bay and discharged same evening.', '2023-12-07'),
(6, '555566667777', 1, 1, '2024-02-14', 'Emergency',          'Cardiology',       'Substernal crushing chest pain radiating to left arm', 'Acute Coronary Syndrome (NSTEMI)', 'I21.4', 'BP: 160/100 mmHg, HR: 110 bpm, SpO2: 94%', 'Tab Clopidogrel 300mg stat, Tab Atorvastatin 80mg, Sublingual Nitroglycerin 0.5mg PRN', 'Emergency angiogram revealed LAD 70% stenosis. Stent placed successfully.', '2024-03-01'),
(7, '444433332222', 5, 5, '2024-01-28', 'OPD Consultation',   'Pulmonology',      'Exertional wheezing and nocturnal dry cough', 'Bronchial Asthma (Moderate Persistent)', 'J45.40', 'BP: 118/76 mmHg, HR: 88 bpm, SpO2: 95%', 'Budesonide + Formoterol Inhaler 200/6mcg 2 puffs BD, Tab Montelukast 10mg OD HS', 'Asthma Action Plan reviewed. Advised to avoid dust and latex gloves.', '2024-04-28');

-- ============================================================
-- SEED DATA: LAB REPORTS
-- ============================================================
INSERT INTO lab_report (report_id, record_id, aadhaar_number, test_name, result, normal_range, unit, is_abnormal, report_date) VALUES
(1, 1, '234567890123', 'Serum Creatinine',        '0.9',   '0.6 - 1.2',  'mg/dL', FALSE, '2024-01-11'),
(2, 1, '234567890123', 'Serum Potassium',         '4.2',   '3.5 - 5.0',  'mEq/L', FALSE, '2024-01-11'),
(3, 2, '234567890123', 'Serum 25-OH Vitamin D',   '14.2',  '30.0 - 100.0','ng/mL', TRUE,  '2023-07-23'),
(4, 3, '234567890123', 'HbA1c (Glycated Hb)',      '5.6',   '< 5.7',      '%',     FALSE, '2022-03-06'),
(5, 3, '234567890123', 'Total Cholesterol',        '228',   '< 200',      'mg/dL', TRUE,  '2022-03-06'),
(6, 3, '234567890123', 'LDL Cholesterol',          '148',   '< 100',      'mg/dL', TRUE,  '2022-03-06'),
(7, 4, '111122223333', 'Knee MRI Scan (Right)',    'Complex tear posterior horn medial meniscus', 'Intact meniscus', 'Imaging', TRUE, '2024-03-16'),
(8, 5, '111122223333', 'Serum Electrolytes (Sodium)','132', '136 - 145', 'mEq/L', TRUE,  '2023-12-01'),
(9, 6, '555566667777', 'Cardiac Troponin-I',       '0.84',  '< 0.04',     'ng/mL', TRUE,  '2024-02-14'),
(10, 6, '555566667777', '12-Lead ECG',            'ST segment depression in V4-V6', 'Normal Sinus Rhythm', 'ECG', TRUE, '2024-02-14'),
(11, 7, '444433332222', 'Spirometry (FEV1/FVC)',   '68%',   '> 75%',      '%',     TRUE,  '2024-01-29');

-- ============================================================
-- SEED DATA: ACCESS LOGS (Audit Trail)
-- ============================================================
INSERT INTO access_log (log_id, aadhaar_number, hospital_id, accessed_by, access_time, purpose, ip_address, status) VALUES
(1, '234567890123', 2, 'Dr. Anita Verma (Apollo)',    '2024-01-10 10:14:00', 'OPD Cardiology Consultation', '192.168.1.45', 'Authorized'),
(2, '234567890123', 1, 'Dr. Ramesh Gupta (AIIMS)',    '2023-07-22 09:30:15', 'Routine Health Checkup',       '10.20.14.88',  'Authorized'),
(3, '111122223333', 4, 'Dr. Vikram Singh (Max)',      '2024-03-18 11:00:22', 'Pre-Operative Ortho Review',   '172.16.5.12',  'Authorized'),
(4, '555566667777', 1, 'Dr. Ramesh Gupta (AIIMS)',    '2024-02-14 02:45:10', 'Break-Glass Emergency Resuscitation', '10.20.14.99', 'Authorized'),
(5, '444433332222', 5, 'Dr. Priya Nair (PGIMER)',     '2024-01-28 14:20:00', 'Outpatient Pulmonology Review', '192.168.10.15', 'Authorized');

-- ============================================================
-- SEED DATA: BED ALLOCATIONS
-- ============================================================
INSERT INTO bed_allocation (allocation_id, hospital_id, ward_name, bed_number, aadhaar_number, status, admitted_at, expected_discharge) VALUES
(1, 1, 'Emergency Trauma Bay', 'ER-101', '555566667777', 'Occupied', '2024-02-14 02:30:00', '2024-02-18'),
(2, 1, 'Emergency Trauma Bay', 'ER-102', NULL,           'Vacant',   NULL, NULL),
(3, 1, 'Intensive Care Unit',   'ICU-201','555566667777', 'Occupied', '2024-02-14 05:00:00', '2024-02-20'),
(4, 1, 'Intensive Care Unit',   'ICU-202', NULL,          'Vacant',   NULL, NULL),
(5, 2, 'Cardiac HDU',           'HDU-301', '234567890123', 'Occupied', '2024-01-10 11:00:00', '2024-01-12'),
(6, 2, 'Cardiac HDU',           'HDU-302', NULL,          'Vacant',   NULL, NULL),
(7, 4, 'Surgical Post-Op Ward', 'SPW-401', '111122223333', 'Occupied', '2024-03-18 14:00:00', '2024-03-21'),
(8, 4, 'Surgical Post-Op Ward', 'SPW-402', NULL,          'Vacant',   NULL, NULL);

-- ============================================================
-- IMPORTANT PRODUCTION QUERIES
-- ============================================================

-- Q1: Full medical history of a patient using Aadhaar
SELECT
    mr.record_id,
    mr.visit_date,
    mr.visit_type,
    mr.department,
    mr.diagnosis,
    mr.icd10_code,
    mr.prescription,
    h.hospital_name,
    h.city,
    d.doctor_name,
    d.specialization
FROM medical_record mr
JOIN hospital h ON mr.hospital_id = h.hospital_id
LEFT JOIN doctor d ON mr.doctor_id = d.doctor_id
WHERE mr.aadhaar_number = '234567890123'
ORDER BY mr.visit_date DESC;

-- Q2: Patient profile with latest record and aggregate visit statistics
SELECT
    p.aadhaar_number,
    p.full_name,
    p.date_of_birth,
    p.gender,
    p.blood_group,
    p.allergies,
    p.chronic_conditions,
    COUNT(mr.record_id) AS total_visits,
    MAX(mr.visit_date) AS last_visit_date
FROM patient p
LEFT JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number
WHERE p.aadhaar_number = '234567890123'
GROUP BY p.aadhaar_number;

-- Q3: All abnormal lab reports across hospitals for a specific patient
SELECT
    lr.test_name,
    lr.result,
    lr.normal_range,
    lr.unit,
    lr.report_date,
    h.hospital_name,
    d.doctor_name
FROM lab_report lr
JOIN medical_record mr ON lr.record_id = mr.record_id
JOIN hospital h ON mr.hospital_id = h.hospital_id
LEFT JOIN doctor d ON mr.doctor_id = d.doctor_id
WHERE lr.aadhaar_number = '234567890123'
  AND lr.is_abnormal = TRUE
ORDER BY lr.report_date DESC;

-- Q4: Hospital-wise visit count and unique patient reach (Hospital Dashboard KPI)
SELECT
    h.hospital_id,
    h.hospital_name,
    h.hospital_type,
    h.city,
    COUNT(mr.record_id) AS total_visits,
    COUNT(DISTINCT mr.aadhaar_number) AS unique_patients
FROM hospital h
LEFT JOIN medical_record mr ON h.hospital_id = mr.hospital_id
GROUP BY h.hospital_id
ORDER BY total_visits DESC;

-- Q5: Patients with emergency visits in the past 90 days
SELECT DISTINCT
    p.full_name,
    p.mobile,
    p.blood_group,
    p.allergies,
    mr.visit_date,
    mr.diagnosis,
    h.hospital_name
FROM patient p
JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number
JOIN hospital h ON mr.hospital_id = h.hospital_id
WHERE mr.visit_type = 'Emergency'
ORDER BY mr.visit_date DESC;
