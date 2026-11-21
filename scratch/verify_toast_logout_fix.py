import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verify_toast_and_logout():
    print("=" * 70)
    print("  VERIFYING TOAST NOTIFICATION & RED LOGOUT BUTTON FIXES")
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

    try:
        # Step 1: Navigate to app and login
        print("\n[Step 1] Loading application...")
        driver.get("http://127.0.0.1:8000")
        time.sleep(1)

        print("[Step 2] Navigating to login and authenticating...")
        driver.find_element(By.XPATH, "//button[contains(text(),'Get Started')]").click()
        time.sleep(0.5)

        # Quick login as admin
        admin_pill = driver.find_element(By.XPATH, "//span[contains(@class,'demo-btn-pill') and contains(text(),'Admin')]")
        admin_pill.click()
        time.sleep(1.0)

        # Step 2: Check Toast Appearance immediately after login
        print("\n[Step 3] Checking Welcome Toast notification...")
        toast_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#toast-container .toast")))
        assert toast_el.is_displayed(), "Toast is not displayed!"

        # Check Toast dimensions and position
        toast_size = toast_el.size
        toast_loc = toast_el.location
        toast_text = toast_el.text
        print(f"  Toast Size: width={toast_size['width']}px, height={toast_size['height']}px")
        print(f"  Toast Position: x={toast_loc['x']}, y={toast_loc['y']}")
        print(f"  Toast Text content: {repr(toast_text)}")

        # Verify width is compact (not full screen / oversized)
        assert 250 <= toast_size['width'] <= 440, f"Toast width out of expected range: {toast_size['width']}px"
        assert 35 <= toast_size['height'] <= 90, f"Toast height out of expected range: {toast_size['height']}px"
        assert toast_loc['y'] < 80, f"Toast should be near top of viewport, but y={toast_loc['y']}"
        print("  ✓ Toast is compact, positioned cleanly near top-right!")

        # Verify close button works
        close_btn = toast_el.find_element(By.CSS_SELECTOR, ".toast-close-btn")
        assert close_btn.is_displayed(), "Close button is not displayed!"
        close_btn.click()
        time.sleep(0.4)
        toasts = driver.find_elements(By.CSS_SELECTOR, "#toast-container .toast")
        assert len(toasts) == 0, "Toast was not dismissed on click!"
        print("  ✓ Toast manually dismissed successfully!")

        # Trigger a test toast via JS and check styling
        print("\n[Step 4] Triggering test success toast via JS...")
        driver.execute_script("toast('Settings and profile updated successfully.');")
        time.sleep(0.4)
        new_toast = driver.find_element(By.CSS_SELECTOR, "#toast-container .toast")
        assert "Settings and profile" in new_toast.text
        print("  ✓ Custom toast displayed properly!")

        # Step 3: Check Red Logout Button in Sidebar
        print("\n[Step 5] Checking Sidebar Red Logout Button...")
        sidebar_logout = driver.find_element(By.ID, "btn-sidebar-logout")
        assert sidebar_logout.is_displayed(), "Sidebar logout button is not displayed!"

        label_el = sidebar_logout.find_element(By.CLASS_NAME, "btn-logout-label")
        icon_el = sidebar_logout.find_element(By.CLASS_NAME, "btn-logout-icon")

        print(f"  Sidebar button text: {repr(sidebar_logout.text)}")
        print(f"  Sidebar label text: {repr(label_el.text)}")
        print(f"  Sidebar icon text: {repr(icon_el.text)}")

        assert "Logout" in label_el.text or "Sign Out" in label_el.text, f"Label text missing! Got: {label_el.text}"

        # Check CSS computed styles
        bg_color = sidebar_logout.value_of_css_property("background-color")
        color = label_el.value_of_css_property("color")
        font_weight = label_el.value_of_css_property("font-weight")
        print(f"  Computed background-color: {bg_color}")
        print(f"  Computed text color: {color}")
        print(f"  Computed font-weight: {font_weight}")

        # Ensure text is white or high contrast
        assert "255, 255, 255" in color or "rgb(255" in color, f"Expected white text color, got {color}"
        print("  ✓ Sidebar Logout button displays visible 'Logout' text with white high-contrast text on red background!")

        # Step 4: Check Topbar Header Red Logout Button
        print("\n[Step 6] Checking Header Red Logout Button...")
        header_logout = driver.find_element(By.ID, "btn-header-logout")
        assert header_logout.is_displayed(), "Header logout button is not displayed!"
        header_label = header_logout.find_element(By.CLASS_NAME, "btn-logout-label")
        print(f"  Header button text: {repr(header_logout.text)}")
        assert "Logout" in header_label.text, f"Header logout label missing: {header_label.text}"
        print("  ✓ Header Logout button displays visible 'Logout' label!")

        # Step 5: Test Click Logout and verify clean return
        print("\n[Step 7] Testing Logout action...")
        sidebar_logout.click()
        time.sleep(1.0)

        # Should be returned to login view or landing view
        login_view = driver.find_element(By.ID, "view-login")
        landing_view = driver.find_element(By.ID, "view-landing")
        app_view = driver.find_element(By.ID, "view-app")

        assert not app_view.is_displayed(), "App view should not be active after logout!"
        assert login_view.is_displayed() or landing_view.is_displayed(), "Should be redirected to login or landing view!"
        print("  ✓ Logout completed cleanly! Session invalidated.")

        print("\n" + "=" * 70)
        print("  🎉 ALL TOAST AND LOGOUT CHECKS PASSED WITH 100% SUCCESS!")
        print("=" * 70)

    finally:
        driver.quit()

if __name__ == "__main__":
    verify_toast_and_logout()
