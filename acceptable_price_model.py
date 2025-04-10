import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import glob

def load_all_price_data(file_paths):
    dfs = []
    for path in file_paths:
        df = pd.read_csv(path, delimiter=';')
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

def calculate_acceptable_prices(df):
    acceptable_prices = {}

    for product in df['product'].unique():
        product_df = df[df['product'] == product].sort_values(by='timestamp')
        X = product_df['timestamp'].values.reshape(-1, 1)
        y = product_df['mid_price'].values

        if len(X) < 2:
            acceptable_prices[product] = None
            continue

        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]
        last_price = y[-1]

        # Acceptable price is the last price adjusted by a small movement in the trend direction
        adjustment_factor = 5  # tweak this
        acceptable_price = last_price + slope * adjustment_factor
        #print(f"product:{product}, slope:{slope}")
        acceptable_prices[product] = round(acceptable_price, 2)

    return acceptable_prices

file_paths = [
    'prices_round_1_day_-2.csv',
    'prices_round_1_day_-1.csv',
    'prices_round_1_day_0.csv'
]

# Load and compute
df_all = load_all_price_data(file_paths)
acceptable_prices = calculate_acceptable_prices(df_all)

# Show results
print(acceptable_prices)


# Using linear regression

def calculate_daily_trend_and_acceptable_prices(df):
    # Group by day and product, and take average mid_price
    daily_avg = df.groupby(['day', 'product'])['mid_price'].mean().reset_index()

    acceptable_prices = {}

    for product in daily_avg['product'].unique():
        product_df = daily_avg[daily_avg['product'] == product].sort_values(by='day')
        X = product_df['day'].values.reshape(-1, 1)
        y = product_df['mid_price'].values

        if len(X) < 2:
            acceptable_prices[product] = None
            continue

        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]
        last_price = y[-1]

        # Adjust by daily trend slope (e.g., extrapolate one day forward)
        acceptable_price = last_price + slope * 1  # *1 for next day forecast

        acceptable_prices[product] = {
            'acceptable_price': round(acceptable_price, 2),
            'trend_per_day': round(slope, 2)
        }

    return acceptable_prices

acceptable_prices = calculate_daily_trend_and_acceptable_prices(df_all)
print(acceptable_prices)
