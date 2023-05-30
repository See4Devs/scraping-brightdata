import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://www.zillow.com/homes/for_sale/San-Francisco_rb/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

listings = []

for listing in soup.find_all('div', {'class': 'property-card-data'}):
    result = {}
    result['address'] = listing.find('address', {'data-test': 'property-card-addr'}).get_text().strip()
    result['price'] = listing.find('span', {'data-test': 'property-card-price'}).get_text().strip()
    details_list = listing.find('ul', {'class': 'dmDolk'})
    details = details_list.find_all('li') if details_list else []
    result['bedrooms'] = details[0].get_text().strip() if len(details) >= 0 else ''
    result['bathrooms'] = details[1].get_text().strip() if len(details) >= 1 else ''
    result['sqft'] = details[2].get_text().strip() if len(details) >= 2 else ''
    result['type'] =  listing.find('div', {'class': 'gxlfal'}).getText().split("-")[1].strip()
    listings.append(result)

print(listings)

#Write data to Json file
with open('listings.json', 'w') as f:
    json.dump(listings, f)
print('Data written to Json file')

#Write data to csv
df = pd.DataFrame(listings)
df.to_csv('listings.csv', index=False)
print('Data written to CSV file')
