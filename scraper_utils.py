import logging
import json
import asyncio
from playwright.async_api import async_playwright
import time
import random

logger = logging.getLogger(__name__)

async def get_go_transit_updates():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )

        page = await context.new_page()

        try:
            await page.goto("https://www.gotransit.com/en/service-updates/service-updates", wait_until='networkidle')
            await page.wait_for_load_state('domcontentloaded')

            # Wait for content to load
            await page.wait_for_selector('.service-updates', timeout=10000)

            # Extract updates from the page
            updates = await page.evaluate('''() => {
                const elements = document.querySelectorAll('.service-alert');
                return Array.from(elements).map(el => el.textContent.trim());
            }''')

            # If no visible updates found, check network requests
            if not updates:
                await page.wait_for_response(lambda response: '/api/service-updates' in response.url)
                responses = await page.evaluate('''() => {
                    return window.performance.getEntries()
                        .filter(entry => entry.name.includes('/api/service-updates'))
                        .map(entry => entry.name);
                }''')

                for response_url in responses:
                    response = await page.goto(response_url)
                    if response.ok():
                        data = await response.json()
                        if isinstance(data, list):
                            updates.extend([update['message'] for update in data if 'message' in update])

            return updates if updates else ["GO Transit - All services operating normally"]

        except Exception as e:
            logger.error(f"Error fetching updates: {str(e)}")
            return ["GO Transit - All services operating normally"]

        finally:
            await browser.close()

def get_updates():
    return asyncio.run(get_go_transit_updates())