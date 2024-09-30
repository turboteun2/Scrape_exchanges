import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Function to scrape exchange rate for a specific date
def scrape_exchange_rate_by_date(base_currency, target_currency, date):
    date_str = date.strftime('%Y-%m-%d')
    url = f'https://www.x-rates.com/historical/?from={base_currency}&amount=1&date={date_str}'
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', attrs={'class': 'ratesTable'})
        
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cells = row.find_all('td')
                if len(cells) > 1 and target_currency in cells[0].text:
                    rate = cells[1].text.strip()
                    return float(rate)
    return None

# Define the base currency, target currency, and date range
base_currency = 'EUR'
# Change US Dollar if necessary
target_currency = 'US Dollar'
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)  # Adjust the end date as needed

# Prepare a list to store the data
data = []

# Loop over each date in the range
current_date = start_date
while current_date <= end_date:
    rate = scrape_exchange_rate_by_date(base_currency, target_currency, current_date)
    if rate:
        data.append({'Date': current_date.strftime('%Y-%m-%d'), 'Exchange Rate': rate})
        print(f'{current_date.strftime("%Y-%m-%d")}: {rate}')
    else:
        print(f'No data for {current_date.strftime("%Y-%m-%d")}')
    
    current_date += timedelta(days=1)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = '2024-exchange_rates_eur_usd.xlsx'
df.to_excel(output_file, index=False)

print(f'Data successfully saved to {output_file}')
