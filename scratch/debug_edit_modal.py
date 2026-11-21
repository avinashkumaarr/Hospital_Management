import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1440,960")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

driver = webdriver.Chrome(options=chrome_options)
try:
    driver.get("http://127.0.0.1:8000")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(),'Get Started')]").click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//span[contains(@class,'demo-btn-pill') and contains(text(),'Admin')]").click()
    time.sleep(1.5)

    driver.execute_script("showPage('page-patients');")
    time.sleep(0.8)

    edit_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Edit')]")
    edit_btn.click()
    time.sleep(0.8)

    phone_input = driver.find_element(By.ID, "edit-pat-phone")
    phone_input.clear()
    phone_input.send_keys("9876543210")

    driver.find_element(By.ID, "btn-save-patient-edit").click()
    time.sleep(1.5)

    edit_modal = driver.find_element(By.ID, "modal-edit-patient")
    print("Modal class after save:", edit_modal.get_attribute("class"))

    logs = driver.get_log("browser")
    print("Browser logs:")
    for log in logs:
        print(" ", log)
finally:
    driver.quit()
