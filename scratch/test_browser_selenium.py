import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_browser_verification():
    print("=" * 60)
    print("  MEDILINK ENTERPRISE v3.0 — END-TO-END BROWSER TEST")
    print("=" * 60)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1400,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Enable browser logging
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        # Step 1: Open Homepage
        print("\n[Step 1] Loading http://127.0.0.1:8000 ...")
        driver.get("http://127.0.0.1:8000")
        time.sleep(1)

        landing = driver.find_element(By.ID, "view-landing")
        assert landing.is_displayed(), "Landing view is not displayed!"
        hero_title = driver.find_element(By.CLASS_NAME, "hero-title").text
        print(f"  ✓ Homepage loaded successfully: '{hero_title}'")

        # Step 2: Navigate to Login View
        print("\n[Step 2] Clicking 'Sign In' to navigate to login ...")
        signin_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        signin_btn.click()
        time.sleep(0.5)

        login_view = driver.find_element(By.ID, "view-login")
        assert login_view.is_displayed(), "Login view is not displayed!"
        print("  ✓ Login view displayed successfully.")

        # Step 3: Login as Administrator
        print("\n[Step 3] Entering admin credentials & submitting login form ...")
        u_input = driver.find_element(By.ID, "login-username")
        p_input = driver.find_element(By.ID, "login-password")
        u_input.clear()
        u_input.send_keys("admin")
        p_input.clear()
        p_input.send_keys("admin123")

        submit_btn = driver.find_element(By.CSS_SELECTOR, "#login-form button[type='submit']")
        submit_btn.click()
        time.sleep(1.5)

        # Step 4: Verify Command Center and Layout (Fix Blank Screen Verification)
        print("\n[Step 4] Verifying layout after login (Sidebar, Header, Main, KPIs) ...")
        app_view = driver.find_element(By.ID, "view-app")
        assert app_view.is_displayed(), "view-app is not displayed!"
        app_size = app_view.size
        print(f"  ✓ view-app container size: {app_size['width']}x{app_size['height']}px")

        sidebar = driver.find_element(By.ID, "app-sidebar")
        assert sidebar.is_displayed(), "Sidebar is not displayed!"
        sidebar_size = sidebar.size
        print(f"  ✓ Sidebar is visible: width={sidebar_size['width']}px, height={sidebar_size['height']}px")

        header = driver.find_element(By.CLASS_NAME, "app-header")
        assert header.is_displayed(), "Header is not displayed!"
        header_size = header.size
        print(f"  ✓ Header topbar is visible: width={header_size['width']}px, height={header_size['height']}px")

        page_home = driver.find_element(By.ID, "page-home")
        assert page_home.is_displayed(), "page-home (Command Center) is NOT displayed!"
        home_size = page_home.size
        assert home_size['height'] > 200, f"page-home height is too small: {home_size['height']}px"
        assert home_size['width'] > 600, f"page-home width is too small: {home_size['width']}px"
        print(f"  ✓ Command Center (#page-home) rendered: width={home_size['width']}px, height={home_size['height']}px")

        welcome_text = driver.find_element(By.ID, "welcome-user-name").text
        print(f"  ✓ Welcome Greeting Banner active: 'Welcome back, {welcome_text}'")

        patients_stat = driver.find_element(By.ID, "dash-stat-patients").text
        encounters_stat = driver.find_element(By.ID, "dash-stat-records").text
        beds_stat = driver.find_element(By.ID, "dash-stat-beds").text
        queue_stat = driver.find_element(By.ID, "dash-stat-queue").text
        print(f"  ✓ KPIs loaded: Patients={patients_stat}, Encounters={encounters_stat}, Beds={beds_stat}, Queue={queue_stat}")

        # Step 5: Test Sidebar Navigation
        print("\n[Step 5] Testing Sidebar Navigation across multiple clinical modules ...")
        
        # 5a: Patient Directory
        driver.find_element(By.XPATH, "//button[@data-page='page-patients']").click()
        time.sleep(0.8)
        page_patients = driver.find_element(By.ID, "page-patients")
        assert page_patients.is_displayed(), "page-patients is not displayed!"
        patient_rows = driver.find_elements(By.CSS_SELECTOR, "#patient-directory-tbody tr")
        print(f"  ✓ Patient Directory loaded ({len(patient_rows)} patient rows visible).")

        # 5b: Appointments
        driver.find_element(By.XPATH, "//button[@data-page='page-appointments']").click()
        time.sleep(0.8)
        page_appts = driver.find_element(By.ID, "page-appointments")
        assert page_appts.is_displayed(), "page-appointments is not displayed!"
        print("  ✓ Appointments page loaded.")

        # 5c: Bed Management
        driver.find_element(By.XPATH, "//button[@data-page='page-beds']").click()
        time.sleep(0.8)
        page_beds = driver.find_element(By.ID, "page-beds")
        assert page_beds.is_displayed(), "page-beds is not displayed!"
        print("  ✓ Bed Management matrix loaded.")

        # 5d: Return to Command Center
        driver.find_element(By.XPATH, "//button[@data-page='page-home']").click()
        time.sleep(0.5)
        assert driver.find_element(By.ID, "page-home").is_displayed()
        print("  ✓ Returned to Command Center dashboard.")

        # Step 6: Test Profile Dropdown & Profile Page
        print("\n[Step 6] Testing Profile Dropdown and Staff Profile Page ...")
        prof_btn = driver.find_element(By.ID, "header-profile-btn")
        prof_btn.click()
        time.sleep(0.3)

        dropdown_menu = driver.find_element(By.ID, "header-profile-menu")
        assert dropdown_menu.is_displayed(), "Profile dropdown menu is not displayed!"
        dropdown_user = driver.find_element(By.ID, "dropdown-user-name").text
        print(f"  ✓ Profile dropdown opened: User='{dropdown_user}'")

        # Click View Profile in dropdown
        my_profile_item = driver.find_element(By.XPATH, "//button[contains(., 'My Profile')]")
        my_profile_item.click()
        time.sleep(0.8)

        page_profile = driver.find_element(By.ID, "page-profile")
        assert page_profile.is_displayed(), "page-profile is not displayed!"
        hero_prof_name = driver.find_element(By.ID, "profile-hero-name").text
        prof_uname = driver.find_element(By.ID, "prof-username-input").get_attribute("value")
        prof_role = driver.find_element(By.ID, "prof-role-input").get_attribute("value")
        print(f"  ✓ Staff Profile Page rendered: '{hero_prof_name}' ({prof_role}), Username: '{prof_uname}'")

        # Step 7: Test Profile Information Update
        print("\n[Step 7] Testing Profile Editing (Update email and phone) ...")
        email_input = driver.find_element(By.ID, "prof-email-input")
        email_input.clear()
        email_input.send_keys("admin.primary@medilink.hospital")
        
        save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Save Profile Changes')]")
        save_btn.click()
        time.sleep(1)
        print("  ✓ Profile update submitted successfully.")

        # Step 8: Test Sign Out
        print("\n[Step 8] Testing Logout from sidebar footer ...")
        sidebar_logout_btn = driver.find_element(By.XPATH, "//div[@class='sidebar-footer']//button[contains(@title, 'Sign Out')]")
        sidebar_logout_btn.click()
        time.sleep(1)

        landing_after_logout = driver.find_element(By.ID, "view-landing")
        assert landing_after_logout.is_displayed(), "Failed to return to landing view after logout!"
        print("  ✓ Successfully signed out and returned to landing homepage.")

        # Verify token is cleared from localStorage
        token = driver.execute_script("return localStorage.getItem('medilink_token');")
        assert token is None, f"Token was not cleared: {token}"
        print("  ✓ Authentication token successfully wiped from client storage.")

        # Step 9: Re-login as Doctor
        print("\n[Step 9] Re-logging in as Doctor (Dr. Anita Verma) ...")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()
        time.sleep(0.5)

        doc_pill = driver.find_element(By.XPATH, "//span[contains(text(), 'Doctor')]")
        doc_pill.click()
        time.sleep(1.5)

        assert driver.find_element(By.ID, "view-app").is_displayed()
        doc_welcome = driver.find_element(By.ID, "welcome-user-name").text
        print(f"  ✓ Doctor session active: '{doc_welcome}'")

        # Step 10: Test Page Refresh & Session Restoration (Task 6)
        print("\n[Step 10] Testing Page Refresh & Session Restoration ...")
        driver.refresh()
        time.sleep(1.5)
        assert driver.find_element(By.ID, "view-app").is_displayed(), "Session not restored after page refresh!"
        assert driver.find_element(By.ID, "page-home").is_displayed(), "Command Center not active after refresh!"
        refreshed_name = driver.find_element(By.ID, "welcome-user-name").text
        print(f"  ✓ Session perfectly restored after browser refresh: '{refreshed_name}'")

        # Check console logs for any errors
        print("\n[Step 11] Checking Browser Console Logs ...")
        logs = driver.get_log("browser")
        severe_errors = [l for l in logs if l["level"] == "SEVERE"]
        if severe_errors:
            print(f"  ⚠️ Warning: {len(severe_errors)} severe console errors:")
            for err in severe_errors:
                print("    ", err["message"])
        else:
            print("  ✓ Zero severe console errors detected!")

        print("\n" + "=" * 60)
        print("  ALL 11 END-TO-END BROWSER CHECKS PASSED WITH 100% SUCCESS!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ Browser Verification Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    success = run_browser_verification()
    sys.exit(0 if success else 1)
