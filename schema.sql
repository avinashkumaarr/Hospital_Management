-- ============================================================
--  MediLink: Aadhaar-Based Unified Medical Records System
--  DBMS Course Project | SQL Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS medilink_db;
USE medilink_db;

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
    doctor_id       INT),
    visit_date      DATE            NOT NULL,
    visit_type      ENUM('OPD Consultation','Emergency','Surgery',
                         'Inpatient Admission','Routine Checkup','Lab Tests')
                    NOT NULL,
    department      VARCHAR(50),
    chief_complaint TEXT,
    diagnosis       TEXT            NOT NULL,
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

    PRIMARY KEY (log_id),
    FOREIGN KEY (aadhaar_number) REFERENCES patient(aadhaar_number)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (hospital_id)   REFERENCES hospital(hospital_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_aadhaar   (aadhaar_number),
    INDEX idx_time      (access_time)
);

-- ============================================================
-- SAMPLE DATA
-- ============================================================
INSERT INTO hospital (hospital_name, registration_no, hospital_type, city, state) VALUES
('AIIMS Delhi',           'REG-AIIMS-001', 'Government', 'New Delhi', 'Delhi'),
('Apollo Hospitals',      'REG-APL-002',   'Private',    'New Delhi', 'Delhi'),
('Fortis Healthcare',     'REG-FRT-003',   'Private',    'Gurugram',  'Haryana'),
('Max Super Speciality',  'REG-MAX-004',   'Private',    'New Delhi', 'Delhi'),
('PGIMER Chandigarh',     'REG-PGI-005',   'Government', 'Chandigarh','Chandigarh'),
('Manipal Hospital',      'REG-MAN-006',   'Private',    'Bengaluru', 'Karnataka');

INSERT INTO patient (aadhaar_number, full_name, date_of_birth, gender, blood_group, mobile) VALUES
('234567890123', 'Priya Sharma',  '1990-05-14', 'Female', 'B+', '9876543210'),
('111122223333', 'Arjun Kapoor',  '1985-11-30', 'Male',   'O+', '7777788888'),
('999988887777', 'Meera Iyer',    '2001-03-22', 'Female', 'A+', '9900112233');

-- ============================================================
-- IMPORTANT QUERIES (for logic build phase)
-- ============================================================

-- Q1: Full medical history of a patient using Aadhaar
SELECT
    mr.visit_date,
    mr.visit_type,
    mr.department,
    mr.diagnosis,
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

-- Q2: Patient profile with latest record
SELECT
    p.full_name, p.date_of_birth, p.gender,
    p.blood_group, p.allergies,
    COUNT(mr.record_id) AS total_visits,
    MAX(mr.visit_date) AS last_visit
FROM patient p
LEFT JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number
WHERE p.aadhaar_number = '234567890123'
GROUP BY p.aadhaar_number;

-- Q3: All abnormal lab reports for a patient
SELECT
    lr.test_name, lr.result, lr.normal_range, lr.report_date,
    h.hospital_name
FROM lab_report lr
JOIN medical_record mr ON lr.record_id = mr.record_id
JOIN hospital h ON mr.hospital_id = h.hospital_id
WHERE lr.aadhaar_number = '234567890123'
  AND lr.is_abnormal = TRUE
ORDER BY lr.report_date DESC;

-- Q4: Hospital-wise visit count (dashboard)
SELECT
    h.hospital_name,
    COUNT(mr.record_id) AS total_visits,
    COUNT(DISTINCT mr.aadhaar_number) AS unique_patients
FROM hospital h
LEFT JOIN medical_record mr ON h.hospital_id = mr.hospital_id
GROUP BY h.hospital_id
ORDER BY total_visits DESC;

-- Q5: Patients with emergency visits in last 30 days
SELECT DISTINCT
    p.full_name, p.mobile, p.aadhaar_number,
    mr.visit_date, h.hospital_name
FROM patient p
JOIN medical_record mr ON p.aadhaar_number = mr.aadhaar_number
JOIN hospital h ON mr.hospital_id = h.hospital_id
WHERE mr.visit_type = 'Emergency'
  AND mr.visit_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
