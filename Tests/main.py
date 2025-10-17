from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def test_login_page():
    driver.get("https://www.rosariosis.org/")
    wait = WebDriverWait(driver, 20)

    # Wait for username field
    username_field = wait.until(ec.presence_of_element_located((By.NAME, "username")))
    # Use JavaScript to set username
    driver.execute_script("arguments[0].value='Teacher';", username_field)

    # Wait for password field
    password_field = wait.until(ec.presence_of_element_located((By.NAME, "password")))
    # Use JavaScript to set password
    driver.execute_script("arguments[0].value='Teacher';", password_field)

    # Click login button
    login_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
    login_button.click()

    # Wait for URL redirection
    wait.until(ec.url_contains("dashboard"))  # replace "dashboard" with actual URL fragment

    print("Login test passed! Redirected to:", driver.current_url)

# tests/test_homepage.py

def test_dummy():
    assert True


# Run the test
driver = webdriver.Chrome()
test_login_page()
driver.quit()

