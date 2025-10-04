from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def syndicate_to_channels(content_path, message):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    try:
        # LinkedIn
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        driver.find_element(By.ID, "username").send_keys("your_linkedin_email")
        driver.find_element(By.ID, "password").send_keys("your_linkedin_password")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "share-box-feed-entry__trigger").click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "mentions-texteditor__contenteditable").send_keys(message)
        driver.find_element(By.XPATH, "//button[contains(text(),'Post')]").click()
        time.sleep(2)

        # Facebook
        driver.get("https://www.facebook.com/login")
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys("your_facebook_email")
        driver.find_element(By.ID, "pass").send_keys("your_facebook_password")
        driver.find_element(By.NAME, "login").click()
        time.sleep(3)
        driver.get("https://www.facebook.com/")
        time.sleep(3)
        driver.find_element(By.XPATH, "//div[@aria-label='Create a post']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[@aria-label='Write something here...']").send_keys(message)
        driver.find_element(By.XPATH, "//div[@aria-label='Post']").click()
        time.sleep(2)

    except Exception as e:
        print(f"❌ Syndication failed: {e}")
    finally:
        driver.quit()
