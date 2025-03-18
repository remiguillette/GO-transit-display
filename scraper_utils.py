
import logging
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json

logger = logging.getLogger(__name__)

def get_go_transit_updates():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    
    # Add additional headers to avoid detection
    wire_options = {
        'disable_encoding': True,
        'ignore_http_methods': ['OPTIONS', 'HEAD'],
        'request_interceptor': lambda req: req.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
    }
    
    # Configure Selenium Wire to capture network requests
    wire_options = {
        'disable_encoding': True,
        'ignore_http_methods': ['OPTIONS', 'HEAD']
    }
    
    driver = None
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            driver = webdriver.Chrome(
                options=options,
                seleniumwire_options=wire_options
            )
            driver.set_page_load_timeout(30)
            
            # Add random delay between 2-5 seconds
            time.sleep(2 + random.random() * 3)
        
        # Visit the page
        url = "https://www.gotransit.com/en/service-updates/service-updates"
        driver.get(url)
        
        # Wait for the content to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "service-updates")))
        
        # Look for API responses in captured requests
        updates = []
        for request in driver.requests:
            if request.response and "/api/service-updates" in request.url:
                data = json.loads(request.response.body.decode('utf-8'))
                if isinstance(data, list):
                    for update in data:
                        if 'message' in update:
                            updates.append(update['message'])
        
        # If no API data found, try scraping visible content
        if not updates:
            elements = driver.find_elements(By.CLASS_NAME, "service-alert")
            updates = [elem.text for elem in elements if elem.text.strip()]
        
        return updates if updates else ["GO Transit - All services operating normally"]

    except Exception as e:
        logger.error(f"Error fetching updates: {str(e)}")
        return ["GO Transit - All services operating normally"]
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
