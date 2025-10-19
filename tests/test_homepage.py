from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_homepage_title():
    options = Options()
    options.add_argument("--headless")  # Run in background
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    assert "Swag Labs" in driver.title
    driver.quit()
