import asyncio
from playwright.async_api import async_playwright
import json
import pandas as pd

username='YOUR_BRIGHTDATA_USERNAME'
password='YOUR_BRIGHTDATA_PASSWORD'
auth=f'{username}:{password}'
host = 'YOUR_BRIGHTDATA_HOST'
browser_url = f'wss://{auth}@{host}'

async def main():
    async with async_playwright() as pw:
        print('Connecting to a remote browser...')
        browser = await pw.chromium.connect_over_cdp(browser_url)
        print('Connected. Opening new page...')
        page = await browser.new_page()
        print('Navigating to Zillow...')
        await page.goto('https://www.zillow.com/homes/for_sale/San-Francisco_rb/', timeout=3600000)
        print('Scraping data...')
        listings = []
        properties = await page.query_selector_all('div.property-card-data')
        for property in properties:
            result = {}
            address = await property.query_selector('address[data-test="property-card-addr"]')
            result['address'] = await address.inner_text() if address else ''
            price = await property.query_selector('span[data-test="property-card-price"]')
            result['price'] = await price.inner_text() if price else ''
            details = await property.query_selector_all('ul.dmDolk > li')
            result['bedrooms'] = await details[0].inner_text() if len(details) >= 1 else ''
            result['bathrooms'] = await details[1].inner_text() if len(details) >= 2 else ''
            result['sqft'] = await details[2].inner_text() if len(details) >= 3 else ''
            type_div = await property.query_selector('div.gxlfal')
            result['type'] = (await type_div.inner_text()).split("-")[1].strip() if type_div else ''
            listings.append(result)
        await browser.close()
        return listings

# Run the asynchronous function
listings = asyncio.run(main()) 

# Print the listings
for listing in listings:
    print(listing)

# Write data to Json file
with open('listings-brightdata.json', 'w') as f:
    json.dump(listings, f)
print('Data written to Json file')

# Write data to csv
df = pd.DataFrame(listings)
df.to_csv('listings-brightdata.csv', index=False)
print('Data written to CSV file')