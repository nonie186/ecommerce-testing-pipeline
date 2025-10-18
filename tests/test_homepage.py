from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def test_homepage():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Automatically download compatible ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.rosariosis.org/demonstration/index.php?locale=en_US.utf8")

        username_field = wait.until(ec.presence_of_element_located((By.NAME, "username")))
        driver.execute_script("arguments[0].value='Teacher';", username_field)

        password_field = wait.until(ec.presence_of_element_located((By.NAME, "password")))
        driver.execute_script("arguments[0].value='Teacher';", password_field)

        login_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
        login_button.click()

        wait.until(ec.url_contains("dashboard"))  # Adjust if needed
        print("Login test passed! Redirected to:", driver.current_url)

    finally:
        driver.quit()
