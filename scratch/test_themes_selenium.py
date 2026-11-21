import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_test():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1400,900')

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        print("[1] Opening MediLink homepage...")
        driver.get('http://127.0.0.1:8000')
        wait.until(EC.presence_of_element_located((By.ID, 'view-landing')))

        # Clear localStorage to test clean first-time user experience
        driver.execute_script("localStorage.removeItem('medilink-theme'); localStorage.removeItem('medilink_theme'); initTheme();")
        time.sleep(0.5)

        pref = driver.execute_script("return document.documentElement.getAttribute('data-theme-preference');")
        resolved = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
        icon = driver.find_element(By.ID, 'landing-theme-btn-icon').text.strip()
        print(f"Default theme state: pref={pref}, resolved={resolved}, icon={icon}")
        assert pref == 'system', f"Expected default pref 'system', got '{pref}'"
        assert resolved in ['light', 'dark'], f"Expected resolved 'light' or 'dark', got '{resolved}'"
        assert icon == '💻', f"Expected '💻', got '{icon}'"
        print("PASS: System Default is the default theme for first-time visitors.")

        # [2] Test landing theme dropdown menu
        print("\n[2] Testing landing theme dropdown menu...")
        toggle_btn = driver.find_element(By.ID, 'landing-theme-toggle')
        driver.execute_script("arguments[0].click();", toggle_btn)
        time.sleep(0.3)

        menu = driver.find_element(By.ID, 'landing-theme-dropdown-menu')
        assert menu.is_displayed(), "Landing theme dropdown menu is not displayed"
        print("PASS: Landing theme dropdown menu opened.")

        # Click Dark option
        dark_opt = driver.find_element(By.CSS_SELECTOR, '#landing-theme-dropdown-menu .theme-menu-item[data-theme-val="dark"]')
        driver.execute_script("arguments[0].click();", dark_opt)
        time.sleep(0.5)

        pref = driver.execute_script("return document.documentElement.getAttribute('data-theme-preference');")
        resolved = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
        stored = driver.execute_script("return localStorage.getItem('medilink-theme');")
        icon = driver.find_element(By.ID, 'landing-theme-btn-icon').text.strip()
        print(f"After selecting Dark: pref={pref}, resolved={resolved}, stored={stored}, icon={icon}")
        assert pref == 'dark' and resolved == 'dark' and stored == 'dark'
        assert icon == '🌙'
        print("PASS: Dark theme applied and persisted in localStorage.")

        # Switch to Midnight Blue
        driver.execute_script("arguments[0].click();", toggle_btn)
        time.sleep(0.3)
        mid_opt = driver.find_element(By.CSS_SELECTOR, '#landing-theme-dropdown-menu .theme-menu-item[data-theme-val="midnight"]')
        driver.execute_script("arguments[0].click();", mid_opt)
        time.sleep(0.5)

        pref = driver.execute_script("return document.documentElement.getAttribute('data-theme-preference');")
        resolved = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
        stored = driver.execute_script("return localStorage.getItem('medilink-theme');")
        icon = driver.find_element(By.ID, 'landing-theme-btn-icon').text.strip()
        print(f"After selecting Midnight: pref={pref}, resolved={resolved}, stored={stored}, icon={icon}")
        assert pref == 'midnight' and resolved == 'midnight' and stored == 'midnight'
        assert icon == '🌌'
        print("PASS: Midnight Blue theme applied and persisted.")

        # [3] Log in to authenticated app
        print("\n[3] Logging in to test dashboard theme controls...")
        driver.execute_script("switchView('login');")
        time.sleep(0.5)

        demo_pill = driver.find_element(By.XPATH, "//span[contains(@class,'demo-btn-pill') and contains(text(),'Admin')]")
        demo_pill.click()

        wait.until(EC.presence_of_element_located((By.ID, 'view-app')))
        time.sleep(1)

        # Topbar theme button should reflect current midnight theme
        top_icon = driver.find_element(By.ID, 'theme-btn-icon').text.strip()
        print(f"Topbar theme icon: '{top_icon}'")
        assert top_icon == '🌌', f"Expected '🌌', got '{top_icon}'"

        # [4] Test topbar dropdown menu
        print("\n[4] Testing topbar dropdown menu...")
        btn_theme = driver.find_element(By.ID, 'btn-theme-toggle')
        driver.execute_script("arguments[0].click();", btn_theme)
        time.sleep(0.3)

        top_menu = driver.find_element(By.ID, 'theme-dropdown-menu')
        assert top_menu.is_displayed(), "Topbar theme menu should be displayed"

        # Switch to Light via topbar
        light_item = driver.find_element(By.CSS_SELECTOR, '#theme-dropdown-menu .theme-menu-item[data-theme-val="light"]')
        driver.execute_script("arguments[0].click();", light_item)
        time.sleep(0.5)

        resolved = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
        top_icon = driver.find_element(By.ID, 'theme-btn-icon').text.strip()
        print(f"After selecting Light via topbar: resolved={resolved}, icon={top_icon}")
        assert resolved == 'light' and top_icon == '☀️'
        print("PASS: Light theme applied from topbar menu.")

        # [5] Test Appearance Settings on Profile page
        print("\n[5] Testing Appearance Settings in Profile page...")
        driver.execute_script("openProfileAppearance();")
        time.sleep(0.8)

        card = driver.find_element(By.ID, 'settings-appearance-card')
        assert card.is_displayed(), "Settings appearance card should be visible"

        badge = driver.find_element(By.ID, 'current-theme-badge').text.strip()
        print(f"Current theme badge on profile: '{badge}'")
        assert 'Light' in badge, f"Expected 'Light' in badge, got '{badge}'"

        # Check that light preview card is active
        light_card = driver.find_element(By.CSS_SELECTOR, '.theme-preview-card[data-theme-opt="light"]')
        assert 'active' in light_card.get_attribute('class'), "Light preview card should be active"

        # Click Dark preview card
        print("Clicking Dark theme preview card...")
        dark_card = driver.find_element(By.CSS_SELECTOR, '.theme-preview-card[data-theme-opt="dark"]')
        driver.execute_script("arguments[0].click();", dark_card)
        time.sleep(0.5)

        resolved = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
        assert resolved == 'dark', f"Expected dark, got {resolved}"
        assert 'active' in dark_card.get_attribute('class')
        assert 'active' not in light_card.get_attribute('class')
        badge = driver.find_element(By.ID, 'current-theme-badge').text.strip()
        print(f"Updated theme badge: '{badge}'")
        assert 'Slate Dark' in badge or 'Dark' in badge
        print("PASS: Appearance preview cards update theme and active states immediately.")

        # [6] Test Page Reload Persistence (Anti-flash)
        print("\n[6] Testing Page Reload Persistence & Flash Prevention...")
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.ID, 'view-app')))
        time.sleep(0.5)

        pref_after_reload = driver.execute_script("return document.documentElement.getAttribute('data-theme-preference');")
        resolved_after_reload = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
        print(f"After reload: pref={pref_after_reload}, resolved={resolved_after_reload}")
        assert pref_after_reload == 'dark' and resolved_after_reload == 'dark'
        print("PASS: Theme persists across reload without flash.")

        # [7] Test Real Live System Default Behavior
        print("\n[7] Testing Real System Default Behavior with matchMedia emulation...")
        driver.execute_script("openProfileAppearance();")
        time.sleep(0.5)

        system_card = driver.find_element(By.CSS_SELECTOR, '.theme-preview-card[data-theme-opt="system"]')
        driver.execute_script("arguments[0].click();", system_card)
        time.sleep(0.5)

        pref = driver.execute_script("return document.documentElement.getAttribute('data-theme-preference');")
        assert pref == 'system', f"Expected 'system', got '{pref}'"

        # Emulate OS Dark Mode via CDP
        print("Emulating OS dark mode via CDP...")
        driver.execute_cdp_cmd('Emulation.setEmulatedMedia', {
            'features': [{'name': 'prefers-color-scheme', 'value': 'dark'}]
        })
        time.sleep(0.6)
        resolved_os_dark = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
        print(f"OS dark mode active -> app resolved theme: '{resolved_os_dark}'")
        assert resolved_os_dark == 'dark', f"Expected 'dark' when OS is dark, got '{resolved_os_dark}'"

        # Emulate OS Light Mode via CDP
        print("Emulating OS light mode via CDP...")
        driver.execute_cdp_cmd('Emulation.setEmulatedMedia', {
            'features': [{'name': 'prefers-color-scheme', 'value': 'light'}]
        })
        time.sleep(0.6)
        resolved_os_light = driver.execute_script("return document.documentElement.getAttribute('data-theme');")
        print(f"OS light mode active -> app resolved theme: '{resolved_os_light}'")
        assert resolved_os_light == 'light', f"Expected 'light' when OS is light, got '{resolved_os_light}'"
        print("PASS: Live OS appearance changes detected and applied immediately without refresh.")

        # [8] Verify Logout Button & Toast Notifications
        print("\n[8] Verifying Logout Button & Toast Notifications styling...")
        logout_btn = driver.find_element(By.ID, 'btn-sidebar-logout')
        bg_col = logout_btn.value_of_css_property('background-color')
        txt_col = logout_btn.value_of_css_property('color')
        print(f"Sidebar logout button bg: '{bg_col}', text color: '{txt_col}'")
        assert '220, 38, 38' in bg_col or '#dc2626' in bg_col, f"Unexpected bg: {bg_col}"
        assert '255, 255, 255' in txt_col or '#ffffff' in txt_col, f"Unexpected color: {txt_col}"
        assert 'Logout' in logout_btn.text
        print("PASS: Logout button is clearly red with crisp white text and 'Logout' label.")

        # [9] Check Console Errors
        print("\n[9] Checking browser console logs...")
        logs = driver.get_log('browser')
        severe_errors = [l for l in logs if l['level'] == 'SEVERE']
        print(f"Severe console errors count: {len(severe_errors)}")
        for err in severe_errors:
            print("  Console Error:", err['message'])
        assert len(severe_errors) == 0, f"Found {len(severe_errors)} console errors!"
        print("PASS: 0 console errors!")

        print("\n=======================================================")
        print("ALL THEME SYSTEM SELENIUM TESTS PASSED SUCCESSFULLY!")
        print("=======================================================")

    finally:
        driver.quit()

if __name__ == '__main__':
    run_test()
