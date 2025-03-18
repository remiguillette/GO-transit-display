
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_go_transit_updates():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(20)
        
        url = "https://www.gotransit.com/en/service-updates/service-updates"
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        view_updates_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='View Updates']")))
        view_updates_button.click()
        
        # Keep clicking 'Load more updates' until all updates are loaded
        while True:
            try:
                load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Load more updates']")))
                load_more_button.click()
                time.sleep(2)
            except:
                break

        updates = driver.find_elements(By.CSS_SELECTOR, ".service-alerts-list .service-alert")
        updates_text = [update.text for update in updates]
        return updates_text if updates_text else ["GO Transit - All services operating normally"]

    except Exception as e:
        print(f"Error fetching updates: {str(e)}")
        return ["GO Transit - Service status unavailable"]
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    updates = get_go_transit_updates()
    for i, update in enumerate(updates, 1):
        print(f"Update {i}:")
        print(update)
