import pandas as pd
import numpy as np
import os
from datetime import datetime

def clean_car_prices_data(input_path, output_path):
    print("=" * 60)
    print("STARTING DATA CLEANING PROCESS")
    print("=" * 60)

    # 1. LOAD DATA
    if not os.path.exists(input_path):
        print(f"ERROR: File not found at {input_path}")
        return

    df = pd.read_csv(input_path, on_bad_lines='skip')
    initial_rows = df.shape[0]
    print(f"Dataset loaded. Initial Shape: {df.shape}")

    # 2. CLEAN VINs
    df = df.dropna(subset=['vin'])
    df = df[df['vin'].str.len() == 17]
    df = df.drop_duplicates(subset=['vin'], keep='first')

    # 3. CLEAN PRICES
    df = df.dropna(subset=['sellingprice'])
    df = df[df['sellingprice'] >= 500] # Removing suspicious lows

    # 4. STANDARDIZE TEXT
    text_columns = ['make', 'model', 'trim', 'body', 'transmission', 'color', 'interior']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    # 5. ODOMETER
    df = df.dropna(subset=['odometer'])
    df = df[(df['odometer'] > 0) & (df['odometer'] <= 500000)]

    # 6. DATE PARSING
    def parse_saledate(date_str):
        try:
            clean_date = str(date_str).split(' GMT')[0]
            return pd.to_datetime(clean_date)
        except:
            return pd.NaT

    df['saledate'] = df['saledate'].apply(parse_saledate)
    df = df.dropna(subset=['saledate'])

    # 7. FINAL TYPES
    df['year'] = df['year'].astype(int)
    df['sellingprice'] = df['sellingprice'].astype(int)

    # SAVE DATA
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"CLEANING COMPLETE. Final Rows: {df.shape[0]} ({initial_rows - df.shape[0]} removed).")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    # Using relative paths based on your new structure
    RAW_DATA = os.path.join("data", "raw", "car_prices.csv")
    PROCESSED_DATA = os.path.join("data", "processed", "car_prices_cleaned.csv")
    
    clean_car_prices_data(RAW_DATA, PROCESSED_DATA) 