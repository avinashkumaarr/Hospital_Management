-- ============================================================
--  MediLink: Aadhaar-Based Unified Medical Records System
--  DBMS Course Project | Extended Production Relational Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS medilink_db;
USE medilink_db;

-- ============================================================
-- TABLE 1: PATIENT (core citizen entity, identified by Aadhaar)
-- ============================================================
CREATE TABLE IF NOT EXISTS patient (
    aadhaar_number      VARCHAR(14)     NOT NULL,
    full_name           VARCHAR(100)    NOT NULL,
    date_of_birth       DATE            NOT NULL,
    gender              ENUM('Male','Female','Other') NOT NULL,
    blood_group         VARCHAR(10),
    mobile              VARCHAR(25),
    email               VARCHAR(100),
    address             TEXT,
    allergies           TEXT,
    chronic_conditions  TEXT,
    emergency_contact   VARCHAR(150),
    created_at          DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (aadhaar_number),
    UNIQUE KEY uk_patient_mobile (mobile),
    INDEX idx_patient_name (full_name)
);

-- ============================================================
-- TABLE 2: HOSPITAL
-- ============================================================
CREATE TABLE IF NOT EXISTS hospital (
    hospital_id         INT             AUTO_INCREMENT,
    hospital_name       VARCHAR(100)    NOT NULL,
    registration_no     VARCHAR(50)     UNIQUE,
    hospital_type       ENUM('Government','Private','Trust','Clinic') DEFAULT 'Private',
    city                VARCHAR(50),
    state               VARCHAR(50),
    pincode             CHAR(10),
    contact             VARCHAR(25),
    email               VARCHAR(100),
    is_active           BOOLEAN         DEFAULT TRUE,
    registered_at       DATETIME        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (hospital_id),
    INDEX idx_hospital_city (city),
    INDEX idx_hospital_state (state)
);

-- ============================================================
-- TABLE 3: DOCTOR
-- ============================================================
CREATE TABLE IF NOT EXISTS doctor (
    doctor_id       INT             AUTO_INCREMENT,
    hospital_id     INT             NOT NULL,
    doctor_name     VARCHAR(100)    NOT NULL,
    specialization  VARCHAR(50),
    qualification   VARCHAR(100),
    license_no      VARCHAR(30)     UNIQUE,
    contact         VARCHAR(25),
    email           VARCHAR(100),
    is_active       BOOLEAN         DEFAULT TRUE,

    PRIMARY KEY (doctor_id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(hospital_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_doctor_specialization (specialization)
);

-- ============================================================
-- TABLE 4: MEDICAL_RECORD (central fact table)
-- ============================================================
CREATE TABLE IF NOT EXISTS medical_record (
    record_id       INT             AUTO_INCREMENT,
    aadhaar_number  VARCHAR(14)     NOT NULL,
    hospital_id     INT             NOT NULL,
    doctor_id       INT,
    visit_date      DATE            NOT NULL,
    visit_type      VARCHAR(50)     NOT NULL,
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
    INDEX idx_record_aadhaar   (aadhaar_number),
    INDEX idx_record_date      (visit_date),
    INDEX idx_record_hospital  (hospital_id)
);

-- ============================================================
-- TABLE 5: LAB_REPORT (diagnostic investigations)
-- ============================================================
CREATE TABLE IF NOT EXISTS lab_report (
    report_id       INT             AUTO_INCREMENT,
    record_id       INT,
    aadhaar_number  VARCHAR(14)     NOT NULL,
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
    INDEX idx_lab_aadhaar (aadhaar_number),
    INDEX idx_lab_test    (test_name)
);

-- ============================================================
-- TABLE 6: ACCESS_LOG (security & interoperability audit trail)
-- ============================================================
CREATE TABLE IF NOT EXISTS access_log (
    log_id          INT             AUTO_INCREMENT,
    aadhaar_number  VARCHAR(14)     NOT NULL,
    hospital_id     INT,
    accessed_by     VARCHAR(100)    NOT NULL,
    access_time     DATETIME        DEFAULT CURRENT_TIMESTAMP,
    purpose         VARCHAR(150),
    ip_address      VARCHAR(45),
    status          VARCHAR(20)     DEFAULT 'Authorized',

    PRIMARY KEY (log_id),
    FOREIGN KEY (aadhaar_number) REFERENCES patient(aadhaar_number)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (hospital_id)   REFERENCES hospital(hospital_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_log_aadhaar   (aadhaar_number),
    INDEX idx_log_time      (access_time)
);

-- ============================================================
-- TABLE 7: BED_ALLOCATION (ward resource management)
-- ============================================================
CREATE TABLE IF NOT EXISTS bed_allocation (
    allocation_id   INT             AUTO_INCREMENT,
    hospital_id     INT             NOT NULL,
    ward_name       VARCHAR(50)     NOT NULL,
    bed_number      VARCHAR(20)     NOT NULL,
    aadhaar_number  VARCHAR(14),
    status          ENUM('Occupied', 'Vacant', 'Cleaning', 'Reserved') DEFAULT 'Vacant',
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
-- TABLE 8: APPOINTMENT (scheduled doctor consultations)
-- ============================================================
CREATE TABLE IF NOT EXISTS appointment (
    appointment_id      INT             AUTO_INCREMENT,
    aadhaar_number      VARCHAR(14)     NOT NULL,
    doctor_id           INT             NOT NULL,
    hospital_id         INT             NOT NULL,
    department          VARCHAR(50),
    appointment_date    DATE            NOT NULL,
    time_slot           VARCHAR(20)     NOT NULL,
    reason              VARCHAR(255),
    status              VARCHAR(20)     DEFAULT 'Scheduled',
    created_at          DATETIME        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (appointment_id),
    FOREIGN KEY (aadhaar_number) REFERENCES patient(aadhaar_number)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (doctor_id)     REFERENCES doctor(doctor_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (hospital_id)   REFERENCES hospital(hospital_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE KEY uk_doctor_slot (doctor_id, appointment_date, time_slot),
    INDEX idx_appt_date (appointment_date)
);

-- ============================================================
-- TABLE 9: OPD_QUEUE (daily outpatient consultation tokens)
-- ============================================================
CREATE TABLE IF NOT EXISTS opd_queue (
    queue_id        INT             AUTO_INCREMENT,
    token_number    VARCHAR(20)     NOT NULL,
    aadhaar_number  VARCHAR(14)     NOT NULL,
    doctor_id       INT,
    hospital_id     INT             NOT NULL,
    queue_date      DATE            NOT NULL,
    status          VARCHAR(20)     DEFAULT 'Waiting',
    time_issued     VARCHAR(20)     NOT NULL,
    completed_at    DATETIME,

    PRIMARY KEY (queue_id),
    FOREIGN KEY (aadhaar_number) REFERENCES patient(aadhaar_number)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (doctor_id)     REFERENCES doctor(doctor_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (hospital_id)   REFERENCES hospital(hospital_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_queue_date (queue_date)
);

-- ============================================================
-- TABLE 10: USER (authentication & role-based access control)
-- ============================================================
CREATE TABLE IF NOT EXISTS `user` (
    user_id         INT             AUTO_INCREMENT,
    username        VARCHAR(50)     NOT NULL UNIQUE,
    password_hash   VARCHAR(255)    NOT NULL,
    full_name       VARCHAR(100)    NOT NULL,
    role            ENUM('Administrator', 'Doctor', 'Receptionist', 'Emergency Staff') NOT NULL,
    doctor_id       INT,
    hospital_id     INT,
    email           VARCHAR(100),
    phone           VARCHAR(20),
    is_active       BOOLEAN         DEFAULT TRUE,
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id),
    FOREIGN KEY (doctor_id)     REFERENCES doctor(doctor_id)
        ON DELETE SET NULL,
    FOREIGN KEY (hospital_id)   REFERENCES hospital(hospital_id)
        ON DELETE SET NULL
);

-- ============================================================
-- TABLE 11: NOTIFICATION (in-app clinical notifications)
-- ============================================================
CREATE TABLE IF NOT EXISTS notification (
    notification_id     INT             AUTO_INCREMENT,
    user_id             INT,
    role                VARCHAR(30),
    title               VARCHAR(100)    NOT NULL,
    message             TEXT            NOT NULL,
    notification_type   VARCHAR(30)     DEFAULT 'info',
    is_read             BOOLEAN         DEFAULT FALSE,
    link                VARCHAR(100),
    created_at          DATETIME        DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (notification_id),
    FOREIGN KEY (user_id) REFERENCES `user`(user_id) ON DELETE CASCADE
);

-- ============================================================
-- SEED DATA: HOSPITALS
-- ============================================================
INSERT IGNORE INTO hospital (hospital_id, hospital_name, registration_no, hospital_type, city, state, pincode, contact, email) VALUES
(1, 'AIIMS Delhi',           'REG-AIIMS-001', 'Government', 'New Delhi', 'Delhi',       '110029', '011-26588500', 'director@aiims.edu'),
(2, 'Apollo Hospitals',      'REG-APL-002',   'Private',    'New Delhi', 'Delhi',       '110076', '011-26925858', 'helpdesk@apollo.com'),
(3, 'Fortis Healthcare',     'REG-FRT-003',   'Private',    'Gurugram',  'Haryana',     '122002', '0124-4921021', 'care@fortis.com'),
(4, 'Max Super Speciality',  'REG-MAX-004',   'Private',    'New Delhi', 'Delhi',       '110017', '011-26515050', 'support@maxhealthcare.com'),
(5, 'PGIMER Chandigarh',     'REG-PGI-005',   'Government', 'Chandigarh','Chandigarh',  '160012', '0172-2746018', 'admin@pgimer.edu.in'),
(6, 'Manipal Hospital',      'REG-MAN-006',   'Private',    'Bengaluru', 'Karnataka',   '560017', '080-25024444', 'info@manipalhospitals.com');

-- ============================================================
-- SEED DATA: DOCTORS
-- ============================================================
INSERT IGNORE INTO doctor (doctor_id, hospital_id, doctor_name, specialization, qualification, license_no, contact, email) VALUES
(1, 1, 'Dr. Ramesh Gupta',    'Cardiology',          'MBBS, MD, DM (Cardio)',  'DMC-CARD-1049', '9811122334', 'ramesh.gupta@aiims.edu'),
(2, 2, 'Dr. Anita Verma',     'General Medicine',    'MBBS, MD (Internal Med)','DMC-GEN-2201',  '9822233445', 'anita.verma@apollo.com'),
(3, 3, 'Dr. Sanjay Mehta',     'Pathology',           'MBBS, MD (Pathology)',   'HMC-PATH-9811', '9833344556', 'sanjay.mehta@fortis.com'),
(4, 4, 'Dr. Vikram Singh',    'Orthopaedics',        'MBBS, MS (Orthopaedics)','DMC-ORTH-5541', '9844455667', 'vikram.singh@max.com'),
(5, 5, 'Dr. Priya Nair',      'Neurology',           'MBBS, MD, DM (Neuro)',   'PMC-NEUR-7782', '9855566778', 'priya.nair@pgimer.edu.in'),
(6, 6, 'Dr. Rajesh Kulkarni', 'Emergency Medicine',  'MBBS, MD (Emergency)',   'KMC-EMER-3390', '9866677889', 'rajesh.k@manipal.com');

-- ============================================================
-- SEED DATA: PATIENTS
-- ============================================================
INSERT IGNORE INTO patient (aadhaar_number, full_name, date_of_birth, gender, blood_group, mobile, email, address, allergies, chronic_conditions, emergency_contact) VALUES
('2345 6789 0123', 'Priya Sharma',  '1990-05-14', 'Female', 'B+',  '+91 98765 43210', 'priya.sharma@gmail.com',  'B-14, Sector 62, Noida, Uttar Pradesh', 'Penicillin, Amoxicillin', 'Hypertension (Grade 1)', 'Sunil Sharma (Husband): +91 98765 43219'),
('1111 2222 3333', 'Arjun Kapoor',  '1985-11-30', 'Male',   'O+',  '+91 77777 88888', 'arjun.kapoor@outlook.com', 'Flat 402, Palm Heights, Gurugram, Haryana','Sulfa drugs, Septra',   'Type-2 Diabetes Mellitus', 'Renu Kapoor (Wife): +91 77777 88889'),
('9999 8888 7777', 'Meera Iyer',    '2001-03-22', 'Female', 'A+',  '+91 99001 12233', 'meera.iyer@gmail.com',    '12/4 Indiranagar, Bengaluru, Karnataka', 'None',                    'None',                    'K. Iyer (Father): +91 99001 12244'),
('5555 6666 7777', 'Rajesh Verma',  '1968-08-19', 'Male',   'AB+', '+91 98123 45678', 'rajesh.verma@corp.in',    '77 Civil Lines, New Delhi',              'Aspirin, Ibuprofen (NSAIDs)','Coronary Artery Disease', 'Anita Verma (Wife): +91 98123 45679'),
('4444 3333 2222', 'Ananya Patel',  '1995-12-04', 'Female', 'O-',  '+91 97654 32100', 'ananya.p@design.io',      '201 Sunrise Apts, Chandigarh',           'Latex',                   'Bronchial Asthma',        'Deepak Patel (Brother): +91 97654 32101');

-- ============================================================
-- SEED DATA: MEDICAL RECORDS
-- ============================================================
INSERT IGNORE INTO medical_record (record_id, aadhaar_number, hospital_id, doctor_id, visit_date, visit_type, department, chief_complaint, diagnosis, icd10_code, vitals_summary, prescription, notes, follow_up_date) VALUES
(1, '2345 6789 0123', 2, 2, '2024-01-10', 'OPD Consultation',   'Cardiology',       'Persistent headaches, evening dizziness', 'Essential Hypertension (Grade 1)', 'I10',     'BP: 145/95 mmHg, HR: 82 bpm, SpO2: 98%, Temp: 98.4°F', 'Tab Amlodipine 5mg OD morning x 30 days\nLow sodium diet (< 2g/day)\n30 min daily brisk aerobic walking', 'Patient presented with tension headaches. Fundoscopy normal. Advised home BP monitoring.', '2024-02-10'),
(2, '2345 6789 0123', 1, 1, '2023-07-22', 'Routine Checkup',    'General Medicine', 'Executive annual checkup',                 'Vitamin D Deficiency',             'E55.9',   'BP: 128/84 mmHg, HR: 74 bpm, SpO2: 99%, Temp: 98.6°F', 'Cap Vitamin D3 60,000 IU weekly x 8 weeks, then monthly', 'Annual executive screening. Mild fatigue reported. Metabolic parameters normal.', '2024-01-20'),
(3, '2345 6789 0123', 3, 3, '2022-03-05', 'Lab Tests',          'Pathology',        'Routine health screening panel',          'Borderline Dyslipidemia',          'E78.5',   'BP: 130/85 mmHg, HR: 76 bpm, SpO2: 98%, Temp: 98.2°F', 'Dietary modifications, reduce saturated fats, retest lipid profile in 6 months', 'Lipid panel demonstrated mild LDL elevation.', '2022-09-05'),
(4, '1111 2222 3333', 4, 4, '2024-03-18', 'Surgery',            'Orthopaedics',     'Right knee lock and acute pain after sports injury', 'Meniscus Tear (Right Knee) - Post Arthroscopy', 'M23.22', 'BP: 122/80 mmHg, HR: 78 bpm, SpO2: 99%, Temp: 98.6°F', 'Tab Paracetamol 650mg TDS PRN, Ice pack application, Physiotherapy 3x/week x 6 weeks', 'Arthroscopic partial meniscectomy performed uneventfully.', '2024-04-15'),
(5, '1111 2222 3333', 6, 6, '2023-12-01', 'Emergency',          'Emergency Medicine', 'Severe abdominal cramps, vomiting and dehydration', 'Acute Gastroenteritis with Moderate Dehydration', 'A09', 'BP: 105/70 mmHg, HR: 102 bpm, SpO2: 98%, Temp: 99.1°F', 'IV Normal Saline 1000ml stat, Tab Ondansetron 4mg TDS, ORS sachet ad libitum', 'Patient stabilized in emergency bay and discharged same evening.', '2023-12-07'),
(6, '5555 6666 7777', 1, 1, '2024-02-14', 'Emergency',          'Cardiology',       'Substernal crushing chest pain radiating to left arm', 'Acute Coronary Syndrome (NSTEMI)', 'I21.4', 'BP: 160/100 mmHg, HR: 110 bpm, SpO2: 94%, Temp: 98.4°F', 'Tab Clopidogrel 300mg stat, Tab Atorvastatin 80mg, Sublingual Nitroglycerin 0.5mg PRN', 'Emergency angiogram revealed LAD 70% stenosis. Stent placed successfully.', '2024-03-01'),
(7, '4444 3333 2222', 5, 5, '2024-01-28', 'OPD Consultation',   'Pulmonology',      'Exertional wheezing and nocturnal dry cough', 'Bronchial Asthma (Moderate Persistent)', 'J45.40', 'BP: 118/76 mmHg, HR: 88 bpm, SpO2: 95%, Temp: 98.6°F', 'Budesonide + Formoterol Inhaler 200/6mcg 2 puffs BD, Tab Montelukast 10mg OD HS', 'Asthma Action Plan reviewed. Advised to avoid dust and latex gloves.', '2024-04-28');

-- ============================================================
-- SEED DATA: LAB REPORTS
-- ============================================================
INSERT IGNORE INTO lab_report (report_id, record_id, aadhaar_number, test_name, result, normal_range, unit, is_abnormal, report_date) VALUES
(1, 1, '2345 6789 0123', 'Serum Creatinine',        '0.9',   '0.6 - 1.2',  'mg/dL', FALSE, '2024-01-11'),
(2, 1, '2345 6789 0123', 'Serum Potassium',         '4.2',   '3.5 - 5.0',  'mEq/L', FALSE, '2024-01-11'),
(3, 2, '2345 6789 0123', 'Serum 25-OH Vitamin D',   '14.2',  '30.0 - 100.0','ng/mL', TRUE,  '2023-07-23'),
(4, 3, '2345 6789 0123', 'HbA1c (Glycated Hb)',      '5.6',   '< 5.7',      '%',     FALSE, '2022-03-06'),
(5, 3, '2345 6789 0123', 'Total Cholesterol',        '228',   '< 200',      'mg/dL', TRUE,  '2022-03-06'),
(6, 3, '2345 6789 0123', 'LDL Cholesterol',          '148',   '< 100',      'mg/dL', TRUE,  '2022-03-06'),
(7, 4, '1111 2222 3333', 'Knee MRI Scan (Right)',    'Complex tear posterior horn medial meniscus', 'Intact meniscus', 'Imaging', TRUE, '2024-03-16'),
(8, 5, '1111 2222 3333', 'Serum Electrolytes (Sodium)','132', '136 - 145', 'mEq/L', TRUE,  '2023-12-01'),
(9, 6, '5555 6666 7777', 'Cardiac Troponin-I',       '0.84',  '< 0.04',     'ng/mL', TRUE,  '2024-02-14'),
(10, 6, '5555 6666 7777', '12-Lead ECG',            'ST segment depression in V4-V6', 'Normal Sinus Rhythm', 'ECG', TRUE, '2024-02-14'),
(11, 7, '4444 3333 2222', 'Spirometry (FEV1/FVC)',   '68%',   '> 75%',      '%',     TRUE,  '2024-01-29');

-- ============================================================
-- SEED DATA: BED ALLOCATIONS (Strictly 1 bed per patient)
-- ============================================================
INSERT IGNORE INTO bed_allocation (allocation_id, hospital_id, ward_name, bed_number, aadhaar_number, status, admitted_at, expected_discharge) VALUES
(1, 1, 'Emergency Trauma Bay', 'ER-101', '5555 6666 7777', 'Occupied', '2024-02-14 02:30:00', '2024-02-18'),
(2, 1, 'Emergency Trauma Bay', 'ER-102', NULL,           'Vacant',   NULL, NULL),
(3, 1, 'Emergency Trauma Bay', 'ER-103', NULL,           'Cleaning', NULL, NULL),
(4, 1, 'Emergency Trauma Bay', 'ER-104', NULL,           'Vacant',   NULL, NULL),
(5, 1, 'Intensive Care Unit',   'ICU-201', NULL,          'Vacant',   NULL, NULL),
(6, 1, 'Intensive Care Unit',   'ICU-202', NULL,          'Vacant',   NULL, NULL),
(7, 2, 'Cardiac HDU',           'HDU-301', '2345 6789 0123', 'Occupied', '2024-01-10 11:00:00', '2024-01-12'),
(8, 2, 'Cardiac HDU',           'HDU-302', NULL,          'Vacant',   NULL, NULL),
(9, 4, 'Surgical Post-Op Ward', 'SPW-401', '1111 2222 3333', 'Occupied', '2024-03-18 14:00:00', '2024-03-21'),
(10, 4, 'Surgical Post-Op Ward', 'SPW-402', NULL,          'Vacant',   NULL, NULL),
(11, 4, 'Surgical Post-Op Ward', 'SPW-403', NULL,          'Vacant',   NULL, NULL),
(12, 6, 'Acute Medical Care',    'AMC-501', NULL,          'Vacant',   NULL, NULL);

-- ============================================================
-- IMPORTANT PRODUCTION QUERIES (Q1–Q5)
-- ============================================================

-- Q1: Full medical history of a patient using Aadhaar
-- SELECT mr.record_id, mr.visit_date, mr.visit_type, mr.department, mr.diagnosis, mr.icd10_code, mr.prescription, h.hospital_name, d.doctor_name FROM medical_record mr JOIN hospital h ON mr.hospital_id = h.hospital_id LEFT JOIN doctor d ON mr.doctor_id = d.doctor_id WHERE mr.aadhaar_number = '2345 6789 0123' ORDER BY mr.visit_date DESC;

-- Q2: Patient profile with aggregate visit statistics
-- SELECT p.aadhaar_number, p.full_name, p.blood_group, COUNT(mr.record_id) AS total_visits, MAX(mr.visit_date) AS last_visit_date FROM patient p LEFT JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number WHERE p.aadhaar_number = '2345 6789 0123' GROUP BY p.aadhaar_number;

-- Q3: All abnormal lab reports across hospitals
-- SELECT lr.test_name, lr.result, lr.normal_range, lr.unit, lr.report_date, h.hospital_name FROM lab_report lr JOIN medical_record mr ON lr.record_id = mr.record_id JOIN hospital h ON mr.hospital_id = h.hospital_id WHERE lr.is_abnormal = TRUE ORDER BY lr.report_date DESC;

-- Q4: Hospital-wise visit count and unique patient reach (KPI)
-- SELECT h.hospital_id, h.hospital_name, h.hospital_type, h.city, COUNT(mr.record_id) AS total_visits, COUNT(DISTINCT mr.aadhaar_number) AS unique_patients FROM hospital h LEFT JOIN medical_record mr ON h.hospital_id = mr.hospital_id GROUP BY h.hospital_id ORDER BY total_visits DESC;

-- Q5: Patients with emergency visits
-- SELECT DISTINCT p.full_name, p.mobile, p.blood_group, p.allergies, mr.visit_date, mr.diagnosis, h.hospital_name FROM patient p JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number JOIN hospital h ON mr.hospital_id = h.hospital_id WHERE mr.visit_type = 'Emergency' ORDER BY mr.visit_date DESC;
