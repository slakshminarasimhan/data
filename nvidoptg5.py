import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# Define the ticker symbol for NVIDIA
symbol = 'NVDA'

# Fetch the stock data for NVIDIA
nvidia = yf.Ticker(symbol)

# Get the available option expiration dates
expirations = nvidia.options

# Filter expiration dates for the past 5 years
five_years_ago = datetime.now() - timedelta(days=5*365)
expirations_filtered = [date for date in expirations if datetime.strptime(date, "%Y-%m-%d") > five_years_ago]

# Initialize empty lists for calls and puts
all_calls = []
all_puts = []

# Fetching data for each expiration date and appending to the lists
for exp_date in expirations_filtered:
    try:
        # Get option chain for the chosen expiration date
        option_chain = nvidia.option_chain(exp_date)
        
        # Get calls and puts and add the expiration date as a column
        calls = option_chain.calls
        calls['expirationDate'] = exp_date
        all_calls.append(calls)
        
        puts = option_chain.puts
        puts['expirationDate'] = exp_date
        all_puts.append(puts)
        
        print(f"Option data for {symbol} on {exp_date} has been fetched.")
    except Exception as e:
        print(f"Error fetching data for {symbol} on {exp_date}: {e}")

# Concatenate all calls and puts into single DataFrames
if all_calls:
    calls_df = pd.concat(all_calls, ignore_index=True)
else:
    calls_df = pd.DataFrame()

if all_puts:
    puts_df = pd.concat(all_puts, ignore_index=True)
else:
    puts_df = pd.DataFrame()

# Create a directory to store the CSV files if it doesn't exist
output_directory = "nvidia_options_data"
os.makedirs(output_directory, exist_ok=True)

# Save the consolidated data to CSV files
calls_df.to_csv(os.path.join(output_directory, f'{symbol}_calls_all.csv'), index=False)
puts_df.to_csv(os.path.join(output_directory, f'{symbol}_puts_all.csv'), index=False)

print(f"Consolidated call options data has been saved to {symbol}_calls_all.csv")
print(f"Consolidated put options data has been saved to {symbol}_puts_all.csv")
