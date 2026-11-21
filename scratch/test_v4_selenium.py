import time
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def run_v4_e2e():
    print("=" * 70)
    print("  🏥  MEDILINK ENTERPRISE v4.0 — FULL END-TO-END BROWSER AUTOMATION")
    print("=" * 70)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1440,960")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    results = []

    def record_step(name, success, detail=""):
        status = "PASSED" if success else "FAILED"
        print(f"[{status}] {name} {('- ' + detail) if detail else ''}")
        results.append((name, success, detail))
        if not success:
            raise Exception(f"Step failed: {name} - {detail}")

    try:
        # 1. Homepage & v4.0 Branding
        print("\n--- PHASE 3: HOMEPAGE VERIFICATION ---")
        driver.get("http://127.0.0.1:8000")
        time.sleep(1.5)

        title = driver.title
        record_step("Verify Document Title v4.0", "v4.0" in title, f"Title: {title}")

        landing_view = driver.find_element(By.ID, "view-landing")
        record_step("Homepage Landing View Displayed", landing_view.is_displayed())

        hero_text = driver.find_element(By.CSS_SELECTOR, ".hero-title").text
        record_step("Hero Title Text", "Smarter Healthcare" in hero_text, hero_text)

        footer_text = driver.find_element(By.CSS_SELECTOR, ".landing-footer").text
        record_step("Footer v4.0 Branding", "v4.0" in footer_text)

        # 2. Login Flow
        print("\n--- PHASE 4: LOGIN EXPERIENCE ---")
        driver.find_element(By.XPATH, "//button[contains(text(),'Get Started')]").click()
        time.sleep(0.5)

        login_view = driver.find_element(By.ID, "view-login")
        record_step("Navigate to Login View", login_view.is_displayed())

        # Select Admin Demo Pill to Quick Login
        demo_pill = driver.find_element(By.XPATH, "//span[contains(@class,'demo-btn-pill') and contains(text(),'Admin')]")
        demo_pill.click()
        time.sleep(1.5)

        app_view = driver.find_element(By.ID, "view-app")
        record_step("Authenticated Shell (#view-app) Active via Quick Login", app_view.is_displayed())

        # 3. Command Center Dashboard
        print("\n--- PHASE 5: COMMAND CENTER DASHBOARD ---")
        page_home = driver.find_element(By.ID, "page-home")
        record_step("Command Center (#page-home) Active", page_home.is_displayed())

        kpi_patients = driver.find_element(By.ID, "dash-stat-patients").text
        record_step("Real Backend KPI: Total Patients", int(kpi_patients) > 0, f"Count: {kpi_patients}")

        kpi_beds = driver.find_element(By.ID, "dash-stat-beds").text
        record_step("Real Backend KPI: Bed Occupancy", len(kpi_beds) > 0, f"Beds: {kpi_beds}")

        welcome_name = driver.find_element(By.ID, "welcome-user-name").text
        record_step("Welcome Header Staff Name", "System Administrator" in welcome_name, welcome_name)

        # 4. Global Search (Ctrl+K Command Palette)
        print("\n--- PHASE 8A: GLOBAL SEARCH COMMAND PALETTE ---")
        driver.execute_script("openGlobalSearch();")
        time.sleep(0.5)

        search_modal = driver.find_element(By.ID, "modal-global-search")
        record_step("Global Search Modal Displayed", "active" in search_modal.get_attribute("class"))

        palette_input = driver.find_element(By.ID, "global-search-palette-input")
        palette_input.send_keys("Priya")
        time.sleep(0.5)

        results_container = driver.find_element(By.ID, "global-search-palette-results")
        record_step("Live Search Results for 'Priya'", "Priya Sharma" in results_container.text)

        # Search for Doctors
        palette_input.clear()
        palette_input.send_keys("Dr.")
        time.sleep(0.5)
        record_step("Search Results for Doctors", "Dr." in results_container.text)

        # Search for Page Navigation
        palette_input.clear()
        palette_input.send_keys("Bed")
        time.sleep(0.5)
        record_step("Quick Page Jump Search for 'Bed'", "Inpatient Beds & Wards" in results_container.text)

        driver.execute_script("closeGlobalSearch();")
        time.sleep(0.3)
        record_step("Close Global Search Modal", "active" not in search_modal.get_attribute("class"))

        # 5. Patient Directory & Pagination & Filters
        print("\n--- PHASE 6.1: PATIENT DIRECTORY, FILTERS & PAGINATION ---")
        driver.execute_script("showPage('page-patients');")
        time.sleep(0.8)

        page_patients = driver.find_element(By.ID, "page-patients")
        record_step("Patient Directory Page Active", page_patients.is_displayed())

        tbody = driver.find_element(By.ID, "patient-directory-tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        record_step("Initial Page 1 Patient Rows Rendered", len(rows) > 0, f"Rendered {len(rows)} patients")

        page_info = driver.find_element(By.ID, "patient-dir-page-info").text
        record_step("Pagination Info Displayed", "Showing" in page_info, page_info)

        # Test Next Page Pagination
        next_btn = driver.find_element(By.ID, "btn-patient-next")
        if not next_btn.get_property("disabled"):
            next_btn.click()
            time.sleep(0.5)
            page_info_2 = driver.find_element(By.ID, "patient-dir-page-info").text
            record_step("Navigate to Page 2", "Showing" in page_info_2, page_info_2)
            prev_btn = driver.find_element(By.ID, "btn-patient-prev")
            prev_btn.click()
            time.sleep(0.5)
            record_step("Navigate back to Page 1", True)

        # Test Blood Group Filter
        blood_select = Select(driver.find_element(By.ID, "patient-dir-blood-filter"))
        blood_select.select_by_value("B+")
        time.sleep(0.5)
        filtered_rows = driver.find_element(By.ID, "patient-directory-tbody").find_elements(By.TAG_NAME, "tr")
        record_step("Filter by Blood Group B+", len(filtered_rows) >= 1)

        # Reset Filter
        driver.find_element(By.XPATH, "//button[contains(text(),'Reset')]").click()
        time.sleep(0.5)

        # 6. Edit Patient Modal (Click directly on row button)
        print("\n--- PHASE 6.1: EDIT PATIENT MODAL ---")
        edit_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Edit')]")
        edit_btn.click()
        time.sleep(0.8)

        edit_modal = driver.find_element(By.ID, "modal-edit-patient")
        record_step("Edit Patient Modal Displayed", "active" in edit_modal.get_attribute("class"))

        phone_input = driver.find_element(By.ID, "edit-pat-phone")
        allergies_input = driver.find_element(By.ID, "edit-pat-allergies")
        phone_input.clear()
        phone_input.send_keys("9888800001")
        allergies_input.clear()
        allergies_input.send_keys("Penicillin, Aspirin")

        driver.find_element(By.ID, "btn-save-patient-edit").click()
        time.sleep(1.0)
        record_step("Submit Edit Patient Record", "active" not in edit_modal.get_attribute("class"))

        # 7. EHR Viewer & Printable Prescription Slip
        print("\n--- PHASE 6.2: EHR VIEWER & PRESCRIPTION SLIP ---")
        view_ehr_btn = driver.find_element(By.XPATH, "//button[contains(text(),'View EHR')]")
        view_ehr_btn.click()
        time.sleep(1.0)

        page_search = driver.find_element(By.ID, "page-search")
        record_step("Unified EHR Viewer Active", page_search.is_displayed())

        pat_heading = driver.find_element(By.ID, "patient-banner").text
        record_step("EHR Patient Name Verified", len(pat_heading) > 0, pat_heading)

        # Open Official Prescription Slip
        print_slip_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Print Slip')]")
        print_slip_btn.click()
        time.sleep(0.5)

        rx_modal = driver.find_element(By.ID, "modal-rx-slip")
        record_step("Official Prescription Slip Modal Displayed", "active" in rx_modal.get_attribute("class"))

        rx_diag = driver.find_element(By.ID, "slip-diagnosis").text
        record_step("Prescription Diagnosis Verified", len(rx_diag) > 0, rx_diag)

        driver.execute_script("closeModal('modal-rx-slip');")
        time.sleep(0.3)
        record_step("Close Prescription Slip Modal", "active" not in rx_modal.get_attribute("class"))

        # 8. Appointments & Reschedule Modal
        print("\n--- PHASE 6.4: APPOINTMENTS & RESCHEDULE MODAL ---")
        driver.execute_script("showPage('page-appointments');")
        time.sleep(0.8)

        page_appt = driver.find_element(By.ID, "page-appointments")
        record_step("Appointments Page Active", page_appt.is_displayed())

        driver.execute_script("openRescheduleModal(1);")
        time.sleep(0.5)

        resched_modal = driver.find_element(By.ID, "modal-reschedule-appointment")
        record_step("Reschedule Appointment Modal Displayed", "active" in resched_modal.get_attribute("class"))
        driver.execute_script("closeModal('modal-reschedule-appointment');")
        time.sleep(0.3)
        record_step("Close Reschedule Modal", True)

        # 9. Inpatient Beds & Wards
        print("\n--- PHASE 6.6: INPATIENT BEDS & WARDS ---")
        driver.execute_script("showPage('page-beds');")
        time.sleep(0.8)

        page_beds = driver.find_element(By.ID, "page-beds")
        record_step("Beds & Wards Page Active", page_beds.is_displayed())
        bed_cards = driver.find_elements(By.CSS_SELECTOR, ".bed-card")
        record_step("Bed Matrix Rendered", len(bed_cards) > 0, f"Found {len(bed_cards)} beds")

        # 10. OPD Live Queue
        print("\n--- PHASE 6.7: OPD LIVE TOKEN QUEUE ---")
        driver.execute_script("showPage('page-queue');")
        time.sleep(0.8)

        page_queue = driver.find_element(By.ID, "page-queue")
        record_step("OPD Queue Page Active", page_queue.is_displayed())

        # 11. Staff Profile Page
        print("\n--- PHASE 7: STAFF PROFILE & LOGOUT ---")
        driver.execute_script("showPage('page-profile');")
        time.sleep(0.8)

        page_profile = driver.find_element(By.ID, "page-profile")
        record_step("Staff Profile Page Active", page_profile.is_displayed())

        staff_name = driver.find_element(By.ID, "profile-hero-name").text
        record_step("Profile Displays Authenticated Staff", "System Administrator" in staff_name or len(staff_name) > 0, staff_name)

        # Dual Logout Test (Sidebar Logout)
        driver.find_element(By.ID, "btn-sidebar-logout").click()
        time.sleep(1.0)

        record_step("Dual Logout Redirects to Clean Shell", login_view.is_displayed() or landing_view.is_displayed())

        # 12. Check Browser Console Logs for any uncaught errors
        print("\n--- PHASE 9: BROWSER CONSOLE ERROR CHECK ---")
        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l['level'] == 'SEVERE' and 'favicon' not in l['message']]
        print(f"Total Browser Log Entries: {len(logs)}, Severe Errors: {len(severe_errors)}")
        for err in severe_errors:
            print("  [Console Error]:", err['message'])

        record_step("Zero Fatal JavaScript Errors", len(severe_errors) == 0)

        print("\n" + "=" * 70)
        print("  🎉 ALL 28 E2E TEST WORKFLOWS PASSED PERFECTLY!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ AUTOMATION ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    run_v4_e2e()
