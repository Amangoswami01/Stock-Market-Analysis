import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Step 1: Download Stock Data
def fetch_stock_data(stock_symbol, start_date, end_date):
    stock = yf.download(stock_symbol, start=start_date, end=end_date)
    stock.reset_index(inplace=True)
    return stock

# Fetching Reliance Stock Data
stock_data = fetch_stock_data("RELIANCE.NS", "2023-01-01", "2024-01-01")

# Step 2: Store Data in SQL Database
conn = sqlite3.connect("stock_data.db")
stock_data.to_sql("stocks", conn, if_exists="replace", index=False)

# Step 3: Data Cleaning & Preprocessing
stock_data.fillna(method='ffill', inplace=True)  # Fill missing values

# Step 4: Calculate Moving Averages
stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
stock_data['200_MA'] = stock_data['Close'].rolling(window=200).mean()

# Step 5: Plot Stock Price with Moving Averages
plt.figure(figsize=(12,6))
plt.plot(stock_data['Date'], stock_data['Close'], label='Close Price', color='blue')
plt.plot(stock_data['Date'], stock_data['50_MA'], label='50-Day MA', color='red')
plt.plot(stock_data['Date'], stock_data['200_MA'], label='200-Day MA', color='green')
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.title("Reliance Stock Price with Moving Averages")
plt.legend()
plt.xticks(rotation=45)  # Rotate date labels for better readability
plt.grid(True)  # Add grid for better visualization
plt.show()

# Step 6: SQL Queries for Analysis
query1 = "SELECT Date, Close FROM stocks ORDER BY Close DESC LIMIT 5;"  # Highest Closing Prices
query2 = "SELECT strftime('%Y-%m', Date) AS Month, AVG(Close) AS Avg_Close FROM stocks GROUP BY Month;"  # Monthly Avg Close Price

highest_prices = pd.read_sql(query1, conn)
monthly_avg = pd.read_sql(query2, conn)

print("Top 5 Highest Closing Prices:")
print(highest_prices)
print("\nMonthly Average Closing Prices:")
print(monthly_avg)

conn.close()
