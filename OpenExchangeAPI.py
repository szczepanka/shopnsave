
# PYTHON API 
# OPEN EXCHANGE RATES

import requests

APP_ID = "5b3f31c22a8a45f1808cc4ba8f93c470"
ENDPOINT = "https://openexchangerates.org/api/latest.json"

# EXAMPLE https://openexchangerates.org/api/latest.json?app_id=YOUR_APP_ID

response = requests.get(f"{ENDPOINT}?app_id={APP_ID}&base=EUR")

print("RESONSE CODE:", response)
print("DATA:\n", response.text)

exchange_rates = response.json()
usd_amount = 1000
gbp_amount = usd_amount * exchange_rates['rates']['GBP']

print("GBP", gbp_amount)