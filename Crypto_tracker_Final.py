# Cryptocurrency Price Tracker - Final Version
# BCA Project 2026-2027
# Technologies: Python, Pandas, Matplotlib, API, CSV

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

print("--- CRYPTOCURRENCY PRICE TRACKER ---")

# Take user input
crypto = input("Enter cryptocurrency (e.g., bitcoin, ethereum, dogecoin): ").lower().strip()

# API Setup
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": crypto,
    "vs_currencies": "inr,usd",
    "include_market_cap": "true",
    "include_24hr_vol": "true",
    "include_24hr_change": "true"
}

try:
    # Fetch live data
    response = requests.get(url, params=params)
    data = response.json()

    if crypto in data:
        price_inr = data[crypto]['inr']
        price_usd = data[crypto]['usd']
        market_cap = data[crypto]['inr_market_cap']
        volume = data[crypto]['inr_24h_vol']
        change = data[crypto]['inr_24h_change']

        # Display Output
        print(f"\nCryptocurrency: {crypto.upper()}")
        print(f"Price (INR): ₹{price_inr}")
        print(f"Price (USD): ${price_usd}")
        print(f"Market Cap: ₹{market_cap}")
        print(f"24h Volume: ₹{volume}")
        print(f"24h Change: {round(change,2)}%")

        # Save to CSV using Pandas (for report requirement)
        new_data = {
            'Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'Name': [crypto],
            'Price_INR': [price_inr],
            'Price_USD': [price_usd],
            'Market_Cap': [market_cap],
            'Change_24h': [change]
        }

        df_new = pd.DataFrame(new_data)

        if os.path.exists('crypto_history.csv'):
            df_old = pd.read_csv('crypto_history.csv')
            df_final = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_final = df_new

        df_final.to_csv('crypto_history.csv', index=False)
        print("\nData saved to crypto_history.csv using Pandas")

        # Visualization using Matplotlib
        plt.figure(figsize=(8,5))
        plt.bar(['Price INR', '24h Change %'], [price_inr, change], color=['orange','green'])
        plt.title(f'{crypto.upper()} Price Analysis')
        plt.savefig('price_chart.png')
        print("Chart saved as price_chart.png")

    else:
        print("Cryptocurrency not found! Try bitcoin, ethereum, solana")

except Exception as e:
    print(f"Error! Check internet connection. Details: {e}")