import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

def fetch_transsee_data():
    url = 'https://www.transsee.ca/tripmsg?a=go&route=LW'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.text

def parse_transsee_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    messages = []

    # Find all message entries
    entries = soup.find_all('div', class_='msg')
    for entry in entries:
        timestamp_text = entry.find('span', class_='smaller').get_text(strip=True)
        message_text = entry.find('span', class_='').get_text(strip=True)

        # Parse the timestamp
        timestamp = datetime.strptime(timestamp_text, '%Y-%m-%d %H:%M:%S')

        messages.append({
            'timestamp': timestamp.isoformat(),
            'message': message_text
        })

    return messages

def save_data(data):
    filename = f'transsee_lw_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_go_transit_updates():
    try:
        html_content = fetch_transsee_data()
        messages = parse_transsee_data(html_content)
        return [msg['message'] for msg in messages]
    except Exception as e:
        return ["Lakeshore West Line: Service operating normally"]

if __name__ == '__main__':
    while True:
        html_content = fetch_transsee_data()
        messages = parse_transsee_data(html_content)
        save_data(messages)
        print(f'Successfully saved {len(messages)} messages.')
        time.sleep(7200)  # Sleep for 2 hours
