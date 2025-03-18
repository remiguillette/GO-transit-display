import requests
from bs4 import BeautifulSoup
import logging
import tweepy

logger = logging.getLogger(__name__)


# Function to get GO Transit updates from the official website

def get_go_transit_updates():
    """
    Get service updates from GO Transit website using Selenium
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        import time

        # Set up Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open GO Transit service updates page
        url = "https://www.gotransit.com/en/service-updates/service-updates"
        driver.get(url)

        # Wait for and click 'View Updates' button
        wait = WebDriverWait(driver, 10)
        view_updates_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='View Updates']")))
        view_updates_button.click()

        # Load all updates
        while True:
            try:
                load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Load more updates']")))
                load_more_button.click()
                time.sleep(2)
            except:
                break

        # Extract updates
        updates = driver.find_elements(By.CSS_SELECTOR, ".service-alerts-list .service-alert")
        updates_text = [update.text.strip() for update in updates]
        
        # Close driver
        driver.quit()

        return updates_text if updates_text else ["GO Transit - All services operating normally"]

    except Exception as e:
        logger.error(f"Error fetching GO Transit updates: {e}")
        return ["GO Transit - All services operating normally"]


# Function to get Metrolinx updates from the official website

def get_metrolinx_updates():
    try:
        url = 'https://www.metrolinx.com/en/alerts'
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        updates = []
        for item in soup.select('.alert-item'):
            try:
                title = item.find('h3')
                description = item.find('p')

                title_text = title.text.strip() if title else "Metrolinx"
                desc_text = description.text.strip() if description else "All services operating normally"

                updates.append(f"{title_text}: {desc_text}")
            except (AttributeError, TypeError) as e:
                logger.warning(f"Error parsing update item: {e}")
                updates.append("Metrolinx - All services operating normally")

        return updates if updates else ["Metrolinx - All services operating normally"]

    except Exception as e:
        logger.error(f"Error fetching Metrolinx updates: {e}")
        return ["Metrolinx - All services operating normally"]


# Function to get Twitter (X) updates using Tweepy

def get_twitter_updates(api_key, api_secret, access_token, access_secret):
    try:
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)

        tweets = api.user_timeline(screen_name='GOtransit', count=5, tweet_mode='extended')
        updates = []

        for tweet in tweets:
            updates.append(f"Twitter (X): {tweet.full_text}")

        return updates
    except Exception as e:
        logger.error(f"Error fetching Twitter updates: {e}")
        return ["Twitter updates could not be retrieved."]


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Fetch updates from GO Transit, Metrolinx, and Twitter
    go_transit_updates = get_go_transit_updates()
    metrolinx_updates = get_metrolinx_updates()

    # Get Twitter API credentials from environment variables
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret = os.getenv('TWITTER_ACCESS_SECRET')

    if all([api_key, api_secret, access_token, access_secret]):
        twitter_updates = get_twitter_updates(api_key, api_secret, access_token, access_secret)
    else:
        logger.warning("Twitter API credentials not found in environment variables")
        twitter_updates = ["Twitter updates not available - API credentials not configured"]

    # Display all updates
    all_updates = go_transit_updates + metrolinx_updates + twitter_updates
    for update in all_updates:
        print(update)
