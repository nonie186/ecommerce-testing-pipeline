from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

def _find_input_with_fallback(wait, names):
    for n in names:
        try:
            return wait.until(ec.presence_of_element_located((By.NAME, n)))
        except TimeoutException:
            continue
    # Try common id/name patterns and generic selectors
    for sel in [
        "input[type='text']",
        "input[type='email']",
        "input[id*='user']",
        "input[id*='login']",
        "input[class*='user']",
    ]:
        try:
            return wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, sel)))
        except TimeoutException:
            continue
    raise TimeoutException("Could not locate username input with any fallback")

def _find_password_with_fallback(wait, names):
    for n in names:
        try:
            return wait.until(ec.presence_of_element_located((By.NAME, n)))
        except TimeoutException:
            continue
    for sel in [
        "input[type='password']",
        "input[id*='pass']",
        "input[class*='pass']",
    ]:
        try:
            return wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, sel)))
        except TimeoutException:
            continue
    raise TimeoutException("Could not locate password input with any fallback")

def test_homepage():
    options = Options()
    # use modern headless flag for recent Chrome
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 40)

    try:
        start_url = "https://www.rosariosis.org/demonstration/index.php?locale=en_US.utf8"
        driver.get(start_url)

        # fallback name candidates (common variants, case differences)
        username_candidates = ["username", "Username", "user", "login", "userid"]
        password_candidates = ["password", "Password", "passwd", "pass"]

        username_field = _find_input_with_fallback(wait, username_candidates)
        # set value via JS to avoid problems with send_keys when headless/CI
        driver.execute_script("arguments[0].value = arguments[1];", username_field, "teacher")

        password_field = _find_password_with_fallback(wait, password_candidates)
        driver.execute_script("arguments[0].value = arguments[1];", password_field, "teacher")

        # robust find for login button: try type=submit then button text (case-insensitive)
        try:
            login_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")))
        except TimeoutException:
            # case-insensitive contains on button text
            login_button = wait.until(
                ec.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'login') or contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'log in')]"
                    )
                )
            )

        original_url = driver.current_url
        login_button.click()

        # Wait for a real post-login condition: URL change or presence of a post-login element.
        try:
            wait.until(ec.url_changes(original_url))
        except TimeoutException:
            # fallback: wait for a logout link or user menu
            try:
                wait.until(ec.presence_of_element_located((By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'logout') or contains(., 'Log out')]")))
            except TimeoutException:
                raise TimeoutException("Login did not complete (no URL change and no logout link).")

        print("Login test passed! Redirected to:", driver.current_url)

    except Exception:
        # Save artifacts for CI debugging
        try:
            driver.save_screenshot("failure_screenshot.png")
            with open("failure_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Saved failure_screenshot.png and failure_page_source.html for debugging.")
        except Exception as e:
            print("Failed to save debug artifacts:", e)
        raise

    finally:
        driver.quit()