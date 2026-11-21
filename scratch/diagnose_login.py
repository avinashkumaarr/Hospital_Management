from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

opts = Options()
opts.add_argument('--headless=new')
opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
driver = webdriver.Chrome(options=opts)

try:
    driver.get('http://127.0.0.1:8000')
    time.sleep(1)

    landing = driver.find_element(By.ID, 'view-landing')
    print('Landing displayed:', landing.is_displayed())
    print('Landing classes:', landing.get_attribute('class'))

    btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
    print('Button text:', btn.text)
    btn.click()
    time.sleep(0.5)

    login_view = driver.find_element(By.ID, 'view-login')
    print('Login classes:', login_view.get_attribute('class'))
    print('Login displayed:', login_view.is_displayed())
    print('Login computed display:', driver.execute_script('return window.getComputedStyle(arguments[0]).display;', login_view))
    print('Login computed opacity:', driver.execute_script('return window.getComputedStyle(arguments[0]).opacity;', login_view))
    print('Login clientHeight:', login_view.get_attribute('clientHeight'))
    print('Login clientWidth:', login_view.get_attribute('clientWidth'))

    logs = driver.get_log('browser')
    print('Browser console logs:', logs)
finally:
    driver.quit()
