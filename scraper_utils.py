
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_go_transit_updates():
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Open the GO Transit service updates page
        url = "https://www.gotransit.com/en/service-updates/service-updates"
        driver.get(url)

        # Wait for the 'View Updates' button to be clickable and click it
        wait = WebDriverWait(driver, 10)
        view_updates_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='View Updates']")))
        view_updates_button.click()

        # Keep clicking 'Load more updates' until all updates are loaded
        while True:
            try:
                load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Load more updates']")))
                load_more_button.click()
                time.sleep(2)  # Allow some time for new updates to load
            except:
                break  # No more 'Load more updates' button

        # Extract all service update lines
        updates = driver.find_elements(By.CSS_SELECTOR, ".service-alerts-list .service-alert")
        updates_text = [update.text for update in updates]
        return updates_text

    except Exception as e:
        return ["GO Transit - Service status unavailable"]
    finally:
        driver.quit()

if __name__ == "__main__":
    updates = get_go_transit_updates()
    for i, update in enumerate(updates, 1):
        print(f"Update {i}:")
        print(update)
        print("-" * 40)
